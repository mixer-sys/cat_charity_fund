from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
    donations = relationship('Donation')