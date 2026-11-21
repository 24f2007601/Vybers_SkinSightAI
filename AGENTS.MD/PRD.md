# Dot & Key: Market Intelligence to Marketing Content (PRD)

**Project:** VYBERS SkinSight-AI  
**Hackathon:** Vibe Coders Hackathon Edition 3 · 21 November 2026 · Hackathon MVP  
**Status:** Aligned to Repository Structure & Codebase

---

## 1. Goal & Mission

An automated end-to-end Python pipeline and web interface where a user selects a Dot & Key product and triggers a synchronized two-stage workflow:

1. **Research & Intelligence:** Extracts product facts, identifies top 5 benchmark competitors, normalizes pricing/ratings/ingredients, performs dual-model NLP sentiment analysis on reviews, and computes evidence-backed SWOT, market gaps, and trend forecasts.
2. **Marketing Content Generation:** Ingests these quantified insights directly into a brand-safe content generator to produce static ads (IG/FB), e-commerce product listings, Amazon A+ modules, 30-second video scripts, storyboards, and short-form video concepts.

**Guiding Rule:** *Evidence-first AI.* Every figure, competitive advantage, customer pain point, and marketing angle traces back to scraped catalog data or real customer reviews. No hallucinated metrics, no unsupported claims.

---

## 2. System Architecture & Repository Layout

The PRD maps directly to the modular codebase structure:

```
VYBERS_SkinSight-AI/
├── AGENTS.MD/
│   ├── PRD.md                   # This document — authoritative product requirements
│   ├── PROJECT_BRAIN.md         # Operational system brain, ontology, constraints & rules
│   └── CONTEXT.md               # Indian BPC landscape, competitor matrix & brand guidelines
├── data/
│   ├── dotkey_products.csv      # Real Dot & Key catalog (extracted from Shopify endpoint)
│   ├── india_cosmetics_brands_market_intel.csv # 50+ Indian cosmetics/skincare brand benchmark matrix
│   ├── competitor_products.csv  # Curated competitor catalog with price, rating, review count, ingredients
│   └── reviews.csv              # Customer reviews tagged with sentiment & topical mentions
├── src/
│   ├── models.py                # Type-safe dataclass models (Product, Review, SWOT, Content, Guidelines)
│   ├── data/
│   │   ├── __init__.py          # Data loader package exports
│   │   └── loader.py            # CSV-to-Dataclass hydration engine with caching
│   ├── catalog/
│   │   └── extractor.py         # Catalog extraction (Shopify JSON-LD / HTML parser / CSV fallback)
│   ├── competitor/
│   │   └── monitor.py           # Competitor selection, ranking algorithm & price/ml comparison
│   ├── sentiment/
│   │   └── analyzer.py          # Dual-model (VADER + TextBlob) sentiment & 16-topic extraction
│   ├── insights/
│   │   └── generator.py         # Evidence-backed SWOT, market gaps, trend forecast & recommendations
│   ├── content/
│   │   └── generator.py         # 8 multi-channel marketing content generators with claims guard
│   └── api/
│       └── main.py              # Central orchestrator & executive report exporter
├── demo_output/                 # Generated per-product JSON output & SUMMARY_REPORT.md
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 3. Data Strategy & Storage

### Layer 1: Dot & Key Catalog
- **Source:** Extracted from `https://dotandkey.com/products.json` (Shopify API endpoint).
- **Storage:** `data/dotkey_products.csv`.
- **Fields:** `id`, `title`, `handle`, `product_type`, `vendor`, `tags`, `description`, `prices_inr`, `sizes`, `image_urls`, `published_at`, `created_at`, `updated_at`.
- **Loader:** `src/catalog/extractor.py` and `src/data/loader.py` (`load_dotkey_products()`).

### Layer 2: Competitor Intelligence
- **Source:** Marketplaces (Amazon, Nykaa, Flipkart, Purplle, Myntra) + `data/india_cosmetics_brands_market_intel.csv`.
- **Storage:** `data/competitor_products.csv`.
- **Fields:** `brand`, `product_name`, `category`, `subcategory`, `price_inr`, `size_ml`, `rating`, `review_count`, `platform`, `product_url`, `ingredients`, `key_claims`, `availability`.
- **Loader:** `src/competitor/monitor.py` and `src/data/loader.py` (`load_competitor_products()`).

### Layer 3: Customer Reviews & Aspect Sentiment
- **Source:** Marketplace reviews (verified buyer reviews from Amazon, Nykaa, Flipkart).
- **Storage:** `data/reviews.csv`.
- **Fields:** `product_id`, `platform`, `rating`, `title`, `text`, `verified_purchase`, `helpful_votes`, `sentiment`, `sentiment_score`, `key_phrases`, `topics`.
- **Loader:** `src/sentiment/analyzer.py` and `src/data/loader.py` (`load_reviews()`).

---

## 4. Functional Requirements

### FR1: Catalog Extraction & Normalization (`src/catalog/extractor.py`)
- Ingests Dot & Key product data via HTTP/Shopify JSON endpoint or cached CSV.
- Maps raw products to `Product` dataclass (`src/models.py`), ensuring parsed ingredients, pricing, unit size in ml/g, and clean text descriptions.
- **Verification:** 30+ clean Dot & Key products accessible with zero missing titles or pricing.

### FR2: Competitor Matching & Comparison Engine (`src/competitor/monitor.py`)
- Filters competitors matching category and subcategory (e.g., Sunscreen -> Hydrating / Gel).
- Ranking algorithm: Composite score sorting:
  $$\text{Score} = \text{Rating} \times \left(1 + \frac{\sqrt{\text{Review Count}}}{100}\right)$$
