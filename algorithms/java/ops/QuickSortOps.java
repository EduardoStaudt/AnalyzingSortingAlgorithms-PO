package algorithms.java.ops;

public class QuickSortOps {
    // Retorna comparacoes e trocas. contador[0]=comparacoes, contador[1]=trocas
    public static Ops sort(int[] arr) {
        long[] contador = {0, 0};
        quickSortRec(arr, 0, arr.length - 1, contador);
        return new Ops(contador[0], contador[1]);
    }

    private static void quickSortRec(int[] arr, int esq, int dir, long[] c) {
        if (esq < dir) {
            int pivoIdx = particionar(arr, esq, dir, c);
            quickSortRec(arr, esq, pivoIdx - 1, c);
            quickSortRec(arr, pivoIdx + 1, dir, c);
        }
    }

    private static int particionar(int[] arr, int esq, int dir, long[] c) {
        int meio = (esq + dir) / 2;
        int tmp = arr[meio]; arr[meio] = arr[dir]; arr[dir] = tmp;
        c[1]++; // troca do pivo pro fim

        int pivo = arr[dir];
        int i = esq - 1;
        for (int j = esq; j < dir; j++) {
            c[0]++; // comparacao arr[j] <= pivo
            if (arr[j] <= pivo) {
                i++;
                int t = arr[i]; arr[i] = arr[j]; arr[j] = t;
                c[1]++;
            }
        }
        int t = arr[i + 1]; arr[i + 1] = arr[dir]; arr[dir] = t;
        c[1]++;
        return i + 1;
    }
}
