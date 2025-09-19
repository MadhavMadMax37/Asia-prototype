#!/usr/bin/env python3
"""
Database initialization script for Insurance CRM
Creates tables, admin user, and sample data
"""

from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from auth_utils import get_password_hash
from datetime import datetime

def create_admin_user(db: Session):
    """Create default admin user"""
    
    # Check if admin user already exists
    admin_user = db.query(models.User).filter(models.User.username == "admin").first()
    if admin_user:
        print("Admin user already exists")
        return admin_user
    
    # Create admin user
    admin = models.User(
        username="admin",
        email="admin@asiainc.co",
        full_name="System Administrator",
        role=models.UserRole.ADMIN,
        hashed_password=get_password_hash("admin123"),
        is_active=True
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"Created admin user: {admin.username} (password: admin123)")
    return admin

def create_sample_agent(db: Session):
    """Create sample agent user"""
    
    # Check if agent user already exists
    agent_user = db.query(models.User).filter(models.User.username == "agent1").first()
    if agent_user:
        print("Sample agent already exists")
        return agent_user
    
    # Create agent user
    agent = models.User(
        username="agent1",
        email="agent@asiainc.co",
        full_name="John Smith",
        role=models.UserRole.AGENT,
        hashed_password=get_password_hash("agent123"),
        is_active=True
    )
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    print(f"Created agent user: {agent.username} (password: agent123)")
    return agent

def create_sample_leads(db: Session, agent: models.User):
    """Create sample leads for testing"""
    
    # Check if sample leads already exist
    existing_leads = db.query(models.Lead).count()
    if existing_leads > 0:
        print(f"Found {existing_leads} existing leads, skipping sample data creation")
        return
    
    sample_leads = [
        {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@email.com",
            "phone_number": "(555) 123-4567",
            "address_line1": "123 Oak Street",
            "city": "Sacramento",
            "state": "CA",
            "zip_code": "95814",
            "personal_lines": True,
            "commercial_lines": False,
            "life_and_health": False,
            "status": models.LeadStatus.NEW,
            "source": models.LeadSource.WEBSITE,
            "assigned_agent_id": agent.id,
            "priority": 2,
            "estimated_value": 2500.00
        },
        {
            "first_name": "Michael",
            "last_name": "Davis",
            "email": "michael.davis@email.com",
            "phone_number": "(555) 987-6543",
            "address_line1": "456 Pine Avenue",
            "city": "Roseville",
            "state": "CA",
            "zip_code": "95661",
            "personal_lines": False,
            "commercial_lines": True,
            "life_and_health": False,
            "status": models.LeadStatus.CONTACTED,
            "source": models.LeadSource.REFERRAL,
            "assigned_agent_id": agent.id,
            "priority": 3,
            "estimated_value": 5000.00
        },
        {
            "first_name": "Emily",
            "last_name": "Rodriguez",
            "email": "emily.rodriguez@email.com",
            "phone_number": "(555) 555-0123",
            "address_line1": "789 Maple Drive",
            "city": "Folsom",
            "state": "CA",
            "zip_code": "95630",
            "personal_lines": True,
            "commercial_lines": False,
            "life_and_health": True,
            "status": models.LeadStatus.QUALIFIED,
            "source": models.LeadSource.WEBSITE,
            "assigned_agent_id": agent.id,
            "priority": 2,
            "estimated_value": 3000.00
        }
    ]
    
    created_leads = []
    for lead_data in sample_leads:
        lead = models.Lead(**lead_data)
        db.add(lead)
        created_leads.append(lead)
    
    db.commit()
    
    print(f"Created {len(created_leads)} sample leads")
    return created_leads

def create_sample_activities(db: Session, leads, agent: models.User):
    """Create sample activities for the leads"""
    
    if not leads:
        return
    
    # Add initial activity for each lead
    activities = [
        {
            "lead_id": leads[0].id,
            "user_id": agent.id,
            "activity_type": models.ActivityType.NOTE,
            "title": "Initial Contact",
            "description": "Lead submitted quote request via website. Interested in auto and home insurance.",
            "created_at": datetime.utcnow()
        },
        {
            "lead_id": leads[1].id,
            "user_id": agent.id,
            "activity_type": models.ActivityType.CALL,
            "title": "Follow-up Call",
            "description": "Called to discuss commercial insurance needs. Scheduled meeting for next week.",
            "duration_minutes": 15,
            "outcome": "Positive - scheduled meeting",
            "created_at": datetime.utcnow()
        },
        {
            "lead_id": leads[2].id,
            "user_id": agent.id,
            "activity_type": models.ActivityType.EMAIL,
            "title": "Quote Sent",
            "description": "Sent personalized quote for auto, home, and life insurance packages.",
            "outcome": "Quote delivered successfully",
            "created_at": datetime.utcnow()
        }
    ]
    
    for activity_data in activities:
        activity = models.Activity(**activity_data)
        db.add(activity)
    
    db.commit()
    print(f"Created {len(activities)} sample activities")

def create_email_templates(db: Session):
    """Create default email templates"""
    
    templates = [
        {
            "name": "Welcome Email",
            "subject": "Thank you for your insurance quote request",
            "body": """Dear {first_name} {last_name},

Thank you for requesting an insurance quote from A.S.I.A Inc. We have received your information and one of our experienced agents will contact you within 24 hours to discuss your insurance needs.

What happens next:
1. Our team will review your information
2. We'll prepare personalized quotes based on your needs
3. An agent will contact you to discuss your options
4. We'll help you find the best coverage at competitive rates

Our office hours:
Monday - Friday: 9am - 5pm
Saturday - Sunday: by appointment only

Contact Information:
Phone: 916-772-4006
Email: TEAM@ASIAINC.CO
Address: 3017 Douglas Blvd STE 140, Roseville, CA 95661

We look forward to serving you!

Best regards,
The A.S.I.A Inc Team
CA License #6009368""",
            "template_type": "welcome",
            "is_active": True
        },
        {
            "name": "Follow-up Reminder",
            "subject": "Following up on your insurance quote",
            "body": """Dear {first_name} {last_name},

I hope this email finds you well. I wanted to follow up on the insurance quote we discussed recently.

Have you had a chance to review the information we provided? I'm here to answer any questions you might have and help you find the best insurance solution for your needs.

Please feel free to call me at 916-772-4006 or reply to this email. I'm available to discuss your options at your convenience.

Best regards,
{agent_name}
A.S.I.A Inc
CA License #6009368""",
            "template_type": "follow_up",
            "is_active": True
        }
    ]
    
    existing_templates = db.query(models.EmailTemplate).count()
    if existing_templates > 0:
        print(f"Found {existing_templates} existing email templates, skipping creation")
        return
    
    for template_data in templates:
        template = models.EmailTemplate(**template_data)
        db.add(template)
    
    db.commit()
    print(f"Created {len(templates)} email templates")

def init_database():
    """Initialize the database with tables and sample data"""
    
    print("Initializing Insurance CRM Database...")
    
    # Create all tables
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create users
        admin = create_admin_user(db)
        agent = create_sample_agent(db)
        
        # Create sample data
        leads = create_sample_leads(db, agent)
        create_sample_activities(db, leads, agent)
        create_email_templates(db)
        
        print("\\nDatabase initialization completed successfully!")
        print("\\nLogin credentials:")
        print("Admin - Username: admin, Password: admin123")
        print("Agent - Username: agent1, Password: agent123")
        print("\\nYou can now start the API server with: uvicorn main:app --reload")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()