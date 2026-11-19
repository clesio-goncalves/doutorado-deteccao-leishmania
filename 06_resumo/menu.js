// Barra de menu compartilhada por todas as páginas HTML do projeto.
// GERADO por atualizar_menu.py: não edite à mão; rode `python 06_resumo/atualizar_menu.py`.
(function () {
  var ITENS = [
 [
  "Resumo",
  "06_resumo/resumo_experimentos.html",
  [
   "06_resumo/resumo_experimentos.html"
  ]
 ],
 [
  "Pré-processamento",
  "01_preprocessamento/README.html",
  [
   "01_preprocessamento/"
  ]
 ],
 [
  "Datasets",
  "02_datasets_derivados/README.html",
  [
   "00_dataset_cvat/",
   "02_datasets_derivados/",
   "03_experimentos anteriores/datasets_derivados/"
  ]
 ],
 [
  "Experimentos anteriores",
  "03_experimentos anteriores/README.html",
  [
   "03_experimentos anteriores/exp",
   "03_experimentos anteriores/README.html"
  ]
 ],
 [
  "Novos experimentos",
  "05_novos_experimentos/README.html",
  [
   "05_novos_experimentos/"
  ]
 ],
 [
  "Pesquisa",
  "06_resumo/pesquisa.html",
  [
   "06_resumo/pesquisa.html"
  ]
 ]
];
  var CSS = ".mn{position:sticky;top:0;z-index:50;margin:0;display:block;background:var(--surface,var(--surface-1));border-bottom:1px solid var(--border);font:14px/1.4 system-ui,-apple-system,\"Segoe UI\",Roboto,sans-serif}\n.mn-in{max-width:1100px;margin:0 auto;padding:6px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:2px 4px}\n.mn a{text-decoration:none;border-bottom:0}\n.mn-marca{font-weight:650;color:var(--text,var(--text-primary));margin-right:10px;padding:6px 0;white-space:nowrap}\n.mn-item{display:inline-block;padding:6px 10px;border-radius:6px;color:var(--text2,var(--text-secondary));white-space:nowrap;font-weight:400}\n.mn-item:hover{background:var(--grid);color:var(--text,var(--text-primary))}\n.mn-item[aria-current]{background:var(--accent-soft);color:var(--text,var(--text-primary));font-weight:600}\n[id]{scroll-margin-top:60px}\n@media (max-width:640px){.mn-marca{width:100%}}\n@media print{.mn{display:none}}";
  var script = document.currentScript;
  var raiz = script.src.replace(/[^\/]+\/menu\.js(\?.*)?$/, '');   // URL da raiz do projeto (menu.js fica em 06_resumo/)
  var atual = decodeURIComponent(location.href.split('#')[0].split('?')[0]);
  var raizDec = decodeURIComponent(raiz);
  var pagina = atual.indexOf(raizDec) === 0 ? atual.slice(raizDec.length) : '';
  function url(p) { return raiz + p.split('/').map(encodeURIComponent).join('/'); }
  function esc(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

  var estilo = document.createElement('style');
  estilo.textContent = CSS;
  document.head.appendChild(estilo);

  var h = '<div class="mn-in"><a class="mn-marca" href="' + url('06_resumo/resumo_experimentos.html') + '">Leishmania · Doutorado</a>';
  ITENS.forEach(function (it) {
    var ativo = it[2].some(function (p) { return pagina.indexOf(p) === 0; });
    h += '<a class="mn-item" href="' + url(it[1]) + '"' + (ativo ? ' aria-current="page"' : '') + '>' + esc(it[0]) + '</a>';
  });
  h += '</div>';

  var nav = document.createElement('nav');
  nav.className = 'mn';
  nav.setAttribute('aria-label', 'Navegação do projeto');
  nav.innerHTML = h;
  script.parentNode.insertBefore(nav, script);

})();
