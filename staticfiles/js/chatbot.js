let chatLoaded = false;

localStorage.clear();
let conversationContext = [];
let userPreferences = {};

// Dynamic suggestions based on context
const contextualSuggestions = {
    initial: [
        "What's the best way to start?",
        "How much does this cost?",
        "Tell me about SEO",
        "I'm confused, help!"
    ],
    afterGreeting: [
        "What services do you offer?",
        "Show me your pricing",
        "How do I get started?",
        "Tell me more about your team"
    ],
    afterPricing: [
        "Can we schedule a call?",
        "What's included in that?",
        "Do you have packages?",
        "Can I customize this?"
    ],
    afterService: [
        "How much does that cost?",
        "How long does it take?",
        "What results can I expect?",
        "Let's get started!"
    ]
};

// Enhanced knowledge base with more personality
const marketingKnowledge = {
    seo: {
        keywords: ['seo', 'search engine', 'ranking', 'google', 'optimization', 'organic', 'keywords', 'rank', 'traffic', 'visibility'],
        responses: [
            "Ooh, SEO! *gets excited* 🚀 Okay so here's the deal - imagine Google is like a massive library, and your website is a book. We make sure your book is on the front shelf where everyone can see it!\n\nWe do keyword research (finding what your customers actually search for), optimize your site to load lightning-fast ⚡, and create content that Google AND people love.\n\nBest part? Once you rank well, that's FREE traffic coming to you 24/7. No ads needed! Usually takes 3-6 months to see big results, but it's SO worth it.\n\nWant to know what we'd do specifically for YOUR business? 😊",
            
            "Great question! Think of SEO like planting a garden 🌱 - it takes time to grow, but once it does, you keep harvesting!\n\nHere's what we do:\n• Find the exact words your customers use when searching\n• Make your website crazy fast (Google loves speed!)\n• Create helpful content that answers real questions\n• Build your credibility online\n\nThe magic happens around month 3-4 when you start climbing those rankings. Then traffic just keeps growing! Sound interesting?",
            
            "I LOVE talking about SEO! 😄 Look, 93% of online experiences start with a search engine. If you're not on page 1 of Google, you're basically invisible.\n\nWe fix that! Through smart optimization, quality content, and building your site's authority. It's not magic - it's strategy mixed with knowing how Google thinks.\n\nThe results compound over time. Month 1 you see small gains, by month 6 you're ranking for tons of keywords. Ready to dominate Google? 🎯"
        ],
        pricing: "💰 **SEO Investment:** Starting at $299/month\n\n✅ What you get:\n• Complete keyword research & strategy\n• Website optimization (speed, mobile, technical stuff)\n• Monthly content creation\n• Progress reports (so you see what's working!)\n• Direct access to me for questions\n\nMost clients see their first page 1 rankings within 4-5 months. Want to see what keywords we'd target for you?",
        followUp: ["What industry are you in?", "Have you tried SEO before?", "What's your main goal - more leads or brand awareness?"]
    },
    
    social: {
        keywords: ['social media', 'facebook', 'instagram', 'twitter', 'linkedin', 'tiktok', 'posts', 'engagement', 'social', 'followers', 'content'],
        responses: [
            "Ah, social media! 📱 This is where you get to show your brand's personality!\n\nHere's my philosophy: It's NOT about posting 10 times a day and praying something works. It's about showing up consistently with content your audience actually cares about.\n\nWe create posts that stop the scroll, engage with your followers like real humans (because we are! 😊), and build a genuine community around your brand.\n\nWhich platforms are you most active on? Instagram? LinkedIn? Let's talk about where YOUR people hang out!",
            
            "Social media done right? *chef's kiss* 🤌 It's SO powerful!\n\nWe handle everything:\n• Creating scroll-stopping content (no boring corporate posts!)\n• Engaging with followers (the secret sauce!)\n• Building a community that actually likes you\n• Turning followers into customers\n\nNo jargon, no boring stuff - just authentic content that feels like YOU. What's your brand's vibe? Fun? Professional? Edgy? Let's make it shine! ✨",
            
            "Let me tell you about social media! 🎉 It's basically your brand's personality online.\n\nThink about it - people follow brands they connect with. We help you:\n• Show up consistently (consistency > perfection!)\n• Tell your story in a way that resonates\n• Actually ENGAGE (not just post and ghost)\n• Turn casual scrollers into loyal customers\n\nWhether it's Instagram, Facebook, LinkedIn, TikTok - wherever your audience lives. The key? Authenticity + Consistency. Want to chat about your target audience? 🎯"
        ],
        pricing: "💰 **Social Media Magic:** Starting at $199/month\n\n✅ What you get:\n• Content for 3-5 platforms (your choice!)\n• 4-5 posts per week per platform\n• Stories, reels, all that good stuff\n• Community management (we respond to comments!)\n• Monthly analytics (see what's crushing it)\n• Hashtag strategy\n\nBasically everything except eating pizza while we work (though we might do that too 🍕). Which platforms do you want to focus on?",
        followUp: ["What platforms are you currently on?", "Who's your target audience?", "Do you have brand guidelines or should we create some?"]
    },
    
    ppc: {
        keywords: ['ppc', 'google ads', 'facebook ads', 'paid', 'advertising', 'campaign', 'ads', 'ad spend', 'adwords', 'sponsored'],
        responses: [
            "PPC is like the express lane! 🚗💨 While SEO is amazing (and we love it), sometimes you need results NOW.\n\nWith paid ads, you're literally showing up RIGHT when people search for what you offer. We set up campaigns on Google, Facebook, Instagram - wherever makes sense for YOUR business.\n\nThe trick? Not wasting money. We constantly test different ads, adjust targeting, and track EVERYTHING to make sure every dollar works hard for you.\n\nWhat's your monthly budget looking like? (Don't worry, we can start small and scale up! 📈)",
            
            "Okay so PPC is pretty straightforward - you pay to show up when people search for your stuff. But here's the thing... most businesses waste SO much money on bad ads! 😰\n\nThat's where we come in! We:\n• Create ads that actually get clicks (no boring corporate speak)\n• Target EXACTLY the right people\n• Track everything obsessively\n• Adjust daily based on what's working\n\nIt's like having a salesperson who never sleeps and only talks to people ready to buy! Want to give it a shot?",
            
            "Love talking about paid ads! Here's why they're great - INSTANT visibility! ⚡\n\nWhile SEO builds over time, PPC can have your phone ringing THIS WEEK. We:\n• Research what converts (not just what gets clicks)\n• Write compelling ad copy\n• Design eye-catching visuals\n• A/B test everything\n• Optimize for YOUR goals (leads, sales, whatever!)\n\nPlus you can start small. Test $500/month, see what works, then scale up! Sound good? 🎯"
        ],
        pricing: "💰 **PPC Management:** $399/month + ad spend\n\n✅ What's included:\n• Campaign setup & strategy\n• Ad creation & copywriting\n• Ongoing optimization (daily adjustments!)\n• A/B testing\n• Detailed reporting\n• Landing page recommendations\n\n💡 **Pro tip:** We recommend at least $500/month in ad spend to start. But here's the thing - we make every dollar count! Most clients see 3-5x return on ad spend within the first few months.\n\nWant to talk about what kind of results you're hoping for?",
        followUp: ["What's your average customer worth?", "Have you run ads before?", "What's your main goal - leads, sales, brand awareness?"]
    },
    
    content: {
        keywords: ['content', 'blog', 'writing', 'articles', 'copywriting', 'posts', 'content marketing', 'copy'],
        responses: [
            "Content is honestly where most businesses drop the ball! 😅 They either don't do it at all, or they write boring stuff nobody wants to read.\n\nWe create content that's actually INTERESTING:\n• Blog posts that answer real questions (and rank on Google!)\n• Social posts that get engagement\n• Emails people actually open\n• Website copy that converts\n\nThe goal? Make your audience think \"wow, these people really get it!\" 🎯\n\nWhat kind of content would help YOUR business most?",
            
            "Oh man, good content makes SUCH a difference! Think about it - before someone buys from you, they want to trust you, right?\n\nGreat content builds that trust! 💪 We:\n• Research what your audience actually cares about\n• Create content that helps them\n• Optimize it so people can find it\n• Make it shareable and engaging\n\nBlog posts, social content, email newsletters, website copy - whatever you need! No fluff, no corporate buzzwords - just helpful, interesting stuff.\n\nWhat topics would your customers want to read about?",
            
            "Let's talk content! 📝 Here's the truth - content marketing gets 3x more leads than traditional marketing and costs 62% less.\n\nWhy? Because you're HELPING people, not interrupting them! We:\n• Find content gaps in your industry\n• Create comprehensive, helpful resources\n• Optimize for SEO (double win!)\n• Promote it strategically\n\nBlog posts, guides, case studies, social content - all designed to attract and convert. Your industry probably has tons of questions people are asking. Let's answer them! What field are you in?"
        ],
        pricing: "💰 **Content Creation:** Starting at $249/month\n\n✅ What you get:\n• 4 high-quality blog posts (1000+ words each)\n• SEO optimization (keywords, meta descriptions, etc.)\n• Topic research & strategy\n• Editing & proofreading\n• WordPress upload (if needed)\n• Social media snippets from each post\n\n📝 **Optional add-ons:**\n• Email newsletters: +$99/month\n• Social media content: +$149/month\n• Website copywriting: Custom quote\n\nWant to see some samples of our work?",
        followUp: ["What industry are you in?", "Do you currently have a blog?", "What topics are important to your customers?"]
    },
    
    email: {
        keywords: ['email', 'newsletter', 'email campaign', 'mailchimp', 'automation', 'email marketing', 'drip campaign'],
        responses: [
            "Email is SO underrated! 📧 Everyone's obsessed with social media, but you know what? Email actually gets results.\n\nHere's why: You OWN your email list. Instagram could disappear tomorrow (knock on wood 🤞), but your email list? That's yours forever!\n\nWe create:\n• Welcome sequences that build relationships\n• Promotional emails people want to open\n• Automations that work while you sleep 😴\n• Newsletters people actually read\n\nNo spam vibes - just genuine, helpful emails! What platform are you using? Mailchimp? Klaviyo?",
            
            "You know what? Email still CRUSHES it for ROI! Like $42 return for every $1 spent. 🤯\n\nWe build campaigns that feel personal, not like mass blasts from a corporation:\n• Segmentation (sending the right message to the right people)\n• Automation (set it and forget it!)\n• Beautiful design (mobile-friendly, of course)\n• Compelling copy (that actually gets clicks)\n\nThe goal? When people see your email, they think \"oh cool, an email from them!\" instead of hitting delete. Sound good?",
            
            "Email marketing is one of my favorites because it WORKS! 💪 Here's what we do:\n\n• Set up automated welcome sequences\n• Create regular newsletters (weekly, monthly - your choice)\n• Build promotional campaigns that convert\n• A/B test everything\n• Clean your list (remove inactive subscribers)\n\nAll designed to nurture relationships and drive sales. No spam, no annoying daily emails - just genuine, helpful content that people look forward to! Do you have an email list started?"
        ],
        pricing: "💰 **Email Marketing:** $199/month\n\n✅ What's included:\n• Email strategy & calendar\n• 4-8 emails per month (depending on your needs)\n• Email design & templates\n• Copywriting\n• List management\n• A/B testing\n• Analytics & reporting\n• Platform setup (if needed)\n\n📧 Works with: Mailchimp, Klaviyo, Constant Contact, or whatever you're using!\n\nMost clients see email driving 20-30% of their revenue within a few months. Ready to start building that list?",
        followUp: ["How big is your email list?", "What platform are you using?", "What do you want to achieve with email?"]
    }
};

