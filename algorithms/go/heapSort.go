package sortgo

func HeapSort(arr []int) {
	n := len(arr)
	for i := n/2 - 1; i >= 0; i-- {
		heapify(arr, n, i)
	}
	for i := n - 1; i > 0; i-- {
		arr[0], arr[i] = arr[i], arr[0]
		heapify(arr, i, 0)
	}
}

func heapify(arr []int, n, i int) {
	maior := i
	esq := 2*i + 1
	dir := 2*i + 2

	if esq < n && arr[esq] > arr[maior] {
		maior = esq
	}
	if dir < n && arr[dir] > arr[maior] {
		maior = dir
	}

	if maior != i {
		arr[i], arr[maior] = arr[maior], arr[i]
		heapify(arr, n, maior)
	}
}
