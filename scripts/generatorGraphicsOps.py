import csv
import re
from pathlib import Path
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "data" / "results"
IMAGES_DIR = BASE_DIR / "images" / "ops"


# --------------------------------------------------------------------------
# CONFIGURACAO
# --------------------------------------------------------------------------

# Metadados dos algoritmos da parte 2
ALGORITMOS = {
    "quick": {"titulo": "Quick Sort", "sigla": "qs", "rotulo": "Quick"},
    "merge": {"titulo": "Merge Sort", "sigla": "ms", "rotulo": "Merge"},
    "radix": {"titulo": "Radix Sort", "sigla": "rs", "rotulo": "Radix"},
    "heap":  {"titulo": "Heap Sort",  "sigla": "hs", "rotulo": "Heap"},
}

# Todos os 4 entram nos graficos de TEMPO
ALGORITMOS_TEMPO = ["quick", "merge", "radix", "heap"]

# Radix NAO entra nos graficos de OPERACOES (nao usa comparacoes/trocas tradicionais)
ALGORITMOS_OPERACOES = ["quick", "merge", "heap"]

# Tipo de entrada usado nos graficos de OPERACOES (caso medio)
# Trocar para "ordenado" ou "invertido" se quiser outro cenario
TIPO_OPERACOES = "aleatorio"


# Estilo por tipo de dataset (graficos de tempo)
ESTILO_POR_TIPO = {
    "aleatorio": {"cor": "#1f3d99", "marcador": "D", "rotulo": "Aleatório"},
    "ordenado":  {"cor": "#e6009e", "marcador": "s", "rotulo": "Ordenados"},
    "invertido": {"cor": "#8faf3c", "marcador": "^", "rotulo": "Invertidos"},
}
ORDEM_TIPOS = ["aleatorio", "ordenado", "invertido"]

# Marcadores por algoritmo (comparacao de tempo)
MARCADORES_ALGORITMO = ["D", "s", "^", "o", "x", "*"]

# Cores das barras (graficos de operacoes)
COR_COMPARACOES = "#1f3d99"
COR_TROCAS = "#00b3b3"

# So le arquivos go_<algo>_ops.csv / java_<algo>_ops.csv
PADRAO_ARQUIVO = re.compile(r"^(?P<linguagem>[a-z]+)_(?P<algoritmo>[a-z]+)_ops\.csv$")


# --------------------------------------------------------------------------
# LEITURA
# --------------------------------------------------------------------------

def ler_dados():
    # dados[ling][algo][tipo] = [(amostras, tempo, comp, troca), ...]
    dados = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    if not RESULTS_DIR.exists():
        return dados

    for caminho in sorted(RESULTS_DIR.glob("*_ops.csv")):
        match = PADRAO_ARQUIVO.match(caminho.name)
        if not match:
            continue
        linguagem = match.group("linguagem")
        algoritmo = match.group("algoritmo")

        with open(caminho, newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                tipo = linha["tipo"].strip()
                amostras = int(linha["amostras"])
                tempo = float(linha["tempo"])
                comp = int(linha["comparacoes"])
                troc = int(linha["trocas"])
                dados[linguagem][algoritmo][tipo].append((amostras, tempo, comp, troc))

    # ordena por quantidade de amostras
    for ling in dados:
        for algo in dados[ling]:
            for tipo in dados[ling][algo]:
                dados[ling][algo][tipo].sort(key=lambda p: p[0])

    return dados


# --------------------------------------------------------------------------
# GRAFICO DE TEMPO INDIVIDUAL (linha, 3 tipos)
# --------------------------------------------------------------------------

def plotar_tempo_individual(dados_algo, titulo, caminho_saida):
    figura, eixo = plt.subplots(figsize=(7, 5))

    for tipo in ORDEM_TIPOS:
        if tipo not in dados_algo:
            continue
        pontos = dados_algo[tipo]
        eixo_x = [p[0] for p in pontos]
        eixo_y = [p[1] for p in pontos]  # tempo
        estilo = ESTILO_POR_TIPO[tipo]
        eixo.plot(eixo_x, eixo_y, color=estilo["cor"], marker=estilo["marcador"],
                  label=estilo["rotulo"], linewidth=1.5, markersize=7)

    eixo.set_title(titulo, fontsize=13, fontweight="bold")
    eixo.set_xlabel("Amostras")
    eixo.set_ylabel("Tempo seg.")
    eixo.legend(loc="upper left")
    eixo.grid(True, linestyle="-", linewidth=0.5, alpha=0.5)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)
    print(f"[OK] {caminho_saida.relative_to(BASE_DIR)}")


# --------------------------------------------------------------------------
# GRAFICO DE COMPARACAO DE TEMPO (linha, N algoritmos)
# --------------------------------------------------------------------------

def plotar_comparacao_tempo(dados_ling, linguagem, caminho_saida):
    validos = [a for a in ALGORITMOS_TEMPO if a in dados_ling]
    if len(validos) < 2:
        return

    figura, eixo = plt.subplots(figsize=(8, 5))
    siglas = [ALGORITMOS[a]["sigla"] for a in validos]
    titulo = f"[{linguagem.upper()}] Comparação de tempo entre {', '.join(siglas)}"

    for algo, marcador in zip(validos, MARCADORES_ALGORITMO):
        sigla = ALGORITMOS[algo]["sigla"]
        for tipo in ORDEM_TIPOS:
            if tipo not in dados_ling[algo]:
                continue
            pontos = dados_ling[algo][tipo]
            eixo_x = [p[0] for p in pontos]
            eixo_y = [p[1] for p in pontos]
            estilo = ESTILO_POR_TIPO[tipo]
            eixo.plot(eixo_x, eixo_y, color=estilo["cor"], marker=marcador,
                      label=f"{estilo['rotulo']} ({sigla})", linewidth=1.5, markersize=7)

    eixo.set_title(titulo, fontsize=12, fontweight="bold")
    eixo.set_xlabel("Amostras")
    eixo.set_ylabel("Tempo seg.")
    eixo.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))
    eixo.grid(True, linestyle="-", linewidth=0.5, alpha=0.5)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)
    print(f"[OK] {caminho_saida.relative_to(BASE_DIR)}")


