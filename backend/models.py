from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
import enum

# Custom ObjectId type for Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ]),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")


# Enums
class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    FOLLOW_UP = "follow_up"


class LeadSource(str, enum.Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    PHONE_CALL = "phone_call"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    WALK_IN = "walk_in"
    OTHER = "other"


class ActivityType(str, enum.Enum):
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    NOTE = "note"
    QUOTE_SENT = "quote_sent"
    FOLLOW_UP = "follow_up"
    STATUS_CHANGE = "status_change"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AGENT = "agent"
    MANAGER = "manager"
    VIEWER = "viewer"

# Base MongoDB Model
class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }


# User Model
class User(MongoBaseModel):
    email: EmailStr
    username: str
    full_name: str
    hashed_password: str
    role: UserRole = UserRole.AGENT
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "email": "agent@example.com",
                "username": "agent123",
                "full_name": "John Agent",
                "role": "agent",
                "is_active": True
            }
        }

# Lead Model
class Lead(MongoBaseModel):
    # Personal Information
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    
    # Address Information
    country: str = "United States"
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    
    # Insurance Interests (from form checkboxes)
    personal_lines: bool = False
    commercial_lines: bool = False
    life_and_health: bool = False
    
    # CRM Fields
    status: LeadStatus = LeadStatus.NEW
    source: LeadSource = LeadSource.WEBSITE
    assigned_agent_id: Optional[PyObjectId] = None
    priority: int = Field(default=1, ge=1, le=3)  # 1=Low, 2=Medium, 3=High
    estimated_value: Optional[float] = None
    notes: Optional[str] = None
    
    # Timestamps
    last_contact_date: Optional[datetime] = None
    next_follow_up_date: Optional[datetime] = None
    
    # Additional data (flexible field for custom fields)
    custom_fields: Optional[Dict[str, Any]] = None

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+1-555-0123",
                "address_line1": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "personal_lines": True,
                "commercial_lines": False,
                "life_and_health": True,
                "status": "new",
                "source": "website",
                "priority": 2,
                "estimated_value": 5000.00
            }
        }

# Activity Model
class Activity(MongoBaseModel):
    lead_id: PyObjectId
    user_id: PyObjectId
    
    activity_type: ActivityType
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "activity_type": "call",
                "title": "Follow-up call",
                "description": "Discussed insurance needs",
                "duration_minutes": 15,
                "outcome": "Interested in life insurance quote"
            }
        }

# Quote Model
class Quote(MongoBaseModel):
    lead_id: PyObjectId
    quote_number: str
    
    # Quote details
    insurance_type: str  # Personal, Commercial, Life, etc.
    coverage_details: Optional[Dict[str, Any]] = None  # Flexible structure for different coverage types
    premium_amount: Optional[float] = None
    deductible: Optional[float] = None
    coverage_start_date: Optional[datetime] = None
    coverage_end_date: Optional[datetime] = None
    
    # Quote status and tracking
    is_active: bool = True
    is_accepted: bool = False
    expires_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    
    # Files and documents
    quote_document_url: Optional[str] = None
    attachments: Optional[List[str]] = None  # Array of file URLs

    class Config:
        schema_extra = {
            "example": {
                "quote_number": "Q-2024-001",
                "insurance_type": "Personal Lines",
                "premium_amount": 1200.00,
                "deductible": 500.00,
                "is_active": True
            }
        }


# Email Template Model
class EmailTemplate(MongoBaseModel):
    name: str
    subject: str
    body: str
    template_type: str  # welcome, follow_up, quote_sent, etc.
    is_active: bool = True

    class Config:
        schema_extra = {
            "example": {
                "name": "Welcome Email",
                "subject": "Welcome to our insurance services",
                "body": "Thank you for your interest in our insurance services...",
                "template_type": "welcome",
                "is_active": True
            }
        }


# Setting Model
class Setting(MongoBaseModel):
    key: str
    value: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "key": "max_leads_per_agent",
                "value": "100",
                "description": "Maximum number of leads that can be assigned to an agent"
            }
        }
