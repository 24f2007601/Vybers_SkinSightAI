# PIPELINE WORKFLOW & CSV INTEGRATION ARCHITECTURE

> **Target Sprint:** 1–2 Hour Hackathon Execution (Decoupled FastAPI + React.js)  
> **Source Documents:** Derived from `AGENTS.MD/dev-roadmap-1-2hr.md`, `AGENTS.MD/PRD.md`, and `data/india_cosmetics_brands_market_intel.csv`

---

## 1. End-to-End Pipeline Workflow (CSV ➔ Engine ➔ Customer Acquisition ➔ React API)

```
[data/dotkey_products.csv]     [data/competitor_products.csv]     [data/reviews.csv]     [data/india_cosmetics_brands_market_intel.csv]
           │                                 │                             │                                    │
           └─────────────────────────┬───────┴─────────────────────────────┴────────────────────────────────────┘
                                     ▼
                            src/data/loader.py
                     (Hydrates typed Dataclass models & 
                      loads 50+ Brand Market Intelligence)
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   ▼
src/catalog/extractor.py                            src/competitor/monitor.py
 (Dot & Key catalog list)                           (Matches category, calculates ₹/ml,
           │                                         ranks top 5 competitors)
           │                                                   │
           └─────────────────────────┬─────────────────────────┘
                                     ▼
                         src/sentiment/analyzer.py
                    (VADER + TextBlob hybrid scoring,
                      16 topical keywords & quotes)
                                     │
                                     ▼
                         src/insights/generator.py
              ┌──────────────────────────────────────────────┐
              │ 1. Product SWOT & Unit Economics (₹/ml)      │
              │ 2. Ingredient Set Differential Engine        │
              │ 3. Customer Acquisition Intelligence Engine:  │
              │    - Competitor Weakness Weaponization       │
              │    - Strategic Whitespace & Gaps Exploitation│
              │    - Segment-Specific Acquisition Triggers   │
              │ 4. 90-Day Category Demand & Trend Forecast   │
              └──────────────────────────────────────────────┘
                                     │
                                     ▼
                         src/content/generator.py
                   (Directly converts Customer Acquisition
                    triggers into 8 high-converting assets:
                    Instagram Ads, 30s Video Script, Amazon
                    A+ Copy, Reels UGC Hooks, Storyboards)
                                     │
                                     ▼
                            src/api/main.py
                        (FastAPI REST Endpoints)
                   ├── GET /api/v1/products
                   ├── GET /api/v1/products/{id}/insights
                   ├── GET /api/v1/products/{id}/acquisition-strategy
                   └── GET /api/v1/products/{id}/content
                                     │
                                     ▼
                        React.js Frontend Dashboard
                       (Vite + Tailwind CSS UI tabs)
```

---

## 2. CSV Data Contracts & How Each CSV is Used

| CSV File | Current State | How the Engine Consumes It |
|---|---|---|
| **`data/dotkey_products.csv`** | 30 real products extracted from Shopify API | `src/catalog/extractor.py` reads this. Feeds commercial title, variant pricing, unit size in ml/g, ingredients, and claims. |
| **`data/competitor_products.csv`** | 15 curated products across Minimalist, Derma Co, Plum, Foxtale, etc. | `src/competitor/monitor.py` filters by `category` and `subcategory`, ranks top 5 using: $$\text{Rating} \times \left(1 + \frac{\sqrt{\text{Reviews}}}{100}\right)$$ and normalizes unit price to **₹ / ml** or **₹ / g**. |
| **`data/reviews.csv`** | Raw customer reviews with star ratings and platforms | `src/sentiment/analyzer.py` runs dual NLP (VADER + TextBlob) to categorize sentiment and map to the 16 topical tags (`white_cast`, `pilling`, `fragrance`, `texture`, etc.). |
| **`data/india_cosmetics_brands_market_intel.csv`** | **50+ Indian Cosmetics & Skincare Brands** with price bands, customer reviews (pros/cons), competitors, and market opportunities | **Customer Market Acquisition Engine** in `src/insights/generator.py`. Maps competitor weaknesses and whitespace opportunities into acquisition strategies. |

---

## 3. Deep Dive: Customer Market Acquisition Using `india_cosmetics_brands_market_intel.csv`

