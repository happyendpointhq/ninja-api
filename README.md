# Ninja API and Scraper

The Ninja API returns data from Ninja (ananinja.com), the Saudi quick-commerce app for
groceries and food delivery, as JSON: grocery, beauty and pharmacy products with current
and original prices in SAR, live on-hand stock by store, restaurants with ratings, delivery
fees and ETAs, and full menus with variant prices, calories and allergens. Ninja has no
public developer API, so this REST API is the way to use its catalog and menus in your own
code without building a Ninja app scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/ninja-api?utm_source=github&utm_medium=readme&utm_campaign=ninja-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/ninja-saudi-arabia
- Product page: https://happyendpoint.com/library/ninja-api?utm_source=github&utm_medium=readme&utm_campaign=ninja-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://ninja-saudi-arabia.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 37, all `GET` |
| Coverage | Restaurants in Saudi Arabia; grocery also in Kuwait, Qatar and Bahrain |
| Catalogs | Grocery and retail, beauty, pharmacy, restaurants |
| Languages | English and Arabic (`language=en` or `ar`) |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Stores and delivery**
- The catalogs that serve a delivery coordinate and the `store_id` for each one
- Store status, opening hours, delivery ETA and delayed-delivery notices

**Grocery, beauty and pharmacy**
- Product search by keyword, category or brand inside a store
- Current and original price in cents and SAR, discount amount and percent, availability, prescription flag, English and Arabic names, images
- Full product records with descriptions, galleries and variants
- Live on-hand stock quantity per product and store
- Category trees, brands, multi-pack bundles, store offers, promoted products

**Restaurants**
- Restaurant search near a point, with cuisine, free-delivery, top-rated and discount filters
- Branch profiles with rating, vote count, distance, ETA, delivery fee and discount campaigns
- Full menus: sections, dishes and every orderable variant with price, pre-discount price, calories, allergens and topping groups
- The delivery-fee ladder by basket value, deal campaigns and their discounted items
- Lookups from a pasted ananinja.com restaurant or cuisine URL

**Search and merchandising**
- Search suggestions, trending and boosted search phrases, smart lists, themed lists, banners and collections

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/ninja-saudi-arabia). There is a free plan. Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Product endpoints take a `store_id`, and the store depends on where you deliver. Look it up
from a coordinate first:

```bash
curl "https://ninja-saudi-arabia.p.rapidapi.com/verticals?lat=24.7136&lon=46.6753" \
  -H "x-rapidapi-host: ninja-saudi-arabia.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://ninja-saudi-arabia.p.rapidapi.com/product-search?store_id=5&query=milk&vertical=RETAIL&response_size=10" \
  -H "x-rapidapi-host: ninja-saudi-arabia.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py milk
```

```python
from client import get

store_id = get("/verticals", lat=24.7136, lon=46.6753)["store_ids"]["RETAIL"]
found = get("/product-search", store_id=store_id, query="milk", vertical="RETAIL", response_size=10)
for p in found["products"]:
    print(p["price_cents"] / 100, p["name"], p["product_id"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs milk
```

---

## Example response

Two products from `GET /product-search?store_id=5&query=eggs&vertical=RETAIL`, trimmed. Values
are from a live call on 20 October 2026. More responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "count": 15,
    "discounted_count": 8,
    "available_count": 15,
    "response_size": 15,
    "truncated": true,
    "products": [
      {
        "id": "5-8283936",
        "product_id": "8283936",
        "store_id": "5",
        "name": "Freshies Large Eggs Tray 30 Pcs",
        "brand_code": "FRESHIES",
        "currency": "SAR",
        "price_cents": 1895,
        "original_price_cents": 2395,
        "is_discounted": true,
        "is_available": true,
        "requires_prescription": false,
        "unit_of_measure": "PCS"
      },
      {
        "id": "5-8286131",
        "product_id": "8286131",
        "store_id": "5",
        "name": "Freshies Large Eggs Tray 6 Pcs",
        "brand_code": "FRESHIES",
        "currency": "SAR",
        "price_cents": 450,
        "original_price_cents": 595,
        "is_discounted": true,
        "is_available": true,
        "requires_prescription": false,
        "unit_of_measure": "PCS"
      }
    ]
  }
}
```

---

## Endpoints

Base URL: `https://ninja-saudi-arabia.p.rapidapi.com`

