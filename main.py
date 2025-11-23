import os
import sys
import logging
from dotenv import load_dotenv
from src.transcriber import Transcriber
from src.pdf_creator import PdfCreator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        logger.error("GOOGLE_API_KEY not found in environment variables.")
        sys.exit(1)

    # Image Extraction
    image_dir = "imagens"
    if not os.path.exists(image_dir):
        logger.error(f"Directory '{image_dir}' not found.")
        sys.exit(1)

    image_paths = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            image_paths.append(os.path.join(image_dir, filename))

    if not image_paths:
        logger.error("No valid images found in 'imagens' directory.")
        sys.exit(1)

    image_paths.sort()
    logger.info(f"Found {len(image_paths)} images to process.")

    # Transcription
    try:
        transcriber = Transcriber(api_key=api_key)
        transcribed_pages = transcriber.transcribe_images(image_paths)
        logger.info("Transcription completed.")
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        sys.exit(1)

    # PDF Creation
    try:
        pdf_creator = PdfCreator(transcribed_pages)
        pdf_creator.create_pdf()
    except Exception as e:
        logger.error(f"PDF creation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
