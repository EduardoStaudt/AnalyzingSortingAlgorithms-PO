package sortgo

func BubbleSort(arr []int) {
	n := len(arr)
	for i := 0; i < n-1; i++ {
		trocou := false
		for j := 0; j < n-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
				trocou = true
			}
		}
		if !trocou {
			break
		}
	}
}
