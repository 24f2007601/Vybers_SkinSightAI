import { useState, useEffect } from "react";

export default function SentimentAnalysisTab({ product, reviews }) {
  const [isLoading, setIsLoading] = useState(true);
  const [sentimentScore, setSentimentScore] = useState(0);
  const [distribution, setDistribution] = useState({});
  const [topPraises, setTopPraises] = useState([]);
  const [topComplaints, setTopComplaints] = useState([]);

  useEffect(() => {
    // Would fetch sentiment analysis from API
    const timeout = setTimeout(() => {
      setIsLoading(false);
      setSentimentScore(0.72);
      setDistribution({
        positive: 9,
        neutral: 2,
        negative: 1,
      });
      setTopPraises(["lightweight non-sticky texture", "instant hydration", "gentle on skin"]);
      setTopComplaints(["mild fragrance irritation", "white cast on deep skin"]);
    }, 500);
    return () => clearTimeout(timeout);
  }, [product, reviews]);

  if (isLoading) {
    return (
      <div className="min-h-[400px] flex items-center justify-center p-8">
        <span className="text-[var(--color-muted)]">Loading sentiment analysis...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Sentiment Gauge */}
      <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
        <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-4">
          Sentiment Overview
        </h3>

        <div className="relative h-64">
          {/* Gauge background */}
          <div className="absolute inset-0 bg-[var(--color-surface2)] rounded-full overflow-hidden">
            <div
              className="absolute top-1/2 -translate-y-1/2 left-2 w-2 h-2 rounded-full bg-[var(--color-primary)]"
              style={{ width: `${sentimentScore * 2 + 10}%` }}
            ></div>
          </div>

          {/* Labels */}
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 text-xs text-[var(--color-muted)]">
            {sentimentScore > 0.6 && "Positive"}
            {sentimentScore > 0.3 && "Neutral"}
            {sentimentScore <= 0.3 && "Negative"}
          </div>
        </div>
      </div>

      {/* Topic Distribution Pills */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
        {["texture", "fragrance", "effectiveness", "gentleness", "hydration", "oil_control", "brightening", "anti_aging"].map((topic) => {
          const count = distribution[topic] || 0;
          const isPositive = topic !== "fragrance" && topic !== "white_cast";
          return (
            <div
              key={topic}
              className={`flex items-center gap-2 px-2 py-1 rounded text-xs ${
                isPositive ? `bg-[var(--color-cream)] text-[var(--color-primary)]` : `bg-[var(--color-surface2)] text-[var(--color-muted)]`
              }`}
            >
              <span className="w-1 h-1 rounded-full bg-current mr-1"
                    style={{ backgroundColor: isPositive ? 'var(--color-primary)' : 'var(--color-muted)' }} />
              <span>{topic}</span>
              <span className="ml-2">{count}</span>
            </div>
          );
        })}
      </div>

      {/* Praises & Complaints */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Top Praises</h3>
          <ul className="space-y-2 text-sm">
            {topPraises.map((praise, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
                <span>{praise}</span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Top Complaints</h3>
          <ul className="space-y-2 text-sm">
            {topComplaints.map((complaint, i) => (
              <li key={i} className="flex items-start gap-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-teal)" strokeWidth="2">
                  <path d="M18 6L9 17l-5 5"/>
                </svg>
                <span>{complaint}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}