### Stores and delivery

| Endpoint | Returns |
|---|---|
| `GET /verticals` | Catalogs serving a coordinate, with the `store_id` for each |
| `GET /delivery-info` | Store status, opening hours, ETA and delivery notices at a coordinate |
| `GET /status` | Service health |

### Grocery, beauty and pharmacy

| Endpoint | Returns |
|---|---|
| `GET /product-search` | Products matching a keyword in one store |
| `GET /products-by-category` | Products in one or more categories |
| `GET /products-by-brand` | Products of one brand |
| `GET /product-details` | Full records for one or more products |
| `GET /product-inventory` | Live on-hand stock for products at a store |
| `GET /product-bundle` | The components of a multi-pack bundle |
| `GET /categories` | A store's category tree |
| `GET /category-sections` | Merchandising sections that group categories |
| `GET /brands` | Brands carried by a store |
| `GET /store-offers` | A store's current promotions |
| `GET /promoted-products` | Sponsored product placements |
| `GET /display-tags` | Display tags used on product cards |

### Restaurants

| Endpoint | Returns |
|---|---|
| `GET /restaurants` | Restaurants near a point, with filters and discounts |
| `GET /restaurant-details` | One branch's profile |
| `GET /restaurant-by-brand` | A brand's nearest branch |
| `GET /restaurant-by-url` | A branch from a pasted restaurant URL |
| `GET /restaurants-by-url` | Restaurants from a pasted cuisine or listing URL |
| `GET /restaurant-menu` | The full menu with variants, calories and allergens |
| `GET /menu-discounted-items` | The discounted dishes on a branch's menu |
| `GET /related-menu-items` | Dishes related to a branch's menu |
| `GET /restaurant-delivery-fees` | The delivery-fee ladder by basket value |
| `GET /restaurant-filters` | The filter vocabulary for restaurant search |
| `GET /cuisines` | Cuisine IDs and slugs at a coordinate |
| `GET /restaurant-deals` | Deal campaigns near a point |
| `GET /restaurant-deal-items` | The items in one deal campaign |
| `GET /restaurant-collections` | Curated restaurant collections |
| `GET /restaurant-banners` | Promotional banners |
| `GET /restaurant-suggestions` | Search suggestions for restaurants and dishes |
| `GET /trending-restaurant-searches` | Trending restaurant searches near a point |

### Search and merchandising

| Endpoint | Returns |
|---|---|
| `GET /search-phrases` | Search phrase suggestions for a catalog |
| `GET /boosted-search-phrases` | Sponsored search phrases |
| `GET /smart-search-lists` | Smart shopping lists |
| `GET /themed-lists` | Themed product lists |
| `GET /retail-stories` | Story-style promotions for a store |

---

## Things to know about the data

Most of these come from running the examples against the live API.

- **Everything starts from a coordinate.** The store that serves an address decides which
  products, prices and stock you see, so call `/verticals` with the customer's location and
  reuse the same point in later calls. Store IDs are not stable constants: the documented
  example gives the Riyadh beauty store as `202686`, while a live call for the same point
  returned `203388`.
- **Use `product_id`, not `id`, for follow-up calls.** Search rows carry both: `id` is
  store-scoped (`5-19289502`), `product_id` is the catalog ID (`19289502`) that
  `/product-inventory` and `/product-details` expect.
- **`count` is what came back, not the total.** With `response_size=10`, a milk search
  returned `count: 10` and `truncated: true`. There is no page cursor: raise `response_size`
  (up to 5000) until `truncated` is false, or narrow the query.
- **The cheapest pack is not the cheapest unit.** Pack size is only in the product name, and
  `unit_of_measure` is `PCS` even for milk. In a live eggs search, the 6-egg tray was the
  cheapest pack at SAR 4.50 (SAR 0.75 an egg), while the 30-egg tray at SAR 18.95 cost SAR
  0.63 an egg. Parse the size from the name before comparing prices.
