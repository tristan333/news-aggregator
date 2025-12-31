import requests
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# API Keys
import os

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

# Email settings
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')

# Topics you're interested in
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
        print(f"Error fetching news: {response.status_code}")
        return []

def format_articles_html(articles, topic):
    """Format articles as HTML for email"""
    if not articles:
        return f"<h3>{topic.upper()}</h3><p>No articles found.</p>"
    
    html = f"<h2>📰 {topic.upper()}</h2><hr>"
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', 'No title')
        description = article.get('description', 'No description')
        url = article.get('url', '')
        published = article.get('publishedAt', '')
        source = article.get('source', {}).get('name', 'Unknown source')
        
        html += f"""
        <div style="margin-bottom: 20px;">
            <h3>{i}. {title}</h3>
            <p><strong>Source:</strong> {source} | <strong>Published:</strong> {published[:10]}</p>
            <p>{description}</p>
            <p><a href="{url}">Read more →</a></p>
        </div>
        """
    
    return html

def send_email(subject, html_content):
    """Send email via SendGrid"""
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject=subject,
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent successfully! Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def main():
    """Main function to run the news aggregator"""
    print("\n🌍 SEMICONDUCTOR GEOPOLITICS NEWS AGGREGATOR - Tristan Paton")
    print(f"Fetching news... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Build HTML email content
    email_html = f"""
    <html>
    <body>
        <h1>🌍 Your Daily Semiconductor Geopolitics News</h1>
        <p><em>Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</em></p>
        <hr>
    """
    
    for topic in topics:
        print(f"Fetching: {topic}...")
        articles = fetch_news(topic)
        email_html += format_articles_html(articles, topic)
    
    email_html += """
        <hr>
        <p style="color: gray; font-size: 12px;">
            This is your automated news digest. To modify topics or frequency, 
            update your news_aggregator.py script.
        </p>
    </body>
    </html>
    """
    
    # Send the email
    subject = f"📰 Semiconductor News Digest - {datetime.now().strftime('%B %d, %Y')}"
    send_email(subject, email_html)
    
    print("\n✅ News aggregation complete!")

if __name__ == "__main__":
    main()