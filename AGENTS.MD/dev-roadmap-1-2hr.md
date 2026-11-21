# ⚡ 1-2 Hour Hackathon Sprint Roadmap: VYBERS SkinSight-AI

> **Time Available:** 90–120 Minutes  
> **Architecture:** Decoupled Python (FastAPI) Backend + React.js (Vite + Tailwind CSS) Frontend  
> **Data Strategy:** Unified 2-CSV Architecture:
> 1. `data/dotkey_products.csv` (Dot & Key catalog from Shopify)
> 2. `data/india_cosmetics_brands_market_intel.csv` (100 Indian Brands — Products, Competitors, Pricing, Pos/Neg Reviews, Market Opportunities)

---

## ⏱️ Timeline Overview (90-Minute Target)

| Phase | Duration | Focus Area | Deliverable |
|---|---|---|---|
| **Phase 1** | Min 00–25 (25m) | **Data & FastAPI Backend Setup** | Merged CSV ingestion verified, FastAPI endpoints serving JSON |
| **Phase 2** | Min 25–50 (25m) | **React.js App Scaffold & UI Shell** | Vite + Tailwind + Lucide setup, Dot & Key design tokens, Navbar |
| **Phase 3** | Min 50–80 (30m) | **React.js Tab Implementation** | 4-tab interactive dashboard (Competitors, Sentiment, Acquisition/SWOT, Content) |
| **Phase 4** | Min 80–90 (10m) | **End-to-End Integration & Pitch** | Live walkthrough rehearsal connecting React to FastAPI |
| *Buffer* | Min 90–120 (30m) | **UI Polish / Copy-to-Clipboard** | Toast notifications, switcher hooks styling, markdown export |

---

## 🎯 Phase-by-Phase Plan

### 🟡 Phase 1: Data & FastAPI Backend Setup (Min 00 – 25)
**Goal:** Ingest the 2 primary CSVs, run the intelligence engine, and expose clean JSON endpoints for React.

- [x] **Data Ingestion:**
  - `data/dotkey_products.csv`: 30 real Dot & Key products (titles, prices, variants, ingredients).
  - `data/india_cosmetics_brands_market_intel.csv`: 100 brands (providing both competitor products and customer reviews).
- [ ] **Task 1.1: Verify Data Loader (`src/data/loader.py`):**
  - Verify `load_dotkey_products()` hydrates 30 `Product` dataclasses.
  - Verify `load_market_intel()` parses 100 `BrandMarketIntel` records.
  - Verify `load_competitor_products()` synthesizes competitor listings with pricing and flagship items.
  - Verify `load_reviews()` synthesizes positive (`Pos:`) and friction (`Neg:`) reviews.
- [ ] **Task 1.2: Pick 2 Hero Products for the Demo:**
  1. *Sunscreen:* Dot & Key Watermelon Sunscreen SPF 50 vs. Minimalist SPF 50, Derma Co Hyaluronic, Foxtale Dewy.
  2. *Serum:* Dot & Key 10% Niacinamide Serum vs. Minimalist 10% Niacinamide, Derma Co 10%, Deconstruct.
- [ ] **Task 1.3: Expose FastAPI Routes (`src/api/main.py`):**
  - `GET /api/v1/products`: List of all available Dot & Key products.
  - `GET /api/v1/products/{id}/insights`: Full competitor benchmarking, customer sentiment breakdown, SWOT, and customer acquisition switcher hooks.
  - `GET /api/v1/products/{id}/content`: Multi-platform marketing content deck.
  - Configure `CORSMiddleware` for `http://localhost:5173`.
- [ ] **Task 1.4: Verify Backend:** `uvicorn src.api.main:app --reload --port 8000` (check `http://localhost:8000/docs`).

**Checkpoint 1:** Swagger API responds with 200 OK and populated JSON containing competitor benchmarking and review sentiment.

---

### 🟢 Phase 2: React.js App Scaffold & UI Shell (Min 25 – 50)
**Goal:** Scaffold the frontend with Vite, Tailwind CSS, Lucide icons, and Dot & Key brand styles.

- [ ] **Task 2.1: Scaffold React Project:**
  ```bash
  npm create vite@latest frontend -- --template react
  cd frontend
  npm install
  npm install -D tailwindcss postcss autoprefixer lucide-react axios
  npx tailwindcss init -p
  ```
- [ ] **Task 2.2: Configure Brand Design Tokens (`tailwind.config.js`):**
  - Primary Pink: `#E85D75` (`bg-primary`, `text-primary`)
  - Secondary Cream: `#F5F0EB` (`bg-secondary`, `border-secondary`)
  - Accent Teal: `#4A90A4` (`bg-accent`, `text-accent`)
  - Dark Charcoal: `#2D2D2D` (`text-charcoal`)
- [ ] **Task 2.3: Build Core Components:**
  - `Navbar.jsx`: Logo, brand tagline (*Clean. Conscious. Effective.*), and product `<select>` dropdown.
  - State management in `App.jsx`: Stores `selectedProductId`, `productsList`, `insightsData`, `contentData`, and loading skeletons.

