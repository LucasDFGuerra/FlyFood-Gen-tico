import random
from utils import ler_matriz, distancia

def calcular_custo_rota_ag(rota, coords):
    """Calcula o custo de uma rota do AG (vai de R, passa pelas letras e volta a R)."""
    custo = 0
    p_atual = coords['R']
    
    for ponto in rota:
        p_prox = coords[ponto]
        custo += distancia(p_atual, p_prox)
        p_atual = p_prox
        
    custo += distancia(p_atual, coords['R'])
    return custo

def crossover_ox(pai1, pai2):
    """Order Crossover (OX) para manter a integridade da permutação sem duplicar cidades."""
    tamanho = len(pai1)
    pt1, pt2 = sorted(random.sample(range(tamanho), 2))
    
    filho = [None] * tamanho
    filho[pt1:pt2+1] = pai1[pt1:pt2+1]
    
    pos_filho = (pt2 + 1) % tamanho
    pos_pai2 = (pt2 + 1) % tamanho
    
    # Executa o loop enquanto ainda existirem espaços vazios (None) no filho
    while None in filho:
        if pai2[pos_pai2] not in filho:
            filho[pos_filho] = pai2[pos_pai2]
            pos_filho = (pos_filho + 1) % tamanho
        pos_pai2 = (pos_pai2 + 1) % tamanho
            
    return filho

def mutacao_swap(cromo, taxa_mutacao=0.2):
    """Inverte a posição de duas entregas aleatórias."""
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(cromo)), 2)
        cromo[idx1], cromo[idx2] = cromo[idx2], cromo[idx1]
    return cromo

def algoritmo_genetico_steady_state(caminho_arquivo, tam_pop=50, max_geracoes=2000):
    origem, entregas = ler_matriz(caminho_arquivo)
    if not entregas: return "", 0
    
    letras = list(entregas.keys())
    coords = entregas.copy()
    coords['R'] = origem
    
    # 1. Inicialização da População
    populacao = []
    for _ in range(tam_pop):
        individuo = random.sample(letras, len(letras))
        custo = calcular_custo_rota_ag(individuo, coords)
        populacao.append((individuo, custo))
        
    populacao.sort(key=lambda x: x[1])
    
    # 2. Loop de Gerações (Substituições Estacionárias)
    for _ in range(max_geracoes):
        # Seleção de Pais por Torneio Binário
        def torneio():
            competidores = random.sample(populacao, 2)
            return min(competidores, key=lambda x: x[1])[0]
        
        pai1 = torneio()
        pai2 = torneio()
        
        # Cruzamento e Mutação
        filho_cromo = crossover_ox(pai1, pai2)
        filho_cromo = mutacao_swap(filho_cromo)
        filho_custo = calcular_custo_rota_ag(filho_cromo, coords)
        
        # Seleção de Sobreviventes (Steady State)
        # Substitui o pior indivíduo se o filho for melhor e não for uma cópia exata
        if filho_custo < populacao[-1][1]:
            if filho_cromo not in [ind[0] for ind in populacao]:
                populacao[-1] = (filho_cromo, filho_custo)
                populacao.sort(key=lambda x: x[1])

    melhor_rota, melhor_custo = populacao[0]
    return " ".join(melhor_rota), melhor_custo