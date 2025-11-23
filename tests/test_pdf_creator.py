import pytest
from unittest.mock import MagicMock, patch, mock_open
from src.pdf_creator import PdfCreator

class TestPdfCreator:
    @patch("src.pdf_creator.subprocess.run")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_pdf_latex(self, mock_file, mock_subprocess):
        # Setup
        transcribed_pages = [
            ["Page 1 Line 1", "Page 1 Line 2"],
            ["Page 2 Line 1", "$$E=mc^2$$"]
        ]
        creator = PdfCreator(transcribed_pages, output_filename="test_output.pdf")
        
        # Execute
        creator.create_pdf()
        
        # Verify file writing
        mock_file.assert_called_with("test_output.tex", "w", encoding="utf-8")
        handle = mock_file()
        
        # Check content
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        assert r"\documentclass{article}" in written_content
        assert "Page 1 Line 1" in written_content
        assert r"\newpage" in written_content
        assert "$$E=mc^2$$" in written_content
        assert r"\end{document}" in written_content
        
        # Verify compilation
        mock_subprocess.assert_called_once()
        args = mock_subprocess.call_args[0][0]
        assert args[0] == "pdflatex"
        assert args[-1] == "test_output.tex"

    @patch("src.pdf_creator.subprocess.run")
    @patch("builtins.open", new_callable=mock_open)
    def test_create_pdf_compilation_error(self, mock_file, mock_subprocess):
        # Setup failure simulation
        import subprocess
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, ["pdflatex"], output="Error", stderr="Fatal error")
        
        creator = PdfCreator([["Test"]], output_filename="error.pdf")
        
        # Execute and expect error
        with pytest.raises(RuntimeError) as excinfo:
            creator.create_pdf()
        
        assert "LaTeX compilation failed" in str(excinfo.value)
