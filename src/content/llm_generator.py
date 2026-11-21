"""
LLM-powered Content Generator using Google AI Studio (Gemini)
Replaces template-based generation with AI for ad scripts & video concepts
"""

import os
import json
from typing import Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

from models import Product, MarketInsights, MarketingContent, ContentType, BRAND_GUIDELINES


class LLMContentGenerator:
    """Generates marketing content using Gemini via Google AI Studio"""

    def __init__(self, api_key: str = None, brand_guidelines = None):
        self.brand_guidelines = brand_guidelines or BRAND_GUIDELINES
        self.api_key = api_key or os.environ.get("GOOGLE_AI_API_KEY")
        self.model = None

        if GENAI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def is_available(self) -> bool:
        return GENAI_AVAILABLE and self.model is not None

    def generate_ad_script(self, product: Product, insights: MarketInsights) -> str:
        """Generate a 30-second video ad script using LLM"""

        if not self.is_available():
            return self._fallback_ad_script(product, insights)

        prompt = f"""
You are a creative director for Dot & Key, a clean Indian skincare brand.
Create a 30-second video ad script for: {product.name}

Product Details:
- Category: {product.category} ({product.subcategory})
- Price: ₹{product.price_inr}/{product.size_ml}ml
- Key Benefits: {', '.join(product.key_benefits)}
- Hero Ingredients: {', '.join(product.ingredients[:3])}
- Target Skin Types: {', '.join(product.skin_type)}
- Target Concerns: {', '.join(product.concerns)}

Market Insights:
- Top Strength: {insights.swot.strengths[0] if insights.swot.strengths else 'N/A'}
- Customer Sentiment: {insights.sentiment_analysis.overall_sentiment_score:.2f} ({insights.sentiment_analysis.total_reviews} reviews)
- Top Customer Praise: {', '.join(insights.sentiment_analysis.key_praises[:2])}
- Top Complaint: {', '.join(insights.sentiment_analysis.key_complaints[:2])}
- Trend: {insights.trend_forecast.trend_direction} ({insights.trend_forecast.predicted_demand_change_pct:+.1f}% demand)

Brand Voice: {self.brand_guidelines.brand_voice}
Key Messages: {', '.join(self.brand_guidelines.key_messages[:3])}
Target Audience: {self.brand_guidelines.target_demographics['age_range']}, {self.brand_guidelines.target_demographics['gender']}, {self.brand_guidelines.target_demographics['location']}

Format the script as a table with columns: TIME | VISUAL | AUDIO | TEXT OVERLAY
Include 6 scenes: HOOK (0-3s), PROBLEM (3-6s), SOLUTION (6-10s), BENEFITS (10-18s), SOCIAL PROOF (18-25s), CTA (25-30s)
Make it engaging, authentic, and aligned with Indian skin tones and concerns.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"LLM error: {e}")
            return self._fallback_ad_script(product, insights)

    def generate_video_concept(self, product: Product, insights: MarketInsights) -> str:
        """Generate a 15-second Reel/TikTok/Shorts concept using LLM"""

        if not self.is_available():
            return self._fallback_video_concept(product, insights)

        prompt = f"""
You are a social media creative for Dot & Key.
Create a 15-second vertical video concept (Reels/TikTok/Shorts) for: {product.name}

Product: {product.name} - {product.category}
Key Benefit: {product.key_benefits[0]}
Hero Ingredient: {product.ingredients[0]}
Price: ₹{product.price_inr}

Customer Insights:
- They love: {', '.join(insights.sentiment_analysis.key_praises[:2])}
- They complain about: {', '.join(insights.sentiment_analysis.key_complaints[:2])}
- Sentiment: {insights.sentiment_analysis.overall_sentiment_score:.2f}

Brand: {self.brand_guidelines.brand_name} - {self.brand_guidelines.tagline}
Voice: {self.brand_guidelines.brand_voice}
Colors: {self.brand_guidelines.color_palette}

