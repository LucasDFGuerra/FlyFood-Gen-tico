import math

def converter_coords_para_tsplib(origem, entregas, nome_arquivo="mapa_gerado.upper.txt", multiplicador_escala=120):
    """Pega coordenadas, calcula Manhattan e aplica multiplicador para custos realistas."""
    nomes = ['R'] + list(entregas.keys())
    coords = [origem] + list(entregas.values())
    dimensao = len(nomes)
    
    linhas_tsp = []
    linhas_tsp.append("NAME: flyfood_convertido")
    linhas_tsp.append("TYPE: TSP")
    linhas_tsp.append(f"DIMENSION: {dimensao}")
    linhas_tsp.append("EDGE_WEIGHT_TYPE: EXPLICIT")
    linhas_tsp.append("EDGE_WEIGHT_FORMAT: UPPER_ROW")
    linhas_tsp.append("EDGE_WEIGHT_SECTION")
    
    pesos = []
    for i in range(dimensao):
        for j in range(i + 1, dimensao):
            p1 = coords[i]
            p2 = coords[j]
            # Calcula a distância e multiplica para ganhar escala realista (ex: km)
            dist = (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])) * multiplicador_escala
            pesos.append(str(dist))
    
    for i in range(0, len(pesos), 15):
        linhas_tsp.append(" ".join(pesos[i:i+15]))
        
    linhas_tsp.append("EOF\n")
    
    with open(nome_arquivo, 'w') as f:
        f.write("\n".join(linhas_tsp))
        
    return nome_arquivo, nomes

def ler_arquivo_tsplib(caminho):
    with open(caminho, 'r') as f:
        linhas = f.readlines()
    
    dimensao = 0
    inicio_pesos = 0
    
    for i, linha in enumerate(linhas):
        if linha.startswith('DIMENSION'):
            dimensao = int(linha.split(':')[1].strip())
        elif linha.startswith('EDGE_WEIGHT_SECTION'):
            inicio_pesos = i + 1
            break
            
    numeros = []
    for linha in linhas[inicio_pesos:]:
        if 'EOF' in linha: # <-- CORRIGIDO AQUI (Removido o 'line' fantasma)
            break 
        for x in linha.split():
            if x.strip().isdigit():
                numeros.append(int(x))
                
    if dimensao == 0 and len(numeros) > 0:
        total_numeros = len(numeros)
        dimensao = int((1 + math.sqrt(1 + 8 * total_numeros)) / 2)
        
    distancias = {}
    idx = 0
    for i in range(dimensao):
        distancias[(i, i)] = 0
        for j in range(i + 1, dimensao):
            peso = numeros[idx]
            distancias[(i, j)] = peso
            distancias[(j, i)] = peso
            idx += 1
            
    qtd_entregas = dimensao - 1
    nomes = ['Origem(0)'] + [f"Ponto({i})" for i in range(1, dimensao)]
    
    return distancias, qtd_entregas, nomes