import sys
import time
from pathlib import Path
import numpy as np


# 12 tamanhos: os 6 da parte 1 + os 6 da parte 2
# O de 1000000 aparece nas duas partes, entao so existe uma vez em disco
TAMANHOS_PADRAO = [
    700_000, 750_000, 800_000, 850_000, 900_000, 1_000_000,  # parte 1
    1_150_000, 1_300_000, 1_350_000, 1_500_000, 2_000_000,   # parte 2 (1M ja esta acima)
]

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "data" / "datasets"


def gerar_aleatorio(quantidade):
    numeros = np.arange(1, quantidade + 1)
    np.random.shuffle(numeros)
    return numeros


def gerar_ordenado(quantidade):
    return np.arange(1, quantidade + 1)


def gerar_invertido(quantidade):
    return np.arange(quantidade, 0, -1)


def salvar_arquivo(caminho, numeros):
    np.savetxt(caminho, numeros, fmt="%d", header=str(len(numeros)), comments="")


def gerar_conjunto(quantidade):
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    tipos = {
        "aleatorio": gerar_aleatorio,
        "ordenado": gerar_ordenado,
        "invertido": gerar_invertido,
    }

    for nome_tipo, funcao_geradora in tipos.items():
        # Se o arquivo ja existe, pula (reaproveita datasets ja gerados)
        nome_arquivo = f"{nome_tipo}_{quantidade}.txt"
        caminho = DATASETS_DIR / nome_arquivo
        if caminho.exists():
            print(f"  [--] {nome_arquivo} ja existe, pulando")
            continue

        inicio = time.time()
        numeros = funcao_geradora(quantidade)
        salvar_arquivo(caminho, numeros)
        duracao = time.time() - inicio
        print(f"  [OK] {nome_arquivo}  ({duracao:.2f}s)")


def main():
    # Se passar argumentos no terminal, usa eles como tamanhos
    # Ex: python generatorDataSets.py 1150000 2000000
    if len(sys.argv) > 1:
        tamanhos = [int(arg) for arg in sys.argv[1:]]
    else:
        tamanhos = TAMANHOS_PADRAO

    for tamanho in tamanhos:
        print(f"\nGerando conjunto de {tamanho:,} numeros...".replace(",", "."))
        gerar_conjunto(tamanho)

    print("\nConcluido.")


if __name__ == "__main__":
    main()
