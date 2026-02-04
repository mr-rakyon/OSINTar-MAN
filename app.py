from flask import Flask, render_template, request, jsonify, session, send_file
from playwright.sync_api import sync_playwright
from functools import wraps
import json
import time
import re
from datetime import datetime, timedelta
import hashlib
from io import BytesIO
import csv
from models.values import *
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Cache for search results to improve performance
search_cache = {}

# Enhanced classification function with more categories
def classify_site(link, title):
    link_lower = link.lower()
    title_lower = title.lower()

    # -------------------------------- Social Media Sites ---------------------------
    social_sites = SOCIAL_SITES

    for site, keywords in social_sites.items():
        if any(k in link_lower or k in title_lower for k in keywords):
            return site
    
    # ------------------------------- Education Sites ---------------------------------
    education_sites = EDUCATION_SITES

    for site, keywords in education_sites.items():
        if any(k in link_lower or k in title_lower for k in keywords):
            return site

    # ------------------------------- News & Media Sites ---------------------------------
    news_sites =NEWS_SITES

    for site, keywords in news_sites.items():
        if any(k in link_lower or k in title_lower for k in keywords):
            return site
        
    # ------------------------------- Government & Official Sites ---------------------------------
    gov_sites = GOV_SITES

    for site_type, keywords in gov_sites.items():
        if any(k in link_lower or k in title_lower for k in keywords):
            return site_type
    
    # ------------------------------- E-commerce & Business ---------------------------------
    business_sites = BUSINESS_SITES
    for site, keywords in business_sites.items():
        if any(k in link_lower or k in title_lower for k in keywords):
            return site
        
    # ------------------------------- Technology & Development ---------------------------------
    tech_sites = TECH_SITES

    for site, keywords in tech_sites.items():
        if any(k in link_lower or k in title_lower for k in keywords):
            return site
        
    # ------------------------------- Emails ---------------------------------
    email_patterns = EMAIL_PATTERNS
    
    for pattern in email_patterns:
        if re.search(pattern, link_lower) or pattern in title_lower:
            return "Email"
    
    # -------------------------------- Phone Numbers ---------------------------------
    phone_patterns = PHONE_PATTERNS
    
    for pattern in phone_patterns:
        if re.search(pattern, link_lower) or (isinstance(pattern, str) and pattern in title_lower):
            return "Phone Number"
    
    # -------------------------------- Documents ---------------------------------
    document_patterns = DOCUMENT_PATTERNS
    
    for pattern in document_patterns:
        if re.search(pattern, link_lower) or pattern in title_lower:
            return "Document"
    
    # -------------------------------- Images & Media ---------------------------------
    media_patterns = MEDIA_PATTERNS

    for pattern in media_patterns:
        if re.search(pattern, link_lower) or pattern in title_lower:
            return "Media File"
    
    # -------------------------------- Search Engines ---------------------------------
    search_engines = SEARCH_ENGINES
    
    for engine, keywords in search_engines.items():
        if any(k in link_lower for k in keywords):
            return f"Search Engine ({engine})"
        
    # -------------------------------- Maps & Location ---------------------------------
    location_patterns = LOCATION_PATTERNS
    
    for pattern in location_patterns:
        if pattern in link_lower or pattern in title_lower:
            return "Map/Location"
    
    # -------------------------------- Forums & Communities ---------------------------------
    forum_patterns = FORUM_PATTERNS
    
    for pattern in forum_patterns:
        if pattern in link_lower or pattern in title_lower:
            return "Forum/Community"
    
    # Check for specific domains
    domain_patterns = DOMAIN_PATTERNS
    
    for site, patterns in domain_patterns.items():
        if any(pattern in link_lower for pattern in patterns):
            return site
    
    # Default categories based on TLD
    tld_categories = {
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
    
    for tld, category in tld_categories.items():
        if link_lower.endswith(tld):
            return category
    
    return "Website"

# Calculate confidence score based on various factors
def calculate_confidence(link, title, site_type):
    confidence = 80  # Base confidence
    
    # Increase confidence for reputable domains
    reputable_domains = ['.gov', '.edu', '.org', 'wikipedia.org', 'github.com']
    if any(domain in link.lower() for domain in reputable_domains):
        confidence += 15
    
    # Decrease confidence for suspicious patterns
    suspicious_patterns = ['bit.ly', 'tinyurl', 'ow.ly', 'shorte.st', 'adf.ly']
    if any(pattern in link.lower() for pattern in suspicious_patterns):
        confidence -= 20
    
    # Adjust based on title length (longer titles often more informative)
    if len(title) > 50:
        confidence += 5
    elif len(title) < 10:
        confidence -= 10
    
    # Specific type adjustments
    if site_type in ["Government Site", "Educational Institution"]:
        confidence += 10
    elif site_type in ["Email", "Phone Number"]:
        confidence -= 5
    
    # Ensure confidence stays within bounds
    return max(30, min(100, confidence))

# Calculate relevance score based on query
def calculate_relevance(query, title, link):
    query_terms = query.lower().split()
    title_lower = title.lower()
    link_lower = link.lower()
    
    relevance = 0
    
    # Check for exact matches
    for term in query_terms:
        if term in title_lower:
            relevance += 15
        if term in link_lower:
            relevance += 10
    
    # Check for partial matches
    for term in query_terms:
        if any(term in word for word in title_lower.split()):
            relevance += 8
        if any(term in word for word in link_lower.split()):
            relevance += 5
    
    # Bonus for exact phrase match
    if query.lower() in title_lower:
        relevance += 25
    
    # Adjust based on position in title
    for i, term in enumerate(query_terms):
        if term in title_lower:
            position = title_lower.find(term) / len(title_lower)
            relevance += int((1 - position) * 10)
    
    return min(100, relevance)

# Assess risk level based on various factors
def assess_risk_level(link, title, site_type):
    # High risk indicators
    high_risk_indicators = [
        'hack', 'leak', 'breach', 'password', 'credit card',
        'social security', 'ssn', 'dox', 'personal information',
        'private data', 'confidential', 'secret', 'classified'
    ]
    
    medium_risk_indicators = [
        'crack', 'keygen', 'serial', 'pirate', 'torrent',
        'free download', 'cracked', 'nulled', 'warez'
    ]
    
    # Check title for risk indicators
    title_lower = title.lower()
    
    for indicator in high_risk_indicators:
        if indicator in title_lower:
            return "High"
    
    for indicator in medium_risk_indicators:
        if indicator in title_lower:
            return "Medium"
    
    # Check link for suspicious patterns
    suspicious_domains = [
        'onion', 'tor', 'i2p', 'darkweb', 'darknet',
        'bitcoin mix', 'cryptocurrency scam'
    ]
    
    for domain in suspicious_domains:
        if domain in link.lower():
            return "High"
    
    # Check site type
    if site_type in ["Email", "Phone Number", "Document"]:
        return "Medium"
    
    return "Low"

# Get popularity score (simulated)
def get_popularity_score():
    return 50 + hash(str(time.time())) % 50  # Random between 50-100

# Enhanced OSINT function with multiple search engines
def enhanced_osint_search(query, pages=2, search_engine="duckduckgo"):
    cache_key = f"{query}_{pages}_{search_engine}"
    
    # Check cache first
    if cache_key in search_cache:
        cached_time, results = search_cache[cache_key]
        if time.time() - cached_time < 300:  # 5 minute cache
            return results
    
    all_results = []
    
    try:
        with sync_playwright() as pr:
            browser = pr.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
            page = context.new_page()
            
            # Select search engine URL
            if search_engine == "google":
                search_url = f"https://www.google.com/search?q={query}"
            elif search_engine == "bing":
                search_url = f"https://www.bing.com/search?q={query}"
            else:  # duckduckgo default
                search_url = f"https://duckduckgo.com/?q={query}&t=h_&ia=web"
            
            page.goto(search_url, timeout=60000, wait_until="domcontentloaded")
            
            for page_num in range(pages):
                try:
                    # Wait for results with different selectors for different engines
                    if search_engine == "google":
                        page.wait_for_selector('div.g', timeout=10000)
                        results = page.query_selector_all('div.g')
                        for result in results:
                            try:
                                title_elem = result.query_selector('h3')
                                link_elem = result.query_selector('a')
                                snippet_elem = result.query_selector('.VwiC3b')
                                
                                if title_elem and link_elem:
                                    title = title_elem.inner_text()
                                    link = link_elem.get_attribute('href')
                                    snippet = snippet_elem.inner_text() if snippet_elem else ""
                                    
                                    if link and not link.startswith('http'):
                                        continue
                                    
                                    site_type = classify_site(link, title)
                                    confidence = calculate_confidence(link, title, site_type)
                                    relevance = calculate_relevance(query, title, link)
                                    risk_level = assess_risk_level(link, title, site_type)
                                    popularity = get_popularity_score()
                                    timestamp = datetime.now().isoformat()
                                    
                                    all_results.append({
                                        'title': title,
                                        'link': link,
                                        'snippet': snippet,
                                        'type': site_type,
                                        'confidence': confidence,
                                        'relevance': relevance,
                                        'risk_level': risk_level,
                                        'popularity': popularity,
                                        'timestamp': timestamp,
                                        'search_engine': search_engine,
                                        'id': hashlib.md5(f"{link}{title}".encode()).hexdigest()[:12]
                                    })
                            except Exception as e:
                                continue
                    
                    elif search_engine == "bing":
                        page.wait_for_selector('li.b_algo', timeout=10000)
                        results = page.query_selector_all('li.b_algo')
                        for result in results:
                            try:
                                title_elem = result.query_selector('h2 a')
                                link_elem = result.query_selector('h2 a')
                                snippet_elem = result.query_selector('.b_caption p')
                                
                                if title_elem and link_elem:
                                    title = title_elem.inner_text()
                                    link = link_elem.get_attribute('href')
                                    snippet = snippet_elem.inner_text() if snippet_elem else ""
                                    
                                    if link and not link.startswith('http'):
                                        continue
                                    
                                    site_type = classify_site(link, title)
                                    confidence = calculate_confidence(link, title, site_type)
                                    relevance = calculate_relevance(query, title, link)
                                    risk_level = assess_risk_level(link, title, site_type)
                                    popularity = get_popularity_score()
                                    timestamp = datetime.now().isoformat()
                                    
                                    all_results.append({
                                        'title': title,
                                        'link': link,
                                        'snippet': snippet,
                                        'type': site_type,
                                        'confidence': confidence,
                                        'relevance': relevance,
                                        'risk_level': risk_level,
                                        'popularity': popularity,
                                        'timestamp': timestamp,
                                        'search_engine': search_engine,
                                        'id': hashlib.md5(f"{link}{title}".encode()).hexdigest()[:12]
                                    })
                            except Exception as e:
                                continue
                    
                    else:  # duckduckgo
                        page.wait_for_selector('article[data-testid="result"]', timeout=10000)
                        results = page.query_selector_all('article[data-testid="result"]')
                        for result in results:
                            try:
                                title_element = result.query_selector('h2 a')
                                link_element = result.query_selector('h2 a')
                                snippet_element = result.query_selector('[data-testid="result-snippet"]')
                                
                                if title_element and link_element:
                                    title = title_element.inner_text()
                                    link = link_element.get_attribute('href')
                                    snippet = snippet_element.inner_text() if snippet_element else ""
                                    
                                    if link and not link.startswith('http'):
                                        continue
                                    
                                    site_type = classify_site(link, title)
                                    confidence = calculate_confidence(link, title, site_type)
                                    relevance = calculate_relevance(query, title, link)
                                    risk_level = assess_risk_level(link, title, site_type)
                                    popularity = get_popularity_score()
                                    timestamp = datetime.now().isoformat()
                                    
                                    all_results.append({
                                        'title': title,
                                        'link': link,
                                        'snippet': snippet,
                                        'type': site_type,
                                        'confidence': confidence,
                                        'relevance': relevance,
                                        'risk_level': risk_level,
                                        'popularity': popularity,
                                        'timestamp': timestamp,
                                        'search_engine': search_engine,
                                        'id': hashlib.md5(f"{link}{title}".encode()).hexdigest()[:12]
                                    })
                            except Exception as e:
                                continue
                    
                    # Try to go to next page
                    if page_num < pages - 1:
                        if search_engine == "google":
                            next_button = page.query_selector('#pnnext')
                        elif search_engine == "bing":
                            next_button = page.query_selector('a.sb_pagN')
                        else:  # duckduckgo
                            next_button = page.query_selector('button#more-results')
                        
                        if next_button:
                            next_button.click()
                            page.wait_for_timeout(3000)
                        else:
                            break
                            
                except Exception as e:
                    print(f"Error on page {page_num}: {e}")
                    continue
            
            browser.close()
            
            # Cache results
            search_cache[cache_key] = (time.time(), all_results)
            
            return all_results
            
    except Exception as e:
        print(f"Error during enhanced OSINT execution: {e}")
        return []

# Generate analytics data
def generate_analytics_data(results):
    if not results:
        return {}
    
    analytics = {
        'total_results': len(results),
        'categories': {},
        'risk_distribution': {'High': 0, 'Medium': 0, 'Low': 0},
        'confidence_stats': {
            'average': 0,
            'min': 100,
            'max': 0
        },
        'relevance_stats': {
            'average': 0,
            'min': 100,
            'max': 0
        },
        'search_engines': {},
        'timeline_data': []
    }
    
    total_confidence = 0
    total_relevance = 0
    
    for result in results:
        # Categories
        cat = result['type']
        analytics['categories'][cat] = analytics['categories'].get(cat, 0) + 1
        
        # Risk distribution
        risk = result['risk_level']
        analytics['risk_distribution'][risk] = analytics['risk_distribution'].get(risk, 0) + 1
        
        # Confidence stats
        conf = result['confidence']
        total_confidence += conf
        analytics['confidence_stats']['min'] = min(analytics['confidence_stats']['min'], conf)
        analytics['confidence_stats']['max'] = max(analytics['confidence_stats']['max'], conf)
        
        # Relevance stats
        rel = result['relevance']
        total_relevance += rel
        analytics['relevance_stats']['min'] = min(analytics['relevance_stats']['min'], rel)
        analytics['relevance_stats']['max'] = max(analytics['relevance_stats']['max'], rel)
        
        # Search engines
        engine = result.get('search_engine', 'duckduckgo')
        analytics['search_engines'][engine] = analytics['search_engines'].get(engine, 0) + 1
    
    # Calculate averages
    analytics['confidence_stats']['average'] = round(total_confidence / len(results), 2)
    analytics['relevance_stats']['average'] = round(total_relevance / len(results), 2)
    
    # Generate timeline data (last 7 days)
    today = datetime.now()
    for i in range(7):
        date = today - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        count = len([r for r in results if r['timestamp'].startswith(date_str)])
        analytics['timeline_data'].append({
            'date': date_str,
            'count': count
        })
    
    # Sort categories by count
    analytics['categories'] = dict(sorted(
        analytics['categories'].items(),
        key=lambda x: x[1],
        reverse=True
    ))
    
    return analytics

# Generate intelligence report
def generate_intelligence_report(results, query):
    report = {
        'query': query,
        'generated_at': datetime.now().isoformat(),
        'executive_summary': {},
        'key_findings': [],
        'recommendations': [],
        'statistics': {},
        'threat_assessment': {}
    }
    
    if not results:
        report['executive_summary'] = {
            'status': 'No results found',
            'message': f'No OSINT data found for query: {query}'
        }
        return report
    
    # Executive Summary
    total_results = len(results)
    high_risk = len([r for r in results if r['risk_level'] == 'High'])
    medium_risk = len([r for r in results if r['risk_level'] == 'Medium'])
    avg_confidence = sum(r['confidence'] for r in results) / total_results
    
    report['executive_summary'] = {
        'status': 'Analysis Complete',
        'total_results': total_results,
        'high_risk_items': high_risk,
        'medium_risk_items': medium_risk,
        'average_confidence': round(avg_confidence, 2),
        'unique_categories': len(set(r['type'] for r in results))
    }
    
    # Key Findings
    # 1. Most common categories
    categories = {}
    for r in results:
        cat = r['type']
        categories[cat] = categories.get(cat, 0) + 1
    
    top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
    report['key_findings'].append({
        'title': 'Top Information Sources',
        'description': f'Information primarily from: {", ".join([c[0] for c in top_categories])}'
    })
    
    # 2. High risk findings
    if high_risk > 0:
        high_risk_items = [r for r in results if r['risk_level'] == 'High']
        report['key_findings'].append({
            'title': 'High Risk Items Detected',
            'description': f'Found {high_risk} high-risk items requiring immediate attention',
            'details': [{'title': r['title'], 'link': r['link']} for r in high_risk_items[:3]]
        })
    
    # 3. Confidence analysis
    high_confidence = len([r for r in results if r['confidence'] >= 80])
    report['key_findings'].append({
        'title': 'Data Reliability',
        'description': f'{high_confidence} of {total_results} results ({high_confidence/total_results*100:.1f}%) have high confidence scores'
    })
    
    # Recommendations
    if high_risk > 0:
        report['recommendations'].append({
            'priority': 'High',
            'action': 'Immediate review of high-risk items',
            'details': 'High-risk items may contain sensitive or dangerous information'
        })
    
    if avg_confidence < 70:
        report['recommendations'].append({
            'priority': 'Medium',
            'action': 'Verify low-confidence sources',
            'details': 'Consider cross-referencing information from multiple sources'
        })
    
    report['recommendations'].append({
        'priority': 'Low',
        'action': 'Regular monitoring',
        'details': 'Set up alerts for new information related to this query'
    })
    
    # Statistics
    report['statistics'] = {
        'total_results': total_results,
        'by_category': categories,
        'by_risk': {
            'High': high_risk,
            'Medium': medium_risk,
            'Low': total_results - high_risk - medium_risk
        },
        'confidence_distribution': {
            'High (80-100)': len([r for r in results if r['confidence'] >= 80]),
            'Medium (60-79)': len([r for r in results if 60 <= r['confidence'] < 80]),
            'Low (<60)': len([r for r in results if r['confidence'] < 60])
        }
    }
    
    # Threat Assessment
    report['threat_assessment'] = {
        'overall_risk': 'High' if high_risk > 0 else 'Medium' if medium_risk > 0 else 'Low',
        'factors': [
            f'{high_risk} high-risk items found',
            f'{medium_risk} medium-risk items found',
            f'Average confidence: {avg_confidence:.1f}%'
        ],
        'recommended_actions': [r['action'] for r in report['recommendations']]
    }
    
    return report

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.form.get('query', '').strip()
        pages = int(request.form.get('pages', 2))
        search_engine = request.form.get('search_engine', 'duckduckgo')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Perform search
        results = enhanced_osint_search(query, pages, search_engine)
        
        # Generate analytics
        analytics = generate_analytics_data(results)
        
        # Store in session for export
        session['last_search'] = {
            'query': query,
            'results': results,
            'analytics': analytics,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': results,
            'analytics': analytics,
            'metadata': {
                'query': query,
                'total_results': len(results),
                'search_time': datetime.now().isoformat(),
                'pages_searched': pages,
                'search_engine': search_engine
            }
        })
        
    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    if 'last_search' not in session:
        return jsonify({'error': 'No search data available'}), 400
    
    search_data = session['last_search']
    return jsonify({
        'analytics': search_data['analytics'],
        'metadata': {
            'query': search_data['query'],
            'timestamp': search_data['timestamp']
        }
    })

