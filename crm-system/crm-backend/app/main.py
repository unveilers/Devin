from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

from .models import Customer, Opportunity, Campaign, Activity, SalesMetrics, OpportunityStage, CustomerStatus
from .sql_database import sql_db as db

app = FastAPI(title="CRM System API", version="1.0.0")

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {
        "message": "CRM System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/healthz"
    }

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/api/customers", response_model=Customer)
async def create_customer(customer: Customer):
    return db.create_customer(customer)

@app.get("/api/customers", response_model=List[Customer])
async def get_customers():
    return db.get_all_customers()

@app.get("/api/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    customer = db.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/api/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_data: dict):
    customer = db.update_customer(customer_id, customer_data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.delete("/api/customers/{customer_id}")
async def delete_customer(customer_id: int):
    if not db.delete_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@app.post("/api/opportunities", response_model=Opportunity)
async def create_opportunity(opportunity: Opportunity):
    if not db.get_customer(opportunity.customer_id):
        raise HTTPException(status_code=400, detail="Customer not found")
    return db.create_opportunity(opportunity)

@app.get("/api/opportunities", response_model=List[Opportunity])
async def get_opportunities():
    return db.get_all_opportunities()

@app.get("/api/opportunities/{opportunity_id}", response_model=Opportunity)
async def get_opportunity(opportunity_id: int):
    opportunity = db.get_opportunity(opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity

@app.get("/api/customers/{customer_id}/opportunities", response_model=List[Opportunity])
async def get_customer_opportunities(customer_id: int):
    if not db.get_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return db.get_opportunities_by_customer(customer_id)

@app.put("/api/opportunities/{opportunity_id}", response_model=Opportunity)
async def update_opportunity(opportunity_id: int, opportunity_data: dict):
    opportunity = db.update_opportunity(opportunity_id, opportunity_data)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity

@app.delete("/api/opportunities/{opportunity_id}")
async def delete_opportunity(opportunity_id: int):
    if not db.delete_opportunity(opportunity_id):
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return {"message": "Opportunity deleted successfully"}

@app.post("/api/campaigns", response_model=Campaign)
async def create_campaign(campaign: Campaign):
    return db.create_campaign(campaign)

@app.get("/api/campaigns", response_model=List[Campaign])
async def get_campaigns():
    return db.get_all_campaigns()

@app.get("/api/campaigns/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: int):
    campaign = db.get_campaign(campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.put("/api/campaigns/{campaign_id}", response_model=Campaign)
async def update_campaign(campaign_id: int, campaign_data: dict):
    campaign = db.update_campaign(campaign_id, campaign_data)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.delete("/api/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int):
    if not db.delete_campaign(campaign_id):
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": "Campaign deleted successfully"}

@app.post("/api/activities", response_model=Activity)
async def create_activity(activity: Activity):
    if not db.get_customer(activity.customer_id):
        raise HTTPException(status_code=400, detail="Customer not found")
    return db.create_activity(activity)

@app.get("/api/customers/{customer_id}/activities", response_model=List[Activity])
async def get_customer_activities(customer_id: int):
    if not db.get_customer(customer_id):
        raise HTTPException(status_code=404, detail="Customer not found")
    return db.get_activities_by_customer(customer_id)

@app.get("/api/activities", response_model=List[Activity])
async def get_all_activities():
    return db.get_all_activities()

@app.get("/api/analytics/sales-metrics", response_model=SalesMetrics)
async def get_sales_metrics():
    customers = db.get_all_customers()
    opportunities = db.get_all_opportunities()
    
    total_customers = len(customers)
    active_customers = len([c for c in customers if c.status == CustomerStatus.ACTIVE])
    total_opportunities = len(opportunities)
    
    total_pipeline_value = sum(opp.value for opp in opportunities if opp.stage != OpportunityStage.CLOSED_LOST)
    won_opportunities = [opp for opp in opportunities if opp.stage == OpportunityStage.CLOSED_WON]
    won_value = sum(opp.value for opp in won_opportunities)
    
    conversion_rate = (len(won_opportunities) / total_opportunities * 100) if total_opportunities > 0 else 0
    avg_deal_size = won_value / len(won_opportunities) if len(won_opportunities) > 0 else 0
    
    return SalesMetrics(
        total_customers=total_customers,
        active_customers=active_customers,
        total_opportunities=total_opportunities,
        total_pipeline_value=total_pipeline_value,
        won_opportunities=len(won_opportunities),
        won_value=won_value,
        conversion_rate=round(conversion_rate, 2),
        avg_deal_size=round(avg_deal_size, 2)
    )

@app.get("/api/analytics/pipeline-by-stage")
async def get_pipeline_by_stage():
    opportunities = db.get_all_opportunities()
    pipeline_data = {}
    
    for stage in OpportunityStage:
        stage_opps = [opp for opp in opportunities if opp.stage == stage]
        pipeline_data[stage.value] = {
            "count": len(stage_opps),
            "value": sum(opp.value for opp in stage_opps)
        }
    
    return pipeline_data
