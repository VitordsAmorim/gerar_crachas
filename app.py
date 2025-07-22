import streamlit as st
import tempfile
import os
from criar_crachas import gerar_crachas_em_memoria
from preparar_impressao import preparar_impressao_em_memoria

st.set_page_config(page_title="Gerador de Crachás", layout="centered")

st.title("🎫 Gerador de Crachás para Impressão")

# Upload do CSV
csv_file = st.file_uploader("📄 Envie o arquivo CSV com os dados dos participantes", type=["csv"])

# Upload da imagem padrão de crachá
modelo_padrao = st.file_uploader("🖼️ Imagem padrão de crachá (usada quando não houver imagem por equipe)", type=["png", "jpg"])

# Upload da pasta de fontes (opcional: só o .ttf)
fonte_ttf = st.file_uploader("🔤 Fonte personalizada (.ttf)", type=["ttf"])

# Upload de imagens por equipe
st.markdown("📁 **Imagens por equipe (opcional)**")
equipes_imgs = st.file_uploader("Envie as imagens das equipes (nome da imagem deve bater com o nome da equipe)", type=["png", "jpg"], accept_multiple_files=True)

if st.button("🚀 Gerar PDFs"):
    if not csv_file or not modelo_padrao or not fonte_ttf:
        st.error("Por favor, envie o CSV, a imagem padrão e a fonte.")
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "dados.csv")
            modelo_path = os.path.join(tmpdir, "modelo.png")
            fonte_path = os.path.join(tmpdir, "fonte.ttf")
            input_dir = os.path.join(tmpdir, "inputs")
            pdf_output_dir = os.path.join(tmpdir, "pdfs")
            os.makedirs(input_dir, exist_ok=True)

            # Salvar arquivos temporários
            with open(csv_path, "wb") as f: f.write(csv_file.getbuffer())
            with open(modelo_path, "wb") as f: f.write(modelo_padrao.getbuffer())
            with open(fonte_path, "wb") as f: f.write(fonte_ttf.getbuffer())

            for img_file in equipes_imgs or []:
                equipe_path = os.path.join(input_dir, img_file.name)
                with open(equipe_path, "wb") as f:
                    f.write(img_file.getbuffer())

            # Geração
            crachas_memoria = gerar_crachas_em_memoria(csv_path, modelo_path, input_dir, fonte_path)
            preparar_impressao_em_memoria(crachas_memoria, pdf_output_dir)

            # Exibir PDFs para download
            for filename in sorted(os.listdir(pdf_output_dir)):
                file_path = os.path.join(pdf_output_dir, filename)
                with open(file_path, "rb") as f:
                    st.download_button(f"⬇️ Baixar {filename}", data=f, file_name=filename)

        st.success("✅ PDFs gerados com sucesso!")
