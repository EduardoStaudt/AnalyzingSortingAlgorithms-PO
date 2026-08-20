package algorithms.java;

public class RadixSort {
    public static void sort(int[] arr) {
        if (arr.length == 0) return;

        int maximo = arr[0];
        for (int v : arr) {
            if (v > maximo) maximo = v;
        }

        for (int exp = 1; maximo / exp > 0; exp *= 10) {
            countingSortPorDigito(arr, exp);
        }
    }

    private static void countingSortPorDigito(int[] arr, int exp) {
        int n = arr.length;
        int[] saida = new int[n];
        int[] count = new int[10];

        for (int v : arr) {
            int digito = (v / exp) % 10;
            count[digito]++;
        }

        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }

        for (int i = n - 1; i >= 0; i--) {
            int digito = (arr[i] / exp) % 10;
            count[digito]--;
            saida[count[digito]] = arr[i];
        }

        System.arraycopy(saida, 0, arr, 0, n);
    }
}