**Checkpoint 2:** React dev server runs on `http://localhost:5173` with a branded header and functional product selector.

---

### 🔵 Phase 3: React.js Tab Implementation (Min 50 – 80)
**Goal:** Build the 4 core interactive tabs consuming FastAPI data derived from the merged dataset.

#### Tab 1: 📊 Competitor Benchmarking (`CompetitorTab.jsx`)
- Side-by-side cards comparing Dot & Key vs. Top 5 Competitors (from market intel).
- Metrics: Price per ml (₹/ml), Rating stars, Unit Size, and Review Count.
- Green badge for Dot & Key advantages; yellow badge for competitor gaps.
- Active ingredient comparison chips (Shared vs. Unique).

#### Tab 2: 🗣️ Voice of Customer & NLP Sentiment (`SentimentTab.jsx`)
- Overall sentiment score meter (Dot & Key vs Competitor Average).
- Aspect bar chart or pill distribution (Texture, White Cast, Fragrance, Hydration, Irritation).
- Two-column card grid: **Top Praises** vs. **Critical Complaints** with clickable raw review quotes synthesized from `Pos:` and `Neg:` clauses.

#### Tab 3: 💡 Strategic Insights & Customer Acquisition (`InsightsTab.jsx`)
- **4-Quadrant SWOT Grid:** Strengths (green), Weaknesses (red), Opportunities (blue), Threats (yellow).
- **Customer Acquisition & Switcher Strategy Card:**
  - Highlights specific competitor friction points (e.g., *Minimalist beginner irritation*, *Derma Co drying cleansers*).
  - Displays generated counter-positioning ad hooks to poach unhappy competitor customers.
- **90-Day Demand Forecast:** Meter with trend direction (`Rising` / `Stable`) and key growth drivers.

#### Tab 4: 🚀 AI Marketing Content Studio (`ContentTab.jsx`)
- Sub-navigation pills: `Instagram Ad` | `Amazon Listing` | `30s Video Script` | `Storyboard` | `Reels Concept`.
- Clean card rendering with platform badges (1:1, 9:16).
- One-click **"Copy to Clipboard"** button with quick toast feedback.

**Checkpoint 3:** Full UI is functional. Changing the product in the dropdown re-fetches and live-updates all 4 tabs in `<1 second`.

---

### 🟣 Phase 4: Pitch Rehearsal & Live Walkthrough (Min 80 – 90)
**Goal:** Perfect the 2–3 minute live judge walkthrough.

- **The Pitch Narrative (2 Minutes):**
  1. *Hook (0:00–0:25):* "Skincare brands spend weeks conducting manual competitor research before launching marketing campaigns. VYBERS SkinSight-AI turns that entire research-to-creative cycle into a real-time full-stack intelligence app."
  2. *Competitor & Sentiment Intelligence (0:25–1:00):* Open the React dashboard. Select *Watermelon Sunscreen*. Show:
     - Competitor pricing gap vs Minimalist & Derma Co on Tab 1.
     - Customer sentiment showing real complaints on *white cast* & *makeup pilling* on Tab 2.
  3. *Customer Market Acquisition (1:00–1:30):* Switch to Tab 3 (Insights). Highlight the **Customer Switcher Strategy** directly weaponizing competitor weaknesses from 100 Indian cosmetics brands.
  4. *The Payoff (1:30–1:55):* Switch to Marketing Content Studio (Tab 4). Show that the generated 30-second Ad Script and Instagram ad hook specifically attack competitor weaknesses ("Zero White Cast, Sits Flawlessly Under Makeup"). Click "Copy Copy".
  5. *Evidence Defense (1:55–2:15):* "Notice every single ad angle is grounded in real customer quotes and catalog facts. Zero hallucinated data."

---

## 👥 If Working in a Team (Parallel Tracks)

| Person | Track | Responsibilities |
|---|---|---|
| **Member 1** (Backend & API) | `src/api/` + `src/insights/` | Expose FastAPI routes, verify merged CSV hydration, ensure sub-second response times. |
| **Member 2** (Frontend Core) | `frontend/` (Vite + React) | Scaffold app, setup Tailwind theme, build Navbar, CompetitorTab, and SentimentTab. |
| **Member 3** (Insights & Content UI) | `frontend/` (React Components) | Build SWOT grid, Customer Acquisition Switcher card, Marketing Content Studio, and copy buttons. |

---

## 🚨 Anti-Fail Guardrails (Hackathon Rules)

1. **Never scrape live during the demo:** Run strictly from the 2 cached CSVs in `data/`. Network timeouts will kill your demo.
2. **Handle Loading States in React:** Always render subtle skeleton loaders or spinners so switching products feels responsive.
3. **No fake numbers:** If judges ask *"Where did this ₹7.9/ml come from?"*, point directly to the normalized catalog pricing in the table.
