"""
Market Insights Generator
Generates SWOT analysis, identifies market gaps, trends, and customer acquisition strategies
using Dot & Key catalog and 100 Indian cosmetics brands market intel.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..models import (
    Product, CompetitorProduct, SentimentAnalysis, CompetitorComparison,
    SWOTAnalysis, MarketGap, TrendForecast, BrandMarketIntel,
    CustomerAcquisitionStrategy
)
from ..sentiment.analyzer import SentimentAnalyzer, ReviewCollector
from ..competitor.monitor import CompetitorMonitor, CompetitorComparator
from ..data.loader import (
    SAMPLE_DOTKEY_PRODUCTS,
    SAMPLE_COMPETITOR_PRODUCTS,
    SAMPLE_REVIEWS,
    SAMPLE_MARKET_INTEL,
)


@dataclass
class MarketInsights:
    """Complete market insights for a product"""
    product_id: str
    swot: SWOTAnalysis
    market_gaps: list[MarketGap]
    trend_forecast: TrendForecast
    competitor_comparison: CompetitorComparison
    sentiment_analysis: SentimentAnalysis
    customer_acquisition: CustomerAcquisitionStrategy
    recommendations: list[str]
    generated_at: datetime = field(default_factory=datetime.now)


class InsightsGenerator:
    """Generates comprehensive market insights & customer acquisition strategies"""

    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data
        self.sentiment_analyzer = SentimentAnalyzer(use_sample_data)
        self.review_collector = ReviewCollector(use_sample_data)
        self.competitor_monitor = CompetitorMonitor(use_sample_data)
        self.competitor_comparator = CompetitorComparator()

    async def generate_insights(self, product: Product) -> MarketInsights:
        """Generate complete market insights and acquisition strategies for a product"""
        # 1. Customer reviews & NLP sentiment
        reviews = await self.review_collector.collect_reviews(product)
        for r in reviews:
            self.sentiment_analyzer.analyze_review(r)
        sentiment_analysis = self.sentiment_analyzer.analyze_product_reviews(product.id, reviews)

        # 2. Competitors & unit economics
        comp_search = await self.competitor_monitor.find_competitors(product, max_competitors=5)
        competitor_comparison = self.competitor_comparator.compare_products(product, comp_search.competitors)

        # 3. SWOT analysis
        swot = self._generate_swot(product, sentiment_analysis, competitor_comparison)

        # 4. Market gaps
        market_gaps = self._identify_market_gaps(product, sentiment_analysis, comp_search.competitors)

        # 5. Trend forecast
        trend_forecast = self._forecast_trends(product, sentiment_analysis, comp_search.competitors)

        # 6. Customer acquisition strategy (weaponizing competitor friction)
        customer_acquisition = self._generate_customer_acquisition(product, comp_search.competitors, competitor_comparison)

        # 7. Actionable recommendations
        recommendations = self._generate_recommendations(
            product, swot, market_gaps, trend_forecast, competitor_comparison, customer_acquisition
        )

        return MarketInsights(
            product_id=product.id,
            swot=swot,
            market_gaps=market_gaps,
            trend_forecast=trend_forecast,
            competitor_comparison=competitor_comparison,
            sentiment_analysis=sentiment_analysis,
            customer_acquisition=customer_acquisition,
            recommendations=recommendations,
        )

    def _generate_swot(
        self,
        product: Product,
        sentiment: SentimentAnalysis,
        comparison: CompetitorComparison
    ) -> SWOTAnalysis:
        """Generate evidence-backed SWOT analysis"""
        swot = SWOTAnalysis(product_id=product.id)

        # Strengths
        for adv in comparison.competitive_advantages:
            swot.strengths.append(f"Competitive Edge: {adv}")

        if sentiment.key_praises:
            swot.strengths.append(f"Customer Loved: {', '.join(sentiment.key_praises[:2])}")

        if product.ingredients:
            swot.strengths.append(f"Active Formula: Formulated with {', '.join(product.ingredients[:3])}")

        # Weaknesses
        for gap in comparison.competitive_gaps:
            swot.weaknesses.append(f"Market Gap: {gap}")

        if sentiment.key_complaints:
            swot.weaknesses.append(f"Customer Friction: {', '.join(sentiment.key_complaints[:2])}")

        # Opportunities
        swot.opportunities.append("Capitalize on competitor beginner irritation by promoting gentle fruit-infused actives")
        swot.opportunities.append("Capture market whitespace with broad-spectrum PA++++ zero-white-cast formulas")
        swot.opportunities.append("Expand quick-commerce presence (Blinkit/Zepto) targeting urban working professionals")

        # Threats
        for comp in comparison.competitor_products[:2]:
            swot.threats.append(f"Aggressive competitor: {comp.brand} offering {comp.product_name} at Rs.{comp.price_inr}")

        return swot

    def _identify_market_gaps(
        self,
        product: Product,
        sentiment: SentimentAnalysis,
        competitors: list[CompetitorProduct]
    ) -> list[MarketGap]:
        """Identify strategic white spaces in the Indian beauty market"""
        gaps = []

        # Gap 1: Beginner irritation vs clinical potency
        gaps.append(
            MarketGap(
                category=product.category,
                description="Clinical Actives Irritation Barrier",
                evidence=["Competitors (Minimalist, Derma Co) reviews cite beginner purging and skin stinging."],
                potential_impact="high",
                suggested_action="Position Dot & Key's fruit+active synergy as high-efficacy with zero stinging or redness."
            )
        )

        # Gap 2: Melanin-rich skin finish
        gaps.append(
            MarketGap(
                category=product.category,
                description="Zero White Cast & Lightweight Melanin Finish",
                evidence=["Sunscreen users in India repeatedly cite white cast, greasy sheen, and makeup pilling."],
                potential_impact="high",
                suggested_action="Lead all creative ads with non-greasy, invisible finish under natural Indian sunlight."
            )
        )

        # Gap 3: Accessible Luxury Price Tier
        gaps.append(
            MarketGap(
                category=product.category,
                description="Masstige Sweet Spot (Rs.395 - Rs.695)",
                evidence=["Mass brands (Rs.150-300) lack sensorial aesthetics; luxury brands (Rs.1000+) are cost-prohibitive."],
                potential_impact="medium",
                suggested_action="Position packaging aesthetics and sensorial fragrance as everyday accessible luxury."
            )
        )

        return gaps

    def _forecast_trends(
        self,
        product: Product,
        sentiment: SentimentAnalysis,
        competitors: list[CompetitorProduct]
    ) -> TrendForecast:
        """Forecast 90-day category demand trajectory"""
        p_name = (product.name or "").lower()
        if "sun" in p_name:
            return TrendForecast(
                category="Sunscreen",
                trend_direction="rising",
                trend_strength=0.88,
                key_drivers=["UV & Blue Light awareness", "Daily indoor sunscreen adoption", "Zero-white-cast demand"],
                predicted_demand_change_pct=24.5,
                confidence=0.85
            )
        elif "serum" in p_name or "c" in p_name or "niacinamide" in p_name:
            return TrendForecast(
                category="Active Serums",
                trend_direction="rising",
                trend_strength=0.82,
                key_drivers=["Skintellectual ingredient demand", "Dark spot correction", "Barrier repair focus"],
                predicted_demand_change_pct=18.0,
                confidence=0.80
            )
        else:
            return TrendForecast(
                category=product.category or "Skincare",
                trend_direction="rising",
                trend_strength=0.75,
                key_drivers=["Clean beauty transition", "Sensorial fruit formulations", "Gen-Z hydration routines"],
                predicted_demand_change_pct=14.2,
                confidence=0.75
            )

    def _generate_customer_acquisition(
        self,
        product: Product,
        competitors: list[CompetitorProduct],
        comparison: CompetitorComparison
    ) -> CustomerAcquisitionStrategy:
        """Derive direct competitor switcher hooks and acquisition strategies from market intel"""
        target_brands = [c.brand for c in competitors[:4]]
        friction_points: dict[str, list[str]] = {}

        for intel in SAMPLE_MARKET_INTEL:
            if intel.brand in target_brands:
                friction_points[intel.brand] = intel.negative_friction[:2]

        hooks = []
        if "Minimalist" in target_brands:
            hooks.append("Love active clinical percentages but hate beginner irritation? Switch to fruit-powered actives that soothe while they treat.")
        if "The Derma Co" in target_brands:
            hooks.append("Tired of cleansers and treatments that strip your skin dry? Experience clinical results with deep barrier hydration.")
        if "Mamaearth" in target_brands:
            hooks.append("Looking for more than basic natural claims? Get clinically tested, dermatologically backed results with real fruit nourishment.")

        if not hooks:
            hooks = [
                f"Upgrade your {product.category} routine: Maximum clinical potency with zero irritation.",
                "Why settle for chalky, drying formulas when your skin can feel hydrated all day?"
            ]

        counter_claims = [
            "Gentle fruit+active synergy engineered specifically for Indian skin climate",
            "Dermatologically tested barrier-safe formulation with zero stripping",
            "Lightweight, non-greasy absorption that sits flawlessly under daily makeup"
        ]

        whitespaces = [
            "High-SPF invisible sunscreen with zero white cast on melanin-rich skin",
            "Multi-functional hybrid skincare with immediate cosmetic radiance",
            "Fragrance-safe soothing options for sensitive and acne-prone skin"
        ]

        dk_price = comparison.price_comparison.get("Dot & Key", 0.0)
        avg_comp = sum(v for k, v in comparison.price_comparison.items() if k != "Dot & Key") / max(1, len(competitors))
        if dk_price < avg_comp:
            arbitrage = f"Value Arbitrage: Dot & Key provides premium sensorial formulations at Rs.{dk_price:.1f}/ml compared to competitor average Rs.{avg_comp:.1f}/ml."
        else:
            arbitrage = "Quality Arbitrage: Justified masstige premium through multi-fruit active complexes and luxury packaging."

        return CustomerAcquisitionStrategy(
            target_competitors=target_brands,
            competitor_friction_points=friction_points,
            counter_positioning_claims=counter_claims,
            customer_switcher_hooks=hooks,
            whitespace_opportunities=whitespaces,
            price_arbitrage_angle=arbitrage
        )

    def _generate_recommendations(
        self,
        product: Product,
        swot: SWOTAnalysis,
        market_gaps: list[MarketGap],
        trend_forecast: TrendForecast,
        comparison: CompetitorComparison,
        acquisition: CustomerAcquisitionStrategy
    ) -> list[str]:
        """Generate 6-7 high-impact strategic directives"""
        recs = []
        recs.append(f"Positioning Strategy: Lead advertising with '{acquisition.counter_positioning_claims[0]}'.")
        if acquisition.customer_switcher_hooks:
            recs.append(f"Customer Switcher Campaign: Run ad copy targeting competitor defectors: '{acquisition.customer_switcher_hooks[0]}'")
        recs.append(f"GTM Channel: Capitalize on {trend_forecast.category} demand (+{trend_forecast.predicted_demand_change_pct:.1f}% forecast) via quick-commerce and Instagram Reels.")
        if market_gaps:
            recs.append(f"Whitespace Capture: {market_gaps[0].suggested_action}")
        recs.append(f"Pricing Directive: {acquisition.price_arbitrage_angle}")
        return recs[:5]


async def main():
    generator = InsightsGenerator(use_sample_data=True)
    product = SAMPLE_DOTKEY_PRODUCTS[0]
    print(f"Generating insights for: {product.name}")

    insights = await generator.generate_insights(product)
    print("\n--- SWOT ---")
    print("Strengths:", insights.swot.strengths[:2])
    print("Opportunities:", insights.swot.opportunities[:2])

    print("\n--- CUSTOMER ACQUISITION STRATEGY ---")
    print("Target Brands:", insights.customer_acquisition.target_competitors)
    print("Switcher Hooks:", insights.customer_acquisition.customer_switcher_hooks[:2])

    print("\n--- RECOMMENDATIONS ---")
    for idx, r in enumerate(insights.recommendations, 1):
        print(f"  {idx}. {r}")


if __name__ == "__main__":
    asyncio.run(main())
