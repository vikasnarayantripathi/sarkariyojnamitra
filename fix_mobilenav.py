#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix mobile navigation. Run: python fix_mobilenav.py"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

gen = read("generate.py")

print("Fixing mobile nav CSS ...")

# Replace the mobile media query block that hides nav
old_mobile = ''' nav a:not(.lang){display:none}'''
new_mobile = ''' nav{gap:10px;flex-wrap:wrap;justify-content:flex-end}
 nav a{font-size:.82rem}
 .logo small{display:none}
 .logo b{font-size:.98rem}'''

if 'nav a:not(.lang){display:none}' in gen:
    gen = gen.replace(old_mobile, new_mobile)
    print("  Done: nav links now visible on mobile (compact, wrapped)")
elif 'nav{gap:10px;flex-wrap:wrap' in gen:
    print("  Already fixed")
else:
    print("  WARN: mobile nav rule not found, checking...")
    for ln in gen.split("\n"):
        if "nav a:not" in ln or "display:none" in ln and "nav" in ln:
            print("  found: [%s]" % ln.strip())

# Also make header wrap gracefully on very small screens
# Ensure .hd allows wrapping
old_hd = '.hd{display:flex;align-items:center;gap:12px;padding:13px 0}'
new_hd = '.hd{display:flex;align-items:center;gap:12px;padding:13px 0;flex-wrap:wrap}'
if old_hd in gen:
    gen = gen.replace(old_hd, new_hd)
    print("  Done: header wraps gracefully")

write("generate.py", gen)

# Syntax check
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

# Verify nav present in a built page
with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as fh:
    idx = fh.read()
if "flex-wrap:wrap" in idx:
    print("  Verified: mobile nav fix in output")

print("""
DONE! Push:
  git add -A
  git commit -m "Fix mobile navigation visibility"
  git push origin main

Deploy ke baad mobile pe nav links (योजनाएँ, फाइंडर, टूल्स, EN) dikhenge.
""")
