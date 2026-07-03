#!/usr/bin/env python3
import os, sys
from datetime import date

REPO = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().strftime("%Y-%m-%d")
TODAY_HI = date.today().strftime("%d/%m/%Y")

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

# ─────────────────────────────────────
# 1. ADD article:modified_time + OG tags to head()
# ─────────────────────────────────────
print("1. Adding OG tags + article:modified_time to generate.py ...")
gen = read("generate.py")

old_head = ("'<title>%s</title><meta name=\"description\" content=\"%s\">'")
new_head = ("'<title>%s</title><meta name=\"description\" content=\"%s\">'\n"
            "            '<meta property=\"og:title\" content=\"%s\"><meta property=\"og:description\" content=\"%s\">'\n"
            "            '<meta property=\"og:type\" content=\"article\"><meta property=\"og:locale\" content=\"%s\">'\n"
            "            '<meta property=\"article:modified_time\" content=\"" + TODAY + "\">'")

# This is tricky because the format string uses %s. Let me use a simpler approach.
# Instead, add the OG/modified tags right after the description meta tag

og_meta = ('<meta property="og:type" content="article">'
           '<meta property="article:modified_time" content="' + TODAY + '">')

if "article:modified_time" not in gen:
    # Add after description meta tag
    old = '<meta name="description" content="%s">'
    new = '<meta name="description" content="%s">' + og_meta
    if old in gen:
        gen = gen.replace(old, new, 1)  # Only first occurrence
        print("  Done: OG + modified_time added")
    else:
        print("  Skip: could not find description meta tag")
else:
    print("  Skip: already has article:modified_time")

write("generate.py", gen)

# ─────────────────────────────────────
# 2. ADD visible "Last Updated" date on scheme pages
# ─────────────────────────────────────
print("\n2. Adding visible 'Last Updated' date to scheme pages ...")
gen = read("generate.py")

# Find where the scheme page intro is rendered and add a date before it
# Looking for the intro paragraph rendering
if 'class="updated"' not in gen:
    # Add a date line before the intro
    old_intro = "e(t[\"lbl_ministry\"])"
    if old_intro in gen:
        # Find the complete line and add date after the h1
        old_h1 = '<h1>%s</h1>'
        new_h1 = '<h1>%s</h1><p class="updated">अंतिम अपडेट: ' + TODAY_HI + '</p>'
        if old_h1 in gen and 'class="updated"' not in gen:
            gen = gen.replace(old_h1, new_h1, 1)
            print("  Done: Last updated date added")
        else:
            print("  Skip: h1 pattern not found or already exists")
    else:
        print("  Skip: intro pattern not found")
else:
    print("  Skip: already has updated date")

# Add CSS for .updated
if '.updated' not in gen:
    old_css = '.faq b{cursor:pointer}'
    new_css = '.faq b{cursor:pointer}\n.updated{font-size:.85rem;color:#777;margin:-.5rem 0 1rem;}'
    if old_css in gen:
        gen = gen.replace(old_css, new_css)
        print("  Done: CSS for .updated added")

write("generate.py", gen)

# ─────────────────────────────────────
# 3. EXPAND Privacy page (Hindi)
# ─────────────────────────────────────
print("\n3. Expanding Privacy page content ...")
sd = read("schemes_data.py")

