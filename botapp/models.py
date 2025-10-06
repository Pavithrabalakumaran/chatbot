from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone





class ChatSession(models.Model):
    """
    Model to store chat sessions for analytics and history.
    """
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = "Chat Session"
        verbose_name_plural = "Chat Sessions"
    
    def __str__(self):
        return f"Session {self.session_id} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"

class ChatMessage(models.Model):
    """
    Model to store individual chat messages.
    """
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('bot', 'Bot Response'),
        ('system', 'System Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_helpful = models.BooleanField(null=True, blank=True)  # User feedback
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
    
    def __str__(self):
        return f"{self.message_type.title()}: {self.content[:50]}..."

class Lead(models.Model):
    """
    Model to capture potential leads from chat interactions.
    """
    LEAD_SOURCES = [
        ('chat', 'Chat Bot'),
        ('form', 'Contact Form'),
        ('phone', 'Phone Call'),
        ('email', 'Email'),
    ]
    
    SERVICES_INTERESTED = [
        ('seo', 'SEO Services'),
        ('social', 'Social Media Marketing'),
        ('ppc', 'PPC Advertising'),
        ('content', 'Content Marketing'),
        ('email', 'Email Marketing'),
        ('multiple', 'Multiple Services'),
    ]
    
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    service_interest = models.CharField(max_length=20, choices=SERVICES_INTERESTED, blank=True)
    budget_range = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    source = models.CharField(max_length=10, choices=LEAD_SOURCES, default='chat')
    chat_session = models.ForeignKey(ChatSession, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    contacted = models.BooleanField(default=False)
    converted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
    
    def __str__(self):
        return f"{self.name or 'Anonymous'} - {self.email or 'No Email'} ({self.service_interest})"

class ChatAnalytics(models.Model):
    """
    Model to store chat analytics and metrics.
    """
    date = models.DateField(unique=True, default=timezone.now)
    total_sessions = models.IntegerField(default=0)
    total_messages = models.IntegerField(default=0)
    avg_session_length = models.FloatField(default=0.0)  # in minutes
    leads_generated = models.IntegerField(default=0)
    most_asked_topic = models.CharField(max_length=100, blank=True)
    conversion_rate = models.FloatField(default=0.0)  # percentage
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Chat Analytics"
        verbose_name_plural = "Chat Analytics"
    
    def __str__(self):
        return f"Analytics for {self.date}"

class FAQ(models.Model):
    """
    Model to store frequently asked questions for chatbot training.
    """
    CATEGORIES = [
        ('pricing', 'Pricing'),
        ('services', 'Services'),
        ('process', 'Process'),
        ('technical', 'Technical'),
        ('general', 'General'),
    ]
    
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    keywords = models.CharField(max_length=200, help_text="Comma-separated keywords for matching")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return f"{self.category.title()}: {self.question}"
