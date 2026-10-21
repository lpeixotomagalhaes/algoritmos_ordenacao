import time
import random
from concurrent.futures import ProcessPoolExecutor

def sort_bucket(bucket):
    return sorted(bucket)

if __name__ == '__main__':
    N = 1_000_000
    print(f"=== BUCKET SORT PARALELO (N = {N:,}) ===")
    
    # Gerando 1 milhão de transações (float de 0 a 1000)
    dados = [random.uniform(0, 1000) for _ in range(N)]
    
    t_start = time.perf_counter()
    
    # Distribuição nos 4 baldes
    b1, b2, b3, b4 = [], [], [], []
    for v in dados:
        if v <= 250: b1.append(v)
        elif v <= 500: b2.append(v)
        elif v <= 750: b3.append(v)
        else: b4.append(v)
    
    # Ordenação paralela dos 4 baldes
    with ProcessPoolExecutor(max_workers=4) as executor:
        baldes_ordenados = list(executor.map(sort_bucket, [b1, b2, b3, b4]))
    
    # Junção (Concatenação simples, pois os baldes já estão em faixas crescentes)
    resultado = baldes_ordenados[0] + baldes_ordenados[1] + baldes_ordenados[2] + baldes_ordenados[3]
    
    t_total = time.perf_counter() - t_start
    print(f"Tempo Total (Distribuição + Ordenação + Junção): {t_total:.4f}s")