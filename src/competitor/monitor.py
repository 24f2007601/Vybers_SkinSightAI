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
        return self._get_sample_competitors(dotkey_product, max_competitors)

    def _get_sample_competitors(
        self,
        dotkey_product: Product,
        max_competitors: int
    ) -> CompetitorSearchResult:
        """Filter and rank competitors dynamically for a given Dot & Key product"""
        p_cat = (dotkey_product.category or "").lower()
        p_name = (dotkey_product.name or "").lower()
        p_ingredients = [i.lower() for i in dotkey_product.ingredients]

        # Broad categorizations
        is_sunscreen = any(k in p_cat or k in p_name for k in ["sun", "spf", "uv"])
        is_wash = any(k in p_cat or k in p_name for k in ["wash", "cleans", "scrub", "shower", "bath"])
        is_serum = any(k in p_cat or k in p_name for k in ["serum", "drops", "treatment", "cica", "salicylic"])
        is_moist = any(k in p_cat or k in p_name for k in ["moist", "cream", "gel", "lotion", "hydrat"])
        is_lip = any(k in p_cat or k in p_name for k in ["lip", "balm", "gloss", "tint"])
        is_combo = any(k in p_cat or k in p_name for k in ["combo", "duo", "routine", "pack", "kit"])

        scored: list[tuple[float, CompetitorProduct]] = []
        for c in SAMPLE_COMPETITOR_PRODUCTS:
            c_cat = (c.category or "").lower()
            c_name = (c.product_name or "").lower()
            c_ingredients = [i.lower() for i in c.ingredients]

            score = 0.0

            # Category matching weight
            if is_lip and any(k in c_cat or k in c_name for k in ["lip", "lipstick", "balm"]):
                score += 50.0
            elif is_sunscreen and any(k in c_cat or k in c_name for k in ["sun", "spf"]):
                score += 50.0
            elif is_wash and any(k in c_cat or k in c_name for k in ["wash", "cleanser", "soap", "gel"]):
                score += 50.0
            elif is_serum and ("serum" in c_cat or "serum" in c_name):
                score += 50.0
            elif is_moist and any(k in c_cat or k in c_name for k in ["moist", "cream", "lotion"]):
                score += 50.0
            elif is_combo and any(k in c_cat or k in c_name for k in ["kit", "combo", "set", "pack"]):
                score += 40.0

            # Ingredient overlap weight
            shared_ing = set(p_ingredients) & set(c_ingredients)
            score += len(shared_ing) * 15.0

            # Price proximity (relative similarity in masstige bracket)
            if dotkey_product.price_inr > 0 and c.price_inr > 0:
                price_ratio = min(dotkey_product.price_inr, c.price_inr) / max(dotkey_product.price_inr, c.price_inr)
                score += price_ratio * 10.0

            # Brand/Review relevance
            score += c.rating * 2.0 + (c.review_count ** 0.5) / 20.0

            scored.append((score, c))

        # Sort descending by calculated score
        scored.sort(key=lambda x: x[0], reverse=True)

        # Deduplicate by brand
        seen_brands = set()
        deduped: list[CompetitorProduct] = []
        for _, comp in scored:
            if comp.brand not in seen_brands:
                seen_brands.add(comp.brand)
                deduped.append(comp)
            if len(deduped) >= max_competitors:
                break

        return CompetitorSearchResult(
            dotkey_product_id=dotkey_product.id,
            category=dotkey_product.category,
            subcategory=dotkey_product.subcategory,
            competitors=deduped
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
        product: Product,
        competitors: list[CompetitorProduct],
        comparison: CompetitorComparison
    ) -> list[str]:
        advantages = []
        dk_price = comparison.price_comparison.get("Dot & Key", 0)
        cheaper_count = sum(1 for b, p in comparison.price_comparison.items() if b != "Dot & Key" and dk_price < p)

        if cheaper_count > 0:
            advantages.append(f"Competitive unit economics: lower cost per ml than {cheaper_count}/{len(competitors)} direct alternatives")

        if product.ingredients:
            hero = ", ".join(product.ingredients[:2])
            advantages.append(f"Hero active formulation blend: {hero}")

        if product.key_benefits:
            advantages.append(f"Targeted clinical benefit: {product.key_benefits[0]}")

        advantages.append("Engineered specifically for Indian weather, humidity, and melanin-rich barrier needs")
        return advantages

    @staticmethod
    def _find_gaps(
        product: Product,
        competitors: list[CompetitorProduct],
        comparison: CompetitorComparison
    ) -> list[str]:
        gaps = []
        if competitors:
            top_comp = max(competitors, key=lambda c: c.review_count)
            gaps.append(f"Review Volume Gap: {top_comp.brand} ({top_comp.product_name}) holds high social proof with {top_comp.review_count} ratings")

        if comparison.unique_competitor_ingredients:
            comp_name, ings = next(iter(comparison.unique_competitor_ingredients.items()))
            if ings:
                gaps.append(f"Competitor Formulation Counter: {comp_name} highlights {ings[0]} for differentiated marketing claims")

        gaps.append("White-cast & fragrance-safety reassurance needed in top-of-funnel creative assets")
        return gaps
