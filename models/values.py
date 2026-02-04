 # -------------------------------- Social Media Sites ---------------------------
SOCIAL_SITES = {
    "Facebook": ["facebook.com", "fb.com"],
    "Twitter": ["twitter.com", "t.co", "x.com"],
    "Instagram": ["instagram.com", "instagr.am"],
    "LinkedIn": ["linkedin.com", "lnkd.in"],
    "Snapchat": ["snapchat.com"],
    "TikTok": ["tiktok.com"],
    "Reddit": ["reddit.com", "redd.it"],
    "Pinterest": ["pinterest.com", "pin.it"],
    "YouTube": ["youtube.com", "youtu.be"],
    "WhatsApp": ["whatsapp.com", "wa.me"],
    "Telegram": ["telegram.org", "t.me"],
    "Discord": ["discord.com", "discord.gg"],
    "Twitch": ["twitch.tv"],
    "GitHub": ["github.com"],
    "StackOverflow": ["stackoverflow.com"],
    "Medium": ["medium.com"],
    "Quora": ["quora.com"],
    "Tumblr": ["tumblr.com"],
    "Flickr": ["flickr.com"],
    "VK": ["vk.com"],
    "Weibo": ["weibo.com"],
    "Line": ["line.me"],
    "Signal": ["signal.org"],
    "Slack": ["slack.com"],
    "Teams": ["teams.microsoft.com"],
    "Zoom": ["zoom.us"],
    "Skype": ["skype.com"],
    "Meet": ["meet.google.com"],
}
# ------------------------------- Education Sites ---------------------------------
EDUCATION_SITES = {
    "Khan Academy": ["khanacademy.org"],
    "Coursera": ["coursera.org"],
    "edX": ["edx.org"],
    "Udemy": ["udemy.com"],
    "LinkedIn Learning": ["linkedin.com/learning"],
    "Duolingo": ["duolingo.com"],
    "Codecademy": ["codecademy.com"],
    "Udacity": ["udacity.com"],
    "FutureLearn": ["futurelearn.com"],
    "Skillshare": ["skillshare.com"],
    "Pluralsight": ["pluralsight.com"],
    "Brilliant": ["brilliant.org"],
    "MIT OpenCourseWare": ["ocw.mit.edu"],
    "Stanford Online": ["online.stanford.edu"],
    "Harvard Online": ["online-learning.harvard.edu"],
    "Coursera": ["coursera.org"],
    "edX": ["edx.org"],
    "Academic Earth": ["academicearth.org"],
    "Open Culture": ["openculture.com"],
    "Alison": ["alison.com"],
    "GCFGlobal": ["edu.gcfglobal.org"],
}
# ------------------------------- News & Media Sites ---------------------------------
NEWS_SITES = {
    "CNN": ["cnn.com"],
    "BBC": ["bbc.com", "bbc.co.uk"],
    "The New York Times": ["nytimes.com"],
    "The Guardian": ["theguardian.com"],
    "Reuters": ["reuters.com"],
    "Al Jazeera": ["aljazeera.com"],
    "Fox News": ["foxnews.com"],
    "NBC News": ["nbcnews.com"],
    "CBS News": ["cbsnews.com"],
    "ABC News": ["abcnews.go.com"],
    "The Washington Post": ["washingtonpost.com"],
    "The Wall Street Journal": ["wsj.com"],
    "Bloomberg": ["bloomberg.com"],
    "Forbes": ["forbes.com"],
    "Business Insider": ["businessinsider.com"],
    "TechCrunch": ["techcrunch.com"],
    "Wired": ["wired.com"],
    "The Verge": ["theverge.com"],
    "Ars Technica": ["arstechnica.com"],
    "Mashable": ["mashable.com"],
    "BuzzFeed": ["buzzfeed.com"],
    "HuffPost": ["huffpost.com"],
    "Politico": ["politico.com"],
    "Axios": ["axios.com"],
    "NPR": ["npr.org"],
    "AP News": ["apnews.com"],
    "USA Today": ["usatoday.com"],
    "Time": ["time.com"],
    "Newsweek": ["newsweek.com"],
}
# ------------------------------- Government & Official Sites ---------------------------------
GOV_SITES = {
    "Government Site": [".gov", ".gob", ".govt", "official website", "government portal"],
    "Educational Institution": [".edu", "university", "college", "academy", "institute"],
    "Organization": [".org", "non-profit", "foundation", "association"],
    "Military": [".mil", "army", "navy", "airforce", "military"],
    "Health Organization": [".health", "hospital", "clinic", "medical center", "who.int"],
    "UN Organizations": ["un.org", "unesco.org", "who.int", "unicef.org"],
}
# ------------------------------- E-commerce & Business ---------------------------------
BUSINESS_SITES = {
    "Amazon": ["amazon.com", "amazon."],
    "eBay": ["ebay.com"],
    "AliExpress": ["aliexpress.com"],
    "Shopify": ["shopify.com"],
    "Etsy": ["etsy.com"],
    "Walmart": ["walmart.com"],
    "Target": ["target.com"],
    "Best Buy": ["bestbuy.com"],
    "Apple Store": ["apple.com/shop"],
    "Microsoft Store": ["microsoftstore.com"],
    "Google Store": ["store.google.com"],
    "Booking.com": ["booking.com"],
    "Airbnb": ["airbnb.com"],
    "Uber": ["uber.com"],
    "Lyft": ["lyft.com"],
    "DoorDash": ["doordash.com"],
    "Grubhub": ["grubhub.com"],
    "PayPal": ["paypal.com"],
    "Stripe": ["stripe.com"],
    "Square": ["square.com"],
}
# ------------------------------- Technology & Development ---------------------------------
TECH_SITES = {
    "GitHub": ["github.com"],
    "GitLab": ["gitlab.com"],
    "Bitbucket": ["bitbucket.org"],
    "Stack Overflow": ["stackoverflow.com"],
    "Stack Exchange": ["stackexchange.com"],
    "DEV Community": ["dev.to"],
    "Hacker News": ["news.ycombinator.com"],
    "Product Hunt": ["producthunt.com"],
    "npm": ["npmjs.com"],
    "PyPI": ["pypi.org"],
    "Docker Hub": ["hub.docker.com"],
    "Kubernetes": ["kubernetes.io"],
    "AWS": ["aws.amazon.com"],
    "Google Cloud": ["cloud.google.com"],
    "Azure": ["azure.microsoft.com"],
    "DigitalOcean": ["digitalocean.com"],
    "Heroku": ["heroku.com"],
    "Vercel": ["vercel.com"],
    "Netlify": ["netlify.com"],
}
# ------------------------------- Emails ---------------------------------
EMAIL_PATTERNS = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "mailto:",
    "email",
    "inbox",
    "compose",
    "sent mail",
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "protonmail.com"
]
# -------------------------------- Phone Numbers ---------------------------------
PHONE_PATTERNS = [
    r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
    r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
    "tel:",
    "call",
    "phone",
    "mobile",
    "contact number",
    "whatsapp",
    "telephone"
]
# -------------------------------- Documents ---------------------------------
DOCUMENT_PATTERNS = [
    r'\.pdf$', r'\.docx?$', r'\.xlsx?$', r'\.pptx?$', 
    r'\.txt$', r'\.rtf$', r'\.odt$', r'\.csv$',
    "document", "file", "download", "report", "whitepaper"
]
# -------------------------------- Images & Media ---------------------------------
MEDIA_PATTERNS = [
    r'\.jpg$', r'\.jpeg$', r'\.png$', r'\.gif$', r'\.bmp$',
    r'\.mp4$', r'\.avi$', r'\.mov$', r'\.wmv$', r'\.flv$',
    r'\.mp3$', r'\.wav$', r'\.flac$', r'\.aac$',
    "image", "photo", "picture", "video", "audio", "media"
]
 # -------------------------------- Search Engines ---------------------------------
