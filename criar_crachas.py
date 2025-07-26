import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def gerar_crachas_em_memoria(csv_path, modelo_padrao_path, inputs_dir, fonte_path):
    df = pd.read_csv(csv_path)

    fonte_nome = ImageFont.truetype(fonte_path, size=70)
    fonte_completo = ImageFont.truetype(fonte_path, size=35)

    crachas_por_equipe = {}

    # for _, row in df.iterrows():
    for row in df.itertuples(index=False):
        apelido = row.APELIDO
        nome_completo = row.NOME_COMPLETO
        equipe = row.EQUIPE   

        # apelido = row["APELIDO"]
        # nome_completo = row["NOME COMPLETO"]
        # equipe = row["EQUIPE"] 

        imagem_equipe_path = os.path.join(inputs_dir, f"{equipe}.png")
        sub_texto = nome_completo

        try:
            img = Image.open(imagem_equipe_path).convert("RGBA")
        except FileNotFoundError:
            img = Image.open(modelo_padrao_path).convert("RGBA")
            sub_texto = equipe

        draw = ImageDraw.Draw(img)
        largura, altura = img.size
        largura_nome = draw.textlength(apelido, font=fonte_nome)
        largura_completo = draw.textlength(sub_texto, font=fonte_completo)

        pos_nome = ((largura - largura_nome) / 2, altura * 0.65 / 2)
        pos_completo = ((largura - largura_completo) / 2, altura * 0.80 / 1.7)

        draw.text(pos_nome, apelido, font=fonte_nome, fill="black")
        draw.text(pos_completo, sub_texto, font=fonte_completo, fill="black")

        buffer = BytesIO()
        img.convert("RGB").save(buffer, format="PNG")
        buffer.seek(0)

        if equipe not in crachas_por_equipe:
            crachas_por_equipe[equipe] = []
        crachas_por_equipe[equipe].append((apelido, buffer))

    print("✅ Crachás gerados em memória.")
    return crachas_por_equipe