The file `data/india_cosmetics_brands_market_intel.csv` contains structured intelligence across 50+ major Indian beauty players (Lakmé, Maybelline, L'Oréal, Sugar, Mamaearth, Minimalist, The Derma Co, Plum, Foxtale, Biotique, Kama Ayurveda, etc.). 

Each row provides:
- **`product_info`**: `Brand | Category | Flagship Lines | Price Band`
- **`customer_reviews`**: Verified customer sentiment split into `Pos:` (pros) and `Neg:` (pain points/cons).
- **`competitors`**: Direct substitute brands.
- **`market_opportunities`**: High-conviction whitespace opportunities.

### How the Engine Powers Customer Acquisition:

```
Competitor Review Friction (from CSV)
  ├── Minimalist: "Plain apothecary packaging, strong actives irritate beginners"
  ├── Derma Co:   "Drying cleansers, mild irritation, batch consistency"
  ├── Mamaearth:  "Inconsistent results, 'natural' claims questioned, breakouts"
  └── Plum:       "Pump dispenser clogs, fragrance intensity, slow results"
                              │
                              ▼
        [Customer Acquisition Matrix in src/insights/generator.py]
                              │
  ┌───────────────────────────┴───────────────────────────┐
  ▼                                                       ▼
1. Competitor Switcher Campaigns                2. Category Whitespace Capture
   (Targeting competitor pain points               (Directing Dot & Key products
    with Dot & Key formulations)                    into verified unmet needs)
  │                                                       │
  ▼                                                       ▼
- "Gentle fruit+active synergy                  - Launching fragrance-free sensitive
   with ZERO beginner irritation"                 variants for irritation-conscious buyers
- "Sensorial cooling texture with               - High-SPF PA++++ zero white-cast
   rich aesthetics vs plain apothecary"           fluid formulas for melanin-rich skin
- "Clinically proven results,                   - Multi-functional hybrid formats
   unlike unverified 'natural' claims"            (Tinted serums / Sunscreen duos)
                              │
                              ▼
[Marketing Content Engine in src/content/generator.py]
  - Static Ad Hooks: "Love Niacinamide but hate the beginner sting?"
  - 30s Video Problem Scene: Visualizes competitor pilling/dryness ➔ Reveals Dot & Key fix
  - Amazon A+ Module: Direct comparison table against market averages
```

### 3-Pillar Customer Acquisition Strategy:

1. **Competitor Defection (Poaching Unhappy Customers):**
   - The engine queries the `customer_reviews` column for the top 5 direct competitors.
   - Extracts negative friction points (`Neg:`).
   - Generates direct counter-claims in Dot & Key ads (e.g. *Derma Co users complaining of drying cleansers* ➔ Dot & Key positions its *Cica Gentle Barrier Repair Cleanser* with zero stripping).

2. **Price-Band Arbitrage & Bridging:**
   - Evaluates the `Price Band` of mass brands (₹150–400: Himalaya, Biotique) vs. luxury brands (₹1000–3500: Kama, Forest Essentials).
   - Identifies masstige switchers: customers seeking luxury sensorial feel and clean actives without paying ₹2,000+. Dot & Key's ₹395–695 price tier is positioned as the **"Accessible Luxury"** alternative.

3. **Whitespace Opportunity Activation:**
   - Reads the `market_opportunities` column (e.g. *Clean-label reformulation*, *fragrance-free lines*, *high-SPF no-cast sunscreen*, *hybrid skincare-makeup*).
   - Generates go-to-market suggestions and hooks directly tied to Dot & Key products meeting those exact criteria (e.g., *Strawberry Dew Tinted Sunscreen* fulfilling the *skincare-makeup hybrid* demand).

---

## 4. Required Edits to Execute `dev-roadmap-1-2hr.md`

To make this pipeline run fast, deterministic, and bug-free within the 1–2 hour sprint, the following **4 targeted edits** are required:

### 🛠️ Edit 1: Fix `src/models.py` Circular Dependency & Add MarketIntel Dataclass
- **Issue:** `models.py` still has residual deleted code and imports `src/data/loader.py`, causing circular imports and indentation errors.
- **Fix:**
  - Keep pure dataclasses in `src/models.py`.
  - Add `BrandMarketIntel` dataclass to model market intelligence:
    ```python
    @dataclass
    class BrandMarketIntel:
        brand: str
        category: str
        flagship_lines: list[str]
        price_band: str
        positive_sentiment: list[str]
        negative_friction: list[str]
        competitors: list[str]
        market_opportunities: list[str]
    ```
  - Ensure pure separation between models and data loading.

### 🛠️ Edit 2: Adapt `src/data/loader.py` to Load Both Datasets
- **Fix in `loader.py`:**
  - Add mapping for real Shopify columns in `load_dotkey_products()` (`title` ➔ `name`, `prices_inr` ➔ `price_inr`, `product_type` ➔ `category`).
  - Add `load_market_intel()` to parse `india_cosmetics_brands_market_intel.csv` and extract competitor pros, cons, and opportunities.

### 🛠️ Edit 3: Integrate Acquisition Intelligence in `src/insights/generator.py` & FastAPI
- **Fix:**
  - Add `_generate_customer_acquisition_strategy()` in `InsightsGenerator`. It cross-references the active Dot & Key product category against competitor friction points in `india_cosmetics_brands_market_intel.csv`.
  - Expose this in FastAPI (`src/api/main.py`) via `GET /api/v1/products/{id}/insights`:
    ```json
    {
      "customer_acquisition": {
        "target_competitor_switchers": ["Minimalist", "The Derma Co"],
        "exploitable_competitor_weaknesses": ["Drying formulations", "Apothecary packaging", "Beginner irritation"],
        "acquisition_ad_hooks": [
          "Love active ingredients but tired of skin irritation?",
          "Switch to fruit-powered actives that soothe while they treat."
        ],
        "whitespace_opportunities": ["Fragrance-free sensitive skin lines", "Zero-white-cast tinted sunscreens"]
      }
    }
    ```

### 🛠️ Edit 4: Scaffold the React Frontend (`frontend/`)
- **Action:** Scaffold React app and render Customer Acquisition hooks directly in **Tab 3 (Insights)** and **Tab 4 (Marketing Content)**:
  - Add an **"Acquisition & Switcher Strategy"** card showing competitor pain points being targeted.
  - One-click copy for customer defection ad hooks.

---

## 5. Execution Sequence (Immediate Next Steps)

1. **Step 1:** Fix `src/models.py` and update `src/data/loader.py` to hydrate both `dotkey_products.csv` and `india_cosmetics_brands_market_intel.csv`.
2. **Step 2:** Wire customer acquisition hooks into `src/insights/generator.py` and wrap `src/api/main.py` with FastAPI.
3. **Step 3:** Scaffold `frontend/` (Vite + React) to display the competitor benchmarks, sentiment quotes, acquisition strategy, and marketing content deck.
