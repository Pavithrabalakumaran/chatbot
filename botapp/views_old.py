import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decouple import config
import random
import re

# ===== CONFIGURATION =====
# Get your free API key from: https://makersuite.google.com/app/apikey

GEMINI_API_KEY = config('GEMINI_API_KEY')
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# Context storage (use Redis/DB in production)
conversation_contexts = {}

# ===== MAIN CHAT VIEW =====

def home(request):
    """Serve the homepage with base.html"""
    return render(request, 'base.html')


def chat_api(request):
    """Main chat endpoint with Gemini AI"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)
            
            # Get or create session
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            
            # Initialize conversation context
            if session_id not in conversation_contexts:
                conversation_contexts[session_id] = []
            
            conversation_contexts[session_id].append(user_message)
            
            # Keep only last 5 messages for context
            if len(conversation_contexts[session_id]) > 5:
                conversation_contexts[session_id] = conversation_contexts[session_id][-5:]
            
            # Get AI response
            context_messages = conversation_contexts[session_id]
            ai_response = get_gemini_response(user_message, context_messages)
            
            if ai_response:
                response_text = enhance_response_with_pricing(ai_response, user_message)
            else:
                # Fallback to enhanced local response
                response_text = get_enhanced_local_response(user_message, context_messages)
            
            return JsonResponse({'response': response_text})
            
        except Exception as e:
            print(f"Chat Error: {e}")
            # Always provide fallback
            fallback_message = data.get('message', '') if 'data' in locals() else ''
            return JsonResponse({
                'response': get_enhanced_local_response(fallback_message, [])
            })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_gemini_response(message, context):
    """Get natural response from Google Gemini API"""
    try:
        # Build conversation history for context
        print(f"🔍 Calling Gemini API for: {message}")
        print(f"🔑 API Key exists: {bool(GEMINI_API_KEY)}")
        print(f"🔑 API Key starts with: {GEMINI_API_KEY[:20]}...")

        conversation_history = ""
        if len(context) > 1:
            conversation_history = "Recent conversation:\n"
            for i, msg in enumerate(context[:-1]):
                conversation_history += f"User: {msg}\n"
        
        # Create the prompt with personality
        prompt = f"""You are Sarah, a friendly, enthusiastic digital marketing expert chatting with a potential client. 

