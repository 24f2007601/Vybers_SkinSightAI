import React from "react";

export default function StrategicInsightsTab({ product, insights }) {
  if (!insights) {
    return (
      <div className="nb-card p-10 text-center">
        <p className="font-bold text-nb-muted">No insights data loaded.</p>
      </div>
    );
  }

  const swot = insights.swot || { strengths: [], weaknesses: [], opportunities: [], threats: [] };
  const gaps = insights.market_gaps || [];
  const trend = insights.trend_forecast || {};
  const acq = insights.customer_acquisition || {};

  const SWOT_BLOCKS = [
    { key: "strengths",    label: "💪 Strengths",    bg: "#4ADE80", textClass: "text-green-900" },
    { key: "weaknesses",   label: "🔍 Weaknesses",   bg: "#FDE047", textClass: "text-yellow-900" },
    { key: "opportunities",label: "🚀 Opportunities",bg: "#60A5FA", textClass: "text-blue-900" },
    { key: "threats",      label: "⚡ Threats",       bg: "#F87171", textClass: "text-red-900" },
  ];

  return (
    <div className="space-y-6">

      {/* ── SWOT Grid ── */}
      <div>
        <div className="nb-section-label">Automated SWOT Matrix</div>
        <div className="grid grid-cols-2 gap-4">
          {SWOT_BLOCKS.map(({ key, label, bg, textClass }) => (
            <div
              key={key}
              className="p-5 border-2 border-black rounded-[10px]"
              style={{ background: bg, boxShadow: "4px 4px 0 #000" }}
            >
              <div className="text-xs font-black mb-3 text-black">{label}</div>
              <ul className="space-y-2">
                {swot[key]?.map((item, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs font-medium text-black">
                    <span className={`mt-0.5 w-4 h-4 flex-shrink-0 border-2 border-black bg-white rounded-nb flex items-center justify-center font-black text-[9px]`}>
                      {i + 1}
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* ── Customer Switcher Acquisition ── */}
      <div
        className="p-5 border-2 border-black rounded-[10px]"
        style={{ background: "#C084FC", boxShadow: "4px 4px 0 #000" }}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="nb-section-label">🎯 Weaponized Customer Switcher Strategy</div>
          <span className="nb-badge-black text-[9px]">ACQUISITION ENGINE</span>
        </div>

        {/* Hooks */}
        {acq.customer_switcher_hooks?.length > 0 && (
          <div className="mb-4">
            <div className="text-[9px] font-black uppercase tracking-widest text-black/50 mb-2">Switcher Hooks</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {acq.customer_switcher_hooks.map((hook, i) => (
                <div
                  key={i}
                  className="border-2 border-black bg-white p-3 rounded-nb text-xs font-medium text-black"
                  style={{ boxShadow: "2px 2px 0 #000" }}
                >
                  <span className="text-purple-700 font-black mr-1">🎯</span>"{hook}"
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Price arbitrage */}
        {acq.price_arbitrage_angle && (
          <div
            className="border-2 border-black bg-white p-3 rounded-nb text-xs font-bold text-black mb-4"
            style={{ boxShadow: "2px 2px 0 #000" }}
          >
            <span className="font-black text-purple-700 mr-1">₹</span>
            {acq.price_arbitrage_angle}
          </div>
        )}

        {/* Competitor friction */}
        {acq.competitor_friction_points && Object.keys(acq.competitor_friction_points).length > 0 && (
          <div>
            <div className="text-[9px] font-black uppercase tracking-widest text-black/50 mb-2">
              Competitor Vulnerabilities Exploited
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {Object.entries(acq.competitor_friction_points).map(([comp, frictions], idx) => (
                <div
                  key={idx}
                  className="border-2 border-black bg-white p-2.5 rounded-nb"
                  style={{ boxShadow: "2px 2px 0 #000" }}
                >
                  <div className="font-black text-xs text-black mb-1">{comp}</div>
                  <ul className="space-y-0.5">
                    {(Array.isArray(frictions) ? frictions : [String(frictions)]).map((f, fi) => (
                      <li key={fi} className="text-[10px] text-red-700 font-medium">⚠ {f}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* ── Market Gaps + Trend Forecast ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">

        {/* Market gaps */}
        <div className="lg:col-span-2 nb-card p-5">
          <div className="nb-section-label">Market Gaps & Tactical Actions</div>
          <div className="space-y-3">
            {gaps.map((gap, i) => (
              <div
                key={i}
                className="border-2 border-black p-3 rounded-nb"
                style={{ background: i % 2 === 0 ? "#F3F4F6" : "#fff", boxShadow: "2px 2px 0 #000" }}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-black text-xs text-black">{gap.description}</span>
                  <span
                    className={`nb-badge text-[9px] ${
                      gap.potential_impact === "high" ? "nb-badge-red" : "nb-badge-blue"
                    }`}
                  >
                    {gap.potential_impact} impact
                  </span>
                </div>
                <p className="text-[11px] font-medium text-nb-muted">
                  <span className="font-black text-black">→ </span>
                  {gap.suggested_action}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Trend forecast */}
        <div
          className="p-5 border-2 border-black rounded-[10px] flex flex-col justify-between"
          style={{ background: "#22D3EE", boxShadow: "4px 4px 0 #000" }}
        >
          <div>
            <div className="nb-section-label">90-Day Demand Forecast</div>
            <div className="text-5xl font-black text-black mt-2">
              {trend.predicted_demand_change_pct > 0 ? `+${trend.predicted_demand_change_pct}%` : `${trend.predicted_demand_change_pct}%`}
            </div>
            <div className="text-xs font-bold text-black/60 mt-1">
              {trend.category} · {trend.direction}
            </div>
            <ul className="mt-3 space-y-1">
              {trend.key_drivers?.map((d, di) => (
                <li key={di} className="text-[11px] font-medium text-black flex items-center gap-1">
                  <span className="font-black">↗</span> {d}
                </li>
              ))}
            </ul>
          </div>
          <div className="pt-3 mt-3 border-t-2 border-black flex justify-between text-[11px] font-black text-black">
            <span>Confidence</span>
            <span>{Math.round((trend.confidence || 0.75) * 100)}%</span>
          </div>
        </div>

      </div>
    </div>
  );
}
