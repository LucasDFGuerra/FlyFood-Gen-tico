import time
from ag import algoritmo_genetico_steady_state
from gerador import gerar_entregas_aleatorias
from tsplib_utils import converter_coords_para_tsplib, ler_arquivo_tsplib

def main():
    print("="*50)
    print(" ✈️ FLYFOOD TSPLIB - PAINEL DE CONTROLE FIXO ✈️ ")
    print("="*50)
    
    print("[1] Gerar Grid aleatório (Com Escala RealISTA)")
    print("[2] Ler matriz TSPLIB direta (Ex: edgesbrasil58.txt)")
    opcao = input("Opção: ").strip()
    
    arquivo_alvo = ""
    nomes_cidades = []
    
    if opcao == '1':
        num_cidades = int(input("Quantas entregas deseja gerar? "))
        print("\nGerando coordenadas e aplicando escala realista de quilometragem...")
        origem, entregas = gerar_entregas_aleatorias(num_cidades)
        
        # O arquivo será gerado multiplicando as distâncias para ficarem realistas
        arquivo_alvo, nomes_cidades = converter_coords_para_tsplib(origem, entregas, "mapa_gerado.upper.txt")
        print(f"[OK] Arquivo realista '{arquivo_alvo}' gerado com sucesso!")
        
    elif opcao == '2':
        arquivo_alvo = input("Digite o nome do arquivo (ex: edgesbrasil58.txt): ")
    else:
        print("Opção inválida.")
        return

    print(f"\nExtraindo dados do arquivo: {arquivo_alvo}...")
    distancias, qtd_entregas, nomes_extraidos = ler_arquivo_tsplib(arquivo_alvo)
    
    if opcao == '2': 
        nomes_cidades = nomes_extraidos

    print(f"Cidades detectadas: {qtd_entregas} entregas.")
    
    # =========================================================
    # DEFINIÇÃO DOS PARÂMETROS GLOBAIS
    # =========================================================
    TAMANHO_POPULACAO = 100
    MAX_GERACOES = 10000  # Modifique aqui a quantidade exata de loops que deseja
    
    print("\nIniciando o Algoritmo Genético de forma linear...")
    print(f"Configuração ativa: População={TAMANHO_POPULACAO} | Gerações Fixas={MAX_GERACOES}")
    
    inicio = time.perf_counter()
    
    melhor_rota_indices, melhor_custo = algoritmo_genetico_steady_state(
        distancias, 
        qtd_entregas, 
        tam_pop=TAMANHO_POPULACAO, 
        max_geracoes=MAX_GERACOES
    )
    
    tempo_total = time.perf_counter() - inicio
    rota_traduzida = [nomes_cidades[i] for i in melhor_rota_indices]

    print("\n" + "-"*50)
    print("🏆 RESULTADOS FINAIS 🏆")
    print("-" * 50)
    print(f"Melhor rota: {nomes_cidades[0]} -> {' -> '.join(rota_traduzida)} -> {nomes_cidades[0]}")
    print(f"Custo total calculado: {melhor_custo}")
    print(f"Gerações processadas com sucesso: {MAX_GERACOES}")
    print(f"Tempo total de execução: {tempo_total:.4f} segundos")
    print("="*50)

if __name__ == "__main__":
    main()