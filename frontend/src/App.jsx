import React, { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import Topbar from "./components/Topbar";
import ProductSelector from "./components/ProductSelector";
import CompetitorBenchmarkingTab from "./components/CompetitorBenchmarkingTab";
import SentimentAnalysisTab from "./components/SentimentAnalysisTab";
import StrategicInsightsTab from "./components/StrategicInsightsTab";
import MarketingContentStudio from "./components/MarketingContentStudio";
import { fetchProducts, fetchProductInsights, fetchProductContent } from "./services/api";

export default function App() {
  const [products, setProducts] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState("");
  const [insights, setInsights] = useState(null);
  const [contentDeck, setContentDeck] = useState(null);
  const [activeTab, setActiveTab] = useState("benchmarking");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadInitialData() {
      try {
        setIsLoading(true);
        const data = await fetchProducts();
        setProducts(data);
        if (data?.length > 0) setSelectedProductId(String(data[0].id));
      } catch {
        setError("Failed to connect to backend API. Is the server running on port 8000?");
      } finally {
        setIsLoading(false);
      }
    }
    loadInitialData();
  }, []);

  useEffect(() => {
    if (!selectedProductId) return;
    async function loadProductData() {
      try {
        setIsLoading(true);
        setError(null);
        const [insightsRes, contentRes] = await Promise.all([
          fetchProductInsights(selectedProductId),
          fetchProductContent(selectedProductId),
        ]);
        setInsights(insightsRes);
        setContentDeck(contentRes);
      } catch {
        setError("Could not retrieve insights for the selected product.");
      } finally {
        setIsLoading(false);
      }
    }
    loadProductData();
  }, [selectedProductId]);

  const selectedProduct = products.find((p) => String(p.id) === String(selectedProductId));

  const TABS = [
    { id: "benchmarking", label: "Competitor Benchmarking", icon: "📊" },
    { id: "sentiment",    label: "Sentiment Engine",       icon: "💬" },
    { id: "insights",     label: "Strategic SWOT & Switcher", icon: "🎯" },
    { id: "content",      label: "Creative Content Studio", icon: "⚡" },
  ];

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#E8E8E8] font-sans">
      {/* 1. Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        productName={selectedProduct?.name}
        category={selectedProduct?.category}
        isLoading={isLoading}
      />

      {/* 2. Middle Product Catalog Column */}
      <div className="w-[280px] h-screen flex-shrink-0 flex flex-col overflow-hidden">
        <ProductSelector
          products={products}
          selectedProductId={selectedProductId}
          onSelect={(id) => setSelectedProductId(String(id))}
        />
      </div>

      {/* 3. Main Workspace Area */}
      <div className="flex-1 h-screen flex flex-col overflow-hidden bg-[#EAE8E0]">
        <Topbar selectedProduct={selectedProduct} isLoading={isLoading} />

        {/* Content Workspace Scroll Area */}
        <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6">
          {/* Header Title & Tab Bar */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b-2 border-black">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] font-black uppercase tracking-widest px-2 py-0.5 rounded border border-black bg-yellow-300 text-black shadow-[1px_1px_0px_#000]">
                  AI INTELLIGENCE VIEW
                </span>
                <span className="text-xs font-bold text-gray-500">
                  {selectedProduct?.category} · ₹{selectedProduct?.price_inr}
                </span>
              </div>
              <h1 className="text-2xl md:text-3xl font-black text-black tracking-tight">
                {selectedProduct?.name || "Loading SKU Intelligence..."}
              </h1>
            </div>

            {/* Neobrutalism Tab Selector */}
            <div className="flex flex-wrap items-center gap-2 bg-white p-1.5 border-2 border-black rounded-xl shadow-[3px_3px_0px_#000]">
              {TABS.map((t) => {
                const isActive = activeTab === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => setActiveTab(t.id)}
                    className={`flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-extrabold rounded-lg border-2 border-black transition-all ${
                      isActive
                        ? "bg-[#FF4081] text-white shadow-[2px_2px_0px_#000] -translate-x-0.5 -translate-y-0.5"
                        : "bg-white text-black hover:bg-yellow-200"
                    }`}
                  >
                    <span>{t.icon}</span>
                    <span>{t.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-4 border-2 border-black rounded-lg bg-red-300 text-black font-extrabold text-sm shadow-[3px_3px_0px_#000]">
              ⚠️ {error}
            </div>
          )}

          {/* Loading Indicator */}
          {isLoading ? (
            <div className="min-h-[400px] flex flex-col items-center justify-center p-8 border-2 border-black rounded-2xl bg-white shadow-[6px_6px_0px_#000]">
              <div className="w-12 h-12 border-4 border-black border-t-[#FF4081] rounded-full animate-spin mb-4" />
              <div className="text-lg font-black text-black">Crunching Skincare Market Intelligence…</div>
              <div className="text-xs font-bold text-gray-500 mt-1">Extracting sentiment topics, price per ml, and counter-positioning angles</div>
            </div>
          ) : (
            <div className="space-y-6">
              {activeTab === "benchmarking" && (
                <CompetitorBenchmarkingTab
                  product={selectedProduct}
                  comparison={insights?.competitor_comparison}
                />
              )}
              {activeTab === "sentiment" && (
                <SentimentAnalysisTab
                  product={selectedProduct}
                  sentiment={insights?.sentiment}
                />
              )}
              {activeTab === "insights" && (
                <StrategicInsightsTab
                  product={selectedProduct}
                  insights={insights}
                />
              )}
              {activeTab === "content" && (
                <MarketingContentStudio
                  product={selectedProduct}
                  contentDeck={contentDeck?.content_pieces}
                />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
