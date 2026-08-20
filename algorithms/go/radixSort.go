package sortgo

func RadixSort(arr []int) {
	if len(arr) == 0 {
		return
	}

	maximo := arr[0]
	for _, v := range arr {
		if v > maximo {
			maximo = v
		}
	}

	for exp := 1; maximo/exp > 0; exp *= 10 {
		countingSortPorDigito(arr, exp)
	}
}

func countingSortPorDigito(arr []int, exp int) {
	n := len(arr)
	saida := make([]int, n)
	count := [10]int{}

	for _, v := range arr {
		digito := (v / exp) % 10
		count[digito]++
	}

	for i := 1; i < 10; i++ {
		count[i] += count[i-1]
	}

	for i := n - 1; i >= 0; i-- {
		digito := (arr[i] / exp) % 10
		count[digito]--
		saida[count[digito]] = arr[i]
	}

	copy(arr, saida)
}
