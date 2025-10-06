from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Conversation {self.session_id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_user = models.BooleanField(default=True)  # True for user, False for bot
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        sender = "User" if self.is_user else "Bot"
        return f"{sender}: {self.content[:50]}..."

class PredefinedQuestion(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    keywords = models.CharField(max_length=300, help_text="Comma-separated keywords for matching")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.question

    def get_keywords_list(self):
        return [keyword.strip().lower() for keyword in self.keywords.split(',')]