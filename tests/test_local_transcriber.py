import pytest
from unittest.mock import MagicMock, patch
from src.local_transcriber import LocalTranscriber

class TestLocalTranscriber:
    @patch("src.local_transcriber.Llama")
    @patch("src.local_transcriber.Llava15ChatHandler")
    @patch("src.local_transcriber.hf_hub_download")
    @patch("src.local_transcriber.os.path.exists")
    def test_transcribe_images_local(self, mock_exists, mock_download, mock_handler, mock_llama):
        # Setup mocks
        mock_exists.return_value = False # Simulate model not found to trigger download logic
        mock_download.return_value = "/tmp/dummy_model.gguf"
        
        mock_llm_instance = MagicMock()
        mock_llama.return_value = mock_llm_instance
        
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": "Line 1\nLine 2"
                    }
                }
            ]
        }
        mock_llm_instance.create_chat_completion.return_value = mock_response
        
        # Initialize
        transcriber = LocalTranscriber()
        
        # Verify download was called
        assert mock_download.call_count == 2 # Main model + CLIP model
        
        # Test transcription
        result = transcriber.transcribe_images(["dummy_path.jpg"])
        
        assert len(result) == 1
        assert result[0] == ["Line 1", "Line 2"]
        mock_llm_instance.create_chat_completion.assert_called_once()
