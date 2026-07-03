"""
Propósito: converter o arquivo PDF em imagens PNG
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025.
Atualização: 03/06/2026

OBS1: nesta pasta do Passo 1, precisa ter o código e o PDF que deseja converter.

OBS2: este código vai criar uma pasta de saída chamada "imagens-convertidas" e vai pegar página por página do PDF e salvar como imagens PNG nessa pasta.

OBS3: execute o código.

OBS4: depois de executar, exclua as imagens com nome de código estranho da pasta de saída, deixando só os nomes que fazem sentido

OBS5: tem que ficar apenas as páginas das questões. Neste caderno, exclua as páginas 1 (capa), 19 (proposta de redação) e 32 (rascunho da redação)
"""

from pdf2image import convert_from_path
import os

arquivo = "2014_PV_impresso_D1_ENEM.pdf"
pasta_saida = "imagens-convertidas"

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

resolucao_dpi = 300

print (f"Convertendo '{arquivo}' para imagens com {resolucao_dpi} DPI...")

try:
    images = convert_from_path(
        arquivo,
        dpi = resolucao_dpi,
        output_folder = pasta_saida,
        fmt = "png",
        paths_only = False,
    )

    for i, image in enumerate(images):
        image_filename = os.path.join(pasta_saida, f"pagina_enem_{i+1}.png")
        image.save(image_filename)
        print(f"Página {i+1} salva como '{image_filename}'")

    print(f"\nConversão concluída! As imagens foram salvas na pasta '{pasta_saida}'.")

except Exception as e:
    print (f"Ocorreu um erro durante a conversão: {e}")
    print("Verifique se o Poppler está instalado corretamente, se o caminho do PDF está correto ou se o PDF não está corrompido.")