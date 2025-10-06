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
            "SEO is essential for getting found on Google! Think of it like making sure your business shows up when people search for what you offer.\n\nWe do keyword research, optimize your website speed, create quality content, and build your online authority. Results typically take 3-6 months, but the organic traffic keeps coming without ongoing ad costs.\n\nWhat industry are you in? I can share relevant strategies for your business.",
            
            "Great question about SEO! Here's what we do:\n• Research the exact terms your customers search for\n• Optimize your website for speed and mobile\n• Create helpful content that ranks well\n• Build credibility through quality backlinks\n\nThe best part? Once you rank well, that's consistent free traffic! Interested in learning more?",
            
            "SEO is one of the most cost-effective marketing strategies. 93% of online experiences start with search engines, so being on page 1 matters.\n\nWe focus on sustainable, white-hat techniques that deliver long-term results. Most clients see significant improvement within 4-6 months.\n\nShall we discuss what would work best for your business?"
        ],
        pricing: "💰 **SEO Services:** Starting at ₹15,000/month\n\n✅ What's included:\n• Complete keyword research & strategy\n• On-page & technical SEO optimization\n• Monthly content creation (blogs/articles)\n• Progress reports & analytics\n• Ongoing support\n\n*Prices are negotiable based on project scope and requirements*\n\nMost clients see page 1 rankings within 4-6 months. Want to discuss your specific needs?",
        followUp: ["What industry are you in?", "Have you tried SEO before?", "What's your main goal - more leads or brand awareness?"]
    },
    
    websites: {
        keywords: ['website', 'web design', 'web development', 'static site', 'dynamic site', 'e-commerce', 'landing page', 'portfolio site'],
        responses: [
            "Looking to build a website? Great choice! Your website is your digital storefront, and we make sure it looks professional and works perfectly.\n\nWe offer:\n• Static websites (perfect for portfolios, basic business sites)\n• Dynamic websites (with CMS, databases, user accounts)\n• E-commerce sites (full online stores)\n• Custom web applications\n\nAll our sites are mobile-responsive, fast-loading, and SEO-friendly. What type of website are you thinking about?",
            
            "Website development is our specialty! Whether you need something simple or complex, we've got you covered.\n\nStatic sites are great for: portfolios, landing pages, small business sites\nDynamic sites work best for: content-heavy sites, membership areas, complex functionality\n\nEvery site includes: responsive design, SSL certificate, basic SEO setup, and training on how to manage it.\n\nWhat features are most important to you?",
            
            "Let's talk about your website needs! We build everything from simple landing pages to full e-commerce platforms.\n\nOur process:\n1. Understand your goals and audience\n2. Create mockups for your approval\n3. Develop & test thoroughly\n4. Launch & provide ongoing support\n\nAll sites are built with modern technologies and best practices. Tell me about your project!"
        ],
        pricing: "💰 **Website Development Pricing:**\n\n🌐 **Static Website:** ₹8,000 - ₹25,000\n• Perfect for: Portfolios, landing pages, basic business sites\n• 5-10 pages, responsive design, contact forms\n• Delivery: 7-15 days\n\n🌐 **Dynamic Website:** ₹25,000 - ₹75,000\n• Perfect for: Business sites, blogs, content management\n• Custom CMS, database integration, admin panel\n• Delivery: 15-30 days\n\n🛒 **E-commerce Website:** ₹40,000 - ₹1,50,000+\n• Full online store with payment gateway\n• Product management, cart, order tracking\n• Delivery: 30-45 days\n\n✅ All packages include:\n• Mobile-responsive design\n• Basic SEO setup\n• SSL certificate\n• 30 days support\n\n*Prices are negotiable based on features and complexity*\n\nWant a detailed quote for your project?",
        followUp: ["What type of website do you need?", "Do you have content ready (text, images)?", "What's your timeline?"]
    },
    
    social: {
        keywords: ['social media', 'facebook', 'instagram', 'twitter', 'linkedin', 'tiktok', 'posts', 'engagement', 'social', 'followers', 'content'],
        responses: [
            "Social media is where your brand personality shines! It's not just about posting frequently - it's about posting content your audience actually engages with.\n\nWe create scroll-stopping content, engage authentically with your followers, and build a real community around your brand.\n\nWhich platforms are you most active on?",
            
            "Social media marketing done right can transform your business! We handle:\n• Content creation (posts, stories, reels)\n• Community engagement\n• Strategy & scheduling\n• Analytics & reporting\n\nNo boring corporate posts - just authentic content that resonates with your audience. What's your target audience like?",
            
            "Let's talk social media strategy! Whether it's Instagram, Facebook, LinkedIn, or others - each platform needs a unique approach.\n\nWe help you:\n• Build consistent brand presence\n• Create engaging content\n• Grow your following organically\n• Turn followers into customers\n\nInterested in learning more about our social media packages?"
        ],
        pricing: "💰 **Social Media Management:** Starting at ₹10,000/month\n\n✅ What you get:\n• Content for 2-3 platforms\n• 12-15 posts per month\n• Stories, reels, and graphics\n• Community management (responding to comments)\n• Monthly analytics report\n• Hashtag research & strategy\n\n*Prices are negotiable based on platforms and post frequency*\n\nMost businesses see significant engagement growth within 2-3 months. Which platforms should we focus on?",
        followUp: ["What platforms are you currently on?", "Who's your target audience?", "Do you have brand guidelines?"]
    },
    
    ppc: {
        keywords: ['ppc', 'google ads', 'facebook ads', 'paid', 'advertising', 'campaign', 'ads', 'ad spend', 'adwords', 'sponsored'],
        responses: [
            "PPC advertising gives you instant visibility! While SEO builds over time, paid ads can start driving traffic and leads immediately.\n\nWe set up campaigns on Google Ads, Facebook, Instagram - wherever your customers are. The key is targeting the right audience and constantly optimizing for better results.\n\nWhat's your monthly advertising budget like?",
            
            "Paid advertising can be incredibly effective when done right. Many businesses waste money on poorly targeted ads - we make sure every rupee counts.\n\nWe:\n• Create compelling ad copy\n• Target precisely based on demographics and behavior\n• A/B test everything\n• Optimize daily for best ROI\n\nMost clients see 3-5x return on their ad spend. Want to discuss a strategy for your business?",
            
            "Let's talk about paid ads! Whether it's Google search ads, display ads, or social media advertising - we can help you get immediate results.\n\nBest part? You can start small, test what works, then scale up. No huge upfront investment needed.\n\nWhat are you hoping to achieve with advertising?"
        ],
        pricing: "💰 **PPC Management:** ₹8,000 - ₹20,000/month + ad spend\n\n✅ What's included:\n• Campaign setup & strategy\n• Ad creation & copywriting\n• Daily monitoring & optimization\n• A/B testing\n• Detailed performance reports\n• Landing page recommendations\n\n💡 **Recommended ad budget:** ₹15,000 - ₹50,000/month to start\n\n*Management fees are negotiable based on ad spend and complexity*\n\nMost clients see positive ROI within the first month. Ready to get started?",
        followUp: ["What's your average customer value?", "Have you run ads before?", "What's your main goal - leads or sales?"]
    },
    
    content: {
        keywords: ['content', 'blog', 'writing', 'articles', 'copywriting', 'posts', 'content marketing', 'copy'],
        responses: [
            "Content is what builds trust and authority! Before someone buys from you, they want to know you understand their problems and can solve them.\n\nWe create:\n• SEO-optimized blog posts\n• Engaging social media content\n• Email newsletters\n• Website copy that converts\n\nAll content is research-backed and tailored to your audience. What topics would resonate with your customers?",
            
            "Good content makes a huge difference! Think about it - quality articles and posts establish you as an expert in your field.\n\nWe research what your audience is searching for, create helpful content that answers their questions, and optimize it to rank well on Google.\n\nInterested in content marketing for your business?",
            
            "Let's discuss content strategy! Content marketing gets 3x more leads than traditional marketing at 62% less cost.\n\nWhy? Because you're helping people, not interrupting them. We create blogs, guides, social content - all designed to attract and convert your ideal customers.\n\nWhat industry are you in?"
        ],
        pricing: "💰 **Content Creation:** Starting at ₹12,000/month\n\n✅ What you get:\n• 4 high-quality blog posts (800-1200 words each)\n• SEO optimization (keywords, meta descriptions)\n• Topic research based on your industry\n• Editing & proofreading\n• Images & formatting\n\n📝 **Add-ons available:**\n• Social media content: +₹5,000/month\n• Email newsletters: +₹4,000/month\n• Website copywriting: Custom quote\n\n*Prices are negotiable based on volume and complexity*\n\nWant to see samples of our work?",
        followUp: ["What industry are you in?", "Do you currently have a blog?", "What topics are important to your customers?"]
    },
    
    email: {
        keywords: ['email', 'newsletter', 'email campaign', 'mailchimp', 'automation', 'email marketing', 'drip campaign'],
        responses: [
            "Email marketing is one of the best ROI channels! You own your email list - unlike social media where algorithms control your reach.\n\nWe create:\n• Welcome sequences for new subscribers\n• Regular newsletters\n• Promotional campaigns\n• Automated workflows\n\nAll designed to build relationships and drive sales. Do you have an email list started?",
            
            "Email still delivers amazing results! For every ₹1 spent, average return is ₹40+.\n\nWe build campaigns that feel personal and valuable:\n• Segmentation (right message to right people)\n• Automation (works while you sleep)\n• Mobile-friendly design\n• Compelling copy that gets clicks\n\nInterested in email marketing for your business?",
            
            "Let's talk email strategy! Whether it's newsletters, promotional campaigns, or automated sequences - email is incredibly effective.\n\nWe handle everything: strategy, design, copywriting, list management, and analytics.\n\nWhat platform are you using? Mailchimp? Another?"
        ],
        pricing: "💰 **Email Marketing:** Starting at ₹10,000/month\n\n✅ What's included:\n• Email strategy & content calendar\n• 4-8 emails per month\n• Professional design & templates\n• Copywriting\n• List management & segmentation\n• A/B testing\n• Performance analytics\n\n📧 Works with: Mailchimp, Sendinblue, or your preferred platform\n\n*Prices are negotiable based on list size and frequency*\n\nMost businesses see email driving 20-30% of revenue. Ready to start?",
        followUp: ["How big is your email list?", "What platform are you using?", "What do you want to achieve with email?"]
    }
};

