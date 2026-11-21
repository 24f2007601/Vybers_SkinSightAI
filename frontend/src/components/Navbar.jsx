import React from "react";

export default function Navbar() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-[1400px] mx-auto px-4 md:px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-pink-500 flex items-center justify-center text-white font-bold text-sm shadow-sm">
            D&K
          </div>
          <div>
            <span className="text-base font-bold text-gray-900 tracking-tight">Dot & Key</span>
            <span className="text-xs text-gray-500 block leading-none mt-0.5">SkinSight-AI Intelligence Engine</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            FastAPI Connected
          </span>
          <span className="text-xs text-gray-400 hidden sm:inline">Port 8000</span>
        </div>
      </div>
    </header>
  );
}
