package sortgo

func ShellSort(arr []int) {
	n := len(arr)

	gap := 1
	for gap < n/3 {
		gap = 3*gap + 1
	}

	for gap > 0 {
		for i := gap; i < n; i++ {
			temp := arr[i]
			j := i
			for j >= gap && arr[j-gap] > temp {
				arr[j] = arr[j-gap]
				j -= gap
			}
			arr[j] = temp
		}
		gap /= 3
	}
}
