import itertools
from utils import distancia

def calcular_custo_rota(rota_completa, coordenadas):
    """Calcula o custo total de uma rota indo de ponto em ponto."""
    custo = 0
    for i in range(len(rota_completa) - 1):
        p1 = coordenadas[rota_completa[i]]
        p2 = coordenadas[rota_completa[i+1]]
        custo += distancia(p1, p2)
    return custo

def forca_bruta(origem_coord, pontos_entrega):
    if not pontos_entrega:
        return "", 0

    letras_entrega = list(pontos_entrega.keys())
    coords = pontos_entrega.copy()
    coords['R'] = origem_coord

    melhor_rota = None
    menor_custo = float('inf')

    for perm in itertools.permutations(letras_entrega):
        rota_teste = ('R',) + perm + ('R',)
        custo_atual = calcular_custo_rota(rota_teste, coords)
        
        if custo_atual < menor_custo:
            menor_custo = custo_atual
            melhor_rota = perm

    return " ".join(melhor_rota), menor_custo