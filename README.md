# ProjetoNotas / NotesProject

[Português](#português) | [English](#english)

---

<a name="português"></a>
# Português

## Sobre o Projeto
Este projeto tem como objetivo resolver um grande problema que tenho há muito tempo - digitalizar meus materiais e notas de forma simples e rápida. 
Com o auxílio da API do Google Gemini, eu consegui criar um sistema que ataca exatamente este problema.
Eu, minha mãe, minha avó, todos já nos encontramos na situação de querer salvar algum material escrito à mão de forma digital, seja para ter mais formalidade ou até mesmo para ter como alterá-lo de forma mais simples posteriormente, mas nunca tivemos acesso à ferramenta correta. 
Para isso, criei o `ProjetoNotas`. O projeto em que utilizamos o potente modelo Gemini da Google para criar de forma automática e dinâmica materiais digitalizados de nossas mídias físicas!


## Funcionalidades:
- Extrai texto de imagens de cadernos
- Converte equações LaTeX em imagens de alta qualidade (em desenvolvimento)
- Gera PDFs formatados

## Pré-Requisitos:
- Python 3.6 ou superior
- Bibliotecas Python:
    - google.generativeai
    - sys
    - os
    - FPDF
    - Pillow (PIL)
    - matplotlib
    - python-dotenv


## Instalação:
1. Clone o Repositório: `git clone https://github.com/Cerne17/ProjetoNotas.git`
2. Instale as dependências: `pip install -r requirements.txt`

## Uso:
1. Tire fotos das notas a serem digitalizadas.
2. Coloque todas as fotos, organizando-as por ordem numérica, dentro da pasta `imagens` do projeto
3. Inclua sua chave da Google API
    1. Note que disponibilizamos um exemplo de como seu arquivo `.env` deve ser para que o código funcione
    2. Mas outra forma de se fazer seria substituir o valor da variável `GOOGLE_API_KEY` diretamente no arquivo `main.py` 
3. Execute o script principal: `python main.py` ou `python3 main.py`
4. Note que todos arquivos devem ter mesmo tamanho de nome para a ordenação funcionar como esperado. Ou seja:
    1. Se precisar do pdf de `1432` páginas, todos arquivos devem ter nome com `4` dígitos: `0001.png`, `0012.png`, `0123.jpg`, ...
    2. Se precisar do pdf de `14` páginas, todos arquivos devem ter nome com `2` dígitos: `01.png`, `09.png`, `12.jpg`, ...
    3. E assim por diante.

## Customização: 
Sinta-se livre para mudar as configurações de fonte, tamanho da escrita, linhas por página.
Essas configurações encontram-se no método `__init__` da classe `CriadorDePdf`, no arquivo `CriadorDePdf.py`.

---

<a name="english"></a>
# English

## About the Project
This project aims to solve a major problem I've had for a long time - digitizing my materials and notes simply and quickly.
With the help of the Google Gemini API, I managed to create a system that addresses exactly this problem.
Me, my mother, my grandmother, we have all found ourselves in the situation of wanting to save some handwritten material digitally, whether to have more formality or even to be able to change it more simply later, but we never had access to the correct tool.
For this, I created `ProjetoNotas` (NotesProject). A project where we use Google's powerful Gemini model to automatically and dynamically create digitized materials from our physical media!

## Features:
- Extracts text from notebook images
- Converts LaTeX equations into high-quality images (in development)
- Generates formatted PDFs

## Prerequisites:
- Python 3.6 or higher
- Python Libraries:
    - google.generativeai
    - sys
    - os
    - FPDF
    - Pillow (PIL)
    - matplotlib
    - python-dotenv

## Installation:
1. Clone the Repository: `git clone https://github.com/Cerne17/ProjetoNotas.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage:
1. Take photos of the notes to be digitized.
2. Place all photos, organized by numerical order, inside the `imagens` folder of the project.
3. Include your Google API Key:
    1. Note that we provide an example of how your `.env` file should be for the code to work.
    2. Another way would be to replace the `GOOGLE_API_KEY` variable value directly in the `main.py` file.
4. Run the main script: `python main.py` or `python3 main.py`
5. Note that all files must have the same name length for sorting to work as expected. That is:
    1. If you need a pdf of `1432` pages, all files must have a name with `4` digits: `0001.png`, `0012.png`, `0123.jpg`, ...
    2. If you need a pdf of `14` pages, all files must have a name with `2` digits: `01.png`, `09.png`, `12.jpg`, ...
    3. And so on.

## Customization:
Feel free to change font settings, writing size, lines per page.
These settings are found in the `__init__` method of the `CriadorDePdf` class, in the `CriadorDePdf.py` file.
