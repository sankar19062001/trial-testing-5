"""
diagrams.py  —  SVG diagram library for SIMODRIVE 611
======================================================
Each function returns a complete SVG string.
Add more diagrams here as you need them.
The bot triggers these by returning [DIAGRAM:key] in its text.
server.py intercepts the tag and appends the SVG to the response.
"""

def get_diagram(key: str) -> str | None:
    """Return SVG string for the given diagram key, or None if not found."""
    diagrams = {
        "encoder_cable":    encoder_cable(),
        "motor_contactor":  motor_contactor(),
        "dc_link":          dc_link(),
        "cable_routing":    cable_routing(),
        "fault_reset":      fault_reset(),
        "drive_leds":       drive_leds(),
    }
    return diagrams.get(key.lower().strip())


def encoder_cable() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 200" style="width:100%;max-width:520px;font-family:sans-serif">
  <rect width="520" height="200" fill="#f8f9fa" rx="10" stroke="#dee2e6" stroke-width="1"/>
  <text x="260" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#003366">Encoder cable routing — SIMODRIVE 611</text>

  <!-- Motor -->
  <rect x="20" y="60" width="110" height="80" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="75" y="96" text-anchor="middle" font-size="12" font-weight="600" fill="#0d47a1">Motor</text>
  <text x="75" y="113" text-anchor="middle" font-size="10" fill="#1565c0">Encoder at rear</text>

  <!-- Encoder connector on motor -->
  <rect x="128" y="88" width="18" height="24" rx="3" fill="#ff8f00" stroke="#e65100" stroke-width="1"/>
  <text x="137" y="83" text-anchor="middle" font-size="9" fill="#bf360c">Connector A</text>
  <text x="137" y="118" text-anchor="middle" font-size="9" fill="#bf360c">must click shut</text>

  <!-- Cable -->
  <line x1="146" y1="100" x2="220" y2="100" stroke="#555" stroke-width="3" stroke-dasharray="6 3"/>
  <text x="183" y="93" text-anchor="middle" font-size="9" fill="#333">thin cable</text>
  <text x="183" y="116" text-anchor="middle" font-size="9" fill="#c62828">check for pinch</text>

  <!-- Drag chain -->
  <rect x="220" y="76" width="80" height="48" rx="6" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="260" y="98" text-anchor="middle" font-size="11" font-weight="600" fill="#6a1b9a">Drag chain</text>
  <text x="260" y="114" text-anchor="middle" font-size="9" fill="#7b1fa2">inspect for damage</text>

  <!-- Cable continues -->
  <line x1="300" y1="100" x2="370" y2="100" stroke="#555" stroke-width="3" stroke-dasharray="6 3"/>

  <!-- Drive cabinet connector -->
  <rect x="368" y="88" width="18" height="24" rx="3" fill="#ff8f00" stroke="#e65100" stroke-width="1"/>
  <text x="377" y="83" text-anchor="middle" font-size="9" fill="#bf360c">Connector B</text>

  <!-- Drive cabinet -->
  <rect x="384" y="50" width="110" height="100" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="439" y="92" text-anchor="middle" font-size="12" font-weight="600" fill="#1b5e20">Drive</text>
  <text x="439" y="108" text-anchor="middle" font-size="10" fill="#2e7d32">SIMODRIVE 611</text>
  <text x="439" y="124" text-anchor="middle" font-size="10" fill="#2e7d32">cabinet</text>

  <!-- Check arrows -->
  <text x="137" y="155" text-anchor="middle" font-size="10" fill="#c62828">1. Check A</text>
  <text x="260" y="155" text-anchor="middle" font-size="10" fill="#7b1fa2">2. Check chain</text>
  <text x="377" y="155" text-anchor="middle" font-size="10" fill="#c62828">3. Check B</text>

  <!-- Legend -->
  <line x1="20" y1="180" x2="50" y2="180" stroke="#555" stroke-width="3" stroke-dasharray="6 3"/>
  <text x="56" y="184" font-size="10" fill="#333">Encoder cable (thin)</text>
  <rect x="240" y="173" width="14" height="14" fill="#ff8f00" stroke="#e65100" rx="2"/>
  <text x="260" y="184" font-size="10" fill="#333">Connector — check locked</text>
