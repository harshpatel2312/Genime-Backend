import os
from google.genai import types, Client
from dotenv import load_dotenv

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
        print(f"Generating {n} image(s) for: {prompt}")

        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=n
            )
        )

        print("✅ Image(s) generated successfully!")
        return response

    except Exception as e:
        print(f"❌ An error occurred during image generation: {e}")
        return None

