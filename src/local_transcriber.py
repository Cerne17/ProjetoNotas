import os
import logging
from typing import List
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

logger = logging.getLogger(__name__)

class LocalTranscriber:
    """
    Handles transcription using a local LLaVA model via llama-cpp-python.
    """
    
    # Default model: LLaVA v1.5 7B (quantized to 4-bit)
    DEFAULT_REPO_ID = "mys/ggml_llava-v1.5-7b"
    DEFAULT_FILENAME = "ggml-model-q4_k.gguf"
    DEFAULT_CLIP_FILENAME = "mmproj-model-f16.gguf"

    def __init__(self, model_path: str = None, n_ctx: int = 2048, n_gpu_layers: int = -1):
        """
        Initialize the LocalTranscriber.
        
        Args:
            model_path: Path to the directory containing model files. If None, downloads to cache.
            n_ctx: Context window size.
            n_gpu_layers: Number of layers to offload to GPU (-1 for all).
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_gpu_layers = n_gpu_layers
        
        self._ensure_model_exists()
        
        logger.info("Loading local LLaVA model...")
        chat_handler = Llava15ChatHandler(clip_model_path=self.clip_model_path)
        
        self.llm = Llama(
            model_path=self.main_model_path,
            chat_handler=chat_handler,
            n_ctx=self.n_ctx,
            n_gpu_layers=self.n_gpu_layers,
            logits_all=True, # Needed for proper chat handling in some versions
            verbose=False
        )
        logger.info("Local LLaVA model loaded successfully.")

        self.prompt = """Transcreva o conteúdo desta imagem de um caderno.
Tente sempre seguir uma mesma formatação, padronização e evitar ao máximo adaptações, sendo o mais fidedígno ao texto original. Mantenha sempre o idioma original do texto.
A saída deve ser formatada para ser inserida diretamente em um documento LaTeX.
Regras:
1. Texto comum deve ser transcrito normalmente.
2. Equações matemáticas devem ser delimitadas por `$$...$$` para equações destacadas (display math) ou `$...$` para equações na linha (inline math).
3. Não use ambientes como `\\begin{equation}` a menos que seja estritamente necessário.
4. Não inclua preâmbulo LaTeX (como `\\documentclass`, `\\usepackage`), apenas o conteúdo do corpo do documento.
5. Separe parágrafos com uma linha em branco."""

    def _ensure_model_exists(self):
        """Checks if model exists locally, otherwise downloads it."""
        if self.model_path and os.path.exists(self.model_path):
            self.main_model_path = os.path.join(self.model_path, self.DEFAULT_FILENAME)
            self.clip_model_path = os.path.join(self.model_path, self.DEFAULT_CLIP_FILENAME)
        else:
            logger.info(f"Model not found locally. Downloading from {self.DEFAULT_REPO_ID}...")
            self.main_model_path = hf_hub_download(
                repo_id=self.DEFAULT_REPO_ID,
                filename=self.DEFAULT_FILENAME
            )
            self.clip_model_path = hf_hub_download(
                repo_id=self.DEFAULT_REPO_ID,
                filename=self.DEFAULT_CLIP_FILENAME
            )
            logger.info(f"Model downloaded to: {self.main_model_path}")

    def transcribe_images(self, image_paths: List[str]) -> List[List[str]]:
        """
        Transcribes a list of images using the local model.
        """
        transcribed_pages = []
        
        for path in image_paths:
            try:
                logger.info(f"Transcribing image locally: {path}")
                
                # LLaVA expects image URI in the content list
                # Note: llama-cpp-python handles file:// URIs or base64
                image_uri = f"file://{os.path.abspath(path)}"
                
                messages = [
                    {"role": "system", "content": "You are a helpful assistant that transcribes handwritten notes."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": image_uri}},
                            {"type": "text", "text": self.prompt}
                        ]
                    }
                ]

                response = self.llm.create_chat_completion(
                    messages=messages,
                    max_tokens=1024,
                    temperature=0.1
                )
                
                text_content = response["choices"][0]["message"]["content"]
                
                if text_content:
                    transcribed_pages.append(text_content.split("\n"))
                else:
                    logger.warning(f"No text generated for {path}")
                    transcribed_pages.append([])
                    
            except Exception as e:
                logger.error(f"Error transcribing {path}: {e}")
                transcribed_pages.append([f"Error transcribing page: {e}"])
                
        return transcribed_pages
