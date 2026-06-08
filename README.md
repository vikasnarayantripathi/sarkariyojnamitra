# Sarkari Yojna Mitra (sarkariyojnamitra.com)

Searchable government-scheme directory with one SEO page per scheme. Quimztech "Mitra" network.

## How it works (engine)
- `generate.py` — **source of truth.** Contains the `SCHEMES` data list + the site generator.
- Running it builds: `index.html` (homepage finder), one `<slug>.html` per scheme, `sitemap.xml`, and `schemes.json`.

### Add / edit a scheme
1. Open `generate.py` → `SCHEMES` list.
2. Copy any block, fill fields (slug = unique, lowercase-with-hyphens).
3. Run:
   ```
   python3 generate.py
   ```
4. Push all generated files to GitHub → Cloudflare Pages auto-deploys.

> Har naya scheme = `SCHEMES` me ek entry + re-run. Page, homepage card, sitemap sab automatic.

## Current batch: 21 schemes
**Central (18):** PM Kisan, Ayushman Bharat, PMAY, Mudra, Kisan Credit Card, PM Fasal Bima, Sukanya Samriddhi, Atal Pension, Ujjwala, e-Shram, PMSBY, PMJJBY, PM Matru Vandana, PM Vishwakarma, PM SVANidhi, National Scholarship, Skill India (PMKVY), Jan Dhan.
**Uttar Pradesh (3):** Kanya Sumangala, SSPY Pension, Abhyudaya.

Target: batch-by-batch tak ~200. Sirf verified schemes add karna (galat info = fraud risk).

## Files to deploy
`index.html`, all `*.html` scheme pages, `sitemap.xml`, `robots.txt`.
(`generate.py`, `schemes.json`, `README.md` repo me rakho — deploy par asar nahi.)

## Deploy (Cloudflare Pages)
1. Push files to GitHub repo `sarkariyojnamitra`.
2. Cloudflare Pages → already connected → auto-deploy on push.
3. Clean URLs: `pm-kisan.html` serves at `/pm-kisan` automatically.

## After live (.com Active hone par)
1. **Google Search Console** → property `https://sarkariyojnamitra.com` → submit `sitemap.xml` (22 URLs index honge).
2. **AdSense** — `index.html` me 2 `ad-box` slots. Approval ke baad `<ins>` code daalo (yeh slots generator ke index template me hain — `generate.py` me edit karke re-run).
3. **Affiliate links** — homepage "उपयोगी सेवाएँ" ke 3 `href="#"` apne real links se badlo (generate.py me).

## SEO built-in (har scheme page par)
- Unique title, meta description, canonical
- JSON-LD: GovernmentService + FAQPage + BreadcrumbList
- Breadcrumb, internal links (homepage ↔ scheme ↔ related), fraud disclaimer
