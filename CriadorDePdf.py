from fpdf import FPDF
import os
import matplotlib.pyplot as plt
import matplotlib


class CriadorDePdf:
    DEFAULT_FONT = "Arial"
    DEFAULT_FONT_SIZE = 12
    DEFAULT_LINES_PER_PAGE = 50
    DEFAULT_OUTPUT_DIR = "./output"
    DEFAULT_TEMP_DIR_NAME = "temp_images"

    def __init__(self,
                 paginas,
                 linhas_por_pagina=DEFAULT_LINES_PER_PAGE,
                 output_filename="caderno.pdf",
                 output_dir=DEFAULT_OUTPUT_DIR):
        self.pdf = FPDF()
        self.linhas_por_pagina = linhas_por_pagina
        self.linhas_pagina_atual = 0
        self.paginas = paginas
        
        self.output_dir = output_dir
        self.output_filepath = os.path.join(self.output_dir, output_filename)
        self.caminho_dir_png_temporario = os.path.join(self.output_dir, self.DEFAULT_TEMP_DIR_NAME)

        self.fonte = self.DEFAULT_FONT
        self.tamanho_padrao = self.DEFAULT_FONT_SIZE
        self.pagina_atual = 0
        self.numero_total_de_paginas = len(paginas)
        self.contador_de_imagens = 0

        # Use Agg backend for Matplotlib to avoid GUI requirements
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
                # Attempt to extract and render LaTeX equation
                # Note: This extraction logic is basic. For robust parsing,
                # one might need a more sophisticated approach to isolate
                # text before, after, and within $$...$$.
                # Current logic assumes the primary content of the line is the equation.
                cleaned_linha = linha
                # This loop to remove all '$' can be problematic if '$' is used
                # for other purposes or if the equation isn't perfectly formatted.
                # A more targeted extraction of content between '$$' would be better.
                try:
                    # Simplistic extraction: remove '$$' and trim, then re-add '$' for matplotlib
                    # This assumes the line is primarily the equation.
                    equation_content = cleaned_linha.replace("$$", "").strip()
                    if not equation_content: # Skip if empty after stripping
                        self.pdf.multi_cell(0, 5, str(linha), border=0, align='L')
                        continue

                    equacao_for_matplotlib = f"${equation_content}$"
                    
                    self.contador_de_imagens += 1
                    if not os.path.exists(self.caminho_dir_png_temporario):
                        os.makedirs(self.caminho_dir_png_temporario)
                    caminho_png_temporario = os.path.join(self.caminho_dir_png_temporario, f"temp_eq_{self.contador_de_imagens}.png")
                    
                    self.gerar_imagem_latex(equacao_for_matplotlib, caminho_png_temporario)
                    self.pdf.image(caminho_png_temporario, h=50)
                    os.remove(caminho_png_temporario)
                except Exception as e: # Catch specific exceptions if possible
                    print(f"Error processing equation line '{linha.strip()}': {e}")
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
        self.pdf.set_font(self.fonte, size=self.tamanho_padrao)

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

        # print(f"Generating image for: {equacao}") # For debugging
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
            # Consider using logging instead of print for progress/debug messages
            print(f"Processing page {self.pagina_atual} of {self.numero_total_de_paginas}")
            self.linhas_pagina_atual = 0
            tem_equacao = False
            for linha in pagina:
                linha_atual += 1
                if linha.find("$$") != -1:
                    tem_equacao = True
                    # print(f"  Line {linha_atual} contains an equation marker.")
                    break
            # print(f"  Finished scanning page {self.pagina_atual} for equations.")

            if tem_equacao:
                # print(f"Page {self.pagina_atual} has equations, using equation-aware adder.")
                self.adicionar_pagina_com_equacoes(pagina)
            else:
                # print(f"Page {self.pagina_atual} has no equations, using common adder.")
                self.adicionar_pagina_comum(pagina)

        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        self.pdf.output(self.output_filepath)
        print(f"PDF created successfully: {self.output_filepath}")
