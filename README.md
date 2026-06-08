# Sarkari Yojna Mitra (sarkariyojnamitra.com)

Single-file scheme-finder site. Part of the Quimztech "Mitra" network (Emimitra ke same engine par).

## Files
- `index.html` — pura site (HTML + CSS + JS ek hi file me)
- `robots.txt` — crawlers ke liye
- `sitemap.xml` — Google Search Console submission ke liye

## Deploy — Cloudflare Pages (Emimitra wala hi flow)
1. GitHub par naya repo banao: `sarkariyojnamitra` → ye teeno files push karo (root me).
2. Cloudflare Dashboard → Pages → **Create a project** → Connect to Git → repo select.
3. Build settings:
   - Framework preset: **None**
   - Build command: *(khaali chhod do)*
   - Output directory: `/` (root)
4. Deploy → `*.pages.dev` URL milega → test karo.
5. Custom domain add karo: **sarkariyojnamitra.com** (DNS already GoDaddy→Cloudflare par hai).

## Live hone ke baad
1. **Google Search Console** → property add (`https://sarkariyojnamitra.com`) → `sitemap.xml` submit.
2. **AdSense** — `index.html` me 2 jagah `<div class="ad-box">Advertisement</div>` hai. Approval ke baad apna `<ins class="adsbygoogle">` code wahan paste karo, aur `<head>` me AdSense loader script add karo.
3. **Affiliate links** — `tools` section me 3 cards me `href="#"` hai (personal loan / health insurance / credit score). Apne affiliate program ke real links daal do. Emi Mitra link already live hai.

## Manual TODO (mere data ki zaroorat)
- [ ] AdSense publisher ID + ad unit codes
- [ ] Affiliate program links (loan/insurance/credit-score partner)
- [ ] Optional: og:image banner (1200×630) host karke `og:image` meta add karna

## Content note
15 central schemes verified hain (June 2026). Aage chahe to UP state schemes add kar sakte hain (audience eastern UP) — `schemes` array me ek object add karne se card apne aap ban jayega.