# --------------------------------------------------------------------------
# GRAFICO DE OPERACOES INDIVIDUAL (linha, comparacoes + trocas ao longo dos tamanhos)
# --------------------------------------------------------------------------

def plotar_operacoes_individual(dados_algo, titulo, caminho_saida):
    if TIPO_OPERACOES not in dados_algo:
        return
    pontos = dados_algo[TIPO_OPERACOES]

    eixo_x = [p[0] for p in pontos]
    comparacoes = [p[2] for p in pontos]
    trocas = [p[3] for p in pontos]

    figura, eixo = plt.subplots(figsize=(7, 5))
    eixo.plot(eixo_x, comparacoes, color=COR_COMPARACOES, marker="D",
              label="Comparações", linewidth=1.5, markersize=7)
    eixo.plot(eixo_x, trocas, color=COR_TROCAS, marker="s",
              label="Trocas", linewidth=1.5, markersize=7)

    eixo.set_title(titulo, fontsize=13, fontweight="bold")
    eixo.set_xlabel("Amostras")
    eixo.set_ylabel("Nº de operações")
    eixo.legend(loc="upper left")
    eixo.grid(True, linestyle="-", linewidth=0.5, alpha=0.5)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)
    print(f"[OK] {caminho_saida.relative_to(BASE_DIR)}")


# --------------------------------------------------------------------------
# GRAFICO DE OPERACOES COMPARACAO (barras, por tamanho, N algoritmos)
# --------------------------------------------------------------------------

def plotar_operacoes_comparacao(dados_ling, linguagem, amostras, caminho_saida):
    # Coleta comparacoes e trocas de cada algoritmo nesse tamanho especifico
    algos_validos = []
    comparacoes = []
    trocas = []

    for algo in ALGORITMOS_OPERACOES:
        if algo not in dados_ling or TIPO_OPERACOES not in dados_ling[algo]:
            continue
        # acha o ponto com esse tamanho
        ponto = next((p for p in dados_ling[algo][TIPO_OPERACOES] if p[0] == amostras), None)
        if ponto is None:
            continue
        algos_validos.append(ALGORITMOS[algo]["rotulo"])
        comparacoes.append(ponto[2])
        trocas.append(ponto[3])

    if len(algos_validos) < 2:
        return

    x = np.arange(len(algos_validos))
    largura = 0.35

    figura, eixo = plt.subplots(figsize=(7, 5))
    eixo.bar(x - largura / 2, comparacoes, largura, label="Comparações", color=COR_COMPARACOES)
    eixo.bar(x + largura / 2, trocas, largura, label="Trocas", color=COR_TROCAS)

    titulo = f"[{linguagem.upper()}] Operações em {amostras:,}".replace(",", ".")
    eixo.set_title(titulo, fontsize=12, fontweight="bold")
    eixo.set_ylabel("Nº de operações")
    eixo.set_xticks(x)
    eixo.set_xticklabels(algos_validos)
    eixo.legend()
    eixo.grid(True, axis="y", linestyle="-", linewidth=0.5, alpha=0.5)

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    figura.tight_layout()
    figura.savefig(caminho_saida, dpi=150)
    plt.close(figura)
    print(f"[OK] {caminho_saida.relative_to(BASE_DIR)}")


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main():
    dados = ler_dados()

    if not dados:
        print(f"[ERRO] Nenhum arquivo *_ops.csv encontrado em {RESULTS_DIR}")
        print("Rode primeiro o benchmark de operacoes.")
        return

    for linguagem, dados_ling in dados.items():
        pasta = IMAGES_DIR / linguagem

        # 1) Tempo individual (4 algoritmos)
        for algo in ALGORITMOS_TEMPO:
            if algo not in dados_ling:
                continue
            titulo = f"[{linguagem.upper()}] {ALGORITMOS[algo]['titulo']}"
            caminho = pasta / f"{linguagem}_{algo}_tempo.png"
            plotar_tempo_individual(dados_ling[algo], titulo, caminho)

        # 2) Comparacao de tempo (4 juntos)
        caminho = pasta / f"{linguagem}_comparacao_tempo.png"
        plotar_comparacao_tempo(dados_ling, linguagem, caminho)

        # 3) Operacoes individual (3 algoritmos, sem radix)
        for algo in ALGORITMOS_OPERACOES:
            if algo not in dados_ling:
                continue
            titulo = f"[{linguagem.upper()}] Operações do {ALGORITMOS[algo]['titulo']}"
            caminho = pasta / f"{linguagem}_{algo}_operacoes.png"
            plotar_operacoes_individual(dados_ling[algo], titulo, caminho)

        # 4) Operacoes comparacao (barras, um grafico por tamanho)
        # descobre os tamanhos presentes a partir de um algoritmo qualquer
        tamanhos = set()
        for algo in ALGORITMOS_OPERACOES:
            if algo in dados_ling and TIPO_OPERACOES in dados_ling[algo]:
                for p in dados_ling[algo][TIPO_OPERACOES]:
                    tamanhos.add(p[0])

        for amostras in sorted(tamanhos):
            caminho = pasta / f"{linguagem}_operacoes_{amostras}.png"
            plotar_operacoes_comparacao(dados_ling, linguagem, amostras, caminho)


if __name__ == "__main__":
    main()
