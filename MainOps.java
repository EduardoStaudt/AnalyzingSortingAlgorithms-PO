import algorithms.java.*;
import algorithms.java.ops.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.stream.Stream;

public class MainOps {

    // Tamanhos da parte 2. So arquivos com esses tamanhos sao processados.
    static final Set<Integer> TAMANHOS = Set.of(
        1_000_000, 1_150_000, 1_300_000, 1_350_000, 1_500_000, 2_000_000
    );

    static final List<String> NOMES = List.of("quick", "merge", "radix", "heap");

    // Funcao normal (mede tempo)
    static final Map<String, Consumer<int[]>> FUNCAO_TEMPO = Map.of(
        "quick", QuickSort::sort,
        "merge", MergeSort::sort,
        "radix", RadixSort::sort,
        "heap",  HeapSort::sort
    );

    // Funcao instrumentada (conta comparacoes e trocas)
    static final Map<String, Function<int[], Ops>> FUNCAO_OPS = Map.of(
        "quick", QuickSortOps::sort,
        "merge", MergeSortOps::sort,
        "radix", RadixSortOps::sort,
        "heap",  HeapSortOps::sort
    );

    static final String DATASETS_DIR = "data/datasets";
    static final String RESULTS_DIR  = "data/results";
    static final String PREFIXO      = "java_";
    static final String SUFIXO       = "_ops";

    static int[] lerArquivo(Path caminho) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(caminho)) {
            int quantidade = Integer.parseInt(reader.readLine().trim());
            int[] numeros = new int[quantidade];
            int idx = 0;
            String linha;
            while ((linha = reader.readLine()) != null) {
                linha = linha.trim();
                if (linha.isEmpty()) continue;
                numeros[idx++] = Integer.parseInt(linha);
            }
            return (idx == quantidade) ? numeros : Arrays.copyOf(numeros, idx);
        }
    }

    static Object[] parseNomeArquivo(String nomeArquivo) {
        String base = nomeArquivo.replaceAll("\\.txt$", "");
        String[] partes = base.split("_");
        if (partes.length != 2) {
            throw new IllegalArgumentException("formato invalido: " + nomeArquivo);
        }
        return new Object[]{ partes[0], Integer.parseInt(partes[1]) };
    }

    // Salva em java_<algoritmo>_ops.csv com tipo,amostras,tempo,comparacoes,trocas
    static void salvarResultado(String algoritmo, String tipo, int amostras,
                                double tempo, long comp, long troc) throws IOException {
        Path pasta = Paths.get(RESULTS_DIR);
        Files.createDirectories(pasta);
        Path caminho = pasta.resolve(PREFIXO + algoritmo + SUFIXO + ".csv");
        boolean precisaCabecalho = !Files.exists(caminho);

        try (BufferedWriter writer = Files.newBufferedWriter(caminho,
                StandardOpenOption.CREATE, StandardOpenOption.APPEND)) {
            if (precisaCabecalho) {
                writer.write("tipo,amostras,tempo,comparacoes,trocas\n");
            }
            writer.write(String.format(Locale.US, "%s,%d,%.4f,%d,%d%n",
                    tipo, amostras, tempo, comp, troc));
        }
    }

    static void processarArquivo(Path caminhoArquivo) {
        String nomeArquivo = caminhoArquivo.getFileName().toString();
        Object[] partes;
        try {
            partes = parseNomeArquivo(nomeArquivo);
        } catch (Exception e) {
            return;
        }
        String tipo = (String) partes[0];
        int amostras = (int) partes[1];

        if (!TAMANHOS.contains(amostras)) return;

        System.out.printf("%n=== %s (tipo=%s, n=%d) ===%n", nomeArquivo, tipo, amostras);

        int[] numerosOriginais;
        try {
            numerosOriginais = lerArquivo(caminhoArquivo);
        } catch (IOException e) {
            System.err.printf("[ERRO] leitura %s: %s%n", nomeArquivo, e.getMessage());
            return;
        }

        for (String nome : NOMES) {
            // PASSADA 1: mede tempo com algoritmo normal
            int[] numerosTempo = numerosOriginais.clone();
            long inicio = System.nanoTime();
            FUNCAO_TEMPO.get(nome).accept(numerosTempo);
            double tempo = (System.nanoTime() - inicio) / 1_000_000_000.0;

            // PASSADA 2: conta operacoes com algoritmo instrumentado
            int[] numerosOps = numerosOriginais.clone();
            Ops ops = FUNCAO_OPS.get(nome).apply(numerosOps);

            System.out.printf("  [%s] tempo=%.4fs comp=%d troc=%d%n",
                    nome, tempo, ops.comparacoes(), ops.trocas());

            try {
                salvarResultado(nome, tipo, amostras, tempo, ops.comparacoes(), ops.trocas());
            } catch (IOException e) {
                System.err.printf("[ERRO] salvar: %s%n", e.getMessage());
            }
        }
    }

    public static void main(String[] args) throws IOException {
        Path datasetsDir = Paths.get(DATASETS_DIR);
        if (!Files.isDirectory(datasetsDir)) {
            System.err.printf("nenhum arquivo encontrado em %s%n", DATASETS_DIR);
            System.exit(1);
        }

        List<Path> arquivos;
        try (Stream<Path> stream = Files.list(datasetsDir)) {
            arquivos = stream
                .filter(p -> p.toString().endsWith(".txt"))
                .sorted()
                .toList();
        }

        System.out.printf("Algoritmos: %s | Tamanhos da parte 2%n", NOMES);

        long inicioGeral = System.nanoTime();
        for (Path arquivo : arquivos) {
            processarArquivo(arquivo);
        }
        double total = (System.nanoTime() - inicioGeral) / 1_000_000_000.0;
        System.out.printf("%n%nConcluido em %.2fs%n", total);
    }
}
