package sortgo

func MergeSort(arr []int) {
	if len(arr) < 2 {
		return
	}
	aux := make([]int, len(arr))
	mergeSortRec(arr, aux, 0, len(arr)-1)
}

func mergeSortRec(arr, aux []int, esq, dir int) {
	if esq >= dir {
		return
	}
	meio := (esq + dir) / 2
	mergeSortRec(arr, aux, esq, meio)
	mergeSortRec(arr, aux, meio+1, dir)
	merge(arr, aux, esq, meio, dir)
}

func merge(arr, aux []int, esq, meio, dir int) {
	for i := esq; i <= dir; i++ {
		aux[i] = arr[i]
	}
	i, j := esq, meio+1
	for k := esq; k <= dir; k++ {
		if i > meio {
			arr[k] = aux[j]
			j++
		} else if j > dir {
			arr[k] = aux[i]
			i++
		} else if aux[i] <= aux[j] {
			arr[k] = aux[i]
			i++
		} else {
			arr[k] = aux[j]
			j++
		}
	}
}
