import re
from django.utils import timezone
from .models import ChatSession, Lead, FAQ

def get_or_create_chat_session(request):
    """
    Get or create a chat session for the current user/request.
    """
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    # Try to get existing active session
    chat_session = ChatSession.objects.filter(
        session_id=session_key,
        is_active=True
    ).first()
    
    if not chat_session:
        # Create new session
        chat_session = ChatSession.objects.create(
            session_id=session_key,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    
    return chat_session

def get_client_ip(request):
    """
    Get the client's IP address from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def extract_contact_info(message):
    """
    Extract potential contact information from a message.
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'(\+?\d{1,4}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    emails = re.findall(email_pattern, message)
    phones = re.findall(phone_pattern, message)
    
    return {
        'emails': emails,
        'phones': phones
    }

def identify_service_interest(message):
    """
    Identify which service the user is most interested in based on their message.
    """
    message_lower = message.lower()
    
    service_keywords = {
        'seo': ['seo', 'search engine', 'ranking', 'google', 'organic'],
        'social': ['social media', 'facebook', 'instagram', 'twitter', 'linkedin', 'social'],
        'ppc': ['ppc', 'ads', 'advertising', 'google ads', 'facebook ads', 'pay per click'],
        'content': ['content', 'blog', 'writing', 'articles', 'copywriting'],
        'email': ['email', 'newsletter', 'email marketing', 'mailchimp']
    }
    
    for service, keywords in service_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            return service
    
    return 'multiple'  # If multiple or unclear

def extract_budget_range(message):
    """
    Extract budget information from user message.
    """
    message_lower = message.lower()
    
    # Common budget patterns
    budget_patterns = [
        (r'\$(\d+)[-\s]*(\d+)?k?', 'budget_range'),
        (r'(\d+)[-\s]*(\d+)?\s*dollars?', 'budget_range'),
        (r'under\s*\$?(\d+)', 'under'),
        (r'less\s*than\s*\$?(\d+)', 'under'),
        (r'around\s*\$?(\d+)', 'around'),
        (r'about\s*\$?(\d+)', 'around'),
    ]
    
    for pattern, type_match in budget_patterns:
        match = re.search(pattern, message_lower)
        if match:
            return match.group(0)
    
    # Check for common budget ranges
    if any(phrase in message_lower for phrase in ['small budget', 'tight budget', 'limited budget']):
        return 'Under $500/month'
    elif any(phrase in message_lower for phrase in ['medium budget', 'moderate budget']):
        return '$500-$2000/month'
    elif any(phrase in message_lower for phrase in ['large budget', 'big budget', 'substantial budget']):
        return '$2000+/month'
    
    return ''

def create_lead_from_message(chat_session, message, contact_info=None):
    """
    Create a lead from a chat message if it contains contact information or shows strong interest.
    """
    service_interest = identify_service_interest(message)
    budget_range = extract_budget_range(message)
    
    if not contact_info:
        contact_info = extract_contact_info(message)
    
    # Only create lead if we have contact info or strong buying signals
    buying_signals = ['quote', 'pricing', 'get started', 'contact', 'call me', 'email me']
    has_buying_signal = any(signal in message.lower() for signal in buying_signals)
    
    if contact_info['emails'] or contact_info['phones'] or has_buying_signal:
        lead = Lead.objects.create(
            email=contact_info['emails'][0] if contact_info['emails'] else '',
            phone=contact_info['phones'][0] if contact_info['phones'] else '',
            service_interest=service_interest,
            budget_range=budget_range,
            message=message,
            source='chat',
            chat_session=chat_session
        )
        return lead
    
    return None

def get_faq_response(message):
    """
    Check if the message matches any FAQ entries.
    """
    message_lower = message.lower()
    
    # Get active FAQs
    faqs = FAQ.objects.filter(is_active=True)
    
    for faq in faqs:
        keywords = [k.strip().lower() for k in faq.keywords.split(',')]
        if any(keyword in message_lower for keyword in keywords):
            return faq.answer
    
    return None

def calculate_session_analytics():
    """
    Calculate and update daily analytics.
    """
    today = timezone.now().date()
    
    # Get today's sessions
    today_sessions = ChatSession.objects.filter(started_at__date=today)
    total_sessions = today_sessions.count()
    
    if total_sessions == 0:
        return
    
    # Calculate metrics
    total_messages = sum(session.messages.count() for session in today_sessions)
    
    # Calculate average session length
    completed_sessions = today_sessions.filter(ended_at__isnull=False)
    if completed_sessions.exists():
        total_duration = sum(
            (session.ended_at - session.started_at).total_seconds() / 60
            for session in completed_sessions
        )
        avg_session_length = total_duration / completed_sessions.count()
    else:
        avg_session_length = 0.0
    
    # Count leads generated today
    leads_generated = Lead.objects.filter(created_at__date=today).count()
    
    # Calculate conversion rate
    conversion_rate = (leads_generated / total_sessions * 100) if total_sessions > 0 else 0.0
    
    # Update or create analytics record
    from .models import ChatAnalytics
    analytics, created = ChatAnalytics.objects.update_or_create(
        date=today,
        defaults={
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'avg_session_length': round(avg_session_length, 2),
            'leads_generated': leads_generated,
            'conversion_rate': round(conversion_rate, 2)
        }
    )
    
    return analytics