Your personality:
- Warm, conversational, and approachable (like texting a friend)
- Passionate about helping businesses grow
- Use casual language ("honestly", "look", "here's the thing")
- Occasionally use emojis naturally (but don't overdo it)
- Keep responses 2-4 short paragraphs max
- Be helpful and specific, not generic

Your services & pricing:
- SEO: $299/month (keyword research, optimization, content, reports)
- Social Media: $199/month (3-5 platforms, daily posts, engagement)
- PPC/Ads: $399/month + ad budget (campaign management, optimization)
- Content: $249/month (4 blog posts, SEO optimized)
- Email: $199/month (campaigns, automation, design)

Guidelines:
- Only mention pricing if asked or highly relevant
- Ask follow-up questions to understand their needs
- Be conversational, not salesy
- Vary your responses (don't use same phrases repeatedly)
- Show genuine interest in their business

{conversation_history}

Current message from user: {message}

Respond as Sarah would - naturally, helpfully, and conversationally:"""

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.9,  # More creative/varied responses
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 500,
            }
        }
        
        response = requests.post(
            GEMINI_API_URL, 
            json=payload, 
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📡 Response Body: {response.text[:200]}")
        

        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                return generated_text.strip()
        else:
            print(f"Gemini API Error: {response.status_code} - {response.text}")
            return None
        
        return None
        
    except requests.exceptions.Timeout:
        print("Gemini API Timeout")
        return None
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None


def enhance_response_with_pricing(response, user_message):
    """Add pricing details if relevant but not already included"""
    lower_msg = user_message.lower()
    
    # Check if pricing already mentioned
    if '$' in response or 'month' in response.lower():
        return response
    
    # Add pricing only if specifically asked
    pricing_addition = ""
    
    if 'how much' in lower_msg or 'price' in lower_msg or 'cost' in lower_msg:
        if 'seo' in lower_msg:
            pricing_addition = "\n\n💰 SEO starts at $299/month with everything included!"
        elif 'social' in lower_msg:
            pricing_addition = "\n\n💰 Social media is $199/month for 3-5 platforms!"
        elif 'ppc' in lower_msg or 'ad' in lower_msg:
            pricing_addition = "\n\n💰 PPC management is $399/month + your ad budget!"
        elif 'content' in lower_msg or 'blog' in lower_msg:
            pricing_addition = "\n\n💰 Content packages start at $249/month for 4 posts!"
        elif 'email' in lower_msg:
            pricing_addition = "\n\n💰 Email marketing is $199/month!"
    
    return response + pricing_addition


def get_enhanced_local_response(message, context):
    """Enhanced fallback responses when API is unavailable"""
    lower_msg = message.lower().strip()
    
    # Greetings
    if re.match(r'^(hi|hello|hey|sup|yo)', lower_msg):
        responses = [
            "Hey there! Thanks for chatting with me! I'm Sarah, and I help businesses grow online through smart digital marketing. What's on your mind today?",
            "Hi! Great to meet you! I'm Sarah, your friendly marketing expert. Whether it's SEO, social media, or ads - I've got you covered. What can I help with?",
            "Hello! I'm Sarah! I love helping businesses succeed with digital marketing. No question is too big or small - what would you like to know?",
        ]
        return random.choice(responses)
    
    # Thanks
    if any(word in lower_msg for word in ['thank', 'thanks', 'appreciate']):
        responses = [
            "You're so welcome! Happy to help anytime. Got any other questions?",
            "Of course! That's what I'm here for! Feel free to ask anything else!",
            "Anytime! This is what I love doing. Don't hesitate if you need anything else!",
        ]
        return random.choice(responses)
    
    # About Sarah
    if 'about you' in lower_msg or 'who are you' in lower_msg:
        return """Thanks for asking! I'm Sarah, and I'm basically obsessed with digital marketing. I've been doing this for years and still get excited when I see a client's rankings jump!

I believe marketing should be authentic, results-driven, and actually fun to work on. No boring corporate stuff here!

But enough about me - tell me about YOUR business! What do you do?"""
    
    # Pricing
    if 'price' in lower_msg or 'cost' in lower_msg or 'how much' in lower_msg:
        return """Let's talk pricing! Here's the breakdown:

🔍 SEO - $299/month (keyword research, optimization, content, reports)
📱 Social Media - $199/month (3-5 platforms, daily management)
💰 PPC/Ads - $399/month + ad budget (full campaign management)
📝 Content - $249/month (4 blog posts, SEO optimized)
📧 Email - $199/month (campaigns, automation, design)

Most businesses bundle 2-3 services for better results. What's most important to you right now?"""
    
    # Services
    if 'what do you do' in lower_msg or 'services' in lower_msg:
        return """Great question! I help businesses get noticed online and turn that attention into customers!

Here's what I do:
🔍 SEO - Get you ranking on Google
📱 Social Media - Build your brand presence
💰 Paid Ads - Run campaigns that convert
📝 Content - Create engaging blogs and posts
📧 Email - Build customer relationships

Most businesses start with 2-3 of these. What sounds most useful for you?"""
    
    # SEO
    if 'seo' in lower_msg:
        return """SEO is one of my favorites! It's about making Google fall in love with your website so you show up when people search for what you offer.

We do keyword research, optimize your site for speed, create quality content, and build your authority. It takes 3-6 months to see big results, but then that traffic keeps coming without paying for ads!

What industry are you in? I'd love to share what keywords might work for you!"""
    
    # Social Media
    if 'social' in lower_msg:
        return """Social media is where you get to show your brand's personality! It's not about posting constantly - it's about consistent, engaging content.

We create posts that stop the scroll, engage with your followers authentically, and build a real community. Which platforms are you most active on?"""
    
    # Default
    return f"""Let me make sure I understand what you need!

You asked: "{message}"

I help businesses with:
🔍 SEO - Getting found on Google
📱 Social Media - Instagram, Facebook, LinkedIn
💰 Paid Ads - Google & Facebook Ads
📝 Content - Blogs and posts
📧 Email - Campaigns and automation

Could you tell me more about what you're trying to achieve? What's your biggest marketing challenge right now?"""


def get_chat_content(request):
    """Serve the chat interface HTML"""
    return render(request, 'marketing_chat.html')