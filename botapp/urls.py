from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('get-chat-content/', views.get_chat_content, name='get_chat_content'),
    path('test-email/', views.test_email, name='test_email'),
]