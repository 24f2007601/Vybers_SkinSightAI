# ⚡ 1-2 Hour Hackathon Sprint Roadmap: VYBERS SkinSight-AI

> **Time Available:** 90–120 Minutes  
> **Goal:** Complete, working, bluff-free full-stack demo featuring a **Python (FastAPI) intelligence backend** and a modern **React.js web dashboard** showing **Product ➔ Competitor Compare ➔ Review Sentiment & SWOT ➔ Multi-Channel Marketing Content Deck**.

---

## ⏱️ Timeline Overview (90-Minute Target)

| Phase | Duration | Focus Area | Deliverable |
|---|---|---|---|
| **Phase 1** | Min 00–25 (25m) | **Data & FastAPI Backend Setup** | CSV loaders verified, FastAPI endpoints serving JSON |
| **Phase 2** | Min 25–50 (25m) | **React.js App Scaffold & UI Shell** | Vite + Tailwind + Lucide setup, Dot & Key design tokens, Navbar |
| **Phase 3** | Min 50–80 (30m) | **React.js Tab Implementation** | 4-tab interactive dashboard (Competitors, Sentiment, SWOT, Content) |
| **Phase 4** | Min 80–90 (10m) | **End-to-End Integration & Pitch** | Live walkthrough rehearsal connecting React to FastAPI |
| *Buffer* | Min 90–120 (30m) | **UI Polish / Copy-to-Clipboard** | Toast notifications, badge styling, export button |

---

## 🎯 Phase-by-Phase Plan

### 🟡 Phase 1: Data & FastAPI Backend Setup (Min 00 – 25)
**Goal:** Ensure the intelligence pipeline runs and exposes clean JSON endpoints for the React frontend.

- [x] `data/dotkey_products.csv` already created (30 real products from Shopify).
- [ ] **Task 1.1:** Pick **2 hero categories** for the demo:
  1. *Sunscreen:* Dot & Key Watermelon Sunscreen SPF 50 vs Minimalist SPF 50, Derma Co Hyaluronic, Foxtale Glow.
  2. *Serum:* Dot & Key 10% Niacinamide Serum vs Minimalist 10% Niacinamide, Derma Co 10%, Deconstruct.
- [ ] **Task 1.2:** Expose FastAPI routes in `src/api/main.py`:
  - `GET /api/v1/products`: List of Dot & Key products.
  - `GET /api/v1/products/{id}/insights`: Full competitor benchmarking, sentiment, and SWOT.
  - `GET /api/v1/products/{id}/content`: Multi-platform marketing content deck.
  - Add CORS middleware so React (`localhost:5173`) can communicate seamlessly.
- [ ] **Task 1.3:** Test backend in terminal: `uvicorn src.api.main:app --reload --port 8000`.

**Checkpoint 1:** Visiting `http://localhost:8000/docs` displays interactive Swagger API with green response payloads.

---

### 🟢 Phase 2: React.js App Scaffold & UI Shell (Min 25 – 50)
**Goal:** Scaffold the frontend with Vite, Tailwind CSS, and Dot & Key brand styles.

- [ ] **Task 2.1: Scaffold React Project:**
  ```bash
  npm create vite@latest frontend -- --template react
  cd frontend
  npm install
  npm install -D tailwindcss postcss autoprefixer lucide-react axios
  npx tailwindcss init -p
  ```
- [ ] **Task 2.2: Configure Brand Design Tokens** (`tailwind.config.js`):
  - Primary Pink: `#E85D75`
  - Secondary Cream: `#F5F0EB`
  - Accent Teal: `#4A90A4`
  - Dark Charcoal: `#2D2D2D`
- [ ] **Task 2.3: Build Core Components:**
  - `Navbar.jsx`: Logo, brand tagline (*Clean. Conscious. Effective.*), and `<select>` dropdown to switch active Dot & Key products.
  - State management in `App.jsx`: Stores `selectedProductId`, `productsList`, `insightsData`, `contentData`, and loading states.

**Checkpoint 2:** React dev server runs on `http://localhost:5173` with a branded header and functional product selector.

---

