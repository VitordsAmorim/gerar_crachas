# preparar_impressao.py

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
# import logging

# # Configuração do sistema de logs
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

def preparar_impressao(output_dir, pdf_output_dir):
    """
    Gera arquivos PDF com crachás organizados para impressão, a partir de imagens PNG
    organizadas em subpastas (cada subpasta representa uma equipe).

    O layout considera páginas A4, com margens e redimensionamento proporcional das imagens.

    Parâmetros:
    - output_dir: diretório contendo subpastas, onde cada subpasta tem os crachás (PNG) de uma equipe.
    - pdf_output_dir: diretório de saída para os PDFs gerados (um por equipe).

    Requisitos:
    - As imagens devem ter 300 DPI (para correspondência correta do tamanho).
    - As bibliotecas Pillow e ReportLab devem estar instaladas.

    Etapas:
    1. Define tamanhos e margens.
    2. Cria o diretório de saída, se necessário.
    3. Para cada subpasta:
        a. Gera um PDF com os crachás da equipe.
        b. Posiciona os crachás na página com layout responsivo.
        c. Quebra página automaticamente conforme o espaço.
    """

    # Dimensões do crachá em pixels (considerando 300 DPI)
    cracha_largura_px = 1181
    cracha_altura_px = 827

    # Converte de pixels para pontos (ReportLab usa pontos: 1 inch = 72 pt)
    fator = 72 / 300  # 300 DPI
    cracha_largura_pt = cracha_largura_px * fator
    cracha_altura_pt = cracha_altura_px * fator

    # Tamanho da página A4
    pagina_largura, pagina_altura = A4

    # Margem externa e entre crachás (em pontos)
    margem = 10

    # Cria a pasta de saída dos PDFs
    os.makedirs(pdf_output_dir, exist_ok=True)

    # Lista de subpastas (cada uma representa uma equipe)
    subpastas = [e for e in sorted(os.listdir(output_dir)) if os.path.isdir(os.path.join(output_dir, e))]
    total_equipes = len(subpastas)

    for idx, equipe in enumerate(subpastas, 1):
        # Mostra progresso de forma dinâmica na mesma linha
        print(f"⏳ [{idx}/{total_equipes}] Gerando PDF para: {equipe:<30}", end='\r', flush=True)

        equipe_path = os.path.join(output_dir, equipe)
        pdf_output_path = os.path.join(pdf_output_dir, f"{equipe}.pdf")
        c = canvas.Canvas(pdf_output_path, pagesize=A4)

        # Coordenadas iniciais para posicionar os crachás na página
        x = margem
        y = pagina_altura - cracha_altura_pt - margem

        for file in sorted(os.listdir(equipe_path)):
            if file.lower().endswith('.png'):
                img_path = os.path.join(equipe_path, file)

                # Abre e redimensiona a imagem mantendo a qualidade
                img = Image.open(img_path).resize(
                    (cracha_largura_px, cracha_altura_px),
                    Image.Resampling.LANCZOS
                )

                # Converte para modo RGB e usa ImageReader para o ReportLab
                img_reader = ImageReader(img.convert("RGB"))

                # Desenha a imagem na posição atual
                c.drawImage(
                    img_reader, x, y,
                    width=cracha_largura_pt,
                    height=cracha_altura_pt
                )

                # Atualiza posição para o próximo crachá na linha
                x += cracha_largura_pt + margem

                # Se ultrapassou a largura da página, vai para próxima linha
                if x + cracha_largura_pt > pagina_largura:
                    x = margem
                    y -= cracha_altura_pt + margem

                    # Se ultrapassou o final da página, cria nova página
                    if y < margem:
                        c.showPage()
                        x = margem
                        y = pagina_altura - cracha_altura_pt - margem

        # Finaliza o PDF da equipe
        c.save()
    print("✅ Todos os PDFs foram gerados com sucesso") 