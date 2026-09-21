package algorithms.java.ops;

public class RadixSortOps {
    // Radix NAO usa comparacoes, entao comparacoes = 0.
    // "trocas" = escritas no array de saida. Nao entra nos graficos de operacoes.
    public static Ops sort(int[] arr) {
        if (arr.length == 0) return new Ops(0, 0);
        long[] contador = {0, 0};

        int maximo = arr[0];
        for (int v : arr) {
            if (v > maximo) maximo = v;
        }
        for (int exp = 1; maximo / exp > 0; exp *= 10) {
            countingSortPorDigito(arr, exp, contador);
        }
        return new Ops(0, contador[1]);
    }

    private static void countingSortPorDigito(int[] arr, int exp, long[] c) {
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
            c[1]++; // escrita no array de saida
        }
        System.arraycopy(saida, 0, arr, 0, n);
    }
}