// Personality responses with more variety
const personalityResponses = {
    greetings: [
        "Hey there! 👋 Thanks for stopping by! I'm Sarah, and I absolutely LOVE helping businesses grow online. Whether you're just starting out or looking to level up your marketing game, I'm here to help! What's on your mind today?",
        
        "Hi! 😊 So glad you're here! I'm your friendly neighborhood marketing nerd (yes, I actually get excited about SEO rankings 📈). No question is too basic or too complicated - I promise! What can I help you figure out?",
        
        "Hey hey! Welcome! 🎉 I'm Sarah, and I help businesses like yours crush it with digital marketing. SEO, social media, ads - all that good stuff. But enough about me, let's talk about YOU! What brings you here today?",
        
        "Hello! Great to meet you! 👋 Fair warning: I'm slightly obsessed with digital marketing, but I promise to keep it fun and jargon-free. What would you like to know about growing your business online?"
    ],
    
    thanks: [
        "You're so welcome! 😊 Happy to help anytime. Seriously, feel free to ask me anything else - I live for this stuff!",
        
        "Of course! That's literally what I'm here for! 💪 Got any other questions? I'm always happy to chat!",
        
        "Anytime! This is what I love doing. 🎯 Don't hesitate to ask if you need anything else - even if it seems random!",
        
        "No problem at all! Glad I could help! 🙌 I'm around if you need anything else - marketing questions, life advice, whatever! (Okay maybe just marketing 😄)"
    ],
    
    confused: [
        "No worries at all! Marketing can feel overwhelming - trust me, I totally get it. 😊\n\nLet me make it simple: What's your biggest challenge right now?\n\n🤔 Is it:\n• Not enough people finding your website?\n• Social media feels like shouting into the void?\n• Ads eating your budget with no results?\n• You're just not sure where to start?\n\nJust tell me what's frustrating you most and we'll figure it out together! I promise to keep it simple.",
        
        "Hey, that's totally okay! This stuff can be confusing. 🤗 Let's break it down together.\n\nThink about your business for a sec. What's the ONE thing that would make the biggest difference right now?\n\nMore website visitors? More social media followers? More sales? Something else?\n\nOnce I know that, I can point you in the right direction!",
        
        "Don't worry! Nobody expects you to be a marketing expert - that's MY job! 😄\n\nHere's a simple question: If you could wave a magic wand and fix ONE thing about your marketing, what would it be?\n\nMore visibility? Better engagement? More leads? Tell me and let's work backwards from there!"
    ]
};

