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

# ✅ STATIC MOUNT (ONLY ONCE)
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

# ✅ Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ Include router
app.include_router(news.router)

templates = Jinja2Templates(directory="backend/app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):

    news_list = db.query(News).all()

    pages = []
    newspaper_folder = "app/static/newspaper"

    if os.path.exists(newspaper_folder):
        for file in sorted(os.listdir(newspaper_folder)):
            if file.lower().endswith(".jpg"):
                pages.append(f"newspaper/{file}")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "news_list": news_list,
            "pages": pages
        }
    )