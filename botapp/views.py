import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from decouple import config
import random
import re
from datetime import datetime

# ===== CONFIGURATION =====
GEMINI_API_KEY = config('GEMINI_API_KEY')

# CORRECT MODEL: gemini-2.5-flash
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=AIzaSyDEjTHtbo8VRh3GIX5hOsSfeeQgB1EAmwM"

# DEBUG: Print the actual URL being used
print(f"🔧 DEBUG: GEMINI_API_URL = {GEMINI_API_URL}")

# Context storage (use Redis/DB in production)
conversation_contexts = {}
contact_form_data = {}

# ===== MAIN CHAT VIEW =====
def home(request):
    """Serve the homepage with base.html"""
    return render(request, 'base.html')

def test_email(request):
    """Test if email is working"""
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        send_mail(
            'Test Email from Django',
            'This is a test email. If you receive this, email is configured correctly.',
            settings.EMAIL_HOST_USER,
            [settings.NOTIFICATION_EMAIL],
            fail_silently=False,
        )
        return JsonResponse({'message': 'Email sent successfully!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
            
            # Check if user is in contact form flow
            if session_id in contact_form_data:
                response_text = handle_contact_form(session_id, user_message)
                return JsonResponse({
                    'response': response_text,
                    'source': 'contact_form'
                })
            
            # Check if user wants to contact
            contact_keywords = ['contact', 'call me', 'phone', 'reach out', 'get in touch', 'schedule', 'book a call']
            if any(keyword in user_message.lower() for keyword in contact_keywords):
                # Start contact form flow
                contact_form_data[session_id] = {'step': 'name'}
                response_text = """Great! I'd love to connect you with our team! 📞

Let me collect a few quick details:

**What's your name?**"""
                return JsonResponse({
                    'response': response_text,
                    'source': 'contact_form'
                })
            
            # Normal AI chat flow
            context_messages = conversation_contexts[session_id]
            ai_response = get_gemini_response(user_message, context_messages)
            
            if ai_response:
                response_text = enhance_response_with_pricing(ai_response, user_message)
                print(f"✅ Gemini Response: {response_text[:100]}...")
            else:
                print("⚠️ Using fallback response")
                response_text = get_enhanced_local_response(user_message, context_messages)
            
            return JsonResponse({
                'response': response_text,
                'source': 'gemini' if ai_response else 'local'
            })
            
        except Exception as e:
            print(f"❌ Chat Error: {e}")
            fallback_message = data.get('message', '') if 'data' in locals() else ''
            return JsonResponse({
                'response': get_enhanced_local_response(fallback_message, []),
                'source': 'fallback'
            })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def handle_contact_form(session_id, user_input):
    """Handle multi-step contact form collection"""
    form_data = contact_form_data[session_id]
    current_step = form_data.get('step')
    
    if current_step == 'name':
        form_data['name'] = user_input
        form_data['step'] = 'phone'
        return f"Nice to meet you, {user_input}! 👋\n\n**What's your phone number?**"
    
    elif current_step == 'phone':
        form_data['phone'] = user_input
        form_data['step'] = 'email'
        return "Perfect! 📱\n\n**What's your email address?**"
    
    elif current_step == 'email':
        form_data['email'] = user_input
        form_data['step'] = 'reason'
        return "Got it! ✉️\n\n**What would you like to discuss?** (e.g., SEO, Social Media, Website Design, General inquiry)"
    
    elif current_step == 'reason':
        form_data['reason'] = user_input
        form_data['step'] = 'budget'
        return """Great! One more thing... 💰\n\n**What's your expected budget/price range for this project?**\n\n(e.g., ₹10,000-₹20,000, ₹50,000+, or "flexible")\n\n💡 Note: We offer the best prices in the market and are always negotiable - all our clients are unique!"""
    
    elif current_step == 'budget':
        form_data['budget'] = user_input

        print(f"🔍 DEBUG: About to send email with data: {form_data}")

        # Send email notification with all collected data
        email_sent = send_detailed_contact_notification(form_data, session_id)
    
        print(f"📧 Email send result: {email_sent}")
        
        # Send email notification with all collected data
        send_detailed_contact_notification(form_data, session_id)
        
        # Clean up form data
        del contact_form_data[session_id]
        
        return f"""Thank you so much, {form_data['name']}! 🎉

I've sent your information to our team. Someone will reach out to you within 24 hours at:
📧 {form_data['email']}
📱 {form_data['phone']}

💼 **Remember:** We pride ourselves on offering the best prices in the market, and we're completely flexible with our pricing because we understand every client has unique needs!

In the meantime, feel free to ask me any questions about our services! Is there anything else I can help you with?"""
    
    return "Something went wrong. Let's start over. Type 'contact' to try again."


def send_detailed_contact_notification(form_data, session_id):
    """Send detailed email notification with form data"""
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f"🔔 New Contact Request: {form_data['name']}"
        
        message = f"""
New Contact Request from Chatbot:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Name: {form_data['name']}
📱 Phone: {form_data['phone']}
📧 Email: {form_data['email']}
💬 Enquiry: {form_data['reason']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session ID: {session_id}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please follow up with this lead within 24 hours.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.NOTIFICATION_EMAIL],
            fail_silently=False,
        )
        print(f"📧 Detailed contact notification sent: {form_data['name']} - {form_data['email']}")
        return True
    except Exception as e:
        print(f"❌ Email notification failed: {e}")
        return False
    

 


def get_gemini_response(message, context):
    """Get natural response from Google Gemini API"""
    try:
        conversation_history = ""
        if len(context) > 1:
            conversation_history = "Recent conversation:\n"
            for msg in context[:-1]:
                conversation_history += f"User: {msg}\n"
        
        prompt = f"""You are Sarah, a friendly, enthusiastic digital marketing expert chatting with a potential client. 

Your personality:
- Warm, conversational, and approachable (like texting a friend)
- Passionate about helping businesses grow
- Use casual language ("honestly", "look", "here's the thing")
- Occasionally use emojis naturally (but don't overdo it)
- Keep responses 2-4 short paragraphs max
- Be helpful and specific, not generic

Your services & pricing (in Indian Rupees - prices are negotiable):
- SEO: ₹24,999/month (keyword research, optimization, content, reports)
- Social Media: ₹16,599/month (3-5 platforms, daily posts, engagement)
- PPC/Ads: ₹33,299/month + ad budget (campaign management, optimization)
- Content: ₹20,799/month (4 blog posts, SEO optimized)
- Email: ₹16,599/month (campaigns, automation, design)

Contact Information (share when asked about contact, call, email, or getting in touch):
- Phone: 9840344562
- Email: pavithrachandrasekar9360@gmail.com
- Website: www.digitalmarketing.com/book

Guidelines:
- Only mention pricing if asked or highly relevant
- Ask follow-up questions to understand their needs
- Be conversational, not salesy
- Vary your responses (don't use same phrases repeatedly)
- Show genuine interest in their business
- Always mention that prices are flexible and negotiable when discussing costs

{conversation_history}

Current message from user: {message}

Respond as Sarah would - naturally, helpfully, and conversationally:"""

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }
        
        print(f"🔄 Calling Gemini API...")
        
        response = requests.post(
            GEMINI_API_URL, 
            json=payload, 
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📡 Gemini Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Better error handling for unexpected response formats
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                
                # Check if content exists
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        generated_text = parts[0]['text']
                        print(f"✅ Gemini success!")
                        return generated_text.strip()
                
                # Handle safety/filter blocks
                if 'finishReason' in candidate:
                    print(f"⚠️ Gemini blocked: {candidate.get('finishReason')}")
                    return None
                    
            print(f"⚠️ Unexpected response format: {result}")
        else:
            print(f"❌ Gemini API Error: {response.status_code}")
            print(f"Error details: {response.text[:500]}")
        
        return None
        
    except requests.exceptions.Timeout:
        print("⏱️ Gemini API Timeout")
        return None
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        import traceback
        traceback.print_exc()
        return None
    
def send_contact_notification(user_message, session_id):
    """Send email notification when user requests contact"""
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = "New Contact Request from Chatbot"
        message = f"""
New contact request received:

Session ID: {session_id}
User Message: {user_message}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please follow up with this lead.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.NOTIFICATION_EMAIL],
            fail_silently=True,
        )
        print(f"📧 Contact notification sent for session: {session_id}")
        return True
    except Exception as e:
        print(f"❌ Email notification failed: {e}")
        return False


def enhance_response_with_pricing(response, user_message):
    """Add pricing details if relevant but not already included"""
    lower_msg = user_message.lower()
    
    if '₹' in response or 'month' in response.lower():
        return response
    
    pricing_addition = ""
    
    if 'how much' in lower_msg or 'price' in lower_msg or 'cost' in lower_msg:
        if 'seo' in lower_msg:
            pricing_addition = "\n\n💰 SEO starts at ₹24,999/month with everything included! (Prices are negotiable)"
        elif 'social' in lower_msg:
            pricing_addition = "\n\n💰 Social media is ₹16,599/month for 3-5 platforms! (Prices are negotiable)"
        elif 'ppc' in lower_msg or 'ad' in lower_msg:
            pricing_addition = "\n\n💰 PPC management is ₹33,299/month + your ad budget! (Prices are negotiable)"
        elif 'content' in lower_msg or 'blog' in lower_msg:
            pricing_addition = "\n\n💰 Content packages start at ₹20,799/month for 4 posts! (Prices are negotiable)"
        elif 'email' in lower_msg:
            pricing_addition = "\n\n💰 Email marketing is ₹16,599/month! (Prices are negotiable)"
    
    return response + pricing_addition


def get_enhanced_local_response(message, context):
    """Enhanced fallback responses when API is unavailable"""
    lower_msg = message.lower().strip()
    
    if re.match(r'^(hi|hello|hey|sup|yo)', lower_msg):
        responses = [
            "Hey there! Thanks for chatting with me! I'm Sarah, and I help businesses grow online through smart digital marketing. What's on your mind today?",
            "Hi! Great to meet you! I'm Sarah, your friendly marketing expert. Whether it's SEO, social media, or ads - I've got you covered. What can I help with?",
            "Hello! I'm Sarah! I love helping businesses succeed with digital marketing. No question is too big or small - what would you like to know?",
        ]
        return random.choice(responses)
    
    if any(word in lower_msg for word in ['thank', 'thanks', 'appreciate']):
        responses = [
            "You're so welcome! Happy to help anytime. Got any other questions?",
            "Of course! That's what I'm here for! Feel free to ask anything else!",
            "Anytime! This is what I love doing. Don't hesitate if you need anything else!",
        ]
        return random.choice(responses)
    
    if 'about you' in lower_msg or 'who are you' in lower_msg:
        return """Thanks for asking! I'm Sarah, and I'm basically obsessed with digital marketing. I've been doing this for years and still get excited when I see a client's rankings jump!

I believe marketing should be authentic, results-driven, and actually fun to work on. No boring corporate stuff here!

But enough about me - tell me about YOUR business! What do you do?"""
    
    if 'price' in lower_msg or 'cost' in lower_msg or 'how much' in lower_msg:
        return """Let's talk pricing! Here's the breakdown (all prices are negotiable):

🔍 SEO - ₹24,999/month (keyword research, optimization, content, reports)
📱 Social Media - ₹16,599/month (3-5 platforms, daily management)
💰 PPC/Ads - ₹33,299/month + ad budget (full campaign management)
📝 Content - ₹20,799/month (4 blog posts, SEO optimized)
📧 Email - ₹16,599/month (campaigns, automation, design)

💡 Note: Prices are flexible based on your specific needs and can be customized!

Most businesses bundle 2-3 services for better results. What's most important to you right now?"""
    
    if 'what do you do' in lower_msg or 'services' in lower_msg:
        return """Great question! I help businesses get noticed online and turn that attention into customers!

Here's what I do:
🔍 SEO - Get you ranking on Google
📱 Social Media - Build your brand presence
💰 Paid Ads - Run campaigns that convert
📝 Content - Create engaging blogs and posts
📧 Email - Build customer relationships

Most businesses start with 2-3 of these. What sounds most useful for you?"""
    
    if 'seo' in lower_msg:
        return """SEO is one of my favorites! It's about making Google fall in love with your website so you show up when people search for what you offer.

We do keyword research, optimize your site for speed, create quality content, and build your authority. It takes 3-6 months to see big results, but then that traffic keeps coming without paying for ads!

What industry are you in? I'd love to share what keywords might work for you!"""
    
    if 'social' in lower_msg:
        return """Social media is where you get to show your brand's personality! It's not about posting constantly - it's about consistent, engaging content.

We create posts that stop the scroll, engage with your followers authentically, and build a real community. Which platforms are you most active on?"""
    
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