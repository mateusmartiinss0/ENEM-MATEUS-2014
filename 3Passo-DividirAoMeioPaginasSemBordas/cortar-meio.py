"""
Propósito: Cortar as imagens de colunas ao meio. As imagens já estão sem as bordas externas, agora só cortar ao meio
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "sem-bordas-externas" do passo 2 para essa pasta do passo 3

OBS2: observe que existe páginas inteiras, que não faz sentido ser cortadas ao meio, e páginas que são colunas, que faz sentido ser cortadas ao meio. 

OBS3: nesse caderno de 2024, as páginas 15 e 28 são páginas inteiras. Crie uma pasta chamada "inteiras" e mova só essas duas páginas para lá.

OBS4: este código vai criar uma pasta de saída chamada "divididas-com-bordas-do-meio", vai cortar ao meio as páginas que são colunas e salvar as imagens cortadas nessa pasta criada

OBS5: execute o código

OBS6: ao cortar ao meio, vai gerar uma bordinha interna. As colunas do lado esquedo vai ter uma bordinha do lado direito e as colunas do lado direito vai ter uma bordinha do lado esquerdo. Essas bordinhas serão removidas no próximo passo.
"""

from PIL import Image
import os

pasta_imagens = "sem-bordas-externas"
pasta_saida = "divididas-com-bordas-do-meio"

os.makedirs(pasta_saida, exist_ok=True)

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith('.png'):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        imagem = Image.open(caminho_entrada)

        largura, altura = imagem.size
        
        metade_largura = largura // 2
        
        caixa_esquerda = (0, 0, metade_largura, altura)
        imagem_esquerda = imagem.crop(caixa_esquerda)
        
        caixa_direita = (metade_largura, 0, largura, altura)
        imagem_direita = imagem.crop(caixa_direita)
        
        nome_base, extensao = os.path.splitext(nome_arquivo)
        
        caminho_esquerda = os.path.join(pasta_saida, f"{nome_base}_esquerda{extensao}")
        caminho_direita = os.path.join(pasta_saida, f"{nome_base}_direita{extensao}")
        
        imagem_esquerda.save(caminho_esquerda)
        imagem_direita.save(caminho_direita)

print("Divisão das imagens ao meio concluída.")