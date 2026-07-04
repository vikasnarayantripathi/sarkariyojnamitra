#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sarkari Yojna Mitra — BILINGUAL static site generator (Hindi + English).

Run:  python3 generate.py
Builds:
  Hindi  (default): index.html, <slug>.html         -> URLs /  and /<slug>
  English         : en/index.html, en/<slug>.html    -> URLs /en/ and /en/<slug>
  + sitemap.xml (both languages), schemes.json
Each page carries hreflang alternates so Google indexes Hindi & English separately.

Edit scheme content in schemes_data.py, then re-run. Push all files to GitHub
-> Cloudflare Pages auto-deploys.
"""
import json, os, html
from schemes_data import SITE, BRAND, LANGS, CAT, LEVELS, T, SCHEMES

OUT = os.path.dirname(os.path.abspath(__file__))
try:
    from subpages_data import SUBPAGES
except Exception:
    SUBPAGES = {}
def e(x): return html.escape(str(x))

# ---------- URL helpers (Hindi at root, English under /en/) ----------
def home_url(lang):       return "/" if lang == "hi" else "/en/"
def scheme_url(lang, sl): return ("/" + sl) if lang == "hi" else ("/en/" + sl)
def static_url(lang, sl): return ("/" + sl) if lang == "hi" else ("/en/" + sl)
def anchor(lang, a):      return home_url(lang) + "#" + a
def other(lang):          return "en" if lang == "hi" else "hi"

STATIC_SLUGS = ["privacy", "about", "contact", "disclaimer", "terms"]

def hreflang(slug=None):
    if slug:
        hi, en = SITE + "/" + slug, SITE + "/en/" + slug
    else:
        hi, en = SITE + "/", SITE + "/en/"
    return ("<link rel=\"alternate\" hreflang=\"hi\" href=\"%s\">\n"
            "<link rel=\"alternate\" hreflang=\"en\" href=\"%s\">\n"
            "<link rel=\"alternate\" hreflang=\"x-default\" href=\"%s\">") % (hi, en, hi)

# ---------- brand SVGs ----------
LOGO = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" '
        'stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/><path d="m9 15 2 2 4-4"/></svg>')
FLAG = ('<svg viewBox="0 0 18 12" width="18" height="12" style="border-radius:2px;vertical-align:middle">'
        '<rect width="18" height="4" y="0" fill="#FF9933"/><rect width="18" height="4" y="4" fill="#fff"/>'
        '<rect width="18" height="4" y="8" fill="#138808"/><circle cx="9" cy="6" r="1.5" fill="none" stroke="#000080" stroke-width="0.5"/></svg>')

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
:root{
 --o:#E4590A;--o2:#F97316;--sun:#F59E1B;--sunbg:#FEF6E7;
 --ink:#241811;--mut:#6E5F52;--bg:#FFFAF4;--line:#F1E4D3;--card:#fff;
 --glow:0 1px 2px rgba(36,24,17,.04),0 8px 24px rgba(228,89,10,.07)
}
html{scroll-behavior:smooth}
body{font-family:'Mukta',system-ui,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;font-size:16.5px;-webkit-font-smoothing:antialiased}
.tricolor{height:3px;background:linear-gradient(90deg,#FF9933 33%,#fff 33% 66%,#138808 66%)}
a{color:inherit;text-decoration:none}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
::selection{background:#FDE4CE}
/* static pages */
.static{padding:34px 0 56px;max-width:760px}
.static h1{font-size:1.9rem;margin-bottom:20px;letter-spacing:-.01em}
.static h2{font-size:1.22rem;margin:28px 0 10px}
.static p{margin-bottom:13px;color:#3D2E22}
.static ul{margin:8px 0 18px 22px}
.static li{margin-bottom:6px}
.static a{color:var(--o);text-decoration:underline;text-underline-offset:3px}
/* header */
header{background:rgba(255,252,248,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.hd{display:flex;align-items:center;gap:12px;padding:13px 0}
.logo{display:flex;align-items:center;gap:11px;font-weight:700}
.logo .box{width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,#F59E1B,#E4590A);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 10px rgba(228,89,10,.3)}
.logo b{font-size:1.1rem;line-height:1.2;letter-spacing:-.01em}
.logo small{display:block;font-size:.68rem;color:var(--mut);font-weight:500}
nav{margin-left:auto;display:flex;align-items:center;gap:20px}
nav a{color:var(--mut);font-weight:600;font-size:.92rem;transition:color .15s}
nav a:hover{color:var(--o)}
.lang{border:1px solid var(--line);color:var(--o);background:#fff;border-radius:8px;padding:5px 14px;font-weight:700;font-size:.84rem;transition:.15s}
.lang:hover{background:var(--o);color:#fff;border-color:var(--o)}
.burger{display:none}
/* hero — dawn glow */
.hero{background:radial-gradient(ellipse 900px 420px at 50% -80px,#FEEFD8 0%,#FFFAF4 55%,var(--bg) 100%);padding:52px 0 36px;text-align:center;border-bottom:1px solid var(--line)}
.badge{display:inline-flex;align-items:center;gap:7px;background:var(--sunbg);border:1px solid #F6DFAE;color:#9A6A08;font-weight:600;font-size:.8rem;padding:6px 14px;border-radius:999px;margin-bottom:18px}
.hero h1{font-family:'Tiro Devanagari Hindi',serif;font-size:2.25rem;line-height:1.28;margin-bottom:13px;letter-spacing:-.01em}
.hero h1 span{background:linear-gradient(100deg,#E4590A,#F59E1B);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{color:var(--mut);max-width:660px;margin:0 auto 26px;font-size:1.02rem}
.search{display:flex;max-width:600px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--glow);transition:border-color .15s}
.search:focus-within{border-color:var(--o2)}
.search input{flex:1;border:0;padding:15px 18px;font-size:1rem;font-family:inherit;outline:none;background:transparent}
.search button{border:0;background:linear-gradient(135deg,#F97316,#E4590A);color:#fff;font-weight:700;padding:0 24px;cursor:pointer;font-size:.94rem;font-family:inherit;transition:filter .15s}
.search button:hover{filter:brightness(1.08)}
.stats{display:flex;justify-content:center;gap:38px;margin-top:28px;flex-wrap:wrap}
.stat b{display:block;font-size:1.55rem;color:var(--o);font-variant-numeric:tabular-nums}
.stat span{font-size:.78rem;color:var(--mut);font-weight:500;letter-spacing:.02em}
/* sections */
section{padding:40px 0}
.sec-h{text-align:center;margin-bottom:26px}
.sec-h h2{font-family:'Tiro Devanagari Hindi',serif;font-size:1.65rem;letter-spacing:-.01em}
.sec-h p{color:var(--mut);font-size:.92rem;margin-top:4px}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:26px}
.chip{border:1px solid var(--line);background:#fff;color:var(--mut);border-radius:999px;padding:7px 16px;font-size:.85rem;font-weight:600;cursor:pointer;font-family:inherit;transition:.15s}
.chip.on,.chip:hover{background:var(--o);color:#fff;border-color:var(--o)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:19px;display:flex;flex-direction:column;transition:border-color .15s,transform .15s,box-shadow .15s;cursor:pointer}
.card:hover{transform:translateY(-2px);box-shadow:var(--glow);border-color:#EBC79E}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.ic{font-size:1.65rem}
.lvl{font-size:.66rem;font-weight:700;padding:3px 10px;border-radius:999px;letter-spacing:.03em}
.lvl.c{background:#E8F0FE;color:#1A56C4}.lvl.up{background:#FDEBDD;color:#C24A05}.lvl.st{background:#FDEBDD;color:#C24A05}
.card h3{font-size:1.03rem;margin-bottom:2px;letter-spacing:-.005em}
.card .sub{font-family:'Tiro Devanagari Hindi',serif;color:var(--mut);font-size:.86rem;margin-bottom:11px}
.ben{background:var(--sunbg);border:1px solid #F6DFAE;border-radius:9px;padding:7px 12px;font-size:.85rem;margin-bottom:13px}
.ben b{color:#9A6A08;font-variant-numeric:tabular-nums}
.more{margin-top:auto;color:var(--o);font-weight:700;font-size:.85rem}
.empty{text-align:center;color:var(--mut);padding:34px;display:none}
/* finder */
.finder{background:#fff;border:1px solid var(--line);border-radius:18px;padding:30px;max-width:780px;margin:0 auto;box-shadow:var(--glow)}
.finder h2{font-family:'Tiro Devanagari Hindi',serif;font-size:1.45rem;text-align:center}
.finder>p{text-align:center;color:var(--mut);font-size:.9rem;margin-bottom:20px}
.fq{font-weight:700;margin:16px 0 9px;font-size:.95rem}
.opts{display:flex;flex-wrap:wrap;gap:8px}
.opt{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 15px;font-size:.87rem;font-weight:600;cursor:pointer;font-family:inherit;transition:.15s}
.opt:hover{border-color:#EBC79E}
.opt.on{background:var(--o);color:#fff;border-color:var(--o)}
.fres{margin-top:20px;display:none}
.fres .lbl{font-weight:700;margin-bottom:10px}
.fres a{display:block;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:11px 14px;margin-bottom:8px;font-weight:600;transition:.15s}
.fres a:hover{border-color:var(--o2);background:#FFF3E6}
/* tools */
.tools{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:14px}
.tool{border:1px solid var(--line);border-radius:14px;padding:19px;position:relative;background:#fff;transition:.15s}
.tool:hover{border-color:#EBC79E;box-shadow:var(--glow)}
.tool .tag{position:absolute;top:13px;right:13px;font-size:.6rem;color:var(--mut);background:var(--bg);padding:2px 9px;border-radius:999px;font-weight:600;letter-spacing:.04em}
.tool .e{font-size:1.7rem}
.tool h3{margin:9px 0 5px;font-size:1.03rem}
.tool p{color:var(--mut);font-size:.85rem;margin-bottom:12px}
.tool a{color:var(--o);font-weight:700;font-size:.86rem}
/* alert */
.alert{background:var(--sunbg);border:1px solid #F6DFAE;border-left:3px solid var(--sun);border-radius:12px;padding:14px 18px;font-size:.88rem;margin:0 auto;max-width:1040px;color:#6B4A06}
.adwrap{margin:28px auto;max-width:1040px;min-height:90px;background:#FCFAF7;border:1px dashed var(--line);border-radius:12px;display:flex;align-items:center;justify-content:center;color:#C9BBA9;font-size:.78rem}
/* footer — dusk */
footer{background:#231407;color:#C4A98E;padding:40px 0 22px;font-size:.9rem}
.fgrid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px;margin-bottom:24px}
footer h4{color:#fff;margin-bottom:13px;font-size:.98rem}
.flogo{display:flex;align-items:center;gap:10px;margin-bottom:11px}
.flogo .box{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,#F59E1B,#E4590A);display:flex;align-items:center;justify-content:center}
.flogo b{color:#fff;font-size:1.03rem}
footer ul{list-style:none}footer li{margin-bottom:7px}
footer a{transition:color .15s}footer a:hover{color:#F5A623}
.disc{border-top:1px solid #3B2812;padding-top:16px;font-size:.77rem;color:#9A8168}
.copy{text-align:center;margin-top:13px;font-size:.77rem;color:#7D6850}
/* scheme page */
.crumb{font-size:.82rem;color:var(--mut);padding:16px 0}
.crumb a:hover{color:var(--o)}
.updated{font-size:.8rem;color:var(--mut);margin:-.4rem 0 1rem}
.sp-hero{background:linear-gradient(160deg,#fff 60%,#FFF6EA);border:1px solid var(--line);border-radius:16px;padding:26px;margin-bottom:20px;box-shadow:var(--glow)}
.sp-hero .ic{font-size:2.5rem}
.sp-hero h1{font-size:1.75rem;margin:9px 0 3px;letter-spacing:-.01em}
.sp-hero .sub{font-family:'Tiro Devanagari Hindi',serif;color:var(--mut);margin-bottom:15px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:11px;margin-top:10px}
.fact{background:#fff;border:1px solid var(--line);border-radius:11px;padding:11px 14px}
.fact span{font-size:.7rem;color:var(--mut);display:block;font-weight:600;letter-spacing:.03em}
.fact b{font-size:.95rem;font-variant-numeric:tabular-nums}
.block{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px 24px;margin-bottom:16px}
.block h2{font-family:'Tiro Devanagari Hindi',serif;font-size:1.32rem;margin-bottom:14px;color:var(--o)}
.block p{color:#3D2E22}
.block ul{list-style:none;margin-top:4px}
.block li{padding:8px 0 8px 30px;position:relative;border-bottom:1px solid #F8EFE2}
.block li:last-child{border-bottom:0}
.block li:before{content:"✓";position:absolute;left:0;top:8px;color:#fff;background:var(--o);width:19px;height:19px;border-radius:50%;font-size:.68rem;display:flex;align-items:center;justify-content:center}
.steps{counter-reset:s}
.steps li:before{content:counter(s);counter-increment:s;background:var(--sun);color:#fff;font-weight:700}
.faq{border-bottom:1px solid #F8EFE2;padding:13px 0}.faq:last-child{border:0}
.faq b{display:block;margin-bottom:4px}
.faq span{color:var(--mut);font-size:.92rem}
.cta-apply{display:inline-block;background:linear-gradient(135deg,#F97316,#E4590A);color:#fff;font-weight:700;padding:13px 26px;border-radius:11px;margin-top:6px;transition:.15s;box-shadow:0 3px 14px rgba(228,89,10,.32)}
.cta-apply:hover{filter:brightness(1.08);transform:translateY(-1px)}
.related{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:12px}
.related a{background:#fff;border:1px solid var(--line);border-radius:11px;padding:13px 15px;font-weight:600;font-size:.9rem;transition:.15s}
.related a:hover{border-color:var(--o2);background:#FFF6EC}
@media(max-width:760px){
 nav{gap:12px}.hero h1{font-size:1.65rem}.fgrid{grid-template-columns:1fr}
 nav a:not(.lang){display:none}
 body{font-size:16px}
 .hero{padding:38px 0 28px}
 section{padding:30px 0}
}
"""

