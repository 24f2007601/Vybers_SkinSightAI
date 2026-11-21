import React from "react";

export default function Topbar({ selectedProduct, isLoading }) {
  return (
    <header
      className="h-14 flex items-center justify-between px-6 flex-shrink-0 bg-white border-b-2 border-black"
      style={{ boxShadow: '0 2px 0 #000' }}
    >
      {/* Left: search mockup */}
      <div
        className="flex items-center gap-2 px-3 py-1.5 bg-nb-bg border-2 border-black rounded-nb text-xs font-medium text-nb-muted cursor-text"
        style={{ boxShadow: '2px 2px 0 #000', minWidth: 220 }}
      >
        <svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
          <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
        </svg>
        <span>Search intelligence…</span>
      </div>

      {/* Right */}
      <div className="flex items-center gap-3">
        {isLoading ? (
          <span
            className="flex items-center gap-2 px-3 py-1 font-black text-[11px] border-2 border-black rounded-nb bg-nb-yellow text-black"
            style={{ boxShadow: '2px 2px 0 #000' }}
          >
            <span className="w-3 h-3 border-2 border-black rounded-full animate-spin" style={{ borderTopColor: 'transparent' }} />
            ANALYZING…
          </span>
        ) : (
          <span
            className="flex items-center gap-2 px-3 py-1 font-black text-[11px] border-2 border-black rounded-nb bg-nb-green text-black"
            style={{ boxShadow: '2px 2px 0 #000' }}
          >
            <span className="w-2 h-2 rounded-full bg-green-700" />
            LIVE
          </span>
        )}

        {/* Brand chip */}
        <div
          className="flex items-center gap-2 px-3 py-1.5 font-black text-xs border-2 border-black rounded-nb text-white"
          style={{ background: '#FF4081', boxShadow: '3px 3px 0 #000' }}
        >
          <div className="w-5 h-5 rounded-full border-2 border-white bg-white text-nb-pink flex items-center justify-center font-black text-[9px]"
            style={{ color: '#FF4081' }}>
            D
          </div>
          Dot & Key
        </div>
      </div>
    </header>
  );
}
