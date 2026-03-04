from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from backend.app.database import Base, engine, get_db
from backend.app.models import News
from backend.app.routes import news

app = FastAPI()

# STATIC FILES
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

# DATABASE TABLE CREATE
Base.metadata.create_all(bind=engine)

# ROUTER
app.include_router(news.router)

templates = Jinja2Templates(directory="backend/app/templates")

# ✅ PDF PATH
pdf_path = "backend/app/uploads/02march2026punevaibhavfinalpages.pdf"


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):

    news_list = db.query(News).all()

    pages = []
    newspaper_folder = "backend/app/static/newspaper"

    if os.path.exists(newspaper_folder):
        for file in sorted(os.listdir(newspaper_folder)):
            if file.lower().endswith(".jpg"):
                pages.append(f"/static/newspaper/{file}")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "news_list": news_list,
            "pages": pages,
            "pdf_file": pdf_path
        }
    )