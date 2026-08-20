package algorithms.java;

public class SelectionSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int menorIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[menorIdx]) {
                    menorIdx = j;
                }
            }
            if (menorIdx != i) {
                int tmp = arr[i]; arr[i] = arr[menorIdx]; arr[menorIdx] = tmp;
            }
        }
    }
}
