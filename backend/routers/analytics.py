from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from bson import ObjectId
import pymongo

from database import get_collection, Collections
import models
import schemas
from auth_utils import get_current_active_user, require_role

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

@router.get("/conversion-funnel")
async def get_conversion_funnel(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get conversion funnel data"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base query filter
    base_filter = {"created_at": {"$gte": start_date}}
    
    # Filter by agent if not admin/manager
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Define funnel stages with progression logic
    stages = [
        {"name": "New Leads", "statuses": ["new"]},
        {"name": "Contacted", "statuses": ["contacted", "qualified", "proposal_sent", "closed_won"]},
        {"name": "Qualified", "statuses": ["qualified", "proposal_sent", "closed_won"]},
        {"name": "Proposal Sent", "statuses": ["proposal_sent", "closed_won"]},
        {"name": "Closed Won", "statuses": ["closed_won"]}
    ]
    
    funnel_data = []
    previous_count = None
    
    for stage in stages:
        stage_filter = {**base_filter, "status": {"$in": stage["statuses"]}}
        count = await collection.count_documents(stage_filter)
        
        conversion_rate = None
        if previous_count is not None and previous_count > 0:
            conversion_rate = round((count / previous_count) * 100, 2)
        
        funnel_data.append({
            "stage": stage["name"],
            "count": count,
            "conversion_rate": conversion_rate
        })
        
        previous_count = count
    
    return {"funnel": funnel_data, "period_days": days}

@router.get("/leads-by-month")
async def get_leads_by_month(
    months: int = Query(12, description="Number of months to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get leads created by month"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=months * 30)
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base pipeline
    pipeline = [
        {"$match": {"created_at": {"$gte": start_date}}}
    ]
    
    # Filter by agent if not admin/manager
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        pipeline[0]["$match"]["assigned_agent_id"] = current_user["_id"]
    
    # Group by year and month
    pipeline.extend([
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"}
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ])
    
    cursor = collection.aggregate(pipeline)
    results = []
    
    async for doc in cursor:
        month_name = datetime(doc["_id"]["year"], doc["_id"]["month"], 1).strftime('%B %Y')
        results.append({
            "month": month_name,
            "year": doc["_id"]["year"],
            "month_number": doc["_id"]["month"],
            "count": doc["count"]
        })
    
    return {"monthly_data": results}

@router.get("/agent-performance")
async def get_agent_performance(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(require_role(models.UserRole.MANAGER.value))
):
    """Get agent performance metrics (manager+ only)"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    # Get all agents
    users_collection = get_collection(Collections.USERS)
    agents_cursor = users_collection.find({
        "role": {"$in": ["agent", "manager"]},
        "is_active": True
    })
    
    performance_data = []
    leads_collection = get_collection(Collections.MAIN_DATA)
    activities_collection = get_collection(Collections.ACTIVITIES)
    
    async for agent in agents_cursor:
        agent_id = agent["_id"]
        
        # Agent's leads in the period
        agent_filter = {
            "assigned_agent_id": agent_id,
            "created_at": {"$gte": start_date}
        }
        
        total_leads = await leads_collection.count_documents(agent_filter)
        qualified_leads = await leads_collection.count_documents({
            **agent_filter,
            "status": "qualified"
        })
        closed_won = await leads_collection.count_documents({
            **agent_filter,
            "status": "closed_won"
        })
        closed_lost = await leads_collection.count_documents({
            **agent_filter,
            "status": "closed_lost"
        })
        
        # Calculate metrics
        qualification_rate = (qualified_leads / total_leads * 100) if total_leads > 0 else 0
        close_rate = (closed_won / (closed_won + closed_lost) * 100) if (closed_won + closed_lost) > 0 else 0
        
        # Get total estimated value
        pipeline = [
            {"$match": agent_filter},
            {"$group": {"_id": None, "total_value": {"$sum": "$estimated_value"}}}
        ]
        cursor = leads_collection.aggregate(pipeline)
        total_value_result = await cursor.to_list(length=1)
        estimated_value = total_value_result[0]["total_value"] if total_value_result else 0
        
        # Get activity count
        activity_count = await activities_collection.count_documents({
            "user_id": agent_id,
            "created_at": {"$gte": start_date}
        })
        
        performance_data.append({
            "agent_name": agent.get("full_name", "Unknown"),
            "agent_id": str(agent_id),
            "total_leads": total_leads,
            "qualified_leads": qualified_leads,
            "closed_won": closed_won,
            "closed_lost": closed_lost,
            "qualification_rate": round(qualification_rate, 2),
            "close_rate": round(close_rate, 2),
            "estimated_value": estimated_value or 0,
            "activity_count": activity_count
        })
    
    # Sort by total leads descending
    performance_data.sort(key=lambda x: x['total_leads'], reverse=True)
    
    return {"performance_data": performance_data, "period_days": days}

@router.get("/lead-sources-analysis")
async def get_lead_sources_analysis(
    days: int = Query(90, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Analyze lead sources performance"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    source_analysis = []
    
    # Analyze each source
    for source in models.LeadSource:
        source_filter = {**base_filter, "source": source.value}
        
        total_count = await collection.count_documents(source_filter)
        qualified_count = await collection.count_documents({
            **source_filter,
            "status": "qualified"
        })
        closed_won_count = await collection.count_documents({
            **source_filter,
            "status": "closed_won"
        })
        closed_lost_count = await collection.count_documents({
            **source_filter,
            "status": "closed_lost"
        })
        
        # Calculate rates
        qualification_rate = (qualified_count / total_count * 100) if total_count > 0 else 0
        close_rate = (closed_won_count / (closed_won_count + closed_lost_count) * 100) if (closed_won_count + closed_lost_count) > 0 else 0
        
        # Average estimated value
        pipeline = [
            {"$match": source_filter},
            {"$group": {"_id": None, "avg_value": {"$avg": "$estimated_value"}}}
        ]
        cursor = collection.aggregate(pipeline)
        avg_result = await cursor.to_list(length=1)
        avg_value = avg_result[0]["avg_value"] if avg_result else 0
        
        source_analysis.append({
            "source": source.value,
            "total_leads": total_count,
            "qualified_leads": qualified_count,
            "closed_won": closed_won_count,
            "closed_lost": closed_lost_count,
            "qualification_rate": round(qualification_rate, 2),
            "close_rate": round(close_rate, 2),
            "average_estimated_value": round(avg_value or 0, 2)
        })
    
    # Sort by total leads descending
    source_analysis.sort(key=lambda x: x['total_leads'], reverse=True)
    
    return {"source_analysis": source_analysis, "period_days": days}

@router.get("/activity-timeline")
async def get_activity_timeline(
    lead_id: Optional[str] = Query(None, description="Specific lead ID"),
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get activity timeline"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    activities_collection = get_collection(Collections.ACTIVITIES)
    
    # Build query filter
    query_filter = {"created_at": {"$gte": start_date}}
    
    # Filter by specific lead if provided
    if lead_id:
        if not ObjectId.is_valid(lead_id):
            raise HTTPException(status_code=400, detail="Invalid lead ID format")
        query_filter["lead_id"] = ObjectId(lead_id)
    
    # Filter by user role
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        # Get only activities for leads assigned to this user
        leads_collection = get_collection(Collections.MAIN_DATA)
        user_leads_cursor = leads_collection.find(
            {"assigned_agent_id": current_user["_id"]},
            {"_id": 1}
        )
        user_lead_ids = [lead["_id"] async for lead in user_leads_cursor]
        query_filter["lead_id"] = {"$in": user_lead_ids}
    
    # Group by date and activity type
    pipeline = [
        {"$match": query_filter},
        {
            "$group": {
                "_id": {
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$created_at"
                        }
                    },
                    "activity_type": "$activity_type"
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.date": 1}}
    ]
    
    cursor = activities_collection.aggregate(pipeline)
    timeline_data = {}
    
    async for doc in cursor:
        date_str = doc["_id"]["date"]
        activity_type = doc["_id"]["activity_type"]
        count = doc["count"]
        
        if date_str not in timeline_data:
            timeline_data[date_str] = {}
        
        timeline_data[date_str][activity_type] = count
    
    return {"timeline_data": timeline_data, "period_days": days}

@router.get("/revenue-forecast")
async def get_revenue_forecast(
    current_user: dict = Depends(get_current_active_user)
):
    """Get revenue forecast based on pipeline"""
    
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter for leads with estimated value in active statuses
    base_filter = {
        "estimated_value": {"$ne": None, "$gt": 0},
        "status": {"$in": ["new", "contacted", "qualified", "proposal_sent"]}
    }
    
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Define probability multipliers for each status
    status_probabilities = {
        "new": 0.1,
        "contacted": 0.2,
        "qualified": 0.5,
        "proposal_sent": 0.8
    }
    
    forecast_data = []
    total_weighted_value = 0
    
    for status, probability in status_probabilities.items():
        # Get leads for this status
        status_filter = {**base_filter, "status": status}
        
        pipeline = [
            {"$match": status_filter},
            {
                "$group": {
                    "_id": None,
                    "count": {"$sum": 1},
                    "total_value": {"$sum": "$estimated_value"}
                }
            }
        ]
        
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=1)
        
        if results:
            result = results[0]
            lead_count = result["count"]
            total_value = result["total_value"]
        else:
            lead_count = 0
            total_value = 0
        
        weighted_value = total_value * probability
        total_weighted_value += weighted_value
        
        forecast_data.append({
            "status": status,
            "lead_count": lead_count,
            "total_value": total_value,
            "probability": probability,
            "weighted_value": round(weighted_value, 2)
        })
    
    return {
        "forecast_data": forecast_data,
        "total_pipeline_value": sum(f["total_value"] for f in forecast_data),
        "weighted_forecast": round(total_weighted_value, 2)
    }

@router.get("/lead-response-time")
async def get_lead_response_time(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Analyze lead response time metrics"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    leads_collection = get_collection(Collections.MAIN_DATA)
    activities_collection = get_collection(Collections.ACTIVITIES)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Get leads with their first contact activities
    pipeline = [
        {"$match": base_filter},
        {
            "$lookup": {
                "from": "activities",
                "localField": "_id",
                "foreignField": "lead_id",
                "as": "activities"
            }
        },
        {
            "$addFields": {
                "first_contact": {
                    "$min": {
                        "$filter": {
                            "input": "$activities",
                            "cond": {"$in": ["$$this.activity_type", ["call", "email", "meeting"]]}
                        }
                    }
                }
            }
        },
        {
            "$addFields": {
                "response_time_hours": {
                    "$cond": {
                        "if": {"$ne": ["$first_contact", None]},
                        "then": {
                            "$divide": [
                                {"$subtract": ["$first_contact.created_at", "$created_at"]},
                                3600000  # Convert milliseconds to hours
                            ]
                        },
                        "else": None
                    }
                }
            }
        },
        {
            "$match": {"response_time_hours": {"$ne": None}}
        }
    ]
    
    cursor = leads_collection.aggregate(pipeline)
    response_times = []
    
    async for doc in cursor:
        if doc["response_time_hours"] is not None:
            response_times.append(doc["response_time_hours"])
    
    if not response_times:
        return {
            "average_response_time_hours": 0,
            "median_response_time_hours": 0,
            "fastest_response_hours": 0,
            "slowest_response_hours": 0,
            "total_responded_leads": 0,
            "response_time_breakdown": []
        }
    
    response_times.sort()
    total_leads = len(response_times)
    
    # Calculate statistics
    average_response = sum(response_times) / total_leads
    median_response = response_times[total_leads // 2] if total_leads % 2 == 1 else (response_times[total_leads // 2 - 1] + response_times[total_leads // 2]) / 2
    
    # Response time breakdown
    breakdown = {
        "< 1 hour": len([t for t in response_times if t < 1]),
        "1-4 hours": len([t for t in response_times if 1 <= t < 4]),
        "4-24 hours": len([t for t in response_times if 4 <= t < 24]),
        "1-3 days": len([t for t in response_times if 24 <= t < 72]),
        "> 3 days": len([t for t in response_times if t >= 72])
    }
    
    breakdown_list = [
        {"range": range_name, "count": count, "percentage": round(count/total_leads*100, 2)}
        for range_name, count in breakdown.items()
    ]
    
    return {
        "average_response_time_hours": round(average_response, 2),
        "median_response_time_hours": round(median_response, 2),
        "fastest_response_hours": round(min(response_times), 2),
        "slowest_response_hours": round(max(response_times), 2),
        "total_responded_leads": total_leads,
        "response_time_breakdown": breakdown_list
    }

@router.get("/geographic-distribution")
async def get_geographic_distribution(
    days: int = Query(90, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Analyze lead geographic distribution"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Group by state
    pipeline = [
        {"$match": base_filter},
        {
            "$group": {
                "_id": "$state",
                "count": {"$sum": 1},
                "total_estimated_value": {"$sum": "$estimated_value"},
                "avg_estimated_value": {"$avg": "$estimated_value"},
                "closed_won": {
                    "$sum": {"$cond": [{"$eq": ["$status", "closed_won"]}, 1, 0]}
                }
            }
        },
        {"$sort": {"count": -1}}
    ]
    
    cursor = collection.aggregate(pipeline)
    state_data = []
    total_leads = 0
    
    async for doc in cursor:
        count = doc["count"]
        total_leads += count
        
        state_data.append({
            "state": doc["_id"] or "Unknown",
            "count": count,
            "total_estimated_value": doc["total_estimated_value"] or 0,
            "avg_estimated_value": round(doc["avg_estimated_value"] or 0, 2),
            "closed_won": doc["closed_won"],
            "close_rate": round((doc["closed_won"] / count) * 100, 2) if count > 0 else 0
        })
    
    # Add percentages
    for state in state_data:
        state["percentage"] = round((state["count"] / total_leads) * 100, 2) if total_leads > 0 else 0
    
    # Group by city for top cities
    city_pipeline = [
        {"$match": base_filter},
        {
            "$group": {
                "_id": {"city": "$city", "state": "$state"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    
    city_cursor = collection.aggregate(city_pipeline)
    city_data = []
    
    async for doc in city_cursor:
        city_data.append({
            "city": doc["_id"]["city"] or "Unknown",
            "state": doc["_id"]["state"] or "Unknown",
            "count": doc["count"]
        })
    
    return {
        "by_state": state_data,
        "top_cities": city_data,
        "total_leads": total_leads,
        "period_days": days
    }

@router.get("/pipeline-velocity")
async def get_pipeline_velocity(
    current_user: dict = Depends(get_current_active_user)
):
    """Analyze pipeline velocity - average time in each stage"""
    
    activities_collection = get_collection(Collections.ACTIVITIES)
    
    # Base filter for status change activities
    base_filter = {"activity_type": "status_change"}
    
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        # Get only activities for leads assigned to this user
        leads_collection = get_collection(Collections.MAIN_DATA)
        user_leads_cursor = leads_collection.find(
            {"assigned_agent_id": current_user["_id"]},
            {"_id": 1}
        )
        user_lead_ids = [lead["_id"] async for lead in user_leads_cursor]
        base_filter["lead_id"] = {"$in": user_lead_ids}
    
    # Get all status change activities ordered by lead and time
    cursor = activities_collection.find(base_filter).sort([("lead_id", 1), ("created_at", 1)])
    
    # Group activities by lead
    lead_activities = {}
    async for activity in cursor:
        lead_id = str(activity["lead_id"])
        if lead_id not in lead_activities:
            lead_activities[lead_id] = []
        lead_activities[lead_id].append(activity)
    
    # Calculate time in each stage
    stage_times = {
        "new": [],
        "contacted": [],
        "qualified": [],
        "proposal_sent": []
    }
    
    for lead_id, activities in lead_activities.items():
        if len(activities) < 2:
            continue
        
        for i in range(len(activities) - 1):
            current_activity = activities[i]
            next_activity = activities[i + 1]
            
            # Extract status from description (format: "Status changed from X to Y")
            desc = current_activity.get("description", "")
            if "Status changed from" in desc:
                try:
                    parts = desc.split(" to ")
                    if len(parts) == 2:
                        from_status = parts[0].split("from ")[-1].strip()
                        
                        # Calculate time difference in hours
                        time_diff = (next_activity["created_at"] - current_activity["created_at"]).total_seconds() / 3600
                        
                        if from_status in stage_times:
                            stage_times[from_status].append(time_diff)
                except:
                    continue
    
    # Calculate average times
    velocity_data = []
    for stage, times in stage_times.items():
        if times:
            avg_hours = sum(times) / len(times)
            velocity_data.append({
                "stage": stage,
                "average_time_hours": round(avg_hours, 2),
                "average_time_days": round(avg_hours / 24, 2),
                "sample_size": len(times),
                "min_time_hours": round(min(times), 2),
                "max_time_hours": round(max(times), 2)
            })
        else:
            velocity_data.append({
                "stage": stage,
                "average_time_hours": 0,
                "average_time_days": 0,
                "sample_size": 0,
                "min_time_hours": 0,
                "max_time_hours": 0
            })
    
    return {"velocity_data": velocity_data}

@router.get("/performance-trends")
async def get_performance_trends(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: dict = Depends(get_current_active_user)
):
    """Get performance trends over time"""
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    collection = get_collection(Collections.MAIN_DATA)
    
    # Base filter
    base_filter = {"created_at": {"$gte": start_date}}
    if current_user.get("role") not in [models.UserRole.ADMIN.value, models.UserRole.MANAGER.value]:
        base_filter["assigned_agent_id"] = current_user["_id"]
    
    # Group by week
    pipeline = [
        {"$match": base_filter},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "week": {"$week": "$created_at"}
                },
                "total_leads": {"$sum": 1},
                "qualified_leads": {
                    "$sum": {"$cond": [{"$eq": ["$status", "qualified"]}, 1, 0]}
                },
                "closed_won": {
                    "$sum": {"$cond": [{"$eq": ["$status", "closed_won"]}, 1, 0]}
                },
                "total_value": {"$sum": "$estimated_value"}
            }
        },
        {"$sort": {"_id.year": 1, "_id.week": 1}}
    ]
    
    cursor = collection.aggregate(pipeline)
    trends = []
    
    async for doc in cursor:
        total = doc["total_leads"]
        qualified = doc["qualified_leads"]
        won = doc["closed_won"]
        
        trends.append({
            "week": f"{doc['_id']['year']}-W{doc['_id']['week']:02d}",
            "total_leads": total,
            "qualified_leads": qualified,
            "closed_won": won,
            "qualification_rate": round((qualified / total) * 100, 2) if total > 0 else 0,
            "close_rate": round((won / total) * 100, 2) if total > 0 else 0,
            "total_value": doc["total_value"] or 0
        })
    
    return {"trends": trends, "period_days": days}