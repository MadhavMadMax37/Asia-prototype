from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from bson import ObjectId

from database import get_collection, Collections
import models
import schemas
from auth_utils import get_current_active_user

router = APIRouter()

# Helper function to serialize MongoDB documents
def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = serialize_doc(value)
            elif isinstance(value, list):
                result[key] = serialize_doc(value)
            else:
                result[key] = value
        return result
    return doc

@router.get("/stats")
async def get_dashboard_stats(
    current_user: dict = Depends(get_current_active_user)
):
    """Get comprehensive dashboard statistics"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter for user role
    base_filter = {}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Get current date ranges
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Total leads
    total_leads = await collection.count_documents(base_filter)
    
    # Leads by status
    status_counts = {}
    for status in models.LeadStatus:
        count = await collection.count_documents({**base_filter, "status": status.value})
        status_counts[status.value] = count
    
    # Recent leads (this week and month)
    leads_this_week = await collection.count_documents({
        **base_filter,
        "created_at": {"$gte": week_ago}
    })
    
    leads_this_month = await collection.count_documents({
        **base_filter,
        "created_at": {"$gte": month_ago}
    })
    
    # Calculate conversion rate
    total_closed = status_counts.get("closed_won", 0) + status_counts.get("closed_lost", 0)
    conversion_rate = (status_counts.get("closed_won", 0) / total_closed * 100) if total_closed > 0 else 0
    
    # Total estimated value
    pipeline = [
        {"$match": base_filter},
        {"$group": {"_id": None, "total_value": {"$sum": "$estimated_value"}}}
    ]
    cursor = collection.aggregate(pipeline)
    value_result = await cursor.to_list(length=1)
    total_estimated_value = value_result[0]["total_value"] if value_result else 0
    
    return {
        "total_leads": total_leads,
        "new_leads": status_counts.get("new", 0),
        "qualified_leads": status_counts.get("qualified", 0),
        "closed_won": status_counts.get("closed_won", 0),
        "closed_lost": status_counts.get("closed_lost", 0),
        "conversion_rate": round(conversion_rate, 2),
        "total_estimated_value": total_estimated_value or 0,
        "leads_this_week": leads_this_week,
        "leads_this_month": leads_this_month
    }

@router.get("/leads-by-status")
async def get_leads_by_status(
    current_user: dict = Depends(get_current_active_user)
):
    """Get leads distribution by status"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter for user role
    base_filter = {}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Get total count first
    total_leads = await collection.count_documents(base_filter)
    
    # Get counts by status
    status_data = []
    for status in models.LeadStatus:
        count = await collection.count_documents({**base_filter, "status": status.value})
        percentage = (count / total_leads * 100) if total_leads > 0 else 0
        
        status_data.append({
            "status": status.value.title().replace("_", " "),
            "count": count,
            "percentage": round(percentage, 2)
        })
    
    # Sort by count descending
    status_data.sort(key=lambda x: x["count"], reverse=True)
    
    return {"status_distribution": status_data, "total_leads": total_leads}

