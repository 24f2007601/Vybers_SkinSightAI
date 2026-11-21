"""
Sentiment Analysis Module for Customer Reviews
Analyzes reviews to extract sentiment, topics, complaints, and praises
"""

import asyncio
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    Review, SentimentAnalysis, SentimentLabel, Product, CompetitorProduct,
    SAMPLE_REVIEWS
)


# Initialize VADER analyzer
vader_analyzer = SentimentIntensityAnalyzer()


# Topic keywords for skincare reviews
TOPIC_KEYWORDS = {
    "texture": ["texture", "consistency", "thick", "thin", "runny", "gel", "cream", "lotion", "lightweight", "heavy", "sticky", "tacky", "greasy", "oily", "matte", "silky", "smooth"],
    "fragrance": ["smell", "scent", "fragrance", "aroma", "perfume", "scented", "unscented", "fragrance-free", "smells"],
    "effectiveness": ["work", "works", "effective", "results", "improve", "improved", "difference", "noticeable", "visible", "fade", "faded", "reduce", "reduced", "clear", "cleared"],
    "gentleness": ["gentle", "harsh", "irritat", "sting", "burn", "red", "sensitive", "soothe", "calm", "mild"],
    "hydration": ["hydrat", "moistur", "dry", "dehydrat", "plump", "supple", "moisture"],
    "oil_control": ["oil", "greasy", "shine", "mattify", "mattifying", "sebum", "pore", "clog"],
    "brightening": ["bright", "glow", "radiant", "dull", "dark spot", "pigment", "even tone", "complexion"],
    "anti_aging": ["wrinkle", "fine line", "aging", "age", "firm", "elastic", "lift", "youth"],
    "acne": ["acne", "pimple", "breakout", "blemish", "zit", "comedone"],
    "white_cast": ["white cast", "whitecast", "ghost", "ashy", "cast", "tint"],
    "makeup_compatibility": ["makeup", "foundation", "pill", "pilling", "primer", "base"],
    "packaging": ["packaging", "bottle", "pump", "dropper", "tube", "jar", "dispenser", "leak", "clog"],
    "value": ["price", "worth", "value", "expensive", "cheap", "affordable", "budget", "cost"],
    "shipping": ["delivery", "shipping", "packed", "damaged", "broken", "late", "fast"],
    "eye_irritation": ["eye", "sting", "burn", "tear", "watery"],
    "sweat_resistance": ["sweat", "workout", "exercise", "gym", "run", "water resistant"],
}


