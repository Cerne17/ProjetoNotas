from fpdf import FPDF
import os
import matplotlib.pyplot as plt
import matplotlib


class CriadorDePdf:
    def __init__(self,
                 paginas,
                 linhas_por_pagina=50):
        self.pdf = FPDF()
        self.linhas_por_pagina = linhas_por_pagina
        self.linhas_pagina_atual = 0
        self.paginas = paginas
        self.caminho_png_temporario = "./output/temp"

        self.fonte = "Arial"
        self.tamanho_padrao = 12
        self.pagina_atual = 0
        self.numero_total_de_paginas = len(paginas)
        self.contador_de_imagens = 0

        # Usa o Backend Agg para não usarmos a interface gráfica do matplotlib
        matplotlib.use("Agg")

    def adicionar_pagina_com_equacoes(self, texto):
        """
        Cria um PDF com o conteúdo de texto extraído,
        convertendo equações LaTeX em imagens.
        """
        self.pdf.add_page()
        self.pdf.set_font(self.fonte, size=self.tamanho_padrao)
        self.contador_de_imagens = 0
        for linha in texto:
            if linha.find("$$") != -1:
                try:
                    # Extrair equação LaTeX
                    while linha.find("$") != -1:
                        linha = linha.replace("$", "")
                    equacao = f"${linha.strip()}$"
                    # Criar imagem da equação
                    self.contador_de_imagens += 1
                    caminho_png_temporario = f"{self.caminho_png_temporario}{
                        self.contador_de_imagens}.png"
                    self.gerar_imagem_latex(equacao, caminho_png_temporario)
                    # Adicionar imagem ao PDF
                    self.pdf.image(caminho_png_temporario, h=50)
                    # Remover imagem temporária
                    os.remove(caminho_png_temporario)
                except:
                    self.pdf.multi_cell(0, 5, str(linha), border=0, align='L')
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

    def gerar_imagem_latex(self, equacao, caminho_png):
        """
            Gera uma imagem a partir de uma equação LaTeX.
        """
        fig = plt.figure()

        print(equacao)
        plt.axis("off")
        plt.text(0.5, 0.5, equacao, size=20, ha="center", va="center")

        plt.savefig(caminho_png, format="png",
                    bbox_inches="tight", pad_inches=0, dpi=300)
        plt.close(fig)

    def criar_pdf(self):
        """
        Adiciona todo o conteúdo ao PDF.
        """
        for pagina in self.paginas:
            self.pagina_atual += 1
            linha_atual = 0
            print(f"Digitalizando a página {self.pagina_atual} de {
                  self.numero_total_de_paginas}")
            self.linhas_pagina_atual = 0
            tem_equacao = False
            for linha in pagina:
                linha_atual += 1
                if linha.find("$$") != -1:
                    tem_equacao = True
                    break
            if tem_equacao:
                print(f"Digitalizando a linha {
                      linha_atual} -> Linha com equação")
                self.adicionar_pagina_com_equacoes(pagina)
            else:
                print(f"Digitalizando a linha {
                      linha_atual} -> Linha sem equação")
                self.adicionar_pagina_comum(pagina)

        # Salvar o PDF com o nome genérico "caderno.pdf" na pastar ./output/
        if not os.path.exists("output"):
            os.makedirs("output")
        self.pdf.output("./output/caderno.pdf")
