"""Gera o menu.js (barra de menu compartilhada) e garante que cada página HTML o carregue.

Uso:  python atualizar_menu.py

O menu (itens, estilo e comportamento) fica todo em menu.js, na raiz do projeto. Cada página
tem só uma linha fixa que carrega esse arquivo:

    <!--menu--><script src="../../menu.js"></script><!--/menu-->

Rode de novo sempre que criar um experimento, um dataset ou um README novo: o script descobre
sozinho as pastas expNN_* e os datasets e reescreve o menu.js. As páginas só são alteradas se
ainda não tiverem a linha do menu (por exemplo, um README novo); as demais ficam intactas.
"""
import html
import json
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR = {'runs', 'folds_yolo', 'legado', '.claude', '.git', 'obj_train_data'}


def titulo_curto(caminho_readme, nome_pasta):
    """Texto do item no menu: 'expNN · <título do h1 depois do travessão>'."""
    try:
        with open(caminho_readme, encoding='utf-8') as f:
            h1 = re.search(r'<h1>(.*?)</h1>', f.read(), re.S)
        texto = html.unescape(re.sub(r'<[^>]+>', '', h1.group(1))).strip() if h1 else nome_pasta
    except OSError:
        texto = nome_pasta
    if '—' in texto:
        texto = texto.split('—', 1)[1].strip()
    num = re.match(r'(exp\d+)', nome_pasta)
    return f"{num.group(1)} · {texto}" if num else texto


def lista(pasta_rel, padrao):
    """Subpastas de pasta_rel que casam com o padrão e têm README.html, em ordem."""
    base = os.path.join(RAIZ, pasta_rel)
    if not os.path.isdir(base):
        return []
    itens = []
    for nome in sorted(os.listdir(base)):
        readme = os.path.join(base, nome, 'README.html')
        if re.match(padrao, nome) and os.path.isfile(readme):
            itens.append([f'{pasta_rel}/{nome}/README.html', titulo_curto(readme, nome)])
    return itens


def estrutura():
    """Itens do menu: [rótulo, página principal, prefixos que deixam o item ativo, subitens]."""
    return [
        ['Resumo', 'resumo_experimentos.html', ['resumo_experimentos.html'], []],
        ['Pré-processamento', '01_preprocessamento/README.html', ['01_preprocessamento/'], []],
        ['Datasets', '02_datasets_derivados/README.html',
         ['00_dataset_cvat/', '02_datasets_derivados/', '03_experimentos anteriores/datasets_derivados/'],
         [['00_dataset_cvat/README.html', '00_dataset_cvat (dados brutos do CVAT)'],
          ['02_datasets_derivados/README.html', 'Visão geral dos datasets derivados']]
         + [[c, os.path.basename(os.path.dirname(c))] for c, _ in lista('02_datasets_derivados', r'\d\d_')]
         + [['03_experimentos anteriores/datasets_derivados/README.html', 'Variantes antigas (exp06, exp07)']]],
        ['Experimentos anteriores', '03_experimentos anteriores/README.html',
         ['03_experimentos anteriores/exp', '03_experimentos anteriores/README.html'],
         [['03_experimentos anteriores/README.html', 'Índice exp01–exp09']] + lista('03_experimentos anteriores', r'exp\d+_')],
        ['Novos experimentos', '05_novos_experimentos/README.html', ['05_novos_experimentos/'],
         [['05_novos_experimentos/README.html', 'Índice, status e plano']] + lista('05_novos_experimentos', r'exp\d+_')],
    ]