</svg>"""


def motor_contactor() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 220" style="width:100%;max-width:440px;font-family:sans-serif">
  <rect width="440" height="220" fill="#f8f9fa" rx="10" stroke="#dee2e6" stroke-width="1"/>
  <text x="220" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#003366">Motor contactor — what to check</text>

  <!-- Cabinet outline -->
  <rect x="60" y="40" width="320" height="150" rx="10" fill="#fff" stroke="#90a4ae" stroke-width="1.5" stroke-dasharray="6 3"/>
  <text x="220" y="58" text-anchor="middle" font-size="10" fill="#607d8b">Inside drive cabinet — engineer access only</text>

  <!-- Contactor body -->
  <rect x="150" y="70" width="140" height="90" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="220" y="100" text-anchor="middle" font-size="12" font-weight="600" fill="#0d47a1">Motor contactor</text>

  <!-- Contacts top -->
  <rect x="170" y="58" width="20" height="16" rx="3" fill="#ffd54f" stroke="#f57f17" stroke-width="1"/>
  <rect x="210" y="58" width="20" height="16" rx="3" fill="#ffd54f" stroke="#f57f17" stroke-width="1"/>
  <rect x="250" y="58" width="20" height="16" rx="3" fill="#ffd54f" stroke="#f57f17" stroke-width="1"/>
  <text x="220" y="52" text-anchor="middle" font-size="9" fill="#e65100">3-phase power in</text>

  <!-- Contacts bottom -->
  <rect x="170" y="156" width="20" height="16" rx="3" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1"/>
  <rect x="210" y="156" width="20" height="16" rx="3" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1"/>
  <rect x="250" y="156" width="20" height="16" rx="3" fill="#a5d6a7" stroke="#2e7d32" stroke-width="1"/>
  <text x="220" y="185" text-anchor="middle" font-size="9" fill="#2e7d32">to motor</text>

  <!-- Status indicator -->
  <circle cx="300" cy="110" r="14" fill="#ef5350" stroke="#c62828" stroke-width="1.5"/>
  <text x="300" y="114" text-anchor="middle" font-size="9" fill="white">LED</text>

  <!-- Check labels -->
  <text x="80" y="110" text-anchor="start" font-size="10" fill="#c62828">Check:</text>
  <text x="80" y="126" text-anchor="start" font-size="10" fill="#333">- Fully engaged?</text>
  <text x="80" y="142" text-anchor="start" font-size="10" fill="#333">- Burn marks?</text>
  <text x="80" y="158" text-anchor="start" font-size="10" fill="#333">- Smell of burning?</text>

  <text x="350" y="110" text-anchor="start" font-size="10" fill="#c62828">Red LED =</text>
  <text x="350" y="126" text-anchor="start" font-size="10" fill="#333">fault / trip</text>
  <text x="350" y="142" text-anchor="start" font-size="10" fill="#333">call engineer</text>
</svg>"""


def dc_link() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 180" style="width:100%;max-width:480px;font-family:sans-serif">
  <rect width="480" height="180" fill="#f8f9fa" rx="10" stroke="#dee2e6" stroke-width="1"/>
  <text x="240" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#003366">DC link — voltage and fault relationship</text>

  <!-- Infeed unit -->
  <rect x="20" y="50" width="110" height="80" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="75" y="84" text-anchor="middle" font-size="11" font-weight="600" fill="#bf360c">Infeed unit</text>
  <text x="75" y="100" text-anchor="middle" font-size="9" fill="#e65100">converts AC to DC</text>
  <text x="75" y="116" text-anchor="middle" font-size="9" fill="#e65100">check LEDs here</text>

  <!-- DC bus -->
  <line x1="130" y1="90" x2="350" y2="90" stroke="#f57f17" stroke-width="4"/>
  <text x="240" y="82" text-anchor="middle" font-size="10" font-weight="600" fill="#e65100">DC link bus  (~540–700V)</text>

  <!-- Drive axis 1 -->
  <rect x="350" y="50" width="50" height="80" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="375" y="86" text-anchor="middle" font-size="9" font-weight="600" fill="#0d47a1">Axis 1</text>
  <text x="375" y="100" text-anchor="middle" font-size="8" fill="#1565c0">drive</text>

  <!-- Drive axis 2 -->
  <rect x="410" y="50" width="50" height="80" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="435" y="86" text-anchor="middle" font-size="9" font-weight="600" fill="#0d47a1">Axis 2</text>
  <text x="435" y="100" text-anchor="middle" font-size="8" fill="#1565c0">drive</text>

  <!-- Fault indicators -->
  <rect x="20" y="148" width="140" height="22" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="1"/>
  <text x="90" y="163" text-anchor="middle" font-size="10" fill="#c62828">F616 = DC undervoltage</text>

  <rect x="170" y="148" width="140" height="22" rx="4" fill="#fff8e1" stroke="#f57f17" stroke-width="1"/>
  <text x="240" y="163" text-anchor="middle" font-size="10" fill="#e65100">F617 = DC overvoltage</text>

  <rect x="320" y="148" width="140" height="22" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1"/>
  <text x="390" y="163" text-anchor="middle" font-size="10" fill="#2e7d32">Fix: cycle infeed power</text>
