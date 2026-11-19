"""Gera o menu.js (barra de menu compartilhada) e garante que cada página HTML o carregue.

Uso:  python 06_resumo/atualizar_menu.py   (a partir da raiz do projeto)

O menu (itens, estilo e comportamento) fica todo em 06_resumo/menu.js. Cada página
tem só uma linha fixa que carrega esse arquivo:

    <!--menu--><script src="../../06_resumo/menu.js"></script><!--/menu-->

O menu só tem links fixos para as páginas-índice; cada índice tem a tabela com os links.
Também gera indice_pesquisa.js (texto de todas as páginas), usado por pesquisa.html.
Rode de novo sempre que criar ou alterar um README (menu nas páginas novas + índice de pesquisa). As páginas só são alteradas se
ainda não tiverem a linha do menu (por exemplo, um README novo); as demais ficam intactas.
"""
import html
from html.parser import HTMLParser
import json
import os
import re

PASTA = os.path.dirname(os.path.abspath(__file__))      # 06_resumo/
RAIZ = os.path.dirname(PASTA)                            # raiz do projeto
SUB = os.path.basename(PASTA)                            # '06_resumo'
IGNORAR = {'runs', 'folds_yolo', 'legado', '.claude', '.git', 'obj_train_data'}


def estrutura():
    """Itens do menu: [rótulo, página, prefixos que deixam o item ativo].

    Sem dropdown (pedido de 18 nov. 2026): cada item abre a página-índice da seção, que tem a
    tabela com links para cada experimento ou dataset.
    """
    return [
        [f'Resumo', f'{SUB}/resumo_experimentos.html', [f'{SUB}/resumo_experimentos.html']],
        ['Pré-processamento', '01_preprocessamento/README.html', ['01_preprocessamento/']],
        ['Datasets', '02_datasets_derivados/README.html',
         ['00_dataset_cvat/', '02_datasets_derivados/', '03_experimentos anteriores/datasets_derivados/']],
        ['Experimentos anteriores', '03_experimentos anteriores/README.html',
         ['03_experimentos anteriores/exp', '03_experimentos anteriores/README.html']],
        ['Novos experimentos', '05_novos_experimentos/README.html', ['05_novos_experimentos/']],
        ['Pesquisa', f'{SUB}/pesquisa.html', [f'{SUB}/pesquisa.html']],
    ]


CSS = """.mn{position:sticky;top:0;z-index:50;margin:0;display:block;background:var(--surface,var(--surface-1));border-bottom:1px solid var(--border);font:14px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mn-in{max-width:1100px;margin:0 auto;padding:6px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:2px 4px}
.mn a{text-decoration:none;border-bottom:0}
.mn-marca{font-weight:650;color:var(--text,var(--text-primary));margin-right:10px;padding:6px 0;white-space:nowrap}
.mn-item{display:inline-block;padding:6px 10px;border-radius:6px;color:var(--text2,var(--text-secondary));white-space:nowrap;font-weight:400}
.mn-item:hover{background:var(--grid);color:var(--text,var(--text-primary))}
.mn-item[aria-current]{background:var(--accent-soft);color:var(--text,var(--text-primary));font-weight:600}
[id]{scroll-margin-top:60px}
@media (max-width:640px){.mn-marca{width:100%}}
@media print{.mn{display:none}}"""

JS = r"""// Barra de menu compartilhada por todas as páginas HTML do projeto.
// GERADO por atualizar_menu.py: não edite à mão; rode `python 06_resumo/atualizar_menu.py`.
(function () {
  var ITENS = __ITENS__;
  var CSS = __CSS__;
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

  var h = '<div class="mn-in"><a class="mn-marca" href="' + url('__SUB__/resumo_experimentos.html') + '">Leishmania · Doutorado</a>';
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
"""


