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

	sortgo "AnalyzingSortingAlgorithms-PO/algorithms/go"
)

type Algoritmo struct {
	Nome   string
	Funcao func([]int)
}

var ALGORITMOS = []Algoritmo{
	{Nome: "bubble", Funcao: sortgo.BubbleSort},
	{Nome: "insertion", Funcao: sortgo.InsertionSort},
	{Nome: "merge", Funcao: sortgo.MergeSort},
	{Nome: "quick", Funcao: sortgo.QuickSort},
	{Nome: "heap", Funcao: sortgo.HeapSort},
	{Nome: "selection", Funcao: sortgo.SelectionSort},
	{Nome: "shell", Funcao: sortgo.ShellSort},
	{Nome: "radix", Funcao: sortgo.RadixSort},
}

const (
	DATASETS_DIR = "data/datasets"
	RESULTS_DIR  = "data/results"
	PREFIXO_CSV  = "go_"
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

func salvarResultado(algoritmo, tipo string, amostras int, tempo float64) error {
	if err := os.MkdirAll(RESULTS_DIR, 0755); err != nil {
		return err
	}

	nomeArquivo := fmt.Sprintf("%s%s.csv", PREFIXO_CSV, algoritmo)
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
		if err := escritor.Write([]string{"tipo", "amostras", "tempo"}); err != nil {
			return err
		}
	}

	return escritor.Write([]string{
		tipo,
		strconv.Itoa(amostras),
		fmt.Sprintf("%.4f", tempo),
	})
}

func processarArquivo(caminhoArquivo string) {
	nomeArquivo := filepath.Base(caminhoArquivo)
	tipo, amostras, err := parseNomeArquivo(nomeArquivo)
	if err != nil {
		log.Printf("[SKIP] %s: %v", nomeArquivo, err)
		return
	}

	fmt.Printf("\n=== %s (tipo=%s, n=%d) ===\n", nomeArquivo, tipo, amostras)

	numerosOriginais, err := lerArquivo(caminhoArquivo)
	if err != nil {
		log.Printf("[ERRO] leitura %s: %v", nomeArquivo, err)
		return
	}

	for _, alg := range ALGORITMOS {
		numeros := make([]int, len(numerosOriginais))
		copy(numeros, numerosOriginais)

		inicio := time.Now()
		alg.Funcao(numeros)
		duracao := time.Since(inicio).Seconds()

		fmt.Printf("  [%s] %.4fs\n", alg.Nome, duracao)

		if err := salvarResultado(alg.Nome, tipo, amostras, duracao); err != nil {
			log.Printf("[ERRO] salvar resultado: %v", err)
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

	fmt.Printf("Encontrados %d arquivos. Algoritmos ativos: %d\n",
		len(arquivos), len(ALGORITMOS))

	inicioGeral := time.Now()
	for _, arquivo := range arquivos {
		processarArquivo(arquivo)
	}
	fmt.Printf("\n\nConcluido em %.2fs\n", time.Since(inicioGeral).Seconds())
}
