
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, text
from sqlalchemy.orm import relationship

from app.database.database import Base


class BrowserConfig(Base):
    __tablename__ = "browser_config"

    id = Column(Integer, primary_key=True, index=True)

    browser_info_id = Column(Integer, ForeignKey("browser_info.id", ondelete="CASCADE"), nullable=False)
    ip_info = Column(JSON, nullable=False, index=True) 
    check_ip_web = Column(String(255), nullable=True, server_default="https://whoer.net/") 
    window_width = Column(Integer, nullable=False) 
    window_height = Column(Integer, nullable=False) 
    user_agent = Column(String(500), nullable=False) 
    browser_language = Column(String(40), nullable=False) 
    browser_languages = Column(JSON, nullable=False) 
    hardware_concurrency = Column(Integer, nullable=False) 
    device_memory = Column(Integer, nullable=False)
    webgl_vendor = Column(String(255), nullable=False) 
    webgl_renderer = Column(String(255), nullable=False) 
    browser_font = Column(JSON, nullable=False) 
    chrome_version = Column(String(50), nullable=False, default="148.0.7778.216", server_default=text("'148.0.7778.216'")) 
    canvas_noise = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # back reference to BrowserInfo
    browser_info = relationship("BrowserInfo", back_populates="configs")
