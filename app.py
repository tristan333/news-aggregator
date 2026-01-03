from flask import Flask, render_template
import requests
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)

# Your News API key
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

# Topics
topics = [
    'semiconductors US China',
    'chip technology geopolitics',
    'TSMC China Taiwan',
    'export controls semiconductors'
]

# Cache settings
CACHE_FILE = '/tmp/news_cache.json'
CACHE_DURATION = timedelta(hours=1)  # Cache for 1 hour

def load_cache():
    """Load cached data if it exists and is still valid"""
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            
            # Check if cache is still valid
            if datetime.now() - cache_time < CACHE_DURATION:
                print(f"Using cached data from {cache_time}")
                return cache['data']
            else:
                print("Cache expired")
                return None
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        print("No valid cache found")
        return None

def save_cache(data):
    """Save data to cache with timestamp"""
    cache = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)
    print(f"Cache saved at {datetime.now()}")

def remove_duplicates(all_articles):
    """Remove duplicate articles based on title"""
    seen_titles = set()
    unique_articles = []
    
    for article in all_articles:
        title = article.get('title', '').lower().strip()
        if title and title not in seen_titles and '[removed]' not in title:
            seen_titles.add(title)
            unique_articles.append(article)
    
    return unique_articles

def fetch_news(query):
    """Fetch news articles for a given query"""
    url = f'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 5
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        articles = response.json()['articles']
        return articles
    else:
        print(f"API Error {response.status_code}: {response.text}")
        return []

def get_all_news():
    """Get all news - from cache if available, otherwise fetch fresh"""
    # Try to load from cache first
    cached_data = load_cache()
    if cached_data:
        return cached_data
    
    # Cache miss - fetch fresh data
    print("Fetching fresh data from API...")
    all_news = {}
    
    for topic in topics:
        articles = fetch_news(topic)
        all_news[topic] = remove_duplicates(articles)
    
    # Save to cache
    save_cache(all_news)
    
    return all_news

@app.route('/')
def home():
    """Main page - shows all news"""
    all_news = get_all_news()
    
    return render_template('index.html', 
                         news_data=all_news, 
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/saved')
def saved():
    """Saved articles page"""
    return render_template('saved.html',
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html',
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)