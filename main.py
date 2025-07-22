# main.py

import os
from criar_crachas import gerar_crachas
from preparar_impressao import preparar_impressao

def main():
    """
    Função principal que define os caminhos dos arquivos de entrada
    e chama a função responsável por gerar os crachás e a outra função para gerar os pdf.
    """

    # Diretório base do script atual
    base_dir = os.path.dirname(__file__)

    # Caminho do modelo de crachá (imagem base)
    modelo_cracha_path = os.path.join(base_dir, "inputs", "cracha_servos.png")

    # Caminho dos dados dos crachás (CSV)
    dados_crachas_path = os.path.join(base_dir, "data", "Dados_cracha.csv")

    # Geração dos crachás
    gerar_crachas(dados_crachas_path, modelo_cracha_path)

    # Define o diretório onde os crachás PNG foram gerados (entrada).
    output_dir = "outputs/crachas_gerados"
    # Define o diretório onde os PDFs de saída serão salvos.
    pdf_output_dir = "outputs/pdfs"
    preparar_impressao(output_dir, pdf_output_dir)

if __name__ == "__main__":
    main()