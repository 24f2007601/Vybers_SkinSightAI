# PIPELINE WORKFLOW & CSV INTEGRATION ARCHITECTURE

> **Target Sprint:** 1–2 Hour Hackathon Execution (Decoupled FastAPI + React.js)  
> **Source Document:** Derived from `AGENTS.MD/dev-roadmap-1-2hr.md` and `AGENTS.MD/PRD.md`

---

## 1. End-to-End Pipeline Workflow (CSV ➔ Engine ➔ React API)

```
[data/dotkey_products.csv]       [data/competitor_products.csv]       [data/reviews.csv]
           │                                   │                               │
           └───────────────────────────┬───────┴───────────────────────────────┘
                                       ▼
                             src/data/loader.py
                      (Hydrates typed Dataclass models)
                                       │
           ┌───────────────────────────┴───────────────────────────┐
           ▼                                                       ▼
src/catalog/extractor.py                                src/competitor/monitor.py
 (Dot & Key catalog list)                               (Matches category & ranks
           │                                             top 5 by review density)
           │                                                       │
           └───────────────────────────┬───────────────────────────┘
                                       ▼
                           src/sentiment/analyzer.py
                      (VADER + TextBlob hybrid scoring,
                        16 topical keywords & quotes)
                                       │
                                       ▼
                           src/insights/generator.py
                       (Unit pricing ₹/ml normalization,
                        Ingredient set diffs, SWOT, Gaps,
                         90-day demand forecast indicator)
                                       │
                                       ▼
                           src/content/generator.py
                     (Injects insights into 8 brand copy
                       templates with claims guardrails)
                                       │
                                       ▼
                              src/api/main.py
                          (FastAPI REST Endpoints)
                     ├── GET /api/v1/products
                     ├── GET /api/v1/products/{id}/insights
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
| **`data/dotkey_products.csv`** | 30 real products extracted from Shopify API | `src/catalog/extractor.py` reads this. Feeds product name, price, ingredients, and claims. |
| **`data/competitor_products.csv`** | 15 curated products across Minimalist, Derma Co, Plum, Foxtale, etc. | `src/competitor/monitor.py` filters by `category` and `subcategory`, ranks top 5 using: $$\text{Rating} \times \left(1 + \frac{\sqrt{\text{Reviews}}}{100}\right)$$ and normalizes unit price to **₹ / ml** or **₹ / g**. |
| **`data/reviews.csv`** | Raw customer reviews with star ratings and platforms | `src/sentiment/analyzer.py` runs dual NLP (VADER + TextBlob) to categorize sentiment and map to the 16 topical tags (`white_cast`, `pilling`, `fragrance`, `texture`, etc.). |
| **`data/india_cosmetics_brands_market_intel.csv`** | 50+ brand intelligence matrix | Feeds competitor market positioning and whitespace opportunities in `src/insights/generator.py`. |

---

## 3. Required Edits to Execute `dev-roadmap-1-2hr.md`

To make this pipeline run fast, deterministic, and bug-free within the 1–2 hour sprint, the following **4 targeted edits** are required:

### 🛠️ Edit 1: Fix `src/models.py` Circular Dependency & Cleanup
- **Issue:** `models.py` still has residual deleted code and imports `src/data/loader.py`, which imports `models.py` (circular import causing `IndentationError`).
- **Fix:**
  - Keep pure dataclasses in `src/models.py`.
  - Remove all circular imports from `src/data/loader.py` into `models.py`.
  - Ensure all modules import data via `src.data.loader`.

### 🛠️ Edit 2: Adapt `src/data/loader.py` to Real Shopify Columns
- **Issue:** The newly generated `data/dotkey_products.csv` uses Shopify column names:
  - `title` instead of `name`
  - `prices_inr` instead of `price_inr`
  - `product_type` instead of `category`
  - `tags` instead of `key_benefits`
- **Fix in `loader.py`:** Add field mapping in `load_dotkey_products()`:
```python
price_val = float(row["prices_inr"].split("|")[0]) if row.get("prices_inr") else 0.0
size_val = float(re.search(r"\d+", row.get("sizes", "50")).group()) if re.search(r"\d+", row.get("sizes", "")) else 50.0

Product(
    id=str(row["id"]),
    name=row["title"],
    category=row.get("product_type") or "Skincare",
    subcategory=row.get("handle", ""),
    price_inr=price_val,
    size_ml=size_val,
    description=row.get("description", ""),
    tags=row.get("tags", "").split("|")
)
```

### 🛠️ Edit 3: Turn `src/api/main.py` into a FastAPI App with CORS
- **Issue:** `src/api/main.py` is currently a standalone CLI script that prints to terminal and saves local files. The React frontend needs JSON endpoints.
- **Fix:** Add FastAPI endpoints and `CORSMiddleware` in `src/api/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VYBERS SkinSight-AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/products")
async def get_products():
    system = DotKeyMarketIntelligence(use_sample_data=True)
    return await system.catalog_extractor.extract_all_products()

@app.get("/api/v1/products/{product_id}/analysis")
async def get_product_analysis(product_id: str):
    system = DotKeyMarketIntelligence(use_sample_data=True)
    products = await system.catalog_extractor.extract_all_products()
    matched = [p for p in products if str(p.id) == str(product_id)]
    if not matched:
        return {"error": "Product not found"}
    return await system.analyze_product(matched[0])
```

### 🛠️ Edit 4: Scaffold the React Frontend (`frontend/`)
- **Action:** Run Phase 2 of the roadmap:
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer lucide-react axios
npx tailwindcss init -p
```
Connect `App.jsx` to fetch `http://localhost:8000/api/v1/products` on load and render the 4 tabs:
1. `CompetitorTab`
2. `SentimentTab`
3. `InsightsTab`
4. `ContentTab` (with one-click copy button)

---

## 4. Execution Sequence (Immediate Next Steps)

1. **Step 1:** Fix `src/models.py` and `src/data/loader.py` so running `python -c "from src.data.loader import load_dotkey_products; print(len(load_dotkey_products()))"` outputs `30`.
2. **Step 2:** Wrap `src/api/main.py` with FastAPI and verify `uvicorn src.api.main:app --port 8000` serves `/docs`.
3. **Step 3:** Scaffold `frontend/` and connect the Axios calls to display the dashboard.
