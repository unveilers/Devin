from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECT = "prospect"

class OpportunityStage(str, Enum):
    LEAD = "lead"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class Customer(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    status: CustomerStatus = CustomerStatus.PROSPECT
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Opportunity(BaseModel):
    id: Optional[int] = None
    customer_id: int
    title: str
    description: Optional[str] = None
    value: float
    stage: OpportunityStage = OpportunityStage.LEAD
    probability: int = 0  # 0-100
    expected_close_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Campaign(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Activity(BaseModel):
    id: Optional[int] = None
    customer_id: int
    opportunity_id: Optional[int] = None
    type: str  # call, email, meeting, note
    subject: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

class SalesMetrics(BaseModel):
    total_customers: int
    active_customers: int
    total_opportunities: int
    total_pipeline_value: float
    won_opportunities: int
    won_value: float
    conversion_rate: float
    avg_deal_size: float
