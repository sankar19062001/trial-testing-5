"""
server.py  —  SIMODRIVE 611 Integrated Diagnostic Platform  v6
==============================================================
Single FastAPI server that handles:
  - Text chat  (POST /ask)
  - Voice lang passthrough (lang= form field)
  - Photo upload / Gemma 4 vision (image= form field)
  - Diagram injection  (diagrams.py library)
  - CORS + PWA static file serving
  - Ticket history (SQLite)

Start:
  uvicorn server:app --host 0.0.0.0 --port 8000 --reload

Operators open Chrome on Android:
  http://<your-laptop-ip>:8000
"""

import base64, json, os, re, sqlite3
from datetime import datetime
from pathlib import Path

import requests
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from diagrams import detect_diagram, get_diagram

# ── Config ────────────────────────────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma4:e2b"
FAULT_JSON   = r"C:\Users\DELL\Documents\Ashokleyland SIP\trial testing 5\simodrive_611_fault_codes.json"
DB_PATH      = "maintenance.db"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# ── Load fault codes ──────────────────────────────────────────────────────────
def load_faults(path: str):
    if not Path(path).exists():
        print(f"WARNING: {path} not found"); return "", {}
    data   = json.load(open(path, encoding="utf-8"))
    lookup = {}
    lines  = ["=== SIMODRIVE 611 — 290 FAULT CODES (Chapter 7, extracted from SOP manual) ===\n"]
    for f in data:
        for k in [f["code"], f["code"].lstrip("0") or "0", f["code"].zfill(3)]:
            lookup[k] = f
        lines.append(
            f"[F{f['code']}] {f['name']}\n"
            f"  Cause  : {f['cause']}\n"
            f"  Remedy : {f['remedy']}\n"
            f"  Reset  : {f['acknowledgement']}  |  Stop: {f['stop_response']}\n"
        )
    block = "\n".join(lines)
    print(f"Faults loaded: {len(data)} | ~{int(len(block.split())/0.75):,} tokens")
    return block, lookup

FAULT_BLOCK, FAULT_LOOKUP = load_faults(FAULT_JSON)

# ── Language helpers ──────────────────────────────────────────────────────────
def lang_rule(code: str) -> str:
    if code.startswith("ta"):
        return ("LANGUAGE: Operator is speaking Tamil. "
                "You MUST reply entirely in Tamil (தமிழ்). "
                "Only keep fault codes and parameter names in English.")
    if code.startswith("hi"):
        return ("LANGUAGE: Operator is speaking Hindi. "
                "You MUST reply entirely in Hindi (हिन्दी). "
                "Only keep fault codes and parameter names in English.")
    return "LANGUAGE: Reply in clear simple English."

DIAGRAM_KEYS = ("encoder_cable", "motor_contactor", "dc_link",
                "cable_routing", "fault_reset", "drive_leds")

# ── System prompt ─────────────────────────────────────────────────────────────
def build_prompt(lang: str = "en-IN") -> str:
    return f"""You are an expert diagnostic engineer for SIMODRIVE 611 industrial drives.
Think like a detective. Guide the operator to find and fix the fault.

{lang_rule(lang)}

RULES:
1. Think before responding — what symptoms, what fault, what ONE best next question?
2. Ask ONE question per response. Never two.
3. Build on what the operator told you. Never repeat a completed check.
4. Simple plain language — operator is unskilled.
5. Visual / cable checks first (operator safe). Cabinet internals = engineer only.
6. When confident: name the fault, give numbered fix steps.
7. After fix: tell operator to press RESET FAULT MEMORY, confirm machine runs.

DIAGNOSTIC ORDER:
  1. What does the display show? (fault code)
  2. Any other codes alongside?
  3. What was happening when it stopped?
  4. Visual check — jam, blockage, loose connectors
  5. Cable check — encoder cable, power cable
  6. Parameter check via SimoCom U
  7. Escalate if unresolved

SAFETY:
  - Never ask operator to open the drive cabinet
  - Never ask operator to touch live terminals
  - Always: "confirm machine is in MANUAL mode before any physical check"

DIAGRAMS — when a physical check would benefit from a visual, add ONE tag on its own line:
  [DIAGRAM:encoder_cable]   — encoder cable routing check
  [DIAGRAM:motor_contactor] — contactor check
  [DIAGRAM:dc_link]         — DC link / F616 / F617
  [DIAGRAM:cable_routing]   — power cable / terminal box
  [DIAGRAM:fault_reset]     — reset procedure steps
  [DIAGRAM:drive_leds]      — LED status meaning
Only ONE diagram per response. Only when it genuinely helps.

IMAGE INPUT: If the operator sends a photo of the display or a cable, describe exactly
what you see (fault code, LED colour, cable condition) and use it to diagnose.

=== SOP MANUAL — CHAPTER 7 FAULT CODES ===
{FAULT_BLOCK}
=== END OF FAULT KNOWLEDGE ===

You are not a search engine. Think → Ask one question → Listen → Guide."""

