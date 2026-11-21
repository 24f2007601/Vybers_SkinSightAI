"""
Marketing Content Generator
Generates marketing content from insights using templates and AI
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from string import Template

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    Product, MarketingContent, ContentType, BrandGuidelines,
    BRAND_GUIDELINES, SAMPLE_DOTKEY_PRODUCTS
)
from insights.generator import MarketInsights
from insights.generator import InsightsGenerator


@dataclass
class ContentTemplate:
    """Template for generating marketing content"""
    content_type: ContentType
    platform: str
    template: str
    required_fields: list[str]
    format_specs: dict


# Content templates
CONTENT_TEMPLATES = {
    ContentType.STATIC_AD: {
        "instagram": ContentTemplate(
            content_type=ContentType.STATIC_AD,
            platform="instagram",
            template="""
🌟 ${headline} 🌟

${body}

✨ Key Benefits:
${benefits_list}

💡 ${key_ingredient_highlight}

${cta}

#${hashtags}
            """.strip(),
            required_fields=["headline", "body", "benefits", "key_ingredient", "cta", "hashtags"],
            format_specs={"aspect_ratio": "1:1", "dimensions": "1080x1080", "format": "image/carousel"}
        ),
        "facebook": ContentTemplate(
            content_type=ContentType.STATIC_AD,
            platform="facebook",
            template="""
${headline}

${body}

🎯 Why customers love it:
${benefits_list}

${key_ingredient_highlight}

${cta}

Shop now: ${product_url}

#${hashtags}
            """.strip(),
            required_fields=["headline", "body", "benefits", "key_ingredient", "cta", "product_url", "hashtags"],
            format_specs={"aspect_ratio": "1.91:1", "dimensions": "1200x628", "format": "image"}
        ),
    },
    ContentType.PRODUCT_DESCRIPTION: {
        "website": ContentTemplate(
            content_type=ContentType.PRODUCT_DESCRIPTION,
            platform="website",
            template="""
# ${product_name}

${hook}

## What it does
${description}

## Key Benefits
${benefits_list}

## Hero Ingredients
${ingredients_detail}

## How to use
${usage_instructions}

## Perfect for
${skin_type_concerns}

## Why ${brand_name}?
${brand_differentiator}
            """.strip(),
            required_fields=["product_name", "hook", "description", "benefits", "ingredients", "usage", "skin_type", "brand_diff"],
            format_specs={"format": "html/markdown", "word_count": "300-500"}
        ),
        "amazon": ContentTemplate(
            content_type=ContentType.PRODUCT_DESCRIPTION,
            platform="amazon",
            template="""
${product_name} - ${tagline}

${short_description}

✨ KEY BENEFITS:
${benefits_bullets}

🌿 KEY INGREDIENTS:
${ingredients_bullets}

📋 HOW TO USE:
${usage_steps}

✅ SUITABLE FOR: ${skin_types}
🎯 TARGETS: ${concerns}

${brand_promise}

${certifications}
            """.strip(),
            required_fields=["product_name", "tagline", "short_desc", "benefits", "ingredients", "usage", "skin_types", "concerns", "brand_promise", "certifications"],
            format_specs={"format": "plain text", "bullet_points": True, "max_chars": 2000}
        ),
    },
    ContentType.A_PLUS_CONTENT: {
        "amazon": ContentTemplate(
            content_type=ContentType.A_PLUS_CONTENT,
            platform="amazon",
            template="""
# A+ Content Modules for ${product_name}

## Module 1: Brand Story
${brand_story}

## Module 2: Feature Comparison
${comparison_chart}

## Module 3: Ingredient Spotlight
${ingredient_spotlight}

## Module 4: Usage Guide
${usage_guide}

## Module 5: Customer Reviews Highlights
${review_highlights}

## Module 6: Cross-sell / Bundle
${bundle_suggestions}
            """.strip(),
            required_fields=["product_name", "brand_story", "comparison", "ingredients", "usage", "reviews", "bundles"],
            format_specs={"format": "modular", "modules": 6, "image_requirements": "high-res lifestyle + ingredient shots"}
        ),
    },
    ContentType.AD_SCRIPT: {
        "video": ContentTemplate(
            content_type=ContentType.AD_SCRIPT,
            platform="video",
            template="""
