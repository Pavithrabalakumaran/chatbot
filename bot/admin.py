from django.contrib import admin
from .models import Conversation, Message, PredefinedQuestion

@admin.register(PredefinedQuestion)
class PredefinedQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('question', 'keywords')
    
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = ('session_id', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'is_user', 'content', 'timestamp')
    list_filter = ('is_user', 'timestamp')
    readonly_fields = ('timestamp',)