// Enhanced message analysis with context
function analyzeMessage(message) {
    const lowerMessage = message.toLowerCase().trim();
    conversationContext.push(lowerMessage);
    
    // Keep context to last 5 messages
    if (conversationContext.length > 5) {
        conversationContext.shift();
    }
    
    // Greetings with personality
    if (/^(hi|hello|hey|sup|yo|good morning|good afternoon|good evening|howdy|greetings|hiya)/.test(lowerMessage)) {
        updateSuggestions('afterGreeting');
        return getRandomResponse(personalityResponses.greetings);
    }
    
    // Thanks/appreciation with warmth
    if (/thank|thanks|appreciate|thx|ty|awesome|great|helpful|perfect|amazing|cool/.test(lowerMessage)) {
        return getRandomResponse(personalityResponses.thanks);
    }
    
    // Pricing - comprehensive and clear
    if ((/^(price|pricing|cost|quote|how much|budget|afford|expensive|cheap)/.test(lowerMessage) && lowerMessage.split(' ').length <= 4) || 
        /show.*all.*pric|all.*pric|full.*pric|complete.*pric/.test(lowerMessage)) {
        updateSuggestions('afterPricing');
        return `Okay, let's talk money! 💰 Here's the full breakdown:\n\n🔍 **SEO Package** - $299/month\n• Keyword research & strategy\n• Website optimization\n• Monthly content creation\n• Progress reports\n\n📱 **Social Media** - $199/month\n• 3-5 platforms (your choice!)\n• Daily posts + engagement\n• Content creation\n• Analytics\n\n💰 **PPC/Ads** - $399/month + ad spend\n• Campaign management\n• Ad creation & testing\n• Daily optimization\n• Detailed reporting\n(We recommend $500+ monthly ad spend)\n\n📝 **Content Creation** - $249/month\n• 4 quality blog posts\n• SEO optimization\n• Strategy & research\n\n📧 **Email Marketing** - $199/month\n• 4-8 emails/month\n• Design & copywriting\n• Automation setup\n• Analytics\n\n✨ **Good news:** Most businesses bundle 2-3 services and we offer package discounts!\n\nWhat's most important to YOU right now? Let's build something that fits your goals! 🎯`;
    }
    
    // Contact/getting started - enthusiastic and clear
    if (/contact|reach|call|phone|email|get started|sign up|hire|work with|schedule|meet|book|talk to|speak with/.test(lowerMessage)) {
        return `Love the enthusiasm! Let's make this happen! 🚀\n\nHere's the easiest way to get rolling:\n\n1️⃣ Quick chat (no pressure, just getting to know your business)\n2️⃣ I'll send you a custom game plan\n3️⃣ If it feels right, we get started!\n\n📱 **Call/Text:** (555) 123-4567\n📧 **Email:** hello@digitalmarketingpro.com\n🌐 **Book a call:** www.digitalmarketing.com/book\n\n💬 **OR** - we can keep chatting right here! I'm loving this conversation! 😊\n\nTell me about your business - what do you do? Who are your customers?`;
    }
    
    // Confused/needs help - empathetic and guiding
    if (/confused|don't understand|not sure|stuck|lost|overwhelm|don't know|clueless/.test(lowerMessage)) {
        return getRandomResponse(personalityResponses.confused);
    }
    
    // Check for service matches with enhanced responses
    let bestMatch = null;
    let highestScore = 0;
    
    for (const [service, data] of Object.entries(marketingKnowledge)) {
        let score = 0;
        for (const keyword of data.keywords) {
            if (lowerMessage.includes(keyword)) {
                score += 2;
            }
        }
        
        if (score > highestScore) {
            highestScore = score;
            bestMatch = service;
        }
    }
    
    if (bestMatch && highestScore > 0) {
        const service = marketingKnowledge[bestMatch];
        const randomResponse = getRandomResponse(service.responses);
        updateSuggestions('afterService');
        
        let fullResponse = randomResponse;
        
        // Add pricing if they're asking about cost
        if (/price|cost|quote|how much|pricing|budget|pay|fee|afford|expensive|cheap/.test(lowerMessage)) {
            fullResponse += `\n\n${service.pricing}`;
        }
        
        // Add natural follow-up question
        if (service.followUp && Math.random() > 0.3) {
            const randomFollowUp = service.followUp[Math.floor(Math.random() * service.followUp.length)];
            fullResponse += `\n\n${randomFollowUp}`;
        }
        
        return fullResponse;
    }
    
    // What do you do / services
    if (/what.*do|help.*with|services|offer|provide|specialize|about.*business|tell me about/.test(lowerMessage)) {
        updateSuggestions('afterService');
        return `Great question! So basically, I help businesses get noticed online and turn that attention into actual customers! 🎯\n\nHere's what we do:\n\n🔍 **SEO** - Get you ranking on Google (organic traffic is the best!)\n📱 **Social Media** - Build your brand on Instagram, Facebook, LinkedIn, TikTok\n💰 **Paid Ads** - Run campaigns that actually convert (no wasted budget!)\n📝 **Content** - Create blogs, posts, stuff people actually want to read\n📧 **Email** - Build relationships with your audience that lead to sales\n\n💡 **Here's my approach:** Most businesses start with 2-3 of these and add more as they grow. No one-size-fits-all here!\n\nWhat sounds most useful for where you're at right now?`;
    }
    
    // Personal questions about Sarah
    if (/who are you|your name|tell me about you|about yourself/.test(lowerMessage)) {
        return `Aw, thanks for asking! 😊 I'm Sarah, and I'm basically a digital marketing nerd who loves helping businesses grow!\n\nI've been doing this for years, and honestly? I still get excited when I see a client's rankings jump or their social media take off. Yeah, I'm that person! 📈\n\nI believe marketing should be:\n✨ Authentic (no fake corporate vibes)\n💪 Results-driven (pretty graphics are nice, but RESULTS matter)\n🤝 Partnership-focused (we're in this together!)\n\nEnough about me though - let's talk about YOUR business! What do you do?`;
    }
    
    // Quality/results questions
    if (/results|guarantee|promise|success rate|track record|proof|examples|case stud/.test(lowerMessage)) {
        return `Love that you're asking about results! That's exactly what matters! 📊\n\nHere's the real talk:\n\n🎯 **SEO:** Most clients see first page rankings within 4-6 months. Organic traffic typically grows 150-300% in the first year.\n\n📱 **Social Media:** Average engagement rate increase of 200-400% within 3 months. Follower growth varies by industry.\n\n💰 **PPC:** Most clients see 3-5x return on ad spend. Some do even better!\n\n📝 **Content:** Blog posts typically rank within 3-6 months, driving consistent organic traffic.\n\n⚠️ **Honest moment:** Results vary based on industry, competition, and budget. I never promise overnight success because that's not real. But I DO promise:\n• Transparency (you'll always know what's happening)\n• Data-driven decisions (not guesswork)\n• Constant optimization (we don't set and forget)\n\nWant to see some specific case studies from your industry?`;
    }
    
    // Timeline questions
    if (/how long|timeline|when.*see|time.*take|fast|quick|soon/.test(lowerMessage)) {
        return `Good question! Nobody wants to wait forever, right? ⏰\n\nHere's the realistic timeline:\n\n🔍 **SEO:** 3-6 months for significant results\n• Month 1-2: Setup, optimization, initial content\n• Month 3-4: Start seeing ranking improvements\n• Month 5-6: Real momentum kicks in\n• Month 12+: Compounding returns (this is when it gets REALLY good!)\n\n📱 **Social Media:** 1-3 months for traction\n• Week 1-4: Strategy, content creation\n• Month 2-3: Engagement grows, community forms\n• Month 3+: Consistent growth and conversions\n\n💰 **PPC:** Immediate visibility (literally day 1!)\n• Week 1-2: Campaign setup, initial testing\n• Week 3-4: Optimization based on data\n• Month 2+: Scaling what works\n\n📝 **Content:** 2-4 months for ranking\n• Content published immediately\n• Rankings build over 2-4 months\n• Long-term traffic continues growing\n\n💡 **Pro tip:** Combining strategies gets faster results! SEO + PPC = immediate visibility while building long-term growth!\n\nWhat's your timeline looking like?`;
    }
    
    // Default response - more engaging and helpful
    return `Hmm, I want to make sure I understand exactly what you need! 🤔\n\nYou said: "${message}"\n\nLet me help you out! I specialize in:\n\n🔍 **SEO** - Getting found on Google organically\n📱 **Social Media** - Instagram, Facebook, LinkedIn, TikTok\n💰 **Paid Ads** - Google Ads, Facebook Ads that convert\n📝 **Content** - Blogs, posts, email campaigns\n\nCould you tell me a bit more about:\n• What you're trying to achieve?\n• What's your biggest marketing challenge right now?\n• Or just ask me anything!\n\nI'm here to help make this as easy as possible! 😊`;
}

