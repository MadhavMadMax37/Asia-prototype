from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from database import get_db
import models
import schemas
from auth_utils import get_current_active_user, require_role

router = APIRouter()

@router.get("/conversion-funnel")
async def get_conversion_funnel(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get conversion funnel data"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    base_query = db.query(models.Lead).filter(models.Lead.created_at >= start_date)
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        base_query = base_query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    # Define funnel stages
    stages = {
        "New Leads": [models.LeadStatus.NEW],
        "Contacted": [models.LeadStatus.CONTACTED, models.LeadStatus.QUALIFIED, models.LeadStatus.PROPOSAL_SENT, models.LeadStatus.CLOSED_WON, models.LeadStatus.CLOSED_LOST],
        "Qualified": [models.LeadStatus.QUALIFIED, models.LeadStatus.PROPOSAL_SENT, models.LeadStatus.CLOSED_WON, models.LeadStatus.CLOSED_LOST],
        "Proposal Sent": [models.LeadStatus.PROPOSAL_SENT, models.LeadStatus.CLOSED_WON, models.LeadStatus.CLOSED_LOST],
        "Closed Won": [models.LeadStatus.CLOSED_WON]
    }
    
    funnel_data = []
    previous_count = None
    
    for stage_name, statuses in stages.items():
        count = base_query.filter(models.Lead.status.in_(statuses)).count()
        
        conversion_rate = None
        if previous_count is not None and previous_count > 0:
            conversion_rate = round((count / previous_count) * 100, 2)
        
        funnel_data.append({
            "stage": stage_name,
            "count": count,
            "conversion_rate": conversion_rate
        })
        
        previous_count = count
    
    return {"funnel": funnel_data, "period_days": days}

@router.get("/leads-by-month")
async def get_leads_by_month(
    months: int = Query(12, description="Number of months to analyze"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get leads created by month"""
    
    base_query = db.query(models.Lead)
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        base_query = base_query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    # Get monthly data
    monthly_data = base_query.filter(
        models.Lead.created_at >= datetime.utcnow() - timedelta(days=months * 30)
    ).with_entities(
        extract('year', models.Lead.created_at).label('year'),
        extract('month', models.Lead.created_at).label('month'),
        func.count().label('count')
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    results = []
    for row in monthly_data:
        month_name = datetime(int(row.year), int(row.month), 1).strftime('%B %Y')
        results.append({
            "month": month_name,
            "year": int(row.year),
            "month_number": int(row.month),
            "count": row.count
        })
    
    return {"monthly_data": results}

@router.get("/agent-performance")
async def get_agent_performance(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(models.UserRole.MANAGER))
):
    """Get agent performance metrics (manager+ only)"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get all agents
    agents = db.query(models.User).filter(
        models.User.role.in_([models.UserRole.AGENT, models.UserRole.MANAGER])
    ).all()
    
    performance_data = []
    
    for agent in agents:
        # Get agent's leads
        agent_leads = db.query(models.Lead).filter(
            and_(
                models.Lead.assigned_agent_id == agent.id,
                models.Lead.created_at >= start_date
            )
        )
        
        total_leads = agent_leads.count()
        qualified_leads = agent_leads.filter(models.Lead.status == models.LeadStatus.QUALIFIED).count()
        closed_won = agent_leads.filter(models.Lead.status == models.LeadStatus.CLOSED_WON).count()
        closed_lost = agent_leads.filter(models.Lead.status == models.LeadStatus.CLOSED_LOST).count()
        
        # Calculate metrics
        qualification_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
        close_rate = (closed_won / (closed_won + closed_lost) * 100) if (closed_won + closed_lost) > 0 else 0
        
        # Get total estimated value
        estimated_value = agent_leads.with_entities(
            func.sum(models.Lead.estimated_value)
        ).scalar() or 0
        
        # Get activity count
        activity_count = db.query(models.Activity).join(models.Lead).filter(
            and_(
                models.Lead.assigned_agent_id == agent.id,
                models.Activity.created_at >= start_date
            )
        ).count()
        
        performance_data.append({
            "agent_name": agent.full_name,
            "agent_id": agent.id,
            "total_leads": total_leads,
            "qualified_leads": qualified_leads,
            "closed_won": closed_won,
            "closed_lost": closed_lost,
            "qualification_rate": round(qualification_rate, 2),
            "close_rate": round(close_rate, 2),
            "estimated_value": estimated_value,
            "activity_count": activity_count
        })
    
    # Sort by total leads descending
    performance_data.sort(key=lambda x: x['total_leads'], reverse=True)
    
    return {"performance_data": performance_data, "period_days": days}

@router.get("/lead-sources-analysis")
async def get_lead_sources_analysis(
    days: int = Query(90, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Analyze lead sources performance"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    base_query = db.query(models.Lead).filter(models.Lead.created_at >= start_date)
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        base_query = base_query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    source_analysis = []
    
    for source in models.LeadSource:
        source_leads = base_query.filter(models.Lead.source == source)
        
        total_count = source_leads.count()
        qualified_count = source_leads.filter(models.Lead.status == models.LeadStatus.QUALIFIED).count()
        closed_won_count = source_leads.filter(models.Lead.status == models.LeadStatus.CLOSED_WON).count()
        closed_lost_count = source_leads.filter(models.Lead.status == models.LeadStatus.CLOSED_LOST).count()
        
        # Calculate rates
        qualification_rate = (qualified_count / total_count * 100) if total_count > 0 else 0
        close_rate = (closed_won_count / (closed_won_count + closed_lost_count) * 100) if (closed_won_count + closed_lost_count) > 0 else 0
        
        # Average estimated value
        avg_value = source_leads.with_entities(
            func.avg(models.Lead.estimated_value)
        ).scalar() or 0
        
        source_analysis.append({
            "source": source.value,
            "total_leads": total_count,
            "qualified_leads": qualified_count,
            "closed_won": closed_won_count,
            "closed_lost": closed_lost_count,
            "qualification_rate": round(qualification_rate, 2),
            "close_rate": round(close_rate, 2),
            "average_estimated_value": round(avg_value, 2)
        })
    
    # Sort by total leads descending
    source_analysis.sort(key=lambda x: x['total_leads'], reverse=True)
    
    return {"source_analysis": source_analysis, "period_days": days}

@router.get("/activity-timeline")
async def get_activity_timeline(
    lead_id: Optional[int] = Query(None, description="Specific lead ID"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get activity timeline"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(models.Activity).filter(models.Activity.created_at >= start_date)
    
    # Filter by specific lead if provided
    if lead_id:
        query = query.filter(models.Activity.lead_id == lead_id)
    
    # Filter by user role
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        query = query.join(models.Lead).filter(models.Lead.assigned_agent_id == current_user.id)
    
    # Group by date and activity type
    daily_activities = query.with_entities(
        func.date(models.Activity.created_at).label('date'),
        models.Activity.activity_type,
        func.count().label('count')
    ).group_by(
        func.date(models.Activity.created_at),
        models.Activity.activity_type
    ).order_by('date').all()
    
    # Format the data
    timeline_data = {}
    for row in daily_activities:
        date_str = row.date.strftime('%Y-%m-%d')
        if date_str not in timeline_data:
            timeline_data[date_str] = {}
        
        timeline_data[date_str][row.activity_type.value] = row.count
    
    return {"timeline_data": timeline_data, "period_days": days}

@router.get("/revenue-forecast")
async def get_revenue_forecast(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get revenue forecast based on pipeline"""
    
    base_query = db.query(models.Lead).filter(
        models.Lead.estimated_value.isnot(None),
        models.Lead.status.in_([
            models.LeadStatus.NEW,
            models.LeadStatus.CONTACTED,
            models.LeadStatus.QUALIFIED,
            models.LeadStatus.PROPOSAL_SENT
        ])
    )
    
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        base_query = base_query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    # Define probability multipliers for each status
    status_probabilities = {
        models.LeadStatus.NEW: 0.1,
        models.LeadStatus.CONTACTED: 0.2,
        models.LeadStatus.QUALIFIED: 0.5,
        models.LeadStatus.PROPOSAL_SENT: 0.8
    }
    
    forecast_data = []
    total_weighted_value = 0
    
    for status, probability in status_probabilities.items():
        leads = base_query.filter(models.Lead.status == status).all()
        
        status_value = sum(lead.estimated_value for lead in leads)
        weighted_value = status_value * probability
        total_weighted_value += weighted_value
        
        forecast_data.append({
            "status": status.value,
            "lead_count": len(leads),
            "total_value": status_value,
            "probability": probability,
            "weighted_value": round(weighted_value, 2)
        })
    
    return {
        "forecast_data": forecast_data,
        "total_pipeline_value": sum(f["total_value"] for f in forecast_data),
        "weighted_forecast": round(total_weighted_value, 2)
    }