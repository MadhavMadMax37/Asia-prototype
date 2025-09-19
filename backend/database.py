from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from decouple import config
from typing import Optional
import asyncio

# Database configuration
MONGO_URL = config('MONGO_URL', default='mongodb://localhost:27017')
DATABASE_NAME = config('DATABASE_NAME', default='infos')
MAIN_COLLECTION = config('MAIN_COLLECTION', default='main_data')

# MongoDB client instances
motor_client: Optional[AsyncIOMotorClient] = None
sync_client: Optional[MongoClient] = None


class MongoDB:
    client: AsyncIOMotorClient = None
    database = None


mongo_db = MongoDB()


def get_mongo_client():
    """Get synchronous MongoDB client for non-async operations"""
    global sync_client
    if sync_client is None:
        sync_client = MongoClient(MONGO_URL)
    return sync_client


async def connect_to_mongo():
    """Create database connection"""
    mongo_db.client = AsyncIOMotorClient(MONGO_URL)
    mongo_db.database = mongo_db.client[DATABASE_NAME]
    
    # Test connection
    try:
        await mongo_db.client.admin.command('ping')
        print(f"Successfully connected to MongoDB at {MONGO_URL}")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        raise e


async def close_mongo_connection():
    """Close database connection"""
    if mongo_db.client:
        mongo_db.client.close()
        print("MongoDB connection closed")


def get_database():
    """Get async database instance"""
    return mongo_db.database


def get_collection(collection_name: str = MAIN_COLLECTION):
    """Get specific collection"""
    if mongo_db.database is None:
        raise Exception("Database not connected. Call connect_to_mongo() first.")
    return mongo_db.database[collection_name]


# Collection names
class Collections:
    MAIN_DATA = MAIN_COLLECTION  # For form submissions
    USERS = 'users'
    LEADS = 'leads'
    ACTIVITIES = 'activities'
    QUOTES = 'quotes'
    EMAIL_TEMPLATES = 'email_templates'
    SETTINGS = 'settings'