# Ad Script: ${product_name}
**Duration:** ${duration} seconds
**Format:** ${format}
**Tone:** ${brand_voice}

---

## SCENE 1: HOOK (0-${hook_duration}s)
**Visual:** ${hook_visual}
**Audio:** ${hook_audio}
**Text Overlay:** ${hook_text}

## SCENE 2: PROBLEM (${problem_start}-${problem_end}s)
**Visual:** ${problem_visual}
**Audio:** ${problem_audio}
**Text Overlay:** ${problem_text}

## SCENE 3: SOLUTION REVEAL (${solution_start}-${solution_end}s)
**Visual:** ${solution_visual}
**Audio:** ${solution_audio}
**Text Overlay:** ${solution_text}

## SCENE 4: BENEFITS DEMO (${benefits_start}-${benefits_end}s)
**Visual:** ${benefits_visual}
**Audio:** ${benefits_audio}
**Text Overlay:** ${benefits_text}

## SCENE 5: SOCIAL PROOF (${proof_start}-${proof_end}s)
**Visual:** ${proof_visual}
**Audio:** ${proof_audio}
**Text Overlay:** ${proof_text}

## SCENE 6: CTA (${cta_start}-${cta_end}s)
**Visual:** ${cta_visual}
**Audio:** ${cta_audio}
**Text Overlay:** ${cta_text}

---
**Key Message:** ${key_message}
**Target Audience:** ${target_audience}
            """.strip(),
            required_fields=["product_name", "duration", "format", "brand_voice", "hook", "problem", "solution", "benefits", "proof", "cta", "key_message", "target_audience"],
            format_specs={"duration_seconds": 30, "format": "vertical 9:16", "aspect_ratio": "9:16"}
        ),
    },
    ContentType.STORYBOARD: {
        "video": ContentTemplate(
            content_type=ContentType.STORYBOARD,
            platform="video",
            template="""
# Storyboard: ${product_name}
**Concept:** ${concept_title}
**Duration:** ${duration}s
**Style:** ${visual_style}

---

## Frame 1: THE HOOK
**Time:** 0-3s
**Visual:** ${frame1_visual}
**Copy:** "${frame1_copy}"
**Camera:** ${frame1_camera}
**Transition:** ${frame1_transition}

## Frame 2: THE PROBLEM
**Time:** 3-6s
**Visual:** ${frame2_visual}
**Copy:** "${frame2_copy}"
**Camera:** ${frame2_camera}
**Transition:** ${frame2_transition}

## Frame 3: THE REVEAL
**Time:** 6-10s
**Visual:** ${frame3_visual}
**Copy:** "${frame3_copy}"
**Camera:** ${frame3_camera}
**Transition:** ${frame3_transition}

## Frame 4: INGREDIENT HERO
**Time:** 10-15s
**Visual:** ${frame4_visual}
**Copy:** "${frame4_copy}"
**Camera:** ${frame4_camera}
**Transition:** ${frame4_transition}

## Frame 5: BENEFITS IN ACTION
**Time:** 15-22s
**Visual:** ${frame5_visual}
**Copy:** "${frame5_copy}"
**Camera:** ${frame5_camera}
**Transition:** ${frame5_transition}

## Frame 6: SOCIAL PROOF
**Time:** 22-27s
**Visual:** ${frame6_visual}
**Copy:** "${frame6_copy}"
**Camera:** ${frame6_camera}
**Transition:** ${frame6_transition}

## Frame 7: CALL TO ACTION
**Time:** 27-30s
**Visual:** ${frame7_visual}
**Copy:** "${frame7_copy}"
**Camera:** ${frame7_camera}

---
**Music/Mood:** ${music_mood}
**Color Palette:** ${color_palette}
**Typography:** ${typography}
            """.strip(),
            required_fields=["product_name", "concept", "duration", "style", "frames", "music", "colors", "typography"],
            format_specs={"frames": 7, "duration_seconds": 30, "aspect_ratio": "9:16"}
        ),
    },
    ContentType.VIDEO_CONCEPT: {
        "social": ContentTemplate(
            content_type=ContentType.VIDEO_CONCEPT,
            platform="social",
            template="""