Return a JSON object with:
{{
  "concept_name": "catchy name",
  "concept_type": "UGC demo / ingredient story / before-after / routine integration",
  "creative_concept": "2-3 sentence core idea",
  "target_audience": "specific",
  "key_message": "one liner",
  "visual_style": "description",
  "audio_direction": "trending audio + voiceover notes",
  "script_outline": "5-beat outline for 15 seconds",
  "talent_requirements": "who appears",
  "location": "setting",
  "props": "what's needed",
  "post_production": "editing style",
  "distribution_strategy": "platform strategy",
  "success_metrics": "KPIs",
  "budget_estimate": "rough range"
}}
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"LLM error: {e}")
            return self._fallback_video_concept(product, insights)

    def _fallback_ad_script(self, product: Product, insights: MarketInsights) -> str:
        """Fallback template-based ad script"""
        return f"""# Ad Script: {product.name}
**Duration:** 30 seconds
**Format:** Vertical 9:16
**Tone:** {self.brand_guidelines.brand_voice}

---

## SCENE 1: HOOK (0-3s)
**Visual:** Close-up of {product.name} packaging with {product.ingredients[0]} ingredient animation
**Audio:** Upbeat music starts. "Tired of {product.concerns[0] if product.concerns else 'skin issues'}?"
**Text Overlay:** Struggling with {product.concerns[0] if product.concerns else 'skin issues'}?

## SCENE 2: PROBLEM (3-6s)
**Visual:** Split screen: dull skin / clogged pores / dark spots
**Audio:** Voiceover: "We get it. {product.concerns[0] if product.concerns else 'Skin concerns'} are frustrating."
**Text Overlay:** Real skin concerns. Real solutions needed.

## SCENE 3: SOLUTION REVEAL (6-10s)
**Visual:** Hero shot of {product.name} with ingredient glow effect
**Audio:** Voiceover: "Meet {product.name}. Powered by {product.ingredients[0]}."
**Text Overlay:** Introducing {product.name}

## SCENE 4: BENEFITS DEMO (10-18s)
**Visual:** Quick cuts: application, absorption, happy skin
**Audio:** Voiceover: "{', '.join(product.key_benefits[:3])}."
**Text Overlay:** {', '.join(product.key_benefits[:3])}

## SCENE 5: SOCIAL PROOF (18-25s)
**Visual:** UGC montage: real customers, before/after, 5-star reviews
**Audio:** Customer voice: "Best {product.category.lower()} I've used!"
**Text Overlay:** ⭐ {insights.sentiment_analysis.average_rating:.1f}/5 from {insights.sentiment_analysis.total_reviews}+ reviews

## SCENE 6: CTA (25-30s)
**Visual:** {product.name} packshot + logo + "Shop at dotkey.in"
**Audio:** Voiceover: "Your skin deserves this. Tap to shop."
**Text Overlay:** Shop now at dotkey.in

---
**Key Message:** {insights.recommendations[0] if insights.recommendations else 'Science-backed skincare for Indian skin'}
**Target Audience:** {self.brand_guidelines.target_demographics['age_range']}, {self.brand_guidelines.target_demographics['gender']}, {self.brand_guidelines.target_demographics['location']}"""

    def _fallback_video_concept(self, product: Product, insights: MarketInsights) -> str:
        """Fallback template-based video concept"""
        return f"""# Video Concept: {product.name} - {product.key_benefits[0]} Challenge
**Product:** {product.name}
**Platform:** Instagram Reels / TikTok / YouTube Shorts
**Duration:** 15 seconds
**Concept Type:** UGC-style demo + ingredient education

## Creative Concept
Real users with {product.concerns[0] if product.concerns else 'skin concerns'} try {product.name} for 7 days. Document journey. Reveal results with ingredient science breakdown.

## Target Audience
{self.brand_guidelines.target_demographics['age_range']}, {self.brand_guidelines.target_demographics['gender']}, {self.brand_guidelines.target_demographics['location']}

## Key Message
{insights.recommendations[0] if insights.recommendations else 'Science-backed skincare for Indian skin'}

## Visual Style
Clean, bright, product-focused with lifestyle moments

## Audio/Music
Trending audio + original voiceover. Upbeat, relatable.

## Script Outline
Day 1: Problem intro → Day 3: First impressions → Day 7: Results reveal → Science breakdown → CTA

## Production Notes
- **Talent:** 3-5 diverse creators (skin types matching product), 1 dermatologist for credibility
- **Location:** Home/bathroom settings (authentic), 1 studio for hero shots
- **Props:** {product.name} products, ingredient visual aids, before/after lighting setup
- **Post-production:** Fast cuts, text overlays, ingredient animations, split-screen before/after

## Distribution Strategy
Launch on Instagram Reels → Cross-post to TikTok/YouTube Shorts → WhatsApp broadcast → Influencer amplification → Paid boost to lookalike audiences

## Success Metrics
Views >100K, Engagement >5%, UGC submissions >50, Click-through >2%, Sales attribution

## Budget Estimate
₹2-5L (creator fees, production, post, paid amplification)"""


def get_llm_generator(api_key: str = None) -> LLMContentGenerator:
    """Factory function to get LLM generator instance"""
    return LLMContentGenerator(api_key=api_key)