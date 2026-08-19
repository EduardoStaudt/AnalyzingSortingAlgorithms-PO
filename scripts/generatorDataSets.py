import sys
import time
from pathlib import Path
import numpy as np


# Tamanhos padrao (usados se o usuario nao passar nenhum argumento no terminal)
TAMANHOS_PADRAO = [700_000, 750_000, 800_000, 850_000, 900_000, 1_000_000]

# Raiz do projeto = pasta acima de /scripts/
BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_DIR = BASE_DIR / "data" / "datasets"


def gerar_aleatorio(quantidade):
    # np.arange cria [1..quantidade] direto em memoria C (rapido)
    numeros = np.arange(1, quantidade + 1)
    # shuffle in-place no backend C do NumPy (bem mais rapido que random.shuffle puro)
    np.random.shuffle(numeros)
    return numeros


def gerar_ordenado(quantidade):
    return np.arange(1, quantidade + 1)


def gerar_invertido(quantidade):
    # np.arange com passo -1 gera decrescente sem precisar de reverse()
    return np.arange(quantidade, 0, -1)


def salvar_arquivo(caminho, numeros):
    # np.savetxt escreve o array inteiro de uma vez em C, sem loop Python
    # fmt="%d" -> formata como inteiro (senao salva como float 1.0, 2.0, ...)
    # header com a quantidade + comments="" pra nao inserir "#" antes
    np.savetxt(caminho, numeros, fmt="%d", header=str(len(numeros)), comments="")


def gerar_conjunto(quantidade):
    # Garante que a pasta destino existe (nao da erro se ja existir)
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    # Dicionario mapeando nome do tipo -> funcao que gera aquele tipo
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
    # Se passar argumentos no terminal, usa eles como tamanhos
    # Ex: python generatorDataSets.py 700000 800000
    # Se nao passar nada, usa a lista TAMANHOS_PADRAO
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