@router.get("/leads-by-source")
async def get_leads_by_source(
    current_user: dict = Depends(get_current_active_user)
):
    """Get leads distribution by source"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter for user role
    base_filter = {}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Get total count first
    total_leads = await collection.count_documents(base_filter)
    
    # Get counts by source
    source_data = []
    for source in models.LeadSource:
        count = await collection.count_documents({**base_filter, "source": source.value})
        percentage = (count / total_leads * 100) if total_leads > 0 else 0
        
        source_data.append({
            "source": source.value.title().replace("_", " "),
            "count": count,
            "percentage": round(percentage, 2)
        })
    
    # Sort by count descending
    source_data.sort(key=lambda x: x["count"], reverse=True)
    
    return {"source_distribution": source_data, "total_leads": total_leads}

@router.get("/activity-summary")
async def get_activity_summary(
    days: int = Query(7, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get activity summary for the dashboard"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    activities_collection = get_collection(Collections.ACTIVITIES)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    
    # Filter by user role
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        # Get only activities for leads assigned to this user
        leads_collection = get_collection(Collections.MAIN_DATA)
        user_leads_cursor = leads_collection.find(
            {"assigned_agent_id": current_user["_id"]},
            {"_id": 1}
        )
        user_lead_ids = [lead["_id"] async for lead in user_leads_cursor]
        base_filter["lead_id"] = {"$in": user_lead_ids}
    
    # Group by activity type
    pipeline = [
        {"$match": base_filter},
        {
            "$group": {
                "_id": "$activity_type",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}}
    ]
    
    cursor = activities_collection.aggregate(pipeline)
    activity_summary = []
    total_activities = 0
    
    async for doc in cursor:
        count = doc["count"]
        total_activities += count
        
        activity_summary.append({
            "activity_type": doc["_id"].title().replace("_", " "),
            "count": count
        })
    
    # Get last 7 days activity count for comparison
    last_week_start = start_date - timedelta(days=days)
    last_week_count = await activities_collection.count_documents({
        **base_filter,
        "created_at": {"$gte": last_week_start, "$lt": start_date}
    })
    
    # Add last 7 days count to each activity type
    for activity in activity_summary:
        activity["last_7_days"] = last_week_count  # Simplified for now
    
    return {
        "activity_summary": activity_summary,
        "total_activities": total_activities,
        "period_days": days
    }

@router.get("/recent-leads")
async def get_recent_leads(
    limit: int = Query(10, description="Number of recent leads to return"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get recent leads for the dashboard"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter for user role
    base_filter = {}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Get recent leads
    cursor = collection.find(base_filter).sort("created_at", -1).limit(limit)
    recent_leads = await cursor.to_list(length=limit)
    
    return {"recent_leads": [serialize_doc(lead) for lead in recent_leads]}

@router.get("/upcoming-followups")
async def get_upcoming_followups(
    days: int = Query(7, description="Number of days ahead to check"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get upcoming follow-ups"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Date range for upcoming follow-ups
    now = datetime.now(timezone.utc)
    future_date = now + timedelta(days=days)
    
    # Base filter
    base_filter = {
        "next_follow_up_date": {"$gte": now, "$lte": future_date},
        "status": {"$in": ["new", "contacted", "qualified", "follow_up"]}
    }
    
    # Filter by user role
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    cursor = collection.find(base_filter).sort("next_follow_up_date", 1)
    followups = await cursor.to_list(length=None)
    
    return {"upcoming_followups": [serialize_doc(lead) for lead in followups]}

@router.get("/overdue-followups")
async def get_overdue_followups(
    current_user: dict = Depends(get_current_active_user)
):
    """Get overdue follow-ups"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Current date
    now = datetime.now(timezone.utc)
    
    # Base filter
    base_filter = {
        "next_follow_up_date": {"$lt": now},
        "status": {"$in": ["new", "contacted", "qualified", "follow_up"]}
    }
    
    # Filter by user role
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    cursor = collection.find(base_filter).sort("next_follow_up_date", 1)
    overdue = await cursor.to_list(length=None)
    
    return {"overdue_followups": [serialize_doc(lead) for lead in overdue]}

