from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
import uuid

from database import get_collection, Collections
import models
import schemas
from auth_utils import get_current_active_user, require_role
from email_utils import send_new_lead_notification

router = APIRouter()

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format and map field names"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        result = {}
        # Field name mapping from snake_case to camelCase
        field_mapping = {
            'first_name': 'firstName',
            'last_name': 'lastName', 
            'phone_number': 'phoneNumber',
            'address_line1': 'addressLine1',
            'address_line2': 'addressLine2',
            'zip_code': 'zipCode',
            'personal_lines': 'personalLines',
            'commercial_lines': 'commercialLines',
            'life_and_health': 'lifeAndHealth'
        }
        
        for key, value in doc.items():
            # Use mapped field name if available, otherwise use original
            output_key = field_mapping.get(key, key)
            
            if isinstance(value, ObjectId):
                result[output_key] = str(value)
            elif isinstance(value, datetime):
                result[output_key] = value.isoformat()
            elif isinstance(value, dict):
                result[output_key] = serialize_doc(value)
            elif isinstance(value, list):
                result[output_key] = serialize_doc(value)
            else:
                result[output_key] = value
        return result
    return doc

# Create lead (public endpoint for form submissions)
@router.post("/", response_model=schemas.Lead, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead: schemas.LeadCreate,
    background_tasks: BackgroundTasks
):
    """Create a new lead from the quote form submission"""
    
    # Get the main_data collection
    collection = get_collection(Collections.MAIN_DATA)
    
    # Check if lead with same email already exists
    existing_lead = await collection.find_one({"email": lead.email})
    
    if existing_lead:
        # Update existing lead with new information
        lead_data = lead.dict(exclude_unset=True)
        lead_data["updated_at"] = datetime.now(timezone.utc)
        
        await collection.update_one(
            {"_id": existing_lead["_id"]},
            {"$set": lead_data}
        )
        
        # Get updated document
        updated_doc = await collection.find_one({"_id": existing_lead["_id"]})
        
        # Log activity for updated lead
        activity_collection = get_collection(Collections.ACTIVITIES)
        activity = {
            "lead_id": existing_lead["_id"],
            "user_id": None,  # System user
            "activity_type": "note",
            "title": "Lead Updated",
            "description": f"Lead information updated via website form",
            "created_at": datetime.now(timezone.utc)
        }
        await activity_collection.insert_one(activity)
        
        return serialize_doc(updated_doc)
    
    # Create new lead
    lead_data = lead.dict()
    # Map camelCase to snake_case for database storage
    snake_case_data = {
        "_id": ObjectId(),
        "first_name": lead_data.get("firstName"),
        "last_name": lead_data.get("lastName"),
        "email": lead_data.get("email"),
        "phone_number": lead_data.get("phoneNumber"),
        "country": lead_data.get("country", "United States"),
        "address_line1": lead_data.get("addressLine1"),
        "address_line2": lead_data.get("addressLine2", ""),
        "city": lead_data.get("city"),
        "state": lead_data.get("state"),
        "zip_code": lead_data.get("zipCode"),
        "personal_lines": lead_data.get("personalLines", False),
        "commercial_lines": lead_data.get("commercialLines", False),
        "life_and_health": lead_data.get("lifeAndHealth", False),
        "source": lead_data.get("source", models.LeadSource.WEBSITE),
        "status": models.LeadStatus.NEW,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "priority": 3,  # Default priority
        "notes": ""
    }
    lead_data = snake_case_data
    
    # Insert into MongoDB
    result = await collection.insert_one(lead_data)
    
    # Create initial activity
    activity_collection = get_collection(Collections.ACTIVITIES)
    interests = []
    if lead.personalLines:
        interests.append("Personal Lines")
    if lead.commercialLines:
        interests.append("Commercial Lines")
    if lead.lifeAndHealth:
        interests.append("Life & Health")
    
    activity = {
        "lead_id": result.inserted_id,
        "user_id": None,  # System user
        "activity_type": "note",
        "title": "Lead Created",
        "description": f"New lead created via website form. Interested in: {', '.join(interests)}",
        "created_at": datetime.now(timezone.utc)
    }
    await activity_collection.insert_one(activity)
    
    # Send email notification in background
    background_tasks.add_task(send_new_lead_notification, lead.email, lead.firstName, lead.lastName)
    
    # Get the created document and return
    created_doc = await collection.find_one({"_id": result.inserted_id})
    return serialize_doc(created_doc)