class _Secoes(HTMLParser):
    """Divide uma página em seções (h1/h2/h3) e guarda o texto visível de cada uma."""
    IGNORA = {'script', 'style', 'nav', 'head'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.secoes, self.titulo = [], ''
        self.pulando, self.em_titulo, self.em_cab = 0, False, None
        self.nova('', '')

    def nova(self, cab, ident):
        self.secoes.append({'cab': cab, 'id': ident, 'txt': []})

    def handle_starttag(self, tag, attrs):
        if tag in self.IGNORA:
            self.pulando += 1
        elif tag == 'title':
            self.em_titulo = True
        elif tag in ('h1', 'h2', 'h3') and not self.pulando:
            self.em_cab = tag
            self.nova('', dict(attrs).get('id') or '')
        elif tag in ('p', 'li', 'tr', 'td', 'th', 'br', 'div', 'figcaption', 'pre'):
            self.secoes[-1]['txt'].append(' ')

    def handle_endtag(self, tag):
        if tag in self.IGNORA:
            self.pulando = max(self.pulando - 1, 0)
        elif tag == 'title':
            self.em_titulo = False
        elif tag == self.em_cab:
            self.em_cab = None

    def handle_data(self, dado):
        if self.em_titulo:
            self.titulo += dado
        elif not self.pulando:
            alvo = self.secoes[-1]
            if self.em_cab:
                alvo['cab'] += dado
            else:
                alvo['txt'].append(dado)


def indice_pesquisa():
    """[página, título, [[cabeçalho, id, texto], ...]] de cada página HTML do projeto."""
    indice = []
    for pag in sorted(paginas()):
        if pag == f'{SUB}/pesquisa.html':
            continue
        with open(os.path.join(RAIZ, pag), encoding='utf-8') as f:
            leitor = _Secoes()
            leitor.feed(f.read())
        secoes = []
        for sec in leitor.secoes:
            txt = re.sub(r'\s+', ' ', ''.join(sec['txt'])).strip()
            cab = re.sub(r'\s+', ' ', sec['cab']).strip()
            if txt or cab:
                secoes.append([cab, sec['id'], txt])
        indice.append([pag, re.sub(r'\s+', ' ', leitor.titulo).strip() or pag, secoes])
    return indice


def paginas():
    for pasta, subpastas, arquivos in os.walk(RAIZ):
        subpastas[:] = [d for d in subpastas if d not in IGNORAR]
        for a in arquivos:
            if a == 'README.html' or (pasta == PASTA and a in ('resumo_experimentos.html', 'pesquisa.html')):
                yield os.path.relpath(os.path.join(pasta, a), RAIZ).replace(os.sep, '/')


def linha_menu(pagina_rel):
    rel = os.path.relpath(os.path.join(PASTA, 'menu.js'), os.path.dirname(os.path.join(RAIZ, pagina_rel)))
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
    js = (JS.replace('__SUB__', SUB).replace('__ITENS__', json.dumps(estrutura(), ensure_ascii=False, indent=1))
            .replace('__CSS__', json.dumps(CSS, ensure_ascii=False)))
    caminho_js = os.path.join(PASTA, 'menu.js')
    antigo = open(caminho_js, encoding='utf-8').read() if os.path.isfile(caminho_js) else None
    if js != antigo:
        with open(caminho_js, 'w', encoding='utf-8') as f:
            f.write(js)
    js_idx = ('// Texto de todas as páginas, para pesquisa.html. GERADO por atualizar_menu.py; não edite.\n'
              'var INDICE_PESQUISA = ' + json.dumps(indice_pesquisa(), ensure_ascii=False) + ';\n')
    with open(os.path.join(PASTA, 'indice_pesquisa.js'), 'w', encoding='utf-8') as f:
        f.write(js_idx)
    lista_paginas = sorted(paginas())
    alteradas = [p for p in lista_paginas if aplica(p)]
    print(f"menu.js {'atualizado' if js != antigo else 'sem mudança'}; "
          f"{len(lista_paginas)} páginas, {len(alteradas)} alteradas"
          + (': ' + ', '.join(alteradas) if 0 < len(alteradas) <= 5 else ''))
