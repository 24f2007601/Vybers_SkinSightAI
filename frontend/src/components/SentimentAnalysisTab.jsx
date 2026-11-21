import React from "react";

export default function SentimentAnalysisTab({ product, sentiment }) {
  if (!sentiment) {
    return (
      <div className="nb-card p-10 text-center">
        <p className="font-bold text-nb-muted">No sentiment data for this SKU.</p>
      </div>
    );
  }

  const score = sentiment.overall_score ?? 0;
  const rating = sentiment.avg_rating ?? 4.0;
  const totalReviews = sentiment.total_reviews ?? 0;
  const praises = sentiment.praises || [];
  const complaints = sentiment.complaints || [];
  const topPositive = sentiment.top_positive || [];
  const topNegative = sentiment.top_negative || [];
  const dist = sentiment.sentiment_distribution || {};
  const totalSent = (dist.positive || 0) + (dist.negative || 0);
  const positivePct = Math.round(((dist.positive || 0) / Math.max(1, totalSent)) * 100);

  const scoreLabel = score > 0.3 ? "POSITIVE" : score > 0 ? "NEUTRAL" : "NEGATIVE";
  const scoreBg = score > 0.3 ? "#4ADE80" : score > 0 ? "#FDE047" : "#F87171";

  return (
    <div className="space-y-6">

      {/* ── Hero Stats Row ── */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

        {/* NLP Score */}
        <div
          className="p-5 border-2 border-black rounded-[10px]"
          style={{ background: scoreBg, boxShadow: '4px 4px 0 #000' }}
        >
          <div className="nb-section-label">NLP Polarity Score</div>
          <div className="text-5xl font-black text-black leading-none mt-2">
            {score > 0 ? `+${score.toFixed(2)}` : score.toFixed(2)}
          </div>
          <div className="mt-3">
            <span className="nb-badge-black">{scoreLabel}</span>
          </div>
          <p className="text-[10px] font-bold text-black/50 mt-2">VADER + TextBlob dual-model</p>
        </div>

        {/* Rating */}
        <div className="nb-card p-5">
          <div className="nb-section-label">Avg Customer Rating</div>
          <div className="text-5xl font-black text-black mt-2">
            {rating.toFixed(1)}
            <span className="text-2xl text-nb-muted">/5</span>
          </div>
          <div className="flex gap-1 mt-3">
            {[1, 2, 3, 4, 5].map((star) => (
              <div
                key={star}
                className="w-7 h-7 border-2 border-black rounded-nb flex items-center justify-center font-black text-xs"
                style={{ background: star <= Math.round(rating) ? "#FDE047" : "#E8E8E8" }}
              >
                ★
              </div>
            ))}
          </div>
          <p className="text-[10px] font-bold text-nb-muted mt-2">{totalReviews} reviews analyzed</p>
        </div>

        {/* Distribution */}
        <div className="nb-card p-5">
          <div className="nb-section-label">Sentiment Split</div>
          <div className="text-5xl font-black text-black mt-2">{positivePct}%</div>
          <p className="text-[10px] font-bold text-nb-muted">positive polarity</p>
          <div className="nb-progress-track mt-3">
            <div className="nb-progress-fill" style={{ width: `${positivePct}%`, background: '#4ADE80' }} />
          </div>
          <div className="flex justify-between mt-2 text-[9px] font-black">
            <span className="text-green-700">✓ POS: {dist.positive || 0}</span>
            <span className="text-red-600">✗ NEG: {dist.negative || 0}</span>
          </div>
        </div>

      </div>

      {/* ── Topic Drivers ── */}
      <div className="nb-card p-5">
        <div className="nb-section-label">Top NLP Topic Drivers</div>
        <div className="flex flex-wrap gap-2">
          {topPositive.slice(0, 5).map(([topic, count], i) => (
            <div
              key={i}
              className="flex items-center gap-1.5 border-2 border-black px-3 py-1 rounded-nb font-bold text-xs"
              style={{ background: "#4ADE80", boxShadow: "2px 2px 0 #000" }}
            >
              <span className="text-green-900 font-black">+</span>
              <span>{topic}</span>
              <span className="ml-1 w-5 h-5 border-2 border-black bg-white rounded-nb flex items-center justify-center font-black text-[9px]">
                {count}
              </span>
            </div>
          ))}
          {topNegative.slice(0, 4).map(([topic, count], i) => (
            <div
              key={i}
              className="flex items-center gap-1.5 border-2 border-black px-3 py-1 rounded-nb font-bold text-xs"
              style={{ background: "#F87171", boxShadow: "2px 2px 0 #000" }}
            >
              <span className="text-red-900 font-black">−</span>
              <span>{topic}</span>
              <span className="ml-1 w-5 h-5 border-2 border-black bg-white rounded-nb flex items-center justify-center font-black text-[9px]">
                {count}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* ── Verbatim Quotes ── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

        <div
          className="p-5 border-2 border-black rounded-[10px]"
          style={{ background: "#DCFCE7", boxShadow: "4px 4px 0 #000" }}
        >
          <div className="nb-section-label">Customer Praises</div>
          {praises.length === 0 ? (
            <p className="text-xs font-medium text-nb-muted italic">No specific praise quotes in this SKU sample.</p>
          ) : (
            <ul className="space-y-3">
              {praises.map((praise, i) => (
                <li
                  key={i}
                  className="border-2 border-black bg-white p-3 rounded-nb text-xs font-medium text-black"
                  style={{ boxShadow: "2px 2px 0 #000" }}
                >
                  <span className="text-green-700 font-black mr-1">✓</span>"{praise}"
                </li>
              ))}
            </ul>
          )}
        </div>

        <div
          className="p-5 border-2 border-black rounded-[10px]"
          style={{ background: "#FEE2E2", boxShadow: "4px 4px 0 #000" }}
        >
          <div className="nb-section-label">Friction Points</div>
          {complaints.length === 0 ? (
            <p className="text-xs font-medium text-nb-muted italic">No complaints recorded for this SKU.</p>
          ) : (
            <ul className="space-y-3">
              {complaints.map((complaint, i) => (
                <li
                  key={i}
                  className="border-2 border-black bg-white p-3 rounded-nb text-xs font-medium text-black"
                  style={{ boxShadow: "2px 2px 0 #000" }}
                >
                  <span className="text-red-600 font-black mr-1">⚠</span>"{complaint}"
                </li>
              ))}
            </ul>
          )}
        </div>

      </div>
    </div>
  );
}
