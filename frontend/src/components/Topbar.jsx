import React from "react";

export default function Topbar({ selectedProduct, isLoading }) {
  return (
    <header className="h-16 flex items-center justify-between px-6 bg-white border-b-2 border-black flex-shrink-0 shadow-[0_2px_0px_#000] z-10">
      {/* Left: Product context banner */}
      <div className="flex items-center gap-3">
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-[#FFF4F7] border-2 border-black rounded-lg shadow-[2px_2px_0px_#000]">
          <span className="w-2.5 h-2.5 rounded-full bg-[#FF4081]"></span>
          <span className="text-xs font-black text-black">DOT & KEY RESEARCH</span>
        </div>
        <div className="text-xs font-bold text-gray-500">
          Viewing: <span className="text-black font-extrabold">{selectedProduct?.name || "Choose Product"}</span>
        </div>
      </div>

      {/* Right: Interactive badges */}
      <div className="flex items-center gap-3">
        {isLoading ? (
          <div className="flex items-center gap-2 px-3 py-1.5 border-2 border-black rounded-lg bg-yellow-300 text-black font-black text-xs shadow-[2px_2px_0px_#000]">
            <div className="w-3.5 h-3.5 border-2 border-black border-t-transparent rounded-full animate-spin" />
            ANALYZING BENCHMARKS…
          </div>
        ) : (
          <div className="flex items-center gap-2 px-3 py-1.5 border-2 border-black rounded-lg bg-emerald-300 text-black font-black text-xs shadow-[2px_2px_0px_#000]">
            <span className="w-2 h-2 rounded-full bg-black"></span>
            REAL-TIME INTEL SYNCED
          </div>
        )}
      </div>
    </header>
  );
}
