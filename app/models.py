from sqlalchemy import Column, Integer, String
from app.database import Base
from enum import Enum


class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer,primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    email = Column(String(150),unique=True,nullable=False)
    phone = Column(String(20))
    country = Column(String(100))
    course = Column(String(150))
    status = Column(String(50),default = 'New')

class LeadStatus(str, Enum):
    NEW = "New"
    CONTACTED = "Contacted"
    QUALIFIED = "Qualified"
    APPLICATION_STARTED = "Application Started"
    CONVERTED = "Converted"
