from fpdf import FPDF
import os
import matplotlib.pyplot as plt
from pdf2image import convert_from_path


class CriadorDePdf:
    def __init__(self,
                 paginas,
                 linhas_por_pagina=50):
        self.pdf = FPDF()
        self.linhas_por_pagina = linhas_por_pagina
        self.linhas_pagina_atual = 0
        self.paginas = paginas
        self.caminho_pdf_temporario = "./output/temp.pdf"
        self.caminho_png_temporario = "./output/temp.png"

        self.fonte = "Arial"
        self.tamanho_padrao = 12

    def adicionar_pagina_com_equacoes(self, texto):
        """
        Cria um PDF com o conteúdo de texto extraído,
        convertendo equações LaTeX em imagens.
        """
        self.pdf.add_page()
        self.pdf.set_font(self.fonte, size=self.tamanho_padrao)
        for linha in texto:
            if linha.find("$$") != -1:
                # Extrair equação LaTeX
                equacao = linha.strip()
                # Criar imagem da equação
                self.gerar_imagem_latex(equacao)
                # Adicionar imagem ao PDF
                self.pdf.image(self.caminho_png_temporario, w=50, h=10)
                # Remover imagem temporária
                os.remove(self.caminho_png_temporario)
            else:
                self.pdf.multi_cell(0, 5, str(linha), border=0, align='L')
            self.linhas_pagina_atual += 1
            if self.linhas_pagina_atual == self.linhas_por_pagina:
                self.linhas_pagina_atual = 0
                self.pdf.add_page()

    def adicionar_pagina_comum(self, texto):
        """
        Cria um PDF com o conteúdo de texto extraído,
        para PDF's com texto puro.
        """
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)

        for linha in texto:
            self.pdf.multi_cell(0, 5, str(linha), border=0, align='L')
            self.linhas_pagina_atual += 1
            if self.linhas_pagina_atual == self.linhas_por_pagina:
                self.linhas_pagina_atual = 0
                self.pdf.add_page()

    def gerar_imagem_latex(self, equacao):
        """
            Gera uma imagem a partir de uma eqação LaTeX.
        """
        fig = plt.figure()

        plt.axis("off")
        plt.text(0.5, 0.5, f"${equacao}$", size=20, ha="center", va="center")

        plt.savefig(self.caminho_pdf_temporario,
                    bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)

        imagens = convert_from_path(self.caminho_pdf_temporario)
        imagens[0].save(self.caminho_png_temporario, "PNG")

    def criar_pdf(self):
        """
        Adiciona todo o conteúdo ao PDF.
        """
        for pagina in self.paginas:
            self.linhas_pagina_atual = 0
            tem_equacao = False
            for linha in pagina:
                if linha.find("$$") != -1:
                    tem_equacao = True
                    break
            if tem_equacao:
                self.adicionar_pagina_com_equacoes(pagina)
            else:
                self.adicionar_pagina_comum(pagina)

        # Salvar o PDF com o nome genérico "caderno.pdf" na pastar ./output/
        if not os.path.exists("output"):
            os.makedirs("output")
        self.pdf.output("./output/caderno.pdf")