// Helper function to get random response
function getRandomResponse(responseArray) {
    return responseArray[Math.floor(Math.random() * responseArray.length)];
}

// Update contextual suggestions
function updateSuggestions(context) {
    const suggestions = contextualSuggestions[context] || contextualSuggestions.initial;
    const suggestionsList = document.getElementById('suggestionsList');
    
    if (suggestionsList) {
        suggestionsList.innerHTML = suggestions.map(s => 
            `<span class="suggestion-chip" onclick="sendQuickMessage('${s}')">${s}</span>`
        ).join('');
    }
}

// Show suggestions when input is focused
function showSuggestions() {
    const suggestionsDiv = document.getElementById('typingSuggestions');
    if (suggestionsDiv && conversationContext.length > 0) {
        suggestionsDiv.style.display = 'block';
    }
}

// Hide suggestions with delay
let hideSuggestionsTimeout;
function hideSuggestionsDelayed() {
    hideSuggestionsTimeout = setTimeout(() => {
        const suggestionsDiv = document.getElementById('typingSuggestions');
        if (suggestionsDiv) {
            suggestionsDiv.style.display = 'none';
        }
    }, 200);
}

// Open chatbot modal with animation
async function openChatbotModal() {
    const modal = document.getElementById('chatbotModal');
    const content = document.getElementById('chatbotContent');
    
    modal.classList.add('active');
    
    if (!chatLoaded) {
        try {
            const response = await fetch('/get-chat-content/');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const html = await response.text();
            content.innerHTML = html;
            chatLoaded = true;
            
            // Initialize suggestions
            updateSuggestions('initial');
            
            // Add welcome message with delay for more natural feel
            setTimeout(() => {
                addSystemMessage("💡 Tip: I'm a real person (well, AI, but I act human! 😄). Feel free to chat naturally!");
            }, 2000);
            
            setTimeout(() => {
                const chatInput = document.getElementById('chatInput');
                if (chatInput) chatInput.focus();
            }, 100);
            
        } catch (error) {
            console.error('Error loading chat:', error);
            content.innerHTML = `
                <div class="error-message" style="padding: 2rem; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">😅</div>
                    <h3 style="color: #e74c3c; margin-bottom: 1rem;">Oops! Chat's having a moment...</h3>
                    <p style="color: #7f8c8d; margin-bottom: 1.5rem;">The chat is being a bit finicky right now. But hey, no worries - you can still reach us the old-fashioned way!</p>
                    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                        <strong style="display: block; margin-bottom: 0.5rem;">Reach out directly:</strong>
                        <p style="margin: 0.5rem 0;">📧 hello@digitalmarketingpro.com</p>
                        <p style="margin: 0.5rem 0;">📱 (555) 123-4567</p>
                        <p style="margin: 0.5rem 0;">🌐 www.digitalmarketing.com</p>
                    </div>
                </div>
            `;
        }
    } else {
        setTimeout(() => {
            const chatInput = document.getElementById('chatInput');
            if (chatInput) chatInput.focus();
        }, 100);
    }
}

