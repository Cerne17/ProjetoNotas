import pytest
import os
from src.pdf_creator import PdfCreator

class TestPdfCreator:
    def test_pdf_creation_simple_text(self, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        input_data = [["Line 1", "Line 2"], ["Page 2 Line 1"]]
        creator = PdfCreator(input_data, output_dir=str(output_dir), output_filename="test.pdf")
        creator.create_pdf()
        
        assert (output_dir / "test.pdf").exists()

    def test_pdf_creation_with_equation(self, tmp_path):
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        input_data = [["Equation: $$E=mc^2$$"]]
        creator = PdfCreator(input_data, output_dir=str(output_dir), output_filename="eq_test.pdf")
        creator.create_pdf()
        
        assert (output_dir / "eq_test.pdf").exists()