PRIVACY_BODY = """<p><b>अंतिम अपडेट:</b> """ + TODAY_HI + """</p>
<p>Sarkari Yojna Mitra ("हम", "हमारी", "वेबसाइट") आपकी गोपनीयता का सम्मान करती है। यह गोपनीयता नीति बताती है कि जब आप <b>sarkariyojnamitra.com</b> पर आते हैं तो हम कौन-सी जानकारी एकत्र करते हैं, उसका उपयोग कैसे करते हैं, और उसे कैसे सुरक्षित रखते हैं। इस वेबसाइट का संचालन <b>Quimztech Solutions</b>, वाराणसी, उत्तर प्रदेश, भारत द्वारा किया जाता है।</p>
<h2>1. हम कौन-सी जानकारी एकत्र करते हैं?</h2>
<p><b>स्वचालित रूप से:</b> जब आप वेबसाइट पर आते हैं, तो आपका IP पता, ब्राउज़र प्रकार, ऑपरेटिंग सिस्टम, देखे गए पेज, रेफ़रर URL, डिवाइस प्रकार, और भौगोलिक स्थान (शहर/राज्य स्तर) स्वचालित रूप से एकत्र हो सकता है।</p>
<p><b>संपर्क फ़ॉर्म:</b> यदि आप हमसे संपर्क करते हैं, तो हम आपका नाम और ईमेल एकत्र कर सकते हैं — केवल उत्तर देने के लिए।</p>
<p><b>हम क्या एकत्र नहीं करते:</b> हम आपका आधार नंबर, बैंक खाता, पासवर्ड, या कोई संवेदनशील व्यक्तिगत जानकारी एकत्र <b>नहीं</b> करते। कोई लॉगिन/रजिस्ट्रेशन नहीं है।</p>
<h2>2. कुकीज़ (Cookies)</h2>
<p><b>आवश्यक कुकीज़:</b> पेज लोड करने और भाषा प्राथमिकता के लिए।</p>
<p><b>एनालिटिक्स कुकीज़ (Google Analytics):</b> ट्रैफ़िक विश्लेषण के लिए अनाम डेटा एकत्र करती है। विवरण: <a href="https://policies.google.com/privacy">Google गोपनीयता नीति</a>।</p>
<p><b>विज्ञापन कुकीज़ (Google AdSense):</b> आपकी रुचि अनुसार विज्ञापन दिखाने के लिए। वैयक्तिकृत विज्ञापन बंद करें: <a href="https://adssettings.google.com/">Google Ads Settings</a>। आप ब्राउज़र सेटिंग्स से कुकीज़ अक्षम कर सकते हैं।</p>
<h2>3. तृतीय-पक्ष सेवाएँ</h2>
<p>हम <b>Google AdSense</b> (विज्ञापन), <b>Google Analytics</b> (ट्रैफ़िक विश्लेषण), और <b>Cloudflare</b> (सुरक्षा, CDN) का उपयोग करते हैं। इन सेवाओं की अपनी गोपनीयता नीतियाँ हैं।</p>
<h2>4. जानकारी का उपयोग</h2>
<p>एकत्र जानकारी का उपयोग: वेबसाइट अनुभव सुधारने, लोकप्रिय सामग्री समझने, तकनीकी समस्याओं के निदान, विज्ञापन प्रदर्शित करने, और संपर्क संदेशों का उत्तर देने के लिए किया जाता है। <b>हम आपकी जानकारी किसी को बेचते नहीं।</b></p>
<h2>5. डेटा सुरक्षा</h2>
<p>SSL/TLS एन्क्रिप्शन (HTTPS) और Cloudflare सुरक्षा (DDoS + WAF) उपयोग करते हैं। इंटरनेट पर 100% सुरक्षा की गारंटी नहीं दी जा सकती।</p>
<h2>6. बच्चों की गोपनीयता</h2>
<p>हमारी वेबसाइट 13 वर्ष से कम आयु के बच्चों से जानबूझकर जानकारी एकत्र नहीं करती।</p>
<h2>7. बाहरी लिंक</h2>
<p>सरकारी पोर्टलों (.gov.in) और अन्य बाहरी वेबसाइटों के लिंक उपयोगकर्ता सुविधा के लिए हैं। हम उनकी सामग्री के लिए ज़िम्मेदार नहीं।</p>
<h2>8. भारतीय कानून के तहत अधिकार</h2>
<p>सूचना प्रौद्योगिकी अधिनियम 2000 (IT Act) और डिजिटल व्यक्तिगत डेटा संरक्षण अधिनियम 2023 (DPDP Act) के अनुसार, आपको अपने डेटा को जानने, सुधारने, हटाने, और सहमति वापस लेने का अधिकार है। संपर्क: <a href="mailto:quimztech@gmail.com">quimztech@gmail.com</a></p>
<h2>9. नीति में परिवर्तन</h2>
<p>हम समय-समय पर इस नीति को अपडेट कर सकते हैं। परिवर्तन इस पेज पर प्रकाशित होंगे।</p>
<h2>10. संपर्क</h2>
<p><b>ईमेल:</b> <a href="mailto:quimztech@gmail.com">quimztech@gmail.com</a> · <b>संचालक:</b> Quimztech Solutions, वाराणसी, उत्तर प्रदेश, भारत</p>"""

# Find and replace Hindi privacy body
# The body is a multi-line string between "body": and the closing of the privacy block
import re

# Find the first privacy block's body
priv_pos = sd.find('"privacy":{')
if priv_pos > 0:
    body_start = sd.find('"body":', priv_pos)
    if body_start > 0 and body_start < priv_pos + 2000:
        # Find the end of body value - it ends with the next key or closing }
        # The body is either a simple string or triple-quoted
        # Let's find the closing of privacy block
        # Look for the next key at the same indent level
        
        # Simple approach: replace everything between "body": and the closing },
        # Find next "}" that closes the privacy dict
        depth = 0
        priv_brace = sd.find('{', priv_pos)
        priv_end = priv_brace
        for i in range(priv_brace, len(sd)):
            if sd[i] == '{': depth += 1
            elif sd[i] == '}':
                depth -= 1
                if depth == 0:
                    priv_end = i + 1
                    break
        
        old_priv = sd[priv_pos:priv_end]
        
        new_priv = ('"privacy":{\n'
                   '   "title":"गोपनीयता नीति | Sarkari Yojna Mitra",\n'
                   '   "desc":"Sarkari Yojna Mitra की गोपनीयता नीति — डेटा संग्रह, कुकीज़, Google AdSense, DPDP Act, और आपके अधिकारों की जानकारी।",\n'
                   '   "h1":"गोपनीयता नीति (Privacy Policy)",\n'
                   '   "body":' + repr(PRIVACY_BODY) + '\n'
                   '  }')
        
        sd = sd[:priv_pos] + new_priv + sd[priv_end:]
        print("  Done: Hindi privacy page expanded (10 sections, DPDP Act)")
    else:
        print("  Skip: body not found in privacy")