// Pricing overview response
const allPricingResponse = `Here's our complete pricing structure:\n\n🌐 **WEBSITE DEVELOPMENT:**\n• Static Website: ₹8,000 - ₹25,000\n• Dynamic Website: ₹25,000 - ₹75,000\n• E-commerce Site: ₹40,000 - ₹1,50,000+\n\n🔍 **SEO Services:** ₹15,000/month\n\n📱 **Social Media:** ₹10,000/month\n\n💰 **PPC Management:** ₹8,000-₹20,000/month + ad spend\n\n📝 **Content Creation:** ₹12,000/month\n\n📧 **Email Marketing:** ₹10,000/month\n\n✨ **Good news:** Prices are negotiable based on your specific requirements and project scope. Most businesses bundle 2-3 services for better results and discounts!\n\nWhat services are you most interested in?`;

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
    // Pricing - comprehensive and clear
    if ((/^(price|pricing|cost|quote|how much|budget|afford|expensive|cheap)/.test(lowerMessage) && lowerMessage.split(' ').length <= 4) || 
    /show.*all.*pric|all.*pric|full.*pric|complete.*pric/.test(lowerMessage)) {
    updateSuggestions('afterPricing');
    return allPricingResponse;
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
    
    const suggestionsDiv = document.getElementById('typingSuggestions');
    if (suggestionsDiv) suggestionsDiv.style.display = 'none';
    
    addMessageToChat(message, 'user');
    input.value = '';
    
    const typingId = addTypingIndicator();
    
    try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                         document.querySelector('meta[name="csrf-token"]')?.content || 
                         getCookie('csrftoken');
        
        console.log('📤 Sending to backend:', message); // Debug log
        
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || 'dummy-token'
            },
            body: JSON.stringify({ 
                'message': message,
                'context': conversationContext.slice(-3)
            })
        });
        
        console.log('📥 Response status:', response.status); // Debug log
        
        removeTypingIndicator(typingId);
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend response:', data); // Debug log
            
            if (data.response) {
                addMessageToChat(data.response, 'bot');
                
                // Show which source was used
                if (data.source) {
                    console.log(`Source: ${data.source}`);
                }
                return;
            }
        }
        
        // If we get here, something went wrong
        console.error('❌ Backend call failed:', response.status);
        throw new Error('Backend unavailable');
        
    } catch (error) {
        console.error('❌ Error:', error);
        removeTypingIndicator(typingId);
        
        // Only use fallback if absolutely necessary
        addMessageToChat(
            "Sorry, I'm having trouble connecting right now. Please try again!",
            'bot'
        );
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