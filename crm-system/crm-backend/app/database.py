from datetime import datetime
from typing import Dict, List, Optional
from .models import Customer, Opportunity, Campaign, Activity

class InMemoryDatabase:
    def __init__(self):
        self.customers: Dict[int, Customer] = {}
        self.opportunities: Dict[int, Opportunity] = {}
        self.campaigns: Dict[int, Campaign] = {}
        self.activities: Dict[int, Activity] = {}
        self.next_customer_id = 1
        self.next_opportunity_id = 1
        self.next_campaign_id = 1
        self.next_activity_id = 1
    
    def create_customer(self, customer: Customer) -> Customer:
        customer.id = self.next_customer_id
        customer.created_at = datetime.now()
        customer.updated_at = datetime.now()
        self.customers[self.next_customer_id] = customer
        self.next_customer_id += 1
        return customer
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self.customers.get(customer_id)
    
    def get_all_customers(self) -> List[Customer]:
        return list(self.customers.values())
    
    def update_customer(self, customer_id: int, customer_data: dict) -> Optional[Customer]:
        if customer_id in self.customers:
            customer = self.customers[customer_id]
            for key, value in customer_data.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
            customer.updated_at = datetime.now()
            return customer
        return None
    
    def delete_customer(self, customer_id: int) -> bool:
        if customer_id in self.customers:
            del self.customers[customer_id]
            return True
        return False
    
    def create_opportunity(self, opportunity: Opportunity) -> Opportunity:
        opportunity.id = self.next_opportunity_id
        opportunity.created_at = datetime.now()
        opportunity.updated_at = datetime.now()
        self.opportunities[self.next_opportunity_id] = opportunity
        self.next_opportunity_id += 1
        return opportunity
    
    def get_opportunity(self, opportunity_id: int) -> Optional[Opportunity]:
        return self.opportunities.get(opportunity_id)
    
    def get_all_opportunities(self) -> List[Opportunity]:
        return list(self.opportunities.values())
    
    def get_opportunities_by_customer(self, customer_id: int) -> List[Opportunity]:
        return [opp for opp in self.opportunities.values() if opp.customer_id == customer_id]
    
    def update_opportunity(self, opportunity_id: int, opportunity_data: dict) -> Optional[Opportunity]:
        if opportunity_id in self.opportunities:
            opportunity = self.opportunities[opportunity_id]
            for key, value in opportunity_data.items():
                if hasattr(opportunity, key):
                    setattr(opportunity, key, value)
            opportunity.updated_at = datetime.now()
            return opportunity
        return None
    
    def delete_opportunity(self, opportunity_id: int) -> bool:
        if opportunity_id in self.opportunities:
            del self.opportunities[opportunity_id]
            return True
        return False
    
    def create_campaign(self, campaign: Campaign) -> Campaign:
        campaign.id = self.next_campaign_id
        campaign.created_at = datetime.now()
        campaign.updated_at = datetime.now()
        self.campaigns[self.next_campaign_id] = campaign
        self.next_campaign_id += 1
        return campaign
    
    def get_campaign(self, campaign_id: int) -> Optional[Campaign]:
        return self.campaigns.get(campaign_id)
    
    def get_all_campaigns(self) -> List[Campaign]:
        return list(self.campaigns.values())
    
    def update_campaign(self, campaign_id: int, campaign_data: dict) -> Optional[Campaign]:
        if campaign_id in self.campaigns:
            campaign = self.campaigns[campaign_id]
            for key, value in campaign_data.items():
                if hasattr(campaign, key):
                    setattr(campaign, key, value)
            campaign.updated_at = datetime.now()
            return campaign
        return None
    
    def delete_campaign(self, campaign_id: int) -> bool:
        if campaign_id in self.campaigns:
            del self.campaigns[campaign_id]
            return True
        return False
    
    def create_activity(self, activity: Activity) -> Activity:
        activity.id = self.next_activity_id
        activity.created_at = datetime.now()
        self.activities[self.next_activity_id] = activity
        self.next_activity_id += 1
        return activity
    
    def get_activities_by_customer(self, customer_id: int) -> List[Activity]:
        return [act for act in self.activities.values() if act.customer_id == customer_id]
    
    def get_all_activities(self) -> List[Activity]:
        return list(self.activities.values())

db = InMemoryDatabase()
