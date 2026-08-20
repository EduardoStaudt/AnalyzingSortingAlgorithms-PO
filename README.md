# Análise de Algoritmos de Ordenação

Projeto da disciplina de Pesquisa e Ordenação - CC4PO, ministrada pela professora Gloria Patricia Lopez Sepulveda, este projeto teve como objetivo mostrar e comparar os diferentes algoritmos de ordenação existentes.

## Configuração do computador:
- Processador: Apple M5 com 10 núcleos, sendo 4 de performance e 6 de eficiência
- Placa de Vídeo: GPU integrada Apple (não utilizada)
- Memória RAM: 24 GB
- Sistema Operacional: macOS
---
## Linguagens:
### Geração dos datasets e gráficos:
- Python 3.11.4 (Para gerar gráficos e datasets)
### Nos algoritmos de ordenação:
- Golang 1.27.0
- Java 26.0.2.1
---
## Como executar o projeto:
Preparar a venv:
```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy matplotlib
```

Gerar os 18 datasets em `data/datasets/`:
```bash
python scripts/generatorDataSets.py
```

### Rodar o benchmark em Go

**Mac:**

```bash
go mod init AnalyzingSortingAlgorithms-PO
go build -o benchmark
./benchmark
```

**Windows (PowerShell):**

```powershell
go mod init AnalyzingSortingAlgorithms-PO
go build -o benchmark.exe
.\benchmark.exe
```

### Rodar o benchmark em Java

**Mac:**

```bash
mkdir -p out
javac -d out Main.java algorithms/java/*.java
java -cp out Main
```

**Windows (PowerShell):**

```powershell
mkdir out
javac -d out Main.java algorithms\java\*.java
java -cp out Main
```

Gerar os gráficos:
```bash
python scripts/generatorGraphics.py
```
## Estrutura do projeto:
```
AnalyzingSortingAlgorithms-PO/
├── algorithms/
│   ├── go/          8 algoritmos em Go
│   └── java/        8 algoritmos em Java
├── data/
│   ├── datasets/    arquivos de números para ordenar
│   └── results/     CSVs com os tempos medidos
├── images/
│   ├── go/          gráficos gerados dos dados Go
│   └── java/        gráficos gerados dos dados Java
├── scripts/
│   ├── generatorDataSets.py
│   └── generatorGraphics.py
├── main.go          entrypoint do benchmark Go
├── Main.java        entrypoint do benchmark Java
└── README.md
```
 

Os 8 algoritmos implementados nas duas linguagens são bubble sort, insertion sort, selection sort, merge sort, quick sort, heap sort, shell sort e radix sort.

## Resultados e conhecimento obtidos:
Passei os algoritmos em datasets.txt compostos por 6 tamanhos sendo eles 700k, 750k, 800k, 850k, 900k e 1M, para cada dataset existiam três variações na disposição dos dados, elas eram: dados aleatórios, invertidos e ordenados.

| Algoritmo | Onde ainda faz sentido usar | O que quebra | Meus resultados (1M elementos) |
|---|---|---|---|
| Bubble Sort | Basicamente só em sala de aula. Insertion sort supera ele em qualquer situação prática. | Qualquer volume médio de dados aleatórios. O(n²) sem nenhuma vantagem prática que outros não tenham. | Aleatório 912s, Ordenado 0s, Invertido 171s |
| Insertion Sort | Arrays pequenos, tipo 10 a 50 itens, e dados quase ordenados. Muitas linguagens usam ele internamente em sorts híbridos como Timsort. | Volumes grandes de dados desordenados. Escala mal e não tem como fugir disso. | Aleatório 70s, Ordenado 0s, Invertido 120s |
| Selection Sort | Quase nunca em código real. A única vantagem é fazer poucas trocas (no máximo N), o que só importa quando escrever no array é caríssimo. Caso raro. | Não tem melhor caso. Roda a mesma quantidade de comparações sempre, independente da entrada. | Aleatório 228s, Ordenado 230s, Invertido 194s |
| Merge Sort | Ordenação estável de arrays grandes, ordenação de dados que não cabem na memória (external sort) e listas ligadas. | Uso de memória. Precisa de espaço extra proporcional ao tamanho do input. Ruim pra ambientes com pouca RAM. | Aleatório 0.08s, Ordenado 0.02s, Invertido 0.03s |
| Quick Sort | Ordenação geral de arrays em memória. É o padrão da maioria das linguagens modernas. | Pivô mal escolhido em dados patológicos faz virar O(n²). Também não é estável, então perde posição se a estabilidade importar. | Aleatório 0.04s, Ordenado 0.007s, Invertido 0.01s |
| Heap Sort | Sistemas onde o pior caso importa mais que a média. Tempo real, embarcados, garantias de latência. Também é a rede de segurança do introsort. | Cache locality ruim. Na média perde para o quicksort mesmo tendo a mesma complexidade teórica. | Aleatório 0.08s, Ordenado 0.04s, Invertido 0.05s |
| Shell Sort | Sistemas embarcados com pouca memória disponível e código enxuto. In-place, simples de implementar. | Volumes muito grandes. Nunca bate os O(n log n) puros. | Aleatório 0.08s, Ordenado 0.006s, Invertido 0.009s |
| Radix Sort | Chaves inteiras curtas, strings de tamanho fixo, ordenação de IDs numéricos. Ganha dos comparison-based nesses casos. | Não serve pra tipos que não têm representação em dígitos. Chaves muito grandes exigem muitas passadas e a vantagem some. | Aleatório 0.015s, Ordenado 0.014s, Invertido 0.015s |


## Método de Estudo:
### Por que estudei isso?
Para passar na disciplina kkkk, e para entender mais sobre o processo de ordenação que está presente em diversos softwares das mais diversas áreas, desde banco de dados (nos índices ordenados) até fora do software (relatórios empresariais). Os algoritmos de ordenação organizam os dados, o que facilita agrupamentos, busca, operações e análise.

### O que eu quero com isso?
Busquei entender os pontos chave de cada algoritmo e aprender a implementá-los. Assim consigo escolher com propriedade qual usar em cada situação, sem cair no reflexo de usar o primeiro que vem na cabeça. Isso me permite construir softwares mais rápidos e eficientes, o que aumenta a coisa mais importante que é a satisfação do usuário.

### Em que problemas esse conhecimento ira me ajudar?
Sempre que eu precisar escolher uma estrutura de ordenação vou saber qual a melhor para cada caso. Com esse estudo eu sei que o insertion sort é muito bom para dados quase ordenados, sei que o radix ignora comparação e ganha em domínios limitados, e que o quick sort quebra se o pivô for mal escolhido.