# Get all leads with filtering and pagination
@router.get("/", response_model=schemas.LeadListResponse)
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[models.LeadStatus] = None,
    source: Optional[models.LeadSource] = None,
    assigned_agent_id: Optional[str] = None,
    priority: Optional[int] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    """Get leads with filtering and pagination"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Build query filter
    query_filter = {}
    
    if status:
        query_filter["status"] = status
    if source:
        query_filter["source"] = source
    if assigned_agent_id and ObjectId.is_valid(assigned_agent_id):
        query_filter["assigned_agent_id"] = ObjectId(assigned_agent_id)
    if priority:
        query_filter["priority"] = priority
    
    # Search functionality
    if search:
        query_filter["$or"] = [
            {"first_name": {"$regex": search, "$options": "i"}},
            {"last_name": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"phone_number": {"$regex": search, "$options": "i"}},
            {"city": {"$regex": search, "$options": "i"}}
        ]
    
# If user is not admin, only show their assigned leads
    if current_user.get("role") != models.UserRole.ADMIN.value:
        query_filter["assigned_agent_id"] = current_user["_id"]
    
    # Get total count
    total = await collection.count_documents(query_filter)
    
    # Get leads with pagination
    cursor = collection.find(query_filter).sort("created_at", -1).skip(skip).limit(limit)
    leads = await cursor.to_list(length=limit)
    
    # Serialize the results
    serialized_leads = [serialize_doc(lead) for lead in leads]
    
    return {
        "leads": serialized_leads,
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit,
        "total_pages": (total + limit - 1) // limit
    }

# Get single lead with full details
@router.get("/{lead_id}", response_model=schemas.LeadWithActivities)
async def get_lead(
    lead_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get a specific lead with all activities and quotes"""
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID format")
    
    collection = get_collection(Collections.MAIN_DATA)
    lead = await collection.find_one({"_id": ObjectId(lead_id)})
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if (current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value] and 
        lead.get("assigned_agent_id") != current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to view this lead")
    
    # Get activities for this lead
    activities_collection = get_collection(Collections.ACTIVITIES)
    activities_cursor = activities_collection.find({"lead_id": ObjectId(lead_id)}).sort("created_at", -1)
    activities = await activities_cursor.to_list(length=None)
    
    # Get quotes for this lead
    quotes_collection = get_collection(Collections.QUOTES)
    quotes_cursor = quotes_collection.find({"lead_id": ObjectId(lead_id)}).sort("created_at", -1)
    quotes = await quotes_cursor.to_list(length=None)
    
    # Serialize and combine data
    result = serialize_doc(lead)
    result["activities"] = serialize_doc(activities)
    result["quotes"] = serialize_doc(quotes)
    
    return result

