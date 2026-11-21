import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-[var(--color-cream)] border-b border-[var(--color-border)] sticky top-0 z-50">
      <div className="max-w-[1400px] mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl font-bold text-[var(--color-primary)]">Dot & Key</span>
            <span className="text-base text-[var(--color-muted)]">Clean. Conscious. Effective.</span>
          </Link>
        </div>

        <div className="hidden md:flex items-center gap-8">
          <Link to="/products" className="text-[var(--color-text)] hover:text-[var(--color-primary)] transition-colors font-medium">Products</Link>
          <Link to="/insights" className="text-[var(--color-text)] hover:text-[var(--color-primary)] transition-colors font-medium">Insights</Link>
          <Link to="/content" className="text-[var(--color-text)] hover:text-[var(--color-primary)] transition-colors font-medium">Content Studio</Link>
        </div>

        <button className="md:hidden flex items-center gap-2 p-2 hover:bg-[var(--color-surface)] rounded-lg transition-colors" aria-label="Open menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
      </div>
    </nav>
  );
}