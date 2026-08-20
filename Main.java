import algorithms.java.*;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.function.Consumer;
import java.util.stream.Stream;

public class Main {

    record Algoritmo(String nome, Consumer<int[]> funcao) {}

    static final List<Algoritmo> ALGORITMOS = List.of(
        new Algoritmo("bubble",    BubbleSort::sort),
        new Algoritmo("insertion", InsertionSort::sort),
        new Algoritmo("merge",     MergeSort::sort),
        new Algoritmo("quick",     QuickSort::sort),
        new Algoritmo("heap",      HeapSort::sort),
        new Algoritmo("selection", SelectionSort::sort),
        new Algoritmo("shell",     ShellSort::sort),
        new Algoritmo("radix",     RadixSort::sort)
    );

    static final String DATASETS_DIR = "data/datasets";
    static final String RESULTS_DIR  = "data/results";
    static final String PREFIXO_CSV  = "java_";

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

    static void salvarResultado(String algoritmo, String tipo, int amostras, double tempo) throws IOException {
        Path pastaResults = Paths.get(RESULTS_DIR);
        Files.createDirectories(pastaResults);

        Path caminho = pastaResults.resolve(PREFIXO_CSV + algoritmo + ".csv");
        boolean precisaCabecalho = !Files.exists(caminho);

        try (BufferedWriter writer = Files.newBufferedWriter(caminho,
                StandardOpenOption.CREATE, StandardOpenOption.APPEND)) {
            if (precisaCabecalho) {
                writer.write("tipo,amostras,tempo\n");
            }
            writer.write(String.format(Locale.US, "%s,%d,%.4f%n", tipo, amostras, tempo));
        }
    }

    static void processarArquivo(Path caminhoArquivo) {
        String nomeArquivo = caminhoArquivo.getFileName().toString();
        Object[] partes;
        try {
            partes = parseNomeArquivo(nomeArquivo);
        } catch (Exception e) {
            System.err.printf("[SKIP] %s: %s%n", nomeArquivo, e.getMessage());
            return;
        }
        String tipo = (String) partes[0];
        int amostras = (int) partes[1];

        System.out.printf("%n=== %s (tipo=%s, n=%d) ===%n", nomeArquivo, tipo, amostras);

        int[] numerosOriginais;
        try {
            numerosOriginais = lerArquivo(caminhoArquivo);
        } catch (IOException e) {
            System.err.printf("[ERRO] leitura %s: %s%n", nomeArquivo, e.getMessage());
            return;
        }

        for (Algoritmo alg : ALGORITMOS) {
            int[] numeros = numerosOriginais.clone();

            long inicio = System.nanoTime();
            alg.funcao().accept(numeros);
            double duracao = (System.nanoTime() - inicio) / 1_000_000_000.0;

            System.out.printf("  [%s] %.4fs%n", alg.nome(), duracao);

            try {
                salvarResultado(alg.nome(), tipo, amostras, duracao);
            } catch (IOException e) {
                System.err.printf("[ERRO] salvar resultado: %s%n", e.getMessage());
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

        if (arquivos.isEmpty()) {
            System.err.printf("nenhum arquivo encontrado em %s%n", DATASETS_DIR);
            System.exit(1);
        }

        System.out.printf("Encontrados %d arquivos. Algoritmos ativos: %d%n",
                arquivos.size(), ALGORITMOS.size());

        long inicioGeral = System.nanoTime();
        for (Path arquivo : arquivos) {
            processarArquivo(arquivo);
        }
        double duracaoTotal = (System.nanoTime() - inicioGeral) / 1_000_000_000.0;
        System.out.printf("%n%nConcluido em %.2fs%n", duracaoTotal);
    }
}
