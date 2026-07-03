#!/usr/bin/env python3
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

GA4_ID = "G-YQ7KBCEX94"

# BROKEN version (single quotes break Python string)
BROKEN = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA4_ID + '"></script>'
          '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
          "gtag('js',new Date());gtag('config','" + GA4_ID + "');</script>")

# FIXED version (double quotes in JS - safe inside single-quoted Python string)
FIXED = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA4_ID + '"></script>'
         '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
         'gtag("js",new Date());gtag("config","' + GA4_ID + '");</script>')

print("Fixing GA4 tag in generate.py ...")
gen = read("generate.py")

if BROKEN in gen:
    gen = gen.replace(BROKEN, FIXED)
    write("generate.py", gen)
    print("  Done: GA4 tag fixed (double quotes in JS)")
elif FIXED in gen:
    print("  Skip: already fixed")
else:
    print("  Broken pattern not found exactly - trying line-level fix ...")
    # Find the line with gtag('js' and fix quotes
    lines = gen.split("\n")
    fixed_any = False
    for i, line in enumerate(lines):
        if "googletagmanager.com/gtag/js" in line and "gtag('js'" in line:
            lines[i] = line.replace("gtag('js',new Date());gtag('config','" + GA4_ID + "');",
                                    'gtag("js",new Date());gtag("config","' + GA4_ID + '");')
            fixed_any = True
            print("  Done: fixed line " + str(i+1))
    if fixed_any:
        gen = "\n".join(lines)
        write("generate.py", gen)
    else:
        print("  ERROR: could not locate broken GA4 line. Manual fix needed.")
        print("  Open generate.py line ~182-186 and change single quotes in gtag() to double quotes")
        sys.exit(1)

print("\nRebuilding site ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r == 0:
    print("  Site rebuilt OK!")
    with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as fh:
        idx = fh.read()
    if GA4_ID in idx:
        print("  Verified: GA4 tag present in index.html")
    else:
        print("  WARNING: GA4 tag NOT in index.html")
else:
    print("  ERROR - check syntax above")
    sys.exit(1)

print("""
DONE! Run:
  git add -A
  git commit -m "Fix GA4 tag syntax"
  git push origin main
""")
