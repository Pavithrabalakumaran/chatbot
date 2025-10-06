from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import ChatSession, ChatMessage, Lead, ChatAnalytics, FAQ

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user_display', 'ip_address', 'started_at', 'duration', 'message_count', 'is_active']
    list_filter = ['is_active', 'started_at', 'ended_at']
    search_fields = ['session_id', 'user__username', 'ip_address']
    readonly_fields = ['session_id', 'started_at', 'message_count', 'duration']
    date_hierarchy = 'started_at'
    
    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return "Anonymous"
    user_display.short_description = "User"
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Messages"
    
    def duration(self, obj):
        if obj.ended_at:
            delta = obj.ended_at - obj.started_at
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes} min"
        elif obj.is_active:
            delta = timezone.now() - obj.started_at
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes} min (active)"
        return "Unknown"
    duration.short_description = "Duration"

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp']
    fields = ['message_type', 'content', 'timestamp', 'is_helpful']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp', 'is_helpful']
    list_filter = ['message_type', 'timestamp', 'is_helpful']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = "Content Preview"

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'service_interest', 'budget_range', 'source', 'created_at', 'contacted', 'converted']
    list_filter = ['service_interest', 'source', 'contacted', 'converted', 'created_at']
    search_fields = ['name', 'email', 'company', 'website']
    readonly_fields = ['created_at', 'chat_session']
    date_hierarchy = 'created_at'
    actions = ['mark_as_contacted', 'mark_as_converted']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company', 'website')
        }),
        ('Lead Details', {
            'fields': ('service_interest', 'budget_range', 'message', 'source', 'chat_session')
        }),
        ('Status', {
            'fields': ('contacted', 'converted', 'created_at')
        }),
    )
    
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(contacted=True)
        self.message_user(request, f'{updated} leads marked as contacted.')
    mark_as_contacted.short_description = "Mark selected leads as contacted"
    
    def mark_as_converted(self, request, queryset):
        updated = queryset.update(converted=True, contacted=True)
        self.message_user(request, f'{updated} leads marked as converted.')
    mark_as_converted.short_description = "Mark selected leads as converted"

@admin.register(ChatAnalytics)
class ChatAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_sessions', 'total_messages', 'avg_session_length', 'leads_generated', 'conversion_rate']
    list_filter = ['date']
    readonly_fields = ['date']
    date_hierarchy = 'date'
    
    def has_add_permission(self, request):
        # Analytics should be auto-generated, not manually added
        return False

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'keywords_preview', 'is_active', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'keywords']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Matching', {
            'fields': ('keywords', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def keywords_preview(self, obj):
        return obj.keywords[:50] + "..." if len(obj.keywords) > 50 else obj.keywords
    keywords_preview.short_description = "Keywords"

# Customize admin site
admin.site.site_header = "Digital Marketing Chatbot Admin"
admin.site.site_title = "Chatbot Admin"
admin.site.index_title = "Welcome to Chatbot Administration"