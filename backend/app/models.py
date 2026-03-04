from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from backend.app.database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    area = Column(String(100))
    image_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)