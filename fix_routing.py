#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Cloudflare Pages routing: subpages as /slug/subslug/index.html
Also cleans up old flat .html subpage files.
Run: python fix_routing.py
"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

print("1. Patching generate.py build loop for folder-style subpages ...")
gen = read("generate.py")

# The current build loop writes: s["slug"] + "/" + sp["slug"] + ".html"
# Change to: s["slug"] + "/" + sp["slug"] + "/index.html"
old = 'w(s["slug"] + "/" + sp["slug"] + ".html", render_subpage(s, sp)); n += 1'
new = 'w(s["slug"] + "/" + sp["slug"] + "/index.html", render_subpage(s, sp)); n += 1'

if old in gen:
    gen = gen.replace(old, new)
    write("generate.py", gen)
    print("  Done: build loop now outputs folder-style /slug/subslug/index.html")
elif new in gen:
    print("  Already folder-style")
else:
    print("  ERROR: build loop line not found. Searching for actual line...")
    for ln in gen.split("\n"):
        if 'render_subpage(s, sp)' in ln and 'w(' in ln:
            print("  actual: [%s]" % ln.strip())
    sys.exit(1)

# Also need to check the 'w' helper - does it create subdirectories?
# Find the w() function
print("\n2. Checking w() helper creates nested directories ...")
if "os.makedirs" in gen:
    print("  w() already creates directories (os.makedirs present)")
else:
    # Find def w( and ensure makedirs
    idx = gen.find("def w(")
    if idx > 0:
        snippet = gen[idx:idx+300]
        print("  w() function found. Checking...")
        if "makedirs" not in snippet:
            # Patch w to create dirs
            # Typical: def w(path, content): ... open(os.path.join(OUT, path)...
            old_w = gen[idx:gen.find("\n\n", idx)]
            print("  Current w():")
            print("  " + old_w.replace("\n", "\n  "))
    
print("\n3. Rebuilding ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r != 0:
    print("  BUILD ERROR — send output to Claude")
    sys.exit(1)

print("\n4. Verify folder-style outputs ...")
ok = True
for f in ["pm-kisan/status/index.html", "pm-kisan/ekyc/index.html",
          "ayushman-bharat/card-download/index.html", "pm-awas-yojana/status/index.html",
          "pm-mudra-loan/apply/index.html"]:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        print("  OK: %s" % f)
    else:
        print("  MISSING: %s" % f); ok = False

# Clean up old flat .html files (they'd cause duplicate content)
print("\n5. Cleaning old flat subpage files ...")
import subpages_data
for sslug, subs in subpages_data.SUBPAGES.items():
    for sp in subs:
        old_flat = os.path.join(REPO, sslug, sp["slug"] + ".html")
        if os.path.exists(old_flat):
            os.remove(old_flat)
            print("  Removed old: %s/%s.html" % (sslug, sp["slug"]))

if ok:
    print("""
SUCCESS — subpages now folder-style (Cloudflare-compatible)!
Push:
  git add -A
  git commit -m "Fix: folder-style subpage routing for Cloudflare"
  git push origin main

After deploy (2-3 min), test:
  sarkariyojnamitra.com/pm-kisan/status
  sarkariyojnamitra.com/ayushman-bharat/card-download
""")
else:
    print("Some missing — send output to Claude")
