/* Baixa Certa — busca e filtro do catálogo (sem dependências) */
(function () {
  'use strict';

  var grade = document.getElementById('grade');
  if (!grade) return;

  var entradaCatalogo = document.getElementById('buscaApp');
  var entradaHero = document.getElementById('buscaHero');
  var chips = Array.prototype.slice.call(
    document.querySelectorAll('.chips [data-chip], #vazio [data-chip]')
  );
  var contador = document.getElementById('contador');
  var vazio = document.getElementById('vazio');
  var cards = Array.prototype.slice.call(grade.querySelectorAll('.app'));
  var total = cards.length;
  var catAtiva = 'todos';

  function norm(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  cards.forEach(function (c) {
    var h3 = c.querySelector('h3');
    c.dataset.busca = norm((c.dataset.busca || '') + ' ' + (h3 ? h3.textContent : ''));
  });

  function aplica() {
    var q = norm(entradaCatalogo ? entradaCatalogo.value.trim() : '');
    var visiveis = 0;

    cards.forEach(function (c) {
      var okCat = catAtiva === 'todos' || c.dataset.cat === catAtiva;
      var okBusca = !q || (c.dataset.busca || '').indexOf(q) !== -1;
      var mostra = okCat && okBusca;
      c.classList.toggle('oculto', !mostra);
      if (mostra) visiveis++;
    });

    if (contador) contador.innerHTML = '<b>' + visiveis + '</b> de ' + total + ' apps';
    if (vazio) vazio.classList.toggle('oculto', visiveis !== 0);
    grade.classList.toggle('oculto', visiveis === 0);
  }

  function liga(a) {
    if (entradaCatalogo && a !== entradaCatalogo) entradaCatalogo.value = a.value;
    if (entradaHero && a !== entradaHero) entradaHero.value = a.value;
    aplica();
  }

  if (entradaCatalogo) entradaCatalogo.addEventListener('input', function () { liga(entradaCatalogo); });
  if (entradaHero) entradaHero.addEventListener('input', function () { liga(entradaHero); });

  // Enter na busca do topo leva ao catálogo
  if (entradaHero) {
    entradaHero.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') {
        ev.preventDefault();
        var alvo = document.getElementById('catalogo');
        if (alvo) alvo.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }

  chips.forEach(function (b) {
    b.addEventListener('click', function (ev) {
      ev.preventDefault();
      chips.forEach(function (o) { o.classList.remove('on'); });
      b.classList.add('on');
      catAtiva = b.dataset.cat;
      aplica();
    });
  });

  // "/" foca a busca do catálogo
  document.addEventListener('keydown', function (ev) {
    var alvo = entradaCatalogo || entradaHero;
    if (!alvo) return;
    var tag = (document.activeElement && document.activeElement.tagName) || '';
    if (ev.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(tag)) {
      ev.preventDefault();
      alvo.focus();
    }
    if (ev.key === 'Escape' && document.activeElement === alvo) {
      alvo.value = '';
      if (entradaCatalogo) entradaCatalogo.value = '';
      if (entradaHero) entradaHero.value = '';
      aplica();
      alvo.blur();
    }
  });

  // busca vinda de link (?q=termo)
  try {
    var q = new URLSearchParams(location.search).get('q');
    if (q) {
      if (entradaCatalogo) entradaCatalogo.value = q;
      if (entradaHero) entradaHero.value = q;
    }
  } catch (e) { /* navegador antigo: ignora */ }

  aplica();
})();
