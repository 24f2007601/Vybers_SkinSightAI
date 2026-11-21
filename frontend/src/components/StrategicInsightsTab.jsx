import { useState, useEffect } from "react";

export default function StrategicInsightsTab({ product, insights }) {
  const [isLoading, setIsLoading] = useState(true);
  const [swot, setSWOT] = useState({});
  const [marketGaps, setMarketGaps] = useState([]);
  const [trendForecast, setTrendForecast] = useState({});
  const [customerAcquisition, setCustomerAcquisition] = useState({});

  useEffect(() => {
    // Would fetch insights from API
    const timeout = setTimeout(() => {
      setIsLoading(false);
      setSWOT({
        strengths: ["Dermatologically tested formulations", "Clean ingredients, no nasties", "Made for Indian skin"],
        weaknesses: ["Premium pricing", "Limited distribution in tier-2 cities"],
        opportunities: ["Growing demand for clean beauty", "Expansion into haircare"],
        threats: ["Intense competition", "Raw material cost increases"],
      });
      setMarketGaps([
        { description: "Hyaluronic acid serums in budget range", evidence: ["Customer requests"], potential_impact: "high", suggested_action: "Launch budget hyaluronic serum" },
        { description: "Fragrance-free options for sensitive skin", evidence: ["Negative feedback on fragrance"], potential_impact: "medium", suggested_action: "Formulate fragrance-free variants" },
      ]);
      setTrendForecast({
        category: "Skincare",
        trend_direction: "rising",
        trend_strength: 0.78,
        key_drivers: ["Increased consciousness", "Social media influence"],
        predicted_demand_change_pct: 12.5,
        confidence: 0.82,
      });
      setCustomerAcquisition({
        target_competitors: ["Minimalist", "The Derma Co"],
        competitor_friction_points: {"Minimalist": ["beginner sting"], "The Derma Co": ["drying cleansers"]},
        counter_positioning_claims: ["Dermatologically tested", "Made for Indian skin"],
        customer_switcher_hooks: ["Try our trial size", "Switch and save 20%"],
        whitespace_opportunities: ["Haircare", "Body care"],
        price_arbitrage_angle: "Premium positioning against mid-range competitors",
      });
    }, 500);
    return () => clearTimeout(timeout);
  }, [product, insights]);

  if (isLoading) {
    return (
      <div className="min-h-[500px] flex items-center justify-center p-8">
        <span className="text-[var(--color-muted)]">Loading strategic insights...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* SWOT Grid */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="text-sm font-medium text-[var(--color-primary)] uppercase tracking-wider mb-3">Strengths</h3>
          <ul className="space-y-2 text-sm">
            {swot.strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-primary)] uppercase tracking-wider mb-3">Weaknesses</h3>
          <ul className="space-y-2 text-sm">
            {swot.weaknesses.map((w, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-teal)" strokeWidth="2">
                  <path d="M6 2L3 6M6 2l3 6M2 6l6 6"/>
                </svg>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-primary)] uppercase tracking-wider mb-3">Opportunities</h3>
          <ul className="space-y-2 text-sm">
            {swot.opportunities.map((o, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-teal)" strokeWidth="2">
                  <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
                </svg>
                <span>{o}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-primary)] uppercase tracking-wider mb-3">Threats</h3>
          <ul className="space-y-2 text-sm">
            {swot.threats.map((t, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-muted)" strokeWidth="2">
                  <path d="M18 6L9 17l-5 5"/>
                </svg>
                <span>{t}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Market Gaps */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
        <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Market Gaps Identified</h3>
        <ul className="space-y-3 text-sm">
          {marketGaps.map((gap, i) => (
            <li key={i} className="flex items-start gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
              </svg>
              <div>
                <p className="font-medium">{gap.description}</p>
                <p className="text-[var(--color-muted)] text-xs">{gap.suggested_action}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Trend Forecast */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Trend Direction</h3>
          <p className="text-2xl font-bold text-[var(--color-primary)]">{trendForecast.trend_direction}</p>
          <p className="text-sm text-[var(--color-muted)]">{trendForecast.trend_strength > 0.7 ? "Strong" : trendForecast.trend_strength > 0.4 ? "Moderate" : "Emerging"} trend</p>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Projected Demand Change</h3>
          <p className="text-2xl font-bold {trendForecast.predicted_demand_change_pct > 0 ? 'text-[var(--color-primary)]' : 'text-[var(--color-teal)]'}">
            {trendForecast.predicted_demand_change_pct > 0 ? '+' : ''}{trendForecast.predicted_demand_change_pct}%
          </p>
          <p className="text-sm text-[var(--color-muted)]">over next 90 days</p>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Confidence</h3>
          <div className="h-4 w-24 bg-[var(--color-surface2)] rounded-full overflow-hidden">
            <div
              className="h-full bg-[var(--color-primary)] rounded-full transition-width"
              style={{ width: `${trendForecast.confidence * 24}px` }}
            ></div>
          </div>
          <p className="text-xs text-[var(--color-muted)] ml-2">{Math.round(trendForecast.confidence * 100)}% confidence</p>
        </div>
      </div>

      {/* Customer Acquisition Strategy */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Target Competitors</h3>
          <ul className="space-y-2 text-sm">
            {customerAcquisition.target_competitors.map((c, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Counter Positioning Claims</h3>
          <ul className="space-y-2 text-sm">
            {customerAcquisition.counter_positioning_claims.map((c, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Whitespace & Price Arbitrage */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Whitespace Opportunities</h3>
          <ul className="space-y-2 text-sm">
            {customerAcquisition.whitespace_opportunities.map((w, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-teal)" strokeWidth="2">
                  <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
                </svg>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Price Arbitrage Angle</h3>
          <p className="font-medium text-[var(--color-primary)]">{customerAcquisition.price_arbitrage_angle}</p>
        </div>
      </div>
    </div>
  );
}