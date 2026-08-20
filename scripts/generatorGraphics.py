import csv
import re
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "data" / "results"
IMAGES_DIR = BASE_DIR / "images"


ALGORITMOS = {
    "bubble":    {"titulo": "Bubble Sort",     "arquivo": "bubble_sort.png",    "sigla": "bs"},
    "insertion": {"titulo": "Insertion Sort",  "arquivo": "insertion_sort.png", "sigla": "is"},
    "merge":     {"titulo": "Merge Sort",      "arquivo": "merge_sort.png",     "sigla": "ms"},
    "quick":     {"titulo": "Quick Sort",      "arquivo": "quick_sort.png",     "sigla": "qs"},
    "heap":      {"titulo": "Heap Sort",       "arquivo": "heap_sort.png",      "sigla": "hs"},
    "selection": {"titulo": "Selection Sort",  "arquivo": "selection_sort.png", "sigla": "ss"},
    "shell":     {"titulo": "Shell Sort",      "arquivo": "shell_sort.png",     "sigla": "sh"},
    "radix":     {"titulo": "Radix Sort",      "arquivo": "radix_sort.png",     "sigla": "rs"},
}

ALGORITMOS_COMPARACAO = []


ESTILO_POR_TIPO = {
    "aleatorio": {"cor": "#1f3d99", "marcador": "D", "rotulo": "Aleatório"},
    "ordenado":  {"cor": "#e6009e", "marcador": "s", "rotulo": "Ordenados"},
    "invertido": {"cor": "#8faf3c", "marcador": "^", "rotulo": "Invertidos"},
}
ORDEM_TIPOS = ["aleatorio", "ordenado", "invertido"]

MARCADORES_ALGORITMO = ["D", "s", "^", "o", "x", "*", "v", "P"]

PADRAO_ARQUIVO_CSV = re.compile(r"^(?P<linguagem>[a-z]+)_(?P<algoritmo>[a-z]+)\.csv$")


def ler_dados():
    dados = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    if not RESULTS_DIR.exists():
        return dados

    for caminho_csv in sorted(RESULTS_DIR.glob("*.csv")):
        match = PADRAO_ARQUIVO_CSV.match(caminho_csv.name)
        if not match:
            print(f"[AVISO] Ignorando arquivo com nome fora do padrao: {caminho_csv.name}")
            continue

        linguagem = match.group("linguagem")
        algoritmo = match.group("algoritmo")

        with open(caminho_csv, newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                tipo = linha["tipo"].strip()
                amostras = int(linha["amostras"])
                tempo = float(linha["tempo"])
                dados[linguagem][algoritmo][tipo].append((amostras, tempo))

    for linguagem in dados:
        for algoritmo in dados[linguagem]:
            for tipo in dados[linguagem][algoritmo]:
                dados[linguagem][algoritmo][tipo].sort(key=lambda ponto: ponto[0])

    return dados


def plotar_grafico_algoritmo(dados_algoritmo, titulo, caminho_saida):
    figura, eixo = plt.subplots(figsize=(7, 5))

    for tipo in ORDEM_TIPOS:
        if tipo not in dados_algoritmo:
            continue

        pontos = dados_algoritmo[tipo]
        eixo_x = [ponto[0] for ponto in pontos]
        eixo_y = [ponto[1] for ponto in pontos]

        estilo = ESTILO_POR_TIPO[tipo]
        eixo.plot(
            eixo_x, eixo_y,
            color=estilo["cor"],
            marker=estilo["marcador"],
            label=estilo["rotulo"],
            linewidth=1.5,
            markersize=7,
        )

    eixo.set_title(titulo, fontsize=13, fontweight="bold")
    eixo.set_xlabel("Amostras")
    eixo.set_ylabel("Tempo seg.")
    eixo.legend(loc="upper left")
    eixo.grid(True, linestyle="-", linewidth=0.5, alpha=0.5)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)

    print(f"[OK] Grafico salvo em: {caminho_saida.relative_to(BASE_DIR)}")


def plotar_grafico_comparacao(dados_linguagem, linguagem, algoritmos_incluidos, caminho_saida):
    algoritmos_validos = [a for a in algoritmos_incluidos if a in dados_linguagem]

    if len(algoritmos_validos) < 2:
        print(f"[AVISO] Comparacao ({linguagem}) ignorada: precisa de pelo menos 2 algoritmos com dados.")
        return

    figura, eixo = plt.subplots(figsize=(8, 5))

    siglas = [ALGORITMOS[a]["sigla"] for a in algoritmos_validos]
    titulo = f"[{linguagem.upper()}] Comparação entre {', '.join(siglas)}"

    for algoritmo, marcador in zip(algoritmos_validos, MARCADORES_ALGORITMO):
        sigla = ALGORITMOS[algoritmo]["sigla"]

        for tipo in ORDEM_TIPOS:
            if tipo not in dados_linguagem[algoritmo]:
                continue

            pontos = dados_linguagem[algoritmo][tipo]
            eixo_x = [ponto[0] for ponto in pontos]
            eixo_y = [ponto[1] for ponto in pontos]

            estilo = ESTILO_POR_TIPO[tipo]
            eixo.plot(
                eixo_x, eixo_y,
                color=estilo["cor"],
                marker=marcador,
                label=f"{estilo['rotulo']} ({sigla})",
                linewidth=1.5,
                markersize=7,
            )

    eixo.set_title(titulo, fontsize=12, fontweight="bold")
    eixo.set_xlabel("Amostras")
    eixo.set_ylabel("Tempo seg.")
    eixo.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
    eixo.grid(True, linestyle="-", linewidth=0.5, alpha=0.5)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)

    print(f"[OK] Grafico salvo em: {caminho_saida.relative_to(BASE_DIR)}")


def main():
    dados = ler_dados()

    if not dados:
        print(f"[ERRO] Nenhum CSV encontrado em {RESULTS_DIR}")
        print("Rode primeiro os benchmarks pra gerar os CSVs.")
        return

    for linguagem, dados_linguagem in dados.items():
        pasta_linguagem = IMAGES_DIR / linguagem

        for algoritmo, dados_alg in dados_linguagem.items():
            if algoritmo not in ALGORITMOS:
                print(f"[AVISO] Algoritmo '{algoritmo}' nao esta em ALGORITMOS, pulando.")
                continue

            meta = ALGORITMOS[algoritmo]
            nome_arquivo = f"{linguagem}_{meta['arquivo']}"
            caminho = pasta_linguagem / nome_arquivo
            titulo = f"[{linguagem.upper()}] {meta['titulo']}"
            plotar_grafico_algoritmo(dados_alg, titulo, caminho)

        if ALGORITMOS_COMPARACAO:
            siglas_lista = [ALGORITMOS[a]["sigla"] for a in ALGORITMOS_COMPARACAO if a in ALGORITMOS]
            nome_comp = f"{linguagem}_comparacao_{'_'.join(siglas_lista)}.png"
            caminho_comp = pasta_linguagem / nome_comp
            plotar_grafico_comparacao(dados_linguagem, linguagem, ALGORITMOS_COMPARACAO, caminho_comp)


if __name__ == "__main__":
    main()
