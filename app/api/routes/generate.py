from pydantic import BaseModel
from fastapi import APIRouter
import base64
from app.services.imagen_service import generate_image
import logging

router = APIRouter(prefix="/generate", tags=["Image Generation"])
logger = logging.getLogger(__name__)

class GenerateRequest(BaseModel):
    prompt: str
    number_of_images: int


@router.post("/")
async def generate(req: GenerateRequest):
    try:
        logger.info(f"Routes------/generate------active")
        result = generate_image(req.prompt, req.number_of_images)
        images_base64 = []

        if result is not None:
            for item in result.generated_images:
                image_obj = item.image
                if image_obj and image_obj.image_bytes:
                    # Convert raw image bytes to base64 string
                    img_b64 = base64.b64encode(image_obj.image_bytes).decode("utf-8")
                    images_base64.append(img_b64)

        return {"status": "success", "images": images_base64, "count": len(images_base64)}

    except Exception as e:
        return {"status": "error", "message": str(e)}