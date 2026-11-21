"""
Competitor Monitoring Module
Monitors competitor products across e-commerce platforms and market intel
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..models import (
    CompetitorProduct, Platform, Product, CompetitorComparison
)
from ..data.loader import (
    SAMPLE_COMPETITOR_PRODUCTS,
    SAMPLE_COMPETITOR_BRANDS,
    SAMPLE_DOTKEY_PRODUCTS,
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
        """Find top competitors for a Dot & Key product based on category matching & ranking"""
        if self.use_sample_data:
            return self._get_sample_competitors(dotkey_product, max_competitors)

        return self._get_sample_competitors(dotkey_product, max_competitors)

    def _get_sample_competitors(
        self,
        dotkey_product: Product,
        max_competitors: int
    ) -> CompetitorSearchResult:
        """Filter and rank competitors for a given Dot & Key product"""
        p_cat = (dotkey_product.category or "").lower()
        p_name = (dotkey_product.name or "").lower()

        # Categorize product intent
        is_sunscreen = "sun" in p_cat or "sun" in p_name
        is_wash = "wash" in p_cat or "cleans" in p_name or "wash" in p_name
        is_serum = "serum" in p_cat or "serum" in p_name or "drops" in p_name
        is_moist = "moist" in p_cat or "cream" in p_name or "gel" in p_name

        matched: list[CompetitorProduct] = []
        for c in SAMPLE_COMPETITOR_PRODUCTS:
            c_cat = (c.category or "").lower()
            c_name = (c.product_name or "").lower()

            if is_sunscreen and ("sun" in c_cat or "sun" in c_name):
                matched.append(c)
            elif is_wash and ("wash" in c_cat or "cleans" in c_name or "wash" in c_name):
                matched.append(c)
            elif is_serum and ("serum" in c_cat or "serum" in c_name):
                matched.append(c)
            elif is_moist and ("moist" in c_cat or "cream" in c_name or "lotion" in c_name):
                matched.append(c)

        # Fallback to general skincare competitors if category is niche (e.g. combo, lip balm)
        if not matched:
            matched = SAMPLE_COMPETITOR_PRODUCTS[:15]

        # Deduplicate by brand (pick best product per brand)
        seen_brands = set()
        deduped: list[CompetitorProduct] = []
        for comp in matched:
            if comp.brand not in seen_brands:
                seen_brands.add(comp.brand)
                deduped.append(comp)

        # Sort by composite popularity score: rating * (1 + sqrt(review_count) / 100)
        deduped.sort(
            key=lambda c: c.rating * (1 + (c.review_count ** 0.5) / 100),
            reverse=True
        )

        return CompetitorSearchResult(
            dotkey_product_id=dotkey_product.id,
            category=dotkey_product.category,
            subcategory=dotkey_product.subcategory,
            competitors=deduped[:max_competitors]
        )


class CompetitorComparator:
    """Compares Dot & Key products with competitors"""

    @staticmethod
    def compare_products(
        dotkey_product: Product,
        competitors: list[CompetitorProduct]
    ) -> CompetitorComparison:
        """Generate detailed comparison"""
        comparison = CompetitorComparison(
            dotkey_product_id=dotkey_product.id,
            competitor_products=competitors
        )

        # Price per ml comparison
        dk_size = dotkey_product.size_ml if dotkey_product.size_ml > 0 else 50.0
        dk_price_per_ml = dotkey_product.price_inr / dk_size if dk_size > 0 else 0.0
        comparison.price_comparison["Dot & Key"] = round(dk_price_per_ml, 2)

        for comp in competitors:
            comp_size = comp.size_ml if comp.size_ml > 0 else 50.0
            comp_price_per_ml = comp.price_inr / comp_size if comp_size > 0 else 0.0
            comparison.price_comparison[comp.brand] = round(comp_price_per_ml, 2)
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
        comparison: CompetitorComparison
    ) -> list[str]:
        """Identify Dot & Key's competitive advantages"""
        advantages = []
        dk_price_per_ml = comparison.price_comparison.get("Dot & Key", 0.0)

        cheaper_count = sum(1 for v in comparison.price_comparison.values() if v > dk_price_per_ml and v > 0)
        if cheaper_count >= len(competitors) * 0.4 and len(competitors) > 0:
            advantages.append(f"Competitive unit economics: lower cost per ml than {cheaper_count}/{len(competitors)} direct alternatives")

        dk_unique = set(i.lower() for i in dotkey_product.ingredients)
        for comp in competitors:
            comp_ingredients = set(i.lower() for i in comp.ingredients)
            dk_unique -= comp_ingredients

        if dk_unique:
            advantages.append(f"Hero fruit-active blend: {', '.join(list(dk_unique)[:3]).title()}")

        if dotkey_product.key_benefits:
            advantages.append(f"Targeted benefit positioning: {', '.join(dotkey_product.key_benefits[:2])}")

        return advantages

    @staticmethod
    def _find_gaps(
        dotkey_product: Product,
        competitors: list[CompetitorProduct],
        comparison: CompetitorComparison
    ) -> list[str]:
        """Identify gaps where competitors are stronger"""
        gaps = []
        dk_price_per_ml = comparison.price_comparison.get("Dot & Key", 0.0)

        cheaper_competitors = [
            (brand, price) for brand, price in comparison.price_comparison.items()
            if brand != "Dot & Key" and price < dk_price_per_ml and price > 0
        ]
        if cheaper_competitors:
            best_price = min(cheaper_competitors, key=lambda x: x[1])
            gaps.append(f"Price premium vs. {best_price[0]} (Rs.{best_price[1]:.1f}/ml vs. Rs.{dk_price_per_ml:.1f}/ml)")

        all_claims = set()
        for comp in competitors:
            all_claims.update(comp.key_claims)

        dk_claims = set(dotkey_product.key_benefits)
        missing_claims = all_claims - dk_claims
        if missing_claims:
            gaps.append(f"Competitor claims to match: {', '.join(list(missing_claims)[:2])}")

        return gaps


async def main():
    monitor = CompetitorMonitor(use_sample_data=True)
    comparator = CompetitorComparator()

    product = SAMPLE_DOTKEY_PRODUCTS[0]
    result = await monitor.find_competitors(product)

    print(f"Competitors for {product.name}:")
    for c in result.competitors:
        print(f"  - {c.brand} ({c.product_name}): Rs.{c.price_inr}, Rating: {c.rating}")

    comp = comparator.compare_products(product, result.competitors)
    print(f"Price per ml: {comp.price_comparison}")
    print(f"Advantages: {comp.competitive_advantages}")


if __name__ == "__main__":
    asyncio.run(main())