SEARCH_ENGINES = {
    "Google": ["google.com/search", "google.com?q="],
    "Bing": ["bing.com/search"],
    "DuckDuckGo": ["duckduckgo.com"],
    "Yahoo": ["yahoo.com/search"],
    "Yandex": ["yandex.com/search"],
    "Baidu": ["baidu.com/s"],
}
# -------------------------------- Maps & Location ---------------------------------
LOCATION_PATTERNS = [
    "maps.google", "google.com/maps", "openstreetmap",
    "map", "location", "address", "coordinates", "gps"
]
# -------------------------------- Forums & Communities ---------------------------------
FORUM_PATTERNS = [
    "forum", "board", "community", "discussion", "thread",
    "reddit.com/r/", "quora.com", "stackexchange.com"
]
# Check for specific domains
DOMAIN_PATTERNS = {
    "Wikipedia": ["wikipedia.org"],
    "Wikileaks": ["wikileaks.org"],
    "Internet Archive": ["archive.org"],
    "Wayback Machine": ["web.archive.org"],
    "Pastebin": ["pastebin.com"],
    "GitHub Pages": ["github.io"],
    "Google Sites": ["sites.google.com"],
    "Blogger": ["blogger.com"],
    "WordPress": ["wordpress.com", ".wordpress."],
    "Wix": [".wixsite.com"],
    "Squarespace": [".squarespace.com"],
}
# Default categories based on TLD
TLD_CATEGORIES = {
    ".com": "Commercial Website",
    ".org": "Organization",
    ".net": "Network Services",
    ".edu": "Education",
    ".gov": "Government",
    ".mil": "Military",
    ".io": "Tech Startup",
    ".ai": "AI/Technology",
    ".co": "Company",
    ".me": "Personal/Blog",
    ".info": "Information",
    ".biz": "Business",
    ".mobi": "Mobile",
    ".app": "Application",
    ".dev": "Development",
}




