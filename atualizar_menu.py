"""Insere (ou atualiza) a barra de menu em todas as páginas HTML de documentação do projeto.

Uso:  python atualizar_menu.py

Rode de novo sempre que criar um experimento, um dataset ou um README novo: o script
descobre sozinho as pastas expNN_* e os datasets e refaz o menu de todas as páginas.
O menu fica entre os marcadores <!--menu--> ... <!--/menu--> e o CSS entre /*menu*/ ... /*/menu*/,
então rodar várias vezes não duplica nada.
"""
import html
import os
import re

RAIZ = os.path.dirname(os.path.abspath(__file__))
IGNORAR = {'runs', 'folds_yolo', 'legado', '.claude', 'obj_train_data'}


def titulo_curto(caminho_readme, nome_pasta):
    """Texto do item no menu: 'expNN · <título do h1 depois do travessão>'."""
    try:
        with open(caminho_readme, encoding='utf-8') as f:
            h1 = re.search(r'<h1>(.*?)</h1>', f.read(), re.S)
        texto = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else nome_pasta
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
            itens.append((f'{pasta_rel}/{nome}/README.html', titulo_curto(readme, nome)))
    return itens


def estrutura():
    return [
        ('Resumo', 'resumo_experimentos.html', None),
        ('Pré-processamento', '01_preprocessamento/README.html', None),
        ('Datasets', '02_datasets_derivados/README.html',
         [('00_dataset_cvat/README.html', '00_dataset_cvat (dados brutos do CVAT)'), ('02_datasets_derivados/README.html', 'Visão geral dos datasets derivados')]
         + [(c, os.path.basename(os.path.dirname(c))) for c, _ in lista('02_datasets_derivados', r'\d\d_')]
         + [('03_experimentos anteriores/datasets_derivados/README.html', 'Variantes antigas (exp06, exp07)')]),
        ('Experimentos anteriores', '03_experimentos anteriores/README.html',
         [('03_experimentos anteriores/README.html', 'Índice exp01–exp09')]
         + lista('03_experimentos anteriores', r'exp\d+_')),
        ('Novos experimentos', '05_novos_experimentos/README.html',
         [('05_novos_experimentos/README.html', 'Índice, status e plano')]
         + lista('05_novos_experimentos', r'exp\d+_')),
    ]


def href(destino, pagina_rel):
    rel = os.path.relpath(os.path.join(RAIZ, destino), os.path.dirname(os.path.join(RAIZ, pagina_rel)))
    return html.escape(rel.replace(os.sep, '/').replace(' ', '%20'), quote=True)


def menu_html(pagina_rel):
    partes = [f'<a class="mn-marca" href="{href("resumo_experimentos.html", pagina_rel)}">Leishmania · Doutorado</a>']
    for rotulo, destino, sub in estrutura():
        secao = os.path.dirname(destino) or destino
        ativo = pagina_rel == destino or (secao != destino and pagina_rel.startswith(secao + '/'))
        if rotulo == 'Datasets' and (pagina_rel.startswith('03_experimentos anteriores/datasets_derivados') or pagina_rel.startswith('00_dataset_cvat/')):
            ativo = True
        if rotulo == 'Experimentos anteriores' and pagina_rel.startswith('03_experimentos anteriores/datasets_derivados'):
            ativo = False
        atual = ' aria-current="page"' if ativo else ''
        if not sub:
            partes.append(f'<a class="mn-item" href="{href(destino, pagina_rel)}"{atual}>{rotulo}</a>')
            continue
        itens = ''.join(
            f'<a href="{href(c, pagina_rel)}"{" aria-current=\"page\"" if c == pagina_rel else ""}>{html.escape(t)}</a>'
            for c, t in sub)
        partes.append(f'<details class="mn-grupo"><summary class="mn-item"{atual}>{rotulo}</summary>'
                      f'<div class="mn-lista">{itens}</div></details>')
    return ('<!--menu-->\n<nav class="mn" aria-label="Navegação do projeto"><div class="mn-in">'
            + ''.join(partes)
            + '</div></nav>\n<script>document.addEventListener("click",function(e){document.querySelectorAll(".mn-grupo[open]").forEach(function(d){if(!d.contains(e.target))d.removeAttribute("open")})});'
            'document.querySelectorAll(".mn-grupo").forEach(function(d){d.addEventListener("toggle",function(){if(d.open)document.querySelectorAll(".mn-grupo[open]").forEach(function(o){if(o!==d)o.removeAttribute("open")})})});</script>\n<!--/menu-->')


CSS = """/*menu*/
.mn{position:sticky;top:0;z-index:50;margin:0;display:block;background:var(--surface,var(--surface-1));border-bottom:1px solid var(--border);font:14px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.mn-in{max-width:1100px;margin:0 auto;padding:6px 16px;display:flex;flex-wrap:wrap;align-items:center;gap:2px 4px}
.mn a{text-decoration:none;border-bottom:0}
.mn-marca{font-weight:650;color:var(--text,var(--text-primary));margin-right:10px;padding:6px 0;white-space:nowrap}
.mn-item{display:inline-block;padding:6px 10px;border-radius:6px;color:var(--text2,var(--text-secondary));cursor:pointer;white-space:nowrap;list-style:none}
.mn-item::-webkit-details-marker{display:none}
summary.mn-item::after{content:" ▾";font-size:.8em}
.mn-item:hover{background:var(--grid);color:var(--text,var(--text-primary))}
.mn-item[aria-current]{background:var(--accent-soft);color:var(--text,var(--text-primary));font-weight:600}
.mn-grupo{position:relative}
.mn-lista{position:absolute;left:0;top:calc(100% + 4px);min-width:260px;max-width:min(440px,90vw);max-height:70vh;overflow:auto;background:var(--surface,var(--surface-1));border:1px solid var(--border);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.18);padding:4px;display:flex;flex-direction:column}
.mn-lista a{padding:7px 10px;border-radius:5px;color:var(--text,var(--text-primary));font-size:.9rem}
.mn-lista a:hover{background:var(--grid)}
.mn-lista a[aria-current]{background:var(--accent-soft);font-weight:600}
@media (max-width:640px){.mn-marca{width:100%}.mn-grupo{position:static}.mn-lista{left:16px;right:16px;max-width:none}}
[id]{scroll-margin-top:60px}
@media print{.mn{display:none}}
/*/menu*/"""


def paginas():
    for pasta, subpastas, arquivos in os.walk(RAIZ):
        subpastas[:] = [d for d in subpastas if d not in IGNORAR]
        for a in arquivos:
            if a == 'README.html' or (pasta == RAIZ and a == 'resumo_experimentos.html'):
                yield os.path.relpath(os.path.join(pasta, a), RAIZ).replace(os.sep, '/')


def aplica(pagina_rel):
    caminho = os.path.join(RAIZ, pagina_rel)
    with open(caminho, encoding='utf-8') as f:
        s = f.read()
    s = re.sub(r'\n?<!--menu-->.*?<!--/menu-->\n?', '\n', s, flags=re.S)
    s = re.sub(r'/\*menu\*/.*?/\*/menu\*/\n?', '', s, flags=re.S)
    s = s.replace('</style>', CSS + '\n</style>', 1)
    s = re.sub(r'<body>\s*', '<body>\n' + menu_html(pagina_rel).replace('\\', '\\\\') + '\n', s, count=1)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == '__main__':
    lista_paginas = sorted(paginas())
    for p in lista_paginas:
        aplica(p)
    print(f'Menu atualizado em {len(lista_paginas)} páginas.')
