package sortgo

func QuickSort(arr []int) {
	quickSortRec(arr, 0, len(arr)-1)
}

func quickSortRec(arr []int, esq, dir int) {
	if esq < dir {
		pivoIdx := particionar(arr, esq, dir)
		quickSortRec(arr, esq, pivoIdx-1)
		quickSortRec(arr, pivoIdx+1, dir)
	}
}

func particionar(arr []int, esq, dir int) int {
	meio := (esq + dir) / 2
	arr[meio], arr[dir] = arr[dir], arr[meio]
	pivo := arr[dir]

	i := esq - 1
	for j := esq; j < dir; j++ {
		if arr[j] <= pivo {
			i++
			arr[i], arr[j] = arr[j], arr[i]
		}
	}
	arr[i+1], arr[dir] = arr[dir], arr[i+1]
	return i + 1
}
