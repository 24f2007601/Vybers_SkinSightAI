import React, { useState } from "react";

const NAV_ITEMS = [
  { id: "benchmarking", icon: "📊", label: "Competitor Intel" },
  { id: "sentiment",    icon: "💬", label: "Customer Voice" },
  { id: "insights",     icon: "🎯", label: "SWOT & Strategy" },
  { id: "content",      icon: "⚡", label: "Creative Studio" },
];

export default function Sidebar({ activeTab, onTabChange, productName, category, isLoading }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    const next = !isDarkMode;
    setIsDarkMode(next);
    if (next) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  };

  return (
    <aside
      className={`h-screen flex-shrink-0 flex flex-col border-r-4 border-black select-none z-20 transition-all duration-200 ${
        isCollapsed ? "w-[72px]" : "w-[260px]"
      } ${isDarkMode ? "bg-[#181820] text-white" : "bg-[#FFFDF9] text-black"}`}
    >
      {/* Brand Header */}
      <div className={`p-3.5 border-b-4 border-black flex items-center justify-between ${isDarkMode ? "bg-[#21212B]" : "bg-[#FFE6EE]"}`}>
        <div className="flex items-center gap-2.5 overflow-hidden">
          <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center font-black text-sm text-black border-2 border-black rounded-lg shadow-[3px_3px_0px_#000] bg-[#FF4081]">
            D&K
          </div>
          {!isCollapsed && (
            <div className="truncate">
              <div className="text-sm font-black tracking-wide flex items-center gap-1.5">
                SkinSight
                <span className="text-[9px] px-1.5 py-0.2 bg-[#FF4081] text-white border-2 border-black font-black rounded shadow-[1px_1px_0px_#000]">
                  AI
                </span>
              </div>
              <div className={`text-[10px] font-black uppercase tracking-wider ${isDarkMode ? "text-gray-400" : "text-gray-600"}`}>
                Dot & Key Intel
              </div>
            </div>
          )}
        </div>

        {/* Action Controls: Small Theme Toggle & Retract Button */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={toggleTheme}
            title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
            className={`w-7 h-7 flex-shrink-0 flex items-center justify-center border-2 border-black rounded-md text-xs shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-transform ${
              isDarkMode ? "bg-[#FFE600] text-black hover:bg-yellow-300" : "bg-white text-black hover:bg-gray-100"
            }`}
          >
            {isDarkMode ? "☀️" : "🌙"}
          </button>
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            className={`w-7 h-7 flex-shrink-0 flex items-center justify-center border-2 border-black rounded-md font-black text-xs shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 active:shadow-none transition-transform ${
              isDarkMode ? "bg-white text-black hover:bg-gray-200" : "bg-white text-black hover:bg-gray-100"
            }`}
          >
            {isCollapsed ? "»" : "«"}
          </button>
        </div>
      </div>

      {/* Navigation Menu */}
      <div className="px-2.5 pt-4 pb-2">
        {!isCollapsed && (
          <div className={`text-[10px] font-black uppercase tracking-widest px-2 mb-2 ${isDarkMode ? "text-gray-400" : "text-gray-500"}`}>
            MODULES
          </div>
        )}
        <nav className="space-y-2">
          {NAV_ITEMS.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                title={isCollapsed ? item.label : undefined}
                className={`w-full flex items-center ${isCollapsed ? "justify-center px-0 py-2.5" : "justify-between px-3 py-2.5"} font-black text-xs text-left border-2 border-black rounded-lg transition-transform ${
                  isActive
                    ? "bg-[#FF4081] text-white shadow-[3px_3px_0px_#000] -translate-x-0.5 -translate-y-0.5"
                    : isDarkMode
                    ? "bg-[#21212B] text-gray-200 hover:bg-[#2C2C3A] shadow-[2px_2px_0px_#000]"
                    : "bg-white text-black hover:bg-[#FFF0F5] shadow-[2px_2px_0px_#000]"
                }`}
              >
                <div className="flex items-center gap-2.5 truncate">
                  <span className="text-sm flex-shrink-0">{item.icon}</span>
                  {!isCollapsed && <span className="tracking-tight truncate">{item.label}</span>}
                </div>
              </button>
            );
          })}
        </nav>
      </div>

      <div className="flex-1" />

      {/* Active SKU Target Card */}
      {!isCollapsed ? (
        <div className={`p-3 m-2.5 border-2 border-black rounded-xl shadow-[4px_4px_0px_#000] ${isDarkMode ? "bg-[#21212B]" : "bg-white"}`}>
          <div className="flex items-center justify-between mb-1.5">
            <span className={`text-[9px] font-black uppercase tracking-wider ${isDarkMode ? "text-gray-400" : "text-gray-500"}`}>
              Target SKU
            </span>
            {isLoading && (
              <span className="text-[9px] font-black text-black bg-yellow-300 border border-black px-1.5 py-0.2 rounded shadow-[1px_1px_0px_#000] animate-pulse">
                SYNCING…
              </span>
            )}
          </div>
          {productName ? (
            <div>
              <div className="text-xs font-black leading-snug line-clamp-2 mb-1">
                {productName}
              </div>
              {category && (
                <span className="inline-block text-[9px] font-black uppercase px-2 py-0.5 rounded border border-black bg-[#FF4081] text-white shadow-[2px_2px_0px_#000]">
                  {category}
                </span>
              )}
            </div>
          ) : (
            <div className={`text-xs font-bold ${isDarkMode ? "text-gray-400" : "text-gray-500"}`}>Pick an SKU from the catalog</div>
          )}
        </div>
      ) : (
        <div className="p-2 flex justify-center">
          <div
            className="w-10 h-10 flex items-center justify-center font-black text-xs border-2 border-black rounded-lg shadow-[2px_2px_0px_#000] bg-[#FFE600]"
            title={productName || "Target SKU"}
          >
            SKU
          </div>
        </div>
      )}
    </aside>
  );
}
