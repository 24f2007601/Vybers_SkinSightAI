"""
Core data models for Dot & Key Market Intelligence System
Pure dataclasses with zero external module dependencies to avoid circular imports.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class Platform(Enum):
    """E-commerce platforms to monitor"""
    AMAZON = "amazon"
    FLIPKART = "flipkart"
    NYKAA = "nykaa"
    PURPLLE = "purplle"
    DOTKEY_OFFICIAL = "dotkey_official"
    MYNTRA = "myntra"


class SentimentLabel(Enum):
    """Sentiment classification"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class ContentType(Enum):
    """Marketing content types to generate"""
    STATIC_AD = "static_ad"
    PRODUCT_DESCRIPTION = "product_description"
    A_PLUS_CONTENT = "a_plus_content"
    AD_SCRIPT = "ad_script"
    STORYBOARD = "storyboard"
    VIDEO_CONCEPT = "video_concept"
    SOCIAL_MEDIA_POST = "social_media_post"
    EMAIL_CAMPAIGN = "email_campaign"


@dataclass
class Product:
    """Dot & Key product catalog entry"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    category: str = ""  # e.g., "Face Wash", "Sunscreen", "Serum", "Moisturizer"
    subcategory: str = ""  # e.g., "Vitamin C", "Niacinamide", "Hyaluronic Acid"
    description: str = ""
    ingredients: list[str] = field(default_factory=list)
    key_benefits: list[str] = field(default_factory=list)
    skin_type: list[str] = field(default_factory=list)  # oily, dry, combination, sensitive
    concerns: list[str] = field(default_factory=list)  # acne, aging, pigmentation, etc.
    price_inr: float = 0.0
    size_ml: float = 0.0
    image_urls: list[str] = field(default_factory=list)
    product_url: str = ""
    is_active: bool = True
    launched_date: Optional[datetime] = None
    tags: list[str] = field(default_factory=list)


@dataclass
class CompetitorProduct:
    """Competitor product entry extracted from market intel / e-commerce"""
    id: str = field(default_factory=lambda: str(uuid4()))
    brand: str = ""
    product_name: str = ""
    category: str = ""
    subcategory: str = ""
    price_inr: float = 0.0
    size_ml: float = 0.0
    rating: float = 0.0
    review_count: int = 0
    platform: Platform = Platform.AMAZON
    product_url: str = ""
    ingredients: list[str] = field(default_factory=list)
    key_claims: list[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    availability: bool = True


@dataclass
class Review:
    """Customer review synthesized from market intel & reviews dataset"""
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: str = ""  # references Product or CompetitorProduct or brand name
    platform: Platform = Platform.AMAZON
    rating: int = 0  # 1-5
    title: str = ""
    text: str = ""
    verified_purchase: bool = False
    helpful_votes: int = 0
    date: datetime = field(default_factory=datetime.now)
    sentiment: Optional[SentimentLabel] = None
    sentiment_score: float = 0.0  # -1 to 1
    key_phrases: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)  # extracted topics: fragrance, texture, effectiveness, etc.


@dataclass
class BrandMarketIntel:
    """Market intelligence record from india_cosmetics_brands_market_intel.csv"""
    brand: str = ""
    category: str = ""
    flagship_lines: list[str] = field(default_factory=list)
    price_band: str = ""
    min_price: float = 0.0
    max_price: float = 0.0
    positive_sentiment: list[str] = field(default_factory=list)
    negative_friction: list[str] = field(default_factory=list)
    competitors: list[str] = field(default_factory=list)
    market_opportunities: list[str] = field(default_factory=list)


@dataclass
class CustomerAcquisitionStrategy:
    """Actionable customer acquisition strategy derived from competitor weaknesses"""
    target_competitors: list[str] = field(default_factory=list)
    competitor_friction_points: dict[str, list[str]] = field(default_factory=dict)
    counter_positioning_claims: list[str] = field(default_factory=list)
    customer_switcher_hooks: list[str] = field(default_factory=list)
    whitespace_opportunities: list[str] = field(default_factory=list)
    price_arbitrage_angle: str = ""


@dataclass
class SentimentAnalysis:
    """Aggregated sentiment analysis for a product"""
    product_id: str = ""
    total_reviews: int = 0
    average_rating: float = 0.0
    sentiment_distribution: dict[SentimentLabel, int] = field(default_factory=dict)
    top_positive_topics: list[tuple[str, int]] = field(default_factory=list)
    top_negative_topics: list[tuple[str, int]] = field(default_factory=list)
    key_complaints: list[str] = field(default_factory=list)
    key_praises: list[str] = field(default_factory=list)
    overall_sentiment_score: float = 0.0


@dataclass
class CompetitorComparison:
    """Comparison between Dot & Key product and competitors"""
    dotkey_product_id: str = ""
    competitor_products: list[CompetitorProduct] = field(default_factory=list)
    price_comparison: dict[str, float] = field(default_factory=dict)  # brand -> price_per_ml
    rating_comparison: dict[str, float] = field(default_factory=dict)
    ingredient_overlap: dict[str, list[str]] = field(default_factory=dict)
    unique_competitor_ingredients: dict[str, list[str]] = field(default_factory=dict)
    competitive_advantages: list[str] = field(default_factory=list)
    competitive_gaps: list[str] = field(default_factory=list)


@dataclass
class SWOTAnalysis:
    """SWOT analysis for a product/category"""
    product_id: str = ""
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    threats: list[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class MarketGap:
    """Identified market gap"""
    id: str = field(default_factory=lambda: str(uuid4()))
    category: str = ""
    description: str = ""
    evidence: list[str] = field(default_factory=list)
    potential_impact: str = ""  # high, medium, low
    suggested_action: str = ""


@dataclass
class TrendForecast:
    """Market trend and sales forecast"""
    category: str = ""
    trend_direction: str = ""  # rising, stable, declining
    trend_strength: float = 0.0  # 0-1
    key_drivers: list[str] = field(default_factory=list)
    forecast_period_days: int = 90
    predicted_demand_change_pct: float = 0.0
    confidence: float = 0.0


@dataclass
class MarketingContent:
    """Generated marketing content"""
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: str = ""
    content_type: ContentType = ContentType.STATIC_AD
    title: str = ""
    content: str = ""
    platform: str = ""
    format_specs: dict = field(default_factory=dict)
    brand_voice: str = "Dot & Key"
    target_audience: str = ""
    key_message: str = ""
    cta: str = ""
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


@dataclass
class BrandGuidelines:
    """Dot & Key brand guidelines for content generation"""
    brand_name: str = "Dot & Key"
    tagline: str = "Clean. Conscious. Effective."
    brand_voice: str = "friendly, scientific, empowering, transparent"
    color_palette: dict[str, str] = field(default_factory=lambda: {
        "primary": "#E85D75",
        "secondary": "#F5F0EB",
        "accent": "#4A90A4",
        "text": "#2D2D2D",
        "background": "#FFFFFF"
    })
    typography: dict[str, str] = field(default_factory=lambda: {
        "heading": "Inter Bold",
        "body": "Inter Regular",
        "accent": "Playfair Display"
    })
    key_messages: list[str] = field(default_factory=lambda: [
        "Science-backed skincare",
        "Clean ingredients, no nasties",
        "Made for Indian skin",
        "Dermatologically tested",
        "Cruelty-free & vegan"
    ])
    prohibited_claims: list[str] = field(default_factory=lambda: [
        "permanent cure", "miracle", "instant results", "medical grade"
    ])
    target_demographics: dict = field(default_factory=lambda: {
        "age_range": "18-35",
        "gender": "primarily women",
        "location": "India (urban)",
        "income": "middle to upper-middle",
        "interests": ["skincare", "beauty", "wellness", "clean beauty"]
    })


BRAND_GUIDELINES = BrandGuidelines()
