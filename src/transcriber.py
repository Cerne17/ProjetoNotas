import os
import google.generativeai as genai
from typing import List, Optional
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class Transcriber:
    """
    Handles the interaction with the Google Gemini API to transcribe text from images.
    """
    
    DEFAULT_MODEL_NAME = "gemini-1.5-flash"
    
    def __init__(self, api_key: str, model_name: str = DEFAULT_MODEL_NAME):
        """
        Initialize the Transcriber with API key and model name.
        
        Args:
            api_key: Google API Key.
            model_name: Name of the Gemini model to use.
        """
        if not api_key:
            raise ValueError("API Key must be provided.")
            
        genai.configure(api_key=api_key)
        
        self.generation_config = {
            "candidate_count": 1,
            "temperature": 0
        }
        
        self.safety_settings = {
            "HARASSMENT": "BLOCK_NONE",
            "HATE": "BLOCK_NONE",
            "SEXUAL": "BLOCK_NONE",
            "DANGEROUS": "BLOCK_NONE"
        }
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        # Prompt designed to handle equations and formatting
        self.prompt = """Transcreva o conteúdo desta imagem de um caderno.
Tente sempre seguir uma mesma formatação, padronização e evitar ao máximo adaptações, sendo o mais fidedígno ao texto original. Mantenha sempre o idioma original do texto.
Caso haja equações, siga as seguintes regras:
    Todas equações devem ser expressas em LaTeX, não há necessidade de configurar o arquivo LaTeX.
    Note que essa transcrição será utilizada para gerar pdf usando python, então cada linha deverá ser separada por um caractere de nova linha '\\n'"""

    def transcribe_images(self, image_paths: List[str]) -> List[List[str]]:
        """
        Transcribes a list of images.
        
        Args:
            image_paths: List of file paths to the images.
            
        Returns:
            A list of lists, where each inner list contains the lines of text for a page.
        """
        transcribed_pages = []
        
        for path in image_paths:
            try:
                logger.info(f"Transcribing image: {path}")
                image = Image.open(path)
                response = self.model.generate_content(
                    [self.prompt, image], stream=True
                )
                response.resolve()
                
                if response.text:
                    transcribed_pages.append(response.text.split("\n"))
                else:
                    logger.warning(f"No text generated for {path}")
                    transcribed_pages.append([])
                    
            except Exception as e:
                logger.error(f"Error transcribing {path}: {e}")
                transcribed_pages.append([f"Error transcribing page: {e}"])
                
        return transcribed_pages
