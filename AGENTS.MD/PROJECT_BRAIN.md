# PROJECT BRAIN & AGENT CONTEXT: VYBERS SkinSight-AI

## 1. Executive Summary & Objective
- **Project:** VYBERS SkinSight-AI
- **Context:** Vibe Coders Hackathon Edition 3 (Dot & Key Problem Statement).
- **Core Mission:** An end-to-end, async AI market intelligence & marketing content generation pipeline for Indian beauty and personal care (BPC), centered on **Dot & Key**.
- **Transformation Pipeline:**
  `Product Catalog + Competitor Intelligence + Reviews` ➔ `Sentiment Analysis (NLP)` ➔ `SWOT & Market Gaps & Trends` ➔ `Marketing Content (8 Multi-channel Formats)` ➔ `JSON & Markdown Executive Reports`.

---

## 2. Repository Layout & Architecture
```
VYBERS_SkinSight-AI/
├── AGENTS.MD/
│   ├── PROJECT_BRAIN.md         # Fast-read system brain, ontology, constraints & operational guidelines
│   └── CONTEXT.md               # Deep domain context, schemas, market landscape & data catalogs
├── data/
│   ├── dotkey_products.csv      # Real Dot & Key catalog (30 products extracted from Shopify API)
│   ├── india_cosmetics_brands_market_intel.csv # 50+ Indian cosmetics & skincare brands, reviews & competitors
│   ├── competitor_products.csv  # Benchmark competitors with pricing, ratings & ingredients
│   └── reviews.csv              # Customer reviews labeled with sentiment, topics & pain points
├── src/
│   ├── models.py                # Type-safe domain models (Product, Review, SWOT, Content, Guidelines)
│   ├── catalog/extractor.py     # Product extraction (live Shopify JSON-LD / CSV-backed)
│   ├── competitor/monitor.py    # Multi-platform competitor matching, price/ml & gap evaluation
│   ├── sentiment/analyzer.py    # VADER + TextBlob hybrid sentiment & 16-class topical taxonomy
│   ├── insights/generator.py    # Automated SWOT, gap identification, 90-day demand forecast & strategy
│   ├── content/generator.py     # 8 marketing content archetypes across IG, FB, Amazon, YouTube
│   └── api/main.py              # Pipeline orchestrator & report exporter
└── requirements.txt
```

---

## 3. Core Ontology & Domain Entities (`src/models.py`)

- **`Product`**: Dot & Key catalog entity. Fields: `id`, `name`, `category`, `subcategory`, `ingredients`, `key_benefits`, `skin_type`, `concerns`, `price_inr`, `size_ml`, `image_urls`, `product_url`.
- **`CompetitorProduct`**: Benchmark listings. Fields: `brand`, `product_name`, `category`, `subcategory`, `price_inr`, `size_ml`, `rating`, `review_count`, `platform` (Amazon, Nykaa, Flipkart, Purplle, Myntra), `ingredients`, `key_claims`.
- **`Review`**: Customer feedback. Fields: `product_id`, `platform`, `rating`, `title`, `text`, `sentiment` (`POSITIVE`, `NEGATIVE`, `NEUTRAL`), `sentiment_score` (-1.0 to 1.0), `topics`, `key_phrases`.
- **`SentimentAnalysis`**: Aggregated metrics across reviews: distributions, top positive/negative themes, key praises, critical complaints.
- **`CompetitorComparison`**: Direct comparative vectors: relative price/ml, ratings, shared/differentiating ingredients, competitive advantages & competitive gaps.
- **`SWOTAnalysis`**: Product & category level Strengths, Weaknesses, Opportunities, Threats.
- **`MarketGap`**: Identified white spaces: missing hero ingredients, unserved price brackets, common customer friction points.
- **`TrendForecast`**: Direction (`rising`, `stable`, `declining`), strength, key growth drivers, 90-day demand variation %.
- **`MarketingContent`**: Structured platform-tailored copy with format specifications, brand voice compliance, target audience, messaging & CTA.
- **`BrandGuidelines`**: Dot & Key guardrails: Voice ("friendly, scientific, empowering, transparent"), core colors (`#E85D75`, `#F5F0EB`, `#4A90A4`), prohibited claims ("miracle", "permanent cure", "medical grade").

---

## 4. Analytical Modules & Algorithmic Logic

### A. Sentiment Analysis (`src/sentiment/analyzer.py`)
- **Dual-Model Scoring:** `(VADER compound score + TextBlob polarity score) / 2`.
  - Score $\ge 0.1 \rightarrow$ `POSITIVE`
  - Score $\le -0.1 \rightarrow$ `NEGATIVE`
  - Else $\rightarrow$ `NEUTRAL`
- **Topic Keyword Taxonomy (16 Categories):** `texture`, `fragrance`, `effectiveness`, `gentleness`, `hydration`, `oil_control`, `brightening`, `anti_aging`, `acne`, `white_cast`, `makeup_compatibility`, `packaging`, `value`, `shipping`, `eye_irritation`, `sweat_resistance`.
- **N-Gram Key Phrase Extraction:** Regex matching for sentiment-heavy adjective-noun pairs and customer verdicts.

### B. Competitor & Market Insights (`src/insights/generator.py`)
- **Price Metric Normalization:** Standardized to **₹ / ml** or **₹ / g** across competitors.
- **Ingredient Differential Engine:** Set intersections and differences across formulations identifying missing trending actives (e.g., Cica, Madecassoside, Peptides, Ceramides).
- **SWOT Engine:**
  - *Strengths:* Positives (>0.3 sentiment), formula differentiators, price advantages.
  - *Weaknesses:* Recurring review complaints, price premiums, missing claims.
  - *Opportunities:* Category white-spaces, price tier voids (>30% jump without competition).
  - *Threats:* High-velocity competitor products (rating > 4.5 and review volume > 10,000), aggressive discounting.
- **Trend Forecasting:** Derived from active ingredient frequencies and positive consumer sentiment momentum.

### C. Content Generation Engine (`src/content/generator.py`)
Supported Content Types:
1. `STATIC_AD`: Instagram (1:1), Facebook (1.91:1)
2. `PRODUCT_DESCRIPTION`: Website (HTML/Markdown), Amazon (Bullet-point structured)
3. `A_PLUS_CONTENT`: 6-module Amazon enhanced brand content layout
4. `AD_SCRIPT`: 30-second vertical video script (Hook, Problem, Solution, Demo, Proof, CTA)
5. `STORYBOARD`: 7-frame video production storyboard
6. `VIDEO_CONCEPT`: 15-second Reels/Shorts concept with talent and production notes
7. `SOCIAL_MEDIA_POST`: Multi-slide carousel copy with hashtags & alt-text
8. `EMAIL_CAMPAIGN`: Extensible CRM format

---

## 5. Token Efficiency & Agent Execution Rules

1. **Do not re-read large raw files:** Use `data/dotkey_products.csv` and `data/india_cosmetics_brands_market_intel.csv` schemas outlined in `CONTEXT.md` rather than loading entire CSVs into conversation memory.
2. **Deterministic Schemas:** Treat all dataclasses in `src/models.py` as strict schemas. Never invent ad-hoc JSON structures when models already exist.
3. **Execution Entrypoint:** Run pipeline via `python -m src.api.main` (or individual module test blocks `python -m src.sentiment.analyzer`, etc.).
4. **Data Isolation:** All raw inputs reside in `data/`, business logic in `src/`, output artifacts in `demo_output/` or `output/`.