@app.route('/report', methods=['GET'])
def get_report():
    if 'last_search' not in session:
        return jsonify({'error': 'No search data available'}), 400
    
    search_data = session['last_search']
    report = generate_intelligence_report(search_data['results'], search_data['query'])
    
    return jsonify({
        'report': report,
        'metadata': {
            'query': search_data['query'],
            'timestamp': search_data['timestamp']
        }
    })

@app.route('/export/<format_type>', methods=['GET'])
def export_data(format_type):
    if 'last_search' not in session:
        return jsonify({'error': 'No search data available'}), 400
    
    search_data = session['last_search']
    results = search_data['results']
    
    if format_type == 'json':
        import io
        output = io.StringIO()
        json.dump({
            'query': search_data['query'],
            'timestamp': search_data['timestamp'],
            'results': results,
            'analytics': search_data['analytics']
        }, output, indent=2)
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'osint_report_{search_data["query"]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
    
    elif format_type == 'csv':
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Title', 'Link', 'Type', 'Risk Level', 'Confidence', 'Relevance', 'Timestamp', 'Snippet'])
        
        # Write data
        for result in results:
            writer.writerow([
                result['title'],
                result['link'],
                result['type'],
                result['risk_level'],
                result['confidence'],
                result['relevance'],
                result['timestamp'],
                result.get('snippet', '')[:100]  # Truncate long snippets
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'osint_data_{search_data["query"]}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    elif format_type == 'pdf':
        # In production, use reportlab or similar to generate PDF
        return jsonify({'error': 'PDF export not implemented'}), 501
    
    else:
        return jsonify({'error': 'Unsupported format'}), 400

@app.route('/profile/save', methods=['POST'])
def save_profile():
    try:
        profile_data = request.json
        if not profile_data:
            return jsonify({'error': 'No profile data provided'}), 400
        
        # Store in session (in production, store in database)
        if 'profiles' not in session:
            session['profiles'] = []
        
        profile_data['id'] = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        profile_data['created_at'] = datetime.now().isoformat()
        
        session['profiles'].append(profile_data)
        session.modified = True
        
        return jsonify({
            'success': True,
            'profile_id': profile_data['id'],
            'message': 'Profile saved successfully'
        })
        
    except Exception as e:
        print(f"Error saving profile: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/profile/list', methods=['GET'])
def list_profiles():
    profiles = session.get('profiles', [])
    return jsonify({
        'profiles': profiles,
        'count': len(profiles)
    })

@app.route('/profile/load/<profile_id>', methods=['GET'])
def load_profile(profile_id):
    profiles = session.get('profiles', [])
    profile = next((p for p in profiles if p.get('id') == profile_id), None)
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    return jsonify({
        'success': True,
        'profile': profile
    })

@app.route('/history', methods=['GET'])
def get_history():
    # In production, store in database
    history = session.get('search_history', [])
    return jsonify({
        'history': history[-10:],  # Last 10 searches
        'total': len(history)
    })

@app.route('/ai/analyze', methods=['POST'])
def ai_analyze():
    try:
        data = request.json
        query = data.get('query', '')
        
        if 'last_search' not in session:
            return jsonify({'error': 'No search data available'}), 400
        
        search_data = session['last_search']
        results = search_data['results']
        
        # Simple AI analysis (in production, use actual AI)
        analysis = {
            'query': query,
            'analysis': f"Based on {len(results)} results, I've identified key patterns in the data.",
            'patterns': [],
            'insights': [],
            'recommendations': []
        }
        
        if results:
            # Analyze categories
            categories = {}
            for r in results:
                cat = r['type']
                categories[cat] = categories.get(cat, 0) + 1
            
            top_category = max(categories.items(), key=lambda x: x[1])
            analysis['patterns'].append(f"Most information comes from {top_category[0]} sources ({top_category[1]} results)")
            
            # Analyze risk
            high_risk = len([r for r in results if r['risk_level'] == 'High'])
            if high_risk > 0:
                analysis['insights'].append(f"Found {high_risk} high-risk items requiring attention")
            
            # Generate recommendations
            avg_conf = sum(r['confidence'] for r in results) / len(results)
            if avg_conf < 70:
                analysis['recommendations'].append("Verify information from multiple sources due to low average confidence")
            else:
                analysis['recommendations'].append("Data shows good reliability based on confidence scores")
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        # Get current settings
        settings = session.get('settings', {
            'default_pages': 2,
            'default_search_engine': 'duckduckgo',
            'privacy_level': 'medium',
            'auto_save': True,
            'notifications': True,
            'theme': 'dark'
        })
        return jsonify({'settings': settings})
    
    elif request.method == 'POST':
        # Update settings
        new_settings = request.json
        if not new_settings:
            return jsonify({'error': 'No settings provided'}), 400
        
        current_settings = session.get('settings', {})
        current_settings.update(new_settings)
        session['settings'] = current_settings
        session.modified = True
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully',
            'settings': current_settings
        })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)