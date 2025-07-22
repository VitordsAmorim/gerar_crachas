from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

# Parâmetros
output_dir = "cracha_gerados"
pdf_output_dir = "pdfs_gerados"  # Pasta para salvar os PDFs
cracha_largura_px = 1181
cracha_altura_px = 827
fator = 72 / 300
cracha_largura_pt = cracha_largura_px * fator
cracha_altura_pt = cracha_altura_px * fator
pagina_largura, pagina_altura = A4
margem = 10

# Criar pasta de saída, se não existir
os.makedirs(pdf_output_dir, exist_ok=True)

# Processar cada subpasta (equipe)
for equipe in sorted(os.listdir(output_dir)):
    equipe_path = os.path.join(output_dir, equipe)
    if os.path.isdir(equipe_path):
        # Caminho completo para o PDF de saída
        pdf_output_path = os.path.join(pdf_output_dir, f"{equipe}.pdf")
        c = canvas.Canvas(pdf_output_path, pagesize=A4)

        x = margem
        y = pagina_altura - cracha_altura_pt - margem

        for file in sorted(os.listdir(equipe_path)):
            if file.lower().endswith('.png'):
                img_path = os.path.join(equipe_path, file)
                img = Image.open(img_path).resize((cracha_largura_px, cracha_altura_px), Image.Resampling.LANCZOS)
                img_reader = ImageReader(img.convert("RGB"))

                c.drawImage(img_reader, x, y, width=cracha_largura_pt, height=cracha_altura_pt)

                x += cracha_largura_pt + margem
                if x + cracha_largura_pt > pagina_largura:
                    x = margem
                    y -= cracha_altura_pt + margem
                    if y < margem:
                        c.showPage()
                        x = margem
                        y = pagina_altura - cracha_altura_pt - margem

        c.save()
        print(f"PDF gerado para {equipe}: {pdf_output_path}")