"""Find the grocery store that serves a delivery point, search it, then check live stock.

    python quickstart.py                    # central Riyadh, "milk"
    python quickstart.py 24.7136 46.6753 laban
"""

import sys

from client import RIYADH, get, money

lat = float(sys.argv[1]) if len(sys.argv) > 2 else RIYADH[0]
lon = float(sys.argv[2]) if len(sys.argv) > 2 else RIYADH[1]
query = sys.argv[3] if len(sys.argv) > 3 else (sys.argv[1] if len(sys.argv) == 2 else "milk")

# 1. Which catalogs serve this point, and from which store. Product calls need the store_id.
verticals = get("/verticals", lat=lat, lon=lon)
if not verticals["verticals"]:
    raise SystemExit("No Ninja coverage at that point")
for v in verticals["verticals"]:
    store = v.get("store") or {}
    eta = store.get("estimated_delivery_minutes")
    print(f"{v['vertical']:<10} store {v.get('store_id')}  status {v['status']}  ETA {eta} min")
store_id = verticals["store_ids"]["RETAIL"]

# 2. Search that store's grocery catalog.
found = get("/product-search", store_id=store_id, query=query, vertical="RETAIL", response_size=10)
print(f"\n{found['count']} products for {query!r} at store {store_id} "
      f"({found['discounted_count']} discounted, truncated={found['truncated']})")
for p in found["products"]:
    print(f"  SAR {money(p['price_cents']):>7.2f}  {'SALE ' if p.get('is_discounted') else '     '}"
          f"{p['name']}  (product_id {p['product_id']})")

# 3. Live on-hand stock. Pass product_id, not the store-scoped id like "5-19312942".
ids = ",".join(p["product_id"] for p in found["products"][:5])
if ids:
    stock = get("/product-inventory", store_id=store_id, product_ids=ids)
    print(f"\nStock: {stock['in_stock_count']} of {stock['count']} in stock")
    for item in stock["items"]:
        print(f"  {item['product_id']}  quantity {item['quantity']}  in_stock {item['in_stock']}")
