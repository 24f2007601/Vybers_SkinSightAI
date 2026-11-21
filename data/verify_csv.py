import csv

with open(r'C:\Users\prith\Projects\VYBERS_SkinSight-AI\data\dotkey_products.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")
print(f"Columns: {list(rows[0].keys())}")
print()
print("All products:")
for r in rows:
    ptype = r["product_type"].ljust(20)
    title = r["title"]
    price = r["prices_inr"]
    sizes = r["sizes"][:40]
    print(f"  [{ptype}] {title} | Rs.{price} | {sizes}")
