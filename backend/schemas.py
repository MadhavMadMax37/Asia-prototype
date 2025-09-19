from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from models import LeadStatus, LeadSource, ActivityType, UserRole, PyObjectId

# Base schemas
class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True
    }

# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole = UserRole.AGENT

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: Optional[PyObjectId] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }

# Lead schemas (matches the form data from frontend)
class LeadBase(BaseSchema):
    firstName: str
    lastName: str
    email: EmailStr
    phoneNumber: str
    country: str = "United States"
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: str
    zipCode: str
    personalLines: bool = False
    commercialLines: bool = False
    lifeAndHealth: bool = False

class LeadCreate(LeadBase):
    source: LeadSource = LeadSource.WEBSITE

class LeadUpdate(BaseSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    country: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    personal_lines: Optional[bool] = None
    commercial_lines: Optional[bool] = None
    life_and_health: Optional[bool] = None
    status: Optional[LeadStatus] = None
    source: Optional[LeadSource] = None
    assigned_agent_id: Optional[PyObjectId] = None
    priority: Optional[int] = None
    estimated_value: Optional[float] = None
    notes: Optional[str] = None
    next_follow_up_date: Optional[datetime] = None
    custom_fields: Optional[Dict[str, Any]] = None

class Lead(LeadBase):
    id: Optional[PyObjectId] = None
    status: LeadStatus
    source: LeadSource
    assigned_agent_id: Optional[PyObjectId] = None
    priority: int
    estimated_value: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_contact_date: Optional[datetime] = None
    next_follow_up_date: Optional[datetime] = None
    custom_fields: Optional[Dict[str, Any]] = None
    assigned_agent: Optional[User] = None
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }

class LeadWithActivities(Lead):
    activities: List['Activity'] = []
    quotes: List['Quote'] = []

# Activity schemas
class ActivityBase(BaseSchema):
    activity_type: ActivityType
    title: str
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class ActivityCreate(ActivityBase):
    lead_id: PyObjectId

class ActivityUpdate(BaseSchema):
    activity_type: Optional[ActivityType] = None
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    outcome: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class Activity(ActivityBase):
    id: Optional[PyObjectId] = None
    lead_id: PyObjectId
    user_id: PyObjectId
    completed_at: Optional[datetime] = None
    created_at: datetime
    user: Optional[User] = None
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }

# Quote schemas
class QuoteBase(BaseSchema):
    insurance_type: str
    coverage_details: Optional[Dict[str, Any]] = None
    premium_amount: Optional[float] = None
    deductible: Optional[float] = None
    coverage_start_date: Optional[datetime] = None
    coverage_end_date: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class QuoteCreate(QuoteBase):
    lead_id: PyObjectId

class QuoteUpdate(BaseSchema):
    insurance_type: Optional[str] = None
    coverage_details: Optional[Dict[str, Any]] = None
    premium_amount: Optional[float] = None
    deductible: Optional[float] = None
    coverage_start_date: Optional[datetime] = None
    coverage_end_date: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    is_accepted: Optional[bool] = None
    quote_document_url: Optional[str] = None
    attachments: Optional[List[str]] = None

class Quote(QuoteBase):
    id: Optional[PyObjectId] = None
    lead_id: PyObjectId
    quote_number: str
    is_active: bool
    is_accepted: bool
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    quote_document_url: Optional[str] = None
    attachments: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }

# Authentication schemas
class Token(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseSchema):
    username: Optional[str] = None

class UserLogin(BaseSchema):
    username: str
    password: str

# Dashboard schemas
class DashboardStats(BaseSchema):
    total_leads: int
    new_leads: int
    qualified_leads: int
    closed_won: int
    closed_lost: int
    conversion_rate: float
    total_estimated_value: float
    leads_this_week: int
    leads_this_month: int

class LeadsByStatus(BaseSchema):
    status: str
    count: int
    percentage: float

class LeadsBySource(BaseSchema):
    source: str
    count: int
    percentage: float

class ActivitySummary(BaseSchema):
    activity_type: str
    count: int
    last_7_days: int

# Response schemas
class Message(BaseSchema):
    message: str

class LeadListResponse(BaseSchema):
    leads: List[Lead]
    total: int
    page: int
    per_page: int
    total_pages: int

# Email template schemas
class EmailTemplateBase(BaseSchema):
    name: str
    subject: str
    body: str
    template_type: str

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplate(EmailTemplateBase):
    id: Optional[PyObjectId] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {PyObjectId: str}
    }

# Forward references for relationships
LeadWithActivities.model_rebuild()
Activity.model_rebuild()