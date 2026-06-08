import random
from utils import distancia

def calcular_custo_rota_ag(rota, coords):
    """Calcula a soma das distâncias de Manhattan indo de R, passando pela permutação e voltando a R."""
    custo = 0
    p_atual = coords['R']
    
    for ponto in rota:
        p_prox = coords[ponto]
        custo += distancia(p_atual, p_prox)
        p_atual = p_prox
        
    custo += distancia(p_atual, coords['R'])
    return custo

def crossover_ox(pai1, pai2):
    """Order Crossover (OX): Preserva sub-rotas do Pai 1 e preenche o resto com a ordem do Pai 2."""
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
    """Mutação Swap: Sorteia duas posições do cromossomo e troca os genes de lugar."""
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(cromo)), 2)
        cromo[idx1], cromo[idx2] = cromo[idx2], cromo[idx1]
    return cromo

def algoritmo_genetico_steady_state(coords, letras, tam_pop, max_geracoes, taxa_crossover, taxa_mutacao):
    """Executa o Algoritmo Genético Steady-State e extrai pontos equidistantes da evolução."""
    if not letras: 
        return [], 0, []
    
    # 1. Criação da População Inicial (Cromossomos Aleatórios)
    populacao = []
    for _ in range(tam_pop):
        individuo = random.sample(letras, len(letras))
        custo = calcular_custo_rota_ag(individuo, coords)
        populacao.append((individuo, custo))
        
    populacao.sort(key=lambda x: x[1])
    
    historico_convergencia = []
    
    # 2. Ciclo de Substituição Estacionária (Steady-State)
    for geracao in range(1, max_geracoes + 1):
        # Torneio Binário para seleção dos pais
        def torneio():
            competidores = random.sample(populacao, 2)
            return min(competidores, key=lambda x: x[1])[0]
        
        pai1 = torneio()
        pai2 = torneio()
        
        # Operação de Cruzamento
        if random.random() < taxa_crossover:
            filho_cromo = crossover_ox(pai1, pai2)
        else:
            filho_cromo = pai1.copy()
            
        # Operação de Mutação
        filho_cromo = mutacao_swap(filho_cromo, taxa_mutacao)
        filho_custo = calcular_custo_rota_ag(filho_cromo, coords)
        
        # Reinserção Elitista: Substitui o pior da população apenas se for melhor e único
        if filho_custo < populacao[-1][1]:
            if filho_cromo not in [ind[0] for ind in populacao]:
                populacao[-1] = (filho_cromo, filho_custo)
                populacao.sort(key=lambda x: x[1])
        
        # Filtra e captura exatamente 20 registros ao longo das gerações para plotagem limpa
        if geracao == 1 or geracao % max(1, max_geracoes // 20) == 0 or geracao == max_geracoes:
            historico_convergencia.append((geracao, populacao[0][1]))

    melhor_rota, melhor_custo = populacao[0]
    return melhor_rota, melhor_custo, historico_convergencia