// KPC Montagefortschritt – Service Worker
// Cacht die App-Shell + CDN-Bibliotheken (cache-first), damit die App offline startet.
// Microsoft Graph / Login / SharePoint werden NIE gecacht (network-only) – Daten und
// Tokens laufen ausschließlich live. Bei jeder Veröffentlichung CACHE-Version erhöhen.
const CACHE = 'kpc-montage-v189';

const SHELL = [
  './',
  './index.html',
  // Die Einweisung arbeitet seit v135 offline (eigene Warteschlange). Damit sie
  // das auch beim ERSTEN Aufruf ohne Netz kann, wird sie mit vorgeladen – sonst
  // läge sie erst nach einem Besuch mit Verbindung im Zwischenspeicher.
  './einweisung.html',
  // Ab v157 auch die Protokoll-App (IBN/DGUV), Kundendienst und Servicebericht:
  // vorher lagen sie erst nach einem Aufruf MIT Netz im Speicher und wurden bei
  // jedem Update wieder verworfen – offline hieß es dann „Seite nicht im Cache".
  './inbetriebnahme.html',
  './kundendienst.html',
  './servicebericht.html',
  './manifest.webmanifest',
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js',
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

  // Navigation same-origin: network-first (immer die neueste Seite online),
  // bei fehlendem Netz aus dem Cache.
  // WICHTIG: Nur die Hauptapp ist die App-Shell. Die Nebenseiten (einweisung.html,
  // inbetriebnahme.html) werden unter IHRER eigenen URL abgelegt – lägen sie unter
  // './index.html', zeigte die Hauptapp offline die zuletzt geöffnete Nebenseite.
  if (sameOrigin && req.mode === 'navigate') {
    const isShell = url.pathname.endsWith('/') || /\/index\.html$/.test(url.pathname);
    const ausCache = async () => isShell
      ? (await caches.match('./index.html') || await caches.match('./'))
      : (await caches.match(req.url, {ignoreSearch: true}));
    e.respondWith((async () => {
      // no-cache: immer beim Server revalidieren -> beim Öffnen sofort die neue Ansicht
      const netz = fetch(req.url, {cache: 'no-cache'}).then(async net => {
        if (net && net.ok) { const c = await caches.open(CACHE); await c.put(isShell ? './index.html' : req.url, net.clone()); }
        return net;
      });
      // Schwaches Netz (Balken, aber keine Daten): nach 4 s die gespeicherte Seite
      // zeigen statt minutenlang weiß. Die Netzantwort aktualisiert den Speicher
      // trotzdem im Hintergrund (v157).
      const zeit = new Promise(r => setTimeout(() => r('zeit'), 4000));
      try {
        const erst = await Promise.race([netz, zeit]);
        if (erst !== 'zeit') return erst;
        const cached = await ausCache();
        if (cached) { e.waitUntil(netz.catch(() => {})); return cached; }
        return await netz;
      } catch (_) {
        const cached = await ausCache();
        return cached || new Response('Offline – Seite nicht im Cache.', {status: 503});
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
