#Upload and Save Image to Disk
from fastapi import FastAPI, HTTPException, UploadFile, File
import os

from fastapi.responses import FileResponse

app = FastAPI()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

def is_valid_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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

        return {
            "filename": file.filename,
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
