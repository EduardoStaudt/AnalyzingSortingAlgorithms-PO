package sortgoops

// MergeSort ordena e retorna (comparacoes, trocas).
// Aqui "trocas" = movimentacoes (cada escrita no array durante o merge),
// ja que merge sort nao faz swap tradicional.
func MergeSort(arr []int) (int64, int64) {
	if len(arr) < 2 {
		return 0, 0
	}
	var comp, troc int64
	aux := make([]int, len(arr))
	mergeSortRec(arr, aux, 0, len(arr)-1, &comp, &troc)
	return comp, troc
}

func mergeSortRec(arr, aux []int, esq, dir int, comp, troc *int64) {
	if esq >= dir {
		return
	}
	meio := (esq + dir) / 2
	mergeSortRec(arr, aux, esq, meio, comp, troc)
	mergeSortRec(arr, aux, meio+1, dir, comp, troc)
	merge(arr, aux, esq, meio, dir, comp, troc)
}

func merge(arr, aux []int, esq, meio, dir int, comp, troc *int64) {
	for i := esq; i <= dir; i++ {
		aux[i] = arr[i]
	}
	i, j := esq, meio+1
	for k := esq; k <= dir; k++ {
		if i > meio {
			arr[k] = aux[j]
			j++
			(*troc)++
		} else if j > dir {
			arr[k] = aux[i]
			i++
			(*troc)++
		} else {
			(*comp)++ // comparacao aux[i] <= aux[j]
			if aux[i] <= aux[j] {
				arr[k] = aux[i]
				i++
				(*troc)++
			} else {
				arr[k] = aux[j]
				j++
				(*troc)++
			}
		}
	}
}
