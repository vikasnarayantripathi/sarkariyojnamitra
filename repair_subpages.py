#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnose + repair subpage engine in generate.py. Run: python repair_subpages.py"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

gen = read("generate.py")

print("=== DIAGNOSTIC ===")
checks = {
    "B1 import":       "from subpages_data import SUBPAGES" in gen,
    "B2 render func":  "def render_subpage" in gen,
    "B3 sitemap":      "SUBPAGES.items()" in gen,
    "B4 build loop":   "render_subpage(s, sp)" in gen,
    "B5 hub links":    "sp_guides" in gen,
}
for k, v in checks.items():
    print("  %s : %s" % (k, "OK" if v else "MISSING"))

# Also test SUBPAGES data loads
sys.path.insert(0, REPO)
try:
    from subpages_data import SUBPAGES as SP
    print("  Data file    : OK (%d schemes, pm-kisan has %d subpages)" % (len(SP), len(SP.get("pm-kisan", []))))
except Exception as ex:
    print("  Data file    : ERROR - %s" % ex)
    sys.exit(1)

print("\n=== REPAIR ===")

# ---- B1 ----
if not checks["B1 import"]:
    anchor = "OUT = os.path.dirname(os.path.abspath(__file__))"
    fix = """OUT = os.path.dirname(os.path.abspath(__file__))
try:
    from subpages_data import SUBPAGES
except Exception:
    SUBPAGES = {}"""
    if anchor in gen:
        gen = gen.replace(anchor, fix, 1)
        print("  B1 applied")
    else:
        print("  B1 FAIL: anchor missing"); sys.exit(1)
else:
    print("  B1 already OK")

# ---- B2 ----
if not checks["B2 render func"]:
    FUNC = '''
def render_subpage(s, sp):
    lang = "hi"; t = T[lang]; c = s[lang]
    url = "/" + s["slug"] + "/" + sp["slug"]
    canonical = SITE + url
    sibs = SUBPAGES.get(s["slug"], [])
    sibnav = '<div class="chips" style="justify-content:flex-start;margin:0 0 18px">'
    sibnav += '<a class="chip" href="%s">%s गाइड होम</a>' % (scheme_url(lang, s["slug"]), s["icon"])
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
    H += '<div class="block"><h2>इस योजना की अन्य गाइड</h2><div class="related">%s<a href="%s">%s पूरी जानकारी</a></div></div>' % (rel, scheme_url(lang, s["slug"]), s["icon"])
    H += "</div>"
    H += footer(lang)
    H += "</body></html>"
    return H

'''
    anchor = "def render_sitemap():"
    if anchor in gen:
        gen = gen.replace(anchor, FUNC + anchor, 1)
        print("  B2 applied")
    else:
        print("  B2 FAIL: anchor missing"); sys.exit(1)
else:
    print("  B2 already OK")

# ---- B3 sitemap ----
if not checks["B3 sitemap"]:
    anchor = """        for sl in STATIC_SLUGS:
            urls.append(SITE + static_url(lang, sl))"""
    fix = """        for sl in STATIC_SLUGS:
            urls.append(SITE + static_url(lang, sl))
    for sslug, subs in SUBPAGES.items():
        for sp in subs:
            urls.append(SITE + "/" + sslug + "/" + sp["slug"])"""
    if anchor in gen:
        gen = gen.replace(anchor, fix, 1)
        print("  B3 applied")
    else:
        print("  B3 WARN: anchor not found — sitemap skip (add manually later)")
else:
    print("  B3 already OK")

# ---- B4 build loop ----
if not checks["B4 build loop"]:
    anchor = "            w(p, render_scheme(s, lang)); n += 1"
    fix = """            w(p, render_scheme(s, lang)); n += 1
            if lang == "hi":
                for sp in SUBPAGES.get(s["slug"], []):
                    w(s["slug"] + "/" + sp["slug"] + ".html", render_subpage(s, sp)); n += 1"""
    if anchor in gen:
        gen = gen.replace(anchor, fix, 1)
        print("  B4 applied")
    else:
        print("  B4 FAIL: anchor missing")
        # Show what the actual line looks like
        for ln in gen.split("\n"):
            if "render_scheme(s, lang)" in ln:
                print("  actual line: [%s]" % ln)
        sys.exit(1)
else:
    print("  B4 already OK")

# ---- B5 hub links ----
if not checks["B5 hub links"]:
    anchor = """    H += '<div class="block"><h2>%s</h2><p>%s</p></div>' % (e(t["sec_what"]), e(c["intro"]))"""
    fix = """    H += '<div class="block"><h2>%s</h2><p>%s</p></div>' % (e(t["sec_what"]), e(c["intro"]))
    sp_guides = SUBPAGES.get(s["slug"], [])
    if lang == "hi" and sp_guides:
        g = ''.join('<a href="/%s/%s">📄 %s</a>' % (s["slug"], x["slug"], e(x["nav"])) for x in sp_guides)
        H += '<div class="block"><h2>विस्तृत गाइड</h2><div class="related">%s</div></div>' % g"""
    if anchor in gen:
        gen = gen.replace(anchor, fix, 1)
        print("  B5 applied")
    else:
        print("  B5 WARN: anchor not found — hub links skip")
else:
    print("  B5 already OK")

write("generate.py", gen)

# Syntax verify
import py_compile
try:
    py_compile.compile(os.path.join(REPO, "generate.py"), doraise=True)
    print("\n  Syntax OK after repair!")
except py_compile.PyCompileError as ex:
    print("\n  SYNTAX BROKEN after repair:")
    print(str(ex)[:600])
    sys.exit(1)

print("\n=== REBUILD ===")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r != 0:
    print("BUILD ERROR — send output to Claude"); sys.exit(1)

ok = True
for f in ["pm-kisan/status.html", "pm-kisan/ekyc.html", "pm-kisan/installment-date.html",
          "pm-kisan/beneficiary-list.html", "pm-kisan/registration.html", "pm-kisan/helpline.html"]:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        print("  OK: /%s (%d bytes)" % (f.replace(".html", ""), os.path.getsize(fp)))
    else:
        print("  MISSING: " + f); ok = False

if ok:
    print("""
ALL 6 SUBPAGES CREATED! Preview:
  start chrome "C:\\Users\\Quimztech\\sarkariyojnamitra\\pm-kisan\\status.html"

Then push:
  git add -A
  git commit -m "Subpage engine live: PM Kisan 6 pages"
  git push origin main
""")
else:
    print("Still missing — send full output to Claude")