else:
    print("  Skip: privacy block not found")

write("schemes_data.py", sd)

# ─────────────────────────────────────
# 4. CREATE llms.txt
# ─────────────────────────────────────
print("\n4. Creating llms.txt ...")

llms_content = """# Sarkari Yojna Mitra — sarkariyojnamitra.com

## About
Sarkari Yojna Mitra is an independent informational portal providing comprehensive details about Indian government schemes (Central & State) in Hindi and English. Operated by Quimztech Solutions, Varanasi, Uttar Pradesh, India.

## What This Site Covers
- 90+ government schemes across 27+ categories
- Central schemes: PM Kisan, Ayushman Bharat, PM Awas, Mudra, KCC, Fasal Bima, Sukanya Samriddhi, Atal Pension, Ujjwala, e-Shram, PM Vishwakarma, PM SVANidhi, etc.
- State schemes from: Uttar Pradesh, Bihar, Maharashtra, Madhya Pradesh, Delhi, Rajasthan, Karnataka, Tamil Nadu, Kerala, West Bengal, Gujarat, Telangana, Andhra Pradesh, Jharkhand, Chhattisgarh, Punjab, Haryana, Uttarakhand, Himachal Pradesh, Assam, Odisha, Goa, J&K, Meghalaya, Mizoram, Arunachal Pradesh

## For Each Scheme We Provide
- Eligibility criteria (who qualifies and who doesn't)
- Required documents
- Step-by-step application process (online + offline)
- Benefits with specific amounts
- Official portal links and helpline numbers
- 5-7 frequently asked questions with detailed answers

## Languages
- Hindi (primary): sarkariyojnamitra.com
- English: sarkariyojnamitra.com/en/

## Disclaimer
This is NOT an official government website. We are not affiliated with any government ministry or department. Information is compiled from public sources for general guidance. Always verify on official .gov.in portals before applying.

## Contact
- Email: quimztech@gmail.com
- Operator: Quimztech Solutions, Varanasi, UP, India
- Website: https://sarkariyojnamitra.com
"""

write("llms.txt", llms_content)
print("  Done: llms.txt created")

# Also add llms.txt to generate.py build output
gen = read("generate.py")
if 'w("llms.txt"' not in gen:
    if 'w("ads.txt"' in gen:
        gen = gen.replace(
            'w("ads.txt"',
            'w("llms.txt", open(os.path.join(OUT,"llms.txt"),"r",encoding="utf-8").read())\n    w("ads.txt"'
        )
        write("generate.py", gen)
        print("  Done: llms.txt added to build output")
    else:
        print("  Skip: could not add llms.txt to build")
else:
    print("  Skip: llms.txt already in build")

# ─────────────────────────────────────
# 5. UPDATE robots.txt to include llms.txt
# ─────────────────────────────────────
print("\n5. Updating robots.txt with llms.txt reference ...")
robots = read("robots.txt")
if "llms.txt" not in robots:
    robots = robots.rstrip() + "\n\n# LLM metadata\nLlms-txt: https://sarkariyojnamitra.com/llms.txt\n"
    write("robots.txt", robots)
    print("  Done: llms.txt reference added to robots.txt")
else:
    print("  Skip: already has llms.txt")

# ─────────────────────────────────────
# 6. REBUILD
# ─────────────────────────────────────
print("\n6. Rebuilding site ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r == 0:
    print("  Site rebuilt OK!")
    # Verify
    for f in ["llms.txt", "ads.txt", "robots.txt", "privacy.html", "disclaimer.html"]:
        fp = os.path.join(REPO, f)
        if os.path.exists(fp):
            print("  OK: " + f + " (" + str(os.path.getsize(fp)) + " bytes)")
else:
    print("  ERROR!")
    sys.exit(1)

print("""
DONE! Run:
  git add -A
  git commit -m "SEO: privacy expand, OG tags, last-updated, llms.txt"
  git push origin main

THEN MANUAL STEPS:
  1. Google Search Console → Sitemaps → Resubmit sitemap.xml
  2. URL Inspection → /disclaimer → Request Indexing
  3. URL Inspection → /terms → Request Indexing
  4. Google Analytics → Add sarkariyojnamitra.com property
""")
