# Panadería Celaya — Multi-Page Bilingual Website

Artisanal Mexican bakery website for **Panadería Celaya** (Grand Prairie, TX).

- **GitHub Repository**: [nikomillender-dotcom/panaderia-celaya](https://github.com/nikomillender-dotcom/panaderia-celaya)
- **Architecture**: Multi-page static site (no framework, zero build dependencies, ultra-fast TTFB).
- **Languages**: 100% bilingual (English & Español) with dedicated URLs and paired language toggling.

---

## Page Structure

| Page | English URL | Spanish URL (`/es/`) | Description |
|---|---|---|---|
| **Home** | `/` (`index.html`) | `/es/` (`es/index.html`) | Warm welcome, today's highlights, bakery ritual, family heritage. |
| **Menu & Orders** | `/menu/` | `/es/menu/` | Full pan dulce, savory weekend specials, cakes, filters & ordering basket. |
| **Custom Cakes** | `/cakes/` | `/es/cakes/` | Tres Leches showcase, birthday/quinceañera guide, sizes & custom orders. |
| **Our Story** | `/about/` | `/es/about/` | 18-year baking heritage in Grand Prairie, photo archive, owner dedication. |
| **Visit & Hours** | `/visit/` | `/es/visit/` | Marshall Dr location, live Open/Closed badge, weekend tamales/barbacoa alert, map & FAQ. |

---

## Design Refinements (No AI Clichés)

- **Authentic Editorial Layout**: Replaced the typical single-page infinite-scroll template with a classic multi-page bakery experience.
- **Removed AI Visual Tells**:
  - Eliminated the continuous endless marquee/ticker tape.
  - Eliminated floating tilted sticker badges cluttered over photos.
  - Replaced generic 3-emoji "Why Choose Us" marketing cards with **El Ritual de la Panadería** (*Toma tu charola y pinzas*, *Horno caliente a las 4 AM*, *Tamales y barbacoa de fin de semana*).
  - Contextualized FAQs rather than dumping a generic accordion onto the landing page.
- **Persistent Shopping Basket**: The order drawer is available on every page and synced via `localStorage`. Items added on the Menu or Cakes page stay in the cart across language switches and navigation.
- **Deep SEO & Schema.org**: Every page has its own dedicated Title, Meta Description, Open Graph tags, canonical link, and Schema.org structured data (Bakery, Menu, Product, AboutPage, Place, FAQPage).

---

## How to Edit & Rebuild

1. **Menu items & pricing**: Edit `src/menu.json`.
2. **Page copy & SEO metadata**: Edit `build.py`.
3. **Rebuild all 10 pages**:
   ```bash
   python3 build.py
   # Or with your production custom domain:
   SITE_URL=https://your-custom-domain.com python3 build.py
   ```
4. **Local Preview**:
   ```bash
   python3 -m http.server 8000
   # Open http://localhost:8000
   ```
