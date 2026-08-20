package algorithms.java;

public class ShellSort {
    public static void sort(int[] arr) {
        int n = arr.length;

        int gap = 1;
        while (gap < n / 3) {
            gap = 3 * gap + 1;
        }

        while (gap > 0) {
            for (int i = gap; i < n; i++) {
                int temp = arr[i];
                int j = i;
                while (j >= gap && arr[j - gap] > temp) {
                    arr[j] = arr[j - gap];
                    j -= gap;
                }
                arr[j] = temp;
            }
            gap /= 3;
        }
    }
}