@router.get("/top-performing-sources")
async def get_top_performing_sources(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get top performing lead sources"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Aggregate by source with conversion metrics
    pipeline = [
        {"$match": base_filter},
        {
            "$group": {
                "_id": "$source",
                "total_leads": {"$sum": 1},
                "qualified": {
                    "$sum": {"$cond": [{"$eq": ["$status", "qualified"]}, 1, 0]}
                },
                "closed_won": {
                    "$sum": {"$cond": [{"$eq": ["$status", "closed_won"]}, 1, 0]}
                },
                "total_value": {"$sum": "$estimated_value"}
            }
        },
        {
            "$addFields": {
                "conversion_rate": {
                    "$cond": [
                        {"$gt": ["$total_leads", 0]},
                        {"$multiply": [{"$divide": ["$closed_won", "$total_leads"]}, 100]},
                        0
                    ]
                }
            }
        },
        {"$sort": {"conversion_rate": -1}}
    ]
    
    cursor = collection.aggregate(pipeline)
    source_performance = []
    
    async for doc in cursor:
        source_performance.append({
            "source": doc["_id"].title().replace("_", " "),
            "total_leads": doc["total_leads"],
            "qualified": doc["qualified"],
            "closed_won": doc["closed_won"],
            "conversion_rate": round(doc["conversion_rate"], 2),
            "total_value": doc["total_value"] or 0
        })
    
    return {"top_sources": source_performance[:5], "period_days": days}

@router.get("/performance-metrics")
async def get_performance_metrics(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get key performance metrics"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    collection = get_collection(Collections.MAIN_DATA)
    activities_collection = get_collection(Collections.ACTIVITIES)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Total leads in period
    total_leads = await collection.count_documents(base_filter)
    
    # Leads by status
    qualified = await collection.count_documents({**base_filter, "status": "qualified"})
    closed_won = await collection.count_documents({**base_filter, "status": "closed_won"})
    closed_lost = await collection.count_documents({**base_filter, "status": "closed_lost"})
    
    # Calculate metrics
    qualification_rate = (qualified / total_leads * 100) if total_leads > 0 else 0
    close_rate = (closed_won / (closed_won + closed_lost) * 100) if (closed_won + closed_lost) > 0 else 0
    
    # Average deal size
    pipeline = [
        {"$match": {**base_filter, "status": "closed_won"}},
        {"$group": {"_id": None, "avg_deal_size": {"$avg": "$estimated_value"}}}
    ]
    cursor = collection.aggregate(pipeline)
    avg_result = await cursor.to_list(length=1)
    avg_deal_size = avg_result[0]["avg_deal_size"] if avg_result else 0
    
    # Activity count
    activity_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        # Get only activities for leads assigned to this user
        user_leads_cursor = collection.find(
            {"assigned_agent_id": current_user["_id"]},
            {"_id": 1}
        )
        user_lead_ids = [lead["_id"] async for lead in user_leads_cursor]
        activity_filter["lead_id"] = {"$in": user_lead_ids}
    
    total_activities = await activities_collection.count_documents(activity_filter)
    
    # Activities per lead
    activities_per_lead = (total_activities / total_leads) if total_leads > 0 else 0
    
    return {
        "total_leads": total_leads,
        "qualification_rate": round(qualification_rate, 2),
        "close_rate": round(close_rate, 2),
        "average_deal_size": round(avg_deal_size or 0, 2),
        "total_activities": total_activities,
        "activities_per_lead": round(activities_per_lead, 2),
        "period_days": days
    }

@router.get("/chart-data/leads-trend")
async def get_leads_trend_chart_data(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get lead creation trend data for charts"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Group by day
    pipeline = [
        {"$match": base_filter},
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$created_at"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    cursor = collection.aggregate(pipeline)
    trend_data = []
    
    async for doc in cursor:
        trend_data.append({
            "date": doc["_id"],
            "count": doc["count"]
        })
    
    return {"trend_data": trend_data}

@router.get("/chart-data/conversion-funnel")
async def get_conversion_funnel_chart_data(
    current_user: dict = Depends(get_current_active_user)
):
    """Get conversion funnel data optimized for chart visualization"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter
    base_filter = {}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Define stages in order
    stages = [
        {"name": "New", "status": "new", "color": "#3B82F6"},
        {"name": "Contacted", "status": "contacted", "color": "#8B5CF6"},
        {"name": "Qualified", "status": "qualified", "color": "#10B981"},
        {"name": "Proposal", "status": "proposal_sent", "color": "#F59E0B"},
        {"name": "Closed Won", "status": "closed_won", "color": "#EF4444"}
    ]
    
    funnel_data = []
    for stage in stages:
        count = await collection.count_documents({
            **base_filter,
            "status": stage["status"]
        })
        
        funnel_data.append({
            "stage": stage["name"],
            "count": count,
            "color": stage["color"]
        })
    
    return {"funnel_data": funnel_data}

@router.get("/notifications")
async def get_dashboard_notifications(
    current_user: dict = Depends(get_current_active_user)
):
    """Get important notifications for the dashboard"""
    
    collection = get_collection(Collections.MAIN_DATA)
    now = datetime.now(timezone.utc)
    
    notifications = []
    
    # Base filter for user role
    base_filter = {}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Overdue follow-ups
    overdue_count = await collection.count_documents({
        **base_filter,
        "next_follow_up_date": {"$lt": now},
        "status": {"$in": ["new", "contacted", "qualified", "follow_up"]}
    })
    
    if overdue_count > 0:
        notifications.append({
            "type": "warning",
            "title": "Overdue Follow-ups",
            "message": f"You have {overdue_count} overdue follow-up{'s' if overdue_count > 1 else ''}",
            "count": overdue_count,
            "priority": "high"
        })
    
    # New leads today
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    new_today = await collection.count_documents({
        **base_filter,
        "created_at": {"$gte": today_start},
        "status": "new"
    })
    
    if new_today > 0:
        notifications.append({
            "type": "info",
            "title": "New Leads Today",
            "message": f"{new_today} new lead{'s' if new_today > 1 else ''} received today",
            "count": new_today,
            "priority": "medium"
        })
    
    # Hot prospects (high priority qualified leads)
    hot_prospects = await collection.count_documents({
        **base_filter,
        "status": "qualified",
        "priority": {"$gte": 3}
    })
    
    if hot_prospects > 0:
        notifications.append({
            "type": "success",
            "title": "Hot Prospects",
            "message": f"{hot_prospects} high-priority qualified lead{'s' if hot_prospects > 1 else ''}",
            "count": hot_prospects,
            "priority": "high"
        })
    
    # Sort by priority
    priority_order = {"high": 3, "medium": 2, "low": 1}
    notifications.sort(key=lambda x: priority_order.get(x["priority"], 0), reverse=True)
    
    return {"notifications": notifications}