# ── SQLite ────────────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT, fault_code TEXT, lang TEXT,
        start_time TEXT, end_time TEXT,
        status TEXT DEFAULT 'Open', resolution TEXT, turns INTEGER DEFAULT 0
    )""")
    conn.commit(); conn.close()

init_db()

def db_open(issue, code=None, lang="en-IN"):
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.execute(
        "INSERT INTO tickets (issue,fault_code,lang,start_time,status) VALUES (?,?,?,?,?)",
        (issue, code, lang, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Open"))
    tid = cur.lastrowid; conn.commit(); conn.close(); return tid

def db_close(tid, res="Resolved"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE tickets SET end_time=?,status=?,resolution=? WHERE id=?",
                 (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Closed", res, tid))
    conn.commit(); conn.close()

def db_tick(tid):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE tickets SET turns=turns+1 WHERE id=?", (tid,))
    conn.commit(); conn.close()

# ── Sessions ──────────────────────────────────────────────────────────────────
sessions: dict[int, dict] = {}

def get_session(tid: int, lang: str = "en-IN") -> dict:
    if tid not in sessions:
        sessions[tid] = {
            "messages": [{"role": "system", "content": build_prompt(lang)}],
            "lang": lang,
        }
    return sessions[tid]

# ── Gemma ─────────────────────────────────────────────────────────────────────
def call_gemma(messages: list, image_b64: str = None) -> str:
    msgs = [dict(m) for m in messages]
    if image_b64:
        for m in reversed(msgs):
            if m["role"] == "user":
                m["images"] = [image_b64]; break
    payload = {
        "model": OLLAMA_MODEL, "messages": msgs, "stream": False,
        "options": {"temperature": 0.15, "num_predict": 800, "repeat_penalty": 1.1},
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=180)
        r.raise_for_status()
        reply = r.json()["message"]["content"].strip()
        reply = re.sub(r"<think>.*?</think>", "", reply, flags=re.DOTALL).strip()
        return reply or "Can you describe what you see on the display?"
    except requests.exceptions.ConnectionError:
        return "Cannot reach Ollama. Please run: ollama serve"
    except Exception as e:
        return f"Error: {e}"

def inject_diagram(text: str):
    key  = detect_diagram(text)
    svg  = get_diagram(key) if key else None
    clean = re.sub(r"\[DIAGRAM:[^\]]+\]", "", text).strip()
    return clean, svg

def extract_code(text: str):
    m = re.search(r"\b(\d{3})\b", text)
    if m: return m.group(1)
    m = re.search(r"\b(\d{2})\b", text)
    if m: return m.group(1).zfill(3)
    return None

# ── /ask ──────────────────────────────────────────────────────────────────────
@app.post("/ask")
async def ask(
    query:     str        = Form(...),
    ticket_id: str        = Form("None"),
    lang:      str        = Form("en-IN"),
    image:     UploadFile = File(None),
):
    query = query.strip()
    if not query:
        return {"answer": "Please describe the problem.", "ticket_id": None}

    code = extract_code(query)
    tid  = (db_open(query, code, lang)
            if ticket_id in ("None", "", None)
            else int(ticket_id))

    sess = get_session(tid, lang)
    if lang != sess["lang"] and lang not in ("en-IN", "en"):
        sess["lang"] = lang
        sess["messages"][0] = {"role": "system", "content": build_prompt(lang)}

    image_b64 = None
    if image and image.filename:
        image_b64 = base64.b64encode(await image.read()).decode()

    sess["messages"].append({"role": "user", "content": query})
    raw = call_gemma(sess["messages"], image_b64)
    clean, svg = inject_diagram(raw)
    sess["messages"].append({"role": "assistant", "content": clean})

    if len(sess["messages"]) > 42:
        sess["messages"][1:] = sess["messages"][-40:]

    db_tick(tid)
    resolved = any(w in clean.lower() for w in
                   ["fault cleared", "running normally", "resolved",
                    "சரிசெய்யப்பட்டது", "ठीक हो गई"])
    escalate = any(w in clean.lower() for w in
                   ["call the engineer", "engineer required",
                    "இன்ஜினியர்", "इंजीनियर"])
    if resolved: db_close(tid, "Resolved")
    elif escalate: db_close(tid, "Escalated")

    return {"answer": clean, "svg": svg, "lang": lang,
            "ticket_id": tid, "resolved": resolved, "escalate": escalate}

# ── /resolve / /health / /tickets ────────────────────────────────────────────
@app.post("/resolve")
def resolve(ticket_id: int):
    db_close(ticket_id, "Closed by operator")
    sessions.pop(ticket_id, None)
    return {"status": "closed"}

@app.get("/health")
def health():
    try:
        r  = requests.get("http://localhost:11434/api/tags", timeout=3)
        ms = [m["name"] for m in r.json().get("models", [])]
        ok = any(OLLAMA_MODEL in m for m in ms)
    except Exception:
        ok = False
    return {"status": "ok",
            "ollama": "connected" if ok else "not reachable — run: ollama serve",
            "model":  OLLAMA_MODEL,
            "faults": len(FAULT_LOOKUP) // 3,
            "source": "Chapter 7 — SIMODRIVE 611 SOP manual"}

@app.get("/tickets")
def get_tickets():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id,issue,fault_code,lang,start_time,status,turns "
        "FROM tickets ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return {"tickets": [
        {"id": r[0], "issue": r[1], "fault_code": r[2], "lang": r[3],
         "start": r[4], "status": r[5], "turns": r[6]} for r in rows]}

# ── Serve PWA ──────────────────────────────────────────────────────────────────
if Path("static").exists():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
