#!/usr/bin/env python3
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

GA4_ID = "G-YQ7KBCEX94"

GA4_TAG = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + GA4_ID + '"></script>'
           '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
           "gtag('js',new Date());gtag('config','" + GA4_ID + "');</script>")

print("Adding GA4 tracking (" + GA4_ID + ") to generate.py ...")
gen = read("generate.py")

if GA4_ID in gen:
    print("  Skip: GA4 already added")
else:
    # Add GA4 tag right before the AdSense script in head()
    adsense_marker = '<script async src="https://pagead2.googlesyndication.com'
    if adsense_marker in gen:
        gen = gen.replace(adsense_marker, GA4_TAG + adsense_marker, 1)
        write("generate.py", gen)
        print("  Done: GA4 tag added before AdSense script")
    else:
        print("  ERROR: Could not find AdSense script marker")
        sys.exit(1)

print("\nRebuilding site ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r == 0:
    print("  Site rebuilt OK!")
    # Verify GA4 in output
    with open(os.path.join(REPO, "index.html"), "r", encoding="utf-8") as fh:
        idx = fh.read()
    if GA4_ID in idx:
        print("  Verified: GA4 tag present in index.html")
    else:
        print("  WARNING: GA4 tag NOT in index.html!")
else:
    print("  ERROR!")
    sys.exit(1)

print("""
DONE! Run:
  git add -A
  git commit -m "Add GA4 tracking G-YQ7KBCEX94"
  git push origin main

Deploy ke 5 min baad Analytics me "Test installation" button dabana
ya Realtime report kholna — apna visit dikhega.
""")
