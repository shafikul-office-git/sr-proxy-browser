
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship

from app.database.database import Base


class BrowserInfo(Base):
    __tablename__ = "browser_info"

    id = Column(Integer, primary_key=True, index=True)

    profile_name = Column(String(100), nullable=False, index=True)
    folder_name = Column(String(255), nullable=False, unique=True)
    browser_port = Column(Integer, nullable=False, unique=True)
    proxy_type = Column(Enum("https", "http", "socks5", "socks4", "socks5h", name="proxy_type"), nullable=False, default="http")
    proxy_host = Column(String(45), nullable=True)
    proxy_port = Column(Integer, nullable=True)
    proxy_username = Column(String(100), nullable=True)
    proxy_password = Column(String(255), nullable=True)
    proxy_country = Column(String(255), nullable=True)
    proxy_city = Column(String(255), nullable=True)
    proxy_status = Column(Boolean, nullable=False, default=False)
    status = Column(Enum("running", "closed", "created", name="browser_status"), default="created")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # ORM relationship to cascade deletes at the ORM level
    configs = relationship("BrowserConfig", back_populates="browser_info", cascade="all, delete-orphan", passive_deletes=True)
