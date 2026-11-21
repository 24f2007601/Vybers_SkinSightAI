# src/data/__init__.py
# Makes src/data a Python package and re-exports the public loader API.

from .loader import (  # noqa: F401
    SAMPLE_COMPETITOR_BRANDS,
    SAMPLE_COMPETITOR_PRODUCTS,
    SAMPLE_DOTKEY_PRODUCTS,
    SAMPLE_REVIEWS,
    load_competitor_products,
    load_dotkey_products,
    load_reviews,
)
