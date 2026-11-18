import os
import shutil
import yaml
from pathlib import Path

from ultralytics import YOLO

# Dataset utilizado
diretorio_raiz = Path("/mnt/arquivos/Doutorado")
RAW_DATA_DIR = Path(os.path.join(diretorio_raiz, "dataset_macrofagos_infectados"))

# Pasta de saída para os datasets preparados por fold
PREPARED_DIR = Path("data/prepared_folds")

# Pasta de saída dos treinamentos
RUNS_DIR = Path("runs/leishmania_folds")

# Extensões de imagem aceitas
IMG_EXTENSIONS = {".png"}

# Classes originais no dataset
ORIGINAL_CLASSES = {
    0: "Non-macrophage",
    1: "Macrophage",
    2: "Leishmania", # - alvo: leishmania FORA do macrófago
    3: "Inside-macrophage", # - IGNORADA (leishmania DENTRO do macrófago)
}

# Classe de interesse: apenas "Leishmania" (classe 2 original --> 0 no modelo)
TARGET_ORIGINAL_CLASS = 2
TARGET_NEW_CLASS = 0 # único índice no YAML do modelo
TARGET_CLASS_NAME = "Leishmania"

# Parâmetros de treinamento
EPOCHS = 100
IMG_SIZE = 640
BATCH_SIZE= 16
PATIENCE = 20 # early stopping
MODEL_NAME  = "yolo12n.pt"

# DIVISÃO DOS 6 FOLDS
FOLDS = [
    {
        "fold":  1,
        "train": ["leish_1", "leish_2", "leish_7", "leish_8", "leish_9"],
        "val":   ["leish_4"],
        "test":  ["leish_3", "leish_5"],
    },
    {
        "fold":  2,
        "train": ["leish_1", "leish_3", "leish_4", "leish_5", "leish_9"],
        "val":   ["leish_8"],
        "test":  ["leish_2", "leish_7"],
    },
    {
        "fold":  3,
        "train": ["leish_2", "leish_3", "leish_4", "leish_5", "leish_7"],
        "val":   ["leish_9"],
        "test":  ["leish_1", "leish_8"],
    },
    {
        "fold":  4,
        "train": ["leish_1", "leish_2", "leish_3", "leish_5", "leish_8"],
        "val":   ["leish_7"],
        "test":  ["leish_4", "leish_9"],
    },
    {
        "fold":  5,
        "train": ["leish_3", "leish_4", "leish_5", "leish_8", "leish_9"],
        "val":   ["leish_2"],
        "test":  ["leish_1", "leish_7"],
    },
    {
        "fold":  6,
        "train": ["leish_3", "leish_4", "leish_5", "leish_7", "leish_9"],
        "val":   ["leish_1"],
        "test":  ["leish_2", "leish_8"],
    },
]

# FUNÇÕES AUXILIARES

def filtrar_anotacao(txt_origem: Path, txt_destino: Path) -> int:
    """
    Lê um arquivo .txt de anotações YOLO, mantém SOMENTE linhas da
    classe 2 (Leishmania fora do macrófago) e remapeia para classe 0.
    """
    anotacoes_validas = []

    if not txt_origem.exists():
        # Imagem sem anotação --> arquivo vazio (sem instâncias)
        txt_destino.write_text("")
        return 0

    with open(txt_origem, "r") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            partes = linha.split()
            classe_original = int(partes[0])

            # Mantém apenas a classe de interesse (Leishmania = 2)
            if classe_original == TARGET_ORIGINAL_CLASS:
                # Remapeia: 2 --> 0
                nova_linha = f"{TARGET_NEW_CLASS} " + " ".join(partes[1:])
                anotacoes_validas.append(nova_linha)
            # Classe 3 (inside-macrophage) e demais são descartadas

    txt_destino.write_text("\n".join(anotacoes_validas))
    return len(anotacoes_validas)


