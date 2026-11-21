# PIPELINE WORKFLOW & CSV INTEGRATION ARCHITECTURE

> **Target Sprint:** 1–2 Hour Hackathon Execution (Decoupled FastAPI + React.js)  
> **Data Strategy Update:** `competitor_products.csv` and `reviews.csv` are **merged** into `data/india_cosmetics_brands_market_intel.csv`.  
> The entire pipeline now operates on **two primary CSV files**:
> 1. `data/dotkey_products.csv` (Dot & Key catalog from Shopify)
> 2. `data/india_cosmetics_brands_market_intel.csv` (100 Indian cosmetics & skincare brands, products, pricing, reviews, and market opportunities)

---

## 1. Unified 2-CSV Pipeline Architecture

```
┌──────────────────────────────────────┐     ┌────────────────────────────────────────────────────────┐
│     data/dotkey_products.csv         │     │     data/india_cosmetics_brands_market_intel.csv       │
│  (Shopify-extracted Dot & Key range, │     │  (100 Indian Brands: Products, Pricing Bands,          │
│   titles, variants, ingredients,     │     │   Competitor Lists, Customer Reviews: Pos/Neg,         │
│   prices, sizes, images, tags)       │     │   Market Opportunities / Whitespaces)                  │
└──────────────────┬───────────────────┘     └───────────────────────────┬────────────────────────────┘
                   │                                                     │
                   └──────────────────────────┬──────────────────────────┘
                                              ▼
                                     src/data/loader.py
                      ┌───────────────────────────────────────────────┐
                      │ 1. load_dotkey_products()                     │
                      │    -> Hydrates Dot & Key Product dataclasses  │
                      │ 2. load_market_intel()                        │
                      │    -> Parses brand intel & market opportunities│
                      │ 3. load_competitor_products()                 │
                      │    -> Derives CompetitorProduct models        │
                      │       from product_info & flagship lines      │
                      │ 4. load_reviews()                             │
                      │    -> Synthesizes positive & negative review  │
                      │       models from Pos: and Neg: customer text │
                      └───────────────────────┬───────────────────────┘
                                              │
                   ┌──────────────────────────┴──────────────────────────┐
                   ▼                                                     ▼
        src/catalog/extractor.py                              src/competitor/monitor.py
         (Extracts active Dot & Key range)                     (Matches competitors by category,
                   │                                            calculates price/ml unit economics,
                   │                                            ranks top 5 competitors)
                   │                                                     │
                   └──────────────────────────┬──────────────────────────┘
                                              ▼
                                  src/sentiment/analyzer.py
                             (VADER + TextBlob hybrid scoring,
                              16 topical taxonomy tags,
                              praise & complaint phrase extraction)
                                              │
                                              ▼
                                  src/insights/generator.py
                       ┌──────────────────────────────────────────────┐
                       │ 1. Product SWOT & Unit Economics (₹/ml)      │
                       │ 2. Ingredient Set Differential Engine        │
                       │ 3. Customer Acquisition Intelligence Engine:  │
                       │    - Competitor Weakness Weaponization       │
                       │    - Strategic Whitespace & Gaps Exploitation│
                       │    - Customer Switcher Acquisition Triggers  │
                       │ 4. 90-Day Category Demand & Trend Forecast   │
                       └──────────────────────┬───────────────────────┘
                                              │
                                              ▼
                                  src/content/generator.py
                            (Directly translates acquisition triggers
                             into 8 high-converting marketing formats:
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

## 2. CSV Data Contracts & Ingestion Mapping

With `competitor_products.csv` and `reviews.csv` merged into `data/india_cosmetics_brands_market_intel.csv`, data ingestion is streamlined into **two distinct sources**:

### Source A: `data/dotkey_products.csv` (Dot & Key Catalog)
Extracted directly from the Shopify endpoint (`dotandkey.com/products.json`).
- `id`: Shopify unique product identifier.
- `title`: Product name (e.g. *Plushie Jelly Lip Balm SPF 50+*, *Watermelon Sunscreen*).
- `handle`: URL slug identifier.
- `product_type`: Categorization (`Sunscreen`, `Face Wash`, `Moisturiser`, `Combo`, `Lip Balm`).
- `tags`: Pipe-separated attribute list (`fltr_ingredients_Ceramide|bestseller|...`).
- `description`: Plaintext product summary and formula benefits.
- `prices_inr`: Variant prices in INR (e.g. `445.00|595.00`).
- `sizes`: Volume / weight variants (e.g. `50g|80g`).
- `image_urls`: CDN product image links.

### Source B: `data/india_cosmetics_brands_market_intel.csv` (Merged Market Intel)
Contains 100 comprehensive Indian beauty and personal care brand profiles. Every row represents a brand's market footprint, competitive landscape, customer feedback, and strategic white-spaces:

| Column | Content Format | What the Pipeline Extracts From It |
|---|---|---|
| **`product_info`** | `Brand \| Positioning \| Flagship Products \| Price Band` <br>*(e.g. `Minimalist \| Science-led actives \| 10% Vit C, 10% Niacinamide, SPF 50 \| ₹300-700`)* | **Competitor Products & Pricing:**<br>1. Brand name & category positioning<br>2. Flagship line items $\rightarrow$ individual `CompetitorProduct` entries<br>3. Price band $\rightarrow$ minimum, maximum, and average price per ml/g |
| **`customer_reviews`** | `Pos: <pros> \| Neg: <cons>` <br>*(e.g. `Pos: transparent percentages, visible results \| Neg: plain packaging, strong actives irritate beginners`)* | **Review Dataset & Sentiment Extraction:**<br>1. `Pos:` clauses $\rightarrow$ 5-star positive `Review` entries & key praises<br>2. `Neg:` clauses $\rightarrow$ 1-2 star friction `Review` entries & complaints<br>3. Text feeds into VADER + TextBlob for 16-topic tagging |
| **`competitors`** | Comma-separated substitute brands <br>*(e.g. `Dot & Key, The Derma Co, The Ordinary, Foxtale`)* | **Competitor Graph & Direct Matchmaking:**<br>Identifies who considers Dot & Key a direct substitute, forming the benchmark comparison pool |
| **`market_opportunities`** | Semicolon-separated strategic whitespaces <br>*(e.g. `Beginner routine kits; fragrance-free sensitive line; high-SPF no-cast sunscreen`)* | **Customer Acquisition & GTM Strategy:**<br>Direct inputs for Dot & Key product positioning, new product opportunities, and ad hooks |

---

## 3. How the Pipeline Unpacks the Merged CSV

In `src/data/loader.py`, the merged CSV is automatically transformed into the standard dataclass models expected by the rest of the pipeline:

### 1. Ingestion: `load_market_intel()`
Parses each row into a structured `BrandMarketIntel` record:
```python
@dataclass
class BrandMarketIntel:
    brand: str
    category: str
    flagship_lines: list[str]
    price_band: str
    min_price: float
    max_price: float
    positive_sentiment: list[str]
    negative_friction: list[str]
    competitors: list[str]
    market_opportunities: list[str]
