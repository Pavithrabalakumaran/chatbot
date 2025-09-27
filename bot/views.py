

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import uuid
import re
from .models import Conversation, Message, PredefinedQuestion

class ChatbotView(View):
    def get(self, request):
        return render(request, 'chatbot/base.html')

@method_decorator(csrf_exempt, name='dispatch')
class ChatAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id', str(uuid.uuid4()))
            
            # Get or create conversation
            conversation, created = Conversation.objects.get_or_create(
                session_id=session_id,
                defaults={'user': request.user if request.user.is_authenticated else None}
            )
            
            # Save user message
            Message.objects.create(
                conversation=conversation,
                content=user_message,
                is_user=True
            )
            
            # Generate bot response
            bot_response = self.get_bot_response(user_message)
            
            # Save bot response
            Message.objects.create(
                conversation=conversation,
                content=bot_response,
                is_user=False
            )
            
            return JsonResponse({
                'response': bot_response,
                'session_id': session_id,
                'status': 'success'
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=400)
    
    def get_bot_response(self, user_message):
        """Generate bot response based on user message"""
        user_message_lower = user_message.lower()
        
        # Check for predefined questions
        predefined_questions = PredefinedQuestion.objects.filter(is_active=True)
        
        best_match = None
        max_score = 0
        
        for question in predefined_questions:
            score = self.calculate_match_score(user_message_lower, question)
            if score > max_score and score > 0.3:  # Minimum threshold
                max_score = score
                best_match = question
        
        if best_match:
            return best_match.answer
        
        # Default responses for common patterns
        return self.get_default_response(user_message_lower)
    
    def calculate_match_score(self, user_message, question):
        """Calculate how well user message matches a predefined question"""
        keywords = question.get_keywords_list()
        question_text = question.question.lower()
        
        # Check exact question match
        if user_message in question_text or question_text in user_message:
            return 1.0
        
        # Check keyword matches
        matched_keywords = 0
        for keyword in keywords:
            if keyword in user_message:
                matched_keywords += 1
        
        if len(keywords) > 0:
            keyword_score = matched_keywords / len(keywords)
        else:
            keyword_score = 0
        
        # Check word overlap
        user_words = set(user_message.split())
        question_words = set(question_text.split())
        common_words = user_words.intersection(question_words)
        
        if len(question_words) > 0:
            word_score = len(common_words) / len(question_words)
        else:
            word_score = 0
        
        # Combine scores
        return (keyword_score * 0.6) + (word_score * 0.4)
    
    def get_default_response(self, user_message):
        """Return default responses for common patterns"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        goodbyes = ['bye', 'goodbye', 'see you', 'farewell', 'exit']
        thanks = ['thank', 'thanks', 'appreciate']
        
        if any(greeting in user_message for greeting in greetings):
            return "Hello! How can I help you today? You can ask me about our services, products, or any general questions."
        
        if any(goodbye in user_message for goodbye in goodbyes):
            return "Goodbye! Thank you for chatting with me. Have a great day!"
        
        if any(thank in user_message for thank in thanks):
            return "You're welcome! Is there anything else I can help you with?"
        
        if '?' in user_message:
            return "I'm not sure about that specific question. Could you try rephrasing it or ask about something else? I'm here to help!"
        
        return "I understand you're trying to tell me something, but I'm not sure how to respond to that. Could you ask me a specific question?"

class ConversationHistoryView(View):
    def get(self, request, session_id):
        try:
            conversation = Conversation.objects.get(session_id=session_id)
            messages = conversation.messages.all()
            
            messages_data = [{
                'content': msg.content,
                'is_user': msg.is_user,
                'timestamp': msg.timestamp.isoformat()
            } for msg in messages]
            
            return JsonResponse({
                'messages': messages_data,
                'status': 'success'
            })
            
        except Conversation.DoesNotExist:
            return JsonResponse({
                'messages': [],
                'status': 'success'
            })