def copiar_laminas(laminas: list, pasta_destino: Path, split: str) -> dict:
    """
    Copia imagens e anotações filtradas de uma lista de lâminas
    para pasta_destino/images e pasta_destino/labels.
    """
    img_dir = pasta_destino / "images"
    lbl_dir = pasta_destino / "labels"
    img_dir.mkdir(parents=True, exist_ok=True)
    lbl_dir.mkdir(parents=True, exist_ok=True)

    stats = {"imagens": 0, "anotacoes": 0, "laminas": laminas}

    for lamina in laminas:
        pasta_lamina = RAW_DATA_DIR / lamina
        if not pasta_lamina.exists():
            print(f"    Lâmina não encontrada: {pasta_lamina}")
            continue

        for arquivo in sorted(pasta_lamina.iterdir()):
            if arquivo.suffix.lower() not in IMG_EXTENSIONS:
                continue

            # Prefixo único para evitar conflito de nomes entre lâminas
            nome_destino = f"{lamina}__{arquivo.name}"

            # Copia imagem
            shutil.copy2(arquivo, img_dir / nome_destino)
            stats["imagens"] += 1

            # Filtra e copia anotação correspondente
            txt_origem = arquivo.with_suffix(".txt")
            txt_destino = lbl_dir / (nome_destino.rsplit(".", 1)[0] + ".txt")
            n = filtrar_anotacao(txt_origem, txt_destino)
            stats["anotacoes"] += n

    print(f"    [{split}] {stats['imagens']} imagens | "
          f"{stats['anotacoes']} anotações válidas | "
          f"lâminas: {laminas}")
    return stats


def criar_yaml_fold(fold_dir: Path) -> Path:
    """
    Cria o arquivo data.yaml necessário pelo YOLO para um fold específico.
    """
    yaml_content = {
        "path":  str(fold_dir.resolve()),
        "train": "train/images",
        "val":   "val/images",
        "test":  "test/images",
        "nc":    1,                          # apenas 1 classe
        "names": [TARGET_CLASS_NAME],        # ["Leishmania"]
    }

    yaml_path = fold_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(yaml_content, f, default_flow_style=False, allow_unicode=True)

    return yaml_path


def preparar_fold(fold_info: dict) -> Path:
    """
    Prepara a estrutura de pastas e arquivos para um fold:
      prepared_folds/fold_X/
        train/images/  train/labels/
        val/images/    val/labels/
        test/images/   test/labels/
        data.yaml
    """
    fold_n   = fold_info["fold"]
    fold_dir = PREPARED_DIR / f"fold_{fold_n}"

    print(f"\n Preparando Fold {fold_n}...")

    # Limpa e recria a pasta do fold se já existir
    if fold_dir.exists():
        shutil.rmtree(fold_dir)
    fold_dir.mkdir(parents=True)

    # Copia cada split
    copiar_laminas(fold_info["train"], fold_dir / "train","TREINO")
    copiar_laminas(fold_info["val"],   fold_dir / "val", "VALIDAÇÃO")
    copiar_laminas(fold_info["test"],  fold_dir / "test", "TESTE")

    # Gera o YAML
    yaml_path = criar_yaml_fold(fold_dir)
    print(f"     data.yaml criado: {yaml_path}")

    return yaml_path


