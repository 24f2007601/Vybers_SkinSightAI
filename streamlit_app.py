"""
Streamlit Web UI for Dot & Key Market Intelligence
Main demo flow: Pick product → Competitors, SWOT, Sentiment, Generated Content
"""

import streamlit as st
import asyncio
import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models import SAMPLE_DOTKEY_PRODUCTS, BRAND_GUIDELINES
from api.main import DotKeyMarketIntelligence
from content.llm_generator import LLMContentGenerator

# Page config
st.set_page_config(
    page_title="SkinSight AI — Dot & Key Market Intelligence",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dot & Key brand colors
st.markdown("""
<style>
    :root {
        --primary: #E85D75;
        --secondary: #F5F0EB;
        --accent: #4A90A4;
        --text: #2D2D2D;
        --bg: #FFFFFF;
    }
    .main { background-color: var(--bg); }
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #d44d65; }
    .metric-card {
        background: linear-gradient(135deg, #FFF 0%, #F5F0EB 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E8E0DA;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .swot-strength { border-left: 4px solid #2E7D32; }
    .swot-weakness { border-left: 4px solid #C62828; }
    .swot-opportunity { border-left: 4px solid #1565C0; }
    .swot-threat { border-left: 4px solid #EF6C00; }
    .tab-content { padding: 1rem 0; }
</style>
""", unsafe_allow_html.html=True)


@st.cache_resource
def get_system():
    """Initialize the market intelligence system"""
    return DotKeyMarketIntelligence(use_sample_data=True, output_dir="demo_output")


@st.cache_data
def load_products():
    """Load sample products"""
    return SAMPLE_DOTKEY_PRODUCTS


def run_async(coro):
    """Run async function in Streamlit"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def format_currency(val):
    """Format INR currency"""
    return f"₹{val:,.2f}"


def format_per_ml(price, size):
    """Format price per ml"""
    if size > 0:
        return f"₹{price/size:.2f}/ml"
    return "N/A"


# Header
st.markdown("""
<div style="display: flex; align-items: center; gap: 1rem; padding: 1rem 0; border-bottom: 2px solid #E85D75; margin-bottom: 2rem;">
    <div style="font-size: 2.5rem;">🧴</div>
    <div>
        <h1 style="margin: 0; color: #E85D75; font-weight: 700;">SkinSight AI</h1>
        <p style="margin: 0; color: #666; font-size: 1rem;">Dot & Key Market Intelligence → Marketing Content</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Product Picker
products = load_products()
product_names = [f"{p.name} ({p.category})" for p in products]
product_map = {f"{p.name} ({p.category})": p for p in products}

with st.sidebar:
    st.markdown("### 🎯 Select Product")
    selected_name = st.selectbox(
        "Choose a Dot & Key product to analyze",
        product_names,
        index=0,
        label_visibility="collapsed"
    )

    selected_product = product_map[selected_name]

    st.markdown("---")
    st.markdown("### 📦 Product Details")
    st.markdown(f"**Category:** {selected_product.category}")
    st.markdown(f"**Subcategory:** {selected_product.subcategory}")
    st.markdown(f"**Price:** {format_currency(selected_product.price_inr)}")
    st.markdown(f"**Size:** {selected_product.size_ml} ml")
    st.markdown(f"**Per ml:** {format_per_ml(selected_product.price_inr, selected_product.size_ml)}")

    st.markdown("**Key Benefits:**")
    for b in selected_product.key_benefits:
        st.markdown(f"• {b}")

    st.markdown("**Hero Ingredients:**")
    for ing in selected_product.ingredients[:5]:
        st.markdown(f"• {ing}")

    st.markdown("---")
    analyze_btn = st.button("🔍 Analyze Market", type="primary", use_container_width=True)

# Initialize LLM generator (uses Google AI Studio if API key available)
@st.cache_resource
def get_llm_generator():
    api_key = os.environ.get("GOOGLE_AI_API_KEY") or st.secrets.get("GOOGLE_AI_API_KEY", None)
    return LLMContentGenerator(api_key=api_key, brand_guidelines=BRAND_GUIDELINES)

# Main content area
if analyze_btn:
    with st.spinner("Running market intelligence pipeline..."):
        system = get_system()
        result = run_async(system.analyze_product(selected_product))

    # Store in session state
    st.session_state.analysis = result
    st.session_state.product = selected_product
    st.success("Analysis complete!")

# Display results if available
if "analysis" in st.session_state:
    result = st.session_state.analysis
    product = st.session_state.product
    insights = result["insights"]
    content = result["marketing_content"]
    llm_gen = get_llm_generator()

    # Tabs for main flow
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏪 Competitors",
        "📊 SWOT Analysis",
        "💬 Sentiment",
        "📝 Ad Script",
        "🎬 Video Concept"
    ])

    # TAB 1: Competitors
    with tab1:
        st.markdown("### Competitor Comparison")

        comp = insights["competitor_comparison"]
        price_comp = comp["price_comparison"]
        rating_comp = comp["rating_comparison"]

        # Price comparison chart data
        import pandas as pd
        price_df = pd.DataFrame([
            {"Brand": k, "Price per ml (₹)": v}
            for k, v in price_comp.items()
        ]).sort_values("Price per ml (₹)")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**Price per ml Comparison**")
            st.bar_chart(price_df.set_index("Brand"), height=300)

        with col2:
            st.markdown("**Rating Comparison**")
            rating_df = pd.DataFrame([
                {"Brand": k, "Rating": v}
                for k, v in rating_comp.items()
            ]).sort_values("Rating", ascending=False)
            st.dataframe(rating_df, hide_index=True, use_container_width=True)

        # Competitive advantages & gaps
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Competitive Advantages")
            for adv in comp["advantages"]:
                st.markdown(f'<div class="metric-card swot-strength" style="margin: 0.5rem 0; padding: 1rem;">{adv}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("### ⚠️ Competitive Gaps")
            for gap in comp["gaps"]:
                st.markdown(f'<div class="metric-card swot-weakness" style="margin: 0.5rem 0; padding: 1rem;">{gap}</div>', unsafe_allow_html=True)

    # TAB 2: SWOT Analysis
    with tab2:
        st.markdown("### SWOT Analysis")

        swot = insights["swot"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 💪 Strengths")
            for s in swot["strengths"]:
                st.markdown(f'<div class="metric-card swot-strength" style="margin: 0.5rem 0; padding: 1rem;">{s}</div>', unsafe_allow_html=True)

            st.markdown("#### 🎯 Opportunities")
            for o in swot["opportunities"]:
                st.markdown(f'<div class="metric-card swot-opportunity" style="margin: 0.5rem 0; padding: 1rem;">{o}</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🔴 Weaknesses")
            for w in swot["weaknesses"]:
                st.markdown(f'<div class="metric-card swot-weakness" style="margin: 0.5rem 0; padding: 1rem;">{w}</div>', unsafe_allow_html=True)

            st.markdown("#### ⚡ Threats")
            for t in swot["threats"]:
                st.markdown(f'<div class="metric-card swot-threat" style="margin: 0.5rem 0; padding: 1rem;">{t}</div>', unsafe_allow_html=True)

        # Market Gaps
        if insights["market_gaps"]:
            st.markdown("---")
            st.markdown("### 🔍 Market Gaps & Opportunities")

            # Visualization: Impact distribution
            import pandas as pd
            gap_df = pd.DataFrame(insights["market_gaps"])
            if not gap_df.empty:
                impact_counts = gap_df["impact"].value_counts()
                st.bar_chart(impact_counts, height=200)

            for gap in insights["market_gaps"]:
                impact_color = {"high": "#C62828", "medium": "#EF6C00", "low": "#1565C0"}.get(gap["impact"], "#666")
                st.markdown(f"""
                <div style="border-left: 4px solid {impact_color}; padding: 1rem; margin: 0.5rem 0; background: #FAFAFA; border-radius: 0 8px 8px 0;">
                    <strong>{gap['description']}</strong> <span style="color: {impact_color};">({gap['impact'].upper()})</span><br>
                    <em>Action: {gap['action']}</em>
                </div>
                """, unsafe_allow_html=True)

    # TAB 3: Sentiment
    with tab3:
        st.markdown("### Customer Sentiment Analysis")

        sent = insights["sentiment"]
        trend = insights["trend_forecast"]

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Reviews Analyzed", sent["total_reviews"])
        col2.metric("Avg Rating", f"{sent['avg_rating']:.1f}/5")
        col3.metric("Sentiment Score", f"{sent['overall_score']:.2f}")
        col4.metric("Trend", trend["direction"].title(), f"{trend['predicted_demand_change_pct']:+.1f}% demand")

        # Trend forecast visualization
        st.markdown("---")
        st.markdown("#### 📈 Trend Forecast (90 days)")
        trend_data = {
            "Metric": ["Direction", "Strength", "Demand Change", "Confidence"],
            "Value": [trend["direction"].title(), f"{trend['trend_strength']:.0%}", f"{trend['predicted_demand_change_pct']:+.1f}%", f"{trend.get('confidence', 0.6):.0%}"]
        }
        st.dataframe(pd.DataFrame(trend_data), hide_index=True, use_container_width=True)

        if trend["key_drivers"]:
            st.markdown("**Key Drivers:**")
            for driver in trend["key_drivers"]:
                st.markdown(f"• {driver}")

        # Top positive/negative topics
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 😊 Top Positive Topics")
            for topic, count in sent["top_positive"]:
                st.markdown(f"• **{topic}**: {count} mentions")

        with col2:
            st.markdown("#### 😟 Top Negative Topics")
            if sent["top_negative"]:
                for topic, count in sent["top_negative"]:
                    st.markdown(f"• **{topic}**: {count} mentions")
            else:
                st.markdown("*No significant negative topics*")

        # Praises & Complaints
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ✨ Key Praises")
            for p in sent["praises"]:
                st.markdown(f"• {p}")

        with col2:
            st.markdown("#### 🔴 Key Complaints")
            for c in sent["complaints"]:
                st.markdown(f"• {c}")

    # TAB 4: Ad Script
    with tab4:
        st.markdown("### Generated Ad Script (30 sec)")

        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            use_llm = st.checkbox("🤖 Use AI (Gemini)", value=llm_gen.is_available(), disabled=not llm_gen.is_available())
            if not llm_gen.is_available():
                st.caption("Set GOOGLE_AI_API_KEY to enable")
        with col3:
            tone = st.selectbox("Tone", ["Default (Brand voice)", "Playful & Gen-Z", "Scientific & Expert", "Minimalist & Clean", "Emotional & Storytelling"])

        with st.spinner("Generating ad script..." + (" 🤖" if use_llm else "")):
            if use_llm and llm_gen.is_available():
                ad_script_content = llm_gen.generate_ad_script(product, type('obj', (object,), insights)())
                # Add tone instruction if not default
                if tone != "Default (Brand voice)":
                    ad_script_content += f"\n\n---\n**Regenerated with tone:** {tone}\n*[In production, this would re-call LLM with tone-specific prompt]*"
            else:
                ad_script = None
                for key, val in content.items():
                    if val["type"] == "ad_script":
                        ad_script = val
                        break
                ad_script_content = ad_script["content"] if ad_script else "Ad script not generated"

        st.markdown(f"**Format:** Vertical 9:16 | 30 seconds")

        if st.button("🔄 Regenerate", key="regen_ad", use_container_width=True):
            st.rerun()

        # Display in code block for easy copying
        st.code(ad_script_content, language="markdown")

        # Download button
        st.download_button(
            "📥 Download Script",
            ad_script_content,
            file_name=f"{product.name.replace(' ', '_')}_ad_script.md",
            mime="text/markdown",
            use_container_width=True
        )

    # TAB 5: Video Concept
    with tab5:
        st.markdown("### Generated Video Concept (15 sec Reel/TikTok/Shorts)")

        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            use_llm = st.checkbox("🤖 Use AI (Gemini)", value=llm_gen.is_available(), disabled=not llm_gen.is_available(), key="video_llm")
            if not llm_gen.is_available():
                st.caption("Set GOOGLE_AI_API_KEY to enable")
        with col3:
            concept_type = st.selectbox("Concept Type", ["UGC Challenge", "Ingredient Story", "Before/After", "Routine Integration", "Expert Demo", "POV Skincare"])

        with st.spinner("Generating video concept..." + (" 🤖" if use_llm else "")):
            if use_llm and llm_gen.is_available():
                video_concept_content = llm_gen.generate_video_concept(product, type('obj', (object,), insights)())
                if concept_type != "UGC Challenge":
                    video_concept_content += f"\n\n---\n**Regenerated as:** {concept_type}\n*[In production, this would re-call LLM with concept-specific prompt]*"
            else:
                video_concept = None
                for key, val in content.items():
                    if val["type"] == "video_concept":
                        video_concept = val
                        break
                video_concept_content = video_concept["content"] if video_concept else "Video concept not generated"

        st.markdown(f"**Platform:** Instagram Reels / TikTok / YouTube Shorts | 15 seconds")

        if st.button("🔄 Regenerate", key="regen_video", use_container_width=True):
            st.rerun()

        st.code(video_concept_content, language="markdown")

        st.download_button(
            "📥 Download Concept",
            video_concept_content,
            file_name=f"{product.name.replace(' ', '_')}_video_concept.md",
            mime="text/markdown",
            use_container_width=True
        )

    # Recommendations at bottom
    st.markdown("---")
    st.markdown("### 🎯 Strategic Recommendations")
    for i, rec in enumerate(insights["recommendations"], 1):
        st.markdown(f"{i}. {rec}")

else:
    # Landing state
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; color: #666;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🧴</div>
        <h2>Select a product and click <strong>Analyze Market</strong></h2>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            SkinSight AI will extract competitor data, analyze customer sentiment,
            generate a SWOT analysis, and create marketing content — all in seconds.
        </p>
        <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="background: #F5F0EB; padding: 1.5rem; border-radius: 12px; min-width: 180px;">
                <strong>🏪 Competitors</strong><br>
                Price & rating comparison
            </div>
            <div style="background: #F5F0EB; padding: 1.5rem; border-radius: 12px; min-width: 180px;">
                <strong>📊 SWOT</strong><br>
                Strengths, weaknesses, opportunities, threats
            </div>
            <div style="background: #F5F0EB; padding: 1.5rem; border-radius: 12px; min-width: 180px;">
                <strong>💬 Sentiment</strong><br>
                Review analysis & trends
            </div>
            <div style="background: #F5F0EB; padding: 1.5rem; border-radius: 12px; min-width: 180px;">
                <strong>📝 Ad Script</strong><br>
                30-sec video script
            </div>
            <div style="background: #F5F0EB; padding: 1.5rem; border-radius: 12px; min-width: 180px;">
                <strong>🎬 Video Concept</strong><br>
                15-sec Reel/TikTok concept
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<hr style="margin-top: 3rem; border-color: #E8E0DA;">
<div style="text-align: center; color: #999; font-size: 0.85rem; padding: 1rem;">
    SkinSight AI — Built for Vibe Coders Hackathon Edition 3 • Team Vybers • Dot & Key
</div>
""", unsafe_allow_html=True)