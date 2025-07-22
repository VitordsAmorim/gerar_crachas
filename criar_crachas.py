# criar_crachas.py

import os
import shutil
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


def gerar_crachas(dados_csv_path: str, modelo_padrao_path: str) -> None:
    """
    Gera crachás personalizados a partir de um arquivo CSV com os dados dos participantes.
    
    Parâmetros:
    - dados_csv_path: Caminho para o arquivo CSV com os dados (colunas: APELIDO, NOME COMPLETO, EQUIPE)
    - modelo_padrao_path: Caminho da imagem base a ser usada como fallback (ex: crachá padrão dos servos)
    """
    
    # Lê os dados do CSV
    df = pd.read_csv(dados_csv_path)

    # print("Colunas encontradas no CSV:", df.columns.tolist())  # Debug

    # Diretório de saída dos crachás
    output_dir = "outputs/crachas_gerados"

    # Caminho da fonte
    base_dir = os.path.dirname(__file__)
    fonte_path = os.path.join(base_dir, "fonts", "Almendra", "Almendra-Regular.ttf")

    # Carregamento das fontes
    fonte_nome = ImageFont.truetype(fonte_path, size=70)
    fonte_completo = ImageFont.truetype(fonte_path, size=35)

    for _, row in df.iterrows():
        apelido = row['APELIDO']
        nome_completo = row['NOME COMPLETO']
        equipe = row['EQUIPE']

        # Diretório da equipe
        equipe_dir = os.path.join(output_dir, equipe.replace(" ", "_"))
        os.makedirs(equipe_dir, exist_ok=True)

        # Caminho da imagem base da equipe
        imagem_equipe_nome = equipe + ".png"
        imagem_equipe_path = os.path.join(base_dir, "inputs", imagem_equipe_nome)

        # Por padrão, escreve o nome completo; muda se cair no fallback
        sub_texto = nome_completo

        try:
            img = Image.open(imagem_equipe_path).convert("RGBA")
        except FileNotFoundError:
            # print(f"[AVISO] Imagem '{imagem_equipe_nome}' não encontrada. Usando modelo padrão.")
            img = Image.open(modelo_padrao_path).convert("RGBA")
            sub_texto = equipe

        draw = ImageDraw.Draw(img)

        # Dimensões
        largura, altura = img.size

        # Medidas dos textos
        largura_nome = draw.textlength(apelido, font=fonte_nome)
        largura_completo = draw.textlength(sub_texto, font=fonte_completo)

        # Posições calculadas para centralizar
        pos_nome = ((largura - largura_nome) / 2, altura * 0.65 / 2)
        pos_completo = ((largura - largura_completo) / 2, altura * 0.80 / 1.7)

        # Escreve na imagem
        draw.text(pos_nome, apelido, font=fonte_nome, fill="black")
        draw.text(pos_completo, sub_texto, font=fonte_completo, fill="black")

        # Salva imagem
        nome_arquivo = f"{apelido.replace(' ', '_')}.png"
        caminho_arquivo = os.path.join(equipe_dir, nome_arquivo)
        img.save(caminho_arquivo)

    print("✅ Crachás gerados com sucesso.")