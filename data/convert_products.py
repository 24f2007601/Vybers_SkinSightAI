import json
import csv
import re
from pathlib import Path

data_dir = Path(r"C:\Users\prith\Projects\VYBERS_SkinSight-AI\data")
raw = json.loads((data_dir / "products_raw.json").read_text(encoding="utf-8"))
products = raw.get("products", [])


def strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def pipe(lst) -> str:
    return "|".join(str(x) for x in lst if x)


rows = []
for p in products:
    variants = p.get("variants", [])
    images = p.get("images", [])
    tags = p.get("tags", [])

    prices = list({v.get("price", "") for v in variants if v.get("price")})
    sizes = list({v.get("title", "") for v in variants if v.get("title") != "Default Title"})
    img_srcs = [i.get("src", "") for i in images[:3]]

    rows.append(
        {
            "id": p.get("id", ""),
            "title": p.get("title", "").strip(),
            "handle": p.get("handle", "").strip(),
            "product_type": p.get("product_type", "").strip(),
            "vendor": p.get("vendor", "").strip(),
            "tags": pipe(tags),
            "description": strip_html(p.get("body_html", "")),
            "prices_inr": pipe(sorted(prices)),
            "sizes": pipe(sizes),
            "image_urls": pipe(img_srcs),
            "published_at": p.get("published_at", ""),
            "created_at": p.get("created_at", ""),
            "updated_at": p.get("updated_at", ""),
        }
    )

FIELDNAMES = [
    "id", "title", "handle", "product_type", "vendor", "tags",
    "description", "prices_inr", "sizes", "image_urls",
    "published_at", "created_at", "updated_at",
]

out = data_dir / "dotkey_products.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(rows)

print(f"Written {len(rows)} rows → {out}")
print("\nSample (first row):")
for k, v in rows[0].items():
    display = str(v)
    print(f"  {k:15s}: {display[:90]}")
