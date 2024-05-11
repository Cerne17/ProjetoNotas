from fpdf import FPDF
import tempfile
import os


class CriadorDePdf:
    def __init__(self,
                 paginas,
                 marcador_equacao="--latex-eq--",
                 linhas_por_pagina=50):
        self.marcador_equacao = marcador_equacao
        self.pdf = FPDF()
        self.linhas_por_pagina = linhas_por_pagina
        self.linhas_pagina_atual = 0
        self.paginas = paginas

    def adicionar_pagina_com_equacoes(self, texto):
        """
        Cria um PDF com o conteúdo de texto extraído,
        convertendo equações LaTeX em imagens.
        """
        self.pdf.add_page()
        self.pdf.set_font("Arial", size=12)
        for linha in texto:
            if linha.startswith(self.marcador_equacao):
                # Extrair equação LaTeX
                equacao = linha.replace(self.marcador_equacao, "").strip()
                # Criar imagem da equação
                imagem_path = self.gerar_imagem_latex(equacao)
                # Adicionar imagem ao PDF
                self.pdf.image(imagem_path, w=50, h=10)
                # Remover imagem temporária
                os.remove(imagem_path)
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
        # Criar o arquivo temporário
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex") as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{amsmath}\n")
            f.write("\\pagestyle{empty}\n")
            f.write("\\begin{document}\n")
            f.write("$" + equacao + "$\n")
            f.write("\\end{document}\n")
            f.flush()

        # Comiplar LaTeX para PDF
        os.system(
            "pdflatex -output-directory={} {}"
            .format(os.path.dirname(f.name), f.name)
        )

        # Converter PDF para imagem
        imagem_path = f.name[:-4] + ".png"
        os.system(
            "convert -density 300 {} -quality 90 {}"
            .format(f.name[:-4] + ".pdf", imagem_path)
        )

        return imagem_path

    def criar_pdf(self):
        """
        Adiciona todo o conteúdo ao PDF.
        """
        for pagina in self.paginas:
            self.linhas_pagina_atual = 0
            tem_equacao = False
            for linha in pagina:
                if self.marcador_equacao in linha:
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
