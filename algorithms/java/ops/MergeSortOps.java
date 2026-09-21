package algorithms.java.ops;

public class MergeSortOps {
    // "trocas" aqui = movimentacoes (escritas no array durante o merge)
    public static Ops sort(int[] arr) {
        long[] contador = {0, 0};
        if (arr.length < 2) return new Ops(0, 0);
        int[] aux = new int[arr.length];
        mergeSortRec(arr, aux, 0, arr.length - 1, contador);
        return new Ops(contador[0], contador[1]);
    }

    private static void mergeSortRec(int[] arr, int[] aux, int esq, int dir, long[] c) {
        if (esq >= dir) return;
        int meio = (esq + dir) / 2;
        mergeSortRec(arr, aux, esq, meio, c);
        mergeSortRec(arr, aux, meio + 1, dir, c);
        merge(arr, aux, esq, meio, dir, c);
    }

    private static void merge(int[] arr, int[] aux, int esq, int meio, int dir, long[] c) {
        for (int i = esq; i <= dir; i++) {
            aux[i] = arr[i];
        }
        int i = esq, j = meio + 1;
        for (int k = esq; k <= dir; k++) {
            if (i > meio) {
                arr[k] = aux[j++];
                c[1]++;
            } else if (j > dir) {
                arr[k] = aux[i++];
                c[1]++;
            } else {
                c[0]++; // comparacao aux[i] <= aux[j]
                if (aux[i] <= aux[j]) {
                    arr[k] = aux[i++];
                    c[1]++;
                } else {
                    arr[k] = aux[j++];
                    c[1]++;
                }
            }
        }
    }
}
