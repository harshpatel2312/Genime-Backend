import os
from google.genai import types, Client
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load env variables
load_dotenv()
api_key = os.getenv("IMAGEN_API_KEY")

# Initialize client
client = Client(api_key=api_key)

def generate_image(prompt: str, n: int = 1):
    """
        Generate image using Imagen
    """
    try:
        logger.info(f"Generating {n} image(s) for: {prompt}")

        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=n
            )
        )

        logger.info("Image(s) generated successfully!")
        return response

    except Exception as e:
        logger.info(f"❌ An error occurred during image generation: {e}")
        return None

