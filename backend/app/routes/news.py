from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pdf2image import convert_from_path
import os

from backend.app.database import get_db
from backend.app.models import News

router = APIRouter()

templates = Jinja2Templates(directory="backend/app/templates")


# -----------------------------
# CREATE NEWS API
# -----------------------------
@router.post("/news")
def create_news(
    title: str = Form(...),
    content: str = Form(...),
    area: str = Form(...),
    image_path: str = Form(...),
    db: Session = Depends(get_db)
):

    news = News(
        title=title,
        content=content,
        area=area,
        image_path=image_path
    )

    db.add(news)
    db.commit()
    db.refresh(news)

    return {"message": "News added successfully"}


# -----------------------------
# E-PAPER ROUTE
# -----------------------------
@router.get("/edition")
def show_edition(request: Request):

    pdf_path = "backend/app/uploads/02march2026punevaibhavfinalpages.pdf"
    output_folder = "backend/app/static/newspaper"

    if not os.path.exists(pdf_path):
        return {"error": "PDF file not found in uploads folder"}

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

        image_list.append(f"static/newspaper/{filename}")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pages": image_list,
            "news_list": []
        }
    )


# -----------------------------
# AREA FILTER ROUTE
# -----------------------------
@router.get("/area/{area_name}")
def news_by_area(area_name: str, request: Request, db: Session = Depends(get_db)):

    news_list = db.query(News).filter(News.area.ilike(area_name)).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "news_list": news_list,
            "pages": []
        }
    )


# -----------------------------
# NEWS DETAIL PAGE
# -----------------------------
@router.get("/news/{news_id}")
def news_detail(news_id: int, request: Request, db: Session = Depends(get_db)):

    news = db.query(News).filter(News.id == news_id).first()

    if not news:
        return {"error": "News not found"}

    return templates.TemplateResponse(
        "news_detail.html",
        {
            "request": request,
            "news": news
        }
    )