# Video Concept: ${concept_name}
**Product:** ${product_name}
**Platform:** ${platform} (Reels/TikTok/Shorts)
**Duration:** ${duration}s
**Concept Type:** ${concept_type}

## Creative Concept
${creative_concept}

## Target Audience
${target_audience}

## Key Message
${key_message}

## Visual Style
${visual_style}

## Audio/Music
${audio_direction}

## Script Outline
${script_outline}

## Production Notes
- **Talent:** ${talent_requirements}
- **Location:** ${location}
- **Props:** ${props}
- **Post-production:** ${post_production}

## Distribution Strategy
${distribution_strategy}

## Success Metrics
${success_metrics}

## Budget Estimate
${budget_estimate}
            """.strip(),
            required_fields=["concept_name", "product_name", "platform", "duration", "concept_type", "creative_concept", "target_audience", "key_message", "visual_style", "audio", "script", "production", "distribution", "metrics", "budget"],
            format_specs={"duration_seconds": 15, "format": "vertical 9:16", "platforms": ["instagram_reels", "tiktok", "youtube_shorts"]}
        ),
    },
    ContentType.SOCIAL_MEDIA_POST: {
        "instagram": ContentTemplate(
            content_type=ContentType.SOCIAL_MEDIA_POST,
            platform="instagram",
            template="""
${headline}

${body}

${benefits_carousel}

${ingredient_spotlight}

${user_generated_content}

${cta}

${hashtags}

