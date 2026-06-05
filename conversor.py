from utils import ler_matriz, distancia

def gerar_formato_tsp(caminho_input, caminho_output):
    origem, entregas = ler_matriz(caminho_input)
    if origem is None:
        print("Erro: Origem 'R' não encontrada.")
        return

    # 'R' será o índice 0, seguido pelas entregas ordenadas alfabeticamente
    letras_ordenadas = ['R'] + sorted(list(entregas.keys()))
    coords = entregas.copy()
    coords['R'] = origem
    
    n = len(letras_ordenadas)
    linhas_tsp = []
    
    linhas_tsp.append("NAME: flyfood_convertido")
    linhas_tsp.append("TYPE: TSP")
    linhas_tsp.append(f"DIMENSION: {n}")
    linhas_tsp.append("EDGE_WEIGHT_TYPE: EXPLICIT")
    linhas_tsp.append("EDGE_WEIGHT_FORMAT: UPPER_ROW")
    linhas_tsp.append("EDGE_WEIGHT_SECTION")
    
    linha_atual = []
    for i in range(n):
        for j in range(i + 1, n):
            p1 = coords[letras_ordenadas[i]]
            p2 = coords[letras_ordenadas[j]]
            dist = distancia(p1, p2)
            linha_atual.append(str(dist))
            
            # Quebra linha a cada 15 elementos para imitar o leiaute do brasil58
            if len(linha_atual) == 15:
                linhas_tsp.append(" ".join(linha_atual))
                linha_atual = []
                
    if linha_atual:
        linhas_tsp.append(" ".join(linha_atual))
        
    linhas_tsp.append("EOF")
    
    with open(caminho_output, "w") as f:
        f.write("\n".join(linhas_tsp) + "\n")
        
    print(f"Sucesso! Arquivo convertido salvo em: {caminho_output}")
    print(f"Ordem de indexação dos nós: {letras_ordenadas}")

if __name__ == "__main__":
    # Altere os caminhos dos arquivos se necessário
    gerar_formato_tsp("Flyfood/input.txt", "flyfood_triangular.tsp")