import React, { useState } from "react";

const PLATFORM_COLORS = {
  instagram: "#FF4081",
  facebook:  "#60A5FA",
  amazon:    "#FB923C",
  video:     "#C084FC",
  website:   "#4ADE80",
};

export default function MarketingContentStudio({ product, contentDeck }) {
  const pieces = contentDeck || {};
  const pieceKeys = Object.keys(pieces);
  const [selectedKey, setSelectedKey] = useState(pieceKeys[0] ?? "");
  const [copied, setCopied] = useState(false);

  if (pieceKeys.length === 0) {
    return (
      <div className="nb-card p-10 text-center">
        <p className="font-bold text-nb-muted">No marketing assets generated for this SKU.</p>
      </div>
    );
  }

  if (!selectedKey && pieceKeys.length > 0) setSelectedKey(pieceKeys[0]);

  const activePiece = pieces[selectedKey] ?? pieces[pieceKeys[0]];
  const platformColor = PLATFORM_COLORS[activePiece?.platform] ?? "#FF4081";

  const handleCopy = () => {
    if (activePiece?.content) {
      navigator.clipboard.writeText(activePiece.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-6">

      {/* ── Archetype Selector ── */}
      <div>
        <div className="nb-section-label">
          Ready-to-Deploy Marketing Archetypes ({pieceKeys.length} generated)
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {pieceKeys.map((key) => {
            const piece = pieces[key];
            const isSelected = selectedKey === key;
            const pc = PLATFORM_COLORS[piece.platform] ?? "#FF4081";
            return (
              <button
                key={key}
                onClick={() => setSelectedKey(key)}
                className="text-left p-3 border-2 border-black rounded-[10px] transition-all duration-100 font-bold text-xs"
                style={{
                  background: isSelected ? pc : "#fff",
                  boxShadow: isSelected ? "3px 3px 0 #000" : "2px 2px 0 #000",
                  transform: isSelected ? "translate(-1px,-1px)" : "translate(0,0)",
                  color: isSelected ? "#fff" : "#000",
                }}
                onMouseEnter={e => { if (!isSelected) { e.currentTarget.style.background = "#F3F4F6"; e.currentTarget.style.transform = "translate(-1px,-1px)"; e.currentTarget.style.boxShadow = "3px 3px 0 #000"; } }}
                onMouseLeave={e => { if (!isSelected) { e.currentTarget.style.background = "#fff"; e.currentTarget.style.transform = "translate(0,0)"; e.currentTarget.style.boxShadow = "2px 2px 0 #000"; } }}
              >
                <div className="capitalize truncate">{piece.type?.replace(/_/g, " ")}</div>
                <div className={`text-[10px] mt-0.5 capitalize font-medium ${isSelected ? "text-white/70" : "text-nb-muted"}`}>
                  {piece.platform}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Asset Preview ── */}
      {activePiece && (
        <div className="nb-card overflow-hidden">

          {/* Card header */}
          <div
            className="px-5 py-4 border-b-2 border-black flex flex-wrap items-center justify-between gap-3"
            style={{ background: platformColor }}
          >
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="nb-badge bg-black text-white border-black text-[9px]">
                  {activePiece.platform?.toUpperCase()}
                </span>
                <span className="text-xs font-bold text-white/80 capitalize">
                  {activePiece.type?.replace(/_/g, " ")}
                </span>
              </div>
              <h2 className="text-sm font-black text-black leading-snug">
                {activePiece.title}
              </h2>
            </div>

            <button
              onClick={handleCopy}
              className="nb-btn bg-black text-white text-xs px-4 py-2"
              style={{ boxShadow: "3px 3px 0 rgba(0,0,0,0.3)" }}
            >
              {copied ? "✓ Copied!" : "📋 Copy Copy"}
            </button>
          </div>

          {/* Metadata row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-0 border-b-2 border-black divide-x-2 divide-black">
            <div className="px-4 py-3">
              <div className="text-[9px] font-black uppercase tracking-widest text-nb-muted mb-1">Format</div>
              <div className="text-xs font-bold text-black">
                {activePiece.format_specs?.dimensions ?? "Multi-format"}
                {activePiece.format_specs?.aspect_ratio && ` · ${activePiece.format_specs.aspect_ratio}`}
              </div>
            </div>
            <div className="px-4 py-3">
              <div className="text-[9px] font-black uppercase tracking-widest text-nb-muted mb-1">Target Audience</div>
              <div className="text-xs font-bold text-black line-clamp-1">
                {activePiece.target_audience ?? "Urban Indian consumers 18–35"}
              </div>
            </div>
            <div className="px-4 py-3">
              <div className="text-[9px] font-black uppercase tracking-widest text-nb-muted mb-1">Call to Action</div>
              <div className="text-xs font-black" style={{ color: "#FF4081" }}>
                {activePiece.cta ?? "Shop on dotkey.in"}
              </div>
            </div>
          </div>

          {/* Copy body */}
          <div className="p-5">
            <div className="text-[9px] font-black uppercase tracking-widest text-nb-muted mb-3">
              Generated Creative Copy
            </div>
            <pre
              className="p-4 border-2 border-black rounded-nb text-xs font-mono whitespace-pre-wrap leading-relaxed overflow-auto text-green-300 max-h-[420px]"
              style={{ background: "#0D1117", boxShadow: "inset 2px 2px 0 rgba(0,0,0,0.3)" }}
            >
              {activePiece.content}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
