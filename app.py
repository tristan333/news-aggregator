from flask import Flask, render_template
import requests
from datetime import datetime
import os

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

@app.route('/')
def home():
    """Main page - shows all news"""
    all_news = {}
    
    for topic in topics:
        articles = fetch_news(topic)
        all_news[topic] = remove_duplicates(articles)
    
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