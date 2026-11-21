/**
 * API Client Service connecting React frontend to FastAPI backend
 */

const BASE_URL = "/api/v1";

export async function fetchProducts() {
  const res = await fetch(`${BASE_URL}/products`);
  if (!res.ok) {
    throw new Error(`Failed to fetch products: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchProductById(productId) {
  const res = await fetch(`${BASE_URL}/products/${productId}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch product details: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchProductInsights(productId) {
  const res = await fetch(`${BASE_URL}/products/${productId}/insights`);
  if (!res.ok) {
    throw new Error(`Failed to fetch insights: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchProductContent(productId) {
  const res = await fetch(`${BASE_URL}/products/${productId}/content`);
  if (!res.ok) {
    throw new Error(`Failed to fetch marketing content: ${res.statusText}`);
  }
  return res.json();
}
