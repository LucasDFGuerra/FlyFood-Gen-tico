import time
from ag import algoritmo_genetico_steady_state

caminho = "input.txt"

inicio = time.perf_counter()
rota, custo = algoritmo_genetico_steady_state(caminho, tam_pop=5000, max_geracoes=10000)
fim = time.perf_counter()

print(f"Rota: {rota}")
print(f"Custo: {custo} dms")
print(f"Tempo: {fim - inicio:.4f} segundos")