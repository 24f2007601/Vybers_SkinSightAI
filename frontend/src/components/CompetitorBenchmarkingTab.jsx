import { useState, useEffect } from "react";

export default function CompetitorBenchmarkingTab({ product }) {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Would fetch competitor data from API
    const timeout = setTimeout(() => {
      setIsLoading(false);
    }, 500);
    return () => clearTimeout(timeout);
  }, [product]);

  if (isLoading) {
    return (
      <div className="min-h-[400px] flex items-center justify-center p-8">
        <span className="text-[var(--color-muted)]">Loading competitor data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-[400px] flex items-center justify-center p-8">
        <span className="text-red-500">Error: {error}</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Unit Economics Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Unit Economics</h3>
          <div className="space-y-3">
            <div>
              <span className="text-[var(--color-text)] font-medium">Dot & Key:</span>
              <span className="text-[var(--color-primary)] font-large">Rs. 3.95/ml</span>
            </div>
            <div>
              <span className="text-[var(--color-text)] font-medium">Minimalist:</span>
              <span className="text-[var(--color-teal)] font-large">Rs. 4.20/ml</span>
            </div>
            <div>
              <span className="text-[var(--color-text)] font-medium">The Derma Co:</span>
              <span className="text-[var(--color-teal)] font-large">Rs. 3.80/ml</span>
            </div>
          </div>
        </div>

        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Rating Comparison</h3>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span>Dot & Key</span>
              <span className="text-[var(--color-primary)]">4.4 ⭐</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Minimalist</span>
              <span className="text-[var(--color-teal)]">4.2 ⭐</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>The Derma Co</span>
              <span className="text-[var(--color-teal)]">4.3 ⭐</span>
            </div>
          </div>
        </div>
      </div>

      {/* Ingredient Badges Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Shared Ingredients</h3>
          <div className="space-y-2">
            <span className="inline-flex items-center gap-2 px-2 py-1 bg-[var(--color-cream)] rounded text-[var(--color-text)] text-sm">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
              </svg>
              Hydrating agents
            </span>
            <span className="inline-flex items-center gap-2 px-2 py-1 bg-[var(--color-cream)] rounded text-[var(--color-text)] text-sm">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
              </svg>
              Brightening actives
            </span>
          </div>
        </div>

        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Unique Ingredients</h3>
          <div className="space-y-2">
            <span className="inline-flex items-center gap-2 px-2 py-1 bg-[var(--color-primary)] rounded text-[var(--color-white)] text-sm">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
              </svg>
              Ceramide Complex
            </span>
            <span className="inline-flex items-center gap-2 px-2 py-1 bg-[var(--color-primary)] rounded text-[var(--color-white)] text-sm">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
              </svg>
              Bakuchiol
            </span>
          </div>
        </div>
      </div>

      {/* Advantages/Gaps Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Competitive Advantages</h3>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
              <span>Dermatologically tested formulations</span>
            </li>
            <li className="flex items-start gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
              <span>Clean ingredients, no nasties</span>
            </li>
            <li className="flex items-start gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
              <span>Made for Indian skin</span>
            </li>
          </ul>
        </div>

        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Market Gaps</h3>
          <ul className="space-y-2 text-sm">
            <li className="flex items-start gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-teal)" strokeWidth="2">
                <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
              </svg>
              <span>Missing hyaluronic acid serums in budget range</span>
            </li>
            <li className="flex items-start gap-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-teal)" strokeWidth="2">
                <path d="M12 2v4l2 5h4l2-5h6l-5 2 5-2h4l-2 5h2l-5-2h-6l5-2-5 2H5z"/>
              </svg>
              <span>Fragrance-free options for sensitive skin</span>
            </li>
          </ul>
        </div>

        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">Price/ML Analysis</h3>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span>Dot & Key Face Wash</span>
              <span>Rs. 3.95/ml</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Minimalist Face Wash</span>
              <span>Rs. 4.20/ml</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>The Derma Co Face Wash</span>
              <span>Rs. 3.80/ml</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Plum Face Wash</span>
              <span>Rs. 4.50/ml</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}