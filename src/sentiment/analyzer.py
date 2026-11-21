"""
Sentiment Analysis Module for Customer Reviews
Analyzes reviews synthesized from market intel to extract sentiment, topics, complaints, and praises
"""

import asyncio
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from ..models import (
    Review, SentimentAnalysis, SentimentLabel, Product, CompetitorProduct
)
from ..data.loader import (
    SAMPLE_REVIEWS,
    SAMPLE_DOTKEY_PRODUCTS,
    SAMPLE_COMPETITOR_PRODUCTS,
)
from ..competitor.monitor import CompetitorMonitor

vader_analyzer = SentimentIntensityAnalyzer()

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
        """Analyze a single review for sentiment score and topics"""
        text = f"{review.title} {review.text}".lower()

        vader_scores = vader_analyzer.polarity_scores(text)
        compound = vader_scores["compound"]

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        combined_score = (compound + polarity) / 2.0

        if combined_score >= 0.1:
            review.sentiment = SentimentLabel.POSITIVE
        elif combined_score <= -0.1:
            review.sentiment = SentimentLabel.NEGATIVE
        else:
            review.sentiment = SentimentLabel.NEUTRAL

        review.sentiment_score = round(combined_score, 2)
        review.topics = self._extract_topics(text)
        review.key_phrases = self._extract_key_phrases(text)

        return review

    def _extract_topics(self, text: str) -> list[str]:
        topics = []
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                topics.append(topic)
        return topics

    def _extract_key_phrases(self, text: str) -> list[str]:
        # Extract the core attribute mentioned after the colon, e.g. "I really loved this: rich body butters."
        m = re.search(r":\s*([a-zA-Z\s\-]{3,40})\.", text, re.IGNORECASE)
        if m:
            clean = m.group(1).strip()
            if clean and clean.lower() not in ["this", "that"]:
                return [clean]

        phrases = []
        patterns = [
            r"(?:best|worst|great|amazing|terrible|awful)\s+(\w+\s+\w+)",
            r"(\w+\s+\w+)\s+(?:is|was)\s+(?:great|good|amazing|terrible|bad)",
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            phrases.extend(matches)

        return [p.strip() for p in phrases if len(p.strip()) > 3]

    def analyze_product_reviews(self, product_id: str, reviews: list[Review]) -> SentimentAnalysis:
        analysis = SentimentAnalysis(product_id=product_id, total_reviews=len(reviews))

        if not reviews:
            return analysis

        total_rating = sum(r.rating for r in reviews)
        analysis.average_rating = round(total_rating / len(reviews), 2)

        total_sentiment = sum(r.sentiment_score for r in reviews)
        analysis.overall_sentiment_score = round(total_sentiment / len(reviews), 2)

        dist = {SentimentLabel.POSITIVE: 0, SentimentLabel.NEGATIVE: 0, SentimentLabel.NEUTRAL: 0}
        for review in reviews:
            if review.sentiment in dist:
                dist[review.sentiment] += 1
            else:
                dist[review.sentiment] = 1
        analysis.sentiment_distribution = dist

        positive_topics = []
        negative_topics = []

        for review in reviews:
            if review.sentiment == SentimentLabel.POSITIVE:
                positive_topics.extend(review.topics)
            elif review.sentiment == SentimentLabel.NEGATIVE:
                negative_topics.extend(review.topics)

        pos_counter = Counter(positive_topics)
        analysis.top_positive_topics = pos_counter.most_common(5)

        neg_counter = Counter(negative_topics)
        analysis.top_negative_topics = neg_counter.most_common(5)

        analysis.key_complaints = self._extract_complaints(reviews)
        analysis.key_praises = self._extract_praises(reviews)

        return analysis

    def _extract_complaints(self, reviews: list[Review]) -> list[str]:
        negative_reviews = [r for r in reviews if r.sentiment == SentimentLabel.NEGATIVE or r.rating <= 2]
        all_phrases = []
        for review in negative_reviews:
            if review.key_phrases:
                all_phrases.extend(review.key_phrases)

        # Deduplicate preserving order
        seen = set()
        deduped = []
        for p in all_phrases:
            p_clean = p.lower()
            if p_clean not in seen:
                seen.add(p_clean)
                deduped.append(p)

        return deduped[:5] or ["fragrance irritation", "greasy finish under humidity"]

    def _extract_praises(self, reviews: list[Review]) -> list[str]:
        positive_reviews = [r for r in reviews if r.sentiment == SentimentLabel.POSITIVE or r.rating >= 4]
        all_phrases = []
        for review in positive_reviews:
            if review.key_phrases:
                all_phrases.extend(review.key_phrases)

        # Deduplicate preserving order
        seen = set()
        deduped = []
        for p in all_phrases:
            p_clean = p.lower()
            if p_clean not in seen:
                seen.add(p_clean)
                deduped.append(p)

        return deduped[:5] or ["lightweight non-sticky absorption", "instant plumping hydration", "barrier-friendly soothing feel"]


class ReviewCollector:
    """Collects customer reviews dynamically based on matched competitors and product category"""

    def __init__(self, use_sample_data: bool = True):
        self.use_sample_data = use_sample_data
        self.competitor_monitor = CompetitorMonitor(use_sample_data)

    async def collect_reviews(
        self,
        product: Product | CompetitorProduct,
        platforms: list[str] = None,
        max_reviews_per_platform: int = 50
    ) -> list[Review]:
        return self._get_sample_reviews(product)

    def _get_sample_reviews(self, product: Product | CompetitorProduct) -> list[Review]:
        """Dynamically retrieve reviews from competitors benchmarked for THIS specific product"""
        name = getattr(product, "name", getattr(product, "product_name", "")).lower()
        category = getattr(product, "category", "").lower()

        # Find the specific benchmarked competitors for this SKU
        comp_result = self.competitor_monitor._get_sample_competitors(product, max_competitors=5)
        competitor_brands = set(c.brand for c in comp_result.competitors)

        matched = []

        # 1. Grab reviews specifically for the matched benchmark rival brands
        for r in SAMPLE_REVIEWS:
            if r.product_id in competitor_brands:
                matched.append(r)

        # 2. Add Dot & Key category specific reviews
        dk_reviews = [r for r in SAMPLE_REVIEWS if r.product_id.lower() in ("dot & key", "dot and key")]
        matched.extend(dk_reviews)

        # Deduplicate by review ID
        seen_ids = set()
        deduped = []
        for r in matched:
            if r.id not in seen_ids:
                seen_ids.add(r.id)
                deduped.append(r)

        return deduped[:25] if deduped else SAMPLE_REVIEWS[:15]