- Normalizes unit economics to **₹ per ml** or **₹ per gram**.
- Computes ingredient set overlaps and unique competitor ingredients.
- Identifies Dot & Key competitive advantages (e.g. price per ml advantage, unique actives) and gaps.

### FR3: Review Sentiment & Topic Analysis (`src/sentiment/analyzer.py`)
- Analyzes customer review texts with a hybrid NLP pipeline:
  $$\text{Sentiment Score} = \frac{\text{VADER Compound} + \text{TextBlob Polarity}}{2}$$
  - $\text{Score} \ge 0.1 \rightarrow \text{POSITIVE}$
  - $\text{Score} \le -0.1 \rightarrow \text{NEGATIVE}$
  - Else $\rightarrow \text{NEUTRAL}$
- Tags reviews against a fixed 16-class topical taxonomy:
  `texture`, `fragrance`, `effectiveness`, `gentleness`, `hydration`, `oil_control`, `brightening`, `anti_aging`, `acne`, `white_cast`, `makeup_compatibility`, `packaging`, `value`, `shipping`, `eye_irritation`, `sweat_resistance`.
- Extracts top phrases, recurring complaints, and praises.

### FR4: Evidence-Backed Market Insights (`src/insights/generator.py`)
- **SWOT Analysis:**
  - *Strengths:* Derived from positive review sentiment (>0.3) and formula/pricing advantages.
  - *Weaknesses:* Derived from negative topical mentions and price premiums.
  - *Opportunities:* Derived from market gaps and ingredient trends.
  - *Threats:* High-velocity competitor products (>4.5 rating, >10,000 reviews) and cheaper alternatives.
- **Market Gaps:** Pinpoints unaddressed consumer complaints, popular missing actives across competitors, and price segment gaps (>30% variance without competitor presence).
- **Trend Forecast:** Computes category trajectory (`rising`, `stable`, `declining`), strength factor, and 90-day estimated demand variance.
- **Recommendations:** Delivers up to 7 actionable product, positioning, and GTM directives.

### FR5: Marketing Content Generation (`src/content/generator.py`)
Generates 8 high-converting, platform-specific content types matching `BrandGuidelines` (voice, color palette, prohibited claims):
1. **Static Ad (Instagram - 1:1, Facebook - 1.91:1):** Catchy hook, benefit checklist, hero ingredient callout, CTA.
2. **Product Description (Website):** Hook, "What it does", key benefits, ingredient breakdown, usage instructions.
3. **Amazon Product Listing:** Title, short description, 5 bullet points, usage steps, target concerns.
4. **Amazon A+ Content:** 6 structured modules (Brand Story, Comparison Chart, Ingredient Spotlight, Usage Guide, Reviews Highlights, Bundle Cross-sell).
5. **Ad Script (30-Second Video):** 6 scenes (Hook 0-3s, Problem 3-6s, Solution 6-10s, Demo 10-18s, Social Proof 18-25s, CTA 25-30s).
6. **Storyboard (7 Frames):** Visual direction, voiceover copy, camera angles, and transitions.
7. **Short-Form Video Concept (Reels/Shorts - 15s):** Creative concept, target audience, visual style, script outline, production notes, and budget.
8. **Social Media Post (Instagram Carousel):** Multi-slide caption, UGC hook, hashtags, and accessibility alt-text.
- **Claims Guard:** Enforces prohibition of forbidden keywords ("miracle", "permanent cure", "medical grade").

### FR6: Pipeline Orchestration & Output Export (`src/api/main.py`)
- Runs end-to-end async batch processing for all products or an isolated product ID.
- Exports results to:
  - Per-product structured JSON in `demo_output/<product_id>_<product_name>.json`.
  - Comprehensive executive Markdown report in `demo_output/SUMMARY_REPORT.md`.

---

## 5. Scope & Hackathon Boundaries

| In Scope (P0 - Implemented) | In Scope (P1 - Polish) | Deliberately Out of Scope |
|---|---|---|
| Complete async Python pipeline | Streamlit web UI | Video pixel rendering / AI video gen |
| Real Dot & Key catalog extraction | Real-time scraper refresh trigger | Complex database setup (Postgres/Redis) |
| Multi-competitor benchmark comparison | Zip bundle exporter for creatives | Financial/stock market sales prediction |
| NLP Sentiment & 16-topic classification | Aspect trend timeline (recent vs old) | Authenticated user logins & RBAC |
| Evidence-backed SWOT & market gaps | | Heavy multi-agent orchestration |
| 8 distinct marketing content types | | |
| JSON & Markdown output generation | | |

---

## 6. Anti-Bluff & Integrity Rules

1. **No Hallucinated Data:** Every rating, price, and competitor review originates from structured datasets in `data/`.
2. **Code Computes Numbers:** Percentages, ratings, and price/ml ratios are calculated using Python / `numpy` arithmetic, not estimated by LLM prose.
3. **Evidence Mapping:** Every SWOT bullet and market gap cites concrete supporting data (e.g., negative complaint count or competitor active presence).
4. **Honest Limitations:** Where data is not available (e.g. internal sales records), the system relies on demand opportunity indicators rather than inventing revenue figures.

---

## 7. Execution Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the complete end-to-end pipeline
python -m src.api.main

# 3. Test individual modules
python -m src.catalog.extractor
python -m src.competitor.monitor
python -m src.sentiment.analyzer
python -m src.insights.generator
python -m src.content.generator
```
