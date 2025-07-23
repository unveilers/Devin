from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
async def root():
    customers = db.get_all_customers()
    opportunities = db.get_all_opportunities()
    campaigns = db.get_all_campaigns()
    activities = db.get_all_activities()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CRM System Database</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ color: #333; text-align: center; }}
            h2 {{ color: #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f8f9fa; font-weight: bold; }}
            tr:hover {{ background-color: #f5f5f5; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
            .nav {{ background: #007bff; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
            .nav a {{ color: white; text-decoration: none; margin: 0 15px; font-weight: bold; }}
            .nav a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 CRM System Database</h1>
            
            <div class="nav">
                <a href="/">Database View</a>
                <a href="/docs">API Documentation</a>
                <a href="/healthz">Health Check</a>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{len(customers)}</div>
                    <div>Total Customers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(opportunities)}</div>
                    <div>Total Opportunities</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(campaigns)}</div>
                    <div>Total Campaigns</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(activities)}</div>
                    <div>Total Activities</div>
                </div>
            </div>
            
            <h2>👥 Customers</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Company</th>
                    <th>Status</th>
                    <th>Created</th>
                </tr>"""
    
    for customer in customers:
        html_content += f"""
                <tr>
                    <td>{customer.id}</td>
                    <td>{customer.first_name} {customer.last_name}</td>
                    <td>{customer.email}</td>
                    <td>{customer.phone or 'N/A'}</td>
                    <td>{customer.company or 'N/A'}</td>
                    <td>{customer.status}</td>
                    <td>{customer.created_at.strftime('%Y-%m-%d %H:%M') if customer.created_at else 'N/A'}</td>
                </tr>"""
    
    html_content += """
            </table>
            
            <h2>💼 Opportunities</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Customer ID</th>
                    <th>Value</th>
                    <th>Stage</th>
                    <th>Probability</th>
                    <th>Expected Close</th>
                    <th>Created</th>
                </tr>"""
    
    for opportunity in opportunities:
        html_content += f"""
                <tr>
                    <td>{opportunity.id}</td>
                    <td>{opportunity.title}</td>
                    <td>{opportunity.customer_id}</td>
                    <td>${opportunity.value:,.2f}</td>
                    <td>{opportunity.stage}</td>
                    <td>{opportunity.probability}%</td>
                    <td>{opportunity.expected_close_date.strftime('%Y-%m-%d') if opportunity.expected_close_date else 'N/A'}</td>
                    <td>{opportunity.created_at.strftime('%Y-%m-%d %H:%M') if opportunity.created_at else 'N/A'}</td>
                </tr>"""
    
    html_content += """
            </table>
            
            <h2>📢 Campaigns</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Budget</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Created</th>
                </tr>"""
    
    for campaign in campaigns:
        budget_display = f"${campaign.budget:,.2f}" if campaign.budget is not None else "$0.00"
        html_content += f"""
                <tr>
                    <td>{campaign.id}</td>
                    <td>{campaign.name}</td>
                    <td>{campaign.status}</td>
                    <td>{budget_display}</td>
                    <td>{campaign.start_date.strftime('%Y-%m-%d') if campaign.start_date else 'N/A'}</td>
                    <td>{campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else 'N/A'}</td>
                    <td>{campaign.created_at.strftime('%Y-%m-%d %H:%M') if campaign.created_at else 'N/A'}</td>
                </tr>"""
    
    html_content += """
            </table>
            
            <h2>📝 Activities</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Subject</th>
                    <th>Customer ID</th>
                    <th>Opportunity ID</th>
                    <th>Description</th>
                    <th>Created</th>
                </tr>"""
    
    for activity in activities:
        html_content += f"""
                <tr>
                    <td>{activity.id}</td>
                    <td>{activity.type}</td>
                    <td>{activity.subject}</td>
                    <td>{activity.customer_id}</td>
                    <td>{activity.opportunity_id or 'N/A'}</td>
                    <td>{activity.description or 'N/A'}</td>
                    <td>{activity.created_at.strftime('%Y-%m-%d %H:%M') if activity.created_at else 'N/A'}</td>
                </tr>"""
    
    html_content += """
            </table>
            
            <div style="margin-top: 40px; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3>🔗 API Endpoints</h3>
                <p><strong>API Documentation:</strong> <a href="/docs">/docs</a></p>
                <p><strong>Health Check:</strong> <a href="/healthz">/healthz</a></p>
                <p><strong>Frontend Application:</strong> <a href="https://crm-management-app-b3zmfkb9.devinapps.com/" target="_blank">CRM Frontend</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

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
