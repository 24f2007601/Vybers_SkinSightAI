"""
FastAPI Backend Application & Orchestrator for Dot & Key Market Intelligence System
Provides high-speed REST API endpoints for the React.js dashboard.
"""

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..models import Product, MarketingContent, ContentType, BRAND_GUIDELINES
from ..catalog.extractor import DotKeyCatalogExtractor
from ..competitor.monitor import CompetitorMonitor
from ..sentiment.analyzer import SentimentAnalyzer, ReviewCollector
from ..insights.generator import InsightsGenerator, MarketInsights
from ..content.generator import ContentGenerator, CONTENT_TEMPLATES
from ..data.loader import SAMPLE_DOTKEY_PRODUCTS, SAMPLE_MARKET_INTEL

# Initialize FastAPI App
app = FastAPI(
    title="VYBERS SkinSight-AI API",
    description="Market Intelligence, Competitor Benchmarking, Sentiment & Marketing Content Generation for Dot & Key",
    version="1.0.0",
)

# Configure CORS for React frontend (Vite default is 5173, Next/CRA is 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core orchestrator instance
catalog_extractor = DotKeyCatalogExtractor(use_sample_data=True)
insights_generator = InsightsGenerator(use_sample_data=True)
content_generator = ContentGenerator(brand_guidelines=BRAND_GUIDELINES)

# In-memory cache for fast sub-second response on repeated product selections
_INSIGHTS_CACHE: dict[str, dict] = {}
_CONTENT_CACHE: dict[str, dict] = {}


def _serialize_product(p: Product) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "subcategory": p.subcategory,
        "description": p.description,
        "ingredients": p.ingredients,
        "key_benefits": p.key_benefits,
        "skin_type": p.skin_type,
        "concerns": p.concerns,
        "price_inr": p.price_inr,
        "size_ml": p.size_ml,
        "image_urls": p.image_urls,
        "product_url": p.product_url,
        "tags": p.tags[:10] if p.tags else [],
    }


def _serialize_insights(product: Product, insights: MarketInsights) -> dict:
    return {
        "product": _serialize_product(product),
        "swot": {
            "strengths": insights.swot.strengths,
            "weaknesses": insights.swot.weaknesses,
            "opportunities": insights.swot.opportunities,
            "threats": insights.swot.threats,
        },
        "market_gaps": [
            {
                "description": gap.description,
                "evidence": gap.evidence,
                "potential_impact": gap.potential_impact,
                "suggested_action": gap.suggested_action,
            }
            for gap in insights.market_gaps
        ],
        "trend_forecast": {
            "category": insights.trend_forecast.category,
            "direction": insights.trend_forecast.trend_direction,
            "strength": round(insights.trend_forecast.trend_strength, 2),
            "predicted_demand_change_pct": round(insights.trend_forecast.predicted_demand_change_pct, 1),
            "key_drivers": insights.trend_forecast.key_drivers,
            "confidence": round(insights.trend_forecast.confidence, 2),
        },
        "sentiment": {
            "total_reviews": insights.sentiment_analysis.total_reviews,
            "avg_rating": insights.sentiment_analysis.average_rating,
            "overall_score": insights.sentiment_analysis.overall_sentiment_score,
            "top_positive": insights.sentiment_analysis.top_positive_topics,
            "top_negative": insights.sentiment_analysis.top_negative_topics,
            "praises": insights.sentiment_analysis.key_praises,
            "complaints": insights.sentiment_analysis.key_complaints,
            "sentiment_distribution": {
                k.value if hasattr(k, "value") else str(k): v
                for k, v in insights.sentiment_analysis.sentiment_distribution.items()
            },
        },
        "competitor_comparison": {
            "price_comparison": insights.competitor_comparison.price_comparison,
            "rating_comparison": insights.competitor_comparison.rating_comparison,
            "ingredient_overlap": insights.competitor_comparison.ingredient_overlap,
            "unique_competitor_ingredients": insights.competitor_comparison.unique_competitor_ingredients,
            "competitive_advantages": insights.competitor_comparison.competitive_advantages,
            "competitive_gaps": insights.competitor_comparison.competitive_gaps,
            "competitors": [
                {
                    "brand": c.brand,
                    "product_name": c.product_name,
                    "category": c.category,
                    "price_inr": c.price_inr,
                    "size_ml": c.size_ml,
                    "rating": c.rating,
                    "review_count": c.review_count,
                    "key_claims": c.key_claims,
                }
                for c in insights.competitor_comparison.competitor_products
            ],
        },
        "customer_acquisition": {
            "target_competitors": insights.customer_acquisition.target_competitors,
            "competitor_friction_points": insights.customer_acquisition.competitor_friction_points,
            "counter_positioning_claims": insights.customer_acquisition.counter_positioning_claims,
            "customer_switcher_hooks": insights.customer_acquisition.customer_switcher_hooks,
            "whitespace_opportunities": insights.customer_acquisition.whitespace_opportunities,
            "price_arbitrage_angle": insights.customer_acquisition.price_arbitrage_angle,
        },
        "recommendations": insights.recommendations,
        "generated_at": insights.generated_at.isoformat() if insights.generated_at else datetime.now().isoformat(),
    }