CSS = """.mn{position:sticky;top:0;z-index:50;margin:0;display:block;background:var(--surface,var(--surface-1));border-bottom:1px solid var(--border);font:14px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mn-in{max-width:1100px;margin:0 auto;padding:6px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:2px 4px}
.mn a{text-decoration:none;border-bottom:0}
.mn-marca{font-weight:650;color:var(--text,var(--text-primary));margin-right:10px;padding:6px 0;white-space:nowrap}
.mn-item{display:inline-block;padding:6px 10px;border-radius:6px;color:var(--text2,var(--text-secondary));cursor:pointer;white-space:nowrap;list-style:none}
.mn-item::-webkit-details-marker{display:none}
summary.mn-item::after{content:" \\25BE";font-size:.8em}
.mn-item:hover{background:var(--grid);color:var(--text,var(--text-primary))}
.mn-item[aria-current]{background:var(--accent-soft);color:var(--text,var(--text-primary));font-weight:600}
.mn-grupo{position:relative}
.mn-lista{position:absolute;left:0;top:calc(100% + 4px);min-width:260px;max-width:min(440px,90vw);max-height:70vh;overflow:auto;background:var(--surface,var(--surface-1));border:1px solid var(--border);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.18);padding:4px;display:flex;flex-direction:column}
.mn-lista a{padding:7px 10px;border-radius:5px;color:var(--text,var(--text-primary));font-size:.9rem}
.mn-lista a:hover{background:var(--grid)}
.mn-lista a[aria-current]{background:var(--accent-soft);font-weight:600}
[id]{scroll-margin-top:60px}
@media (max-width:640px){.mn-marca{width:100%}.mn-grupo{position:static}.mn-lista{left:16px;right:16px;max-width:none}}
@media print{.mn{display:none}}"""

JS = r"""// Barra de menu compartilhada por todas as páginas HTML do projeto.
// GERADO por atualizar_menu.py: não edite à mão; rode `python atualizar_menu.py`.
(function () {
  var ITENS = __ITENS__;
  var CSS = __CSS__;
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
"""


def paginas():
    for pasta, subpastas, arquivos in os.walk(RAIZ):
        subpastas[:] = [d for d in subpastas if d not in IGNORAR]
        for a in arquivos:
            if a == 'README.html' or (pasta == RAIZ and a == 'resumo_experimentos.html'):
                yield os.path.relpath(os.path.join(pasta, a), RAIZ).replace(os.sep, '/')


def linha_menu(pagina_rel):
    rel = os.path.relpath(os.path.join(RAIZ, 'menu.js'), os.path.dirname(os.path.join(RAIZ, pagina_rel)))
    return '<!--menu--><script src="' + rel.replace(os.sep, '/').replace(' ', '%20') + '"></script><!--/menu-->'


def aplica(pagina_rel):
    """Garante a linha do menu na página. Só grava o arquivo se algo mudar."""
    caminho = os.path.join(RAIZ, pagina_rel)
    with open(caminho, encoding='utf-8') as f:
        original = f.read()
    s = re.sub(r'\n?<!--menu-->.*?<!--/menu-->\n?', '\n', original, flags=re.S)   # remove menu antigo/embutido
    s = re.sub(r'/\*menu\*/.*?/\*/menu\*/\n?', '', s, flags=re.S)                  # remove CSS antigo embutido
    s = re.sub(r'<body>\s*', '<body>\n' + linha_menu(pagina_rel) + '\n', s, count=1)
    if s != original:
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(s)
        return True
    return False


if __name__ == '__main__':
    js = (JS.replace('__ITENS__', json.dumps(estrutura(), ensure_ascii=False, indent=1))
            .replace('__CSS__', json.dumps(CSS, ensure_ascii=False)))
    caminho_js = os.path.join(RAIZ, 'menu.js')
    antigo = open(caminho_js, encoding='utf-8').read() if os.path.isfile(caminho_js) else None
    if js != antigo:
        with open(caminho_js, 'w', encoding='utf-8') as f:
            f.write(js)
    lista_paginas = sorted(paginas())
    alteradas = [p for p in lista_paginas if aplica(p)]
    print(f"menu.js {'atualizado' if js != antigo else 'sem mudança'}; "
          f"{len(lista_paginas)} páginas, {len(alteradas)} alteradas"
          + (': ' + ', '.join(alteradas) if 0 < len(alteradas) <= 5 else ''))
