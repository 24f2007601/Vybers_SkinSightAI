import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function ProductSelector({ initialProductId, onSelect }) {
  const [productId, setProductId] = useState(initialProductId);
  const navigate = useNavigate();

  const handleSelect = async (id) => {
    setProductId(id);
    if (onSelect) await onSelect(id);
    navigate(`/products/${id}`);
  };

  return (
    <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-4 shadow-sm">
      <h2 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-3">
        Select Product
      </h2>
      <div className="space-y-2">
        {/* Products would be populated from API */}
        <div className="p-3 hover:bg-[var(--color-primary)] rounded-lg cursor-pointer transition-colors select-none">
          <span className="font-medium text-[var(--color-text)]">Vitamin C + E Super Bright Face Wash</span>
          <span className="text-xs text-[var(--color-muted)]">₹395/100ml</span>
        </div>
        <div className="p-3 hover:bg-[var(--color-primary)] rounded-lg cursor-pointer transition-colors select-none">
          <span className="font-medium text-[var(--color-text)]">Watermelon Hydrating Sunscreen SPF 50</span>
          <span className="text-xs text-[var(--color-muted)]">₹595/50ml</span>
        </div>
        <div className="p-3 hover:bg-[var(--color-primary)] rounded-lg cursor-pointer transition-colors select-none">
          <span className="font-medium text-[var(--color-text)]">Niacinamide 10% + Zinc PCA Serum</span>
          <span className="text-xs text-[var(--color-muted)]">₹495/30ml</span>
        </div>
        <div className="p-3 hover:bg-[var(--color-primary)] rounded-lg cursor-pointer transition-colors select-none">
          <span className="font-medium text-[var(--color-text)]">Ceramide + Hyaluronic Acid Moisturizer</span>
          <span className="text-xs text-[var(--color-muted)]">₹545/50ml</span>
        </div>
        <div className="p-3 hover:bg-[var(--color-primary)] rounded-lg cursor-pointer transition-colors select-none">
          <span className="font-medium text-[var(--color-text)]">Retinol 0.3% + Bakuchiol Night Serum</span>
          <span className="text-xs text-[var(--color-muted)]">₹695/30ml</span>
        </div>
      </div>
    </div>
  );
}