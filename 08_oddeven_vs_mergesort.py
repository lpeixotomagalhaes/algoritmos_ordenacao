import time
import random
from mergesort_paralelo import parallel_merge_sort
from oddeven_sort_paralelo import odd_even_sort_seq

if __name__ == '__main__':
    N = 10_000  # Altere para 50_000 se puder aguardar ~2 a 3 minutos na CPU
    print(f"=== PROBLEMA 3: ODD-EVEN SORT vs MERGESORT PARALELO (N = {N:,}) ===")
    dados = [random.randint(1, 100_000) for _ in range(N)]

    t0 = time.perf_counter()
    res_merge = parallel_merge_sort(dados.copy(), num_workers=4)
    t_merge = time.perf_counter() - t0
    print(f"[MergeSort Paralelo]         Tempo: {t_merge:.4f}s")

    t0 = time.perf_counter()
    res_oe = odd_even_sort_seq(dados.copy())
    t_oe = time.perf_counter() - t0
    print(f"[Odd-Even Transposition CPU] Tempo: {t_oe:.4f}s")
    print(f"-> Razão de desempenho: MergeSort foi {t_oe / t_merge:.1f}x mais rápido na CPU!")