GF = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
      '<link href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;600;700&'
      'family=Tiro+Devanagari+Hindi&display=swap" rel="stylesheet">')

def head(lang, title, desc, canonical, slug=None, jsonld=None):
    j = ""
    if jsonld:
        j = "\n".join('<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False) for o in jsonld)
    return ('<!DOCTYPE html><html lang="%s"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s"><meta property="og:type" content="article"><meta property="article:modified_time" content="2026-07-03">'
            '<link rel="canonical" href="%s"><link rel="icon" type="image/svg+xml" href="/favicon.svg">\n%s\n%s%s'
            '<script async src="https://www.googletagmanager.com/gtag/js?id=G-YQ7KBCEX94"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-YQ7KBCEX94");</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3246006644123903" crossorigin="anonymous"></script>'
            '<style>%s</style></head><body><div class="tricolor"></div>'
            % (lang, e(title), e(desc), canonical, hreflang(slug), GF, j, CSS))

def header(lang, toggle_href):
    t = T[lang]
    nav = ''.join('<a href="%s">%s</a>' % (anchor(lang, a), e(n))
                  for a, n in zip(["schemes","finder","tools","schemes"], t["nav"]))
    return ('<header><div class="wrap hd">'
            '<a class="logo" href="%s"><span class="box">%s</span>'
            '<span><b>%s</b><small>%s</small></span></a>'
            '<nav>%s<a class="lang" href="%s">%s</a></nav>'
            '</div></header>' % (home_url(lang), LOGO, BRAND, e(t["tagline"]), nav, toggle_href, e(t["toggle"])))

def footer(lang):
    t = T[lang]
    pop = ''.join('<li><a href="%s">%s</a></li>' % (scheme_url(lang, s["slug"]), e(s["name"]))
                  for s in SCHEMES[:6])
    lk = ''.join('<li><a href="%s">%s</a></li>' % (anchor(lang, a), e(x))
                 for a, x in zip(["schemes","finder","tools"], t["foot_links_items"]))
    pg = ''.join('<li><a href="%s">%s</a></li>' % (static_url(lang, sl), e(lb))
                 for sl, lb in t["foot_pages_items"])
    return ('<footer><div class="wrap"><div class="fgrid">'
            '<div><div class="flogo"><span class="box">%s</span><b>%s</b></div>'
            '<p>%s</p></div>'
            '<div><h4>%s</h4><ul>%s</ul></div>'
            '<div><h4>%s</h4><ul>%s%s</ul></div></div>'
            '<div class="disc">%s</div>'
            '<div class="copy">© 2026 %s · A Quimztech Network site</div>'
            '</div></footer>' % (LOGO, BRAND, t["foot_about"], e(t["foot_popular"]), pop,
                                 e(t["foot_links"]), lk, pg, t["disclaimer"], BRAND))

def alert(lang):
    return '<div class="wrap"><div class="alert">%s</div></div>' % T[lang]["alert"]

def card(s, lang):
    c = s[lang]; lv = LEVELS[s["level"]]
    txt = e(s["name"] + " " + s["hindi"] + " " + c["benefit"] + " " + " ".join(s["tags"]))
    return ('<a class="card" href="%s" data-cat="%s" data-tags="%s" data-text="%s">'
            '<div class="card-top"><span class="ic">%s</span>'
            '<span class="lvl %s">%s</span></div>'
            '<h3>%s</h3><p class="sub">%s</p>'
            '<div class="ben">%s: <b>%s</b></div>'
            '<span class="more">%s</span></a>'
            % (scheme_url(lang, s["slug"]), s["cat"], e(" ".join(s["tags"])), txt,
               s["icon"], lv["badge"], e(lv[lang]), e(s["name"]), e(s["hindi"]),
               e(T[lang]["lbl_benefit"]), e(c["benefit"]), e(T[lang]["card_cta"])))

def render_index(lang):
    t = T[lang]
    cats = [c for c in CAT if any(s["cat"] == c for s in SCHEMES)]
    chips = '<button class="chip on" data-f="all">%s</button>' % e(t["all"])
    chips += ''.join('<button class="chip" data-f="%s">%s</button>' % (c, e(CAT[c][lang])) for c in cats)
    cards = ''.join(card(s, lang) for s in SCHEMES)
    who = ''.join('<button class="opt" data-g="who" data-v="%s">%s</button>' % (v, e(n)) for v, n in t["who_opts"])
    need = ''.join('<button class="opt" data-g="need" data-v="%s">%s</button>' % (v, e(n)) for v, n in t["need_opts"])
    tools = ''.join('<div class="tool"><span class="tag">%s</span><div class="e">%s</div>'
                    '<h3>%s</h3><p>%s</p><a href="%s" target="_blank" rel="noopener">%s</a></div>'
                    % (e(tg), ic, e(ti), e(de), hr, e(ct))
                    for ic, ti, de, ct, hr, tg in t["tools"])
    js_data = [{"slug": s["slug"], "name": s["name"], "url": scheme_url(lang, s["slug"]),
                "tags": s["tags"], "cat": s["cat"]} for s in SCHEMES]
    jd = json.dumps(js_data, ensure_ascii=False)
    flbl = e(t["finder_label"]); felse = e(t["finder_else"])
    jsonld = [
        {"@context":"https://schema.org","@type":"WebSite","name":BRAND,"url":SITE+home_url(lang),
         "inLanguage":lang,"potentialAction":{"@type":"SearchAction",
         "target":SITE+home_url(lang)+"?q={q}","query-input":"required name=q"}},
        {"@context":"https://schema.org","@type":"ItemList","itemListElement":[
            {"@type":"ListItem","position":i+1,"url":SITE+scheme_url(lang,s["slug"]),"name":s["name"]}
            for i,s in enumerate(SCHEMES)]}
    ]
    H = head(lang, t["title_home"], t["desc_home"], SITE + home_url(lang), None, jsonld)
    H += header(lang, home_url(other(lang)))
    H += ('<section class="hero"><div class="wrap">'
          '<span class="badge">%s %s</span>'
          '<h1>%s<span>%s</span>%s</h1><p>%s</p>'
          '<div class="search"><input id="q" placeholder="%s"><button onclick="run()">%s</button></div>'
          '<div class="stats"><div class="stat"><b>%d</b><span>%s</span></div>'
          '<div class="stat"><b>%d</b><span>%s</span></div>'
          '<div class="stat"><b>100%%</b><span>%s</span></div></div>'
          '</div></section>'
          % (FLAG, e(t["badge"]), e(t["h1a"]), e(t["h1span"]), e(t["h1b"]), e(t["hp"]),
             e(t["search_ph"]), e(t["search_btn"]),
             len(SCHEMES), e(t["stat_schemes"]), len(cats), e(t["stat_cats"]), e(t["stat_official"])))
    H += alert(lang)
    H += ('<section id="schemes"><div class="wrap"><div class="sec-h"><h2>%s</h2><p>%s</p></div>'
          '<div class="chips">%s</div><div class="grid" id="grid">%s</div>'
          '<div class="empty" id="empty"><b>%s</b><br>%s</div></div></section>'
          % (e(t["sec_schemes_h"]), e(t["sec_schemes_p"]), chips, cards,
             e(t["no_results_b"]), e(t["no_results"])))
    H += '<div class="wrap"><div class="adwrap">Ad space</div></div>'
    H += ('<section id="finder"><div class="wrap"><div class="finder"><h2>%s</h2><p>%s</p>'
          '<div class="fq">%s</div><div class="opts">%s</div>'
          '<div class="fq">%s</div><div class="opts">%s</div>'
          '<div class="fres" id="fres"></div></div></div></section>'
          % (e(t["finder_h"]), e(t["finder_p"]), e(t["finder_q1"]), who, e(t["finder_q2"]), need))
    H += ('<section class="tools" id="tools"><div class="wrap"><div class="sec-h"><h2>%s</h2><p>%s</p></div>'
          '<div class="tgrid">%s</div></div></section>' % (e(t["tools_h"]), e(t["tools_p"]), tools))
    H += footer(lang)
    H += """<script>
var SCHEMES=__DATA__;var FL="__FLBL__",FE="__FELSE__";
var curF="all",sel={who:[],need:[]};
function run(){var q=(document.getElementById('q').value||'').toLowerCase().trim();
 var n=0;document.querySelectorAll('.card').forEach(function(c){
  var okF=curF==='all'||c.dataset.cat===curF;
  var okQ=!q||c.dataset.text.toLowerCase().indexOf(q)>-1;
  var sh=okF&&okQ;c.style.display=sh?'flex':'none';if(sh)n++;});
 document.getElementById('empty').style.display=n?'none':'block';}
document.querySelectorAll('.chip').forEach(function(ch){ch.onclick=function(){
 document.querySelectorAll('.chip').forEach(function(x){x.classList.remove('on')});
 ch.classList.add('on');curF=ch.dataset.f;run();}});
document.getElementById('q').addEventListener('keyup',function(ev){if(ev.key==='Enter')run();run();});
document.querySelectorAll('.opt').forEach(function(o){o.onclick=function(){
 o.classList.toggle('on');var g=o.dataset.g,v=o.dataset.v;var i=sel[g].indexOf(v);
 if(i>-1)sel[g].splice(i,1);else sel[g].push(v);finder();}});
function finder(){var picks=sel.who.concat(sel.need);var box=document.getElementById('fres');
 if(!picks.length){box.style.display='none';return;}
 var hits=SCHEMES.filter(function(s){return s.tags.some(function(t){return picks.indexOf(t)>-1;});});
 var html='<div class="lbl">'+FL+'</div>';
 if(hits.length){hits.slice(0,8).forEach(function(s){html+='<a href="'+s.url+'">'+s.name+' →</a>';});}
 else{html+='<a href="#schemes">'+FE+'</a>';}
 box.innerHTML=html;box.style.display='block';}
</script>"""
    H = H.replace("__DATA__", jd).replace("__FLBL__", flbl.replace('"','\\"')).replace("__FELSE__", felse.replace('"','\\"'))
    H += "</body></html>"
    return H

def render_scheme(s, lang):
    t = T[lang]; c = s[lang]; lv = LEVELS[s["level"]]
    def ul(items, cls=""):
        return '<ul class="%s">%s</ul>' % (cls, ''.join('<li>%s</li>' % e(i) for i in items))
    faqs = ''.join('<div class="faq"><b>%s</b><span>%s</span></div>' % (e(q), e(a)) for q, a in c["faqs"])
    related = [x for x in SCHEMES if x["cat"] == s["cat"] and x["slug"] != s["slug"]][:3]
    if len(related) < 3:
        related += [x for x in SCHEMES if x["slug"] != s["slug"] and x not in related][:3-len(related)]
    rel = ''.join('<a href="%s">%s %s</a>' % (scheme_url(lang, r["slug"]), r["icon"], e(r["name"])) for r in related)
    title = "%s — %s | %s" % (s["name"], c["benefit"], BRAND)
    desc = c["intro"][:155]
    jsonld = [
        {"@context":"https://schema.org","@type":"GovernmentService","name":s["name"],
         "alternateName":s["hindi"],"serviceType":CAT[s["cat"]]["en"],
         "areaServed":{"@type":"AdministrativeArea","name":lv["area"]},
         "provider":{"@type":"GovernmentOrganization","name":c["ministry"]},
         "description":c["intro"],"url":SITE+scheme_url(lang,s["slug"]),
         "availableChannel":{"@type":"ServiceChannel","serviceUrl":s["portal"]}},
        {"@context":"https://schema.org","@type":"FAQPage","inLanguage":lang,
         "mainEntity":[{"@type":"Question","name":q,
            "acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c["faqs"]]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":t["crumb_home"],"item":SITE+home_url(lang)},
            {"@type":"ListItem","position":2,"name":s["name"],"item":SITE+scheme_url(lang,s["slug"])}]}
    ]
    H = head(lang, title, desc, SITE + scheme_url(lang, s["slug"]), s["slug"], jsonld)
    H += header(lang, scheme_url(other(lang), s["slug"]))
    H += ('<div class="wrap"><div class="crumb"><a href="%s">%s</a> › %s</div>'
          % (home_url(lang), e(t["crumb_home"]), e(s["name"])))
    H += ('<div class="sp-hero"><span class="ic">%s</span>'
          '<span class="lvl %s" style="margin-left:10px">%s</span>'
          '<h1>%s</h1><p class="updated">अंतिम अपडेट: 03/07/2026</p><p class="sub">%s</p>'
          '<div class="facts">'
          '<div class="fact"><span>%s</span><b>%s</b></div>'
          '<div class="fact"><span>%s</span><b>%s</b></div>'
          '<div class="fact"><span>%s</span><b>%s</b></div>'
          '<div class="fact"><span>%s</span><b>%s</b></div></div></div>'
          % (s["icon"], lv["badge"], e(lv[lang]), e(s["name"]), e(s["hindi"]),
             e(t["lbl_benefit"]), e(c["benefit"]), e(t["lbl_who"]), e(c["who"]),
             e(t["lbl_ministry"]), e(c["ministry"]), e(t["lbl_lastdate"]), e(c["lastDate"])))
    H += '<div class="block"><h2>%s</h2><p>%s</p></div>' % (e(t["sec_what"]), e(c["intro"]))
    sp_guides = SUBPAGES.get(s["slug"], [])
    if lang == "hi" and sp_guides:
        g = ''.join('<a href="/%s/%s">📄 %s</a>' % (s["slug"], x["slug"], e(x["nav"])) for x in sp_guides)
        H += '<div class="block"><h2>विस्तृत गाइड</h2><div class="related">%s</div></div>' % g
    H += '<div class="block"><h2>%s</h2>%s</div>' % (e(t["sec_benefits"]), ul(c["benefits"]))
    H += '<div class="block"><h2>%s</h2>%s</div>' % (e(t["sec_elig"]), ul(c["eligibility"]))
    H += '<div class="block"><h2>%s</h2>%s</div>' % (e(t["sec_docs"]), ul(c["documents"]))
    H += '<div class="block"><h2>%s</h2>%s</div>' % (e(t["sec_apply"]), ul(c["howToApply"], "steps"))
    H += ('<div class="block" style="text-align:center">'
          '<a class="cta-apply" href="%s" target="_blank" rel="nofollow noopener">%s</a></div>'
          % (s["portal"], e(t["cta_apply"])))
    H += '<div class="block"><h2>%s</h2>%s</div>' % (e(t["sec_faq"]), faqs)
    H += alert(lang)
    H += ('<section><div class="wrap"><div class="sec-h"><h2>%s</h2></div>'
          '<div class="related">%s</div></div></section>' % (e(t["related"]), rel))
    H += '</div>'  # close wrap
    H += footer(lang)
    H += "</body></html>"
    return H

def render_static(slug, lang):
    t = T[lang]
    sp = t["static"][slug]
    canonical = SITE + static_url(lang, slug)
    H = head(lang, sp["title"], sp["desc"], canonical, slug=slug)
    H += header(lang, static_url(other(lang), slug))
    H += '<main><div class="wrap"><div class="static">'
    H += '<h1>%s</h1>' % e(sp["h1"])
    H += sp["body"]
    H += '</div></div></main>'
    H += footer(lang)
    H += '</body></html>'
    return H


def render_subpage(s, sp):
    """Render one Hindi subpage for scheme s."""
    lang = "hi"; t = T[lang]; c = s[lang]
    url = "/" + s["slug"] + "/" + sp["slug"]
    canonical = SITE + url
    sibs = SUBPAGES.get(s["slug"], [])
    sibnav = '<div class="chips" style="justify-content:flex-start;margin:0 0 18px">'
    sibnav += '<a class="chip" href="%s">%s सम्पूर्ण गाइड</a>' % (scheme_url(lang, s["slug"]), s["icon"])
    for x in sibs:
        cls = "chip on" if x["slug"] == sp["slug"] else "chip"
        sibnav += '<a class="%s" href="/%s/%s">%s</a>' % (cls, s["slug"], x["slug"], e(x["nav"]))
    sibnav += "</div>"
    steps_html = '<ul class="steps">%s</ul>' % ''.join('<li>%s</li>' % e(i) for i in sp["steps"])
    faqs_html = ''.join('<div class="faq"><b>%s</b><span>%s</span></div>' % (e(q), e(a)) for q, a in sp["faqs"])
    jsonld = [
        {"@context":"https://schema.org","@type":"HowTo","name":sp["h1"],
         "description":sp["intro"][:200],"inLanguage":"hi",
         "step":[{"@type":"HowToStep","position":i+1,"text":st} for i, st in enumerate(sp["steps"])]},
        {"@context":"https://schema.org","@type":"FAQPage","inLanguage":"hi",
         "mainEntity":[{"@type":"Question","name":q,
            "acceptedAnswer":{"@type":"Answer","text":a}} for q, a in sp["faqs"]]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":t["crumb_home"],"item":SITE+home_url(lang)},
            {"@type":"ListItem","position":2,"name":s["name"],"item":SITE+scheme_url(lang,s["slug"])},
            {"@type":"ListItem","position":3,"name":sp["nav"],"item":canonical}]}
    ]
    H = head(lang, sp["title"], sp["desc"], canonical, None, jsonld)
    H += header(lang, home_url("en"))
    H += ('<div class="wrap"><div class="crumb"><a href="%s">%s</a> › <a href="%s">%s</a> › %s</div>'
          % (home_url(lang), e(t["crumb_home"]), scheme_url(lang, s["slug"]), e(s["name"]), e(sp["nav"])))
    H += sibnav
    H += ('<div class="sp-hero"><span class="ic">%s</span>'
          '<h1>%s</h1><p class="updated">अंतिम अपडेट: जुलाई 2026 · स्रोत: %s</p>'
          '<p style="color:#3D2E22;margin-top:8px">%s</p></div>'
          % (s["icon"], e(sp["h1"]), e(s["portal"].replace("https://","")), e(sp["intro"])))
    H += '<div class="block"><h2>%s</h2>%s</div>' % (e(sp["steps_h"]), steps_html)
    if sp.get("extra_html"):
        H += sp["extra_html"]
    H += '<div class="block"><h2>अक्सर पूछे जाने वाले सवाल</h2>%s</div>' % faqs_html
    H += ('<div class="block"><h2>आधिकारिक लिंक</h2>'
          '<p><a class="cta-apply" href="%s" target="_blank" rel="noopener">%s पर जाएं →</a></p></div>'
          % (s["portal"], e(s["portal"].replace("https://",""))))
    rel = ''.join('<a href="/%s/%s">%s</a>' % (s["slug"], x["slug"], e(x["nav"]))
                  for x in sibs if x["slug"] != sp["slug"])
    H += '<div class="block"><h2>इस योजना की अन्य गाइड</h2><div class="related">%s<a href="%s">%s सम्पूर्ण जानकारी</a></div></div>' % (rel, scheme_url(lang, s["slug"]), s["icon"])
    H += "</div>"
    H += footer(lang)
    H += "</body></html>"
    return H

