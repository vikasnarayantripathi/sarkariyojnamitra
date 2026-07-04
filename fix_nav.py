#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix nav: About links to /about, not #schemes. Run: python fix_nav.py"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

gen = read("generate.py")
print("Fixing nav links ...")

# The header builds nav from zip(["schemes","finder","tools","schemes"], t["nav"])
# The 4th should be "about" (a static page), and anchor() only handles homepage #anchors.
# We need About to use static_url, not anchor. Rewrite the nav-building line.

old_nav = '''    nav = ''.join('<a href="%s">%s</a>' % (anchor(lang, a), e(n))
                  for a, n in zip(["schemes","finder","tools","schemes"], t["nav"]))'''

new_nav = '''    _navkeys = ["schemes","finder","tools","about"]
    _navhrefs = [anchor(lang,"schemes"), anchor(lang,"finder"), anchor(lang,"tools"), static_url(lang,"about")]
    nav = ''.join('<a href="%s">%s</a>' % (h, e(n))
                  for h, n in zip(_navhrefs, t["nav"]))'''

if 'zip(["schemes","finder","tools","schemes"], t["nav"])' in gen:
    gen = gen.replace(old_nav, new_nav)
    print("  Done: 4th nav item (About) now links to /about page")
elif '_navhrefs' in gen:
    print("  Already fixed")
else:
    print("  ERROR: nav pattern not found. Actual header nav lines:")
    for i, ln in enumerate(gen.split("\n")):
        if "zip([" in ln and "nav" in ln:
            print("  line %d: [%s]" % (i+1, ln.strip()))
    sys.exit(1)

write("generate.py", gen)

import py_compile
try:
    py_compile.compile(os.path.join(REPO, "generate.py"), doraise=True)
    print("  Syntax OK")
except py_compile.PyCompileError as ex:
    print("  SYNTAX ERROR:"); print(str(ex)[:400]); sys.exit(1)

print("\nRebuilding ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r != 0:
    print("BUILD ERROR"); sys.exit(1)

# Verify /about link present in nav of index
with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as fh:
    idx = fh.read()
if 'href="/about"' in idx:
    print("  Verified: About links to /about in nav")
else:
    print("  Check: /about link — verify manually")

print("""
DONE! Push:
  git add -A
  git commit -m "Fix nav: About links to /about page"
  git push origin main
""")