// Close modal
function closeChatbotModal() {
    const modal = document.getElementById('chatbotModal');
    modal.classList.remove('active');
}

// Handle enter key
function handleChatKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendChatMessage();
    }
}

// Main send message function with enhanced interactions
async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (message === '') return;
    
    // Hide suggestions
    const suggestionsDiv = document.getElementById('typingSuggestions');
    if (suggestionsDiv) suggestionsDiv.style.display = 'none';
    
    addMessageToChat(message, 'user');
    input.value = '';
    
    // Vary typing delay based on message complexity
    const typingId = addTypingIndicator();
    const wordCount = message.split(' ').length;
    const baseDelay = 1000;
    const perWordDelay = 100;
    const naturalDelay = baseDelay + (wordCount * perWordDelay) + (Math.random() * 500);
    
    await new Promise(resolve => setTimeout(resolve, naturalDelay));
    
    try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                         document.querySelector('meta[name="csrf-token"]')?.content || 
                         getCookie('csrftoken');
        
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || 'dummy-token'
            },
            body: JSON.stringify({ 
                'message': message,
                'context': conversationContext.slice(-3) // Send recent context
            })
        });
        
        removeTypingIndicator(typingId);
        
        if (response.ok) {
            const data = await response.json();
            if (data.response) {
                addMessageToChat(data.response, 'bot');
                return;
            }
        }
        
        throw new Error('Backend unavailable');
        
    } catch (error) {
        console.log('Using local AI fallback');
        removeTypingIndicator(typingId);
        
        const botResponse = analyzeMessage(message);
        addMessageToChat(botResponse, 'bot');
    }
}

