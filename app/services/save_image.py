import os
from base64 import b64encode
from datetime import datetime
from PIL import Image
from io import BytesIO

def save_image(image_bytes, output_dir: str = "assets/generated-images/"):
    """
         Save base64 image string as PNG in local folder.
         Returns the file path.
     """
    print("Saving generated image...")
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(output_dir, filename)

    image = Image.open(BytesIO(image_bytes))
    image.save(filepath)
    print(f"Saved image to {filepath}")

    return filepath