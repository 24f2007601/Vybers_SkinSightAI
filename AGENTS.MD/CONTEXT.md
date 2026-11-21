# PROJECT CONTEXT & DOMAIN KNOWLEDGE BASE

## 1. Domain Overview: Indian Beauty & Personal Care (BPC)
The Indian skincare and cosmetics landscape is rapidly shifting toward **active ingredient awareness** ("skintellectuals"), **clean beauty**, and **masstige/D2C-first models**. Consumers evaluate products based on:
1. **Active Ingredients & Transparency:** Niacinamide, Vitamin C, Salicylic Acid, Ceramides, Hyaluronic Acid, Retinol.
2. **Sensory & Climatic Suitability:** Lightweight, non-sticky, fast-absorbing, no white-cast on melanin-rich skin, sweat/humidity-resistant formulations.
3. **Value Proposition:** Price per ml/gram comparisons against traditional FMCG vs pure clinical brands.

---

## 2. Competitive Landscape Benchmark

| Brand | Positioning | Core Range | Price Tier | Consumer Positives | Consumer Negatives | Key Competitors |
|---|---|---|---|---|---|---|
| **Dot & Key** | D2C Fruit-forward active skincare | Vitamin C+E, Watermelon Sunscreen, Cica, Ceramides | ₹300 - ₹900 (Masstige) | Lightweight textures, great hydration, pleasant sensorial feel, aesthetic packaging | Fragrance irritation for sensitive skin, white-cast on older sunscreens | Minimalist, Plum, The Derma Co, Foxtale, Pilgrim |
| **Minimalist** | Transparent clinical actives | 10% Niacinamide, 10% Vit C, Ceramide 0.3%, SPF 50 | ₹300 - ₹700 (Affordable-Science) | High ingredient transparency, clinical efficacy, fragrance-free | Plain apothecary packaging, initial purging/irritation | The Ordinary, Dot & Key, The Derma Co, Deconstruct |
| **The Derma Co** | Dermatologist-partnered actives | 1% Hyaluronic Sunscreen, 2% Salicylic Cleanser | ₹300 - ₹800 (Derma-accessible) | Quick action on active acne, high-spreadability sunscreen | Cleanser over-drying, batch consistency issues | Minimalist, Dot & Key, Fixderma, Cetaphil |
| **Plum** | 100% Vegan & cruelty-free clean | Green Tea line, 15% Vit C, Niacinamide Rice Water | ₹300 - ₹800 (Clean mass) | Gentle on oily/acne skin, ethical branding | Fragrance intensity, pump/dispenser clogs | Mamaearth, Dot & Key, The Body Shop |
| **Foxtale** | High-performance sensorial actives | Dewy Sunscreen, CoverUp Duos, Vit C | ₹350 - ₹850 (Trendy Gen-Z) | Instant cosmetic glow, multi-functional makeup-skincare | Scent intensity, oily finish on extreme summer days | Dot & Key, Plum, The Derma Co |

---

## 3. Data Catalog & File Specs

### A. `data/dotkey_products.csv`
Source: Official Shopify catalog extraction (`https://dotandkey.com/products.json`).
- **Columns:**
  - `id`: Shopify unique product identifier.
  - `title`: Commercial title (e.g. *Watermelon Hydrating Sunscreen SPF 50 PA+++*).
  - `handle`: URL slug identifier.
  - `product_type`: Categorization (e.g. `Face Wash`, `Sunscreen`, `Moisturiser`, `Lip Balm`, `Combo`).
  - `vendor`: `Dot & Key`.
  - `tags`: Pipe-separated attribute list (`fltr_ingredients_Ceramide|bestseller|...`).
  - `description`: Plaintext summary of formula, claims, and usage.
  - `prices_inr`: Variant prices in INR (pipe-delimited if multi-variant).
  - `sizes`: Sizes/Volumes (e.g. `50g|80g`).
  - `image_urls`: CDN product image links.
  - `published_at`, `created_at`, `updated_at`: Timestamps.

### B. `data/india_cosmetics_brands_market_intel.csv`
Source: 50+ Brand comprehensive Indian market intelligence matrix.
- **Columns:**
  - `product_info`: `Brand | Category | Flagship Lines | Price Band`
  - `customer_reviews`: `Pos: <pros> | Neg: <cons>`
  - `competitors`: Comma-separated list of direct market substitutes.
  - `market_opportunities`: Specific whitespace formulation and marketing opportunities.

### C. `data/competitor_products.csv`
Curated benchmark set of competitive cross-references for direct algorithmic comparison (price per ml, ingredient match percentage, ratings).

### D. `data/reviews.csv`
Pre-annotated sentiment and topical customer feedback records across Amazon, Flipkart, Nykaa, and Purplle.

---

## 4. Dot & Key Brand Guide Guidelines (`BrandGuidelines`)

- **Tone & Voice:** Friendly, conversational, scientific yet accessible, empowering, transparent.
- **Brand Identity:** Fruit-forward + dermatological active synergy ("Science meets Nature").
- **Target Demographics:** Women and men aged 18–35, urban India (Tier 1 & Tier 2 metros), looking for efficacious, aesthetic, clean personal care.
- **Visual Palette:**
  - Primary Pink: `#E85D75`
  - Secondary Cream: `#F5F0EB`
  - Ocean Accent: `#4A90A4`
  - Charcoal Text: `#2D2D2D`
  - Pure Canvas: `#FFFFFF`
- **Prohibited & Restricted Copy:**
  - ❌ NEVER use: "miracle cure", "instant permanent fix", "100% white skin", "medical grade", "treats all diseases".
  - ✅ ALWAYS emphasize: "Dermatologically tested", "Cruelty-free & vegan", "Formulated for Indian skin", "Clinical results without irritation".

---

## 5. Standard Output Contracts
- **Per-product JSON:** `<output_dir>/<product_id>_<product_name>.json`
- **Consolidated Executive Brief:** `<output_dir>/SUMMARY_REPORT.md` containing:
  1. Executive Summary & Timestamp.
  2. Product by Product SWOT Matrix.
  3. Identified Market Gaps & Actionable Solution.
  4. 90-Day Trend & Demand Forecasting.
  5. Top Customer Praises & Complaints.
  6. Multi-Channel Marketing Content Deck.
