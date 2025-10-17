from fastapi import APIRouter,HTTPException,UploadFile,File,Form,Depends
import os 
from datetime import datetime
from hackathon.database import submissions_collection


router = APIRouter(
    prefix = "/files",
    tags = ["File Upload"]
)

UPLOAD_DIR = "uploads"


if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@router.post("/upload")
async def upload_submission_file(
    hackathon_id: str = Form(...),
    user_id : str = Form(...),
    project_name : str = Form(...),
    file: UploadFile = File(...)
):

    allowed_extensions = [".zip", ".pdf", ".pptx"]
    ext = file.filename.split(".")[-1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(status_code = 400,detail = "Invalid file type.")
    

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open (file_path,"wb") as f:
        f.write (await file.read())

    submission_data = {
        "hackathon_id":hackathon_id,
        "user_id":user_id,
        "project_name":project_name,
        "filename":file.filename,
        "file_path":file_path,
        "submitted_at":datetime.utcnow()
    }
            
    result = submissions_collection.insert_one(submission_data)

    return {"message":"File uploaded successfully","file_path":file_path,"submission_id":str(result.inserted_id)}
