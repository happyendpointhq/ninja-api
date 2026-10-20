"""Price a shopping list at one Ninja store and write a CSV.

    python basket_prices.py milk eggs "basmati rice" --out basket.csv
    python basket_prices.py milk --store-id 5            # skip the store lookup

For each item, searches the store's grocery catalog and records every match with its
current and original price, so you can track discounts over time by re-running daily.
One API call per item (plus one /verticals call when --store-id is not given).
"""

import argparse
import csv

from client import RIYADH, get, money

COLUMNS = [
    "query", "product_id", "name", "brand_code", "price_sar", "original_price_sar",
    "is_discounted", "available", "unit_of_measure",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("items", nargs="+", help="search terms, one per shopping-list item")
    parser.add_argument("--store-id", help="from /verticals; looked up from --lat/--lon if omitted")
    parser.add_argument("--lat", type=float, default=RIYADH[0])
    parser.add_argument("--lon", type=float, default=RIYADH[1])
    parser.add_argument("--matches", type=int, default=20, help="products kept per item")
    parser.add_argument("--out", default="basket.csv")
    args = parser.parse_args()

    store_id = args.store_id or get("/verticals", lat=args.lat, lon=args.lon)["store_ids"]["RETAIL"]

    with open(args.out, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for item in args.items:
            found = get("/product-search", store_id=store_id, query=item, vertical="RETAIL",
                        response_size=args.matches)
            for p in found["products"]:
                writer.writerow({
                    "query": item,
                    "product_id": p["product_id"],
                    "name": p["name"],
                    "brand_code": p.get("brand_code"),
                    "price_sar": money(p.get("price_cents")),
                    "original_price_sar": money(p.get("original_price_cents")),
                    "is_discounted": p.get("is_discounted"),
                    "available": p.get("is_available"),
                    "unit_of_measure": p.get("unit_of_measure"),
                })
            cheapest = min(found["products"], key=lambda p: p["price_cents"], default=None)
            note = f"cheapest pack SAR {money(cheapest['price_cents']):.2f} {cheapest['name']}" if cheapest else "no match"
            print(f"{item:<16} {found['count']:>4} matches  {note}")
    print(f"Wrote {args.out} (store {store_id})")


if __name__ == "__main__":
    main()
