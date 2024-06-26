# Sobre o Projeto
Este projeto tem como objetivo resolver um grande problema que 
tenho há muito tempo - digitalizar meus materiais e notas de
forma simples e rápida. 
Com o auxílio da API do Google Gemini, eu consegui criar um 
sistema que ataca exatamente este problema.
Eu, minha mãe, minha avó, todos já nos encontramos na situação
de querer salvar algum material escrito à mão de forma digital,
seja para ter mais formalidade ou até mesmo para ter como alterá-lo
de forma mais simples posteriormente, mas nunca tivemos acesso à
ferramenta correta. 
Para isso, criei o `ProjetoNotas`. O projeto em que utilizamos o
potente modelo Gemini da Google para criar de forma automática e
dinâmica materiais digitalizados de nossas mídias físicas!


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
Essas configurações encontram-se no método `__init__` da classe `CriadorDePdf`, no arquivo
`CriadorDePdf.py`.