class SentimentAnalyzer:
    """Analyzes sentiment and topics in customer reviews"""

    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data

    def analyze_review(self, review: Review) -> Review:
        """Analyze a single review for sentiment and topics"""
        text = f"{review.title} {review.text}".lower()

        # VADER sentiment
        vader_scores = vader_analyzer.polarity_scores(text)
        compound = vader_scores['compound']

        # TextBlob sentiment
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        # Combine scores (weighted average)
        combined_score = (compound + polarity) / 2

        # Assign sentiment label
        if combined_score >= 0.1:
            review.sentiment = SentimentLabel.POSITIVE
        elif combined_score <= -0.1:
            review.sentiment = SentimentLabel.NEGATIVE
        else:
            review.sentiment = SentimentLabel.NEUTRAL

        review.sentiment_score = combined_score

        # Extract topics
        review.topics = self._extract_topics(text)

        # Extract key phrases (simple n-gram extraction)
        review.key_phrases = self._extract_key_phrases(text)

        return review

    def _extract_topics(self, text: str) -> list[str]:
        """Extract topics mentioned in review"""
        topics = []
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        return topics

    def _extract_key_phrases(self, text: str, max_phrases: int = 5) -> list[str]:
        """Extract key phrases from review text"""
        # Simple approach: find adjective-noun pairs and important phrases
        phrases = []

        # Look for specific patterns
        patterns = [
            r'(?:really|very|super|extremely|quite)\s+(\w+\s+\w+)',  # "really good texture"
            r'(?:love|hate|like|dislike)\s+(?:the|my|this|that)?\s*(\w+\s+\w+)',  # "love the texture"
            r'(?:best|worst|great|amazing|terrible|awful)\s+(\w+\s+\w+)',  # "best sunscreen"
            r'(\w+\s+\w+)\s+(?:is|was)\s+(?:great|good|amazing|terrible|bad|okay)',  # "texture is great"
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            phrases.extend(matches)

        # Clean and deduplicate
        cleaned = []
        seen = set()
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if len(phrase) > 3 and phrase not in seen:
                seen.add(phrase)
                cleaned.append(phrase)

        return cleaned[:max_phrases]

    def analyze_product_reviews(
        self,
        product_id: str,
        reviews: list[Review]
    ) -> SentimentAnalysis:
        """Aggregate sentiment analysis for a product"""
        if not reviews:
            return SentimentAnalysis(product_id=product_id)

        # Filter reviews for this product
        product_reviews = [r for r in reviews if r.product_id == product_id]

        if not product_reviews:
            return SentimentAnalysis(product_id=product_id)

        analysis = SentimentAnalysis(
            product_id=product_id,
            total_reviews=len(product_reviews)
        )

        # Average rating
        analysis.average_rating = sum(r.rating for r in product_reviews) / len(product_reviews)

        # Sentiment distribution
        sentiment_counts = Counter(r.sentiment for r in product_reviews if r.sentiment)
        analysis.sentiment_distribution = dict(sentiment_counts)

        # Overall sentiment score
        scores = [r.sentiment_score for r in product_reviews if r.sentiment_score != 0]
        analysis.overall_sentiment_score = sum(scores) / len(scores) if scores else 0

        # Topic analysis
        all_topics = []
        positive_topics = []
        negative_topics = []

        for review in product_reviews:
            all_topics.extend(review.topics)
            if review.sentiment == SentimentLabel.POSITIVE:
                positive_topics.extend(review.topics)
            elif review.sentiment == SentimentLabel.NEGATIVE:
                negative_topics.extend(review.topics)

        # Top positive topics
        pos_counter = Counter(positive_topics)
        analysis.top_positive_topics = pos_counter.most_common(5)

        # Top negative topics
        neg_counter = Counter(negative_topics)
        analysis.top_negative_topics = neg_counter.most_common(5)

        # Extract key complaints and praises from review text
        analysis.key_complaints = self._extract_complaints(product_reviews)
        analysis.key_praises = self._extract_praises(product_reviews)

        return analysis

    def _extract_complaints(self, reviews: list[Review]) -> list[str]:
        """Extract common complaints from negative/neutral reviews"""
        complaints = []
        negative_reviews = [r for r in reviews if r.sentiment in [SentimentLabel.NEGATIVE, SentimentLabel.NEUTRAL] and r.sentiment_score < 0.3]

        # Collect key phrases from negative reviews
        all_phrases = []
        for review in negative_reviews:
            all_phrases.extend(review.key_phrases)

        # Count and return top complaints
        phrase_counts = Counter(all_phrases)
        return [phrase for phrase, count in phrase_counts.most_common(5)]

    def _extract_praises(self, reviews: list[Review]) -> list[str]:
        """Extract common praises from positive reviews"""
        praises = []
        positive_reviews = [r for r in reviews if r.sentiment == SentimentLabel.POSITIVE]

        all_phrases = []
        for review in positive_reviews:
            all_phrases.extend(review.key_phrases)

        phrase_counts = Counter(all_phrases)
        return [phrase for phrase, count in phrase_counts.most_common(5)]


class ReviewCollector:
    """Collects reviews from various platforms (placeholder for real implementation)"""

    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data

    async def collect_reviews(
        self,
        product: Product | CompetitorProduct,
        platforms: list[str] = None,
        max_reviews_per_platform: int = 100
    ) -> list[Review]:
        """Collect reviews for a product from multiple platforms"""
        if self.use_sample_data:
            return self._get_sample_reviews(product)

        # Real implementation would scrape or use APIs
        return []

    def _get_sample_reviews(self, product: Product | CompetitorProduct) -> list[Review]:
        """Get sample reviews for demo"""
        product_id = product.id if hasattr(product, 'id') else str(product)
        return [r for r in SAMPLE_REVIEWS if r.product_id == product_id]


async def main():
    from models import SAMPLE_DOTKEY_PRODUCTS, SAMPLE_COMPETITOR_PRODUCTS

    analyzer = SentimentAnalyzer(use_sample_data=True)
    collector = ReviewCollector(use_sample_data=True)

    # Test with Dot & Key Vitamin C Face Wash
    product = SAMPLE_DOTKEY_PRODUCTS[0]
    reviews = await collector.collect_reviews(product)

    print(f"Analyzing {len(reviews)} reviews for {product.name}")

    # Analyze each review
    for review in reviews:
        analyzer.analyze_review(review)
        print(f"  Rating: {review.rating}/5 | Sentiment: {review.sentiment.value} ({review.sentiment_score:.2f}) | Topics: {review.topics}")

    # Aggregate analysis
    analysis = analyzer.analyze_product_reviews(product.id, reviews)

    print(f"\nAggregate Analysis:")
    print(f"  Total Reviews: {analysis.total_reviews}")
    print(f"  Average Rating: {analysis.average_rating:.1f}/5")
    print(f"  Overall Sentiment: {analysis.overall_sentiment_score:.2f}")
    print(f"  Sentiment Distribution: {analysis.sentiment_distribution}")
    print(f"  Top Positive Topics: {analysis.top_positive_topics}")
    print(f"  Top Negative Topics: {analysis.top_negative_topics}")
    print(f"  Key Complaints: {analysis.key_complaints}")
    print(f"  Key Praises: {analysis.key_praises}")


if __name__ == "__main__":
    asyncio.run(main())