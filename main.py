import time
from ag import algoritmo_genetico_steady_state
from gerador import gerar_entregas_aleatorias
from tsplib_utils import converter_coords_para_tsplib, ler_arquivo_tsplib

def main():
    print("="*50)
    print(" ✈️ FLYFOOD TSPLIB - COM ALGORITMO GENÉTICO ✈️ ")
    print("="*50)
    
    print("[1] Gerar Grid aleatório e Converter para TSPLIB")
    print("[2] Ler matriz TSPLIB direta (Ex: edgesbrasil58.txt)")
    opcao = input("Opção: ").strip()
    
    arquivo_alvo = ""
    nomes_cidades = []
    
    if opcao == '1':
        num_cidades = int(input("Quantas entregas deseja gerar? "))
        print("\nGerando coordenadas e convertendo...")
        origem, entregas = gerar_entregas_aleatorias(num_cidades)
        
        arquivo_alvo, nomes_cidades = converter_coords_para_tsplib(origem, entregas, "mapa_gerado.upper.txt")
        print(f"[OK] Arquivo '{arquivo_alvo}' gerado com sucesso!")
        
    elif opcao == '2':
        arquivo_alvo = input("Digite o nome do arquivo (ex: edgesbrasil58.txt): ")
    else:
        print("Opção inválida.")
        return

    print(f"\nExtraindo Matriz TSPLIB do arquivo: {arquivo_alvo}...")
    distancias, qtd_entregas, nomes_extraidos = ler_arquivo_tsplib(arquivo_alvo)
    
    if opcao == '2': 
        nomes_cidades = nomes_extraidos

    print(f"Cidades detectadas: {qtd_entregas} entregas.")
    
    # =========================================================
    # PAINEL DE CONTROLE DO ALGORITMO GENÉTICO
    # =========================================================
    TAMANHO_POPULACAO = 100
    MAX_GERACOES = 50000       # Teto máximo de gerações
    LIMITE_ESTAGNACAO = 2000   # Corta se passar X gerações sem melhorar
    
    print("\nIniciando o Algoritmo Genético...")
    print(f"Configuração: População={TAMANHO_POPULACAO} | Limite Max={MAX_GERACOES} | Gatilho Parada={LIMITE_ESTAGNACAO}")
    
    inicio = time.perf_counter()
    
    # Passando os parâmetros definidos no MAIN para o AG
    melhor_rota_indices, melhor_custo, geracoes_reais = algoritmo_genetico_steady_state(
        distancias, 
        qtd_entregas, 
        tam_pop=TAMANHO_POPULACAO, 
        max_geracoes=MAX_GERACOES,
        limite_estagnacao=LIMITE_ESTAGNACAO
    )
    
    tempo_total = time.perf_counter() - inicio

    rota_traduzida = [nomes_cidades[i] for i in melhor_rota_indices]

    print("\n" + "-"*50)
    print("🏆 RESULTADOS FINAIS 🏆")
    print("-" * 50)
    print(f"Melhor rota: {nomes_cidades[0]} -> {' -> '.join(rota_traduzida)} -> {nomes_cidades[0]}")
    print(f"Custo total: {melhor_custo}")
    
    # Informa ao usuário se parou mais cedo ou foi até o limite
    print(f"Gerações processadas: {geracoes_reais} de {MAX_GERACOES}")
    if geracoes_reais < MAX_GERACOES:
        print("*(A Parada Inteligente cortou o processamento para poupar tempo!)*")
        
    print(f"Tempo de execução: {tempo_total:.4f} segundos")
    print("="*50)

if __name__ == "__main__":
    main()