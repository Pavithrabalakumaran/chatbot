from django.urls import path
from . import views

urlpatterns = [
    path('', views.ChatbotView.as_view(), name='chatbot'),
    path('api/chat/', views.ChatAPIView.as_view(), name='chat_api'),
    path('api/history/<str:session_id>/', views.ConversationHistoryView.as_view(), name='conversation_history'),
]