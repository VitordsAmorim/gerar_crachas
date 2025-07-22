from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def preparar_impressao():
    """
    Este script automatiza a preparação de crachás gerados em formato PNG
    para impressão em páginas PDF. Ele organiza os crachás por equipe (subpasta)
    e os diagramas em páginas A4, garantindo que o layout e as margens sejam respeitados.

    O processo envolve:
    1. Leitura de parâmetros de dimensão e margem.
    2. Criação de um diretório de saída para os PDFs, se necessário.
    3. Iteração sobre subpastas (equipes) no diretório de entrada.
    4. Para cada equipe, cria um arquivo PDF.
    5. Itera sobre os arquivos PNG (crachás) dentro de cada pasta de equipe.
    6. Redimensiona cada imagem do crachá e a posiciona na página PDF.
    7. Gerencia o layout dos crachás na página, criando novas páginas A4
       conforme necessário para acomodar todos os crachás de uma equipe.
    8. Salva o PDF final para cada equipe.

    Pré-requisitos:
    - O diretório 'cracha_gerados' (definido em `output_dir`) deve existir
      e conter subpastas, onde cada subpasta representa uma equipe
      e contém os arquivos PNG dos crachás dessa equipe.
    - As bibliotecas 'Pillow' (PIL) e 'ReportLab' devem estar instaladas.
    """

    # --- Parâmetros e Constantes ---
    # Define o diretório onde os crachás PNG foram gerados (entrada).
    output_dir = "outputs/crachas_gerados"
    # Define o diretório onde os PDFs de saída serão salvos.
    pdf_output_dir = "outputs/pdfs"

    # Dimensões dos crachás em pixels (assumindo uma resolução de 300 DPI)
    cracha_largura_px = 1181
    cracha_altura_px = 827

    # Fator de conversão: ReportLab usa pontos (pt) onde 1 polegada = 72 pontos.
    # Se os PNGs foram gerados a 300 DPI (dots per inch / pontos por polegada),
    # então para converter pixels para pontos: (pixels / DPI) * 72 pt/inch
    fator = 72 / 300

    # Dimensões dos crachás em pontos (unidade de medida do ReportLab)
    cracha_largura_pt = cracha_largura_px * fator
    cracha_altura_pt = cracha_altura_px * fator

    # Dimensões da página A4 em pontos (importadas de reportlab.lib.pagesizes)
    pagina_largura, pagina_altura = A4

    # Margem a ser usada nas bordas da página e entre os crachás.
    margem = 10 # pontos

    # --- Lógica Principal ---

    # Cria a pasta de saída para os PDFs, se ela ainda não existir.
    # exist_ok=True evita erro caso a pasta já exista.
    os.makedirs(pdf_output_dir, exist_ok=True)

    # Itera sobre cada subpasta dentro do diretório de crachás gerados.
    # Cada subpasta é tratada como uma "equipe". As pastas são ordenadas alfabeticamente.
    for equipe in sorted(os.listdir(output_dir)):
        equipe_path = os.path.join(output_dir, equipe)

        # Verifica se o item é realmente um diretório (uma pasta de equipe).
        if os.path.isdir(equipe_path):
            # Define o caminho completo para o arquivo PDF de saída desta equipe.
            # O nome do PDF será o nome da pasta da equipe.
            pdf_output_path = os.path.join(pdf_output_dir, f"{equipe}.pdf")

            # Cria um novo objeto Canvas (documento PDF) para a equipe,
            # definindo o nome do arquivo de saída e o tamanho da página como A4.
            c = canvas.Canvas(pdf_output_path, pagesize=A4)

            # Inicializa as coordenadas X e Y para posicionar o primeiro crachá na página.
            # O ReportLab usa coordenadas cartesianas, onde (0,0) é o canto inferior esquerdo.
            x = margem # Posição X inicial (da esquerda, com margem)
            y = pagina_altura - cracha_altura_pt - margem # Posição Y inicial (do topo, com margem)

            # Itera sobre cada arquivo dentro da pasta da equipe, ordenando-os.
            for file in sorted(os.listdir(equipe_path)):
                # Verifica se o arquivo é uma imagem PNG (case-insensitive).
                if file.lower().endswith('.png'):
                    img_path = os.path.join(equipe_path, file)

                    # Abre a imagem PNG usando Pillow e a redimensiona para as dimensões em pixels desejadas.
                    # Image.Resampling.LANCZOS é um filtro de alta qualidade para redimensionamento.
                    img = Image.open(img_path).resize((cracha_largura_px, cracha_altura_px), Image.Resampling.LANCZOS)
                    # Converte a imagem para o modo "RGB" (se ainda não estiver) e a prepara para o ReportLab.
                    img_reader = ImageReader(img.convert("RGB"))

                    # Desenha a imagem do crachá no Canvas PDF, nas coordenadas (x, y)
                    # e com as dimensões já convertidas para pontos.
                    c.drawImage(img_reader, x, y, width=cracha_largura_pt, height=cracha_altura_pt)

                    # --- Lógica de Posicionamento e Paginação ---
                    # Move a posição X para o próximo crachá na mesma linha.
                    x += cracha_largura_pt + margem
                    
                    # Verifica se o próximo crachá ultrapassaria a largura da página.
                    if x + cracha_largura_pt > pagina_largura:
                        # Se sim, reinicia X para a margem esquerda (próxima linha).
                        x = margem
                        # Move a posição Y para a linha abaixo (próximo crachá na vertical).
                        y -= cracha_altura_pt + margem
                        
                        # Verifica se ainda há espaço vertical suficiente na página para o próximo crachá.
                        if y < margem:
                            # Se não houver, salva a página atual e inicia uma nova página no PDF.
                            c.showPage()
                            # Reinicia X e Y para o topo esquerdo da nova página.
                            x = margem
                            y = pagina_altura - cracha_altura_pt - margem

            # Após processar todos os crachás de uma equipe, salva o arquivo PDF.
            c.save()
        # Imprime uma mensagem de confirmação no console.
    print(f" ✅ PDF gerados com sucesso.")