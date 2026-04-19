from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
import os
from extractor import extract

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract_from_doc")
def extract_from_doc(
        file_format: str = Form(...),
        file: UploadFile = File(...),
):
    contents = file.file.read()

    file_path = "../uploads/" + str(uuid.uuid4()) + ".pdf"

    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        data = extract(file_path, file_format)
    except Exception as e:
        data = {'error': str(e)}

    if os.path.exists(file_path):
        os.remove(file_path)

    return data


@app.post("/test_extract")
async def test_extract(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = "../uploads/test.pdf"
    with open(file_path, "wb") as f:
        f.write(contents)
    from pdf2image import convert_from_path
    import pytesseract
    import util
    pages = convert_from_path(file_path, poppler_path=r"C:\poppler\Library\bin")
    page = pages[0]
    processed_image = util.preprocess_image(page)
    text = pytesseract.image_to_string(processed_image, lang="eng")
    return {"extracted_text": text}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)