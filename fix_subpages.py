#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix the literal \\n corruption in generate.py, then rebuild."""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

print("Fixing generate.py ...")
gen = read("generate.py")

# The corrupted text contains LITERAL backslash-n (2 chars), written on one line.
BROKEN = "OUT = os.path.dirname(os.path.abspath(__file__))\\ntry:\\n    from subpages_data import SUBPAGES\\nexcept Exception:\\n    SUBPAGES = {}"
FIXED = "OUT = os.path.dirname(os.path.abspath(__file__))\ntry:\n    from subpages_data import SUBPAGES\nexcept Exception:\n    SUBPAGES = {}"

if BROKEN in gen:
    gen = gen.replace(BROKEN, FIXED)
    write("generate.py", gen)
    print("  Done: literal \\n corruption fixed")
elif "from subpages_data import SUBPAGES" in gen and BROKEN not in gen:
    print("  Looks already fixed or differently corrupted — checking syntax ...")
else:
    print("  Pattern not found — trying generic repair ...")
    # Generic: any remaining literal \n on the OUT line
    lines = gen.split("\n")
    for i, ln in enumerate(lines):
        if "\\ntry:" in ln and "SUBPAGES" in ln:
            lines[i] = ln.replace("\\n", "\n")
            print("  Fixed line %d" % (i+1))
    gen = "\n".join(lines)
    write("generate.py", gen)

# Syntax check
print("\nSyntax check ...")
import py_compile
try:
    py_compile.compile(os.path.join(REPO, "generate.py"), doraise=True)
    print("  generate.py syntax OK!")
except py_compile.PyCompileError as ex:
    print("  STILL BROKEN:")
    print(str(ex)[:500])
    sys.exit(1)

try:
    py_compile.compile(os.path.join(REPO, "subpages_data.py"), doraise=True)
    print("  subpages_data.py syntax OK!")
except py_compile.PyCompileError as ex:
    print("  subpages_data.py BROKEN:")
    print(str(ex)[:500])
    sys.exit(1)

print("\nRebuilding ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r == 0:
    print("  Rebuilt OK!")
    ok = True
    for f in ["pm-kisan/status.html", "pm-kisan/ekyc.html", "pm-kisan/installment-date.html",
              "pm-kisan/beneficiary-list.html", "pm-kisan/registration.html", "pm-kisan/helpline.html"]:
        fp = os.path.join(REPO, f)
        if os.path.exists(fp):
            print("  OK: /%s (%d bytes)" % (f.replace(".html", ""), os.path.getsize(fp)))
        else:
            print("  MISSING: " + f); ok = False
    if not ok:
        print("  Some subpages missing — send output to Claude")
else:
    print("  BUILD ERROR — send output to Claude")
    sys.exit(1)

print("""
DONE! Preview:
  start chrome "C:\\Users\\Quimztech\\sarkariyojnamitra\\pm-kisan\\status.html"

Then push:
  git add -A
  git commit -m "Fix: subpage engine working"
  git push origin main
""")
