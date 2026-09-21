// Pacote sortgoops = versao instrumentada dos algoritmos, que conta
// comparacoes e trocas em vez de so ordenar. Separado do pacote sortgo
// pra nao adicionar overhead de contagem na medicao de tempo.
package sortgoops

// QuickSort ordena e retorna (comparacoes, trocas).
func QuickSort(arr []int) (int64, int64) {
	var comp, troc int64
	quickSortRec(arr, 0, len(arr)-1, &comp, &troc)
	return comp, troc
}

func quickSortRec(arr []int, esq, dir int, comp, troc *int64) {
	if esq < dir {
		pivoIdx := particionar(arr, esq, dir, comp, troc)
		quickSortRec(arr, esq, pivoIdx-1, comp, troc)
		quickSortRec(arr, pivoIdx+1, dir, comp, troc)
	}
}

func particionar(arr []int, esq, dir int, comp, troc *int64) int {
	meio := (esq + dir) / 2
	arr[meio], arr[dir] = arr[dir], arr[meio]
	(*troc)++ // troca do pivo pro fim
	pivo := arr[dir]

	i := esq - 1
	for j := esq; j < dir; j++ {
		(*comp)++ // comparacao arr[j] <= pivo
		if arr[j] <= pivo {
			i++
			arr[i], arr[j] = arr[j], arr[i]
			(*troc)++
		}
	}
	arr[i+1], arr[dir] = arr[dir], arr[i+1]
	(*troc)++
	return i + 1
}
