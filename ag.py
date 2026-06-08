import random

def calcular_custo_rota_ag(rota_indices, distancias):
    custo = distancias[(0, rota_indices[0])]
    for i in range(len(rota_indices) - 1):
        custo += distancias[(rota_indices[i], rota_indices[i+1])]
    custo += distancias[(rota_indices[-1], 0)]
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

def mutacao_swap(cromo, taxa_mutacao=0.2):
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(cromo)), 2)
        cromo[idx1], cromo[idx2] = cromo[idx2], cromo[idx1]
    return cromo

def algoritmo_genetico_steady_state(distancias, qtd_entregas, tam_pop, max_geracoes):
    if qtd_entregas == 0: return [], 0
    
    indices_cidades = list(range(1, qtd_entregas + 1))
    
    populacao = []
    for _ in range(tam_pop):
        individuo = random.sample(indices_cidades, len(indices_cidades))
        custo = calcular_custo_rota_ag(individuo, distancias)
        populacao.append((individuo, custo))
        
    populacao.sort(key=lambda x: x[1])
    
    # Roda exatamente até o número máximo fixado, sem interrupções
    for geracao_atual in range(max_geracoes):
        def torneio():
            competidores = random.sample(populacao, 2)
            return min(competidores, key=lambda x: x[1])[0]
        
        pai1 = torneio()
        pai2 = torneio()
        
        filho_cromo = crossover_ox(pai1, pai2)
        filho_cromo = mutacao_swap(filho_cromo)
        filho_custo = calcular_custo_rota_ag(filho_cromo, distancias)
        
        if  filho_custo < populacao[-1][1]:
            if filho_cromo not in [ind[0] for ind in populacao]:
                populacao[-1] = (filho_cromo, filho_custo)
                populacao.sort(key=lambda x: x[1])

    melhor_rota_indices, melhor_custo = populacao[0]
    return melhor_rota_indices, melhor_custo