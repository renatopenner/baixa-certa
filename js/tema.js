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
