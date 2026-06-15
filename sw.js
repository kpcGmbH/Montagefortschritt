// KPC Montagefortschritt – Service Worker
// Cacht die App-Shell + CDN-Bibliotheken (cache-first), damit die App offline startet.
// Microsoft Graph / Login / SharePoint werden NIE gecacht (network-only) – Daten und
// Tokens laufen ausschließlich live. Bei jeder Veröffentlichung CACHE-Version erhöhen.
const CACHE = 'kpc-montage-v18';

const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js',
  'https://cdn.jsdelivr.net/npm/@azure/msal-browser@2.38.4/lib/msal-browser.min.js',
  'https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js'
];

// Hosts, deren GET-Antworten gecacht werden dürfen (Bibliotheken + CD-Schriften).
const CACHE_HOSTS = ['cdnjs.cloudflare.com', 'cdn.jsdelivr.net', 'fonts.googleapis.com', 'fonts.gstatic.com'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    // Einzeln cachen + Fehler tolerieren, damit ein einzelner CDN-Ausfall die
    // Installation nicht komplett scheitern lässt.
    await Promise.all(SHELL.map(u => c.add(u).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') self.skipWaiting();
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;                 // Uploads/PATCH/DELETE nie abfangen
  let url;
  try { url = new URL(req.url); } catch (_) { return; }

  const sameOrigin = url.origin === self.location.origin;
  const isCDN = CACHE_HOSTS.includes(url.hostname);

  // Graph, Login, SharePoint-Downloads etc. -> network-only, NICHT abfangen.
  if (!sameOrigin && !isCDN) return;

  // App-Shell-Navigation: network-first (immer neueste index.html online),
  // bei fehlendem Netz aus dem Cache.
  if (sameOrigin && req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const net = await fetch(req);
        const c = await caches.open(CACHE);
        c.put('./index.html', net.clone());
        return net;
      } catch (_) {
        const cached = await caches.match('./index.html') || await caches.match('./');
        return cached || new Response('Offline – App-Shell nicht im Cache.', {status: 503});
      }
    })());
    return;
  }

  // CDN-Bibliotheken + sonstige same-origin GETs: cache-first.
  e.respondWith((async () => {
    const cached = await caches.match(req);
    if (cached) return cached;
    try {
      const net = await fetch(req);
      if (net && net.ok) {
        const c = await caches.open(CACHE);
        c.put(req, net.clone());
      }
      return net;
    } catch (_) {
      return cached || new Response('Offline', {status: 503});
    }
  })());
});