def treinar_fold(fold_info: dict, yaml_path: Path) -> dict:
    """
    Treina o modelo YOLO-nano para um fold específico.
    Retorna as métricas do conjunto de teste.
    """
    fold_n    = fold_info["fold"]
    run_name  = f"fold_{fold_n}"
    print(f"\n Treinando Fold {fold_n} com {MODEL_NAME}...")

    # Carrega o modelo (baixa os pesos pré-treinados na primeira vez)
    model = YOLO(MODEL_NAME)

    # Treinamento
    model.train(
        data      = str(yaml_path),
        epochs    = EPOCHS,
        imgsz     = IMG_SIZE,
        batch     = BATCH_SIZE,
        patience  = PATIENCE,        # early stopping sem melhora
        name      = run_name,
        project   = str(RUNS_DIR),
        exist_ok  = True,
        verbose   = True,
        # Augmentações recomendadas para imagens microscópicas
        flipud    = 0.5,             # flip vertical
        fliplr    = 0.5,             # flip horizontal
        degrees   = 15,              # rotação pequena
        hsv_h     = 0.01,            # variação mínima de matiz (microscopia)
        hsv_s     = 0.4,
        hsv_v     = 0.3,
    )

    # -- Localiza o best.pt de forma robusta ----------------------------------
    # O YOLO pode criar subpastas numeradas (fold_1, fold_12, fold_13...)
    best_weights = None

    # 1ª opção: caminho direto via trainer (mais confiável)
    if hasattr(model, "trainer") and hasattr(model.trainer, "best"):
        candidato = Path(str(model.trainer.best))
        if candidato.exists():
            best_weights = candidato

    # 2ª opção: busca recursiva pelo best.pt mais recente no projeto
    if best_weights is None:
        candidatos = sorted(
            RUNS_DIR.rglob("best.pt"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if candidatos:
            best_weights = candidatos[0]

    # 3ª opção: fallback para last.pt
    if best_weights is None:
        candidatos_last = sorted(
            RUNS_DIR.rglob("last.pt"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if candidatos_last:
            best_weights = candidatos_last[0]
            print(f"    best.pt não encontrado - usando last.pt: {best_weights}")

    if best_weights is None:
        raise FileNotFoundError(
            f"Nenhum peso encontrado em {RUNS_DIR}. "
            "Verifique se o treinamento foi concluído corretamente."
        )

    print(f"   Pesos carregados: {best_weights}")
    print(f"\n Avaliando Fold {fold_n} no conjunto de TESTE...")

    model_best = YOLO(str(best_weights))
    metricas   = model_best.val(
        data   = str(yaml_path),
        split  = "test",             # avalia no split 'test' do data.yaml
        imgsz  = IMG_SIZE,
        name   = f"{run_name}_test",
        project= str(RUNS_DIR),
        exist_ok=True,
    )

    return {
        "fold": fold_n,
        "mAP50": round(float(metricas.box.map50), 4),
        "mAP50-95": round(float(metricas.box.map), 4),
        "precision": round(float(metricas.box.mp), 4),
        "recall": round(float(metricas.box.mr), 4),
        "best_model": str(best_weights),
    }


def salvar_resumo(resultados: list):
    """
    Imprime e salva um resumo consolidado com as métricas de todos os folds.
    """
    print("\n" + "=" * 65)
    print("  RESUMO - Métricas por Fold (conjunto de TESTE)")
    print("=" * 65)
    print(f"{'Fold':>6} {'mAP@50':>10} {'mAP@50-95':>12} "
          f"{'Precision':>12} {'Recall':>10}")
    print("-" * 65)

    map50_vals  = []
    map5095_vals = []

    for r in resultados:
        print(f"  {r['fold']:>4}   {r['mAP50']:>10.4f}   {r['mAP50-95']:>10.4f}"
              f"   {r['precision']:>10.4f}   {r['recall']:>8.4f}")
        map50_vals.append(r["mAP50"])
        map5095_vals.append(r["mAP50-95"])

    print("-" * 65)
    media50    = sum(map50_vals)    / len(map50_vals)
    media5095  = sum(map5095_vals)  / len(map5095_vals)
    print(f"  {'MÉDIA':>4}   {media50:>10.4f}   {media5095:>10.4f}")
    print("=" * 65)

    # Salva em arquivo de texto
    resumo_path = RUNS_DIR / "resumo_folds.txt"
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    with open(resumo_path, "w") as f:
        f.write("Fold,mAP50,mAP50-95,Precision,Recall,BestModel\n")
        for r in resultados:
            f.write(f"{r['fold']},{r['mAP50']},{r['mAP50-95']},"
                    f"{r['precision']},{r['recall']},{r['best_model']}\n")
        f.write(f"MEDIA,{media50:.4f},{media5095:.4f},,,\n")

    print(f"\n Resumo salvo em: {resumo_path}")


# EXECUÇÃO PRINCIPAL

def main():
    # Garante que os caminhos são objetos Path
    global RAW_DATA_DIR, PREPARED_DIR, RUNS_DIR
    RAW_DATA_DIR = Path(RAW_DATA_DIR)
    PREPARED_DIR = Path(PREPARED_DIR)
    RUNS_DIR     = Path(RUNS_DIR)

    print("=" * 65)
    print("  Leishmania Detection - YOLOv12-nano - 6-Fold Cross-Validation")
    print("=" * 65)
    print(f"\n Dados brutos:    {RAW_DATA_DIR.resolve()}")
    print(f" Dados preparados:{PREPARED_DIR.resolve()}")
    print(f" Resultados:      {RUNS_DIR.resolve()}")
    print(f"\n Classe alvo: '{TARGET_CLASS_NAME}' "
          f"(original: {TARGET_ORIGINAL_CLASS} --> remapeada para: {TARGET_NEW_CLASS})")
    print(f" Classe ignorada: 'Inside-macrophage' (classe 3)")

    resultados = []

    for fold_info in FOLDS:
        # 1. Prepara as pastas e filtra as anotações
        yaml_path = preparar_fold(fold_info)

        # 2. Treina e avalia
        metricas = treinar_fold(fold_info, yaml_path)
        resultados.append(metricas)

        print(f"\n Fold {fold_info['fold']} concluído - "
              f"mAP@50: {metricas['mAP50']:.4f} | "
              f"mAP@50-95: {metricas['mAP50-95']:.4f}")

    # 3. Resumo final
    salvar_resumo(resultados)


if __name__ == "__main__":
    main()
