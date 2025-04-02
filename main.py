from fastapi import FastAPI, HTTPException, UploadFile, File
import os
from fastapi.responses import FileResponse
from PIL import Image

app = FastAPI()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

def is_valid_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(file_path: str):
    with Image.open(file_path) as img:
        original_size = img.size  
        img = img.resize((800, 800))  
        img.save(file_path, quality=85)  
        return original_size, img.size  

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if not is_valid_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        original_size, new_size = resize_image(file_path) 

        return {
            "filename": file.filename,
            "original_size": original_size,  
            "new_size": new_size, 
            "path": file_path,
            "message": "File uploaded successfully"
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    return FileResponse(file_path)
