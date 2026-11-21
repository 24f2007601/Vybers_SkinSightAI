"""
Market Insights Generator
Generates SWOT analysis, identifies market gaps, trends, and forecasts
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    Product, CompetitorProduct, SentimentAnalysis, CompetitorComparison,
    SWOTAnalysis, MarketGap, TrendForecast, MarketGap, SAMPLE_DOTKEY_PRODUCTS,
    SAMPLE_COMPETITOR_PRODUCTS, SAMPLE_REVIEWS
)
from sentiment.analyzer import SentimentAnalyzer, ReviewCollector
from competitor.monitor import CompetitorMonitor, CompetitorComparator


@dataclass
class MarketInsights:
    """Complete market insights for a product"""
    product_id: str
    swot: SWOTAnalysis
    market_gaps: list[MarketGap]
    trend_forecast: TrendForecast
    competitor_comparison: CompetitorComparison
    sentiment_analysis: SentimentAnalysis
    recommendations: list[str]
    generated_at: datetime = None

    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now()


class InsightsGenerator:
    """Generates comprehensive market insights"""

    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data
        self.sentiment_analyzer = SentimentAnalyzer(use_sample_data)
        self.review_collector = ReviewCollector(use_sample_data)
        self.competitor_monitor = CompetitorMonitor(use_sample_data)
        self.competitor_comparator = CompetitorComparator()

    async def generate_insights(self, product: Product) -> MarketInsights:
        """Generate complete market insights for a product"""

        # 1. Collect and analyze reviews
        reviews = await self.review_collector.collect_reviews(product)
        for review in reviews:
            self.sentiment_analyzer.analyze_review(review)
        sentiment_analysis = self.sentiment_analyzer.analyze_product_reviews(product.id, reviews)

        # 2. Find and compare competitors
        competitor_result = await self.competitor_monitor.find_competitors(product)
        competitor_comparison = self.competitor_comparator.compare_products(
            product, competitor_result.competitors
        )

        # 3. Generate SWOT analysis
        swot = self._generate_swot(product, sentiment_analysis, competitor_comparison)

        # 4. Identify market gaps
        market_gaps = self._identify_market_gaps(
            product, sentiment_analysis, competitor_comparison, competitor_result.competitors
        )

        # 5. Forecast trends
        trend_forecast = self._forecast_trends(
            product, sentiment_analysis, competitor_result.competitors
        )

        # 6. Generate recommendations
        recommendations = self._generate_recommendations(
            product, swot, market_gaps, trend_forecast, competitor_comparison
        )

        return MarketInsights(
            product_id=product.id,
            swot=swot,
            market_gaps=market_gaps,
            trend_forecast=trend_forecast,
            competitor_comparison=competitor_comparison,
            sentiment_analysis=sentiment_analysis,
            recommendations=recommendations
        )

    def _generate_swot(
        self,
        product: Product,
        sentiment: SentimentAnalysis,
        comparison: CompetitorComparison
    ) -> SWOTAnalysis:
        """Generate SWOT analysis"""
        swot = SWOTAnalysis(product_id=product.id)

        # Strengths - from positive sentiment and competitive advantages
        if sentiment.overall_sentiment_score > 0.3:
            swot.strengths.append("Strong positive customer sentiment")

        if sentiment.top_positive_topics:
            for topic, count in sentiment.top_positive_topics[:3]:
                swot.strengths.append(f"Customers love: {topic} ({count} mentions)")

        for advantage in comparison.competitive_advantages:
            swot.strengths.append(f"Competitive advantage: {advantage}")

        # Product-specific strengths
        if product.key_benefits:
            swot.strengths.append(f"Clear benefit positioning: {', '.join(product.key_benefits[:3])}")

        if product.ingredients:
            unique_ingredients = set(i.lower() for i in product.ingredients)
            for comp in comparison.competitor_products:
                comp_ingredients = set(i.lower() for i in comp.ingredients)
                unique_ingredients -= comp_ingredients
            if unique_ingredients:
                swot.strengths.append(f"Unique ingredient blend: {', '.join(list(unique_ingredients)[:3])}")

        # Weaknesses - from negative sentiment and competitive gaps
        if sentiment.overall_sentiment_score < -0.1:
            swot.weaknesses.append("Negative customer sentiment overall")

        for topic, count in sentiment.top_negative_topics[:3]:
            swot.weaknesses.append(f"Customer pain point: {topic} ({count} complaints)")

        for complaint in sentiment.key_complaints[:3]:
            swot.weaknesses.append(f"Common complaint: {complaint}")

        for gap in comparison.competitive_gaps:
            swot.weaknesses.append(f"Competitive gap: {gap}")

        # Opportunities - from market gaps and trends
        # (will be populated from market_gaps analysis)

        # Threats - from competitor actions and market trends
        for comp in comparison.competitor_products:
            if comp.rating > 4.5 and comp.review_count > 10000:
                swot.threats.append(f"Strong competitor: {comp.brand} {comp.product_name} (rating {comp.rating}, {comp.review_count} reviews)")

        # Price pressure
        dk_price_per_ml = comparison.price_comparison.get("Dot & Key", 0)
        cheaper = [(b, p) for b, p in comparison.price_comparison.items() if b != "Dot & Key" and p < dk_price_per_ml]
        if cheaper:
            swot.threats.append(f"Price pressure from {len(cheaper)} cheaper competitors")

        return swot

    def _identify_market_gaps(
        self,
        product: Product,
        sentiment: SentimentAnalysis,
        comparison: CompetitorComparison,
        competitors: list[CompetitorProduct]
    ) -> list[MarketGap]:
        """Identify market gaps and opportunities"""
        gaps = []

        # Gap 1: Unmet customer needs from negative sentiment
        for topic, count in sentiment.top_negative_topics:
            if count >= 2:  # Multiple people complaining
                gap = MarketGap(
                    category=product.category,
                    description=f"Customer dissatisfaction with {topic} in {product.subcategory} products",
                    evidence=[f"{count} negative mentions in reviews", f"Common complaint: {sentiment.key_complaints[0] if sentiment.key_complaints else 'N/A'}"],
                    potential_impact="high" if count >= 3 else "medium",
                    suggested_action=f"Improve {topic} in formulation or communicate better about {topic}"
                )
                gaps.append(gap)

        # Gap 2: Missing popular ingredients
        all_comp_ingredients = {}
        for comp in competitors:
            for ing in comp.ingredients:
                all_comp_ingredients[ing.lower()] = all_comp_ingredients.get(ing.lower(), 0) + 1

        dk_ingredients = set(i.lower() for i in product.ingredients)
        popular_missing = [
            (ing, freq) for ing, freq in all_comp_ingredients.items()
            if freq >= 2 and ing not in dk_ingredients
        ]
        popular_missing.sort(key=lambda x: x[1], reverse=True)

        for ing, freq in popular_missing[:3]:
            gap = MarketGap(
                category=product.category,
                description=f"Missing popular ingredient: {ing} (used by {freq} competitors)",
                evidence=[f"{freq} competitors use {ing}", f"Customer demand for {ing} benefits"],
                potential_impact="medium",
                suggested_action=f"Consider adding {ing} to formulation or launch variant with {ing}"
            )
            gaps.append(gap)

        # Gap 3: Underserved skin types/concerns
        all_skin_types = set()
        all_concerns = set()
        for comp in competitors:
            # Would need skin_type/concerns data for competitors
            pass

        # Gap 4: Price segment gaps
        price_points = sorted([c.price_inr / c.size_ml for c in competitors if c.size_ml > 0])
        if price_points:
            # Check for gaps in price distribution
            for i in range(len(price_points) - 1):
                gap_size = price_points[i+1] - price_points[i]
                if gap_size > price_points[i] * 0.3:  # >30% gap
                    mid_price = (price_points[i] + price_points[i+1]) / 2
                    gap = MarketGap(
                        category=product.category,
                        description=f"Price gap between ₹{price_points[i]:.0f}/ml and ₹{price_points[i+1]:.0f}/ml",
                        evidence=[f"No products in ₹{mid_price:.0f}/ml range"],
                        potential_impact="medium",
                        suggested_action=f"Launch product at ₹{mid_price:.0f}/ml to capture mid-segment"
                    )
                    gaps.append(gap)

        # Gap 5: Emerging trends from competitor launches
        # Would analyze new product launches

        return gaps[:5]  # Top 5 gaps

    def _forecast_trends(
        self,
        product: Product,
        sentiment: SentimentAnalysis,
        competitors: list[CompetitorProduct]
    ) -> TrendForecast:
        """Forecast market trends for product category"""

        # Simple trend analysis based on available data
        forecast = TrendForecast(
            category=product.category,
            trend_direction="stable",
            trend_strength=0.5,
            key_drivers=[],
            forecast_period_days=90,
            predicted_demand_change_pct=0.0,
            confidence=0.6
        )

        # Analyze sentiment trend
        if sentiment.overall_sentiment_score > 0.5:
            forecast.trend_direction = "rising"
            forecast.trend_strength = min(0.8, sentiment.overall_sentiment_score)
            forecast.key_drivers.append("Strong positive customer sentiment")
        elif sentiment.overall_sentiment_score < -0.2:
            forecast.trend_direction = "declining"
            forecast.trend_strength = min(0.8, abs(sentiment.overall_sentiment_score))
            forecast.key_drivers.append("Negative customer sentiment")

        # Analyze competitor activity
        high_rated_competitors = [c for c in competitors if c.rating > 4.3]
        if len(high_rated_competitors) >= 3:
            forecast.key_drivers.append("Highly competitive landscape with strong alternatives")

        # Check for trending ingredients in competitor products
        trending_ingredients = ["niacinamide", "hyaluronic acid", "ceramide", "retinol", "bakuchiol", "peptide"]
        comp_ingredients = set()
        for c in competitors:
            comp_ingredients.update(i.lower() for i in c.ingredients)

        trending_in_market = [ing for ing in trending_ingredients if ing in comp_ingredients]
        if trending_in_market:
            forecast.key_drivers.append(f"Trending ingredients in market: {', '.join(trending_in_market[:3])}")

        # Estimate demand change based on trend
        if forecast.trend_direction == "rising":
            forecast.predicted_demand_change_pct = 10 + (forecast.trend_strength * 20)
        elif forecast.trend_direction == "declining":
            forecast.predicted_demand_change_pct = -10 - (forecast.trend_strength * 15)

        forecast.confidence = 0.5 + (len(forecast.key_drivers) * 0.1)
        forecast.confidence = min(0.9, forecast.confidence)

        return forecast

    def _generate_recommendations(
        self,
        product: Product,
        swot: SWOTAnalysis,
        market_gaps: list[MarketGap],
        trend_forecast: TrendForecast,
        comparison: CompetitorComparison
    ) -> list[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Product improvements
        if swot.weaknesses:
            top_weakness = swot.weaknesses[0]
            recommendations.append(f"Product Improvement: Address '{top_weakness}' through formulation update or customer education")

        # New product opportunities from market gaps
        for gap in market_gaps[:2]:
            if gap.potential_impact in ["high", "medium"]:
                recommendations.append(f"New Product Opportunity: {gap.suggested_action}")

        # Go-to-market strategies
        if trend_forecast.trend_direction == "rising":
            recommendations.append(f"Go-to-Market: Accelerate marketing for {product.category} - trend is rising ({trend_forecast.predicted_demand_change_pct:.0f}% demand increase predicted)")

        # Competitive positioning
        if comparison.competitive_advantages:
            top_advantage = comparison.competitive_advantages[0]
            recommendations.append(f"Positioning: Lead with '{top_advantage}' in all marketing communications")

        # Pricing strategy
        dk_price = comparison.price_comparison.get("Dot & Key", 0)
        avg_comp_price = np.mean([p for b, p in comparison.price_comparison.items() if b != "Dot & Key" and p > 0])
        if dk_price > avg_comp_price * 1.2:
            recommendations.append("Pricing: Consider competitive pricing or justify premium with stronger value communication")
        elif dk_price < avg_comp_price * 0.8:
            recommendations.append("Pricing: Strong price advantage - emphasize value-for-money in marketing")

        # Content strategy based on customer loves
        if swot.strengths:
            customer_loves = [s for s in swot.strengths if "love" in s.lower() or "positive" in s.lower()]
            if customer_loves:
                recommendations.append(f"Content Strategy: Highlight '{customer_loves[0]}' in advertisements and social media")

        return recommendations[:7]  # Top 7 recommendations


async def main():
    generator = InsightsGenerator(use_sample_data=True)

    # Test with Vitamin C Face Wash
    product = SAMPLE_DOTKEY_PRODUCTS[0]
    print(f"Generating insights for: {product.name}")

    insights = await generator.generate_insights(product)

    print(f"\n=== SWOT ANALYSIS ===")
    print(f"Strengths: {insights.swot.strengths}")
    print(f"Weaknesses: {insights.swot.weaknesses}")
    print(f"Opportunities: {insights.swot.opportunities}")
    print(f"Threats: {insights.swot.threats}")

    print(f"\n=== MARKET GAPS ===")
    for gap in insights.market_gaps:
        print(f"  - {gap.description} (Impact: {gap.potential_impact})")
        print(f"    Action: {gap.suggested_action}")

    print(f"\n=== TREND FORECAST ===")
    print(f"  Direction: {insights.trend_forecast.trend_direction}")
    print(f"  Strength: {insights.trend_forecast.trend_strength:.2f}")
    print(f"  Demand Change: {insights.trend_forecast.predicted_demand_change_pct:.1f}%")
    print(f"  Key Drivers: {insights.trend_forecast.key_drivers}")

    print(f"\n=== RECOMMENDATIONS ===")
    for i, rec in enumerate(insights.recommendations, 1):
        print(f"  {i}. {rec}")


if __name__ == "__main__":
    asyncio.run(main())