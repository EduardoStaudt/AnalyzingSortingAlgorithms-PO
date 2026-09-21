package sortgoops

// HeapSort ordena e retorna (comparacoes, trocas).
func HeapSort(arr []int) (int64, int64) {
	var comp, troc int64
	n := len(arr)
	for i := n/2 - 1; i >= 0; i-- {
		heapify(arr, n, i, &comp, &troc)
	}
	for i := n - 1; i > 0; i-- {
		arr[0], arr[i] = arr[i], arr[0]
		troc++ // troca raiz com ultimo
		heapify(arr, i, 0, &comp, &troc)
	}
	return comp, troc
}

func heapify(arr []int, n, i int, comp, troc *int64) {
	maior := i
	esq := 2*i + 1
	dir := 2*i + 2

	if esq < n {
		(*comp)++ // comparacao com filho esquerdo
		if arr[esq] > arr[maior] {
			maior = esq
		}
	}
	if dir < n {
		(*comp)++ // comparacao com filho direito
		if arr[dir] > arr[maior] {
			maior = dir
		}
	}

	if maior != i {
		arr[i], arr[maior] = arr[maior], arr[i]
		(*troc)++
		heapify(arr, n, maior, comp, troc)
	}
}
