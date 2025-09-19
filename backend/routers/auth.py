from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime, timezone
from bson import ObjectId
from typing import List

from database import get_collection, Collections
import models
import schemas
from auth_utils import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_active_user,
    require_role,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

# Helper function to serialize MongoDB documents
def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
    return doc

@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Authenticate user and return access token"""
    
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    }

@router.post("/register", response_model=schemas.User)
async def register_user(
    user: schemas.UserCreate,
    current_user: dict = Depends(require_role(models.UserRole.ADMIN))
):
    """Register a new user (admin only)"""
    
    users_collection = get_collection(Collections.USERS)
    
    # Check if user already exists
    existing_user = await users_collection.find_one({
        "$or": [
            {"email": user.email},
            {"username": user.username}
        ]
    })
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_data = {
        "_id": ObjectId(),
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role.value,
        "hashed_password": hashed_password,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    result = await users_collection.insert_one(user_data)
    
    # Get the created user and return
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    return serialize_doc(created_user)

@router.get("/me", response_model=schemas.User)
async def get_current_user_info(
    current_user: dict = Depends(get_current_active_user)
):
    """Get current user information"""
    return serialize_doc(current_user)

@router.put("/me", response_model=schemas.User)
async def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """Update current user information"""
    
    users_collection = get_collection(Collections.USERS)
    
    # Users can only update their own basic info (not role or active status)
    allowed_fields = ["email", "full_name"]
    update_data = user_update.dict(exclude_unset=True, include=set(allowed_fields))
    
    # Check for duplicate email
    if "email" in update_data and update_data["email"] != current_user["email"]:
        existing_user = await users_collection.find_one({"email": update_data["email"]})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    # Update the user
    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc)
        await users_collection.update_one(
            {"_id": current_user["_id"]},
            {"$set": update_data}
        )
    
    # Get updated user
    updated_user = await users_collection.find_one({"_id": current_user["_id"]})
    return serialize_doc(updated_user)

@router.get("/users", response_model=List[schemas.User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(require_role(models.UserRole.ADMIN))
):
    """Get all users (admin only)"""
    
    users_collection = get_collection(Collections.USERS)
    
    cursor = users_collection.find({}).sort("created_at", -1).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    
    return [serialize_doc(user) for user in users]

@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: str,
    user_update: schemas.UserUpdate,
    current_user: dict = Depends(require_role(models.UserRole.ADMIN))
):
    """Update any user (admin only)"""
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    users_collection = get_collection(Collections.USERS)
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Check for duplicate email
    if "email" in update_data and update_data["email"] != user["email"]:
        existing_user = await users_collection.find_one({"email": update_data["email"]})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
    
    # Convert role enum to string if present
    if "role" in update_data and hasattr(update_data["role"], "value"):
        update_data["role"] = update_data["role"].value
    
    # Update the user
    if update_data:
        update_data["updated_at"] = datetime.now(timezone.utc)
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
    
    # Get updated user
    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return serialize_doc(updated_user)

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(require_role(models.UserRole.ADMIN))
):
    """Delete a user (admin only)"""
    
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    if str(current_user["_id"]) == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    users_collection = get_collection(Collections.USERS)
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Instead of deleting, just deactivate the user to preserve data integrity
    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}}
    )
    
    return {"message": "User deactivated successfully"}

@router.post("/create-admin")
async def create_admin_user():
    """Create initial admin user if no users exist"""
    
    users_collection = get_collection(Collections.USERS)
    
    # Check if any users exist
    user_count = await users_collection.count_documents({})
    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user already exists or users found in system"
        )
    
    # Create default admin user
    hashed_password = get_password_hash("admin123")  # Change this in production!
    admin_user = {
        "_id": ObjectId(),
        "email": "admin@insurance-crm.com",
        "username": "admin",
        "full_name": "System Administrator",
        "role": models.UserRole.ADMIN.value,
        "hashed_password": hashed_password,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    result = await users_collection.insert_one(admin_user)
    
    return {
        "message": "Admin user created successfully",
        "username": "admin",
        "email": "admin@insurance-crm.com",
        "note": "Please change the default password after first login"
    }