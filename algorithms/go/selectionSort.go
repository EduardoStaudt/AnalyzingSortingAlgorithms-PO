package sortgo

func SelectionSort(arr []int) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		menorIdx := i
		for j := i + 1; j < n; j++ {
			if arr[j] < arr[menorIdx] {
				menorIdx = j
			}
		}
		if menorIdx != i {
			arr[i], arr[menorIdx] = arr[menorIdx], arr[i]
		}
	}
}
