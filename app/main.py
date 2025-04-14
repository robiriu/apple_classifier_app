# app/main.py

import os
import uuid
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.detect import detect_and_crop

app = FastAPI()

# Allow frontend to connect (CORS setup if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static files and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(BASE_DIR, "templates")  # Ensure this is correct

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=templates_dir)

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
CROP_FOLDER = os.path.join(BASE_DIR, "static", "crops")

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CROP_FOLDER, exist_ok=True)

# Temporary modification to render test.html
@app.get("/")
async def home(request: Request):
    try:
        return templates.TemplateResponse("test.html", {"request": request})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Failed to render test.html", "details": str(e)})

@app.post("/detect/")
async def detect(request: Request, file: UploadFile = File(...)):
    try:
        # Save uploaded image
        contents = await file.read()
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(contents)

        # Run detection and cropping logic
        result = detect_and_crop(file_path, CROP_FOLDER)

        # Return response with accessible paths
        return JSONResponse(content={"message": "Detection completed", "results": result})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
