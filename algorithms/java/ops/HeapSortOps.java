package algorithms.java.ops;

public class HeapSortOps {
    public static Ops sort(int[] arr) {
        long[] contador = {0, 0};
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i, contador);
        }
        for (int i = n - 1; i > 0; i--) {
            int tmp = arr[0]; arr[0] = arr[i]; arr[i] = tmp;
            contador[1]++; // troca raiz com ultimo
            heapify(arr, i, 0, contador);
        }
        return new Ops(contador[0], contador[1]);
    }

    private static void heapify(int[] arr, int n, int i, long[] c) {
        int maior = i;
        int esq = 2 * i + 1;
        int dir = 2 * i + 2;

        if (esq < n) {
            c[0]++; // comparacao com filho esquerdo
            if (arr[esq] > arr[maior]) maior = esq;
        }
        if (dir < n) {
            c[0]++; // comparacao com filho direito
            if (arr[dir] > arr[maior]) maior = dir;
        }

        if (maior != i) {
            int tmp = arr[i]; arr[i] = arr[maior]; arr[maior] = tmp;
            c[1]++;
            heapify(arr, n, maior, c);
        }
    }
}