### 🔵 Phase 3: React.js Tab Implementation (Min 50 – 80)
**Goal:** Build the 4 core interactive tabs consuming FastAPI data.

#### Tab 1: 📊 Competitor Benchmarking (`CompetitorTab.jsx`)
- Side-by-side cards comparing Dot & Key vs. Top 5 Competitors.
- Metrics: Price per ml (₹/ml), Rating with star icons, Size, and Review Count.
- Green badge for Dot & Key advantages; yellow badge for competitor gaps.
- Active ingredient comparison chips (Shared vs. Unique).

#### Tab 2: 🗣️ Voice of Customer & NLP Sentiment (`SentimentTab.jsx`)
- Overall sentiment score meter (Dot & Key vs Competitor Average).
- Aspect bar chart or pill distribution (Texture, White Cast, Fragrance, Hydration).
- Two-column card grid: **Top Praises** vs. **Critical Complaints** with clickable raw review quotes.

#### Tab 3: 💡 Strategic Insights & SWOT (`InsightsTab.jsx`)
- 4-quadrant responsive grid: **Strengths** (green), **Weaknesses** (red), **Opportunities** (blue), **Threats** (yellow).
- Market gaps white-space list with potential business impact badges.
- 90-day demand forecast meter with direction badge (`Rising` / `Stable`).

#### Tab 4: 🚀 AI Marketing Content Studio (`ContentTab.jsx`)
- Sub-navigation pills: `Instagram Ad` | `Amazon Listing` | `30s Video Script` | `Storyboard` | `Reels Concept`.
- Clean card rendering with platform badges (1:1, 9:16).
- One-click **"Copy to Clipboard"** button with quick toast feedback.

**Checkpoint 3:** Full UI is functional. Changing the product in the dropdown re-fetches and live-updates all 4 tabs in `<1 second`.

---

### 🟣 Phase 4: Pitch Rehearsal & Live Walkthrough (Min 80 – 90)
**Goal:** Perfect the 2–3 minute judge walkthrough.

- **The Pitch Narrative (2 Minutes):**
  1. *Hook (0:00–0:25):* "Skincare brands spend weeks conducting manual market research before creating ad campaigns. VYBERS SkinSight-AI turns that entire research-to-creative cycle into a real-time full-stack intelligence app."
  2. *Live Action (0:25–1:15):* Open the React dashboard. Select *Watermelon Sunscreen*. Show:
     - Competitor pricing gap vs Minimalist & Derma Co on Tab 1.
     - Customer sentiment showing complaints on *white cast* & *makeup pilling* on Tab 2.
     - Automated SWOT highlighting Dot & Key's lightweight feel as a strength on Tab 3.
  3. *The Payoff (1:15–1:50):* Switch to Marketing Content Studio (Tab 4). Show that the generated 30-second Ad Script and Instagram ad hook specifically attack competitor weaknesses ("Zero White Cast, Sits Flawlessly Under Makeup"). Click "Copy Copy".
  4. *Evidence Defense (1:50–2:10):* "Notice every single ad angle is grounded in real customer quotes and catalog facts. Zero hallucinated data."

---

## 👥 If Working in a Team (Parallel Tracks)

| Person | Track | Responsibilities |
|---|---|---|
| **Member 1** (Backend & API) | `src/api/` + `src/insights/` | Expose FastAPI routes, ensure fast response payloads, verify CORS. |
| **Member 2** (Frontend Core) | `frontend/` (Vite + React) | Scaffold app, setup Tailwind theme, build Navbar and Tab 1 & Tab 2. |
| **Member 3** (Frontend Insights & Deck) | `frontend/` (React Components) | Build SWOT 4-quadrant grid, Marketing Content Studio, Copy buttons, and pitch deck. |

---

## 🚨 Anti-Fail Guardrails (Hackathon Rules)

1. **Never scrape live during the demo:** Run strictly from cached CSVs in `data/`. Network timeouts will kill your demo.
2. **Handle Loading States in React:** Always render subtle skeleton loaders or spinners so switching products feels responsive.
3. **No fake numbers:** If judges ask *"Where did this ₹7.9/ml come from?"*, point directly to the normalized catalog pricing in the table.
