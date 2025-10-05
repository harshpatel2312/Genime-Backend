from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64

from app.services.imagen_service import generate_image

app = FastAPI(title="Genime-Backend")

# CORS setup
origins = ["http://127.0.0.1:5500", "http://localhost:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    prompt: str
    number_of_images: int


@app.post("/generate")
async def generate(req: GenerateRequest):
    try:
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
