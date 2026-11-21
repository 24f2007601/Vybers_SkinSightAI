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

  const PAGE_TITLES = {
    benchmarking: "Competitor Benchmarking",
    sentiment:    "Customer Sentiment Analysis",
    insights:     "Strategic Insights & SWOT",
    content:      "Creative Content Studio",
  };

  return (
    <div className="flex h-screen overflow-hidden">

      {/* 1. Left sidebar — black, always visible */}
      <Sidebar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        productName={selectedProduct?.name}
        category={selectedProduct?.category}
        isLoading={isLoading}
      />

      {/* 2. Product picker column */}
      <div className="w-[240px] flex-shrink-0 flex flex-col overflow-hidden border-r-2 border-black">
        <div
          className="h-14 flex items-center px-4 bg-white border-b-2 border-black"
          style={{ boxShadow: '0 2px 0 #000' }}
        >
          <span className="text-[9px] font-black uppercase tracking-widest text-nb-muted">Product Catalog</span>
        </div>
        <div className="flex-1 overflow-hidden">
          <ProductSelector
            products={products}
            selectedProductId={selectedProductId}
            onSelect={(id) => setSelectedProductId(String(id))}
          />
        </div>
      </div>

      {/* 3. Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden">

        {/* Topbar */}
        <Topbar selectedProduct={selectedProduct} isLoading={isLoading} />

        {/* Scroll area */}
        <div className="flex-1 overflow-y-auto p-6" style={{ background: '#E8E8E8' }}>

          {/* Page header */}
          <div className="mb-6">
            {/* Tab filter row — matches reference image style */}
            <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
              <div>
                <h1 className="text-xl font-black text-black">
                  {PAGE_TITLES[activeTab]}
                </h1>
                {selectedProduct && (
                  <p className="text-xs font-medium text-nb-muted mt-0.5">
                    {selectedProduct.name} &nbsp;·&nbsp;
                    {selectedProduct.category} &nbsp;·&nbsp;
                    ₹{selectedProduct.price_inr} &nbsp;·&nbsp;
                    {selectedProduct.size_ml}ml
                  </p>
                )}
              </div>

              {/* Tab switcher — neobrutalism pills */}
              <div
                className="flex items-center gap-1 p-1 bg-white border-2 border-black rounded-[10px]"
                style={{ boxShadow: '3px 3px 0 #000' }}
              >
                {[
                  { id: "benchmarking", label: "Benchmarks" },
                  { id: "sentiment",    label: "Sentiment" },
                  { id: "insights",     label: "SWOT" },
                  { id: "content",      label: "Content" },
                ].map((t) => (
                  <button
                    key={t.id}
                    onClick={() => setActiveTab(t.id)}
                    className="px-3 py-1.5 text-xs font-bold border-2 border-black rounded-nb transition-all duration-100"
                    style={
                      activeTab === t.id
                        ? { background: '#FF4081', color: '#fff', boxShadow: '2px 2px 0 #000', transform: 'translate(-1px,-1px)' }
                        : { background: 'transparent', color: '#000' }
                    }
                    onMouseEnter={(e) => { if (activeTab !== t.id) e.currentTarget.style.background = '#FFD6E5'; }}
                    onMouseLeave={(e) => { if (activeTab !== t.id) e.currentTarget.style.background = 'transparent'; }}
                  >
                    {t.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Error banner */}
            {error && (
              <div className="nb-alert-error mb-4 text-xs font-bold">
                <span>⚠</span>
                <span>{error}</span>
              </div>
            )}
          </div>

          {/* Loading state */}
          {isLoading ? (
            <div
              className="nb-card flex flex-col items-center justify-center h-64 bg-nb-yellow"
              style={{ background: '#FDE047' }}
            >
              <div className="w-10 h-10 border-4 border-black rounded-full animate-spin mb-4"
                style={{ borderTopColor: '#FF4081' }} />
              <p className="text-sm font-black text-black">Running Market Intelligence Pipeline…</p>
              <p className="text-xs font-medium text-nb-muted mt-1">
                Benchmarking · Sentiment · SWOT · Acquisition
              </p>
            </div>
          ) : (
            <div>
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
