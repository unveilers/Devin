import os
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from .db_models import Base, CustomerDB, OpportunityDB, CampaignDB, ActivityDB
from .models import Customer, Opportunity, Campaign, Activity

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

class SQLDatabase:
    def __init__(self):
        pass
    
    def get_db(self) -> Session:
        return SessionLocal()
    
    def _convert_customer_to_pydantic(self, customer_db: CustomerDB) -> Customer:
        return Customer(
            id=customer_db.id,
            first_name=customer_db.first_name,
            last_name=customer_db.last_name,
            email=customer_db.email,
            phone=customer_db.phone,
            company=customer_db.company,
            status=customer_db.status,
            created_at=customer_db.created_at,
            updated_at=customer_db.updated_at
        )
    
    def _convert_opportunity_to_pydantic(self, opportunity_db: OpportunityDB) -> Opportunity:
        return Opportunity(
            id=opportunity_db.id,
            customer_id=opportunity_db.customer_id,
            title=opportunity_db.title,
            description=opportunity_db.description,
            value=opportunity_db.value,
            stage=opportunity_db.stage,
            probability=opportunity_db.probability,
            expected_close_date=opportunity_db.expected_close_date,
            created_at=opportunity_db.created_at,
            updated_at=opportunity_db.updated_at
        )
    
    def _convert_campaign_to_pydantic(self, campaign_db: CampaignDB) -> Campaign:
        return Campaign(
            id=campaign_db.id,
            name=campaign_db.name,
            description=campaign_db.description,
            status=campaign_db.status,
            budget=campaign_db.budget,
            start_date=campaign_db.start_date,
            end_date=campaign_db.end_date,
            created_at=campaign_db.created_at,
            updated_at=campaign_db.updated_at
        )
    
    def _convert_activity_to_pydantic(self, activity_db: ActivityDB) -> Activity:
        return Activity(
            id=activity_db.id,
            customer_id=activity_db.customer_id,
            opportunity_id=activity_db.opportunity_id,
            type=activity_db.type,
            subject=activity_db.subject,
            description=activity_db.description,
            created_at=activity_db.created_at
        )
    
    def create_customer(self, customer: Customer) -> Customer:
        db = self.get_db()
        try:
            customer_db = CustomerDB(
                first_name=customer.first_name,
                last_name=customer.last_name,
                email=customer.email,
                phone=customer.phone,
                company=customer.company,
                status=customer.status
            )
            db.add(customer_db)
            db.commit()
            db.refresh(customer_db)
            return self._convert_customer_to_pydantic(customer_db)
        finally:
            db.close()
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        db = self.get_db()
        try:
            customer_db = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
            if customer_db:
                return self._convert_customer_to_pydantic(customer_db)
            return None
        finally:
            db.close()
    
    def get_all_customers(self) -> List[Customer]:
        db = self.get_db()
        try:
            customers_db = db.query(CustomerDB).all()
            return [self._convert_customer_to_pydantic(customer_db) for customer_db in customers_db]
        finally:
            db.close()
    
    def update_customer(self, customer_id: int, customer_data: dict) -> Optional[Customer]:
        db = self.get_db()
        try:
            customer_db = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
            if customer_db:
                for key, value in customer_data.items():
                    if hasattr(customer_db, key):
                        setattr(customer_db, key, value)
                customer_db.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(customer_db)
                return self._convert_customer_to_pydantic(customer_db)
            return None
        finally:
            db.close()
    
    def delete_customer(self, customer_id: int) -> bool:
        db = self.get_db()
        try:
            customer_db = db.query(CustomerDB).filter(CustomerDB.id == customer_id).first()
            if customer_db:
                db.delete(customer_db)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def create_opportunity(self, opportunity: Opportunity) -> Opportunity:
        db = self.get_db()
        try:
            opportunity_db = OpportunityDB(
                customer_id=opportunity.customer_id,
                title=opportunity.title,
                description=opportunity.description,
                value=opportunity.value,
                stage=opportunity.stage,
                probability=opportunity.probability,
                expected_close_date=opportunity.expected_close_date
            )
            db.add(opportunity_db)
            db.commit()
            db.refresh(opportunity_db)
            return self._convert_opportunity_to_pydantic(opportunity_db)
        finally:
            db.close()
    
    def get_opportunity(self, opportunity_id: int) -> Optional[Opportunity]:
        db = self.get_db()
        try:
            opportunity_db = db.query(OpportunityDB).filter(OpportunityDB.id == opportunity_id).first()
            if opportunity_db:
                return self._convert_opportunity_to_pydantic(opportunity_db)
            return None
        finally:
            db.close()
    
    def get_all_opportunities(self) -> List[Opportunity]:
        db = self.get_db()
        try:
            opportunities_db = db.query(OpportunityDB).all()
            return [self._convert_opportunity_to_pydantic(opportunity_db) for opportunity_db in opportunities_db]
        finally:
            db.close()
    
    def get_opportunities_by_customer(self, customer_id: int) -> List[Opportunity]:
        db = self.get_db()
        try:
            opportunities_db = db.query(OpportunityDB).filter(OpportunityDB.customer_id == customer_id).all()
            return [self._convert_opportunity_to_pydantic(opportunity_db) for opportunity_db in opportunities_db]
        finally:
            db.close()
    
    def update_opportunity(self, opportunity_id: int, opportunity_data: dict) -> Optional[Opportunity]:
        db = self.get_db()
        try:
            opportunity_db = db.query(OpportunityDB).filter(OpportunityDB.id == opportunity_id).first()
            if opportunity_db:
                for key, value in opportunity_data.items():
                    if hasattr(opportunity_db, key):
                        setattr(opportunity_db, key, value)
                opportunity_db.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(opportunity_db)
                return self._convert_opportunity_to_pydantic(opportunity_db)
            return None
        finally:
            db.close()
    
    def delete_opportunity(self, opportunity_id: int) -> bool:
        db = self.get_db()
        try:
            opportunity_db = db.query(OpportunityDB).filter(OpportunityDB.id == opportunity_id).first()
            if opportunity_db:
                db.delete(opportunity_db)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def create_campaign(self, campaign: Campaign) -> Campaign:
        db = self.get_db()
        try:
            campaign_db = CampaignDB(
                name=campaign.name,
                description=campaign.description,
                status=campaign.status,
                budget=campaign.budget,
                start_date=campaign.start_date,
                end_date=campaign.end_date
            )
            db.add(campaign_db)
            db.commit()
            db.refresh(campaign_db)
            return self._convert_campaign_to_pydantic(campaign_db)
        finally:
            db.close()
    
    def get_campaign(self, campaign_id: int) -> Optional[Campaign]:
        db = self.get_db()
        try:
            campaign_db = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
            if campaign_db:
                return self._convert_campaign_to_pydantic(campaign_db)
            return None
        finally:
            db.close()
    
    def get_all_campaigns(self) -> List[Campaign]:
        db = self.get_db()
        try:
            campaigns_db = db.query(CampaignDB).all()
            return [self._convert_campaign_to_pydantic(campaign_db) for campaign_db in campaigns_db]
        finally:
            db.close()
    
    def update_campaign(self, campaign_id: int, campaign_data: dict) -> Optional[Campaign]:
        db = self.get_db()
        try:
            campaign_db = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
            if campaign_db:
                for key, value in campaign_data.items():
                    if hasattr(campaign_db, key):
                        setattr(campaign_db, key, value)
                campaign_db.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(campaign_db)
                return self._convert_campaign_to_pydantic(campaign_db)
            return None
        finally:
            db.close()
    
    def delete_campaign(self, campaign_id: int) -> bool:
        db = self.get_db()
        try:
            campaign_db = db.query(CampaignDB).filter(CampaignDB.id == campaign_id).first()
            if campaign_db:
                db.delete(campaign_db)
                db.commit()
                return True
            return False
        finally:
            db.close()
    
    def create_activity(self, activity: Activity) -> Activity:
        db = self.get_db()
        try:
            activity_db = ActivityDB(
                customer_id=activity.customer_id,
                opportunity_id=activity.opportunity_id,
                type=activity.type,
                subject=activity.subject,
                description=activity.description
            )
            db.add(activity_db)
            db.commit()
            db.refresh(activity_db)
            return self._convert_activity_to_pydantic(activity_db)
        finally:
            db.close()
    
    def get_activities_by_customer(self, customer_id: int) -> List[Activity]:
        db = self.get_db()
        try:
            activities_db = db.query(ActivityDB).filter(ActivityDB.customer_id == customer_id).all()
            return [self._convert_activity_to_pydantic(activity_db) for activity_db in activities_db]
        finally:
            db.close()
    
    def get_all_activities(self) -> List[Activity]:
        db = self.get_db()
        try:
            activities_db = db.query(ActivityDB).all()
            return [self._convert_activity_to_pydantic(activity_db) for activity_db in activities_db]
        finally:
            db.close()

sql_db = SQLDatabase()
