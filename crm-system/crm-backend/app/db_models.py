from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

from .models import CustomerStatus, OpportunityStage, CampaignStatus

Base = declarative_base()

class CustomerDB(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    status = Column(SQLEnum(CustomerStatus), default=CustomerStatus.PROSPECT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    opportunities = relationship("OpportunityDB", back_populates="customer")
    activities = relationship("ActivityDB", back_populates="customer")

class OpportunityDB(Base):
    __tablename__ = "opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    value = Column(Float, nullable=False)
    stage = Column(SQLEnum(OpportunityStage), default=OpportunityStage.LEAD)
    probability = Column(Integer, default=0)
    expected_close_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    customer = relationship("CustomerDB", back_populates="opportunities")
    activities = relationship("ActivityDB", back_populates="opportunity")

class CampaignDB(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT)
    budget = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ActivityDB(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    type = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("CustomerDB", back_populates="activities")
    opportunity = relationship("OpportunityDB", back_populates="activities")
