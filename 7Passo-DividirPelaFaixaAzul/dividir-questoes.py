from PIL import Image
import os

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores do GIMP (0-100) para RGB (0-255)
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def verificar_cor(pixel, cor_alvo, tolerancia=15):
    """
    Verifica se um pixel RGB/RGBA está dentro da tolerância da cor alvo
    """
    if len(pixel) == 4:  # RGBA
        r, g, b, a = pixel
    else:  # RGB
        r, g, b = pixel[:3]
        
    return (abs(r - cor_alvo[0]) <= tolerancia and 
            abs(g - cor_alvo[1]) <= tolerancia and 
            abs(b - cor_alvo[2]) <= tolerancia)

def encontrar_padrao_vertical(imagem, tolerancia_cor=15):
    """
    Encontra posições com o padrão vertical de 5 faixas no pixel central:
    1) 2px (35, 31, 32)
    2) 2px (255, 255, 255)
    3) 4px (35, 31, 32)
    4) 3px (255, 255, 255)
    5) 1px (35, 31, 32)
    Margem de erro de tamanho: ±1 pixel em cada faixa.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    x_central = largura // 2  # Percorrer o pixel central
    
    # Definição do padrão: (Cor RGB, Tamanho Alvo)
    padrao = [
        ((35, 31, 32), 2),
        ((255, 255, 255), 2),
        ((35, 31, 32), 4),
        ((255, 255, 255), 3),
        ((35, 31, 32), 1)
    ]
    
    posicoes_corte = []
    y = 0
    
    # Altura máxima aproximada do padrão total (~12px) mais margens
    while y < altura - 20:
        y_atual = y
        padrao_valido = True
        
        # Analisa cada uma das 5 faixas sequencialmente
        for cor_alvo, tam_alvo in padrao:
            tam_detectado = 0
            
            # Conta quantos pixels seguidos pertencem à cor da faixa atual
            while y_atual < altura and verificar_cor(pixels[x_central, y_atual], cor_alvo, tolerancia_cor):
                tam_detectado += 1
                y_atual += 1
                # Limita a busca para não passar muito do tamanho máximo aceitável (tam_alvo + 1)
                if tam_detectado > tam_alvo + 1:
                    break
            
            # Valida com a margem de erro de ±1 pixel no tamanho da faixa
            if tam_detectado < (tam_alvo - 1) or tam_detectado > (tam_alvo + 1):
                padrao_valido = False
                break
                
        if padrao_valido:
            # Corta 15 pixels ACIMA do padrão começar
            posicao_corte = y - 20
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Padrão visual encontrado em y={y}, cortando em y={posicao_corte}")
            
            # Avança o ponteiro 'y' para o final do padrão detectado para evitar re-detecção
            y = y_atual
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente cortando ANTES das faixas do padrão
    """
    # Abre a imagem
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    # Encontra as posições com base no padrão de 5 faixas
    posicoes_corte = encontrar_padrao_vertical(imagem)
    
    if not posicoes_corte:
        print("Nenhum padrão visual encontrado na imagem!")
        return
    
    print(f"Encontrados {len(posicoes_corte)} padrões visuais para corte")
    
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Corta as seções da imagem
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta a seção anterior até a posição de corte atual
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # A próxima seção começa exatamente onde esta foi cortada
        posicao_anterior = posicao_corte
    
    # Corta a seção final (após o último padrão)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Substitua pelo caminho da sua imagem
    pasta_saida = "colunas" # Substitua pelo nome da pasta de saída desejada
    
    # Executa a divisão baseada no padrão de pixels
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    
    print("Divisão concluída!")