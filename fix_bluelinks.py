#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix blue content links -> vermillion. Run: python fix_bluelinks.py"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

gen = read("generate.py")
print("Fixing blue content links ...")

# Add link styling for content areas after the base a{} rule
anchor = 'a{color:inherit;text-decoration:none}'
addition = ('''a{color:inherit;text-decoration:none}
.block a,.block p a,.block li a,.faq span a,.sp-hero p a{color:var(--o);text-decoration:underline;text-underline-offset:2px;font-weight:600;word-break:break-word}
.block a:hover,.faq span a:hover{color:#B8460A}
a{-webkit-tap-highlight-color:rgba(228,89,10,.12)}''')

if '.block a,.block p a' in gen:
    print("  Already fixed")
elif anchor in gen:
    gen = gen.replace(anchor, addition, 1)
    write("generate.py", gen)
    print("  Done: content links now vermillion + underline")
else:
    print("  ERROR: base anchor rule not found")
    sys.exit(1)

import py_compile
try:
    py_compile.compile(os.path.join(REPO, "generate.py"), doraise=True)
    print("  Syntax OK")
except py_compile.PyCompileError as ex:
    print("  ERROR:"); print(str(ex)[:400]); sys.exit(1)

print("\nRebuilding ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r != 0:
    print("BUILD ERROR"); sys.exit(1)
print("  Rebuilt OK!")

print("""
DONE! Push:
  git add -A
  git commit -m "Fix blue content links to vermillion"
  git push origin main
""")
