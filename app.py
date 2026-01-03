from flask import Flask, render_template
import requests
from datetime import datetime, timedelta
import os
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

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
CACHE_DURATION = timedelta(hours=1)

def analyze_sentiment(text):
    """Analyze sentiment of text and return category and score"""
    if not text:
        return {'category': 'neutral', 'score': 0, 'label': 'NEUTRAL'}
    
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Categorize based on compound score
    if compound >= 0.05:
        category = 'positive'
        label = 'BULLISH'
    elif compound <= -0.05:
        category = 'negative'
        label = 'BEARISH'
    else:
        category = 'neutral'
        label = 'NEUTRAL'
    
    return {
        'category': category,
        'score': compound,
        'label': label
    }

def load_cache():
    """Load cached data if it exists and is still valid"""
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            
            if datetime.now() - cache_time < CACHE_DURATION:
                return cache['data']
            else:
                return None
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None

def save_cache(data):
    """Save data to cache with timestamp"""
    cache = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

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
        return response.json()['articles']
    else:
        return []

def add_sentiment_to_articles(articles):
    """Add sentiment analysis to each article"""
    for article in articles:
        # Analyze title + description for better accuracy
        text = f"{article.get('title', '')} {article.get('description', '')}"
        sentiment = analyze_sentiment(text)
        article['sentiment'] = sentiment
    
    return articles

def get_all_news():
    """Get all news - from cache if available, otherwise fetch fresh"""
    cached_data = load_cache()
    if cached_data:
        return cached_data
    
    all_news = {}
    
    for topic in topics:
        articles = fetch_news(topic)
        unique_articles = remove_duplicates(articles)
        # Add sentiment analysis
        articles_with_sentiment = add_sentiment_to_articles(unique_articles)
        all_news[topic] = articles_with_sentiment
    
    save_cache(all_news)
    return all_news

def calculate_sentiment_stats(all_news):
    """Calculate overall sentiment breakdown"""
    total = 0
    positive = 0
    negative = 0
    neutral = 0
    
    for articles in all_news.values():
        for article in articles:
            total += 1
            category = article.get('sentiment', {}).get('category', 'neutral')
            if category == 'positive':
                positive += 1
            elif category == 'negative':
                negative += 1
            else:
                neutral += 1
    
    if total == 0:
        return {'positive': 0, 'negative': 0, 'neutral': 0}
    
    return {
        'positive': round((positive / total) * 100),
        'negative': round((negative / total) * 100),
        'neutral': round((neutral / total) * 100)
    }

@app.route('/')
def home():
    """Main page - shows all news"""
    all_news = get_all_news()
    sentiment_stats = calculate_sentiment_stats(all_news)
    
    return render_template('index.html', 
                         news_data=all_news,
                         sentiment_stats=sentiment_stats,
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