import pytest
from src.data.loader import load_dotkey_products, load_competitor_products, load_reviews
from src.sentiment.analyzer import SentimentAnalyzer
from src.competitor.monitor import CompetitorMonitor
from src.insights.generator import InsightsGenerator


def test_catalog_loader():
    products = load_dotkey_products()
    assert len(products) > 0
    p = products[0]
    assert p.id
    assert p.name
    assert p.price_inr > 0


def test_competitor_monitor():
    products = load_dotkey_products()
    monitor = CompetitorMonitor(use_sample_data=True)
    res = monitor._get_sample_competitors(products[0], max_competitors=5)
    assert len(res.competitors) <= 5
    assert len(res.competitors) > 0


def test_sentiment_analyzer():
    analyzer = SentimentAnalyzer(use_sample_data=True)
    reviews = load_reviews()
    assert len(reviews) > 0
    analyzed = analyzer.analyze_review(reviews[0])
    assert analyzed.sentiment_score is not None


@pytest.mark.asyncio
async def test_insights_generator():
    generator = InsightsGenerator(use_sample_data=True)
    products = load_dotkey_products()
    insights = await generator.generate_insights(products[0])
    assert insights.product_id == products[0].id
    assert len(insights.swot.strengths) > 0
    assert len(insights.customer_acquisition.customer_switcher_hooks) > 0
