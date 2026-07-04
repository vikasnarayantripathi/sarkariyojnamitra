#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnose subpage routing. Run: python diag.py"""
import os

REPO = os.path.dirname(os.path.abspath(__file__))

print("=== LOCAL FILE CHECK ===")
checks = [
    "index.html",
    "favicon.svg",
    "pm-kisan/status.html",
    "pm-kisan/ekyc.html",
    "ayushman-bharat/card-download.html",
    "pm-awas-yojana/status.html",
    "_redirects",
    "_routes.json",
]
for f in checks:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        sz = os.path.getsize(fp)
        # Check if pm-kisan/status.html actually has status content or is a copy of home
        tag = ""
        if f.endswith(".html") and "/" in f:
            with open(fp, "r", encoding="utf-8") as fh:
                content = fh.read()
            if "किस्त स्टेटस कैसे चेक" in content or "Beneficiary Status" in content or "e-KYC कैसे" in content or "card-download" in f:
                tag = " [correct subpage content]"
            elif "आपके लिए कौन" in content or 'id="grid"' in content:
                tag = " [WARNING: looks like homepage content!]"
        print("  EXISTS: %s (%d bytes)%s" % (f, sz, tag))
    else:
        print("  --none: %s" % f)

# Check if there's a _redirects or Cloudflare config causing catch-all
print("\n=== CLOUDFLARE ROUTING FILES ===")
for cfg in ["_redirects", "_routes.json", "wrangler.toml", "functions"]:
    fp = os.path.join(REPO, cfg)
    if os.path.exists(fp):
        print("  FOUND: %s" % cfg)
        if os.path.isfile(fp):
            with open(fp, "r", encoding="utf-8") as fh:
                print("    content: " + fh.read()[:300])
    else:
        print("  not present: %s" % cfg)

# Verify the actual content difference
print("\n=== CONTENT SAMPLE: pm-kisan/status.html (first 400 chars of body) ===")
fp = os.path.join(REPO, "pm-kisan/status.html")
if os.path.exists(fp):
    with open(fp, "r", encoding="utf-8") as fh:
        c = fh.read()
    bi = c.find("<h1>")
    print(c[bi:bi+300] if bi > 0 else "no h1 found")

print("""
=== LIKELY CAUSE ===
Cloudflare Pages serves /pm-kisan/status by looking for:
  1. pm-kisan/status/index.html  (folder style)  <- NOT what we have
  2. pm-kisan/status.html         (file style)   <- what we have

If Cloudflare's setting is folder-style, /pm-kisan/status won't find
status.html and falls back to serving index.html (the 404/SPA fallback).

FIX: Either (A) output folder-style index.html files, OR
     (B) rely on Cloudflare's automatic .html matching (usually works).

Run the fix script Claude will provide next.
""")
