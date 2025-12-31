from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# Your News API key
import os
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

# Topics
topics = [
    'semiconductors US China',
    'chip technology geopolitics',
    'TSMC China Taiwan',
    'export controls semiconductors'
]

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
        all_news[topic] = articles
    
    return render_template('index.html', 
                         news_data=all_news, 
                         current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

# This lets it work on Render's servers.

## Your folder should now look like this:
"""News_Aggregator/
  ├── news_aggregator.py
  ├── app.py
  ├── requirements.txt
  └── templates/
      └── index.html

"""