# 01_mergesort_paralelo.py
# Computação Paralela e Concorrente — Aulas 09
# Parallel MergeSort com Particionamento e Redução por Árvore
import time
import random
import math
from concurrent.futures import ProcessPoolExecutor


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort_seq(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return merge(merge_sort_seq(arr[:mid]), merge_sort_seq(arr[mid:]))


def parallel_merge_sort(arr, num_workers=4, threshold=10000):
    if len(arr) <= threshold:
        return merge_sort_seq(arr)

    chunk_size = math.ceil(len(arr) / num_workers)
    chunks = [arr[i : i + chunk_size] for i in range(0, len(arr), chunk_size)]
    t_bloqueio_inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        sorted_chunks = list(executor.map(merge_sort_seq, chunks))
    t_bloqueio_fim = time.perf_counter()
    
    tempo_bloqueado = t_bloqueio_fim - t_bloqueio_inicio
    print(f"-> Tempo bloqueado aguardando workers: {tempo_bloqueado:.4f}s")

    while len(sorted_chunks) > 1:
        next_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                next_chunks.append(
                    merge(sorted_chunks[i], sorted_chunks[i + 1])
                )
            else:
                next_chunks.append(sorted_chunks[i])
        sorted_chunks = next_chunks

    return sorted_chunks[0]


if __name__ == "__main__":
   if __name__ == '__main__':
    N = 1_000_000
    # Altere ESTE valor para testar: 100, 1000, 10000, 50000, 100000
    THRESHOLD_TESTE = 50000 
    
    print(f"=== BENCHMARK MERGESORT PARALELO (N = {N:,} | Threshold = {THRESHOLD_TESTE}) ===")
    dados = [random.randint(1, 10_000_000) for _ in range(N)]
    
    # 1. Execução Sequencial
    t_start = time.perf_counter()
    res_seq = merge_sort_seq(dados.copy())
    t_seq = time.perf_counter() - t_start
    print(f"[Sequencial] Tempo: {t_seq:.4f}s")
    
    # 2. Execução Paralela (4 Cores)
    t_start = time.perf_counter()
    # Adicione a variável threshold aqui na chamada da função:
    res_par = parallel_merge_sort(dados, num_workers=4, threshold=THRESHOLD_TESTE) 
    t_par = time.perf_counter() - t_start

    speedup = t_seq / t_par if t_par > 0 else 0
    eficiencia = (speedup / 4) * 100
    print(
        f"[Paralelo 4 Cores] Tempo: {t_par:.4f}s | "
        f"Speedup: {speedup:.2f}x | Eficiência: {eficiencia:.1f}%"
    )

    assert res_seq == res_par, "Erro: Inconsistência nos resultados!"
    print("✓ Validação: Resultados idênticos com sucesso!")
