package sortgoops

// RadixSort ordena e retorna (comparacoes, trocas).
// Radix NAO usa comparacoes, entao comparacoes = 0.
// "trocas" = escritas no array de saida em cada passada de digito.
// Este resultado nao entra nos graficos de operacoes, mas o algoritmo
// ainda roda aqui para medir tempo junto com os outros.
func RadixSort(arr []int) (int64, int64) {
	if len(arr) == 0 {
		return 0, 0
	}
	var troc int64

	maximo := arr[0]
	for _, v := range arr {
		if v > maximo {
			maximo = v
		}
	}

	for exp := 1; maximo/exp > 0; exp *= 10 {
		countingSortPorDigito(arr, exp, &troc)
	}
	return 0, troc
}

func countingSortPorDigito(arr []int, exp int, troc *int64) {
	n := len(arr)
	saida := make([]int, n)
	count := [10]int{}

	for _, v := range arr {
		digito := (v / exp) % 10
		count[digito]++
	}
	for i := 1; i < 10; i++ {
		count[i] += count[i-1]
	}
	for i := n - 1; i >= 0; i-- {
		digito := (arr[i] / exp) % 10
		count[digito]--
		saida[count[digito]] = arr[i]
		(*troc)++ // escrita no array de saida
	}
	copy(arr, saida)
}
