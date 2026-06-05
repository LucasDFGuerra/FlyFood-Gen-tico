import random

def gerar_entregas_aleatorias(qtd_cidades, limite_mapa=100):
    """
    Gera automaticamente pontos de entrega aleatórios em um grid.
    Evita que duas cidades caiam na mesma coordenada.
    """
    coordenadas_usadas = set()
    
    # Define a Origem (R) em uma posição aleatória
    origem_coord = (random.randint(0, limite_mapa), random.randint(0, limite_mapa))
    coordenadas_usadas.add(origem_coord)
    
    entregas = {}
    
    # Gera as outras cidades (usando nomes como C1, C2, C3...)
    for i in range(1, qtd_cidades + 1):
        nome_cidade = f"C{i}" 
        
        while True:
            coord = (random.randint(0, limite_mapa), random.randint(0, limite_mapa))
            if coord not in coordenadas_usadas:
                coordenadas_usadas.add(coord)
                entregas[nome_cidade] = coord
                break
                
    return origem_coord, entregas