```

### 2. Synthesizing `CompetitorProduct` Instances (`load_competitor_products()`)
- For each brand in the market intel file (excluding Dot & Key), each item in `flagship_lines` is turned into a `CompetitorProduct`.
- Category is mapped dynamically (e.g. items with *"sun"* $\rightarrow$ `Sunscreen`, *"serum"* $\rightarrow$ `Serum`, *"wash"* $\rightarrow$ `Face Wash`, *"cream"* $\rightarrow$ `Moisturizer`).
- Average price is derived from `(min_price + max_price) / 2`.
- Key claims are populated from `positive_sentiment`.

### 3. Synthesizing `Review` Records (`load_reviews()`)
- **Positive Reviews:** Each phrase in `Pos:` is converted into a positive `Review` instance (rating 5/5, sentiment score +0.85).
- **Negative / Friction Reviews:** Each phrase in `Neg:` is converted into a critical `Review` instance (rating 2/5, sentiment score -0.65).
- These reviews flow directly into `src/sentiment/analyzer.py` for keyword topic extraction across the 16 skincare categories (`texture`, `fragrance`, `white_cast`, `gentleness`, `irritation`, etc.).

---

## 4. Customer Market Acquisition Strategy Flow

The combination of the Dot & Key catalog and the merged market intel enables a **3-pillar Customer Market Acquisition Engine** in `src/insights/generator.py`:

```
┌────────────────────────────────────────────────────────────────────────┐
│      1. Competitor Defection Engine ("Switcher Campaigns")             │
│  - Reads competitor Neg: friction points from market intel             │
│  - Pairs each competitor weakness with a Dot & Key product strength    │
│  - Example:                                                            │
│    Minimalist: "Strong actives irritate beginners"                     │
│    --> Dot & Key Counter-Hook: "10% Niacinamide with Zinc PCA + Cica:   │
│        Maximum clinical clarity, ZERO beginner sting."                 │
│    The Derma Co: "Drying cleansers, mild irritation"                   │
│    --> Dot & Key Counter-Hook: "Cica Barrier Repair Cleanser:          │
│        Deep pore cleansing that restores moisture without stripping."  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│      2. Price-Band Arbitrage ("Accessible Luxury Positioning")         │
│  - Analyzes Price Bands across mass (₹150-400: Himalaya, Biotique)     │
│    vs prestige (₹1000-3500: Kama Ayurveda, Forest Essentials)          │
│  - Positions Dot & Key's ₹395-695 range as the Masstige sweet spot:    │
│    Sensorial textures and clean actives at a fraction of luxury costs  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────┐
│      3. Strategic Whitespace Exploitation                              │
│  - Ingests market_opportunities column directly                         │
│  - Identifies verified consumer gaps:                                  │
│    * "High-SPF no-white-cast sunscreen for melanin-rich skin"          │
│    * "Skin-tint / serum-hybrid makeup crossover"                       │
│    * "Fragrance-free sensitive skin lines"                             │
│  - Matches Dot & Key catalog products directly to these gaps           │
│    (e.g. Strawberry Dew Tinted Sunscreen, Watermelon Sunscreen SPF 50) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
                [Direct Input to Marketing Content Studio]
                - Static Ad Copy (Instagram 1:1, Facebook 1.91:1)
                - 30-Second Video Ad Script (Problem = Competitor flaw)
                - Amazon Product Listing Bullets & A+ Content
                - Reels / TikTok 15-Second UGC Video Concepts