---
**Alt Text:** ${alt_text}
**Image Specs:** 1080x1080 (feed) / 1080x1920 (story)
            """.strip(),
            required_fields=["headline", "body", "benefits", "ingredient", "ugc", "cta", "hashtags", "alt_text"],
            format_specs={"format": "carousel or single image", "max_hashtags": 30}
        ),
    },
}


class ContentGenerator:
    """Generates marketing content from insights"""

    def __init__(self, brand_guidelines: BrandGuidelines = None, use_ai: bool = False):
        self.brand_guidelines = brand_guidelines or BRAND_GUIDELINES
        self.use_ai = use_ai  # Would integrate with actual LLM API

    def generate_content(
        self,
        product: Product,
        insights: MarketInsights,
        content_type: ContentType,
        platform: str = "instagram"
    ) -> MarketingContent:
        """Generate marketing content for a product"""

        template_key = platform if platform in CONTENT_TEMPLATES.get(content_type, {}) else "default"
        template = CONTENT_TEMPLATES.get(content_type, {}).get(template_key)

        if not template:
            # Fallback to first available template for this content type
            templates = CONTENT_TEMPLATES.get(content_type, {})
            template = list(templates.values())[0] if templates else None

        if not template:
            raise ValueError(f"No template for {content_type} on {platform}")

        # Prepare template variables
        variables = self._prepare_variables(product, insights, content_type, platform)

        # Generate content using template
        content_text = self._render_template(template, variables)

        # Create MarketingContent object
        return MarketingContent(
            product_id=product.id,
            content_type=content_type,
            title=variables.get("headline", f"{product.name} - {content_type.value}"),
            content=content_text,
            platform=platform,
            format_specs=template.format_specs,
            brand_voice=self.brand_guidelines.brand_voice,
            target_audience=self._get_target_audience_string(),
            key_message=insights.recommendations[0] if insights.recommendations else "",
            cta=variables.get("cta", "Shop now at dotkey.in"),
            metadata={
                "template_used": template_key,
                "variables": variables,
                "insights_summary": {
                    "top_strength": insights.swot.strengths[0] if insights.swot.strengths else "",
                    "top_gap": insights.market_gaps[0].description if insights.market_gaps else "",
                    "trend": insights.trend_forecast.trend_direction,
                }
            }
        )

    def _prepare_variables(
        self,
        product: Product,
        insights: MarketInsights,
        content_type: ContentType,
        platform: str
    ) -> dict:
        """Prepare template variables from product and insights"""

        # Common variables
        variables = {
            "product_name": product.name,
            "brand_name": self.brand_guidelines.brand_name,
            "tagline": self.brand_guidelines.tagline,
            "brand_voice": self.brand_guidelines.brand_voice,
            "product_url": product.product_url,
            "price_inr": product.price_inr,
            "size_ml": product.size_ml,
        }

        # Color palette
        variables.update({f"color_{k}": v for k, v in self.brand_guidelines.color_palette.items()})

        # Benefits formatting
        variables["benefits_list"] = "\n".join([f"• {b}" for b in product.key_benefits])
        variables["benefits_bullets"] = "\n".join([f"▸ {b}" for b in product.key_benefits])
        variables["benefits_carousel"] = "\n\n".join([f"Slide {i+1}: {b}" for i, b in enumerate(product.key_benefits)])

        # Ingredients
        variables["ingredients_detail"] = "\n".join([
            f"**{ing}**: {self._get_ingredient_benefit(ing)}" for ing in product.ingredients[:5]
        ])
        variables["ingredients_bullets"] = "\n".join([f"▸ {ing}" for ing in product.ingredients[:6]])
        variables["ingredient_spotlight"] = self._format_ingredient_spotlight(product.ingredients[:3])

        # Skin type & concerns
        variables["skin_types"] = ", ".join(product.skin_type)
        variables["concerns"] = ", ".join(product.concerns)
        variables["skin_type_concerns"] = f"Skin types: {', '.join(product.skin_type)} | Concerns: {', '.join(product.concerns)}"

        # Usage
        variables["usage_instructions"] = self._generate_usage_instructions(product)
        variables["usage_steps"] = self._generate_usage_steps(product)

        # Insights-driven content
        variables["headline"] = self._generate_headline(product, insights, platform)
        variables["body"] = self._generate_body(product, insights, platform)
        variables["hook"] = self._generate_hook(product, insights)
        variables["short_description"] = self._generate_short_description(product, insights)
        variables["description"] = product.description

        # Key ingredient highlight
        hero_ingredient = product.ingredients[0] if product.ingredients else "key ingredients"
        variables["key_ingredient_highlight"] = f"Powered by {hero_ingredient} ✨"

        # CTA
        variables["cta"] = self._generate_cta(product, platform)

        # Hashtags
        variables["hashtags"] = self._generate_hashtags(product, platform)

        # Brand differentiator
        variables["brand_differentiator"] = self._generate_brand_differentiator(insights)

        # Brand promise
        variables["brand_promise"] = " | ".join(self.brand_guidelines.key_messages[:3])

        # Certifications
        variables["certifications"] = "Dermatologically Tested • Cruelty-Free • Vegan • Made for Indian Skin"

        # Video-specific variables
        if content_type in [ContentType.AD_SCRIPT, ContentType.STORYBOARD, ContentType.VIDEO_CONCEPT]:
            variables.update(self._generate_video_variables(product, insights, content_type))

        return variables

    def _get_ingredient_benefit(self, ingredient: str) -> str:
        """Get benefit description for ingredient"""
        benefits = {
            "Vitamin C": "Brightens & fades dark spots",
            "Vitamin E": "Antioxidant protection & healing",
            "Niacinamide": "Minimizes pores & controls oil",
            "Zinc PCA": "Regulates sebum & prevents acne",
            "Hyaluronic Acid": "Deep hydration & plumping",
            "Ceramide": "Repairs skin barrier",
            "Retinol": "Reduces fine lines & wrinkles",
            "Bakuchiol": "Natural retinol alternative",
            "Watermelon Extract": "Hydrating & soothing",
            "Aloe Vera": "Soothes & calms irritation",
            "Squalane": "Non-greasy moisturization",
            "Peptides": "Boosts collagen & firmness",
        }
        return benefits.get(ingredient, "Skin-loving ingredient")

    def _format_ingredient_spotlight(self, ingredients: list[str]) -> str:
        """Format ingredient spotlight section"""
        lines = []
        for ing in ingredients:
            lines.append(f"🌿 **{ing}**: {self._get_ingredient_benefit(ing)}")
        return "\n".join(lines)

    def _generate_usage_instructions(self, product: Product) -> str:
        """Generate usage instructions based on product category"""
        base = "Apply to clean, dry skin. "
        if product.category == "Face Wash":
            return base + "Massage gently on damp face for 30 seconds. Rinse thoroughly. Use AM & PM."
        elif product.category == "Sunscreen":
            return base + "Apply generously 15 mins before sun exposure. Reapply every 2 hours."
        elif product.category == "Serum":
            return base + "Apply 2-3 drops. Pat gently until absorbed. Follow with moisturizer."
        elif product.category == "Moisturizer":
            return base + "Apply evenly on face & neck. Use AM & PM after serum."
        return base + "Use as directed."

    def _generate_usage_steps(self, product: Product) -> str:
        """Generate numbered usage steps"""
        steps = {
            "Face Wash": ["Wet face", "Massage for 30s", "Rinse thoroughly", "Pat dry"],
            "Sunscreen": ["Cleanse face", "Apply serum/moisturizer", "Apply sunscreen generously", "Wait 15 mins before sun"],
            "Serum": ["Cleanse & tone", "Apply 2-3 drops", "Pat to absorb", "Follow with moisturizer"],
            "Moisturizer": ["Cleanse & apply serum", "Take pea-sized amount", "Massage upward", "Use AM & PM"],
        }
        return "\n".join([f"{i+1}. {s}" for i, s in enumerate(steps.get(product.category, ["Apply to clean skin"]))])

    def _generate_headline(self, product: Product, insights: MarketInsights, platform: str) -> str:
        """Generate platform-appropriate headline"""
        headlines = {
            "instagram": [
                f"✨ Meet your new skincare obsession: {product.name}",
                f"🌟 Why {product.name} is breaking the internet",
                f"💫 The secret to {product.key_benefits[0].lower()}? {product.name}",
            ],
            "facebook": [
                f"Discover {product.name} - {product.key_benefits[0]}",
                f"Real results with {product.name}",
            ],
            "video": [
                f"{product.name}: {product.key_benefits[0]} in 30 seconds",
            ]
        }
        return headlines.get(platform, headlines["instagram"])[0]

    def _generate_body(self, product: Product, insights: MarketInsights, platform: str) -> str:
        """Generate body copy"""
        strength = insights.swot.strengths[0] if insights.swot.strengths else "loved by customers"
        return f"Formulated with {', '.join(product.ingredients[:3])}, {product.name} delivers {product.key_benefits[0].lower()} like never before. {strength}!"

    def _generate_hook(self, product: Product, insights: MarketInsights) -> str:
        """Generate hook for product description"""
        return f"Struggling with {product.concerns[0] if product.concerns else 'skin concerns'}? You're not alone."

    def _generate_short_description(self, product: Product, insights: MarketInsights) -> str:
        """Generate short description for Amazon"""
        return f"{product.name} - {product.description[:150]}..."

    def _generate_cta(self, product: Product, platform: str) -> str:
        """Generate platform-appropriate CTA"""
        ctas = {
            "instagram": "🛍️ Tap to shop at dotkey.in",
            "facebook": "Shop Now →",
            "amazon": "Add to Cart",
            "video": "Swipe up to shop!",
            "website": "Add to Bag",
        }
        return ctas.get(platform, "Shop now at dotkey.in")

    def _generate_hashtags(self, product: Product, platform: str) -> str:
        """Generate relevant hashtags"""
        base_tags = ["DotAndKey", "SkincareRoutine", "CleanBeauty", "IndianSkincare", "DermatologistTested"]
        category_tags = [product.category.replace(" ", ""), product.subcategory.replace(" ", "")]
        ingredient_tags = [ing.replace(" ", "").replace("%", "") for ing in product.ingredients[:2]]
        all_tags = base_tags + category_tags + ingredient_tags
        return " ".join([f"#{tag}" for tag in all_tags[:20]])

    def _generate_brand_differentiator(self, insights: MarketInsights) -> str:
        """Generate brand differentiator from insights"""
        if insights.competitor_comparison.competitive_advantages:
            return f"Unlike others, {insights.competitor_comparison.competitive_advantages[0].lower()}."
        return "Science-backed, clean formulations made specifically for Indian skin."

    def _get_target_audience_string(self) -> str:
        """Format target audience from brand guidelines"""
        demo = self.brand_guidelines.target_demographics
        return f"{demo['age_range']}, {demo['gender']}, {demo['location']}, interested in {', '.join(demo['interests'][:3])}"

    def _generate_video_variables(self, product: Product, insights: MarketInsights, content_type: ContentType) -> dict:
        """Generate variables for video content"""
        vars = {
            "duration": 30,
            "format": "Vertical 9:16",
            "concept_title": f"{product.name} - {product.key_benefits[0]} Story",
            "visual_style": "Clean, bright, product-focused with lifestyle moments",
            "music_mood": "Upbeat, confident, modern",
            "color_palette": ", ".join(self.brand_guidelines.color_palette.values()),
            "typography": f"{self.brand_guidelines.typography['heading']} / {self.brand_guidelines.typography['body']}",
        }

        if content_type == ContentType.AD_SCRIPT:
            vars.update({
                "hook_duration": 3,
                "problem_start": 3, "problem_end": 6,
                "solution_start": 6, "solution_end": 10,
                "benefits_start": 10, "benefits_end": 18,
                "proof_start": 18, "proof_end": 25,
                "cta_start": 25, "cta_end": 30,
                "hook_visual": f"Close-up of {product.name} packaging with {product.ingredients[0]} ingredient animation",
                "hook_audio": "Upbeat music starts. 'Tired of [concern]?'",
                "hook_text": f"Struggling with {product.concerns[0] if product.concerns else 'skin issues'}?",
                "problem_visual": "Split screen: dull skin / clogged pores / dark spots",
                "problem_audio": "Voiceover: 'We get it. [Concern] is frustrating.'",
                "problem_text": "Real skin concerns. Real solutions needed.",
                "solution_visual": f"Hero shot of {product.name} with ingredient glow effect",
                "solution_audio": f"Voiceover: 'Meet {product.name}. Powered by {product.ingredients[0]}.'",
                "solution_text": f"Introducing {product.name}",
                "benefits_visual": "Quick cuts: application, absorption, happy skin",
                "benefits_audio": "Voiceover: 'Brightens. Hydrates. Transforms.'",
                "benefits_text": ", ".join(product.key_benefits[:3]),
                "proof_visual": "UGC montage: real customers, before/after, 5-star reviews",
                "proof_audio": "Customer voice: 'Best [category] I've used!'",
                "proof_text": f"⭐ {insights.sentiment_analysis.average_rating:.1f}/5 from {insights.sentiment_analysis.total_reviews}+ reviews",
                "cta_visual": f"{product.name} packshot + logo + 'Shop at dotkey.in'",
                "cta_audio": "Voiceover: 'Your skin deserves this. Tap to shop.'",
                "cta_text": "Shop now at dotkey.in",
                "key_message": insights.recommendations[0] if insights.recommendations else "",
                "target_audience": self._get_target_audience_string(),
            })

        elif content_type == ContentType.STORYBOARD:
            vars.update({
                "frame1_visual": f"Extreme close-up: {product.ingredients[0]} molecule animation",
                "frame1_copy": "Science meets nature",
                "frame1_camera": "Macro lens, slow push in",
                "frame1_transition": "Match cut to",
                "frame2_visual": "Relatable skin concern moment (mirror check, frustration)",
                "frame2_copy": "We see you. We get it.",
                "frame2_camera": "Handheld, intimate",
                "frame2_transition": "Wipe to",
                "frame3_visual": f"Product hero reveal - {product.name} floating with ingredient particles",
                "frame3_copy": f"Meet {product.name}",
                "frame3_camera": "Crane shot, dramatic lighting",
                "frame3_transition": "Dissolve to",
                "frame4_visual": f"Ingredient story: {product.ingredients[0]} sourcing + benefit animation",
                "frame4_copy": f"Powered by {product.ingredients[0]}",
                "frame4_camera": "Macro + animation",
                "frame4_transition": "Cut to",
                "frame5_visual": "Split screen: application → absorption → glowing result",
                "frame5_copy": product.key_benefits[0],
                "frame5_camera": "Beauty lighting, smooth motion",
                "frame5_transition": "Jump cut to",
                "frame6_visual": "Real customer testimonials / UGC grid",
                "frame6_copy": f"Loved by {insights.sentiment_analysis.total_reviews}+ customers",
                "frame6_camera": "Authentic, diverse",
                "frame6_transition": "Fade to",
                "frame7_visual": f"Packshot + logo + CTA button animation",
                "frame7_copy": "Your turn to glow. Shop dotkey.in",
                "frame7_camera": "Static, clean",
            })

        elif content_type == ContentType.VIDEO_CONCEPT:
            vars.update({
                "concept_name": f"{product.name} - {product.key_benefits[0]} Challenge",
                "concept_type": "UGC-style demo + ingredient education",
                "creative_concept": f"Real users with {product.concerns[0] if product.concerns else 'skin concerns'} try {product.name} for 7 days. Document journey. Reveal results with ingredient science breakdown.",
                "target_audience": self._get_target_audience_string(),
                "key_message": insights.recommendations[0] if insights.recommendations else "",
                "visual_style": vars["visual_style"],
                "audio_direction": "Trending audio + original voiceover. Upbeat, relatable.",
                "script_outline": "Day 1: Problem intro → Day 3: First impressions → Day 7: Results reveal → Science breakdown → CTA",
                "talent_requirements": "3-5 diverse creators (skin types matching product), 1 dermatologist for credibility",
                "location": "Home/bathroom settings (authentic), 1 studio for hero shots",
                "props": f"{product.name} products, ingredient visual aids, before/after lighting setup",
                "post_production": "Fast cuts, text overlays, ingredient animations, split-screen before/after",
                "distribution_strategy": "Launch on Instagram Reels → Cross-post to TikTok/YouTube Shorts → WhatsApp broadcast → Influencer amplification → Paid boost to lookalike audiences",
                "success_metrics": "Views >100K, Engagement >5%, UGC submissions >50, Click-through >2%, Sales attribution",
                "budget_estimate": "₹2-5L (creator fees, production, post, paid amplification)",
            })

        return vars

    def _render_template(self, template: ContentTemplate, variables: dict) -> str:
        """Render template with variables"""
        try:
            return Template(template.template).safe_substitute(variables)
        except Exception as e:
            print(f"Template rendering error: {e}")
            return template.template


async def main():
    from models import SAMPLE_DOTKEY_PRODUCTS
    from insights.generator import InsightsGenerator

    # Generate insights first
    generator = InsightsGenerator(use_sample_data=True)
    product = SAMPLE_DOTKEY_PRODUCTS[0]  # Vitamin C Face Wash
    insights = await generator.generate_insights(product)

    # Generate content
    content_gen = ContentGenerator()

    print(f"=== Generating Content for: {product.name} ===\n")

    # Static Ad - Instagram
    ad = content_gen.generate_content(product, insights, ContentType.STATIC_AD, "instagram")
    print(f"--- STATIC AD (Instagram) ---")
    print(ad.content[:500] + "..." if len(ad.content) > 500 else ad.content)

    print(f"\n--- PRODUCT DESCRIPTION (Website) ---")
    desc = content_gen.generate_content(product, insights, ContentType.PRODUCT_DESCRIPTION, "website")
    print(desc.content[:500] + "..." if len(desc.content) > 500 else desc.content)

    print(f"\n--- AD SCRIPT (Video) ---")
    script = content_gen.generate_content(product, insights, ContentType.AD_SCRIPT, "video")
    print(script.content[:500] + "..." if len(script.content) > 500 else script.content)

    print(f"\n--- STORYBOARD ---")
    storyboard = content_gen.generate_content(product, insights, ContentType.STORYBOARD, "video")
    print(storyboard.content[:500] + "..." if len(storyboard.content) > 500 else storyboard.content)

    print(f"\n--- VIDEO CONCEPT ---")
    video = content_gen.generate_content(product, insights, ContentType.VIDEO_CONCEPT, "social")
    print(video.content[:500] + "..." if len(video.content) > 500 else video.content)

    print(f"\n--- A+ CONTENT (Amazon) ---")
    aplus = content_gen.generate_content(product, insights, ContentType.A_PLUS_CONTENT, "amazon")
    print(aplus.content[:500] + "..." if len(aplus.content) > 500 else aplus.content)


if __name__ == "__main__":
    asyncio.run(main())