# Update lead
@router.put("/{lead_id}", response_model=schemas.Lead)
async def update_lead(
    lead_id: str,
    lead_update: schemas.LeadUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update a lead"""
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID format")
    
    collection = get_collection(Collections.MAIN_DATA)
    lead = await collection.find_one({"_id": ObjectId(lead_id)})
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if (current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value] and 
        lead.get("assigned_agent_id") != current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this lead")
    
    # Track status changes
    old_status = lead.get("status")
    
    # Update lead fields
    update_data = lead_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # Update last contact date if status changed
    if "status" in update_data and old_status != update_data["status"]:
        update_data["last_contact_date"] = datetime.now(timezone.utc)
        
        # Log status change activity
        activity_collection = get_collection(Collections.ACTIVITIES)
        activity = {
            "lead_id": ObjectId(lead_id),
            "user_id": current_user["_id"],
            "activity_type": "status_change",
            "title": "Status Changed",
            "description": f"Status changed from {old_status} to {update_data['status']}",
            "created_at": datetime.now(timezone.utc)
        }
        await activity_collection.insert_one(activity)
    
    # Update the document
    await collection.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": update_data}
    )
    
    # Get updated document
    updated_lead = await collection.find_one({"_id": ObjectId(lead_id)})
    return serialize_doc(updated_lead)

# Delete lead
@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: str,
    current_user: dict = Depends(require_role(models.UserRole.ADMIN.value))
):
    """Delete a lead (admin only)"""
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID format")
    
    collection = get_collection(Collections.MAIN_DATA)
    lead = await collection.find_one({"_id": ObjectId(lead_id)})
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Delete lead and related data
    await collection.delete_one({"_id": ObjectId(lead_id)})
    
    # Delete related activities
    activities_collection = get_collection(Collections.ACTIVITIES)
    await activities_collection.delete_many({"lead_id": ObjectId(lead_id)})
    
    # Delete related quotes
    quotes_collection = get_collection(Collections.QUOTES)
    await quotes_collection.delete_many({"lead_id": ObjectId(lead_id)})
    
    return {"message": "Lead deleted successfully"}

# Assign lead to agent
@router.post("/{lead_id}/assign/{agent_id}")
async def assign_lead(
    lead_id: str,
    agent_id: str,
    current_user: dict = Depends(require_role(models.UserRole.MANAGER.value))
):
    """Assign a lead to an agent (manager+ only)"""
    
    if not ObjectId.is_valid(lead_id) or not ObjectId.is_valid(agent_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    collection = get_collection(Collections.MAIN_DATA)
    lead = await collection.find_one({"_id": ObjectId(lead_id)})
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check if agent exists
    users_collection = get_collection(Collections.USERS)
    agent = await users_collection.find_one({"_id": ObjectId(agent_id)})
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Update lead assignment
    await collection.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {
            "assigned_agent_id": ObjectId(agent_id),
            "updated_at": datetime.now(timezone.utc)
        }}
    )
    
    # Log assignment activity
    activity_collection = get_collection(Collections.ACTIVITIES)
    activity = {
        "lead_id": ObjectId(lead_id),
        "user_id": current_user["_id"],
        "activity_type": "note",
        "title": "Lead Assigned",
        "description": f"Lead assigned to {agent.get('full_name', 'Unknown')}",
        "created_at": datetime.now(timezone.utc)
    }
    await activity_collection.insert_one(activity)
    
    return {"message": f"Lead assigned to {agent.get('full_name', 'agent')}"}

# Add activity to lead
@router.post("/{lead_id}/activities", response_model=schemas.Activity)
async def add_activity(
    lead_id: str,
    activity: schemas.ActivityCreate,
    current_user: dict = Depends(get_current_active_user)
):
    """Add an activity to a lead"""
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID format")
    
    collection = get_collection(Collections.MAIN_DATA)
    lead = await collection.find_one({"_id": ObjectId(lead_id)})
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if (current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value] and 
        lead.get("assigned_agent_id") != current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to add activities to this lead")
    
    # Create activity
    activity_data = activity.dict()
    activity_data["_id"] = ObjectId()
    activity_data["lead_id"] = ObjectId(lead_id)
    activity_data["user_id"] = current_user["_id"]
    activity_data["created_at"] = datetime.now(timezone.utc)
    
    activity_collection = get_collection(Collections.ACTIVITIES)
    result = await activity_collection.insert_one(activity_data)
    
    # Update lead's last contact date
    await collection.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {"last_contact_date": datetime.now(timezone.utc)}}
    )
    
    # Get the created activity and return
    created_activity = await activity_collection.find_one({"_id": result.inserted_id})
    return serialize_doc(created_activity)

# Get lead activities
@router.get("/{lead_id}/activities", response_model=List[schemas.Activity])
async def get_lead_activities(
    lead_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """Get all activities for a lead"""
    
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead ID format")
    
    collection = get_collection(Collections.MAIN_DATA)
    lead = await collection.find_one({"_id": ObjectId(lead_id)})
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check permissions
    if (current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value] and 
        lead.get("assigned_agent_id") != current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to view activities for this lead")
    
    activity_collection = get_collection(Collections.ACTIVITIES)
    cursor = activity_collection.find({"lead_id": ObjectId(lead_id)}).sort("created_at", -1)
    activities = await cursor.to_list(length=None)
    
    return [serialize_doc(activity) for activity in activities]

# Get leads requiring follow-up
@router.get("/followup/pending", response_model=List[schemas.Lead])
async def get_pending_followups(
    current_user: dict = Depends(get_current_active_user)
):
    """Get leads that require follow-up"""
    
    today = datetime.now(timezone.utc)
    
    collection = get_collection(Collections.MAIN_DATA)
    
    query_filter = {
        "next_follow_up_date": {"$lte": today},
        "status": {"$in": ["new", "contacted", "qualified", "follow_up"]}
    }
    
    # If not admin/manager, only show assigned leads
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        query_filter["assigned_agent_id"] = current_user["_id"]
    
    cursor = collection.find(query_filter).sort("next_follow_up_date", 1)
    leads = await cursor.to_list(length=None)
    
    return [serialize_doc(lead) for lead in leads]