def render_sitemap():
    urls = []
    for lang in LANGS:
        urls.append(SITE + home_url(lang))
        for s in SCHEMES:
            urls.append(SITE + scheme_url(lang, s["slug"]))
        for sl in STATIC_SLUGS:
            urls.append(SITE + static_url(lang, sl))
    for sslug, subs in SUBPAGES.items():
        for sp in subs:
            urls.append(SITE + "/" + sslug + "/" + sp["slug"])
    def pri(u):
        if u.rstrip("/") in (SITE, SITE+"/en"): return "1.0"
        if any(u.endswith("/"+sl) or u.endswith("/en/"+sl) for sl in STATIC_SLUGS): return "0.5"
        return "0.8"
    body = ''.join('<url><loc>%s</loc><changefreq>weekly</changefreq><priority>%s</priority></url>'
                   % (u, pri(u)) for u in urls)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % body

# ---------------- build ----------------
def w(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(path) else None
    open(full, "w", encoding="utf-8").write(content)

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "en"), exist_ok=True)
    n = 0
    for lang in LANGS:
        idx = "index.html" if lang == "hi" else "en/index.html"
        w(idx, render_index(lang)); n += 1
        for s in SCHEMES:
            p = (s["slug"] + ".html") if lang == "hi" else ("en/" + s["slug"] + ".html")
            w(p, render_scheme(s, lang)); n += 1
            if lang == "hi":
                for sp in SUBPAGES.get(s["slug"], []):
                    w(s["slug"] + "/" + sp["slug"] + ".html", render_subpage(s, sp)); n += 1
        for sl in STATIC_SLUGS:
            p = (sl + ".html") if lang == "hi" else ("en/" + sl + ".html")
            w(p, render_static(sl, lang)); n += 1
    w("sitemap.xml", render_sitemap())
    w("llms.txt", open(os.path.join(OUT,"llms.txt"),"r",encoding="utf-8").read())
    w("favicon.svg", open(os.path.join(OUT,"favicon.svg"),encoding="utf-8").read())
    w("ads.txt", "google.com, pub-3246006644123903, DIRECT, f08c47fec0942fa0\n")
    w("google6b8fece3b82b2876.html", "google-site-verification: google6b8fece3b82b2876.html")
    json.dump([{**{k:s[k] for k in ("slug","icon","cat","level","tags","name","hindi","portal")},
                "hi":s["hi"],"en":s["en"]} for s in SCHEMES],
              open(os.path.join(OUT,"schemes.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Built %d HTML pages (%d schemes x 2 + 2 homes + %d static x 2) + sitemap.xml + schemes.json" % (n, len(SCHEMES), len(STATIC_SLUGS)))