</svg>"""


def cable_routing() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 200" style="width:100%;max-width:480px;font-family:sans-serif">
  <rect width="480" height="200" fill="#f8f9fa" rx="10" stroke="#dee2e6" stroke-width="1"/>
  <text x="240" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#003366">Motor cable routing — power cable check</text>

  <!-- Drive cabinet -->
  <rect x="20" y="50" width="110" height="110" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="75" y="84" text-anchor="middle" font-size="11" font-weight="600" fill="#1b5e20">Drive</text>
  <text x="75" y="100" text-anchor="middle" font-size="9" fill="#2e7d32">SIMODRIVE 611</text>

  <!-- Power terminals in cabinet -->
  <rect x="128" y="100" width="22" height="30" rx="3" fill="#ffd54f" stroke="#f57f17" stroke-width="1.5"/>
  <text x="139" y="95" text-anchor="middle" font-size="8" fill="#e65100">U V W</text>

  <!-- Power cable — thick -->
  <line x1="150" y1="115" x2="300" y2="115" stroke="#333" stroke-width="6"/>
  <text x="225" y="108" text-anchor="middle" font-size="9" fill="#333">power cable (thick, 3-core)</text>
  <text x="225" y="138" text-anchor="middle" font-size="9" fill="#c62828">check: no heat damage, no cuts</text>

  <!-- Motor terminal box -->
  <rect x="300" y="96" width="60" height="38" rx="5" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="330" y="114" text-anchor="middle" font-size="9" font-weight="600" fill="#bf360c">Terminal</text>
  <text x="330" y="128" text-anchor="middle" font-size="9" fill="#bf360c">box</text>

  <!-- Motor -->
  <rect x="360" y="60" width="100" height="110" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="410" y="108" text-anchor="middle" font-size="11" font-weight="600" fill="#0d47a1">Motor</text>

  <!-- Check steps -->
  <text x="20" y="178" font-size="10" fill="#333">1. Check cable for heat discolouration</text>
  <text x="20" y="192" font-size="10" fill="#333">2. Engineer checks terminal tightness (torque wrench)</text>
</svg>"""


def fault_reset() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 180" style="width:100%;max-width:400px;font-family:sans-serif">
  <rect width="400" height="180" fill="#f8f9fa" rx="10" stroke="#dee2e6" stroke-width="1"/>
  <text x="200" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#003366">Fault reset procedure</text>

  <!-- Step boxes -->
  <rect x="20" y="40" width="80" height="60" rx="8" fill="#fff3e0" stroke="#e65100" stroke-width="1.5"/>
  <text x="60" y="66" text-anchor="middle" font-size="10" font-weight="600" fill="#bf360c">Step 1</text>
  <text x="60" y="80" text-anchor="middle" font-size="9" fill="#e65100">Press RESET</text>
  <text x="60" y="93" text-anchor="middle" font-size="9" fill="#e65100">FAULT MEM</text>

  <line x1="100" y1="70" x2="120" y2="70" stroke="#555" stroke-width="1.5" marker-end="url(#a)"/>

  <rect x="120" y="40" width="80" height="60" rx="8" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5"/>
  <text x="160" y="66" text-anchor="middle" font-size="10" font-weight="600" fill="#0d47a1">Step 2</text>
  <text x="160" y="80" text-anchor="middle" font-size="9" fill="#1565c0">Wait for</text>
  <text x="160" y="93" text-anchor="middle" font-size="9" fill="#1565c0">LED green</text>

  <line x1="200" y1="70" x2="220" y2="70" stroke="#555" stroke-width="1.5" marker-end="url(#a)"/>

  <rect x="220" y="40" width="80" height="60" rx="8" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1.5"/>
  <text x="260" y="66" text-anchor="middle" font-size="10" font-weight="600" fill="#6a1b9a">Step 3</text>
  <text x="260" y="80" text-anchor="middle" font-size="9" fill="#7b1fa2">MANUAL</text>
  <text x="260" y="93" text-anchor="middle" font-size="9" fill="#7b1fa2">mode, slow jog</text>

  <line x1="300" y1="70" x2="320" y2="70" stroke="#555" stroke-width="1.5" marker-end="url(#a)"/>

  <rect x="320" y="40" width="60" height="60" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <text x="350" y="66" text-anchor="middle" font-size="10" font-weight="600" fill="#1b5e20">Step 4</text>
  <text x="350" y="80" text-anchor="middle" font-size="9" fill="#2e7d32">Run OK?</text>
  <text x="350" y="93" text-anchor="middle" font-size="9" fill="#2e7d32">30 sec test</text>

  <text x="200" y="130" text-anchor="middle" font-size="10" fill="#c62828">If fault returns immediately → do not retry → call engineer</text>
  <text x="200" y="148" text-anchor="middle" font-size="10" fill="#2e7d32">If clears → run production cycle → log in maintenance book</text>
  <text x="200" y="168" text-anchor="middle" font-size="10" fill="#555">Always inform supervisor before handing machine back</text>

  <defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="#555" stroke-width="1.5"/></marker></defs>
