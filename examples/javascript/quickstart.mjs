// Ninja API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs milk

const HOST = 'ninja-saudi-arabia.p.rapidapi.com';
const [LAT, LON] = [24.7136, 46.6753]; // central Riyadh

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries({ language: 'en', ...params })) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Ninja API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const query = process.argv[2] ?? 'milk';
const { store_ids: storeIds } = await get('/verticals', { lat: LAT, lon: LON });
console.log('Stores at this point:', storeIds);

const found = await get('/product-search', {
  store_id: storeIds.RETAIL,
  query,
  vertical: 'RETAIL',
  response_size: 10,
});
console.log(`${found.count} products for "${query}"`);
for (const p of found.products) {
  console.log(`SAR ${(p.price_cents / 100).toFixed(2).padStart(7)}  ${p.name}`);
}