- **Work in cents.** Prices come as `price_cents` and as SAR (`price`). Sum and compare the
  cents fields; `original_price_cents` equals `price_cents` when nothing is discounted.
- **Stock rows come back in their own order.** `/product-inventory` returned the five
  requested IDs sorted differently from the request, so join on `product_id`.
- **Calories can be placeholders.** In the live Future Burger menu, 11 of 17 variants had
  `calories: 1`. Treat implausibly small values as missing.
- **Trust the fee numbers, not the label.** A live branch showed the label `**Free Delivery**`
  with `fee_cents: 500` (SAR 5, down from SAR 18). Labels also carry markdown asterisks. Use
  `fee_cents`, and `/restaurant-delivery-fees` for the full basket ladder.
- **Restaurant search is not sorted by distance.** The first live result for "burger" from
  central Riyadh was 14.6 km away with a 69 minute ETA. Sort by `delivery.distance_km`
  yourself if nearness matters. `page=1` is the first paginated page; omitting `page` returns
  a separate unpaginated nearby selection.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Finds the stores for a coordinate, searches groceries, checks live stock |
| [`examples/python/basket_prices.py`](examples/python/basket_prices.py) | Prices a shopping list at one store and writes a CSV with current and original prices |
| [`examples/python/menu_to_csv.py`](examples/python/menu_to_csv.py) | Exports a nearby restaurant's menu, one row per variant, with discounts, calories and allergens |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | Store lookup and product search in Node 18+, no dependencies |
| [`samples/`](samples/) | Example responses for six endpoints |

---

## API or your own Ninja scraper

Ninja's catalog lives in a mobile app, so a homemade Ninja scraper means reverse engineering
app traffic and keeping up with every app release. This API returns the same catalog, stock
and menus as documented JSON, in English and Arabic, so the work you keep is the analysis.
If you need a recurring export of a whole catalog instead of API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=ninja-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Ninja prices and
menus without code:

```json
{
  "mcpServers": {
    "ninja": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: ninja-saudi-arabia.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Ninja app API for Saudi Arabia?

Ninja does not publish a public developer API. This API, built and maintained by Happy
Endpoint and independent of Ninja, provides its grocery catalog, stock, restaurants and
menus as REST and JSON.

### Is there a free Ninja API?

Yes. The RapidAPI listing has a free plan, and every endpoint can be tried on it.

### How do I use the Ninja API in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI
headers. [`examples/python/client.py`](examples/python/client.py) is the client, and the
other scripts in that folder are ready to run.

### Where is the Ninja API documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the
endpoint table above summarises them. Example responses are in [`samples/`](samples/).

### Can I track Ninja grocery prices and discounts?

Yes. Every product row has its current and original price and a discount flag.
[`basket_prices.py`](examples/python/basket_prices.py) writes a shopping list to CSV; run it
daily to build a price history.

### Can I check whether a product is in stock at a Ninja store?

Yes. `/product-inventory` returns the live on-hand quantity and `in_stock` for up to
several products in one call, for the store that serves your coordinate.

### Does it work in Arabic?

Yes. Pass `language=ar` for Arabic names and text. Product rows also carry `name_ar`.

### Do you cover other Saudi and Gulf platforms?

Yes, including Aqar and Wasalt for property and Bayut and PropertyFinder for the UAE. See
the [API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=ninja-api).

---

## Related repos

- [awesome-ecommerce-data-apis](https://github.com/happyendpointhq/awesome-ecommerce-data-apis) - ecommerce and product data APIs, including price tracking and open data
- [awesome-alternative-data](https://github.com/happyendpointhq/awesome-alternative-data) - alternative data sources for investment research
- [aqar-api](https://github.com/happyendpointhq/aqar-api) - Saudi Arabia property listings and district prices
- [wasalt-api](https://github.com/happyendpointhq/wasalt-api) - Saudi listings, REGA licences and Infath auctions

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
