import math

def converter_coords_para_tsplib(origem, entregas, nome_arquivo="gerado.upper.txt"):
    """Pega coordenadas físicas, calcula Manhattan e cria um arquivo formato TSPLIB."""
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
            dist = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) 
            pesos.append(str(dist))
    
    for i in range(0, len(pesos), 15):
        linhas_tsp.append(" ".join(pesos[i:i+15]))
        
    linhas_tsp.append("EOF\n")
    
    with open(nome_arquivo, 'w') as f:
        f.write("\n".join(linhas_tsp))
        
    return nome_arquivo, nomes

def ler_arquivo_tsplib(caminho):
    """Lê um arquivo .txt no formato TSPLIB (com cabeçalho) ou RAW (só números)."""
    with open(caminho, 'r') as f:
        linhas = f.readlines()
    
    dimensao = 0
    inicio_pesos = 0
    
    # 1. Tenta achar o cabeçalho (Para os arquivos que nós mesmos geramos)
    for i, linha in enumerate(linhas):
        if linha.startswith('DIMENSION'):
            dimensao = int(linha.split(':')[1].strip())
        elif linha.startswith('EDGE_WEIGHT_SECTION'):
            inicio_pesos = i + 1
            break
            
    # 2. Extrai todos os números do arquivo
    numeros = []
    for linha in linhas[inicio_pesos:]:
        if 'EOF' in linha: break
        # Pega só o que é número (Ignora eventuais palavras perdidas)
        for x in linha.split():
            if x.strip().isdigit():
                numeros.append(int(x))
                
    # 3. A MÁGICA: Se não tinha cabeçalho, calcula a dimensão matematicamente!
    if dimensao == 0 and len(numeros) > 0:
        total_numeros = len(numeros)
        # Fórmula para achar a dimensão (N) a partir de uma matriz triangular superior
        dimensao = int((1 + math.sqrt(1 + 8 * total_numeros)) / 2)
        
    # Monta o dicionário de distâncias
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