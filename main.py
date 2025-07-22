# main.py

import os
from criar_crachas import gerar_crachas

def main():
    """
    Função principal que define os caminhos dos arquivos de entrada
    e chama a função responsável por gerar os crachás.
    """

    # Diretório base do script atual
    base_dir = os.path.dirname(__file__)

    # Caminho do modelo de crachá (imagem base)
    modelo_cracha_path = os.path.join(base_dir, "inputs", "cracha_servos.png")

    # Caminho dos dados dos crachás (CSV)
    dados_crachas_path = os.path.join(base_dir, "data", "Dados_cracha.csv")

    # Geração dos crachás
    gerar_crachas(dados_crachas_path, modelo_cracha_path)

if __name__ == "__main__":
    main()
