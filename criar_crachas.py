# criar_crachas.py

import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import shutil


def gerar_crachas(dados_crachas, cracha_modelo_servos):

    # Leitura do CSV
    df = pd.read_csv(dados_crachas)

    # Verifique os nomes das colunas (ajuste se necessário)
    print(df.columns)

    # Diretório de saída
    output_dir = 'Cracha_gerados'
    os.makedirs(output_dir, exist_ok=True)

    # Cria o diretório, se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Apaga todos os arquivos e subpastas dentro de output_dir
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove arquivo ou link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove subpasta
        except Exception as e:
            print(f'Erro ao apagar {file_path}. Detalhes: {e}')

    """
        Loclaização relativa da pasta em que está o arquivo de fonte - Almendra
    """
    # Diretório atual do script
    base_dir = os.path.dirname(__file__)

    # Caminho completo da fonte
    fonte_path = os.path.join(base_dir, "Fontes", "Almendra", "Almendra-Regular.ttf")

    # Carregar a fonte
    fonte_nome = ImageFont.truetype(fonte_path, 70)
    fonte_completo = ImageFont.truetype(fonte_path, 35)


    for index, row in df.iterrows():
        apelido = row['APELIDO'] 
        nome_completo = row['NOME COMPLETO']
        equipe = row['EQUIPE']

        # Criar subpasta para a equipe
        equipe_dir = os.path.join(output_dir, equipe.replace(' ', '_'))
        os.makedirs(equipe_dir, exist_ok=True)

        # Abrir a imagem base - que muda conforme o nome da equipe
        # Garantir que exista uma imagem base conforme o nome da equipe, caso contrário
        # vou inserir uma menssagem de erro.
        cracha_equipe_modelo = equipe + ".png"
        base_image_path = os.path.join(base_dir, "Inputs", cracha_equipe_modelo)

        # o texto a ser escrito depende se o modelo do crachá é para servos
        # ou se o modelo é para os encontristas
        sub_texto = nome_completo

        try:
            img = Image.open(base_image_path).convert("RGBA")           
        except FileNotFoundError:
            # print(f"Imagem da equipe '{cracha_equipe_modelo}' não encontrada. Usando imagem padrão/servos.")
            img = Image.open(cracha_modelo_servos).convert("RGBA")
            sub_texto = equipe

        draw = ImageDraw.Draw(img)
        
        # Tamanho da imagem
        largura, altura = img.size


        # Centralizar textos
        largura_nome = draw.textlength(apelido, font=fonte_nome)
        largura_completo = draw.textlength(sub_texto, font=fonte_completo)

        # Posição aproximada — ajuste conforme seu template
        pos_nome = ((largura - largura_nome) / 2, altura * 0.65 /2)
        pos_completo = ((largura - largura_completo) / 2, altura * 0.80/(1.7))

        # Escrevendo os textos
        draw.text(pos_nome, apelido, font=fonte_nome, fill="black")
        draw.text(pos_completo, sub_texto, font=fonte_completo, fill="black")

        # Nome do arquivo e salvar
        nome_arquivo = f"{apelido.replace(' ', '_')}.png"
        caminho_arquivo = os.path.join(equipe_dir, nome_arquivo)
        img.save(caminho_arquivo)

    print("Crachás gerados com sucesso.")