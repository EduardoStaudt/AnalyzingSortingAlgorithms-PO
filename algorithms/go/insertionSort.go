package sortgo

func InsertionSort(arr []int) {
	for i := 1; i < len(arr); i++ {
		chave := arr[i]
		j := i - 1
		for j >= 0 && arr[j] > chave {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = chave
	}
}
