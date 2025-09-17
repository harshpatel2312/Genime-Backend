from fastapi import FastAPI
from pydantic import BaseModel
from app.services.imagen_service import generate_image
from app.services.save_image import save_image

app = FastAPI(title="Genima")

class GenerateRequest(BaseModel):
    prompt: str
    number_of_images: int

@app.post("/generate")
async def generate(req: GenerateRequest):
    try:
        result = generate_image(req.prompt, req.number_of_images)
        print(result)

        saved_files = []

        if result is not None:
            for item in result.generated_images:
                image_obj = item.image
                if image_obj and image_obj.image_bytes:
                    filepath = save_image(image_obj.image_bytes)
                    saved_files.append(filepath)
            return {"status": "success", "files": saved_files, "count": len(saved_files)}

    except Exception as e:
        return {"status": "error", "message": str(e)}