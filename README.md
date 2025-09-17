# Genime-Backend

Backend service for the **Genime** project — a full-scale web app (like *nano banana*) using **Google Imagen-4** for **Anime-Style** generation.  

This repo contains the **FastAPI backend**, responsible for:
- Handling API requests  
- Calling Imagen-4 model to generate images  
- Saving images locally (for now; cloud storage will be added later)  

---

## 📂 Project Structure
```bash
Genime-Backend/
│
├── app/
│   ├── main.py # FastAPI entry point
│   └── services/
│       └── imagen_service.py # Imagen client + save helpers
│
├── assets/
├   └── generated_images/ # Saved images (auto-created)
|
├── .env # Stores your API key
├── requirements.txt # Python dependencies
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Clone repo** & create virtual environment:
   ```bash
     git clone https://github.com/harshpatel2312/Genime-Backend.git
     cd Genime-Backend
   
     python -m venv venv
   
     source venv/bin/activate   # Linux/Mac
     venv\Scripts\activate      # Windows
   ```

2. Install dependencies:
   ```bash
     pip install -r requirements.txt
   ```

3. Create `.env` file in project root:
   ```python
     IMAGEN_API_KEY=your_api_key_here
   ```

4. Run the server:
   ```bash
     uvicorn app.main:app --reload
   ```

---

## 🚀 API Endpoints

| Method | Endpoint     | Description                                                | Request Body Example | Response Example |
|--------|-------------|------------------------------------------------------------|----------------------|------------------|
| POST   | `/generate` | Generate one or more images from a text prompt using Imagen-4 and save them locally | ```json { "prompt": "Robot holding a red skateboard", "number_of_images": 1 } ``` | ```json { "status": "success", "files": ["assets/generated_images/20250916_175422.png"], "count": 1 } ``` |

---

## 🛠️ How Images Are Saved

- Images are returned by the Imagen API as raw **PNG bytes**.
- They are saved locally in the `assets/generated_images/` folder with filenames like:
  ```bash
    YYYYMMDD_HHMMSS.png
  ```
- Internally, saving is handled by **PIL (Pillow)**:
  ```python
    from PIL import Image
    import io
    
    image = Image.open(io.BytesIO(image_bytes))
    image.save("assets/generated_images/filename.png")
  ```

---

## ✅ Roadmap
- Save generated images in **cloud storage (GCP)**
- Add **authentication & user accounts**
- Store image metadata in **PostgreSQL**
- Integrate **Celery + Redis** for background tasks
- Add more endpoints (`/gallery`, `/auth`, etc.)
- Connect to **Genime-Frontend** repo

---

## 📖 References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Imagen Documentation](https://ai.google.dev/gemini-api/docs/imagen)
- [Pillow (PIL) Docs](https://pillow.readthedocs.io/en/stable/)
