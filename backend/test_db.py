#!/usr/bin/env python3
from pymongo import MongoClient
from decouple import config

# Database configuration
MONGO_URL = config('MONGO_URL', default='mongodb://localhost:27017')
DATABASE_NAME = config('DATABASE_NAME', default='insurance_crm')
MAIN_COLLECTION = config('MAIN_COLLECTION', default='main_data')

def test_database():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URL)
        db = client[DATABASE_NAME]
        collection = db[MAIN_COLLECTION]
        
        # Test connection
        client.admin.command('ping')
        print(f"✅ Successfully connected to MongoDB at {MONGO_URL}")
        print(f"📊 Database: {DATABASE_NAME}")
        print(f"📁 Collection: {MAIN_COLLECTION}")
        
        # Count documents
        count = collection.count_documents({})
        print(f"📈 Total documents in collection: {count}")
        
        # Get all documents
        if count > 0:
            print("\n📋 Documents in collection:")
            for i, doc in enumerate(collection.find().limit(10), 1):
                print(f"\n--- Document {i} ---")
                print(f"ID: {doc.get('_id')}")
                print(f"Name: {doc.get('first_name')} {doc.get('last_name')}")
                print(f"Email: {doc.get('email')}")
                print(f"Phone: {doc.get('phone_number')}")
                print(f"Status: {doc.get('status')}")
                print(f"Created: {doc.get('created_at')}")
        else:
            print("🚫 No documents found in collection")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_database()