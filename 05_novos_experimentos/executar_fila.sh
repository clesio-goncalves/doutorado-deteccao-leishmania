#!/bin/bash
# Executa em sequência os notebooks de experimento passados como argumento (nomes das pastas),
# com papermill, desligado do editor. Cada notebook é salvo depois de cada célula e o log
# fica em <pasta>/execucao.log. Uso:
#   setsid nohup ./executar_fila.sh exp11_... exp12_... > fila.log 2>&1 < /dev/null & disown
PAPERMILL=/home/clesio/anaconda3/bin/papermill
cd "$(dirname "$0")"
for exp in "$@"; do
  echo "$(date '+%F %T') início $exp"
  (cd "$exp" && "$PAPERMILL" -k python3 --cwd . "$exp.ipynb" "$exp.ipynb" > execucao.log 2>&1)
  echo "$(date '+%F %T') fim $exp (código $?)"
done
echo "$(date '+%F %T') fila concluída"
