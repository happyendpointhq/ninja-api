# Sample responses

Example `200` responses for six Ninja API endpoints. Long arrays are cut to their first
few items.

Five of them are **live responses from 20 October 2026**, because the examples in the API's
documentation leave out fields the API returns (for example `original_price_cents`,
`is_available`, `name_ar` and `store_id` on product rows) and show 15 restaurants per page
where the live call returned 20. Business WhatsApp contact numbers were removed from
`verticals.json`. `restaurant-delivery-fees.json` is the documentation's own example.

| File | Request |
|---|---|
| `verticals.json` | `GET /verticals?lat=24.7136&lon=46.6753` |
| `product-search.json` | `GET /product-search?store_id=5&query=milk&vertical=RETAIL&response_size=10` |
| `product-inventory.json` | `GET /product-inventory?store_id=5&product_ids=19289502,7518,1223,3705,1306` |
| `restaurants.json` | `GET /restaurants?lat=24.7136&lon=46.6753&query=burger&page=1` |
| `restaurant-menu.json` | `GET /restaurant-menu?branch_id=56969` |
| `restaurant-delivery-fees.json` | `GET /restaurant-delivery-fees?branch_id=50036&lat=24.7136&lon=46.6753` |

They are useful for writing parsers and tests before you subscribe. Prices and stock change
constantly, so do not hard-code these values.
