import React from "react";

const NAV_ITEMS = [
  { id: "benchmarking", icon: "▤", label: "Competitors & Pricing" },
  { id: "sentiment",    icon: "◎", label: "Customer Sentiment" },
  { id: "insights",     icon: "◈", label: "SWOT & Acquisition" },
  { id: "content",      icon: "✦", label: "Creative Studio" },
];

export default function Sidebar({ activeTab, onTabChange, productName, category, isLoading }) {
  return (
    <aside className="w-[220px] min-h-screen flex-shrink-0 flex flex-col bg-black select-none">

      {/* Logo */}
      <div className="px-5 py-5 border-b-2 border-white/10">
        <div className="flex items-center gap-3">
          <div
            className="w-9 h-9 flex items-center justify-center font-black text-xs text-white border-2 border-white rounded-nb"
            style={{ background: '#FF4081', boxShadow: '3px 3px 0 rgba(255,255,255,0.2)' }}
          >
            D&K
          </div>
          <div>
            <div className="text-sm font-black text-white leading-none tracking-tight">SkinSight-AI</div>
            <div className="text-[10px] font-medium text-white/40 mt-0.5">Intelligence Engine</div>
          </div>
        </div>
      </div>

      {/* Nav */}
      <div className="px-4 pt-5 pb-2">
        <div className="text-[9px] font-black uppercase tracking-widest text-white/25 mb-3">PAGES</div>
        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className="w-full flex items-center gap-3 px-3 py-2.5 font-bold text-xs text-left transition-all duration-100 rounded-nb border-2"
                style={
                  isActive
                    ? {
                        background: '#FF4081',
                        borderColor: '#FF4081',
                        color: '#fff',
                        boxShadow: '3px 3px 0 rgba(255,64,129,0.5)',
                        transform: 'translate(-1px,-1px)',
                      }
                    : {
                        background: 'transparent',
                        borderColor: 'transparent',
                        color: 'rgba(255,255,255,0.45)',
                      }
                }
                onMouseEnter={e => { if (!isActive) { e.currentTarget.style.background = 'rgba(255,255,255,0.07)'; e.currentTarget.style.color = '#fff'; } }}
                onMouseLeave={e => { if (!isActive) { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = 'rgba(255,255,255,0.45)'; } }}
              >
                <span className="text-sm">{item.icon}</span>
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="flex-1" />

      {/* Active SKU widget */}
      <div className="px-4 pb-5">
        <div className="text-[9px] font-black uppercase tracking-widest text-white/25 mb-2">ACTIVE SKU</div>
        {productName ? (
          <div className="border-2 border-white/15 rounded-nb p-3 bg-white/5">
            <div className="text-xs font-bold text-white leading-snug mb-2">{productName}</div>
            {category && (
              <span className="inline-block text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-nb border border-white/20 text-white/60">
                {category}
              </span>
            )}
            <div className="flex items-center gap-1.5 mt-2.5">
              {isLoading ? (
                <>
                  <div className="w-1.5 h-1.5 rounded-full bg-nb-yellow animate-pulse" />
                  <span className="text-[9px] font-black text-nb-yellow">ANALYZING…</span>
                </>
              ) : (
                <>
                  <div className="w-1.5 h-1.5 rounded-full bg-nb-green" style={{ boxShadow: '0 0 6px #4ADE80' }} />
                  <span className="text-[9px] font-black text-nb-green">LIVE DATA</span>
                </>
              )}
            </div>
          </div>
        ) : (
          <p className="text-[10px] text-white/30">Select a product →</p>
        )}
      </div>
    </aside>
  );
}
