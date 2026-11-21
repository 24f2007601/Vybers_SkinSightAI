# Dot & Key Market Intelligence to Marketing Content System

An AI-powered solution that studies the market for Dot & Key products and turns insights into marketing content.

## 🎯 Problem Statement (Vibe Coders Hackathon Edition 3)

Build a solution that:
1. **Extracts** Dot & Key product catalogue from website
2. **Monitors** competitors across e-commerce marketplaces (Amazon, Flipkart, Nykaa, Purplle, Myntra)
3. **Analyzes** product info, pricing, ratings, customer reviews
4. **Identifies** top 5 competitors per product/category and compares offerings
5. **Performs sentiment analysis** on reviews to find preferences, complaints, strengths/weaknesses
6. **Generates SWOT analysis**, market gaps, emerging needs, trends, competitor launches
7. **Forecasts** sales opportunities
8. **Generates marketing content**: static ads, product descriptions, A+ content, ad scripts, storyboards, video concepts, social posts

## 🏗️ Architecture

```
dotkey-market-intel/
├── src/
│   ├── models.py              # Core data models (Product, Competitor, Review, SWOT, etc.)
│   ├── catalog/
│   │   └── extractor.py       # Dot & Key website product extraction
│   ├── competitor/
│   │   └── monitor.py         # Competitor monitoring & comparison
│   ├── sentiment/
│   │   └── analyzer.py        # Review sentiment & topic analysis
│   ├── insights/
│   │   └── generator.py       # SWOT, market gaps, trends, recommendations
│   ├── content/
│   │   └── generator.py       # Marketing content generation (templates + AI)
│   └── api/
│       └── main.py            # Main orchestrator / pipeline
├── requirements.txt
├── demo_output/               # Generated results
└── README.md
```

## 📊 Data Models

### Core Entities
- **Product**: Dot & Key catalog entry (name, category, ingredients, benefits, price, skin types, concerns)
- **CompetitorProduct**: Competitor entries with platform, rating, review count, ingredients, claims
- **Review**: Customer reviews with sentiment, topics, key phrases
- **SentimentAnalysis**: Aggregated sentiment with positive/negative topics, complaints, praises
- **CompetitorComparison**: Price/rating/ingredient comparison, advantages, gaps
- **SWOTAnalysis**: Strengths, Weaknesses, Opportunities, Threats
- **MarketGap**: Unmet needs, missing ingredients, price gaps
- **TrendForecast**: Direction, strength, drivers, demand prediction
- **MarketingContent**: Generated content for 8 types across platforms

### Content Types Supported
1. **Static Ad** (Instagram, Facebook)
2. **Product Description** (Website, Amazon)
3. **A+ Content** (Amazon)
4. **Ad Script** (Video - 30 sec)
5. **Storyboard** (Video - 7 frames)
6. **Video Concept** (Reels/TikTok/Shorts - 15 sec)
7. **Social Media Post** (Instagram carousel)
8. **Email Campaign** (extensible)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run demo (uses sample data)
python -m src.api.main
```

## 📁 Sample Data Included

The system includes realistic sample data for immediate testing:

### 5 Dot & Key Products
1. **Vitamin C + E Super Bright Face Wash** - ₹395/100ml
2. **Watermelon Hydrating Sunscreen SPF 50** - ₹595/50ml
3. **Niacinamide 10% + Zinc PCA Serum** - ₹495/30ml
4. **Ceramide + Hyaluronic Acid Moisturizer** - ₹545/50ml
5. **Retinol 0.3% + Bakuchiol Night Serum** - ₹695/30ml

### 10 Competitor Brands with 15 Products
- Minimalist, The Derma Co, Plum, Mamaearth, WOW Skin Science, Pilgrim, Foxtale, Deconstruct, Simple, Neutrogena

### Sample Reviews
Realistic reviews with ratings, sentiment, topics for Dot & Key and competitor products

### Brand Guidelines
Complete Dot & Key brand voice, color palette, typography, key messages, prohibited claims, target demographics

## 📈 Output

Running the pipeline generates for each product:
- **SWOT Analysis** (strengths, weaknesses, opportunities, threats)
- **Market Gaps** (unmet needs, missing ingredients, price gaps)
- **Trend Forecast** (direction, strength, demand prediction)
- **Competitor Comparison** (price/ml, ratings, ingredient overlap)
- **Sentiment Analysis** (rating, sentiment score, top topics)
- **Recommendations** (product improvements, new opportunities, GTM strategies)
- **9 Marketing Content Pieces** across platforms

Results saved as:
- JSON files per product (`demo_output/`)
- Human-readable Markdown summary (`demo_output/SUMMARY_REPORT.md`)

## 🔧 Extending for Production

### Real Data Integration
Replace `use_sample_data=True` with `False` and implement:

1. **Catalog Extractor**: Add web scraping (Playwright/Selenium) for dotkey.in
2. **Competitor Monitor**: Integrate platform APIs (Amazon PA-API, Flipkart Affiliate, etc.)
3. **Review Collector**: Scrape reviews or use review APIs
4. **Sentiment**: Upgrade to transformer-based models (BERT, RoBERTa) for better accuracy
5. **Content Generation**: Integrate LLM APIs (OpenAI GPT-4, Anthropic Claude) for creative content

### Scalability
- Add database (PostgreSQL + pgvector for embeddings)
- Message queue (Redis/RabbitMQ) for async processing
- Scheduler (Celery Beat) for daily monitoring
- API layer (FastAPI) for frontend integration
- Vector search for competitor matching

### Demo Customization
The hackathon demo can focus on any single module or the full chain. The system is modular - pick what to showcase!

## 📝 Hackathon Notes

> "This brief is wide on purpose. You do not have to build all of it. Pick one part and build it well, or build the whole chain. Your call." - Calcutta AI Club

### Suggested Demo Focus Areas
1. **Full Pipeline** (what this repo demonstrates) - end-to-end working system
2. **Deep Dive: Sentiment + SWOT** - best for data science focus
3. **Deep Dive: Content Generation** - best for creative/AI focus
4. **Deep Dive: Competitor Intelligence** - best for market research focus

## 🛠️ Tech Stack
- Python 3.11+
- Async/await for concurrent operations
- httpx + BeautifulSoup for web scraping
- TextBlob + VADER for sentiment analysis
- Jinja2-style templates for content generation
- Dataclasses for type-safe data models

## 📄 License
Built for Vibe Coders Hackathon Edition 3 - Dot & Key Problem Statement