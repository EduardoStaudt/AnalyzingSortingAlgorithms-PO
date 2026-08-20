package algorithms.java;

public class MergeSort {
    public static void sort(int[] arr) {
        if (arr.length < 2) return;
        int[] aux = new int[arr.length];
        mergeSortRec(arr, aux, 0, arr.length - 1);
    }

    private static void mergeSortRec(int[] arr, int[] aux, int esq, int dir) {
        if (esq >= dir) return;
        int meio = (esq + dir) / 2;
        mergeSortRec(arr, aux, esq, meio);
        mergeSortRec(arr, aux, meio + 1, dir);
        merge(arr, aux, esq, meio, dir);
    }

    private static void merge(int[] arr, int[] aux, int esq, int meio, int dir) {
        for (int i = esq; i <= dir; i++) {
            aux[i] = arr[i];
        }
        int i = esq, j = meio + 1;
        for (int k = esq; k <= dir; k++) {
            if (i > meio)               arr[k] = aux[j++];
            else if (j > dir)           arr[k] = aux[i++];
            else if (aux[i] <= aux[j])  arr[k] = aux[i++];
            else                        arr[k] = aux[j++];
        }
    }
}
