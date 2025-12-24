from sqlalchemy import Column, Integer, String
from .database import Base

class UrlModel(Base):
    __tablename__ = "short_url"
    
    id = Column(Integer, primary_key=True, index=True)
    full_url = Column(String, nullable=False)
    # short_url = Column(String, nullable=False)
 