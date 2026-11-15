/* Alterna tema claro/escuro e grava a preferência no cookie pt_tema. */
(function () {
  var raiz = document.documentElement;
  var btn = document.getElementById('btn-tema');

  function atual() {
    return raiz.getAttribute('data-tema') === 'escuro' ? 'escuro' : 'claro';
  }

  function pinta(tema) {
    raiz.setAttribute('data-tema', tema);
    try {
      document.cookie = 'pt_tema=' + tema + ';path=/;max-age=31536000;SameSite=Lax';
    } catch (e) { /* cookie bloqueado: mantém só na sessão */ }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', tema === 'escuro' ? '#050a12' : '#ffffff');
    if (btn) {
      btn.textContent = tema === 'escuro' ? '☀' : '🌙';
      btn.setAttribute('title', tema === 'escuro' ? 'Ativar tema claro' : 'Ativar tema escuro');
      btn.setAttribute('aria-label', btn.getAttribute('title'));
    }
  }

  pinta(atual());

  if (btn) {
    btn.addEventListener('click', function () {
      pinta(atual() === 'escuro' ? 'claro' : 'escuro');
    });
  }
})();

/* ------------------------------------------------------------------ */
/* Telemetria Anônima Sem Cookies — Ecossistema Penner Tech           */
/* ------------------------------------------------------------------ */
(function(){
  var TELEMETRY_ENDPOINTS = [
    'https://baixa.duckdns.org:8095/monitor/api/web-analytics/hit',
    'https://pennerflix.duckdns.org:8095/monitor/api/web-analytics/hit',
    'https://pennerserver2.tail69feb4.ts.net/monitor/api/web-analytics/hit',
    'https://pennerserver.tail69feb4.ts.net/monitor/api/web-analytics/hit'
  ];

  function detectSiteId() {
    var h = (location.hostname || '').toLowerCase();
    if (h.indexOf('baixatube') !== -1 || h.indexOf('baixa.duckdns') !== -1 || h.indexOf('pennerflix.duckdns') !== -1) return 'baixatube';
    if (h.indexOf('loja') !== -1) return 'loja';
    if (h.indexOf('baixa') !== -1) return 'baixa';
    return 'pennertech';
  }

  var currentSite = detectSiteId();

  function getUtmOrRef() {
    var u = '';
    try {
      var sp = new URLSearchParams(location.search);
      u = sp.get('utm_source') || sp.get('origem') || sp.get('from') || sp.get('ref') || '';
    } catch (e) {}
    return u;
  }

  async function sendTelemetryEvent(evType, extra) {
    var payload = {
      site: currentSite,
      type: evType || 'pageview',
      path: location.pathname || '/',
      ref: document.referrer || '',
      utm: getUtmOrRef(),
      target: (extra && extra.target) || '',
      label: (extra && extra.label) || ''
    };
    var bodyStr = JSON.stringify(payload);
    for (var i = 0; i < TELEMETRY_ENDPOINTS.length; i++) {
      var ep = TELEMETRY_ENDPOINTS[i];
      try {
        var ctl = new AbortController();
        var t = setTimeout(function(){ ctl.abort(); }, 2800);
        var r = await fetch(ep, {
          method: 'POST',
          headers: { 'Content-Type': 'text/plain;charset=UTF-8' },
          body: bodyStr,
          keepalive: true,
          signal: ctl.signal
        });
        clearTimeout(t);
        if (r && r.ok) return true;
      } catch (e) {}
    }
    return false;
  }

  window.ptTrackEvent = sendTelemetryEvent;

  // 1) Registra o pageview inicial (sem cookies, sem identificar usuário)
  sendTelemetryEvent('pageview');

  // 2) Captura cliques cruzados entre os subsites (BaixaTube <-> Loja <-> Baixa Certa)
  document.addEventListener('click', function(ev){
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (!href || href.charAt(0) === '#' || href.indexOf('javascript:') === 0) return;
    try {
      var destUrl = new URL(href, location.origin);
      var destHost = (destUrl.hostname || '').toLowerCase();
      if (!destHost || destHost === (location.hostname || '').toLowerCase()) return;

      var targetId = '';
      if (destHost.indexOf('loja.pennertech') !== -1) targetId = 'loja';
      else if (destHost.indexOf('baixa.pennertech') !== -1) targetId = 'baixa';
      else if (destHost.indexOf('baixatube.pennertech') !== -1 || destHost.indexOf('baixa.duckdns') !== -1) targetId = 'baixatube';
      else if (destHost.indexOf('pennertech.com.br') !== -1) targetId = 'pennertech';

      if (targetId && targetId !== currentSite) {
        // Anexa ?utm_source=<currentSite> no link para que o site de destino também saiba de onde veio o clique
        if (!destUrl.searchParams.get('utm_source')) {
          destUrl.searchParams.set('utm_source', currentSite);
          a.setAttribute('href', destUrl.toString());
        }
        sendTelemetryEvent('click', {
          target: targetId,
          label: (a.textContent || destHost).trim().slice(0, 60)
        });
      }
    } catch (e) {}
  }, true);
})();
