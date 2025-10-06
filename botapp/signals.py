from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ChatMessage, ChatSession, ChatAnalytics, Lead
import uuid

@receiver(pre_save, sender=ChatSession)
def generate_session_id(sender, instance, **kwargs):
    """
    Generate a unique session ID for new chat sessions.
    """
    if not instance.session_id:
        instance.session_id = str(uuid.uuid4())[:8]  # Short UUID

@receiver(post_save, sender=ChatMessage)
def update_session_activity(sender, instance, created, **kwargs):
    """
    Update session activity when a new message is added.
    """
    if created:
        session = instance.session
        session.is_active = True
        session.save(update_fields=['is_active'])

@receiver(post_save, sender=Lead)
def update_analytics_on_lead(sender, instance, created, **kwargs):
    """
    Update daily analytics when a new lead is created.
    """
    if created:
        today = timezone.now().date()
        analytics, created_analytics = ChatAnalytics.objects.get_or_create(
            date=today,
            defaults={
                'total_sessions': 0,
                'total_messages': 0,
                'leads_generated': 0,
                'conversion_rate': 0.0
            }
        )
        analytics.leads_generated += 1
        analytics.save(update_fields=['leads_generated'])