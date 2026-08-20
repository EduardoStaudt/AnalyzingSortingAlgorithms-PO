package algorithms.java;

public class QuickSort {
    public static void sort(int[] arr) {
        quickSortRec(arr, 0, arr.length - 1);
    }

    private static void quickSortRec(int[] arr, int esq, int dir) {
        if (esq < dir) {
            int pivoIdx = particionar(arr, esq, dir);
            quickSortRec(arr, esq, pivoIdx - 1);
            quickSortRec(arr, pivoIdx + 1, dir);
        }
    }

    private static int particionar(int[] arr, int esq, int dir) {
        int meio = (esq + dir) / 2;
        int tmp = arr[meio]; arr[meio] = arr[dir]; arr[dir] = tmp;

        int pivo = arr[dir];
        int i = esq - 1;
        for (int j = esq; j < dir; j++) {
            if (arr[j] <= pivo) {
                i++;
                int t = arr[i]; arr[i] = arr[j]; arr[j] = t;
            }
        }
        int t = arr[i + 1]; arr[i + 1] = arr[dir]; arr[dir] = t;
        return i + 1;
    }
}
