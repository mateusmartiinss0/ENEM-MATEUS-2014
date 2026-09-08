from PIL import Image  
import os

def encontrar_padrao_vertical(imagem, tolerancia=15):
    """
    Encontra posições onde há o padrão vertical de 5 faixas especificadas na coluna central:
    1. Faixa 1: ~2px da cor (35, 31, 32) [margem 1-3px]
    2. Faixa 2: ~2px da cor (255, 255, 255) [margem 1-3px]
    3. Faixa 3: ~4px da cor (35, 31, 32) [margem 3-5px]
    4. Faixa 4: ~2px da cor (255, 255, 255) [margem 1-3px]
    5. Faixa 5: ~2px da cor (35, 31, 32) [margem 1-3px]
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    x_meio = largura // 2  # Pixel do meio
    
    posicoes_corte = []
    
    def cor_bate(pixel, cor_alvo):
        r, g, b = pixel[:3]
        return (abs(r - cor_alvo[0]) <= tolerancia and 
                abs(g - cor_alvo[1]) <= tolerancia and 
                abs(b - cor_alvo[2]) <= tolerancia)

    cor_escura = (35, 31, 32)
    cor_branca = (255, 255, 255)
    
    # Define a sequência de cores e o intervalo de altura para cada bloco (com margem de +-1px)
    # Estrutura: (cor, altura_minima, altura_maxima)
    padrao = [
        (cor_escura, 1, 3),  # Esperado: 2px (1 a 3)
        (cor_branca, 1, 3),  # Esperado: 2px (1 a 3)
        (cor_escura, 3, 5),  # Esperado: 4px (3 a 5)
        (cor_branca, 1, 3),  # Esperado: 2px (1 a 3)
        (cor_escura, 1, 3)   # Esperado: 2px (1 a 3)
    ]

    y = 0
    while y < altura - 20:
        y_atual = y
        padrao_valido = True
        
        for cor_alvo, alt_min, alt_max in padrao:
            contagem_px = 0
            while y_atual < altura and cor_bate(pixels[x_meio, y_atual], cor_alvo):
                contagem_px += 1
                y_atual += 1
                
            if not (alt_min <= contagem_px <= alt_max):
                padrao_valido = False
                break
        
        if padrao_valido:
            # Corta 21 pixels antes do padrão começar
            posicao_corte = y - 21
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Padrão encontrado iniciando em y={y}, cortando em y={posicao_corte}")
            # Avança o ponteiro 'y' para além do padrão detectado
            y = y_atual
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente cortando nas posições identificadas
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_padrao_vertical(imagem)
    
    if not posicoes_corte:
        print("Nenhum padrão encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} ocorrências do padrão para corte")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    # Seção final após o último corte
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "./inteiras/pagina_enem_29.png"  # Atualize para o nome da sua imagem
    pasta_saida = "pg29"  # Atualize para o nome da pasta desejada
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    
    print("Divisão concluída!")