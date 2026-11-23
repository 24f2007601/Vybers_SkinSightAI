# Dot & Key: Market Intelligence to Marketing Content (PRD)

**Project:** VYBERS SkinSight-AI  
**Hackathon:** Vibe Coders Hackathon Edition 3 · 21 November 2026 · Hackathon MVP  
**Status:** Aligned to Decoupled Architecture (FastAPI Backend + React.js Frontend)

---

## 1. Goal & Mission

An automated end-to-end platform featuring a **Python (FastAPI) intelligence engine** and an interactive **React.js web interface**. A marketer selects a Dot & Key product and triggers a synchronized two-stage workflow:

1. **Research & Intelligence:** Extracts product facts, identifies top 5 benchmark competitors, normalizes pricing/ratings/ingredients, performs dual-model NLP sentiment analysis on reviews, and computes evidence-backed SWOT, market gaps, and trend forecasts.
2. **Marketing Content Generation:** Ingests these quantified insights directly into a brand-safe content generator to produce static ads (IG/FB), e-commerce product listings, Amazon A+ modules, 30-second video scripts, storyboards, and short-form video concepts.

**Guiding Rule:** *Evidence-first AI.* Every figure, competitive advantage, customer pain point, and marketing angle traces back to scraped catalog data or real customer reviews. No hallucinated metrics, no unsupported claims.

---

## 2. System Architecture & Repository Layout

The PRD maps directly to the decoupled full-stack architecture:

```
VYBERS_SkinSight-AI/
├── AGENTS.MD/
│   ├── PRD.md                   # This document — authoritative product requirements (React.js UI)
│   ├── PROJECT_BRAIN.md         # Operational system brain, ontology, constraints & rules
│   ├── CONTEXT.md               # Indian BPC landscape, competitor matrix & brand guidelines
│   └── dev-roadmap-1-2hr.md     # 90-120 minute hackathon sprint roadmap (React.js frontend focus)
├── data/
│   ├── dotkey_products.csv      # Real Dot & Key catalog (extracted from Shopify endpoint)
│   ├── india_cosmetics_brands_market_intel.csv # 50+ Indian cosmetics/skincare brand benchmark matrix
│   ├── competitor_products.csv  # Curated competitor catalog with price, rating, review count, ingredients
│   └── reviews.csv              # Customer reviews tagged with sentiment & topical mentions
├── frontend/                    # Modern React.js Web Application
│   ├── package.json             # React 18, Vite, Tailwind CSS, Lucide icons, Axios
│   ├── vite.config.js           # Vite dev server with proxy to backend (/api -> localhost:8000)
│   ├── tailwind.config.js       # Dot & Key brand theme tokens (primary, secondary, accent)
│   └── src/
│       ├── App.jsx              # Main dashboard container & tab navigation
│       ├── components/
│       │   ├── Navbar.jsx       # Header with Dot & Key branding and active product selector
│       │   ├── CompetitorTab.jsx# Side-by-side cards, unit economics (₹/ml) & ingredient badges
│       │   ├── SentimentTab.jsx # Sentiment gauges, topic breakdown, raw customer voice quotes
│       │   ├── InsightsTab.jsx  # 4-quadrant SWOT matrix, market gaps, 90-day demand forecast
│       │   └── ContentTab.jsx   # Marketing decks (Ads, A+ listing, 30s script, storyboard, Reels)
│       └── services/api.js      # Axios client fetching from FastAPI /api/v1 endpoints
├── src/                         # Python Backend Engine & API
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
│       └── main.py              # FastAPI REST endpoints serving the React frontend
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

### FR6: React.js UI & Frontend Specifications (`frontend/`)
- Single-page application built with **React.js + Vite + Tailwind CSS**.
- **Visual Language:** Custom-tailored to Dot & Key brand tokens:
  - Primary Pink: `#E85D75`
  - Secondary Cream: `#F5F0EB`
  - Accent Teal: `#4A90A4`
  - Dark Charcoal: `#2D2D2D`
- **Dashboard Views / Tabs:**
  1. **Navigation & Selector:** Product dropdown with thumbnail, category badge, and instant API trigger.
  2. **Competitor Benchmarking:** Side-by-side cards showing price/ml, ratings, review volume, and shared vs unique ingredient tags.
  3. **Voice of Customer (Sentiment):** Sentiment breakdown bars, topical sentiment heatmaps, and expandable customer quotes.
  4. **Strategic Insights (SWOT):** Color-coded 4-quadrant SWOT grid with evidence pills, identified market gaps, and 90-day demand forecast meter.
  5. **Marketing Content Studio:** Tabbed copy generator (Instagram Ad, Amazon A+, 30s Script, Storyboard, Reels Concept) with one-click "Copy to Clipboard" and markdown export.

### FR7: Backend API Layer (`src/api/main.py`)
- FastAPI application serving structured JSON responses to the React frontend:
  - `GET /api/v1/products`: List of all available Dot & Key products.
  - `GET /api/v1/products/{id}/insights`: Full competitor benchmarking, sentiment, and SWOT payload.
  - `GET /api/v1/products/{id}/content`: Generated multi-platform marketing content deck.
  - `POST /api/v1/pipeline/run`: Triggers full end-to-end intelligence pipeline.

---

## 5. Scope & Hackathon Boundaries

| In Scope (P0 - Implemented) | In Scope (P1 - Polish) | Deliberately Out of Scope |
|---|---|---|
| Complete async Python backend engine | React UI live export to PDF/Docx | Video pixel rendering / AI video gen |
| FastAPI REST endpoints (`/api/v1/*`) | Custom brand theme color picker | Complex database setup (Postgres/Redis) |
| React.js (Vite + Tailwind CSS) Dashboard | Dark / Light mode toggle | Financial/stock market sales prediction |
| Multi-competitor benchmark comparison | Historical aspect trend graph | Authenticated user logins & RBAC |
| NLP Sentiment & 16-topic classification | | Heavy multi-agent orchestration |
| Evidence-backed SWOT & market gaps | | |
| 8 distinct marketing content types in UI | | |

---

## 6. Anti-Bluff & Integrity Rules

1. **No Hallucinated Data:** Every rating, price, and competitor review originates from structured datasets in `data/`.
2. **Code Computes Numbers:** Percentages, ratings, and price/ml ratios are calculated using Python / `numpy` arithmetic, not estimated by LLM prose.
3. **Evidence Mapping:** Every SWOT bullet and market gap cites concrete supporting data (e.g., negative complaint count or competitor active presence).
4. **Honest Limitations:** Where data is not available (e.g. internal sales records), the system relies on demand opportunity indicators rather than inventing revenue figures.

---

## 7. Execution Commands

```bash
# Terminal 1: Backend FastAPI Server
pip install -r requirements.txt
uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Frontend React.js Application
cd frontend
npm install
npm run dev
# React app opens at http://localhost:5173
```
