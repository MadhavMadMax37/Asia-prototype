from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from typing import List

from database import get_db
import models
import schemas
from auth_utils import get_current_active_user

router = APIRouter()

@router.get("/stats", response_model=schemas.DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get dashboard statistics"""
    
    # Base query - filter by user role
    base_query = db.query(models.Lead)
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        base_query = base_query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    # Total leads
    total_leads = base_query.count()
    
    # Leads by status
    new_leads = base_query.filter(models.Lead.status == models.LeadStatus.NEW).count()
    qualified_leads = base_query.filter(models.Lead.status == models.LeadStatus.QUALIFIED).count()
    closed_won = base_query.filter(models.Lead.status == models.LeadStatus.CLOSED_WON).count()
    closed_lost = base_query.filter(models.Lead.status == models.LeadStatus.CLOSED_LOST).count()
    
    # Conversion rate
    total_closed = closed_won + closed_lost
    conversion_rate = (closed_won / total_closed * 100) if total_closed > 0 else 0
    
    # Total estimated value
    estimated_value_result = base_query.with_entities(
        func.sum(models.Lead.estimated_value)
    ).scalar()
    total_estimated_value = estimated_value_result or 0
    
    # Time-based metrics
    week_ago = datetime.utcnow() - timedelta(days=7)
    month_ago = datetime.utcnow() - timedelta(days=30)
    
    leads_this_week = base_query.filter(models.Lead.created_at >= week_ago).count()
    leads_this_month = base_query.filter(models.Lead.created_at >= month_ago).count()
    
    return schemas.DashboardStats(
        total_leads=total_leads,
        new_leads=new_leads,
        qualified_leads=qualified_leads,
        closed_won=closed_won,
        closed_lost=closed_lost,
        conversion_rate=round(conversion_rate, 2),
        total_estimated_value=total_estimated_value,
        leads_this_week=leads_this_week,
        leads_this_month=leads_this_month
    )

@router.get("/leads-by-status", response_model=List[schemas.LeadsByStatus])
async def get_leads_by_status(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get lead distribution by status"""
    
    base_query = db.query(models.Lead)
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        base_query = base_query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    total_leads = base_query.count()
    
    results = []
    for status in models.LeadStatus:
        count = base_query.filter(models.Lead.status == status).count()
        percentage = (count / total_leads * 100) if total_leads > 0 else 0
        
        results.append(schemas.LeadsByStatus(
            status=status.value,
            count=count,
            percentage=round(percentage, 2)
        ))
    
    return results

@router.get("/leads-by-source", response_model=List[schemas.LeadsBySource])
async def get_leads_by_source(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get lead distribution by source"""
    
    base_query = db.query(models.Lead)
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        base_query = base_query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    total_leads = base_query.count()
    
    results = []
    for source in models.LeadSource:
        count = base_query.filter(models.Lead.source == source).count()
        percentage = (count / total_leads * 100) if total_leads > 0 else 0
        
        results.append(schemas.LeadsBySource(
            source=source.value,
            count=count,
            percentage=round(percentage, 2)
        ))
    
    return results

@router.get("/activity-summary", response_model=List[schemas.ActivitySummary])
async def get_activity_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get activity summary statistics"""
    
    # Base query for activities
    base_query = db.query(models.Activity)
    
    # Filter by user role
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        # Join with leads to filter by assigned agent
        base_query = base_query.join(models.Lead).filter(
            models.Lead.assigned_agent_id == current_user.id
        )
    
    # Last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    results = []
    for activity_type in models.ActivityType:
        # Total count for this activity type
        total_count = base_query.filter(models.Activity.activity_type == activity_type).count()
        
        # Count in last 7 days
        last_7_days_count = base_query.filter(
            and_(
                models.Activity.activity_type == activity_type,
                models.Activity.created_at >= week_ago
            )
        ).count()
        
        results.append(schemas.ActivitySummary(
            activity_type=activity_type.value,
            count=total_count,
            last_7_days=last_7_days_count
        ))
    
    return results

@router.get("/recent-activities", response_model=List[schemas.Activity])
async def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get recent activities"""
    
    query = db.query(models.Activity).join(models.Lead)
    
    # Filter by user role
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        query = query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    activities = query.order_by(
        models.Activity.created_at.desc()
    ).limit(limit).all()
    
    return activities

@router.get("/top-leads", response_model=List[schemas.Lead])
async def get_top_leads(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get top leads by estimated value"""
    
    query = db.query(models.Lead).filter(
        models.Lead.estimated_value.isnot(None)
    )
    
    # Filter by user role
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        query = query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    leads = query.order_by(
        models.Lead.estimated_value.desc()
    ).limit(limit).all()
    
    return leads