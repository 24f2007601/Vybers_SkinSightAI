import React from "react";

const NAV_ITEMS = [
  { id: "benchmarking", icon: "📊", label: "Competitor Intel", tag: "Live" },
  { id: "sentiment",    icon: "💬", label: "Customer Voice", tag: "NLP" },
  { id: "insights",     icon: "🎯", label: "SWOT & Strategy", tag: "AI" },
  { id: "content",      icon: "⚡", label: "Creative Studio", tag: "9 Decks" },
];

export default function Sidebar({ activeTab, onTabChange, productName, category, isLoading }) {
  return (
    <aside className="w-[240px] h-screen flex-shrink-0 flex flex-col bg-[#0F0F12] border-r-2 border-black select-none z-20">

      {/* Brand Header */}
      <div className="p-4 border-b-2 border-black bg-[#16161B] flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div
            className="w-10 h-10 flex items-center justify-center font-black text-sm text-black border-2 border-black rounded-lg shadow-[2px_2px_0px_#000]"
            style={{ background: "#FF4081" }}
          >
            D&K
          </div>
          <div>
            <div className="text-sm font-black text-white tracking-wide flex items-center gap-1.5">
              SkinSight
              <span className="text-[9px] px-1.5 py-0.2 bg-[#FF4081] text-white border border-black font-extrabold rounded">AI</span>
            </div>
            <div className="text-[10px] font-bold text-gray-400">Dot & Key Intelligence</div>
          </div>
        </div>
      </div>

      {/* Navigation Menu */}
      <div className="px-3 pt-5 pb-2">
        <div className="text-[10px] font-black uppercase tracking-widest text-gray-400 px-3 mb-2.5 flex items-center justify-between">
          <span>INTELLIGENCE MODULES</span>
        </div>
        <nav className="space-y-1.5">
          {NAV_ITEMS.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 font-bold text-xs text-left transition-all duration-100 border-2 rounded-lg ${
                  isActive
                    ? "bg-[#FF4081] text-white border-black shadow-[3px_3px_0px_#000] -translate-x-0.5 -translate-y-0.5"
                    : "bg-[#16161B] text-gray-300 border-transparent hover:border-black hover:bg-[#202028] hover:text-white"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className="text-sm">{item.icon}</span>
                  <span className="font-extrabold tracking-tight">{item.label}</span>
                </div>
                <span
                  className={`text-[9px] font-black px-1.5 py-0.5 rounded border ${
                    isActive
                      ? "bg-black text-white border-white/20"
                      : "bg-[#252530] text-gray-400 border-black/50"
                  }`}
                >
                  {item.tag}
                </span>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="flex-1" />

      {/* Active SKU Card */}
      <div className="p-3 m-3 bg-[#181820] border-2 border-black rounded-xl shadow-[3px_3px_0px_#000]">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[9px] font-black uppercase tracking-wider text-gray-400">Target Product</span>
          {isLoading ? (
            <span className="flex items-center gap-1 text-[9px] font-black text-yellow-400 bg-yellow-400/10 px-1.5 py-0.5 rounded border border-yellow-400/30">
              <span className="w-1.5 h-1.5 rounded-full bg-yellow-400 animate-pulse" />
              COMPUTING
            </span>
          ) : (
            <span className="flex items-center gap-1 text-[9px] font-black text-emerald-400 bg-emerald-400/10 px-1.5 py-0.5 rounded border border-emerald-400/30">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              LIVE ENGINE
            </span>
          )}
        </div>
        
        {productName ? (
          <div>
            <div className="text-xs font-black text-white leading-snug line-clamp-2 mb-1.5">
              {productName}
            </div>
            {category && (
              <span className="inline-block text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded bg-[#FF4081]/20 text-[#FF4081] border border-[#FF4081]/30">
                {category}
              </span>
            )}
          </div>
        ) : (
          <div className="text-xs text-gray-400 font-bold">Pick an SKU from the catalog</div>
        )}
      </div>

      {/* Bottom Status bar */}
      <div className="p-3 bg-[#111116] border-t-2 border-black flex items-center justify-between text-[10px] text-gray-400 font-bold">
        <span>FastAPI Engine</span>
        <span className="text-emerald-400 font-black">Online (8000)</span>
      </div>
    </aside>
  );
}
