import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config
import logging

# Email configuration
SMTP_HOST = config('SMTP_HOST', default='smtp.gmail.com')
SMTP_PORT = int(config('SMTP_PORT', default=587))
SMTP_USER = config('SMTP_USER', default='')
SMTP_PASSWORD = config('SMTP_PASSWORD', default='')
FROM_EMAIL = config('FROM_EMAIL', default='')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str, is_html: bool = False):
    """Send an email"""
    try:
        if not SMTP_USER or not SMTP_PASSWORD:
            logger.warning("Email configuration not set. Skipping email send.")
            return False
            
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def send_new_lead_notification(email: str, first_name: str, last_name: str):
    """Send welcome email to new leads"""
    subject = "Thank you for your insurance quote request"
    
    body = f"""
    Dear {first_name} {last_name},

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
    CA License #6009368
    """
    
    return send_email(email, subject, body)

def send_agent_new_lead_alert(agent_email: str, lead_name: str, lead_email: str, interests: list):
    """Send alert to agent about new lead assignment"""
    subject = f"New Lead Assigned: {lead_name}"
    
    interests_text = ", ".join(interests) if interests else "Not specified"
    
    body = f"""
    You have been assigned a new lead:

    Name: {lead_name}
    Email: {lead_email}
    Interests: {interests_text}

    Please log into the CRM to view full details and follow up with this lead.

    CRM Dashboard: {config('FRONTEND_URL', default='http://localhost:5173')}/dashboard

    Best regards,
    A.S.I.A Inc CRM System
    """
    
    return send_email(agent_email, subject, body)

def send_follow_up_reminder(agent_email: str, agent_name: str, lead_name: str, lead_email: str):
    """Send follow-up reminder to agent"""
    subject = f"Follow-up Reminder: {lead_name}"
    
    body = f"""
    Hi {agent_name},

    This is a reminder that you have a follow-up scheduled for:

    Lead: {lead_name}
    Email: {lead_email}

    Please log into the CRM to view full details and update the lead status.

    CRM Dashboard: {config('FRONTEND_URL', default='http://localhost:5173')}/dashboard

    Best regards,
    A.S.I.A Inc CRM System
    """
    
    return send_email(agent_email, subject, body)