// Quick messages with smooth interaction
function sendQuickMessage(message) {
    const input = document.getElementById('chatInput');
    input.value = message;
    
    // Animate the input
    input.style.transform = 'scale(1.02)';
    setTimeout(() => {
        input.style.transform = 'scale(1)';
        sendChatMessage();
    }, 100);
}

// Add message to chat with enhanced formatting
function addMessageToChat(message, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(10px)';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'bot' ? '🤖' : '👤';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Enhanced formatting
    let formattedMessage = message
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    // Wrap in paragraph if not already
    if (!formattedMessage.startsWith('<p>')) {
        formattedMessage = `<p>${formattedMessage}</p>`;
    }
    
    content.innerHTML = formattedMessage;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);
    
    // Animate in
    setTimeout(() => {
        messageDiv.style.transition = 'all 0.3s ease-out';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    }, 10);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Add system message (tips, notifications, etc.)
function addSystemMessage(message) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const systemDiv = document.createElement('div');
    systemDiv.style.textAlign = 'center';
    systemDiv.style.padding = '0.5rem';
    systemDiv.style.margin = '1rem 0';
    
    systemDiv.innerHTML = `
        <div style="display: inline-block; background: #f8f9fa; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; color: #6c757d;">
            ${message}
        </div>
    `;
    
    messagesContainer.appendChild(systemDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Typing indicator with personality
function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typing-' + Date.now();
    typingDiv.style.opacity = '0';
    
    const randomTypingText = [
        'Sarah is typing',
        'Thinking',
        'Writing',
        'One sec'
    ][Math.floor(Math.random() * 4)];
    
    typingDiv.innerHTML = `
        <div class="message-avatar">✍️</div>
        <div class="message-content">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 0.9rem; color: #6c757d;">${randomTypingText}...</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    
    setTimeout(() => {
        typingDiv.style.transition = 'opacity 0.3s ease';
        typingDiv.style.opacity = '1';
    }, 10);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return typingDiv.id;
}

function removeTypingIndicator(typingId) {
    const typingElement = document.getElementById(typingId);
    if (typingElement) {
        typingElement.style.opacity = '0';
        setTimeout(() => typingElement.remove(), 300);
    }
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('chatbotModal');
    const overlay = modal?.querySelector('.modal-overlay');
    
    if (overlay) {
        overlay.addEventListener('click', closeChatbotModal);
    }
    
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal?.classList.contains('active')) {
            closeChatbotModal();
        }
    });
    
    // Add input character counter
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('input', function() {
            if (this.value.length > 500) {
                this.value = this.value.substring(0, 500);
            }
        });
    }
});