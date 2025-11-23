from fpdf import FPDF
import os
import re
import shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List
import logging

logger = logging.getLogger(__name__)

class PdfCreator:
    """
    Creates a PDF from transcribed text, handling LaTeX equations by rendering them as images.
    """
    
    DEFAULT_FONT = "Arial"
    DEFAULT_FONT_SIZE = 12
    DEFAULT_LINES_PER_PAGE = 50
    DEFAULT_OUTPUT_DIR = "./output"
    DEFAULT_TEMP_DIR_NAME = "temp_images"

    # PDF Element Styling
    PDF_CELL_HEIGHT = 5
    PDF_CELL_WIDTH = 0  # 0 means full available width
    PDF_CELL_BORDER = 0
    PDF_CELL_ALIGN = 'L'

    # LaTeX Image Styling
    LATEX_IMAGE_HEIGHT = 10
    LATEX_EQUATION_FONT_SIZE = 20
    LATEX_IMAGE_DPI = 300

    def __init__(self,
                 input_pages_data: List[List[str]],
                 lines_per_pdf_page: int = DEFAULT_LINES_PER_PAGE,
                 output_filename: str = "caderno.pdf",
                 output_dir: str = DEFAULT_OUTPUT_DIR):
        """
        Initialize the PdfCreator.
        
        Args:
            input_pages_data: List of pages, where each page is a list of text lines.
            lines_per_pdf_page: Number of lines before forcing a new page.
            output_filename: Name of the output PDF file.
            output_dir: Directory to save the PDF.
        """
        self.pdf = FPDF()
        self.lines_per_pdf_page = lines_per_pdf_page
        self.current_pdf_page_lines_count = 0
        self.input_pages_data = input_pages_data
        
        self.output_dir = output_dir
        self.output_filepath = os.path.join(self.output_dir, output_filename)
        self.temp_image_dir_path = os.path.join(self.output_dir, self.DEFAULT_TEMP_DIR_NAME)

        self.font_name = self.DEFAULT_FONT
        self.default_font_size = self.DEFAULT_FONT_SIZE
        
        self.total_images_generated = 0

    def _start_new_pdf_page(self):
        """Adds a new page to the PDF and resets line counter."""
        self.pdf.add_page()
        self.pdf.set_font(self.font_name, size=self.default_font_size)
        self.current_pdf_page_lines_count = 0

    def _add_text_to_pdf(self, text_content: str):
        """Adds a block of text to the PDF."""
        lines_for_this_block = 1 

        if self.current_pdf_page_lines_count + lines_for_this_block > self.lines_per_pdf_page and self.current_pdf_page_lines_count > 0:
            self._start_new_pdf_page()

        self.pdf.multi_cell(self.PDF_CELL_WIDTH, self.PDF_CELL_HEIGHT, str(text_content),
                            border=self.PDF_CELL_BORDER, align=self.PDF_CELL_ALIGN)
        self.current_pdf_page_lines_count += lines_for_this_block

    def _generate_latex_image(self, matplotlib_equation_str: str, output_image_path: str):
        """Generates an image from a LaTeX equation string using Matplotlib."""
        fig = plt.figure()
        plt.axis("off")
        plt.text(0.5, 0.5, matplotlib_equation_str, 
                 size=self.LATEX_EQUATION_FONT_SIZE, 
                 ha="center", va="center")

        plt.savefig(output_image_path, format="png",
                    bbox_inches="tight", pad_inches=0.1,
                    dpi=self.LATEX_IMAGE_DPI)
        plt.close(fig)

    def _process_input_line(self, line_text: str):
        """Processes a single input line, handling text and LaTeX equations."""
        parts = re.split(r"(\$\$.*?\$\$)", line_text)

        for part_text in parts:
            if not part_text:
                continue

            is_equation_part = part_text.startswith("$$") and part_text.endswith("$$")

            if is_equation_part:
                extracted_equation = part_text[2:-2].strip()

                if not extracted_equation:
                    self._add_text_to_pdf(part_text)
                    continue
                
                try:
                    effective_image_lines = max(1, int(self.LATEX_IMAGE_HEIGHT / self.PDF_CELL_HEIGHT))

                    if self.current_pdf_page_lines_count + effective_image_lines > self.lines_per_pdf_page and self.current_pdf_page_lines_count > 0:
                        self._start_new_pdf_page()

                    matplotlib_equation_str = f"${extracted_equation}$"
                    self.total_images_generated += 1
                    
                    if not os.path.exists(self.temp_image_dir_path):
                        os.makedirs(self.temp_image_dir_path)
                    
                    temp_image_filename = f"temp_eq_{self.total_images_generated}.png"
                    temp_image_file_path = os.path.join(self.temp_image_dir_path, temp_image_filename)
                    
                    self._generate_latex_image(matplotlib_equation_str, temp_image_file_path)
                    self.pdf.image(temp_image_file_path, h=self.LATEX_IMAGE_HEIGHT)
                    os.remove(temp_image_file_path)

                    self.current_pdf_page_lines_count += effective_image_lines

                except Exception as e:
                    logger.error(f"Error rendering equation '{extracted_equation}': {e}. Adding as raw text.")
                    self._add_text_to_pdf(part_text)
            else:
                self._add_text_to_pdf(part_text)

    def create_pdf(self):
        """Main method to generate the PDF."""
        self.total_images_generated = 0

        try:
            for page_idx, page_lines_list in enumerate(self.input_pages_data):
                logger.info(f"Processing input page {page_idx + 1} of {len(self.input_pages_data)}")
                self._start_new_pdf_page()

                for line_text in page_lines_list:
                    self._process_input_line(line_text)
            
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            
            self.pdf.output(self.output_filepath)
            logger.info(f"PDF created successfully: {self.output_filepath}")

        finally:
            if os.path.exists(self.temp_image_dir_path):
                try:
                    shutil.rmtree(self.temp_image_dir_path)
                    logger.info(f"Temporary image directory {self.temp_image_dir_path} removed.")
                except Exception as e:
                    logger.warning(f"Could not remove temporary image directory {self.temp_image_dir_path}: {e}")
