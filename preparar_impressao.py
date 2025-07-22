import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

def preparar_impressao_em_memoria(crachas_por_equipe, pdf_output_dir):
    os.makedirs(pdf_output_dir, exist_ok=True)

    cracha_largura_px = 1181
    cracha_altura_px = 827
    fator = 72 / 300
    cracha_largura_pt = cracha_largura_px * fator
    cracha_altura_pt = cracha_altura_px * fator
    pagina_largura, pagina_altura = A4
    margem = 10

    total_equipes = len(crachas_por_equipe)

    for idx, (equipe, crachas) in enumerate(sorted(crachas_por_equipe.items()), 1):
        print(f"📄 [{idx}/{total_equipes}] Gerando PDF: {equipe:<30}", end='\r', flush=True)

        pdf_path = os.path.join(pdf_output_dir, f"{equipe}.pdf")
        c = canvas.Canvas(pdf_path, pagesize=A4)

        x = margem
        y = pagina_altura - cracha_altura_pt - margem

        for apelido, buffer in crachas:
            img_reader = ImageReader(buffer)

            c.drawImage(
                img_reader, x, y,
                width=cracha_largura_pt,
                height=cracha_altura_pt
            )

            x += cracha_largura_pt + margem

            if x + cracha_largura_pt > pagina_largura:
                x = margem
                y -= cracha_altura_pt + margem

                if y < margem:
                    c.showPage()
                    x = margem
                    y = pagina_altura - cracha_altura_pt - margem

        c.save()

    print("\n✅ Todos os PDFs foram gerados com sucesso.")
