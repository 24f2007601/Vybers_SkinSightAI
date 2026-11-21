import React from "react";

export default function CompetitorBenchmarkingTab({ product, comparison }) {
  if (!comparison) {
    return (
      <div className="nb-card p-10 text-center">
        <p className="font-bold text-nb-muted">No competitor benchmark data for this SKU.</p>
      </div>
    );
  }

  const { price_comparison = {}, competitive_advantages = [], competitive_gaps = [], competitors = [] } = comparison;
  const dkPrice = price_comparison["Dot & Key"] || 0;
  const others = Object.entries(price_comparison).filter(([brand]) => brand !== "Dot & Key");

  return (
    <div className="space-y-6">

      {/* ── Unit Economics Cards ── */}
      <div>
        <div className="nb-section-label">Normalized Unit Economics (₹ / ml)</div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

          {/* Dot & Key — pink */}
          <div
            className="p-5 border-2 border-black rounded-[10px]"
            style={{ background: '#FF4081', boxShadow: '4px 4px 0 #000' }}
          >
            <div className="text-[9px] font-black uppercase tracking-widest text-white/70 mb-2">DOT & KEY</div>
            <div className="text-4xl font-black text-white">₹{dkPrice}</div>
            <div className="text-[10px] font-bold text-white/60 mt-1">per ml · OUR SKU</div>
          </div>

          {/* Competitors */}
          {others.slice(0, 3).map(([brand, price]) => {
            const diff = ((price - dkPrice) / (dkPrice || 1) * 100).toFixed(0);
            const isMore = price > dkPrice;
            return (
              <div key={brand} className="nb-card p-5">
                <div className="text-[9px] font-black uppercase tracking-widest text-nb-muted mb-2 truncate">{brand}</div>
                <div className="text-4xl font-black text-black">₹{price}</div>
                <span className={`nb-badge mt-2 text-[9px] ${isMore ? 'nb-badge-green' : 'nb-badge-red'}`}>
                  {isMore ? `+${diff}% costlier` : `${diff}% cheaper`}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── Competitor Table ── */}
      <div>
        <div className="nb-section-label">
          Top Benchmark Competitors ({competitors.length} tracked)
        </div>
        <table className="nb-table w-full">
          <thead>
            <tr>
              <th>#</th>
              <th>Brand & Product</th>
              <th>Price (INR)</th>
              <th>Volume</th>
              <th>Rating</th>
              <th>Reviews</th>
            </tr>
          </thead>
          <tbody>
            {competitors.map((comp, idx) => (
              <tr key={idx}>
                <td className="font-black text-nb-muted text-xs">{idx + 1}</td>
                <td>
                  <div className="font-bold text-xs">{comp.brand}</div>
                  <div className="text-[10px] text-nb-muted mt-0.5 line-clamp-1">{comp.product_name}</div>
                </td>
                <td><span className="font-black text-sm">₹{comp.price_inr}</span></td>
                <td className="text-xs font-medium text-nb-muted">{comp.size_ml}ml</td>
                <td>
                  <span className="nb-badge-yellow text-[10px]">★ {comp.rating}</span>
                </td>
                <td className="text-xs font-bold">{comp.review_count?.toLocaleString() ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ── Advantages & Gaps ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div
          className="p-5 border-2 border-black rounded-[10px]"
          style={{ background: '#4ADE80', boxShadow: '4px 4px 0 #000' }}
        >
          <div className="nb-section-label">✅ Competitive Advantages</div>
          <ul className="space-y-2">
            {competitive_advantages.map((adv, i) => (
              <li key={i} className="flex items-start gap-2 text-xs font-medium text-black">
                <span className="mt-0.5 w-4 h-4 flex-shrink-0 border-2 border-black bg-white rounded-nb flex items-center justify-center font-black text-[9px]">
                  {i + 1}
                </span>
                {adv}
              </li>
            ))}
          </ul>
        </div>

        <div
          className="p-5 border-2 border-black rounded-[10px]"
          style={{ background: '#FDE047', boxShadow: '4px 4px 0 #000' }}
        >
          <div className="nb-section-label">⚠ Market Gaps to Address</div>
          <ul className="space-y-2">
            {competitive_gaps.map((gap, i) => (
              <li key={i} className="flex items-start gap-2 text-xs font-medium text-black">
                <span className="mt-0.5 w-4 h-4 flex-shrink-0 border-2 border-black bg-white rounded-nb flex items-center justify-center font-black text-[9px]">
                  {i + 1}
                </span>
                {gap}
              </li>
            ))}
          </ul>
        </div>
      </div>

    </div>
  );
}