</svg>"""


def drive_leds() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 190" style="width:100%;max-width:420px;font-family:sans-serif">
  <rect width="420" height="190" fill="#f8f9fa" rx="10" stroke="#dee2e6" stroke-width="1"/>
  <text x="210" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#003366">Drive LED status guide — SIMODRIVE 611</text>

  <!-- Drive panel -->
  <rect x="20" y="40" width="100" height="130" rx="8" fill="#263238" stroke="#455a64" stroke-width="2"/>
  <text x="70" y="58" text-anchor="middle" font-size="9" fill="#90a4ae">Drive panel</text>
  <circle cx="70" cy="80" r="10" fill="#4caf50"/>
  <circle cx="70" cy="110" r="10" fill="#f44336"/>
  <circle cx="70" cy="140" r="10" fill="#ff9800"/>
  <text x="70" y="165" text-anchor="middle" font-size="8" fill="#78909c">LEDs</text>

  <!-- Status table -->
  <rect x="140" y="44" width="14" height="14" rx="7" fill="#4caf50"/>
  <text x="162" y="55" font-size="11" font-weight="600" fill="#2e7d32">Green steady</text>
  <text x="162" y="70" font-size="10" fill="#333">Drive ready, no fault — normal operation</text>

  <rect x="140" y="84" width="14" height="14" rx="7" fill="#f44336"/>
  <text x="162" y="95" font-size="11" font-weight="600" fill="#c62828">Red steady</text>
  <text x="162" y="110" font-size="10" fill="#333">Active fault — check display for code</text>

  <rect x="140" y="124" width="14" height="14" rx="7" fill="#ff9800"/>
  <text x="162" y="135" font-size="11" font-weight="600" fill="#e65100">Amber flashing</text>
  <text x="162" y="150" font-size="10" fill="#333">Warning — machine running, monitor closely</text>

  <rect x="140" y="157" width="14" height="14" rx="7" fill="#263238" stroke="#90a4ae" stroke-width="1.5"/>
  <text x="162" y="168" font-size="11" font-weight="600" fill="#333">LED off</text>
  <text x="162" y="180" font-size="10" fill="#333">No power to drive — check main supply</text>
</svg>"""


# ── Map keyword triggers from Gemma output to diagram keys ───────────────────
DIAGRAM_TRIGGERS = {
    "encoder_cable":    ["encoder cable", "encoder connector", "encoder plug"],
    "motor_contactor":  ["motor contactor", "contactor", "relay switch"],
    "dc_link":          ["dc link", "dc bus", "fault 616", "fault 617", "undervoltage", "overvoltage"],
    "cable_routing":    ["power cable", "motor cable", "terminal box", "cable routing"],
    "fault_reset":      ["reset fault", "reset procedure", "press reset", "fault memory"],
    "drive_leds":       ["led status", "drive led", "green led", "red led"],
}

def detect_diagram(text: str) -> str | None:
    """
    Scan bot response text for keyword triggers.
    Returns diagram key if found, None if not.
    Also handles explicit [DIAGRAM:key] tags from the model.
    """
    import re
    # Explicit tag from model
    m = re.search(r'\[DIAGRAM:(\w+)\]', text, re.IGNORECASE)
    if m:
        return m.group(1).lower()

    # Keyword matching
    text_lower = text.lower()
    for key, keywords in DIAGRAM_TRIGGERS.items():
        if any(kw in text_lower for kw in keywords):
            return key
    return None
