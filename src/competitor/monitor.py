"""
Competitor Monitoring Module
Monitors competitor products across e-commerce platforms
"""

import asyncio
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    CompetitorProduct, Platform, SAMPLE_COMPETITOR_PRODUCTS,
    SAMPLE_COMPETITOR_BRANDS, Product
)


@dataclass
class CompetitorSearchResult:
    """Result of competitor search"""
    dotkey_product_id: str
    category: str
    subcategory: str
    competitors: list[CompetitorProduct]
    search_timestamp: datetime = None

    def __post_init__(self):
        if self.search_timestamp is None:
            self.search_timestamp = datetime.now()


class CompetitorMonitor:
    """Monitors competitor products across platforms"""

    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data
        self.platforms = [
            Platform.AMAZON,
            Platform.FLIPKART,
            Platform.NYKAA,
            Platform.PURPLLE,
            Platform.MYNTRA,
        ]

    async def find_competitors(
        self,
        dotkey_product: Product,
        max_competitors: int = 5
    ) -> CompetitorSearchResult:
        """Find top competitors for a Dot & Key product"""

        if self.use_sample_data:
            return self._get_sample_competitors(dotkey_product, max_competitors)

        # Real implementation would:
        # 1. Search each platform for category/subcategory keywords
        # 2. Filter by similar price range, ingredients, claims
        # 3. Rank by rating * review_count (popularity + quality)
        # 4. Return top N
        competitors = []
        for platform in self.platforms:
            platform_competitors = await self._search_platform(
                platform, dotkey_product.category, dotkey_product.subcategory
            )
            competitors.extend(platform_competitors)

        # Sort by composite score (rating * log(review_count))
        competitors.sort(
            key=lambda c: c.rating * (1 + (c.review_count ** 0.5) / 100),
            reverse=True
        )

        return CompetitorSearchResult(
            dotkey_product_id=dotkey_product.id,
            category=dotkey_product.category,
            subcategory=dotkey_product.subcategory,
            competitors=competitors[:max_competitors]
        )

    def _get_sample_competitors(
        self,
        dotkey_product: Product,
        max_competitors: int
    ) -> CompetitorSearchResult:
        """Get sample competitors for demo"""
        # Filter sample competitors by category/subcategory
        relevant = [
            c for c in SAMPLE_COMPETITOR_PRODUCTS
            if c.category.lower() == dotkey_product.category.lower()
            and c.subcategory.lower() == dotkey_product.subcategory.lower()
        ]

        # Sort by rating * review_count
        relevant.sort(
            key=lambda c: c.rating * (1 + (c.review_count ** 0.5) / 100),
            reverse=True
        )

        return CompetitorSearchResult(
            dotkey_product_id=dotkey_product.id,
            category=dotkey_product.category,
            subcategory=dotkey_product.subcategory,
            competitors=relevant[:max_competitors]
        )

    async def _search_platform(
        self,
        platform: Platform,
        category: str,
        subcategory: str
    ) -> list[CompetitorProduct]:
        """Search a specific platform for competitors (placeholder)"""
        # In production, this would use platform APIs or web scraping
        # For now, return empty list
        return []

    async def monitor_price_changes(
        self,
        competitors: list[CompetitorProduct],
        interval_hours: int = 24
    ) -> dict[str, list[dict]]:
        """Monitor price changes for competitor products over time"""
        # Placeholder for price tracking implementation
        # Would store historical prices and detect changes
        return {}

    async def detect_new_launches(
        self,
        category: str,
        known_competitor_ids: set[str]
    ) -> list[CompetitorProduct]:
        """Detect newly launched competitor products"""
        # Placeholder - would compare current listings with known products
        return []


