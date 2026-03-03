from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pdf2image import convert_from_path
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/edition")
def show_edition(request: Request):

    pdf_path = "app/uploads/02march2026punevaibhavfinalpages.pdf"
    output_folder = "app/static/newspaper"

    # 🔎 Check PDF exists
    if not os.path.exists(pdf_path):
        return {"error": "PDF file not found in uploads folder"}

    # 📁 Create folder if not exists
    os.makedirs(output_folder, exist_ok=True)

    try:
        pages = convert_from_path(pdf_path, dpi=200)
    except Exception as e:
        return {"error": f"PDF conversion failed: {str(e)}"}

    image_list = []

    for i, page in enumerate(pages):
        filename = f"page_{i+1}.jpg"
        save_path = os.path.join(output_folder, filename)
        page.save(save_path, "JPEG")
        image_list.append(f"newspaper/{filename}")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pages": image_list,
            "news_list": []
        }
    )