def _serialize_content_deck(product: Product, insights: MarketInsights) -> dict:
    content_map = {}
    for ctype in ContentType:
        platforms = list(CONTENT_TEMPLATES.get(ctype, {}).keys())
        for platform in platforms:
            try:
                c = content_generator.generate_content(product, insights, ctype, platform)
                key = f"{ctype.value}_{platform}"
                content_map[key] = {
                    "type": c.content_type.value,
                    "platform": c.platform,
                    "title": c.title,
                    "content": c.content,
                    "format_specs": c.format_specs,
                    "key_message": c.key_message,
                    "cta": c.cta,
                    "target_audience": c.target_audience,
                }
            except Exception as e:
                print(f"Error generating {ctype.value} for {platform}: {e}")
    return content_map


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    """Health check & API documentation link"""
    return {
        "service": "VYBERS SkinSight-AI API",
        "status": "online",
        "docs_url": "/docs",
        "brand": "Dot & Key",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/products")
async def get_products():
    """Returns all 30 Dot & Key products for the selector dropdown"""
    products = await catalog_extractor.extract_all_products()
    return [_serialize_product(p) for p in products]


@app.get("/api/v1/products/{product_id}")
async def get_product_details(product_id: str):
    """Returns single product details by id"""
    products = await catalog_extractor.extract_all_products()
    matched = [p for p in products if str(p.id) == str(product_id)]
    if not matched:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
    return _serialize_product(matched[0])


@app.get("/api/v1/products/{product_id}/insights")
async def get_product_insights(product_id: str):
    """
    Returns complete market intelligence payload:
    - Competitor Benchmarking & unit economics (Rs/ml)
    - Sentiment breakdown, top praises, critical complaints
    - 4-Quadrant SWOT
    - Customer Acquisition Strategy (Switcher Hooks targeting competitors)
    - Market Gaps & 90-day demand forecast
    """
    if product_id in _INSIGHTS_CACHE:
        return _INSIGHTS_CACHE[product_id]

    products = await catalog_extractor.extract_all_products()
    matched = [p for p in products if str(p.id) == str(product_id)]
    if not matched:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    product = matched[0]
    insights = await insights_generator.generate_insights(product)
    payload = _serialize_insights(product, insights)

    _INSIGHTS_CACHE[product_id] = payload
    return payload


@app.get("/api/v1/products/{product_id}/content")
async def get_product_marketing_content(product_id: str):
    """
    Returns ready-to-publish marketing content deck for the product:
    - Static Ads (Instagram 1:1, Facebook)
    - Product Description (Website & Amazon)
    - Amazon A+ Content Modules
    - 30-Second Video Ad Script (Scene-by-scene)
    - 7-Frame Storyboard Specifications
    - 15-Second Short-Form Video Concept
    """
    if product_id in _CONTENT_CACHE:
        return _CONTENT_CACHE[product_id]

    products = await catalog_extractor.extract_all_products()
    matched = [p for p in products if str(p.id) == str(product_id)]
    if not matched:
        raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

    product = matched[0]
    insights = await insights_generator.generate_insights(product)
    content_deck = _serialize_content_deck(product, insights)

    payload = {
        "product_id": product_id,
        "product_name": product.name,
        "generated_at": datetime.now().isoformat(),
        "brand_voice": BRAND_GUIDELINES.brand_voice,
        "content_pieces": content_deck,
    }

    _CONTENT_CACHE[product_id] = payload
    return payload


@app.get("/api/v1/market-landscape")
async def get_market_landscape(category: Optional[str] = None):
    """Returns overview of 100 Indian cosmetics brands and whitespace opportunities"""
    records = []
    for intel in SAMPLE_MARKET_INTEL[:25]:
        if not category or category.lower() in intel.category.lower():
            records.append({
                "brand": intel.brand,
                "category": intel.category,
                "price_band": intel.price_band,
                "positive_sentiment": intel.positive_sentiment,
                "negative_friction": intel.negative_friction,
                "market_opportunities": intel.market_opportunities,
            })
    return records


# ---------------------------------------------------------------------------
# CLI Pipeline Runner (Maintains compatibility with `python -m src.api.main`)
# ---------------------------------------------------------------------------

class DotKeyMarketIntelligence:
    """Main orchestrator for batch execution and report export"""

    def __init__(self, use_sample_data: bool = True, output_dir: str = "demo_output"):
        self.use_sample_data = use_sample_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.catalog_extractor = catalog_extractor
        self.insights_generator = insights_generator
        self.content_generator = content_generator

    async def run_full_pipeline(self) -> dict:
        print("[BOX] Extracting product catalog...")
        products = await self.catalog_extractor.extract_all_products()

        results = {
            "pipeline_run_at": datetime.now().isoformat(),
            "products_analyzed": len(products[:5]),
            "products": [],
        }

        # Analyze top 5 demo products
        for product in products[:5]:
            print(f"[SEARCH] Analyzing: {product.name}")
            insights = await self.insights_generator.generate_insights(product)
            serialized = _serialize_insights(product, insights)
            serialized["marketing_content"] = _serialize_content_deck(product, insights)
            results["products"].append(serialized)

        return results


async def demo():
    print("[START] Running Dot & Key Market Intelligence Pipeline...")
    system = DotKeyMarketIntelligence(use_sample_data=True, output_dir="demo_output")
    results = await system.run_full_pipeline()
    print(f"[DONE] Successfully analyzed {len(results['products'])} products!")


if __name__ == "__main__":
    asyncio.run(demo())
