import React, { useState } from "react";

export default function ProductSelector({ products = [], selectedProductId, onSelect }) {
  const [search, setSearch] = useState("");

  const filtered = products.filter(
    (p) =>
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      (p.category && p.category.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="flex flex-col h-full bg-white border-r-2 border-black">
      {/* Header */}
      <div className="px-3 py-3 border-b-2 border-black bg-nb-bg">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[9px] font-black uppercase tracking-widest text-nb-muted">SKU Catalog</span>
          <span className="nb-badge-pink text-[9px]">{products.length}</span>
        </div>
        <input
          type="text"
          placeholder="Filter products…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="nb-input text-xs py-1.5"
        />
      </div>

      {/* Product List */}
      <div className="flex-1 overflow-y-auto divide-y-2 divide-black">
        {filtered.map((p, idx) => {
          const isSelected = String(p.id) === String(selectedProductId);
          return (
            <button
              key={p.id}
              onClick={() => onSelect(p.id)}
              className="w-full text-left px-3 py-3 transition-colors duration-100"
              style={{ background: isSelected ? '#FF4081' : idx % 2 === 0 ? '#fff' : '#fafafa' }}
              onMouseEnter={(e) => { if (!isSelected) e.currentTarget.style.background = '#FFD6E5'; }}
              onMouseLeave={(e) => { if (!isSelected) e.currentTarget.style.background = idx % 2 === 0 ? '#fff' : '#fafafa'; }}
            >
              <div className="flex items-start justify-between gap-2">
                <span className={`text-xs font-bold leading-snug line-clamp-2 ${isSelected ? 'text-white' : 'text-black'}`}>
                  {p.name}
                </span>
                <span className={`text-[10px] font-black shrink-0 mt-0.5 ${isSelected ? 'text-white' : 'text-black'}`}>
                  ₹{p.price_inr}
                </span>
              </div>
              <div className="flex items-center gap-1.5 mt-1.5">
                <span
                  className={`text-[9px] font-bold uppercase px-1.5 py-0.5 border rounded-nb ${
                    isSelected ? 'border-white/40 text-white/80 bg-white/10' : 'border-black text-black'
                  }`}
                >
                  {p.category}
                </span>
                {p.size_ml > 0 && (
                  <span className={`text-[9px] font-medium ${isSelected ? 'text-white/70' : 'text-nb-muted'}`}>
                    {p.size_ml}ml
                  </span>
                )}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
