import { BrowserRouter as Router, Routes, Route, Link, useRoutes } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProductSelector from "./components/ProductSelector";
import CompetitorBenchmarkingTab from "./components/CompetitorBenchmarkingTab";
import SentimentAnalysisTab from "./components/SentimentAnalysisTab";
import StrategicInsightsTab from "./components/StrategicInsightsTab";
import MarketingContentStudio from "./components/MarketingContentStudio";

function Home() {
  return (
    <div className="min-h-screen bg-[var(--color-background)] text-[var(--color-text)] font-poppins">
      <Navbar />

      <main className="max-w-[1400px] mx-auto p-4 pb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-[var(--color-primary)] mb-6">
          VYBERS SkinSight-AI
        </h1>
        <p className="text-[var(--color-muted)] text-lg mb-8">
          Market Intelligence, Competitor Benchmarking & Marketing Content Generation for Dot & Key
        </p>

        <ProductSelector
          initialProductId="product-1"
          onSelect={(id) => console.log("Product selected:", id)}
        />
      </main>
    </div>
  );
}

function ProductDetail({ productId }) {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[var(--color-background)] text-[var(--color-text)] font-poppins">
      <Navbar />

      <main className="max-w-[1400px] mx-auto p-4 pb-12">
        <nav className="mb-6" aria-label="breadcrumb">
          <ol className="flex list-none md:flexspace-between">
            <li>
              <Link to="/" className="text-[var(--color-text)] hover:text-[var(--color-primary)] transition-colors">
                Home
              </Link>
            </li>
            <li className="text-[var(--color-muted)]">Product Details</li>
          </ol>
        </nav>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <ProductSelector
            initialProductId={productId}
            onSelect={(id) => navigate(`/products/${id}`)}
          />

          {/* When product ID matches, show details */}
          {productId && (
            <div className="lg:col-span-2 space-y-6">
              <CompetitorBenchmarkingTab product={{ id: productId, name: `Product ${productId}` }} />
              <SentimentAnalysisTab product={{ id: productId, name: `Product ${productId}` }} reviews={[]} />
              <StrategicInsightsTab product={{ id: productId, name: `Product ${productId}` }} insights={{}} />
              <MarketingContentStudio product={{ id: productId, name: `Product ${productId}` }} insights={{}} />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products/:productId" element={<ProductDetail productId="product-1" />} />
      </Routes>
    </Router>
  );
}