import time
import random
import sys
from concurrent.futures import ProcessPoolExecutor

# Aumenta o limite de recursão para suportar o pior caso do pivô ruim
sys.setrecursionlimit(100000)

def quicksort_primeiro(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]  # (a) Estratégia: Primeiro Elemento
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_primeiro(left) + middle + quicksort_primeiro(right)

def quicksort_mediana3(arr):
    if len(arr) <= 1:
        return arr
    # (b) Estratégia: Mediana de Três
    a, b, c = arr[0], arr[len(arr) // 2], arr[-1]
    pivot = sorted([a, b, c])[1]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_mediana3(left) + middle + quicksort_mediana3(right)

def executar_paralelo(arr, func_pivo, workers=4):
    pivot = arr[0] if func_pivo == quicksort_primeiro else sorted([arr[0], arr[len(arr)//2], arr[-1]])[1]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        f_left = executor.submit(func_pivo, left)
        f_right = executor.submit(func_pivo, right)
        return f_left.result() + middle + f_right.result()

if __name__ == '__main__':
    N = 20_000
    print(f"=== PROBLEMA 2: IMPACTO DO PIVÔ NO QUICKSORT PARALELO (N = {N:,}) ===")
    # Vetor parcialmente ordenado (95% ordenado)
    dados = list(range(N))
    for _ in range(int(N * 0.05)):
        i, j = random.randint(0, N - 1), random.randint(0, N - 1)
        dados[i], dados[j] = dados[j], dados[i]

    t0 = time.perf_counter()
    res1 = executar_paralelo(dados.copy(), quicksort_primeiro)
    t_primeiro = time.perf_counter() - t0
    print(f"[Pivô: Primeiro Elemento] Tempo: {t_primeiro:.4f}s")

    t0 = time.perf_counter()
    res2 = executar_paralelo(dados.copy(), quicksort_mediana3)
    t_mediana = time.perf_counter() - t0
    print(f"[Pivô: Mediana de Três]   Tempo: {t_mediana:.4f}s")
    print(f"-> Ganho da Mediana de Três: {t_primeiro / t_mediana:.2f}x mais rápido!")