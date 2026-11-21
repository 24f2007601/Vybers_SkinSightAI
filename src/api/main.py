"""
Main API / Orchestrator for Dot & Key Market Intelligence System
Ties together all modules and provides a unified interface
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models import Product, MarketingContent, ContentType, BRAND_GUIDELINES
from ..insights.generator import MarketInsights
from ..catalog.extractor import DotKeyCatalogExtractor
from ..competitor.monitor import CompetitorMonitor
from ..sentiment.analyzer import SentimentAnalyzer, ReviewCollector
from ..insights.generator import InsightsGenerator, MarketInsights
from ..content.generator import ContentGenerator, CONTENT_TEMPLATES


class DotKeyMarketIntelligence:
    """Main orchestrator for the complete pipeline"""

    def __init__(self, use_sample_data: bool = True, output_dir: str = "output"):
        self.use_sample_data = use_sample_data
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize modules
        self.catalog_extractor = DotKeyCatalogExtractor(use_sample_data)
        self.competitor_monitor = CompetitorMonitor(use_sample_data)
        self.sentiment_analyzer = SentimentAnalyzer(use_sample_data)
        self.review_collector = ReviewCollector(use_sample_data)
        self.insights_generator = InsightsGenerator(use_sample_data)
        self.content_generator = ContentGenerator(brand_guidelines=BRAND_GUIDELINES)

    async def run_full_pipeline(self, product_id: str = None) -> dict:
        """Run the complete market intelligence pipeline"""

        # 1. Extract product catalog
        print("[BOX] Step 1: Extracting product catalog...")
        products = await self.catalog_extractor.extract_all_products()

        if product_id:
            products = [p for p in products if p.id == product_id]
            if not products:
                raise ValueError(f"Product {product_id} not found")

        results = {
            "pipeline_run_at": datetime.now().isoformat(),
            "products_analyzed": len(products),
            "products": []
        }

        # 2. Process each product
        for product in products:
            print(f"\n[SEARCH] Analyzing: {product.name}")

            product_result = await self.analyze_product(product)
            results["products"].append(product_result)

            # Save individual product results
            self._save_product_results(product, product_result)

        # 3. Generate summary report
        self._generate_summary_report(results)

        return results

    async def analyze_product(self, product: Product) -> dict:
        """Run complete analysis for a single product"""

        # Generate insights
        insights = await self.insights_generator.generate_insights(product)

        # Generate marketing content for all types
        content_pieces = {}
        for content_type in ContentType:
            for platform in CONTENT_TEMPLATES.get(content_type, {}).keys():
                try:
                    content = self.content_generator.generate_content(
                        product, insights, content_type, platform
                    )
                    key = f"{content_type.value}_{platform}"
                    content_pieces[key] = content
                except Exception as e:
                    print(f"  [WARN] Failed to generate {content_type.value} for {platform}: {e}")

        return {
            "product": {
                "id": product.id,
                "name": product.name,
                "category": product.category,
                "subcategory": product.subcategory,
                "price_inr": product.price_inr,
            },
            "insights": {
                "swot": {
                    "strengths": insights.swot.strengths,
                    "weaknesses": insights.swot.weaknesses,
                    "opportunities": insights.swot.opportunities,
                    "threats": insights.swot.threats,
                },
                "market_gaps": [
                    {
                        "description": gap.description,
                        "impact": gap.potential_impact,
                        "action": gap.suggested_action
                    }
                    for gap in insights.market_gaps
                ],
                "trend_forecast": {
                    "direction": insights.trend_forecast.trend_direction,
                    "strength": insights.trend_forecast.trend_strength,
                    "demand_change_pct": insights.trend_forecast.predicted_demand_change_pct,
                    "key_drivers": insights.trend_forecast.key_drivers,
                },
                "sentiment": {
                    "total_reviews": insights.sentiment_analysis.total_reviews,
                    "avg_rating": insights.sentiment_analysis.average_rating,
                    "overall_score": insights.sentiment_analysis.overall_sentiment_score,
                    "top_positive": insights.sentiment_analysis.top_positive_topics,
                    "top_negative": insights.sentiment_analysis.top_negative_topics,
                    "complaints": insights.sentiment_analysis.key_complaints,
                    "praises": insights.sentiment_analysis.key_praises,
                },
                "competitor_comparison": {
                    "price_comparison": insights.competitor_comparison.price_comparison,
                    "rating_comparison": insights.competitor_comparison.rating_comparison,
                    "advantages": insights.competitor_comparison.competitive_advantages,
                    "gaps": insights.competitor_comparison.competitive_gaps,
                },
                "recommendations": insights.recommendations,
            },
            "marketing_content": {
                key: {
                    "type": content.content_type.value,
                    "platform": content.platform,
                    "title": content.title,
                    "content": content.content,
                    "format_specs": content.format_specs,
                    "key_message": content.key_message,
                    "cta": content.cta,
                }
                for key, content in content_pieces.items()
            }
        }

    def _save_product_results(self, product: Product, result: dict):
        """Save results for a product to JSON"""
        filename = f"{product.id}_{product.name.lower().replace(' ', '_')}.json"
        filepath = self.output_dir / filename

        # Convert non-serializable objects
        serializable = self._make_serializable(result)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)

        print(f"  [SAVE] Saved: {filepath}")

    def _generate_summary_report(self, results: dict):
        """Generate a human-readable summary report"""
        report_path = self.output_dir / "SUMMARY_REPORT.md"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Dot & Key Market Intelligence - Summary Report\n\n")
            f.write(f"**Generated:** {results['pipeline_run_at']}\n")
            f.write(f"**Products Analyzed:** {results['products_analyzed']}\n\n")

            for product_result in results["products"]:
                p = product_result["product"]
                i = product_result["insights"]

                f.write(f"## {p['name']} ({p['category']} - {p['subcategory']})\n\n")
                f.write(f"**Price:** ₹{p['price_inr']}\n\n")

                # SWOT
                f.write("### SWOT Analysis\n")
                f.write("**Strengths:**\n")
                for s in i["swot"]["strengths"]:
                    f.write(f"- {s}\n")
                f.write("\n**Weaknesses:**\n")
                for w in i["swot"]["weaknesses"]:
                    f.write(f"- {w}\n")
                f.write("\n**Opportunities:**\n")
                for o in i["swot"]["opportunities"]:
                    f.write(f"- {o}\n")
                f.write("\n**Threats:**\n")
                for t in i["swot"]["threats"]:
                    f.write(f"- {t}\n")
                f.write("\n")

                # Market Gaps
                f.write("### Market Gaps & Opportunities\n")
                for gap in i["market_gaps"]:
                    f.write(f"- **{gap['description']}** (Impact: {gap['impact']})\n")
                    f.write(f"  - Action: {gap['action']}\n")
                f.write("\n")

                # Trend
                f.write("### Trend Forecast\n")
                tf = i["trend_forecast"]
                f.write(f"- **Direction:** {tf['direction'].title()}\n")
                f.write(f"- **Strength:** {tf['strength']:.0%}\n")
                f.write(f"- **Predicted Demand Change:** {tf['demand_change_pct']:+.1f}%\n")
                f.write(f"- **Key Drivers:** {', '.join(tf['key_drivers'])}\n\n")

                # Sentiment
                f.write("### Customer Sentiment\n")
                s = i["sentiment"]
                f.write(f"- **Reviews Analyzed:** {s['total_reviews']}\n")
                f.write(f"- **Average Rating:** {s['avg_rating']:.1f}/5\n")
                f.write(f"- **Overall Sentiment:** {s['overall_score']:.2f}\n")
                f.write(f"- **Top Praises:** {', '.join(s['praises'][:3])}\n")
                f.write(f"- **Top Complaints:** {', '.join(s['complaints'][:3])}\n\n")

                # Recommendations
                f.write("### Recommendations\n")
                for idx, rec in enumerate(i["recommendations"], 1):
                    f.write(f"{idx}. {rec}\n")
                f.write("\n")

                # Content Generated
                f.write("### Marketing Content Generated\n")
                for key, content in product_result["marketing_content"].items():
                    f.write(f"- **{content['type']}** ({content['platform']}): {content['title']}\n")
                f.write("\n---\n\n")

        print(f"\n[REPORT] Summary report saved: {report_path}")

    def _make_serializable(self, obj):
        """Convert objects to JSON-serializable format"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(v) for v in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif hasattr(obj, '__dict__'):
            return self._make_serializable(obj.__dict__)
        else:
            return str(obj)


async def demo():
    """Run demo with sample data"""
    print("[START] Dot & Key Market Intelligence System - Demo")
    print("=" * 50)

    system = DotKeyMarketIntelligence(use_sample_data=True, output_dir="demo_output")

    # Run full pipeline
    results = await system.run_full_pipeline()

    print("\n" + "=" * 50)
    print("[DONE] Pipeline Complete!")
    print(f"[SAVE] Results saved to: demo_output/")
    print(f"[STATS] Analyzed {results['products_analyzed']} products")

    # Print quick summary
    for product_result in results["products"]:
        p = product_result["product"]
        i = product_result["insights"]
        print(f"\n  [PRODUCT] {p['name']}")
        print(f"     Sentiment: {i['sentiment']['overall_score']:.2f} ({i['sentiment']['total_reviews']} reviews)")
        print(f"     Trend: {i['trend_forecast']['direction']} ({i['trend_forecast']['demand_change_pct']:+.1f}%)")
        print(f"     Content pieces: {len(product_result['marketing_content'])}")


if __name__ == "__main__":
    asyncio.run(demo())