import { useState } from "react";

export default function MarketingContentStudio({ product, insights }) {
  const [contentType, setContentType] = useState("static_ad");
  const [platform, setPlatform] = useState("instagram");
  const [isGenerating, setIsGenerating] = useState(false);

  const contentTypes = [
    { value: "static_ad", label: "Static Ad" },
    { value: "product_description", label: "Product Description" },
    { value: "ad_script", label: "30s Ad Script" },
    { value: "storyboard", label: "7-Frame Storyboard" },
    { value: "video_concept", label: "Video Concept" },
    { value: "social_media_post", label: "Social Media Post" },
  ];

  const platforms = [
    { value: "instagram", label: "Instagram" },
    { value: "facebook", label: "Facebook" },
    { value: "amazon", label: "Amazon" },
    { value: "video", label: "Video" },
    { value: "website", label: "Website" },
  ];

  const handleGenerate = async () => {
    setIsGenerating(true);
    // Would call API to generate content
    setIsGenerating(false);
  };

  return (
    <div className="space-y-6">
      {/* Content Type & Platform Selector */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-2">Content Type</h3>
          <div className="space-y-1">
            {contentTypes.map((ctype) => (
              <label key={ctype.value} className="flex items-center gap-2 px-3 py-1.5 rounded border border-transparent hover:border-[var(--color-border)] transition-colors cursor-pointer ${
                contentType === ctype.value ? "bg-[var(--color-primary)] text-white" : ""
              }">
                <input
                  type="radio"
                  name="content-type"
                  value={ctype.value}
                  checked={contentType === ctype.value}
                  className="hidden peer"
                  onChange={() => setContentType(ctype.value)}
                />
                <span>{ctype.label}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium text-[var(--color-muted)] uppercase tracking-wider mb-2">Platform</h3>
          <div className="space-y-1">
            {platforms.map((plat) => (
              <label key={plat.value} className="flex items-center gap-2 px-3 py-1.5 rounded border border-transparent hover:border-[var(--color-border)] transition-colors cursor-pointer ${
                platform === plat.value ? "bg-[var(--color-primary)] text-white" : ""
              }">
                <input
                  type="radio"
                  name="platform"
                  value={plat.value}
                  checked={platform === plat.value}
                  className="hidden peer"
                  onChange={() => setPlatform(plat.value)}
                />
                <span>{plat.label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {/* Generated Content Preview */}
      {isGenerating ? (
        <div className="min-h-[300px] flex items-center justify-center p-8">
          <span className="text-[var(--color-muted)]">Generating content...</span>
        </div>
      ) : (
        <div className="bg-[var(--color-surface)] border border-[var(--color-border)] rounded-lg p-6">
          <h3 className="text-sm font-medium text-[var(--color-primary)] uppercase tracking-wider mb-4">
            {contentType.replace("_", " ")} - {platform}
          </h3>

          <pre className="text-xs text-[var(--color-muted)] overflow-auto" style={{ maxHeight: '400px' }}>
            {/* Would render generated content here */}
            Generating {contentType} for {product?.name} on {platform}...
            • Brand voice: {product?.brand_guidelines?.brand_voice || "Dot & Key: friendly, scientific, empowering, transparent"}
            • Key message: {insights?.recommendations?.[0] || ""}
            • Target: {product?.skin_type?.join(", ") || "All skin types"}
            • CTA: Shop now at dotkey.in
          </pre>
        </div>
      )}

      {/* CTA Button */}
      <div className="flex justify-end">
        <button
          onClick={handleGenerate}
          className={`inline-flex items-center gap-2 rounded-md font-medium transition-colors ${
            isGenerating ? "opacity-50 cursor-not-allowed" : "bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary-hover)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)] focus-visible:ring-offset-2"
          }`}
          disabled={isGenerating}
        >
          {isGenerating ? "Generating..." : "Generate Content"}
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="animate-spin opacity-70">
            <circle cx="12" cy="12" r="10" strokeWidth="2" opacity="0.25"/>
          </svg>
        </button>
      </div>
    </div>
  );
}