// Barra de menu compartilhada por todas as páginas HTML do projeto.
// GERADO por atualizar_menu.py: não edite à mão; rode `python atualizar_menu.py`.
(function () {
  var ITENS = [
 [
  "Resumo",
  "resumo_experimentos.html",
  [
   "resumo_experimentos.html"
  ],
  []
 ],
 [
  "Pré-processamento",
  "01_preprocessamento/README.html",
  [
   "01_preprocessamento/"
  ],
  []
 ],
 [
  "Datasets",
  "02_datasets_derivados/README.html",
  [
   "00_dataset_cvat/",
   "02_datasets_derivados/",
   "03_experimentos anteriores/datasets_derivados/"
  ],
  [
   [
    "00_dataset_cvat/README.html",
    "00_dataset_cvat (dados brutos do CVAT)"
   ],
   [
    "02_datasets_derivados/README.html",
    "Visão geral dos datasets derivados"
   ],
   [
    "02_datasets_derivados/01_imagens_macrofagos_infectados/README.html",
    "01_imagens_macrofagos_infectados"
   ],
   [
    "02_datasets_derivados/02_recortes_512/README.html",
    "02_recortes_512"
   ],
   [
    "02_datasets_derivados/03_recortes_512_sem_macrofago/README.html",
    "03_recortes_512_sem_macrofago"
   ],
   [
    "02_datasets_derivados/04_recortes_512_sem_macrofago_reinhard/README.html",
    "04_recortes_512_sem_macrofago_reinhard"
   ],
   [
    "02_datasets_derivados/05_recortes_512_macrofago_cor_fundo/README.html",
    "05_recortes_512_macrofago_cor_fundo"
   ],
   [
    "03_experimentos anteriores/datasets_derivados/README.html",
    "Variantes antigas (exp06, exp07)"
   ]
  ]
 ],
 [
  "Experimentos anteriores",
  "03_experimentos anteriores/README.html",
  [
   "03_experimentos anteriores/exp",
   "03_experimentos anteriores/README.html"
  ],
  [
   [
    "03_experimentos anteriores/README.html",
    "Índice exp01–exp09"
   ],
   [
    "03_experimentos anteriores/exp01_yolo11n/README.html",
    "exp01 · YOLO11n, recorte original"
   ],
   [
    "03_experimentos anteriores/exp02_yolo11n_p2/README.html",
    "exp02 · YOLO11n + cabeça P2, imgsz 640"
   ],
   [
    "03_experimentos anteriores/exp03_yolo11l/README.html",
    "exp03 · YOLO11l, recorte original"
   ],
   [
    "03_experimentos anteriores/exp04_yolo26m/README.html",
    "exp04 · YOLO26m"
   ],
   [
    "03_experimentos anteriores/exp05_yolo26l/README.html",
    "exp05 · YOLO26l"
   ],
   [
    "03_experimentos anteriores/exp06_yolo11m_realce/README.html",
    "exp06 · YOLO11m + realce CLAHE + aumento de dados"
   ],
   [
    "03_experimentos anteriores/exp07_yolo11l_lab/README.html",
    "exp07 · YOLO11l + Lab puro + batch 4"
   ],
   [
    "03_experimentos anteriores/exp08_yolo11n_sem_macrofago/README.html",
    "exp08 · YOLO11n, recorte sem macrófago"
   ],
   [
    "03_experimentos anteriores/exp09_yolo11l_sem_macrofago/README.html",
    "exp09 · YOLO11l, recorte sem macrófago"
   ]
  ]
 ],
 [
  "Novos experimentos",
  "05_novos_experimentos/README.html",
  [
   "05_novos_experimentos/"
  ],
  [
   [
    "05_novos_experimentos/README.html",
    "Índice, status e plano"
   ],
   [
    "05_novos_experimentos/exp10_yolov8l_sem_macrofago/README.html",
    "exp10 · YOLOv8l sobre os recortes sem macrófago"
   ],
   [
    "05_novos_experimentos/exp11_yolo11n_reinhard/README.html",
    "exp11 · YOLO11n sobre os recortes com coloração normalizada (Reinhard)"
   ],
   [
    "05_novos_experimentos/exp12_yolo11n_aumento_hed/README.html",
    "exp12 · YOLO11n com aumento de cor HED no treino"
   ],
   [
    "05_novos_experimentos/exp13_yolo11n_mascara_cor_fundo/README.html",
    "exp13 · YOLO11n sobre os recortes com o macrófago preenchido pela cor do fundo"
   ],
   [
    "05_novos_experimentos/exp14_yolo11n_imgsz1024/README.html",
    "exp14 · YOLO11n com imgsz 1024"
   ],
   [
    "05_novos_experimentos/exp15_yolo11l_optuna/README.html",
    "exp15 · YOLO11l com hiperparâmetros otimizados pelo Optuna"
   ],
   [
    "05_novos_experimentos/exp16_yolo11n_params_optuna/README.html",
    "exp16 · YOLO11n com os hiperparâmetros encontrados pelo Optuna"
   ]
  ]
 ]
];
  var CSS = ".mn{position:sticky;top:0;z-index:50;margin:0;display:block;background:var(--surface,var(--surface-1));border-bottom:1px solid var(--border);font:14px/1.4 system-ui,-apple-system,\"Segoe UI\",Roboto,sans-serif}\n.mn-in{max-width:1100px;margin:0 auto;padding:6px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:2px 4px}\n.mn a{text-decoration:none;border-bottom:0}\n.mn-marca{font-weight:650;color:var(--text,var(--text-primary));margin-right:10px;padding:6px 0;white-space:nowrap}\n.mn-item{display:inline-block;padding:6px 10px;border-radius:6px;color:var(--text2,var(--text-secondary));cursor:pointer;white-space:nowrap;list-style:none}\n.mn-item::-webkit-details-marker{display:none}\nsummary.mn-item::after{content:\" \\25BE\";font-size:.8em}\n.mn-item:hover{background:var(--grid);color:var(--text,var(--text-primary))}\n.mn-item[aria-current]{background:var(--accent-soft);color:var(--text,var(--text-primary));font-weight:600}\n.mn-grupo{position:relative}\n.mn-lista{position:absolute;left:0;top:calc(100% + 4px);min-width:260px;max-width:min(440px,90vw);max-height:70vh;overflow:auto;background:var(--surface,var(--surface-1));border:1px solid var(--border);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.18);padding:4px;display:flex;flex-direction:column}\n.mn-lista a{padding:7px 10px;border-radius:5px;color:var(--text,var(--text-primary));font-size:.9rem}\n.mn-lista a:hover{background:var(--grid)}\n.mn-lista a[aria-current]{background:var(--accent-soft);font-weight:600}\n[id]{scroll-margin-top:60px}\n@media (max-width:640px){.mn-marca{width:100%}.mn-grupo{position:static}.mn-lista{left:16px;right:16px;max-width:none}}\n@media print{.mn{display:none}}";
  var script = document.currentScript;
  var raiz = script.src.replace(/menu\.js(\?.*)?$/, '');            // URL da raiz do projeto
  var atual = decodeURIComponent(location.href.split('#')[0].split('?')[0]);
  var raizDec = decodeURIComponent(raiz);
  var pagina = atual.indexOf(raizDec) === 0 ? atual.slice(raizDec.length) : '';
  function url(p) { return raiz + p.split('/').map(encodeURIComponent).join('/'); }
  function esc(t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

  var estilo = document.createElement('style');
  estilo.textContent = CSS;
  document.head.appendChild(estilo);

  var h = '<div class="mn-in"><a class="mn-marca" href="' + url('resumo_experimentos.html') + '">Leishmania · Doutorado</a>';
  ITENS.forEach(function (it) {
    var rotulo = it[0], destino = it[1], prefixos = it[2], sub = it[3];
    var ativo = prefixos.some(function (p) { return pagina.indexOf(p) === 0; });
    var cur = ativo ? ' aria-current="page"' : '';
    if (!sub.length) { h += '<a class="mn-item" href="' + url(destino) + '"' + cur + '>' + esc(rotulo) + '</a>'; return; }
    h += '<details class="mn-grupo"><summary class="mn-item"' + cur + '>' + esc(rotulo) + '</summary><div class="mn-lista">';
    sub.forEach(function (s) {
      h += '<a href="' + url(s[0]) + '"' + (s[0] === pagina ? ' aria-current="page"' : '') + '>' + esc(s[1]) + '</a>';
    });
    h += '</div></details>';
  });
  h += '</div>';

  var nav = document.createElement('nav');
  nav.className = 'mn';
  nav.setAttribute('aria-label', 'Navegação do projeto');
  nav.innerHTML = h;
  script.parentNode.insertBefore(nav, script);

  document.addEventListener('click', function (e) {
    document.querySelectorAll('.mn-grupo[open]').forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute('open'); });
  });
  nav.querySelectorAll('.mn-grupo').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) nav.querySelectorAll('.mn-grupo[open]').forEach(function (o) { if (o !== d) o.removeAttribute('open'); });
    });
  });
})();
