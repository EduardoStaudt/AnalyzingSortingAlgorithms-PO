import csv
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt


# Raiz do projeto = pasta acima de /scripts/
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "results" / "tempos.csv"
IMAGES_DIR = BASE_DIR / "images"


# METADADOS
ALGORITMOS = {
    "bubble":    {"titulo": "Ordenação Bubble Sort",     "arquivo": "bubble_sort.png",    "sigla": "bs"},
    "insertion": {"titulo": "Ordenação por Inserção",    "arquivo": "insertion_sort.png", "sigla": "is"},
    "merge":     {"titulo": "Ordenação Merge Sort",      "arquivo": "merge_sort.png",     "sigla": "ms"},
    "quick":     {"titulo": "Ordenação Quick Sort",      "arquivo": "quick_sort.png",     "sigla": "qs"},
    "heap":      {"titulo": "Ordenação Heap Sort",       "arquivo": "heap_sort.png",      "sigla": "hs"},
    "selection": {"titulo": "Ordenação Selection Sort",  "arquivo": "selection_sort.png", "sigla": "ss"},
    "shell":     {"titulo": "Ordenação Shell Sort",      "arquivo": "shell_sort.png",     "sigla": "sh"},
    "radix":     {"titulo": "Ordenação Radix Sort",      "arquivo": "radix_sort.png",     "sigla": "rs"},
}


# QUAIS ENTRAM NA COMPARAÇÃO
# ["bubble", "insertion", "merge", "quick", "heap"]
ALGORITMOS_COMPARACAO = []


# STYLE
ESTILO_POR_TIPO = {
    "aleatorio": {"cor": "#1f3d99", "marcador": "D", "rotulo": "Aleatório"},
    "ordenado":  {"cor": "#e6009e", "marcador": "s", "rotulo": "Ordenados"},
    "invertido": {"cor": "#8faf3c", "marcador": "^", "rotulo": "Invertidos"},
}
ORDEM_TIPOS = ["aleatorio", "ordenado", "invertido"]

# MARCADORES
MARCADORES_ALGORITMO = ["D", "s", "^", "o", "x", "*", "v", "P"]


# LEITURA DO CSV
def ler_dados():
    # dados["bubble"]["aleatorio"] = [(700000, 12.34), (750000, 15.0), ...]
    # defaultdict cria a estrutura interna sozinho, sem checar "if key in dict"
    dados = defaultdict(lambda: defaultdict(list))

    with open(CSV_PATH, newline="") as arquivo_csv:
        # DictReader le cada linha como dict {nome_coluna: valor}
        leitor = csv.DictReader(arquivo_csv)
        for linha in leitor:
            algoritmo = linha["algoritmo"].strip()
            tipo = linha["tipo"].strip()
            amostras = int(linha["amostras"])
            tempo = float(linha["tempo"])
            dados[algoritmo][tipo].append((amostras, tempo))

    # Ordena pontos por quantidade de amostras (linha do grafico da esquerda p/ direita)
    for algoritmo in dados:
        for tipo in dados[algoritmo]:
            dados[algoritmo][tipo].sort(key=lambda ponto: ponto[0])

    return dados


# GRAFICO INDIVIDUAL 
def plotar_grafico_algoritmo(dados_algoritmo, titulo, nome_arquivo_saida):
    figura, eixo = plt.subplots(figsize=(7, 5))

    for tipo in ORDEM_TIPOS:
        if tipo not in dados_algoritmo:
            continue

        pontos = dados_algoritmo[tipo]
        # Separa lista [(x,y), ...] em duas: [x, x, ...] e [y, y, ...]
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

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = IMAGES_DIR / nome_arquivo_saida
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)

    print(f"[OK] Grafico salvo em: {caminho_saida}")


# GRAFICO DE COMPARACAO (N algoritmos)
def plotar_grafico_comparacao(dados, algoritmos_incluidos, nome_arquivo_saida):
    # Filtra so os algoritmos que foram pedidos E que existem no CSV
    algoritmos_validos = [a for a in algoritmos_incluidos if a in dados]

    if len(algoritmos_validos) < 2:
        print("[AVISO] Comparacao ignorada: precisa de pelo menos 2 algoritmos com dados no CSV.")
        return

    figura, eixo = plt.subplots(figsize=(8, 5))

    # Cria titulo dinamico com as siglas: "Comparacao entre bs, is, ms"
    siglas = [ALGORITMOS[a]["sigla"] for a in algoritmos_validos]
    titulo = f"Comparação entre {', '.join(siglas)}"

    # Cada algoritmo recebe um marcador diferente da lista
    # zip para percorrer os dois em paralelo (algoritmo + marcador correspondente)
    for algoritmo, marcador in zip(algoritmos_validos, MARCADORES_ALGORITMO):
        sigla = ALGORITMOS[algoritmo]["sigla"]

        for tipo in ORDEM_TIPOS:
            if tipo not in dados[algoritmo]:
                continue

            pontos = dados[algoritmo][tipo]
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
    # bbox_to_anchor joga legenda pra fora do grafico (a direita), evita cobrir dados
    eixo.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
    eixo.grid(True, linestyle="-", linewidth=0.5, alpha=0.5)

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = IMAGES_DIR / nome_arquivo_saida
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)

    print(f"[OK] Grafico salvo em: {caminho_saida}")


# MAIN
def main():
    if not CSV_PATH.exists():
        print(f"[ERRO] Nao encontrei o arquivo: {CSV_PATH}")
        print("Rode primeiro o benchmark pra gerar os tempos.")
        return

    dados = ler_dados()

    # Gera 1 grafico individual pra cada algoritmo que aparece no CSV
    # (nao precisa listar manualmente -- descobre sozinho)
    for algoritmo, dados_alg in dados.items():
        if algoritmo not in ALGORITMOS:
            print(f"[AVISO] Algoritmo '{algoritmo}' nao esta em ALGORITMOS, pulando.")
            continue

        meta = ALGORITMOS[algoritmo]
        plotar_grafico_algoritmo(dados_alg, meta["titulo"], meta["arquivo"])

    # Grafico de comparacao SO se a lista estiver preenchida
    if ALGORITMOS_COMPARACAO:
        plotar_grafico_comparacao(dados, ALGORITMOS_COMPARACAO, "comparacao.png")


if __name__ == "__main__":
    main()