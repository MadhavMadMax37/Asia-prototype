from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from database import get_db
import models
import schemas
from auth_utils import get_current_active_user, require_role
from email_utils import send_new_lead_notification

router = APIRouter()

# Create lead (public endpoint for form submissions)
@router.post("/", response_model=schemas.Lead, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead: schemas.LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new lead from the quote form submission"""
    
    # Check if lead with same email already exists
    existing_lead = db.query(models.Lead).filter(models.Lead.email == lead.email).first()
    if existing_lead:
        # Update existing lead with new information
        for field, value in lead.dict(exclude_unset=True).items():
            setattr(existing_lead, field, value)
        existing_lead.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_lead)
        
        # Log activity for updated lead
        activity = models.Activity(
            lead_id=existing_lead.id,
            user_id=1,  # System user - should be configurable
            activity_type=models.ActivityType.NOTE,
            title="Lead Updated",
            description=f"Lead information updated via website form"
        )
        db.add(activity)
        db.commit()
        
        return existing_lead
    
    # Create new lead
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # Create initial activity
    activity = models.Activity(
        lead_id=db_lead.id,
        user_id=1,  # System user
        activity_type=models.ActivityType.NOTE,
        title="Lead Created",
        description=f"New lead created via website form. Interested in: {', '.join([k for k, v in {'Personal Lines': lead.personal_lines, 'Commercial Lines': lead.commercial_lines, 'Life & Health': lead.life_and_health}.items() if v])}"
    )
    db.add(activity)
    db.commit()
    
    # Send email notification in background
    background_tasks.add_task(send_new_lead_notification, db_lead.email, db_lead.first_name, db_lead.last_name)
    
    return db_lead

# Get all leads with filtering and pagination
@router.get("/", response_model=schemas.LeadListResponse)
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[models.LeadStatus] = None,
    source: Optional[models.LeadSource] = None,
    assigned_agent_id: Optional[int] = None,
    priority: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get leads with filtering and pagination"""
    
    query = db.query(models.Lead).options(joinedload(models.Lead.assigned_agent))
    
    # Apply filters
    if status:
        query = query.filter(models.Lead.status == status)
    if source:
        query = query.filter(models.Lead.source == source)
    if assigned_agent_id:
        query = query.filter(models.Lead.assigned_agent_id == assigned_agent_id)
    if priority:
        query = query.filter(models.Lead.priority == priority)
    
    # Search functionality
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Lead.first_name.ilike(search_pattern),
                models.Lead.last_name.ilike(search_pattern),
                models.Lead.email.ilike(search_pattern),
                models.Lead.phone_number.ilike(search_pattern),
                models.Lead.city.ilike(search_pattern)
            )
        )
    
    # If user is not admin, only show their assigned leads
    if current_user.role != models.UserRole.ADMIN:
        query = query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    leads = query.order_by(models.Lead.created_at.desc()).offset(skip).limit(limit).all()
    
    return schemas.LeadListResponse(
        leads=leads,
        total=total,
        page=(skip // limit) + 1,
        per_page=limit,
        total_pages=(total + limit - 1) // limit
    )

# Get single lead with full details
@router.get("/{lead_id}", response_model=schemas.LeadWithActivities)
async def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get a specific lead with all activities and quotes"""
    
    query = db.query(models.Lead).options(
        joinedload(models.Lead.assigned_agent),
        joinedload(models.Lead.activities).joinedload(models.Activity.user),
        joinedload(models.Lead.quotes)
    )
    
    lead = query.filter(models.Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER] and lead.assigned_agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this lead")
    
    return lead

# Update lead
@router.put("/{lead_id}", response_model=schemas.Lead)
async def update_lead(
    lead_id: int,
    lead_update: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update a lead"""
    
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER] and lead.assigned_agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this lead")
    
    # Track status changes
    old_status = lead.status
    
    # Update lead fields
    update_data = lead_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lead, field, value)
    
    lead.updated_at = datetime.utcnow()
    
    # Update last contact date if status changed
    if "status" in update_data and old_status != lead.status:
        lead.last_contact_date = datetime.utcnow()
        
        # Log status change activity
        activity = models.Activity(
            lead_id=lead.id,
            user_id=current_user.id,
            activity_type=models.ActivityType.STATUS_CHANGE,
            title="Status Changed",
            description=f"Status changed from {old_status.value} to {lead.status.value}"
        )
        db.add(activity)
    
    db.commit()
    db.refresh(lead)
    
    return lead

# Delete lead
@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(models.UserRole.ADMIN))
):
    """Delete a lead (admin only)"""
    
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(lead)
    db.commit()
    
    return {"message": "Lead deleted successfully"}

# Assign lead to agent
@router.post("/{lead_id}/assign/{agent_id}")
async def assign_lead(
    lead_id: int,
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(models.UserRole.MANAGER))
):
    """Assign a lead to an agent (manager+ only)"""
    
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    agent = db.query(models.User).filter(models.User.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    old_agent_id = lead.assigned_agent_id
    lead.assigned_agent_id = agent_id
    lead.updated_at = datetime.utcnow()
    
    # Log assignment activity
    activity = models.Activity(
        lead_id=lead.id,
        user_id=current_user.id,
        activity_type=models.ActivityType.NOTE,
        title="Lead Assigned",
        description=f"Lead assigned to {agent.full_name}"
    )
    db.add(activity)
    
    db.commit()
    
    return {"message": f"Lead assigned to {agent.full_name}"}

# Add activity to lead
@router.post("/{lead_id}/activities", response_model=schemas.Activity)
async def add_activity(
    lead_id: int,
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add an activity to a lead"""
    
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER] and lead.assigned_agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add activities to this lead")
    
    # Create activity
    db_activity = models.Activity(
        **activity.dict(),
        user_id=current_user.id
    )
    db.add(db_activity)
    
    # Update lead's last contact date
    lead.last_contact_date = datetime.utcnow()
    
    db.commit()
    db.refresh(db_activity)
    
    return db_activity

# Get lead activities
@router.get("/{lead_id}/activities", response_model=List[schemas.Activity])
async def get_lead_activities(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all activities for a lead"""
    
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER] and lead.assigned_agent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view activities for this lead")
    
    activities = db.query(models.Activity).options(
        joinedload(models.Activity.user)
    ).filter(
        models.Activity.lead_id == lead_id
    ).order_by(models.Activity.created_at.desc()).all()
    
    return activities

# Get leads requiring follow-up
@router.get("/followup/pending", response_model=List[schemas.Lead])
async def get_pending_followups(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get leads that require follow-up"""
    
    today = datetime.utcnow().date()
    
    query = db.query(models.Lead).options(joinedload(models.Lead.assigned_agent)).filter(
        and_(
            models.Lead.next_follow_up_date <= today,
            models.Lead.status.in_([
                models.LeadStatus.NEW,
                models.LeadStatus.CONTACTED,
                models.LeadStatus.QUALIFIED,
                models.LeadStatus.FOLLOW_UP
            ])
        )
    )
    
    # If not admin/manager, only show assigned leads
    if current_user.role not in [models.UserRole.ADMIN, models.UserRole.MANAGER]:
        query = query.filter(models.Lead.assigned_agent_id == current_user.id)
    
    leads = query.order_by(models.Lead.next_follow_up_date.asc()).all()
    
    return leads