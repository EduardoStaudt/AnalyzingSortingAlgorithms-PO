package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	// Algoritmos normais (sem contador) -> usados pra medir TEMPO
	sortgo "AnalyzingSortingAlgorithms-PO/algorithms/go"
	// Algoritmos instrumentados (com contador) -> usados pra contar OPERACOES
	sortgoops "AnalyzingSortingAlgorithms-PO/algorithms/goops"
)

// Tamanhos da parte 2. So arquivos com esses tamanhos sao processados,
// mesmo que existam datasets menores (700k etc) na mesma pasta.
var TAMANHOS = map[int]bool{
	1_000_000: true,
	1_150_000: true,
	1_300_000: true,
	1_350_000: true,
	1_500_000: true,
	2_000_000: true,
}

// Ordem dos algoritmos ativos
var NOMES_ALGORITMOS = []string{"quick", "merge", "radix", "heap"}

// Funcao normal (mede tempo)
var FUNCAO_TEMPO = map[string]func([]int){
	"quick": sortgo.QuickSort,
	"merge": sortgo.MergeSort,
	"radix": sortgo.RadixSort,
	"heap":  sortgo.HeapSort,
}

// Funcao instrumentada (conta comparacoes e trocas)
var FUNCAO_OPS = map[string]func([]int) (int64, int64){
	"quick": sortgoops.QuickSort,
	"merge": sortgoops.MergeSort,
	"radix": sortgoops.RadixSort,
	"heap":  sortgoops.HeapSort,
}

const (
	DATASETS_DIR = "data/datasets"
	RESULTS_DIR  = "data/results"
	PREFIXO      = "go_"
	SUFIXO       = "_ops" // arquivos separados: go_quick_ops.csv etc
)

func lerArquivo(caminho string) ([]int, error) {
	arquivo, err := os.Open(caminho)
	if err != nil {
		return nil, err
	}
	defer arquivo.Close()

	scanner := bufio.NewScanner(arquivo)
	scanner.Buffer(make([]byte, 1024*1024), 1024*1024)

	if !scanner.Scan() {
		return nil, fmt.Errorf("arquivo vazio: %s", caminho)
	}
	quantidade, err := strconv.Atoi(strings.TrimSpace(scanner.Text()))
	if err != nil {
		return nil, fmt.Errorf("cabecalho invalido: %v", err)
	}

	numeros := make([]int, 0, quantidade)
	for scanner.Scan() {
		linha := strings.TrimSpace(scanner.Text())
		if linha == "" {
			continue
		}
		n, err := strconv.Atoi(linha)
		if err != nil {
			return nil, err
		}
		numeros = append(numeros, n)
	}
	return numeros, scanner.Err()
}

func parseNomeArquivo(nomeArquivo string) (tipo string, amostras int, err error) {
	base := strings.TrimSuffix(nomeArquivo, ".txt")
	partes := strings.Split(base, "_")
	if len(partes) != 2 {
		return "", 0, fmt.Errorf("formato invalido: %s", nomeArquivo)
	}
	amostras, err = strconv.Atoi(partes[1])
	if err != nil {
		return "", 0, err
	}
	return partes[0], amostras, nil
}

// Salva em go_<algoritmo>_ops.csv com colunas tipo,amostras,tempo,comparacoes,trocas
func salvarResultado(algoritmo, tipo string, amostras int, tempo float64, comp, troc int64) error {
	if err := os.MkdirAll(RESULTS_DIR, 0755); err != nil {
		return err
	}
	nomeArquivo := fmt.Sprintf("%s%s%s.csv", PREFIXO, algoritmo, SUFIXO)
	caminho := filepath.Join(RESULTS_DIR, nomeArquivo)

	_, errStat := os.Stat(caminho)
	precisaCabecalho := os.IsNotExist(errStat)

	arquivo, err := os.OpenFile(caminho, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer arquivo.Close()

	escritor := csv.NewWriter(arquivo)
	defer escritor.Flush()

	if precisaCabecalho {
		if err := escritor.Write([]string{"tipo", "amostras", "tempo", "comparacoes", "trocas"}); err != nil {
			return err
		}
	}
	return escritor.Write([]string{
		tipo,
		strconv.Itoa(amostras),
		fmt.Sprintf("%.4f", tempo),
		strconv.FormatInt(comp, 10),
		strconv.FormatInt(troc, 10),
	})
}

func processarArquivo(caminhoArquivo string) {
	nomeArquivo := filepath.Base(caminhoArquivo)
	tipo, amostras, err := parseNomeArquivo(nomeArquivo)
	if err != nil {
		return // ignora nomes fora do padrao
	}

	// So processa os tamanhos da parte 2
	if !TAMANHOS[amostras] {
		return
	}

	fmt.Printf("\n=== %s (tipo=%s, n=%d) ===\n", nomeArquivo, tipo, amostras)

	numerosOriginais, err := lerArquivo(caminhoArquivo)
	if err != nil {
		log.Printf("[ERRO] leitura %s: %v", nomeArquivo, err)
		return
	}

	for _, nome := range NOMES_ALGORITMOS {
		// PASSADA 1: mede tempo com o algoritmo normal (sem overhead de contador)
		numerosTempo := make([]int, len(numerosOriginais))
		copy(numerosTempo, numerosOriginais)

		inicio := time.Now()
		FUNCAO_TEMPO[nome](numerosTempo)
		tempo := time.Since(inicio).Seconds()

		// PASSADA 2: conta operacoes com o algoritmo instrumentado
		numerosOps := make([]int, len(numerosOriginais))
		copy(numerosOps, numerosOriginais)

		comp, troc := FUNCAO_OPS[nome](numerosOps)

		fmt.Printf("  [%s] tempo=%.4fs comp=%d troc=%d\n", nome, tempo, comp, troc)

		if err := salvarResultado(nome, tipo, amostras, tempo, comp, troc); err != nil {
			log.Printf("[ERRO] salvar: %v", err)
		}
	}
}

func main() {
	padrao := filepath.Join(DATASETS_DIR, "*.txt")
	arquivos, err := filepath.Glob(padrao)
	if err != nil {
		log.Fatalf("erro ao listar arquivos: %v", err)
	}
	if len(arquivos) == 0 {
		log.Fatalf("nenhum arquivo encontrado em %s", DATASETS_DIR)
	}

	fmt.Printf("Algoritmos: %v | Tamanhos da parte 2\n", NOMES_ALGORITMOS)

	inicioGeral := time.Now()
	for _, arquivo := range arquivos {
		processarArquivo(arquivo)
	}
	fmt.Printf("\n\nConcluido em %.2fs\n", time.Since(inicioGeral).Seconds())
}
