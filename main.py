import google.generativeai as genai
from dotenv import load_dotenv
from CriadorDePdf import CriadorDePdf
import os
import sys
import PIL.Image

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Inicializando a API
genai.configure(api_key=GOOGLE_API_KEY)

# Configurando o Modelo
"""
Note que configuramos o modelo de modo que ele tenha o
mínimo de liberdade possível para alterar o conteúdo
original das nossas anotações, para isso, diminuímos
a tempurature do modelo e liberamos quaisquer gatilhos
para que ele não modifique o material de forma alguma.
"""
generation_config = {
    "candidate_count": 1,
    "temperature": 0
}
safety_settings = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE"
}

# Inicializando o Modelo
"""
Escolhemos o Modelo Vision pois nossa aplicação exige
a multimodalidade dessa versão. Caso estivéssemos
trabalhando apenas com texto, provavelmente essa
escolha mudaria.
"""
model = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=generation_config,
    safety_settings=safety_settings
)


# Fazendo a requisição de uma página:
CAMINHO_PAGINAS = []
PAGINAS = []


def extrair_paginas():
    global CAMINHO_PAGINAS
    for filename in os.listdir("imagens"):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            CAMINHO_PAGINAS.append(os.path.join("imagens", filename))

    if len(CAMINHO_PAGINAS) == 0:
        sys.exit("Nenhuma imagem válida foi encontrada. Certifique-se de que as imagens estão no diretório 'imagens' e que são dos tipos: '.png', '.jpg', '.jpeg'.")

    CAMINHO_PAGINAS = sorted(CAMINHO_PAGINAS)

    print("Caminhos Extraídos Ordenados: ", CAMINHO_PAGINAS)


def traduzir_imagens(CAMINHO_PAGINAS):
    global PAGINAS
    for caminho in CAMINHO_PAGINAS:
        PAGINAS.append(PIL.Image.open(caminho))


extrair_paginas()
traduzir_imagens(CAMINHO_PAGINAS)

print("Páginas Extraídas: ", PAGINAS)

# Criação das Transcrições:
PAGINAS_TRANSCRITAS = []

# Criando o Prompt:
PROMPT_COM_EQUACOES = """Transcreva o conteúdo desta imagem de um caderno.
Tente sempre seguir uma mesma formatação, padronização e evitar ao máximo adaptações, sendo o mais fidedígno ao texto original. Mantenha sempre o idioma original do texto.
Caso haja equações, siga as seguintes regras:
    Todas equações devem ser expressas em LaTeX, não há necessidade de configurar o arquivo LaTeX.
    Note que essa transcrição será utilizada para gerar pdf usando python, então cada linha deverá ser separada por um caractere de nova linha '\\n'"""


def transcrever_paginas():
    global PAGINAS_TRANSCRITAS
    for pagina in PAGINAS:
        response = model.generate_content(
            [PROMPT_COM_EQUACOES, pagina], stream=True)
        response.resolve()
        PAGINAS_TRANSCRITAS.append(response.text.split("\n"))


transcrever_paginas()

print("Transcrição das Páginas: ", PAGINAS_TRANSCRITAS)


CriadorDePdf = CriadorDePdf(PAGINAS_TRANSCRITAS)
CriadorDePdf.criar_pdf()
