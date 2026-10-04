# Panadería Celaya — bilingual website

Static site (no framework). `/` = English, `/es/` = Español. The EN|ES toggle links between the two real pages (best for Google); the cart is shared via localStorage.

## Edit & rebuild
- Menu / prices: `src/menu.json` (`price: null` = "price at pickup")
- All copy (EN + ES), SEO tags, JSON-LD: `build.py`
- Rebuild: `SITE_URL=https://your-real-domain.com python3 build.py`

## Before launch (TODO)
1. Set the real domain via `SITE_URL` (placeholder is www.panaderiacelaya.com) and rebuild.
2. Optional: set `ORDER_ENDPOINT` (Formspree/Basin URL) so orders arrive by email automatically. Without it, customers send the order by text/call.
3. Claim & complete the Google Business Profile (biggest local-SEO lever), claim Yelp, add the site URL to both.
4. Submit `sitemap.xml` in Google Search Console + Bing Webmaster Tools.
5. Confirm hours (sources disagree: 8:45 / 8:50 / 9 PM) and fill in real prices in `src/menu.json`.

## Preview
`python3 -m http.server 8000` in this folder → http://localhost:8000
