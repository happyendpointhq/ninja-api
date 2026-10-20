"""Export a nearby restaurant's full menu, with discounts, calories and allergens, to CSV.

    python menu_to_csv.py --query burger --out menu.csv
    python menu_to_csv.py --branch-id 50036              # a branch you already know

Two API calls: /restaurants to pick the branch (skipped with --branch-id), then
/restaurant-menu. Each row is one orderable variant (size or option) of a dish.
"""

import argparse
import csv

from client import RIYADH, get, money

COLUMNS = [
    "section", "item_id", "item", "variant_id", "variant", "price_sar", "original_price_sar",
    "is_discounted", "available", "calories", "allergens",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch-id")
    parser.add_argument("--query", help="dish or restaurant search, for example burger")
    parser.add_argument("--lat", type=float, default=RIYADH[0])
    parser.add_argument("--lon", type=float, default=RIYADH[1])
    parser.add_argument("--out", default="menu.csv")
    args = parser.parse_args()

    branch_id = args.branch_id
    if not branch_id:
        # page=1 is the first paginated page (15 per page); omitting page gives a different,
        # unpaginated "nearby" selection.
        page = get("/restaurants", lat=args.lat, lon=args.lon, query=args.query, page=1)
        if not page["branches"]:
            raise SystemExit("No restaurants found near that point")
        branch = page["branches"][0]
        fee = (branch.get("delivery") or {}).get("fee") or {}
        print(f"{branch['restaurant']['name']} ({branch['branch_name']}), "
              f"rating {(branch.get('rating') or {}).get('score')}, delivery SAR {fee.get('fee')}")
        branch_id = branch["branch_id"]

    menu = get("/restaurant-menu", branch_id=branch_id)
    rows = 0
    with open(args.out, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for section in menu["sections"]:
            for item in section["items"]:
                for v in item.get("variants") or []:
                    writer.writerow({
                        "section": section["name"],
                        "item_id": item["id"],
                        "item": item["name"],
                        "variant_id": v["id"],
                        "variant": v.get("name"),
                        "price_sar": money(v.get("price_cents")),
                        "original_price_sar": money(v.get("original_price_cents")),
                        "is_discounted": v.get("is_discounted"),
                        "available": item.get("available"),
                        "calories": v.get("calories"),
                        "allergens": ";".join(v.get("allergens") or []),
                    })
                    rows += 1
    print(f"{menu['name']}: {menu['section_count']} sections, {menu['item_count']} items, "
          f"{rows} variants written to {args.out}")


if __name__ == "__main__":
    main()
