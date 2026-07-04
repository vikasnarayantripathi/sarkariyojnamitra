#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINAL FIX: apply missing build loop (B4). Run: python final_fix.py"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

gen = read("generate.py")

# Correct detection: look for the WRITE CALL, not the function name
if 'w(s["slug"] + "/" + sp["slug"]' in gen:
    print("Build loop already present — something else is wrong. Send output to Claude.")
else:
    anchor = '            w(p, render_scheme(s, lang)); n += 1'
    fix = '''            w(p, render_scheme(s, lang)); n += 1
            if lang == "hi":
                for sp in SUBPAGES.get(s["slug"], []):
                    w(s["slug"] + "/" + sp["slug"] + ".html", render_subpage(s, sp)); n += 1'''
    if anchor in gen:
        gen = gen.replace(anchor, fix, 1)
        write("generate.py", gen)
        print("B4 build loop APPLIED (this was the missing piece)")
    else:
        print("Anchor not found. Actual lines containing render_scheme call:")
        for ln in gen.split("\n"):
            if "render_scheme(s, lang)" in ln and "def " not in ln:
                print("  [%s]" % ln)
        sys.exit(1)

# Syntax check
import py_compile
try:
    py_compile.compile(os.path.join(REPO, "generate.py"), doraise=True)
    print("Syntax OK")
except py_compile.PyCompileError as ex:
    print("SYNTAX ERROR:"); print(str(ex)[:600]); sys.exit(1)

print("\nRebuilding ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r != 0:
    print("BUILD ERROR"); sys.exit(1)

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
SUCCESS — ALL 6 SUBPAGES BUILT!
Preview:
  start chrome "C:\\Users\\Quimztech\\sarkariyojnamitra\\pm-kisan\\status.html"
Push:
  git add -A
  git commit -m "PM Kisan 6 subpages live"
  git push origin main
""")
else:
    print("Still missing — send output to Claude")