class CompetitorComparator:
    """Compares Dot & Key products with competitors"""

    @staticmethod
    def compare_products(
        dotkey_product: Product,
        competitors: list[CompetitorProduct]
    ) -> dict:
        """Generate detailed comparison"""
        from models import CompetitorComparison

        comparison = CompetitorComparison(
            dotkey_product_id=dotkey_product.id,
            competitor_products=competitors
        )

        # Price per ml comparison
        dk_price_per_ml = dotkey_product.price_inr / dotkey_product.size_ml if dotkey_product.size_ml > 0 else 0
        comparison.price_comparison["Dot & Key"] = dk_price_per_ml

        for comp in competitors:
            comp_price_per_ml = comp.price_inr / comp.size_ml if comp.size_ml > 0 else 0
            comparison.price_comparison[comp.brand] = comp_price_per_ml
            comparison.rating_comparison[comp.brand] = comp.rating

        # Ingredient analysis
        dk_ingredients = set(i.lower() for i in dotkey_product.ingredients)
        for comp in competitors:
            comp_ingredients = set(i.lower() for i in comp.ingredients)
            overlap = dk_ingredients & comp_ingredients
            unique = comp_ingredients - dk_ingredients

            if overlap:
                comparison.ingredient_overlap[comp.brand] = list(overlap)
            if unique:
                comparison.unique_competitor_ingredients[comp.brand] = list(unique)

        # Identify advantages and gaps
        comparison.competitive_advantages = CompetitorComparator._find_advantages(
            dotkey_product, competitors, comparison
        )
        comparison.competitive_gaps = CompetitorComparator._find_gaps(
            dotkey_product, competitors, comparison
        )

        return comparison

    @staticmethod
    def _find_advantages(
        dotkey_product: Product,
        competitors: list[CompetitorProduct],
        comparison: 'CompetitorComparison'
    ) -> list[str]:
        """Identify Dot & Key's competitive advantages"""
        advantages = []

        # Price advantage
        dk_price_per_ml = comparison.price_comparison.get("Dot & Key", 0)
        cheaper_count = sum(1 for v in comparison.price_comparison.values() if v > dk_price_per_ml and v > 0)
        if cheaper_count >= len(competitors) * 0.5:
            advantages.append(f"Competitive pricing - cheaper than {cheaper_count}/{len(competitors)} competitors per ml")

        # Unique ingredients
        dk_unique = set(i.lower() for i in dotkey_product.ingredients)
        for comp in competitors:
            comp_ingredients = set(i.lower() for i in comp.ingredients)
            dk_unique -= comp_ingredients

        if dk_unique:
            advantages.append(f"Unique ingredients: {', '.join(list(dk_unique)[:3])}")

        # Rating advantage (if we had Dot & Key ratings)
        # Would compare ratings here

        # Claims/benefits
        if dotkey_product.key_benefits:
            advantages.append(f"Strong benefit claims: {', '.join(dotkey_product.key_benefits[:3])}")

        return advantages

    @staticmethod
    def _find_gaps(
        dotkey_product: Product,
        competitors: list[CompetitorProduct],
        comparison: 'CompetitorComparison'
    ) -> list[str]:
        """Identify gaps where competitors are stronger"""
        gaps = []

        # Price gap
        dk_price_per_ml = comparison.price_comparison.get("Dot & Key", 0)
        cheaper_competitors = [
            (brand, price) for brand, price in comparison.price_comparison.items()
            if brand != "Dot & Key" and price < dk_price_per_ml and price > 0
        ]
        if cheaper_competitors:
            best_price = min(cheaper_competitors, key=lambda x: x[1])
            gaps.append(f"Priced higher than {best_price[0]} (₹{best_price[1]:.2f}/ml vs ₹{dk_price_per_ml:.2f}/ml)")

        # Ingredient gaps
        all_comp_ingredients = set()
        for comp in competitors:
            all_comp_ingredients.update(i.lower() for i in comp.ingredients)

        dk_ingredients = set(i.lower() for i in dotkey_product.ingredients)
        missing_popular = all_comp_ingredients - dk_ingredients

        # Filter for ingredients that appear in multiple competitor products
        ingredient_frequency = {}
        for comp in competitors:
            for ing in comp.ingredients:
                ingredient_frequency[ing.lower()] = ingredient_frequency.get(ing.lower(), 0) + 1

        popular_missing = [
            ing for ing, freq in ingredient_frequency.items()
            if freq >= 2 and ing in missing_popular
        ][:3]

        if popular_missing:
            gaps.append(f"Missing popular ingredients: {', '.join(popular_missing)}")

        # Rating gaps
        avg_comp_rating = sum(c.rating for c in competitors) / len(competitors) if competitors else 0
        # Would need Dot & Key rating to compare

        # Claim gaps
        all_claims = set()
        for comp in competitors:
            all_claims.update(comp.key_claims)

        dk_claims = set(dotkey_product.key_benefits)
        missing_claims = all_claims - dk_claims
        if missing_claims:
            gaps.append(f"Competitors highlight: {', '.join(list(missing_claims)[:3])}")

        return gaps


async def main():
    from models import SAMPLE_DOTKEY_PRODUCTS

    monitor = CompetitorMonitor(use_sample_data=True)
    comparator = CompetitorComparator()

    # Test with Vitamin C Face Wash
    product = SAMPLE_DOTKEY_PRODUCTS[0]
    result = await monitor.find_competitors(product)

    print(f"Competitors for {product.name}:")
    for c in result.competitors:
        print(f"  - {c.brand} {c.product_name}: ₹{c.price_inr}/{c.size_ml}ml, Rating: {c.rating} ({c.review_count} reviews)")

    print("\nComparison:")
    comparison = comparator.compare_products(product, result.competitors)
    print(f"  Price per ml: {comparison.price_comparison}")
    print(f"  Advantages: {comparison.competitive_advantages}")
    print(f"  Gaps: {comparison.competitive_gaps}")


if __name__ == "__main__":
    asyncio.run(main())