```

---

## 5. Summary of Edits for the Pipeline Workflow

| Module | What Needs to Be Configured |
|---|---|
| **`src/models.py`** | Maintain pure dataclasses (`Product`, `CompetitorProduct`, `Review`, `BrandMarketIntel`, `CustomerAcquisitionStrategy`, `SWOTAnalysis`, `MarketingContent`). Keep decoupled from loaders to avoid circular imports. |
| **`src/data/loader.py`** | Loads `dotkey_products.csv` (Shopify schema) and `india_cosmetics_brands_market_intel.csv`. Provides `load_dotkey_products()`, `load_market_intel()`, `load_competitor_products()`, and `load_reviews()`. |
| **`src/catalog/extractor.py`** | Ingests from `load_dotkey_products()` instead of hardcoded lists. |
| **`src/competitor/monitor.py`** | Uses synthesized competitor products from `load_competitor_products()`. Compares unit pricing (₹/ml) against Dot & Key. |
| **`src/sentiment/analyzer.py`** | Evaluates reviews synthesized from `load_reviews()`, running dual-model NLP scoring (VADER + TextBlob) and 16-topic tagging. |
| **`src/insights/generator.py`** | Produces SWOT, Market Gaps, 90-day trend forecasts, and the **Customer Acquisition Strategy** derived from competitor friction points. |
| **`src/content/generator.py`** | Generates 8 marketing copy archetypes injecting the customer acquisition switcher hooks and brand guidelines. |
| **`src/api/main.py`** | FastAPI app with CORS serving endpoints (`/api/v1/products`, `/api/v1/products/{id}/insights`, `/api/v1/products/{id}/content`) to the React.js frontend. |

---

## 6. Execution Flow for Hackathon Demo

```bash
# Terminal 1: Start FastAPI Engine
uvicorn src.api.main:app --reload --port 8000
# Accessible at http://localhost:8000/docs

# Terminal 2: Start React.js Dashboard
cd frontend
npm run dev
# Accessible at http://localhost:5173
```
