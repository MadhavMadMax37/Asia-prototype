from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from contextlib import asynccontextmanager

from database import connect_to_mongo, close_mongo_connection
from routers import leads, auth, dashboard, analytics
from auth_utils import get_current_user
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - Connect to MongoDB
    await connect_to_mongo()
    yield
    # Shutdown - Close MongoDB connection
    await close_mongo_connection()

app = FastAPI(
    title="Insurance CRM API",
    description="A comprehensive CRM system for insurance agencies",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {"message": "Insurance CRM API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)