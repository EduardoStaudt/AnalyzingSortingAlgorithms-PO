import sys
import time
from pathlib import Path
import numpy as np


TAMANHOS_PADRAO = [700_000, 750_000, 800_000, 850_000, 900_000, 1_000_000]

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
        inicio = time.time()
        numeros = funcao_geradora(quantidade)
        nome_arquivo = f"{nome_tipo}_{quantidade}.txt"
        salvar_arquivo(DATASETS_DIR / nome_arquivo, numeros)
        duracao = time.time() - inicio
        print(f"  [OK] {nome_arquivo}  ({duracao:.2f}s)")


def main():
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
