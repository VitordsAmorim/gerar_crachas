import os
import time
from criar_crachas import gerar_crachas_em_memoria
from preparar_impressao import preparar_impressao_em_memoria

def main():
    start_time = time.time()  # Início da contagem

    base_dir = os.path.dirname(__file__)
    inputs_dir = os.path.join(base_dir, "inputs")
    modelo_padrao_path = os.path.join(inputs_dir, "padrao.png")
    csv_path = os.path.join(base_dir, "data", "dados.csv")
    fonte_path = os.path.join(base_dir, "fonts", "Almendra", "Almendra-Regular.ttf")
    pdf_output_dir = os.path.join(base_dir, "outputs", "pdfs")

    crachas_memoria = gerar_crachas_em_memoria(csv_path, modelo_padrao_path, inputs_dir, fonte_path)
    preparar_impressao_em_memoria(crachas_memoria, pdf_output_dir)

    end_time = time.time()  # Fim da contagem
    elapsed_time = end_time - start_time
    print(f"Tempo de execução: {elapsed_time:.2f} segundos")

if __name__ == "__main__":
    main()