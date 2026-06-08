import random
import time
import urllib.request
import ssl

# ==============================================================================
# 🎛️ CONFIGURAÇÃO DOS PARÂMETROS DO AG STEADY-STATE
# ==============================================================================
TAMANHO_POPULACAO = 100
MAX_GERACOES = 500000   # Ciclos de substituição do Steady-State
TAXA_CROSSOVER = 0.9    # 90%
TAXA_MUTACAO = 0.25     # 25%
NUM_CIDADES = 58        # Instância brazil58
# ==============================================================================

def carregar_matriz_brazil58_online():
    """
    Faz o download da matriz UPPER_ROW oficial diretamente do repositório da TSPLIB no GitHub,
    garantindo que os dados originais (sem formatação corrompida) sejam utilizados.
    """
    url = "https://raw.githubusercontent.com/mastqe/tsplib/master/brazil58.tsp"
    print("🌐 Conectando ao repositório TSPLIB no GitHub e baixando a matriz brazil58...")
    
    # Ignora verificação de certificado SSL local para evitar bloqueios de rede/antivírus
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(url, context=ctx) as response:
            linhas = response.read().decode('utf-8').splitlines()
        print("✅ Dados baixados com sucesso!")
    except Exception as e:
        print(f"❌ ERRO ao tentar baixar os dados da internet: {e}")
        return None

    pesos = []
    lendo = False
    for linha in linhas:
        if "EDGE_WEIGHT_SECTION" in linha:
            lendo = True
            continue
        if "EOF" in linha:
            break
        if lendo:
            # Captura todos os números na linha e adiciona na lista linear de pesos
            pesos.extend([int(x) for x in linha.split() if x.strip()])
            
    if len(pesos) == 0:
        print("❌ ERRO: O arquivo foi baixado, mas nenhuma distância foi encontrada.")
        return None
        
    print(f"✅ Matriz interpretada: {len(pesos)} distâncias carregadas na estrutura (Upper Row).")

    # Reconstrói a Matriz Simétrica 58x58 no formato legível pelo Algoritmo Genético
    matriz = [[0]*NUM_CIDADES for _ in range(NUM_CIDADES)]
    idx = 0
    for i in range(NUM_CIDADES):
        for j in range(i+1, NUM_CIDADES):
            if idx < len(pesos):
                matriz[i][j] = pesos[idx]
                matriz[j][i] = pesos[idx]
                idx += 1
                
    return matriz

def calcular_custo_rota(rota, matriz_dist):
    custo = 0
    for i in range(len(rota) - 1):
        custo += matriz_dist[rota[i]][rota[i+1]]
    custo += matriz_dist[rota[-1]][rota[0]]
    return custo

def crossover_ox(pai1, pai2):
    tamanho = len(pai1)
    pt1, pt2 = sorted(random.sample(range(tamanho), 2))
    filho = [None] * tamanho
    filho[pt1:pt2+1] = pai1[pt1:pt2+1]
    
    pos_filho = (pt2 + 1) % tamanho
    pos_pai2 = (pt2 + 1) % tamanho
    
    while None in filho:
        if pai2[pos_pai2] not in filho:
            filho[pos_filho] = pai2[pos_pai2]
            pos_filho = (pos_filho + 1) % tamanho
        pos_pai2 = (pos_pai2 + 1) % tamanho
    return filho

def mutacao_swap(cromo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(cromo)), 2)
        cromo[idx1], cromo[idx2] = cromo[idx2], cromo[idx1]
    return cromo

def algoritmo_genetico_steady_state(matriz_dist):
    populacao = []
    for _ in range(TAMANHO_POPULACAO):
        individuo = random.sample(range(NUM_CIDADES), NUM_CIDADES)
        custo = calcular_custo_rota(individuo, matriz_dist)
        populacao.append((individuo, custo))
        
    populacao.sort(key=lambda x: x[1])
    historico_convergencia = []
    
    for geracao in range(1, MAX_GERACOES + 1):
        def torneio():
            comp = random.sample(populacao, 2)
            return min(comp, key=lambda x: x[1])[0]
        
        pai1 = torneio()
        pai2 = torneio()
        
        if random.random() < TAXA_CROSSOVER:
            filho_cromo = crossover_ox(pai1, pai2)
        else:
            filho_cromo = pai1.copy()
            
        filho_cromo = mutacao_swap(filho_cromo, TAXA_MUTACAO)
        filho_custo = calcular_custo_rota(filho_cromo, matriz_dist)
        
        if filho_custo < populacao[-1][1]:
            if filho_cromo not in [ind[0] for ind in populacao]:
                populacao[-1] = (filho_cromo, filho_custo)
                populacao.sort(key=lambda x: x[1])
        
        if geracao == 1 or geracao % (MAX_GERACOES // 20) == 0 or geracao == MAX_GERACOES:
            historico_convergencia.append((geracao, populacao[0][1]))

    return populacao[0][0], populacao[0][1], historico_convergencia

def main():
    matriz_dist = carregar_matriz_brazil58_online()
    if not matriz_dist:
        return

    print("\n" + "=" * 60)
    print(" 🚀 AG STEADY-STATE (MATRIZ VIA REDE - TSPLIB) ".center(60, "="))
    print("=" * 60)
    print(f"📋 População: {TAMANHO_POPULACAO} | Gerações: {MAX_GERACOES} | Crossover: {TAXA_CROSSOVER*100}% | Mutação: {TAXA_MUTACAO*100}%")
    print("-" * 60)
    print("Evoluindo a população... Aguarde o processamento.")
    
    random.seed(time.time()) 
    inicio_tempo = time.perf_counter()
    melhor_rota, melhor_custo, historico = algoritmo_genetico_steady_state(matriz_dist)
    tempo_execucao = time.perf_counter() - inicio_tempo
    
    print("\n" + "🏆 RESULTADO OTIMIZADO DA INSTÂNCIA ".center(60, "="))
    print(f"📉 Melhor Custo Alcançado: {melhor_custo} (O Ótimo matemático da literatura é ~25.395)")
    print(f"⏱️ Tempo de Processamento: {tempo_execucao:.4f} segundos")
    print("=" * 60)
    
    print("\n📈 DADOS PARA O GRÁFICO DE CONVERGÊNCIA (Copie e cole no seu relatório):")
    print(f"{'Geração':<15} | {'Custo Mínimo Obtido':<20}")
    print("-" * 40)
    for ger, cst in historico:
        print(f"{ger:<15} | {cst:<20}")
    print("-" * 40)

if __name__ == "__main__":
    main()