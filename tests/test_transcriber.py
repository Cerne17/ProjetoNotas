import pytest
from unittest.mock import MagicMock, patch
from src.transcriber import Transcriber

class TestTranscriber:
    @patch("src.transcriber.genai")
    @patch("src.transcriber.Image")
    def test_transcribe_images(self, mock_image, mock_genai):
        # Setup mocks
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Line 1\nLine 2"
        mock_model.generate_content.return_value = mock_response
        
        transcriber = Transcriber(api_key="dummy_key")
        result = transcriber.transcribe_images(["dummy_path.jpg"])
        
        assert len(result) == 1
        assert result[0] == ["Line 1", "Line 2"]
        mock_model.generate_content.assert_called_once()

    def test_init_no_api_key(self):
        with pytest.raises(ValueError):
            Transcriber(api_key="")
