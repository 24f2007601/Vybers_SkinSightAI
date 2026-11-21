import React, { useState } from "react";

export default function ProductSelector({ products = [], selectedProductId, onSelect }) {
  const [search, setSearch] = useState("");

  const filtered = products.filter(
    (p) =>
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      (p.category && p.category.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="flex flex-col h-full bg-[#FAF9F5] border-r-2 border-black">
      {/* Header */}
      <div className="p-3 border-b-2 border-black bg-white">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-1.5">
            <span className="text-xs font-black uppercase tracking-wider text-black">SKU Catalog</span>
            <span className="text-[10px] font-black px-1.5 py-0.2 rounded border border-black bg-yellow-300 text-black shadow-[1px_1px_0px_#000]">
              {products.length}
            </span>
          </div>
          <span className="text-[10px] font-bold text-gray-400">Dot & Key</span>
        </div>
        
        <div className="relative">
          <input
            type="text"
            placeholder="Search SKUs or categories…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 bg-[#FFF4F7] border-2 border-black rounded-md text-xs font-bold text-black placeholder:text-gray-400 shadow-[2px_2px_0px_#000] focus:outline-none focus:bg-white"
          />
          <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-xs">🔍</span>
        </div>
      </div>

      {/* Product List */}
      <div className="flex-1 overflow-y-auto divide-y-2 divide-black p-2 space-y-1.5">
        {filtered.map((p) => {
          const isSelected = String(p.id) === String(selectedProductId);
          return (
            <button
              key={p.id}
              onClick={() => onSelect(p.id)}
              className={`w-full text-left p-3 border-2 border-black rounded-lg transition-all duration-100 ${
                isSelected
                  ? "bg-[#FF4081] text-white shadow-[3px_3px_0px_#000] -translate-x-0.5 -translate-y-0.5"
                  : "bg-white text-black shadow-[2px_2px_0px_#000] hover:bg-pink-50 hover:-translate-y-0.5"
              }`}
            >
              <div className="flex items-start justify-between gap-1.5">
                <span className={`text-xs font-black leading-snug line-clamp-2 ${isSelected ? "text-white" : "text-black"}`}>
                  {p.name}
                </span>
                <span
                  className={`text-[11px] font-extrabold px-1.5 py-0.5 rounded border border-black shrink-0 ${
                    isSelected ? "bg-black text-white" : "bg-yellow-300 text-black shadow-[1px_1px_0px_#000]"
                  }`}
                >
                  ₹{p.price_inr}
                </span>
              </div>

              <div className="flex items-center gap-1.5 mt-2">
                <span
                  className={`text-[9px] font-black uppercase px-1.5 py-0.5 rounded border ${
                    isSelected
                      ? "bg-white text-black border-black"
                      : "bg-[#F0EFF5] text-black border-black"
                  }`}
                >
                  {p.category}
                </span>
                {p.size_ml > 0 && (
                  <span className={`text-[10px] font-bold ${isSelected ? "text-white/80" : "text-gray-500"}`}>
                    {p.size_ml} ml
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
