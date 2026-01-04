# Semiconductor Intelligence Terminal

> A real-time intelligence aggregation platform tracking semiconductor geopolitics, US-China tech competition, and global chip supply chains.

🔗 **[Live Terminal](https://news-aggregator-ru4n.onrender.com/)** | 📊 **[View Source](https://github.com/tristan333/news-aggregator)**

![Terminal Interface](https://img.shields.io/badge/Status-Live-00ff88?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python) ![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)

---

## 📋 Overview

Professional Bloomberg-style web terminal that aggregates semiconductor news across four critical domains: US-China tech relations, export controls, TSMC/Taiwan dynamics, and chip technology geopolitics. Built with real-time data aggregation, NLP-powered sentiment analysis, and intelligent caching.

**Key Use Case:** Real-time monitoring of the semiconductor arms race—where silicon has become as strategic as oil, and manufacturing capability translates directly to economic and military power.

---

## ✨ Features

### 🔍 **Intelligence Gathering**
- **Multi-source aggregation** via NewsAPI with automatic deduplication
- **Smart caching** (1-hour intervals) to optimize API usage
- **Four topic streams**: Semiconductors & US-China, Chip Geopolitics, TSMC/Taiwan, Export Controls
- **Real-time updates** with live status indicators

### 🧠 **Machine Learning & NLP**
- **VADER sentiment analysis** on every article (trained for news/social media)
- **Automatic classification**: BULLISH, BEARISH, or NEUTRAL
- **Sentiment dashboard** showing aggregate market mood
- **Color-coded indicators** for instant visual parsing

### 🎨 **Terminal Interface**
- **Bloomberg-inspired design** with professional dark theme
- **Multi-page navigation**: Feed, Saved Articles, About
- **Live search & filtering** by keyword, source, or date
- **Responsive mobile design** optimized for all devices

### 💾 **Personal Features**
- **Save articles** with localStorage (browser-based bookmarking)
- **Saved articles page** with remove/clear functionality
- **Automated email digests** (separate cron-scheduled script)
- **Custom topic tracking** across geopolitical developments

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10, Flask 3.0 |
| **ML/NLP** | VADER Sentiment Analysis |
| **Data Source** | NewsAPI (with intelligent caching) |
| **Email** | SendGrid API |
| **Frontend** | Custom HTML/CSS (terminal aesthetic) |
| **Fonts** | IBM Plex Mono, Inter |
| **Deployment** | Render (with PostgreSQL option) |
| **Version Control** | Git, GitHub Actions ready |

---

## 🚀 Live Demo

**Main Terminal:** https://news-aggregator-ru4n.onrender.com/

### Pages:
- `/` - Live news feed with search/filter
- `/saved` - Your bookmarked articles
- `/about` - Project documentation & methodology

---

## 📊 How It Works

### Data Pipeline:
```
NewsAPI → Cache (1hr) → Sentiment Analysis → Deduplication → Terminal UI
```

1. **Fetches** articles from NewsAPI for 4 keyword queries
2. **Caches** results for 1 hour (reduces API calls from 100+/day to ~96/day)
3. **Analyzes** sentiment using VADER NLP model
4. **Deduplicates** articles across topics
5. **Displays** in professional terminal interface

### Sentiment Analysis:
Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to classify articles:
- **BULLISH** (Compound score ≥ 0.05): Positive developments, breakthroughs, partnerships
- **BEARISH** (Compound score ≤ -0.05): Restrictions, tensions, supply chain issues
- **NEUTRAL** (|score| < 0.05): Factual reporting without directional bias

---

## 💻 Local Development

### Prerequisites:
```bash
Python 3.10+
NewsAPI key (free tier: 100 requests/day)
SendGrid key (optional, for email digests)
```

### Setup:
```bash
# Clone repository
git clone https://github.com/tristan333/news-aggregator.git
cd news-aggregator

# Install dependencies
pip3 install -r requirements.txt

# Set environment variable
export NEWS_API_KEY='your_key_here'

# Run locally
python3 app.py
```

Visit `http://localhost:5000`

---

## 📧 Email Automation (Optional)

The `news_aggregator.py` script can be scheduled for daily digests:
```bash
# Set up cron job (macOS/Linux)
crontab -e

# Add this line for 8am daily digest
0 8 * * * NEWS_API_KEY='your_key' SENDGRID_API_KEY='your_key' python3 /path/to/news_aggregator.py
```

---

## 🎯 Skills Demonstrated

This project showcases capabilities directly relevant to solutions engineering and data infrastructure:

✅ **API Integration** - RESTful API consumption, rate limiting, error handling  
✅ **Data Processing** - Deduplication algorithms, text processing, caching strategies  
✅ **Machine Learning** - NLP sentiment analysis, model integration  
✅ **Web Development** - Multi-page Flask apps, responsive design, UX/UI  
✅ **DevOps** - Environment variable management, deployment pipelines, Git workflow  
✅ **Database Design** - localStorage implementation (PostgreSQL upgrade path ready)  

---

## 🔮 Future Enhancements

- [ ] Historical article database with PostgreSQL
- [ ] User authentication and multi-user support
- [ ] Advanced data visualization (charts, trend analysis)
- [ ] Custom topic management and alerts
- [ ] Export functionality (PDF, CSV)
- [ ] RSS feed integration for additional sources
- [ ] Keyword-based email notifications

---

## 👤 Author

**Tristan Paton**  
Data Analyst @ Chronograph | Geopolitics Researcher

Working on data systems and API integrations for private capital markets. Background in Computer Science and French from Denison University.

- 💼 [LinkedIn](https://www.linkedin.com/in/tristanpaton/)
- 📧 [Email](mailto:tristanpaton0@gmail.com)
- 🌐 [GitHub Profile](https://github.com/tristan333)

---

## 📄 License

This project is open source and available for educational purposes. Built in public as a learning exercise in API integration, web development, and NLP.

---

**⚡ Deployed on Render | Powered by NewsAPI**
