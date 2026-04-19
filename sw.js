// sw.js  —  Service Worker for SIMODRIVE 611 PWA
// Caches the UI shell so it loads even when the plant server is unreachable.
// API calls (/ask, /health) are NEVER cached — always go live to the server.

const CACHE   = 'simodrive-v1';
const SHELL   = ['/', '/index.html', '/manifest.json'];

// ── Install: cache the UI shell immediately ───────────────────────────────────
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

// ── Activate: clean up old caches ─────────────────────────────────────────────
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: serve shell from cache, API always live ───────────────────────────
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // API calls — always go to the live server, never cache
  if (url.pathname.startsWith('/ask') ||
      url.pathname.startsWith('/health') ||
      url.pathname.startsWith('/resolve') ||
      url.pathname.startsWith('/tickets')) {
    e.respondWith(fetch(e.request));
    return;
  }

  // Shell files — cache first, fallback to network
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(response => {
        // Cache new shell resources as they are loaded
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return response;
      }).catch(() => {
        // Offline and not cached — return the main page
        return caches.match('/index.html');
      });
    })
  );
});
