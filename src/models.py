"""
Core data models for Dot & Key Market Intelligence System
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
    """Competitor product entry"""
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
    """Customer review"""
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: str = ""  # references Product or CompetitorProduct
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
class SentimentAnalysis:
    """Aggregated sentiment analysis for a product"""
    product_id: str = ""
    total_reviews: int = 0
    average_rating: float = 0.0
    sentiment_distribution: dict[SentimentLabel, int] = field(default_factory=dict)
    top_positive_topics: list[tuple[str, int]] = field(default_factory=list)  # (topic, count)
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
    ingredient_overlap: dict[str, list[str]] = field(default_factory=dict)  # brand -> common ingredients
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
    evidence: list[str] = field(default_factory=list)  # supporting data points
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
    content: str = ""  # main content body
    platform: str = ""  # instagram, facebook, amazon, website, youtube, etc.
    format_specs: dict = field(default_factory=dict)  # dimensions, duration, etc.
    brand_voice: str = "Dot & Key"  # friendly, scientific, empowering
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


# ---------------------------------------------------------------------------
# Sample data — loaded from data/ CSVs via src/data/loader.py
# Keep these imports here so existing code (e.g. insights/generator.py) that
# does `from ..models import SAMPLE_DOTKEY_PRODUCTS` continues to work unchanged.
# ---------------------------------------------------------------------------
from .data.loader import (  # noqa: E402  (import not at top of file)
    SAMPLE_COMPETITOR_BRANDS,
    SAMPLE_COMPETITOR_PRODUCTS,
    SAMPLE_DOTKEY_PRODUCTS,
    SAMPLE_REVIEWS,
)

# ---------------------------------------------------------------------------
# (deleted) hardcoded SAMPLE_* lists — now sourced from data/ CSVs
# ---------------------------------------------------------------------------
# fmt: off — the block below was removed; keeping this comment for git history
# SAMPLE_DOTKEY_PRODUCTS = [Product(id="dk-001",
        name="Vitamin C + E Super Bright Face Wash",
        category="Face Wash",
        subcategory="Vitamin C",
        description="A gentle yet effective face wash powered by Vitamin C & E that brightens dull skin, fades dark spots, and gives a radiant glow.",
        ingredients=["Vitamin C", "Vitamin E", "Aloe Vera", "Glycerin", "Coconut-based surfactants"],
        key_benefits=["Brightens skin", "Fades dark spots", "Gentle cleansing", "Radiant glow"],
        skin_type=["all", "dull", "uneven tone"],
        concerns=["dullness", "pigmentation", "uneven tone"],
        price_inr=395.0,
        size_ml=100.0,
        image_urls=["https://dotkey.in/cdn/shop/files/vitamin-c-face-wash.jpg"],
        product_url="https://dotkey.in/products/vitamin-c-e-super-bright-face-wash",
        tags=["bestseller", "vitamin-c", "brightening"],
        launched_date=datetime(2023, 6, 15)
    ),
    Product(
        id="dk-002",
        name="Watermelon Hydrating Sunscreen SPF 50 PA+++",
        category="Sunscreen",
        subcategory="Hydrating",
        description="Lightweight, non-greasy sunscreen with watermelon extract that hydrates while protecting against UVA/UVB rays. No white cast.",
        ingredients=["Watermelon Extract", "Hyaluronic Acid", "Zinc Oxide", "Titanium Dioxide", "Vitamin E"],
        key_benefits=["SPF 50 PA+++", "No white cast", "Hydrating", "Lightweight", "Non-comedogenic"],
        skin_type=["oily", "combination", "acne-prone", "sensitive"],
        concerns=["sun protection", "hydration", "white cast"],
        price_inr=595.0,
        size_ml=50.0,
        image_urls=["https://dotkey.in/cdn/shop/files/watermelon-sunscreen.jpg"],
        product_url="https://dotkey.in/products/watermelon-hydrating-sunscreen",
        tags=["bestseller", "sunscreen", "hydrating", "no-white-cast"],
        launched_date=datetime(2023, 3, 10)
    ),
    Product(
        id="dk-003",
        name="Niacinamide 10% + Zinc PCA Serum",
        category="Serum",
        subcategory="Niacinamide",
        description="High-strength niacinamide serum that minimizes pores, controls oil, reduces acne marks, and improves skin texture.",
        ingredients=["Niacinamide 10%", "Zinc PCA", "Hyaluronic Acid", "Panthenol", "Allantoin"],
        key_benefits=["Minimizes pores", "Controls excess oil", "Fades acne marks", "Improves texture"],
        skin_type=["oily", "combination", "acne-prone"],
        concerns=["large pores", "acne marks", "excess oil", "uneven texture"],
        price_inr=495.0,
        size_ml=30.0,
        image_urls=["https://dotkey.in/cdn/shop/files/niacinamide-serum.jpg"],
        product_url="https://dotkey.in/products/niacinamide-10-zinc-pca-serum",
        tags=["niacinamide", "pore-minimizing", "oil-control"],
        launched_date=datetime(2023, 8, 22)
    ),
    Product(
        id="dk-004",
        name="Ceramide + Hyaluronic Acid Barrier Repair Moisturizer",
        category="Moisturizer",
        subcategory="Barrier Repair",
        description="Rich yet fast-absorbing moisturizer with 3 essential ceramides and hyaluronic acid to repair skin barrier and lock in hydration.",
        ingredients=["Ceramide NP", "Ceramide AP", "Ceramide EOP", "Hyaluronic Acid", "Squalane", "Oat Extract"],
        key_benefits=["Repairs skin barrier", "Deep hydration", "Soothes irritation", "Non-greasy"],
        skin_type=["dry", "sensitive", "compromised barrier", "eczema-prone"],
        concerns=["dryness", "sensitivity", "barrier damage", "irritation"],
        price_inr=545.0,
        size_ml=50.0,
        image_urls=["https://dotkey.in/cdn/shop/files/ceramide-moisturizer.jpg"],
        product_url="https://dotkey.in/products/ceramide-hyaluronic-acid-moisturizer",
        tags=["ceramide", "barrier-repair", "hydrating"],
        launched_date=datetime(2024, 1, 18)
    ),
    Product(
        id="dk-005",
        name="Retinol 0.3% + Bakuchiol Night Repair Serum",
        category="Serum",
        subcategory="Retinol",
        description="Gentle retinol alternative with bakuchiol that reduces fine lines, improves elasticity, and evens skin tone without irritation.",
        ingredients=["Retinol 0.3%", "Bakuchiol", "Peptides", "Squalane", "Vitamin E"],
        key_benefits=["Reduces fine lines", "Improves elasticity", "Evens tone", "Gentle on skin"],
        skin_type=["normal", "combination", "aging", "mature"],
        concerns=["fine lines", "wrinkles", "loss of elasticity", "uneven tone"],
        price_inr=695.0,
        size_ml=30.0,
        image_urls=["https://dotkey.in/cdn/shop/files/retinol-serum.jpg"],
        product_url="https://dotkey.in/products/retinol-bakuchiol-night-serum",
        tags=["retinol", "anti-aging", "bakuchiol", "night-repair"],
        launched_date=datetime(2024, 5, 12)
    ),
]

SAMPLE_COMPETITOR_BRANDS = [
    "Minimalist",
    "The Derma Co",
    "Plum",
    "Mamaearth",
    "WOW Skin Science",
    "Pilgrim",
    "Foxtale",
    "Deconstruct",
    "Simple",
    "Neutrogena"
]

SAMPLE_COMPETITOR_PRODUCTS = [
    # Vitamin C Face Wash competitors
    CompetitorProduct(
        brand="Minimalist",
        product_name="Vitamin C 10% Face Wash",
        category="Face Wash",
        subcategory="Vitamin C",
        price_inr=299.0,
        size_ml=100.0,
        rating=4.3,
        review_count=12450,
        platform=Platform.AMAZON,
        ingredients=["Vitamin C 10%", "Glycerin", "Aloe Vera"],
        key_claims=["Brightens", "Reduces tan", "Gentle"],
    ),
    CompetitorProduct(
        brand="The Derma Co",
        product_name="Vitamin C Face Wash with Hyaluronic Acid",
        category="Face Wash",
        subcategory="Vitamin C",
        price_inr=349.0,
        size_ml=100.0,
        rating=4.2,
        review_count=8920,
        platform=Platform.AMAZON,
        ingredients=["Vitamin C", "Hyaluronic Acid", "Aloe Vera"],
        key_claims=["Hydrating", "Brightening", "Anti-aging"],
    ),
    CompetitorProduct(
        brand="Plum",
        product_name="Vitamin C Face Wash with White Tea",
        category="Face Wash",
        subcategory="Vitamin C",
        price_inr=395.0,
        size_ml=100.0,
        rating=4.4,
        review_count=6780,
        platform=Platform.NYKAA,
        ingredients=["Vitamin C", "White Tea Extract", "Grapefruit Extract"],
        key_claims=["Antioxidant", "Glow", "Vegan"],
    ),
    # Watermelon Sunscreen competitors
    CompetitorProduct(
        brand="Minimalist",
        product_name="SPF 50 PA+++ Sunscreen",
        category="Sunscreen",
        subcategory="Hydrating",
        price_inr=399.0,
        size_ml=50.0,
        rating=4.5,
        review_count=15670,
        platform=Platform.AMAZON,
        ingredients=["Ethylhexyl Methoxycinnamate", "Avobenzone", "Vitamin E"],
        key_claims=["Broad spectrum", "Non-greasy", "No white cast"],
    ),
    CompetitorProduct(
        brand="The Derma Co",
        product_name="Hyaluronic Sunscreen SPF 50",
        category="Sunscreen",
        subcategory="Hydrating",
        price_inr=449.0,
        size_ml=50.0,
        rating=4.3,
        review_count=9840,
        platform=Platform.FLIPKART,
        ingredients=["Hyaluronic Acid", "Zinc Oxide", "Titanium Dioxide"],
        key_claims=["Hydrating", "Mineral filter", "Blue light protection"],
    ),
    CompetitorProduct(
        brand="Foxtale",
        product_name="Glow Sunscreen SPF 50 PA+++",
        category="Sunscreen",
        subcategory="Glow",
        price_inr=495.0,
        size_ml=50.0,
        rating=4.6,
        review_count=11230,
        platform=Platform.NYKAA,
        ingredients=["Niacinamide", "Vitamin C", "Hyaluronic Acid", "SPF filters"],
        key_claims=["Glow finish", "Niacinamide", "Vitamin C", "Makeup base"],
    ),
    # Niacinamide Serum competitors
    CompetitorProduct(
        brand="Minimalist",
        product_name="Niacinamide 10% Serum",
        category="Serum",
        subcategory="Niacinamide",
        price_inr=299.0,
        size_ml=30.0,
        rating=4.4,
        review_count=23450,
        platform=Platform.AMAZON,
        ingredients=["Niacinamide 10%", "Zinc PCA", "Hyaluronic Acid"],
        key_claims=["Pore minimizing", "Oil control", "Acne marks"],
    ),
    CompetitorProduct(
        brand="The Derma Co",
        product_name="10% Niacinamide Serum",
        category="Serum",
        subcategory="Niacinamide",
        price_inr=399.0,
        size_ml=30.0,
        rating=4.2,
        review_count=12340,
        platform=Platform.AMAZON,
        ingredients=["Niacinamide 10%", "Zinc", "Hyaluronic Acid", "Vitamin B5"],
        key_claims=["Oil control", "Pore refining", "Barrier support"],
    ),
    CompetitorProduct(
        brand="Deconstruct",
        product_name="Niacinamide 10% + Zinc 1% Serum",
        category="Serum",
        subcategory="Niacinamide",
        price_inr=349.0,
        size_ml=30.0,
        rating=4.5,
        review_count=8760,
        platform=Platform.PURPLLE,
        ingredients=["Niacinamide 10%", "Zinc PCA 1%", "Hyaluronic Acid"],
        key_claims=["Clinically proven", "Dermatologist tested", "Fragrance-free"],
    ),
    # Ceramide Moisturizer competitors
    CompetitorProduct(
        brand="Minimalist",
        product_name="Ceramide 0.3% + Madecassoside Moisturizer",
        category="Moisturizer",
        subcategory="Barrier Repair",
        price_inr=399.0,
        size_ml=50.0,
        rating=4.6,
        review_count=14560,
        platform=Platform.AMAZON,
        ingredients=["Ceramide NP", "Madecassoside", "Panthenol", "Squalane"],
        key_claims=["Barrier repair", "Soothing", "Cica"],
    ),
    CompetitorProduct(
        brand="Plum",
        product_name="Ceramide & Peptide Moisturizer",
        category="Moisturizer",
        subcategory="Barrier Repair",
        price_inr=475.0,
        size_ml=50.0,
        rating=4.3,
        review_count=5670,
        platform=Platform.NYKAA,
        ingredients=["Ceramide Complex", "Peptides", "Hyaluronic Acid", "Oat"],
        key_claims=["Anti-aging", "Firming", "Barrier repair"],
    ),
    CompetitorProduct(
        brand="Simple",
        product_name="Kind to Skin Replenishing Rich Moisturizer",
        category="Moisturizer",
        subcategory="Barrier Repair",
        price_inr=299.0,
        size_ml=75.0,
        rating=4.2,
        review_count=8900,
        platform=Platform.FLIPKART,
        ingredients=["Ceramide", "Glycerin", "Panthenol", "Bisabolol"],
        key_claims=["Sensitive skin", "Dermatologist approved", "No perfume"],
    ),
    # Retinol Serum competitors
    CompetitorProduct(
        brand="Minimalist",
        product_name="Retinol 0.3% Serum with Squalane",
        category="Serum",
        subcategory="Retinol",
        price_inr=399.0,
        size_ml=30.0,
        rating=4.3,
        review_count=9870,
        platform=Platform.AMAZON,
        ingredients=["Retinol 0.3%", "Squalane", "Vitamin E"],
        key_claims=["Anti-aging", "Fine lines", "Squalane buffer"],
    ),
    CompetitorProduct(
        brand="The Derma Co",
        product_name="Retinol 0.5% Serum",
        category="Serum",
        subcategory="Retinol",
        price_inr=499.0,
        size_ml=30.0,
        rating=4.1,
        review_count=6540,
        platform=Platform.AMAZON,
        ingredients=["Retinol 0.5%", "Bakuchiol", "Peptides", "Hyaluronic Acid"],
        key_claims=["Higher retinol", "Bakuchiol", "Peptide complex"],
    ),
    CompetitorProduct(
        brand="Pilgrim",
        product_name="Retinol Night Serum with Bakuchiol",
        category="Serum",
        subcategory="Retinol",
        price_inr=549.0,
        size_ml=30.0,
        rating=4.4,
        review_count=4320,
        platform=Platform.NYKAA,
        ingredients=["Retinol", "Bakuchiol", "Squalane", "Vitamin E"],
        key_claims=["K-beauty", "Gentle retinol", "Overnight repair"],
    ),
]

SAMPLE_REVIEWS = [
    # Dot & Key Vitamin C Face Wash reviews
    Review(product_id="dk-001", platform=Platform.AMAZON, rating=5, title="Love this face wash!",
           text="Been using for 2 months and my skin has never looked brighter. The Vitamin C actually works on my dark spots from acne. Gentle enough for daily use.",
           verified_purchase=True, helpful_votes=45, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.85,
           key_phrases=["brighter skin", "dark spots fade", "gentle", "daily use"],
           topics=["brightening", "pigmentation", "gentleness"]),
    Review(product_id="dk-001", platform=Platform.AMAZON, rating=4, title="Good but takes time",
           text="Nice face wash, smells good and doesn't strip my skin. Dark spots are fading but slowly - been 6 weeks. Good value for money.",
           verified_purchase=True, helpful_votes=23, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.65,
           key_phrases=["doesn't strip", "slow results", "value for money"],
           topics=["gentleness", "effectiveness timeline", "value"]),
    Review(product_id="dk-001", platform=Platform.NYKAA, rating=3, title="Average",
           text="It's okay. Doesn't irritate but also doesn't do much for my stubborn pigmentation. Maybe good for maintenance but not treatment.",
           verified_purchase=True, helpful_votes=12, sentiment=SentimentLabel.NEUTRAL, sentiment_score=0.1,
           key_phrases=["doesn't irritate", "not effective for stubborn marks"],
           topics=["gentleness", "limited effectiveness"]),
    Review(product_id="dk-001", platform=Platform.AMAZON, rating=2, title="Dried out my skin",
           text="Used for a week and my skin felt tight and dry after washing. Maybe not for dry skin types. Returning.",
           verified_purchase=True, helpful_votes=8, sentiment=SentimentLabel.NEGATIVE, sentiment_score=-0.6,
           key_phrases=["dried out", "tight skin", "not for dry skin"],
           topics=["drying", "skin type mismatch"]),

    # Dot & Key Watermelon Sunscreen reviews
    Review(product_id="dk-002", platform=Platform.AMAZON, rating=5, title="Holy grail sunscreen!",
           text="Finally a sunscreen that doesn't leave white cast on my brown skin! Feels like a moisturizer, sits perfectly under makeup. Watermelon scent is subtle and nice.",
           verified_purchase=True, helpful_votes=120, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.92,
           key_phrases=["no white cast", "brown skin", "makeup friendly", "moisturizing"],
           topics=["white cast", "makeup compatibility", "texture", "fragrance"]),
    Review(product_id="dk-002", platform=Platform.FLIPKART, rating=5, title="Best sunscreen for oily skin",
           text="I have very oily skin and most sunscreens make me greasy. This one is truly lightweight and matte finish. No breakouts either!",
           verified_purchase=True, helpful_votes=89, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.88,
           key_phrases=["oily skin", "matte finish", "no breakouts", "lightweight"],
           topics=["oily skin suitability", "finish", "acne-safe", "texture"]),
    Review(product_id="dk-002", platform=Platform.NYKAA, rating=4, title="Good but pills under foundation",
           text="Great protection and hydration but pills a bit under my full coverage foundation. Works fine with tinted moisturizer though.",
           verified_purchase=True, helpful_votes=34, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.55,
           key_phrases=["pills under foundation", "works with tinted moisturizer"],
           topics=["makeup compatibility", "pilling"]),
    Review(product_id="dk-002", platform=Platform.AMAZON, rating=3, title="Stings my eyes",
           text="Good sunscreen but when I sweat it runs into my eyes and stings badly. Have to be careful during workouts.",
           verified_purchase=True, helpful_votes=15, sentiment=SentimentLabel.NEUTRAL, sentiment_score=-0.2,
           key_phrases=["stings eyes", "sweat", "workout"],
           topics=["eye irritation", "sweat resistance"]),

    # Competitor reviews (Minimalist Vitamin C Face Wash)
    Review(product_id="comp-minimalist-vitc", platform=Platform.AMAZON, rating=5, title="Better than expensive brands",
           text="Minimalist vitamin C face wash is amazing for the price. My skin feels clean but not stripped. Dark spots fading visibly in 3 weeks.",
           verified_purchase=True, helpful_votes=234, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.88,
           key_phrases=["price", "not stripped", "dark spots fading", "3 weeks"],
           topics=["value", "gentleness", "effectiveness", "timeline"]),
    Review(product_id="comp-minimalist-vitc", platform=Platform.AMAZON, rating=4, title="Good concentration",
           text="10% vitamin C is a good concentration. Fragrance-free which I like. Packaging could be better - pump gets clogged.",
           verified_purchase=True, helpful_votes=67, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.6,
           key_phrases=["10% concentration", "fragrance-free", "pump clogged"],
           topics=["ingredient concentration", "fragrance", "packaging"]),

    # Competitor reviews (Minimalist Sunscreen)
    Review(product_id="comp-minimalist-spf", platform=Platform.AMAZON, rating=5, title="Best budget sunscreen",
           text="Unbeatable at 399 for 50ml. No white cast, matte finish, doesn't break me out. Rebuy #3.",
           verified_purchase=True, helpful_votes=456, sentiment=SentimentLabel.POSITIVE, sentiment_score=0.9,
           key_phrases=["budget", "no white cast", "matte", "no breakouts", "rebought"],
           topics=["value", "white cast", "finish", "acne-safe", "loyalty"]),
]

BRAND_GUIDELINES = BrandGuidelines()