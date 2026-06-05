import time
import os
from ag import algoritmo_genetico_steady_state

def executar_comparacao():
    caminhos_possiveis = ["Flyfood/input.txt", "FlyFood/input.txt", "input.txt"]
    caminho_dataset = None

    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            caminho_dataset = caminho
            break

    if caminho_dataset is None:
        print("ERRO: O arquivo 'input.txt' não foi encontrado!")
        return

    print("=" * 60)
    print("         ALGORITMO GENÉTICO (STEADY STATE) - FLYFOOD")
    print("=" * 60)
    print(f"Arquivo: '{caminho_dataset}'")
    print("-" * 60)

    print("Executando Algoritmo Genético...")
    inicio = time.perf_counter()
    rota, custo = algoritmo_genetico_steady_state(caminho_dataset, tam_pop=50, max_geracoes=3000)
    fim = time.perf_counter()
    tempo = fim - inicio

    print("=" * 60)
    print("                      RESULTADO")
    print("=" * 60)
    print(f"Rota:  {rota}")
    print(f"Custo: {custo} dms")
    print(f"Tempo: {tempo:.6f} segundos")
    print("=" * 60)

if __name__ == "__main__":
    executar_comparacao()