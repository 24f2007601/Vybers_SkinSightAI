# 🚀 VYBERS SkinSight-AI: Focused Build Plan

> **Strategic Scope:**  
> - **Primary Focus:** Deep Sentiment Analysis, Competitor Benchmarking, and Strategic Market Insights Dashboard.  
> - **Creative Feature:** High-converting Marketing Content Deck, 30s Ad Script & 7-Frame Storyboard Specifications (Instantaneous, deterministic, zero-latency).  
> - **Decoupled Architecture:** Python (FastAPI) Backend + React.js (Vite + Tailwind CSS) Frontend.  
> - **Data Foundation:** 2 Master Datasets (`data/dotkey_products.csv` + `data/india_cosmetics_brands_market_intel.csv`).

---

## 🏗️ 4-Step Build Sequence

```
Step 1: Backend Data Engine Cleanup (models.py + loader.py)
   │
   ▼
Step 2: Insights & Customer Acquisition Logic (insights/generator.py)
   │
   ▼
Step 3: FastAPI REST API Service (src/api/main.py)
   │
   ▼
Step 4: Modern React.js Dashboard UI (frontend/)
```

---

### 🔹 Step 1: Backend Data Engine Cleanup & Decoupling
- **Goal:** Ensure all data hydrations (`Product`, `CompetitorProduct`, `Review`, `BrandMarketIntel`) execute without circular imports or syntax errors.
- **Actions:**
  1. Clean `src/models.py` to hold pure typed dataclasses.
  2. In `src/data/loader.py`, ingest:
     - `data/dotkey_products.csv` (30 real Shopify products).
     - `data/india_cosmetics_brands_market_intel.csv` (100 Indian beauty brands).
  3. Ensure `load_dotkey_products()`, `load_competitor_products()`, `load_reviews()`, and `load_market_intel()` execute cleanly.
- **Verification:** Run a lightweight test script verifying 30 Dot & Key products, 100+ competitors, and 500+ reviews load into memory in $<500\text{ms}$.

---

### 🔹 Step 2: Customer Acquisition & Strategic Insights Engine
- **Goal:** Transform competitor reviews and market intel into concrete business advantages.
- **Actions:**
  1. **Competitor Benchmarking:** Calculate unit pricing (₹/ml or ₹/g) and active ingredient set differences.
  2. **NLP Sentiment & Topic Extraction:** Run VADER + TextBlob hybrid scoring across the 16 topical tags.
  3. **Customer Acquisition Engine:**
     - Extract competitor pain points (`Neg:` in market intel: *Minimalist beginner sting*, *Derma Co drying cleansers*, *Mamaearth slow results*).
     - Map each competitor friction point into a Dot & Key counter-positioning ad hook.
  4. **SWOT & Whitespace Gaps:** Generate 4-quadrant SWOT and 90-day demand forecast.
- **Verification:** Verify that `generate_insights(product)` returns a complete `MarketInsights` object with non-empty competitor comparisons, SWOT, and customer acquisition hooks.

---

### 🔹 Step 3: FastAPI REST Service Layer (`src/api/main.py`)
- **Goal:** Provide clean, high-speed JSON endpoints for the React frontend.
- **Actions:**
  1. Set up FastAPI app with `CORSMiddleware` (allowing `http://localhost:5173`).
  2. Implement core REST endpoints:
     - `GET /api/v1/products`: Returns list of Dot & Key products for the selector dropdown.
     - `GET /api/v1/products/{id}/insights`: Returns competitor benchmarking, sentiment breakdown, SWOT matrix, market gaps, and customer acquisition hooks.
     - `GET /api/v1/products/{id}/content`: Returns generated marketing assets (Instagram copy, Amazon listing, 30-sec ad script, 7-frame storyboard, Reels concept).
- **Verification:** Test endpoints locally with Uvicorn and confirm Swagger documentation (`/docs`) responds with valid JSON.

---

### 🔹 Step 4: Modern React.js Frontend Dashboard (`frontend/`)
- **Goal:** Build an aesthetic, judge-ready interface with Dot & Key brand identity (`#E85D75` Primary Pink, `#F5F0EB` Cream, `#4A90A4` Teal).
- **Actions:**
  1. Scaffold `frontend/` using Vite + React + Tailwind CSS + Lucide Icons.
  2. Build components:
     - **Navbar & Selector:** Brand logo, tagline (*Clean. Conscious. Effective.*), and product dropdown with thumbnails.
     - **Tab 1: 📊 Competitor Benchmarking:** Side-by-side cards with ₹/ml unit economics, star ratings, review count, and shared vs. unique ingredient badges.
     - **Tab 2: 🗣️ Voice of Customer & Sentiment:** Sentiment polarity gauge, 16-topic pill distribution, and side-by-side raw customer praise vs. complaint quotes.
     - **Tab 3: 💡 Strategic Insights & Customer Acquisition:** 4-quadrant SWOT grid, market whitespaces, and **Customer Switcher Strategy Card** (exploiting competitor weaknesses).
     - **Tab 4: 🚀 Marketing Content Studio:** Tabbed copy generator (Instagram Ad, Amazon A+ Listing, 30s Ad Script, 7-Frame Storyboard) with one-click **"Copy to Clipboard"**.
- **Verification:** Live dashboard loads in browser, switches products seamlessly, and updates all metrics in $<1\text{ second}$.

---

## 🎯 Verification Criteria (Definition of Done)
1. **Zero Hallucinated Metrics:** Every price/ml, competitor rating, and review quote traces back to the 2 CSV datasets.
2. **Sub-second Latency:** Switching products updates all tabs instantly without live web scraping bottlenecks.
3. **Flawless Judge Walkthrough:** Clean narrative demonstrating Product Selection ➔ Competitor Benchmark ➔ Customer Voice ➔ Acquisition Strategy ➔ Production-ready Marketing Copy.
