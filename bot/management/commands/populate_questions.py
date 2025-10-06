# REPLACE your populate_questions.py with this complete version
# chatbot/management/commands/populate_questions.py

from django.core.management.base import BaseCommand
from bot.models import PredefinedQuestion

class Command(BaseCommand):
    help = 'Populate chatbot with complete digital marketing questions, pricing, and portfolio'

    def handle(self, *args, **options):
        complete_questions = [
            # WEBSITE PRICING - DETAILED
            {
                'question': 'Show me website pricing',
                'answer': '''
                <div class="pricing-table">
                    <h4>🌐 Website Development Pricing</h4>
                    
                    <div class="price-item">
                        <span class="service">Static Website (5-8 pages)</span>
                        <span class="price">₹15,000 - ₹25,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Dynamic Website (10-15 pages)</span>
                        <span class="price">₹35,000 - ₹55,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">E-commerce Website</span>
                        <span class="price">₹45,000 - ₹85,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Custom Web Application</span>
                        <span class="price">₹75,000 - ₹1,50,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Website Redesign</span>
                        <span class="price">₹25,000 - ₹45,000</span>
                    </div>
                </div>
                
                <strong>What's Included:</strong><br>
                ✅ Responsive Design (Mobile + Desktop)<br>
                ✅ SEO Optimized<br>
                ✅ Contact Forms<br>
                ✅ Social Media Integration<br>
                ✅ 1 Year Free Maintenance<br>
                ✅ SSL Certificate<br>
                ✅ Google Analytics Setup<br><br>
                
                Want a custom quote? Tell me about your project requirements!
                ''',
                'keywords': 'website pricing, website cost, web development price, static website price, dynamic website cost'
            },
            
            # STATIC WEBSITE DETAILS
            {
                'question': 'What is included in static website?',
                'answer': '''
                <div class="pricing-table">
                    <h4>🏠 Static Website Package (₹15,000 - ₹25,000)</h4>
                    
                    <strong>Pages Included:</strong><br>
                    • Home Page<br>
                    • About Us<br>
                    • Services/Products<br>
                    • Portfolio/Gallery<br>
                    • Contact Us<br>
                    • Blog (optional)<br>
                    • Privacy Policy & Terms<br><br>
                    
                    <strong>Technical Features:</strong><br>
                    ✅ HTML5, CSS3, JavaScript<br>
                    ✅ Fully Responsive Design<br>
                    ✅ Fast Loading Speed<br>
                    ✅ SEO Friendly Structure<br>
                    ✅ Contact Form with Email<br>
                    ✅ Google Maps Integration<br>
                    ✅ Social Media Links<br>
                    ✅ Image Optimization<br><br>
                    
                    <strong>Free Inclusions:</strong><br>
                    • Domain Name (1 year)<br>
                    • Web Hosting (1 year)<br>
                    • SSL Certificate<br>
                    • Google Analytics<br>
                    • Basic SEO Setup<br>
                    • 1 Year Maintenance<br>
                </div>
                
                <strong>Perfect for:</strong> Small businesses, portfolios, service providers, restaurants, consultants.
                ''',
                'keywords': 'static website, simple website, basic website, static site features, static web development'
            },
            
            # DYNAMIC WEBSITE DETAILS
            {
                'question': 'What is included in dynamic website?',
                'answer': '''
                <div class="pricing-table">
                    <h4>⚡ Dynamic Website Package (₹35,000 - ₹55,000)</h4>
                    
                    <strong>Advanced Features:</strong><br>
                    • Content Management System (CMS)<br>
                    • Admin Dashboard<br>
                    • Dynamic Content Updates<br>
                    • User Registration/Login<br>
                    • News/Blog Management<br>
                    • Photo Gallery Management<br>
                    • Inquiry Management System<br>
                    • Newsletter Subscription<br><br>
                    
                    <strong>Technical Specifications:</strong><br>
                    ✅ PHP/Python/Django Framework<br>
                    ✅ MySQL Database<br>
                    ✅ Responsive Bootstrap Design<br>
                    ✅ Advanced SEO Features<br>
                    ✅ Multiple User Roles<br>
                    ✅ Backup System<br>
                    ✅ Security Features<br>
                    ✅ Payment Gateway Ready<br><br>
                    
                    <strong>Content Management:</strong><br>
                    • Add/Edit/Delete Pages<br>
                    • Upload Images & Videos<br>
                    • Manage Products/Services<br>
                    • Update Company Information<br>
                    • Manage Testimonials<br>
                </div>
                
                <strong>Best for:</strong> Growing businesses, service companies, educational institutes, healthcare providers.
                ''',
                'keywords': 'dynamic website, CMS website, content management, dynamic web development, admin panel'
            },
            
            # DIGITAL MARKETING PRICING
            {
                'question': 'What is your SEO pricing?',
                'answer': '''
                <div class="pricing-table">
                    <h4>📈 SEO Service Packages</h4>
                    
                    <div class="price-item">
                        <span class="service">Local SEO (Small Business)</span>
                        <span class="price">₹8,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Standard SEO (5-10 keywords)</span>
                        <span class="price">₹15,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Premium SEO (15-20 keywords)</span>
                        <span class="price">₹25,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">E-commerce SEO</span>
                        <span class="price">₹30,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">SEO Audit (One-time)</span>
                        <span class="price">₹5,000</span>
                    </div>
                </div>
                
                <strong>What's Included in SEO:</strong><br>
                ✅ Keyword Research & Analysis<br>
                ✅ On-page Optimization<br>
                ✅ Technical SEO<br>
                ✅ Content Creation (2-4 articles/month)<br>
                ✅ Link Building<br>
                ✅ Google My Business Optimization<br>
                ✅ Monthly Performance Reports<br>
                ✅ Competitor Analysis<br><br>
                
                <strong>Expected Results:</strong> 3-6 months for significant improvements, 40-60% traffic increase in first year.
                ''',
                'keywords': 'SEO pricing, SEO cost, search engine optimization price, SEO packages, local SEO cost'
            },
            
            {
                'question': 'Google Ads pricing',
                'answer': '''
                <div class="pricing-table">
                    <h4>📊 Google Ads Management</h4>
                    
                    <div class="price-item">
                        <span class="service">Setup Fee (One-time)</span>
                        <span class="price">₹10,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Management Fee</span>
                        <span class="price">20% of ad spend</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Minimum Monthly Ad Spend</span>
                        <span class="price">₹15,000</span>
                    </div>
                </div>
                
                <strong>Our Management Includes:</strong><br>
                ✅ Campaign Strategy & Setup<br>
                ✅ Keyword Research<br>
                ✅ Ad Copy Creation<br>
                ✅ Landing Page Optimization<br>
                ✅ Bid Management<br>
                ✅ A/B Testing<br>
                ✅ Conversion Tracking<br>
                ✅ Weekly Performance Reports<br>
                ✅ Monthly Strategy Calls<br><br>
                
                <strong>Example Investment:</strong><br>
                • Ad Spend: ₹20,000/month<br>
                • Management Fee: ₹4,000/month<br>
                • Total: ₹24,000/month<br><br>
                
                <strong>Expected ROI:</strong> 3-5x return on ad spend within 3 months.
                ''',
                'keywords': 'google ads pricing, PPC cost, google adwords price, paid advertising cost'
            },
            
            {
                'question': 'Social media marketing cost',
                'answer': '''
                <div class="pricing-table">
                    <h4>📱 Social Media Marketing Packages</h4>
                    
                    <div class="price-item">
                        <span class="service">Basic Package (2 platforms)</span>
                        <span class="price">₹8,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Standard Package (4 platforms)</span>
                        <span class="price">₹15,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Premium Package (6 platforms)</span>
                        <span class="price">₹25,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Social Media Ads Management</span>
                        <span class="price">₹5,000/month + ad spend</span>
                    </div>
                </div>
                
                <strong>Platforms We Manage:</strong><br>
                • Facebook & Instagram<br>
                • LinkedIn<br>
                • Twitter<br>
                • YouTube<br>
                • Pinterest<br>
                • TikTok<br><br>
                
                <strong>Services Included:</strong><br>
                ✅ Content Creation (15-30 posts/month)<br>
                ✅ Graphic Design<br>
                ✅ Content Calendar<br>
                ✅ Community Management<br>
                ✅ Hashtag Strategy<br>
                ✅ Performance Analytics<br>
                ✅ Competitor Analysis<br>
                ✅ Monthly Growth Reports<br><br>
                
                <strong>Results You Can Expect:</strong> 25-50% follower growth, 300%+ engagement increase.
                ''',
                'keywords': 'social media marketing cost, social media management price, facebook marketing cost, instagram marketing price'
            },
            
            # PORTFOLIO EXAMPLES
            {
                'question': 'Show me your portfolio',
                'answer': '''
                <h4>🎨 Our Recent Projects</h4>
                
                <div class="portfolio-item">
                    <h5>🏥 MedCare Hospital - Healthcare Website</h5>
                    <p><strong>Type:</strong> Dynamic Website with Appointment Booking<br>
                    <strong>Cost:</strong> ₹45,000 | <strong>Duration:</strong> 6 weeks<br>
                    <strong>Results:</strong> 40% increase in online appointments, 200% traffic growth</p>
                </div>
                
                <div class="portfolio-item">
                    <h5>🛒 FashionHub - E-commerce Store</h5>
                    <p><strong>Type:</strong> E-commerce + Digital Marketing<br>
                    <strong>Investment:</strong> ₹65,000 website + ₹20,000/month marketing<br>
                    <strong>Results:</strong> ₹5 lakhs monthly sales within 4 months</p>
                </div>
                
                <div class="portfolio-item">
                    <h5>🏠 DreamHomes - Real Estate</h5>
                    <p><strong>Type:</strong> Property Listing Website + SEO<br>
                    <strong>Investment:</strong> ₹35,000 + ₹15,000/month SEO<br>
                    <strong>Results:</strong> 10x increase in property inquiries</p>
                </div>
                
                <div class="portfolio-item">
                    <h5>🎓 EduTech Academy - Online Learning</h5>
                    <p><strong>Type:</strong> Learning Management System<br>
                    <strong>Cost:</strong> ₹85,000 | <strong>Features:</strong> Course management, payments<br>
                    <strong>Results:</strong> 500+ students enrolled in first month</p>
                </div>
                
                <div class="portfolio-item">
                    <h5>🍕 TastyBites Restaurant</h5>
                    <p><strong>Type:</strong> Static Website + Social Media<br>
                    <strong>Investment:</strong> ₹18,000 + ₹8,000/month marketing<br>
                    <strong>Results:</strong> 60% increase in orders, doubled social following</p>
                </div>
                
                <br><strong>Industries We've Worked With:</strong><br>
                Healthcare • E-commerce • Real Estate • Education • Restaurants • Manufacturing • Professional Services • Non-profits • Startups<br><br>
                
                <strong>Want to see a specific project or discuss your requirements?</strong> Just ask!
                ''',
                'keywords': 'portfolio, projects, work samples, case studies, examples, our work'
            },
            
            # COMPLETE SERVICES LIST
            {
                'question': 'What services do you offer?',
                'answer': '''
                <h4>🚀 Our Complete Digital Services</h4>
                
                <div class="pricing-table">
                    <h4>💻 Website Development</h4>
                    • Static Websites (₹15,000 - ₹25,000)<br>
                    • Dynamic Websites (₹35,000 - ₹55,000)<br>
                    • E-commerce Stores (₹45,000 - ₹85,000)<br>
                    • Web Applications (₹75,000 - ₹1,50,000)<br>
                    • Website Redesign (₹25,000 - ₹45,000)<br>
                </div>
                
                <div class="pricing-table">
                    <h4>📈 Digital Marketing</h4>
                    • Search Engine Optimization (₹8,000 - ₹30,000/month)<br>
                    • Google Ads Management (20% of ad spend + setup)<br>
                    • Social Media Marketing (₹8,000 - ₹25,000/month)<br>
                    • Content Marketing (₹10,000 - ₹20,000/month)<br>
                    • Email Marketing (₹5,000 - ₹12,000/month)<br>
                </div>
                
                <div class="pricing-table">
                    <h4>🎨 Design Services</h4>
                    • Logo Design (₹5,000 - ₹15,000)<br>
                    • Brand Identity (₹15,000 - ₹35,000)<br>
                    • Print Design (₹2,000 - ₹10,000)<br>
                    • UI/UX Design (₹20,000 - ₹50,000)<br>
                </div>
                
                <div class="pricing-table">
                    <h4>📊 Analytics & Strategy</h4>
                    • Digital Audit (₹5,000)<br>
                    • Marketing Strategy (₹8,000 - ₹15,000)<br>
                    • Competitor Analysis (₹3,000)<br>
                    • Performance Reports (₹2,000/month)<br>
                </div>
                
                <strong>🎯 Our Specialties:</strong><br>
                ✅ Complete Digital Transformation<br>
                ✅ Lead Generation Systems<br>
                ✅ E-commerce Solutions<br>
                ✅ Local Business Marketing<br>
                ✅ Startup Growth Strategies<br><br>
                
                <strong>Why Choose Us?</strong><br>
                • 100+ Successful Projects<br>
                • 5+ Years Experience<br>
                • Guaranteed Results<br>
                • 24/7 Support<br>
                • Transparent Pricing<br>
                ''',
                'keywords': 'services, what do you do, digital marketing services, web development services, offerings'
            },
            
            # SPECIFIC BUSINESS TYPE RESPONSES
            {
                'question': 'I have a restaurant business',
                'answer': '''
                <h4>🍕 Perfect! Here's what we recommend for restaurants:</h4>
                
                <div class="pricing-table">
                    <h4>🌟 Restaurant Growth Package</h4>
                    
                    <div class="price-item">
                        <span class="service">Restaurant Website</span>
                        <span class="price">₹20,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Online Menu Integration</span>
                        <span class="price">Included</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Online Ordering System</span>
                        <span class="price">+₹15,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Social Media Marketing</span>
                        <span class="price">₹8,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Google My Business Setup</span>
                        <span class="price">₹3,000</span>
                    </div>
                </div>
                
                <strong>Restaurant Website Features:</strong><br>
                ✅ Beautiful Food Gallery<br>
                ✅ Interactive Menu with Prices<br>
                ✅ Table Reservation System<br>
                ✅ Location & Contact Info<br>
                ✅ Customer Reviews Section<br>
                ✅ Special Offers Page<br>
                ✅ Mobile-First Design<br><br>
                
                <strong>Marketing Strategy:</strong><br>
                • Mouth-watering food photography<br>
                • Daily specials promotion<br>
                • Customer review management<br>
                • Local SEO optimization<br>
                • Event & catering promotion<br><br>
                
                <strong>Expected Results:</strong><br>
                📈 40-60% increase in orders<br>
                👥 Double your social media followers<br>
                ⭐ Improved online reputation<br><br>
                
                Want to discuss your restaurant's specific needs?
                ''',
                'keywords': 'restaurant, food business, hotel, cafe, catering, food delivery'
            },
            
            {
                'question': 'I need an e-commerce website',
                'answer': '''
                <h4>🛒 E-commerce Website Solutions</h4>
                
                <div class="pricing-table">
                    <h4>💼 E-commerce Packages</h4>
                    
                    <div class="price-item">
                        <span class="service">Basic Store (50 products)</span>
                        <span class="price">₹45,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Standard Store (200 products)</span>
                        <span class="price">₹65,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Advanced Store (Unlimited)</span>
                        <span class="price">₹85,000</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Multi-vendor Marketplace</span>
                        <span class="price">₹1,20,000</span>
                    </div>
                </div>
                
                <strong>🔥 Key Features Included:</strong><br>
                ✅ Product Catalog Management<br>
                ✅ Shopping Cart & Checkout<br>
                ✅ Payment Gateway Integration<br>
                ✅ Order Management System<br>
                ✅ Inventory Management<br>
                ✅ Customer Accounts<br>
                ✅ Wishlist & Reviews<br>
                ✅ Discount & Coupon System<br>
                ✅ Mobile Responsive Design<br>
                ✅ SEO Optimized<br><br>
                
                <strong>🚚 Payment & Shipping:</strong><br>
                • Razorpay, PayU, Paytm Integration<br>
                • COD (Cash on Delivery)<br>
                • Shipping Calculator<br>
                • Order Tracking System<br><br>
                
                <strong>📊 Free Bonus Services:</strong><br>
                • Google Analytics Setup<br>
                • Facebook Pixel Installation<br>
                • Basic SEO Setup<br>
                • Product Upload (First 50 products)<br>
                • 3 Months Free Support<br><br>
                
                <strong>💰 Marketing Add-ons:</strong><br>
                • E-commerce SEO: ₹20,000/month<br>
                • Google Shopping Ads: ₹15,000/month<br>
                • Social Media Marketing: ₹12,000/month<br><br>
                
                What type of products are you planning to sell?
                ''',
                'keywords': 'ecommerce, online store, shopping website, sell online, online business'
            },
            
            # MAINTENANCE & SUPPORT
            {
                'question': 'What about website maintenance?',
                'answer': '''
                <div class="pricing-table">
                    <h4>🔧 Website Maintenance Packages</h4>
                    
                    <div class="price-item">
                        <span class="service">Basic Maintenance</span>
                        <span class="price">₹2,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Standard Maintenance</span>
                        <span class="price">₹4,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Premium Maintenance</span>
                        <span class="price">₹7,000/month</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Emergency Support</span>
                        <span class="price">₹1,500/hour</span>
                    </div>
                </div>
                
                <strong>✅ Basic Maintenance Includes:</strong><br>
                • Regular backups<br>
                • Security updates<br>
                • Uptime monitoring<br>
                • Basic content updates<br>
                • Email support<br><br>
                
                <strong>⭐ Standard Maintenance Includes:</strong><br>
                • Everything in Basic<br>
                • Plugin/software updates<br>
                • Performance optimization<br>
                • Monthly analytics report<br>
                • Priority email support<br>
                • 2 hours content changes/month<br><br>
                
                <strong>🚀 Premium Maintenance Includes:</strong><br>
                • Everything in Standard<br>
                • Advanced security monitoring<br>
                • SEO maintenance<br>
                • Speed optimization<br>
                • Phone support<br>
                • 5 hours changes/month<br>
                • Quarterly website review<br><br>
                
                <strong>🎁 First Year FREE:</strong> All our website packages include first year maintenance absolutely free!
                ''',
                'keywords': 'maintenance, support, website maintenance, ongoing support, updates'
            },
            
            # TIMELINE & PROCESS
            {
                'question': 'How long does it take to build a website?',
                'answer': '''
                <h4>⏰ Project Timelines & Process</h4>
                
                <div class="pricing-table">
                    <h4>🚀 Development Timelines</h4>
                    
                    <div class="price-item">
                        <span class="service">Static Website (5-8 pages)</span>
                        <span class="price">7-10 days</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Dynamic Website</span>
                        <span class="price">15-20 days</span>
                    </div>
                    <div class="price-item">
                        <span class="service">E-commerce Store</span>
                        <span class="price">20-25 days</span>
                    </div>
                    <div class="price-item">
                        <span class="service">Custom Web Application</span>
                        <span class="price">30-45 days</span>
                    </div>
                </div>
                
                <strong>📋 Our 5-Step Process:</strong><br><br>
                
                <strong>Step 1: Discovery (Day 1-2)</strong><br>
                • Requirements gathering<br>
                • Design preferences<br>
                • Content collection<br>
                • Project timeline finalization<br><br>
                
                <strong>Step 2: Design (Day 3-7)</strong><br>
                • Wireframes creation<br>
                • UI/UX design<br>
                • Client approval<br>
                • Revisions if needed<br><br>
                
                <strong>Step 3: Development (Day 8-15)</strong><br>
                • Frontend development<br>
                • Backend programming<br>
                • Database setup<br>
                • Feature implementation<br><br>
                
                <strong>Step 4: Testing (Day 16-18)</strong><br>
                • Quality assurance testing<br>
                • Cross-browser testing<br>
                • Mobile responsiveness check<br>
                • Performance optimization<br><br>
                
                <strong>Step 5: Launch (Day 19-20)</strong><br>
                • Final client approval<br>
                • Domain & hosting setup<br>
                • Website launch<br>
                • Training & handover<br><br>
                
                <strong>⚡ Rush Delivery Available:</strong> Need it faster? We offer rush delivery at 50% extra cost.
                ''',
                'keywords': 'timeline, how long, development time, project duration, when ready'
            },
            
            # PAYMENT & TERMS
            {
                'question': 'What are your payment terms?',
                'answer': '''
                <div class="pricing-table">
                    <h4>💳 Payment Structure</h4>
                    
                    <strong>🏗️ Website Development:</strong><br>
                    • 50% advance payment to start<br>
                    • 50% on project completion<br><br>
                    
                    <strong>📈 Monthly Services (SEO, Marketing):</strong><br>
                    • First month advance<br>
                    • Then monthly billing<br>
                    • Quarterly payment discount: 5%<br>
                    • Yearly payment discount: 10%<br><br>
                    
                    <strong>💰 Accepted Payment Methods:</strong><br>
                    ✅ Bank Transfer (NEFT/RTGS)<br>
                    ✅ UPI (Google Pay, PhonePe, Paytm)<br>
                    ✅ Credit/Debit Cards<br>
                    ✅ Cheque<br>
                    ✅ Online Payment Gateway<br><br>
                    
                    <strong>📄 What You Get:</strong><br>
                    • GST Invoice<br>
                    • Detailed work breakdown<br>
                    • Project agreement<br>
                    • Regular progress updates<br>
                    • All source files<br><br>
                    
                    <strong>🔄 Revision Policy:</strong><br>
                    • 2 free revisions included<br>
                    • Additional revisions: ₹1,000 each<br><br>
                    
                    <strong>✅ Money-Back Guarantee:</strong><br>
                    Not satisfied? Get 100% refund within 7 days of project start.
                </div>
                
                Ready to get started? Let's discuss your project!
                ''',
                'keywords': 'payment, terms, cost, money, invoice, billing, advance, installment'
            },
            
            # CONTACT & CONSULTATION
            {
                'question': 'How can I contact you?',
                'answer': '''
                <h4>📞 Let's Connect!</h4>
                
                <div class="pricing-table">
                    <h4>🤝 Get in Touch</h4>
                    
                    <strong>📱 Phone/WhatsApp:</strong><br>
                    +91 98765 43210<br><br>
                    
                    <strong>📧 Email:</strong><br>
                    hello@yourdigitalagency.com<br>
                    quotes@yourdigitalagency.com<br><br>
                    
                    <strong>🏢 Office:</strong><br>
                    123 Business Park,<br>
                    Tech City, Your State 123456<br><br>
                    
                    <strong>⏰ Working Hours:</strong><br>
                    Monday - Saturday: 9 AM - 7 PM<br>
                    Sunday: 10 AM - 5 PM<br><br>
                    
                    <strong>💬 Social Media:</strong><br>
                    Facebook: /YourDigitalAgency<br>
                    Instagram: @yourdigitalagency<br>
                    LinkedIn: /company/yourdigitalagency<br>
                </div>
                
                <strong>🎯 Free Consultation Available!</strong><br><br>
                
                Book a free 30-minute consultation to discuss:<br>
                • Your business goals<br>
                • Digital marketing strategy<br>
                • Website requirements<br>
                • Custom pricing for your needs<br><br>
                
                <strong>📅 Schedule Your Free Call:</strong><br>
                Simply WhatsApp us or call to book your slot!<br><br>
                
                <strong>⚡ Quick Response:</strong><br>
                • WhatsApp queries: Within 1 hour<br>
                • Email queries: Within 4 hours<br>
                • Calls: Answered during business hours<br><br>
                
                What's the best way to reach you for your project discussion?
                ''',
                'keywords': 'contact, phone, email, consultation, talk, discuss, meeting, call'
            }
        ]

        created_count = 0
        updated_count = 0

        for question_data in complete_questions:
            question_obj, created = PredefinedQuestion.objects.get_or_create(
                question=question_data['question'],
                defaults={
                    'answer': question_data['answer'],
                    'keywords': question_data['keywords'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"✅ Created: {question_data['question']}")
            else:
                question_obj.answer = question_data['answer']
                question_obj.keywords = question_data['keywords']
                question_obj.is_active = True
                question_obj.save()
                updated_count += 1
                self.stdout.write(f"🔄 Updated: {question_data['question']}")

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Successfully processed {created_count + updated_count} questions!\n'
                f'📊 Created: {created_count} | Updated: {updated_count}\n'
                f'🚀 Your chatbot is now ready with complete pricing & portfolio!'
            )
        )