#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SARKARIYOJNAMITRA SEO PATCH SCRIPT
===================================
Run this ONCE from inside your repo folder:
    python patch_seo.py

It will:
1. Update generate.py — add "disclaimer" and "terms" to STATIC_SLUGS + ads.txt build
2. Update schemes_data.py — add disclaimer/terms pages + expand privacy + update footer links
3. Delete old raw HTML files (all-schemas.html, disclaimer.html, terms.html, privacy.html)
4. Run generate.py automatically to rebuild the site
5. Show you what to do next (git add, commit, push)
"""

import os, re, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh:
        return fh.read()

def write(f, content):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  ✅ Updated: {f}")

# ─────────────────────────────────────────────
# 1. PATCH generate.py
# ─────────────────────────────────────────────
print("\n🔧 Step 1: Patching generate.py ...")

gen = read("generate.py")

# 1a. Update STATIC_SLUGS
old_slugs = 'STATIC_SLUGS = ["privacy", "about", "contact"]'
new_slugs = 'STATIC_SLUGS = ["privacy", "about", "contact", "disclaimer", "terms"]'
if old_slugs in gen:
    gen = gen.replace(old_slugs, new_slugs)
    print("  ✅ STATIC_SLUGS updated (added disclaimer, terms)")
elif "disclaimer" in gen and "terms" in gen:
    print("  ⏭️  STATIC_SLUGS already has disclaimer & terms — skipping")
else:
    print("  ❌ Could not find STATIC_SLUGS line — please update manually")

# 1b. Add ads.txt generation (if not already there)
if 'w("ads.txt"' not in gen:
    old_gverify = 'w("google6b8fece3b82b2876.html"'
    if old_gverify in gen:
        gen = gen.replace(
            old_gverify,
            'w("ads.txt", "google.com, pub-3246006644123903, DIRECT, f08c47fec0942fa0\\n")\n    ' + old_gverify
        )
        print("  ✅ ads.txt build step added")
    else:
        print("  ⚠️  Could not auto-add ads.txt build step — add manually")
else:
    print("  ⏭️  ads.txt build already exists — skipping")

write("generate.py", gen)


# ─────────────────────────────────────────────
# 2. PATCH schemes_data.py
# ─────────────────────────────────────────────
print("\n🔧 Step 2: Patching schemes_data.py ...")

sd = read("schemes_data.py")

# ── 2a. Hindi footer links ──
old_hi_foot = '"foot_pages_items":[("privacy","गोपनीयता नीति"),("about","हमारे बारे में"),("contact","संपर्क")]'
new_hi_foot = '"foot_pages_items":[("privacy","गोपनीयता नीति"),("disclaimer","अस्वीकरण"),("terms","उपयोग की शर्तें"),("about","हमारे बारे में"),("contact","संपर्क")]'
if old_hi_foot in sd:
    sd = sd.replace(old_hi_foot, new_hi_foot)
    print("  ✅ Hindi footer links updated")
elif "अस्वीकरण" in sd:
    print("  ⏭️  Hindi footer already has disclaimer — skipping")
else:
    print("  ❌ Could not find Hindi foot_pages_items — update manually")

# ── 2b. English footer links ──
old_en_foot = '"foot_pages_items":[("privacy","Privacy Policy"),("about","About"),("contact","Contact")]'
new_en_foot = '"foot_pages_items":[("privacy","Privacy Policy"),("disclaimer","Disclaimer"),("terms","Terms of Use"),("about","About"),("contact","Contact")]'
if old_en_foot in sd:
    sd = sd.replace(old_en_foot, new_en_foot)
    print("  ✅ English footer links updated")
elif '"disclaimer","Disclaimer"' in sd:
    print("  ⏭️  English footer already has disclaimer — skipping")
else:
    print("  ❌ Could not find English foot_pages_items — update manually")

# ── 2c. Add Hindi disclaimer + terms static pages ──
# We insert AFTER the Hindi "about" block starts — actually, we insert BEFORE "about"
# Strategy: find the Hindi about block and insert disclaimer+terms before it

HI_DISCLAIMER_TERMS = '''  "disclaimer":{
   "title":"अस्वीकरण (Disclaimer) | Sarkari Yojna Mitra",
   "desc":"Sarkari Yojna Mitra अस्वीकरण — यह वेबसाइट किसी सरकारी विभाग की आधिकारिक वेबसाइट नहीं है।",
   "h1":"अस्वीकरण (Disclaimer)",
   "body":"""<p><b>अंतिम अपडेट:</b> 2 जुलाई 2026</p>
<p>Sarkari Yojna Mitra (<b>sarkariyojnamitra.com</b>) एक <b>स्वतंत्र सूचनात्मक वेबसाइट</b> है। कृपया उपयोग से पहले नीचे दिए गए अस्वीकरण को ध्यान से पढ़ें।</p>
<h2>1. सरकारी संबद्धता नहीं</h2>
<p><b>यह वेबसाइट किसी भी सरकारी मंत्रालय, विभाग, एजेंसी या संस्था की आधिकारिक वेबसाइट नहीं है।</b> हम भारत सरकार, किसी राज्य सरकार, या किसी सरकारी निकाय से संबद्ध, प्रायोजित या जुड़े हुए नहीं हैं। इस वेबसाइट का संचालन <b>Quimztech Solutions</b> (एक निजी संस्था, वाराणसी, उत्तर प्रदेश) द्वारा किया जाता है।</p>
<h2>2. जानकारी की सटीकता</h2>
<p>हम हर योजना की जानकारी सटीक रखने का प्रयास करते हैं, लेकिन सरकारी योजनाओं की शर्तें, पात्रता, लाभ राशि और प्रक्रिया समय-समय पर बदल सकती हैं। हम पूर्ण सटीकता या समयबद्धता की गारंटी नहीं देते। <b>आवेदन से पहले संबंधित .gov.in पोर्टल पर पुष्टि अवश्य करें।</b></p>
<h2>3. कानूनी या वित्तीय सलाह नहीं</h2>
<p>यह वेबसाइट सामान्य सूचना प्रदान करती है। यह कानूनी, वित्तीय, कर या पेशेवर सलाह का विकल्प नहीं है। निर्णय लेने से पहले योग्य पेशेवर से परामर्श लें।</p>
<h2>4. बाहरी लिंक</h2>
<p>हम सरकारी पोर्टलों और अन्य वेबसाइटों के लिंक देते हैं जो उपयोगकर्ता की सुविधा के लिए हैं। हम इन बाहरी वेबसाइटों की सामग्री या उपलब्धता के लिए ज़िम्मेदार नहीं हैं।</p>
<h2>5. धोखाधड़ी से सावधान</h2>
<p>असली सरकारी योजनाओं में आवेदन <b>निःशुल्क</b> होता है। किसी एजेंट को पैसे न दें, अनजान लिंक से APK डाउनलोड न करें, अपनी बैंक/OTP जानकारी किसी से साझा न करें। आवेदन केवल <b>.gov.in</b> पोर्टलों से करें। धोखाधड़ी की शिकायत: <b>साइबर क्राइम हेल्पलाइन 1930</b> या <a href="https://cybercrime.gov.in">cybercrime.gov.in</a></p>
<h2>6. विज्ञापन</h2>
<p>यह वेबसाइट Google AdSense विज्ञापन प्रदर्शित कर सकती है। विज्ञापनों की सामग्री का हमारे द्वारा समर्थन नहीं है। विज्ञापनों से संबंधित किसी समस्या के लिए हम उत्तरदायी नहीं हैं।</p>
<h2>7. उत्तरदायित्व की सीमा</h2>
<p>इस वेबसाइट की जानकारी के उपयोग से होने वाले किसी भी नुकसान (आवेदन अस्वीकृति, लाभ न मिलना, ग़लत जानकारी) के लिए Sarkari Yojna Mitra या Quimztech Solutions उत्तरदायी नहीं होंगे।</p>
<h2>8. कॉपीराइट</h2>
<p>मूल सामग्री (लेख, डिज़ाइन, लोगो) © 2026 Quimztech Solutions की संपत्ति है। सरकारी योजनाओं की जानकारी सार्वजनिक स्रोतों से ली गई है।</p>
<h2>9. संपर्क</h2>
<p><b>ईमेल:</b> <a href="mailto:quimztech@gmail.com">quimztech@gmail.com</a> · <b>संचालक:</b> Quimztech Solutions, वाराणसी, उत्तर प्रदेश</p>"""
  },
  "terms":{
   "title":"उपयोग की शर्तें | Sarkari Yojna Mitra",
   "desc":"Sarkari Yojna Mitra उपयोग की शर्तें — वेबसाइट उपयोग के नियम और शर्तें।",
   "h1":"उपयोग की शर्तें (Terms of Use)",
   "body":"""<p><b>अंतिम अपडेट:</b> 2 जुलाई 2026</p>
<p>Sarkari Yojna Mitra (<b>sarkariyojnamitra.com</b>) पर आने का धन्यवाद। इस वेबसाइट का उपयोग करके, आप नीचे दी गई शर्तों से सहमत होते हैं।</p>
<h2>1. वेबसाइट का स्वरूप</h2>
<p>यह एक स्वतंत्र सूचनात्मक वेबसाइट है जो सरकारी योजनाओं की जानकारी सरल हिंदी में देती है। संचालक: <b>Quimztech Solutions</b>, वाराणसी। यह किसी सरकारी संस्था की आधिकारिक वेबसाइट <b>नहीं</b> है।</p>
<h2>2. उपयोग के नियम</h2>
<p>आप सहमत हैं कि: वेबसाइट का उपयोग केवल वैध उद्देश्यों के लिए करेंगे, सामग्री को बिना अनुमति कॉपी/पुनर्प्रकाशित नहीं करेंगे, मैलवेयर या हानिकारक कोड नहीं डालेंगे, और वेबसाइट के संचालन में बाधा नहीं डालेंगे।</p>
<h2>3. बौद्धिक संपदा</h2>
<p>मूल सामग्री (लेख, डिज़ाइन, लोगो, कोड) © 2026 Quimztech Solutions की बौद्धिक संपत्ति है। व्यक्तिगत उपयोग और सोशल मीडिया पर लिंक शेयर करना (उचित श्रेय के साथ) अनुमत है। बड़े पैमाने पर कॉपी, स्क्रैपिंग, या अनधिकृत पुनर्प्रकाशन वर्जित है। सरकारी योजनाओं की तथ्यात्मक जानकारी सार्वजनिक डोमेन में है।</p>
<h2>4. सटीकता और अस्वीकरण</h2>
<p>जानकारी "जैसी है" (as-is) प्रदान की जाती है। सरकारी नीतियाँ बिना पूर्व सूचना बदल सकती हैं। विस्तृत जानकारी के लिए हमारा <a href="/disclaimer">अस्वीकरण</a> पेज देखें।</p>
<h2>5. विज्ञापन</h2>
<p>Google AdSense विज्ञापनों की सामग्री, गुणवत्ता या सटीकता के लिए हम ज़िम्मेदार नहीं हैं।</p>
<h2>6. उत्तरदायित्व की सीमा</h2>
<p>Sarkari Yojna Mitra और Quimztech Solutions किसी भी प्रत्यक्ष या अप्रत्यक्ष हानि के लिए उत्तरदायी नहीं होंगे जो इस वेबसाइट के उपयोग से उत्पन्न हो।</p>
<h2>7. शासी कानून</h2>
<p>ये शर्तें भारतीय कानून द्वारा शासित हैं। किसी विवाद में <b>वाराणसी, उत्तर प्रदेश</b> के न्यायालयों का विशेष क्षेत्राधिकार होगा।</p>
<h2>8. संपर्क</h2>
<p><b>ईमेल:</b> <a href="mailto:quimztech@gmail.com">quimztech@gmail.com</a> · <b>संचालक:</b> Quimztech Solutions, वाराणसी, उत्तर प्रदेश</p>"""
  },
'''

EN_DISCLAIMER_TERMS = '''  "disclaimer":{
   "title":"Disclaimer | Sarkari Yojna Mitra",
   "desc":"Sarkari Yojna Mitra disclaimer — This website is not affiliated with any government department.",
   "h1":"Disclaimer",
   "body":"""<p><b>Last Updated:</b> July 2, 2026</p>
<p>Sarkari Yojna Mitra (<b>sarkariyojnamitra.com</b>) is an <b>independent informational website</b>. Please read this disclaimer carefully.</p>
<h2>1. No Government Affiliation</h2>
<p><b>This website is not an official website of any government ministry, department, or body.</b> We are not affiliated with the Government of India or any state government. Operated by <b>Quimztech Solutions</b> (Varanasi, UP).</p>
<h2>2. Accuracy of Information</h2>
<p>We strive to keep scheme information accurate, but government terms, eligibility, and benefits may change. We do not guarantee complete accuracy. <b>Verify on official .gov.in portals before applying.</b></p>
<h2>3. Not Legal or Financial Advice</h2>
<p>This website provides general information only, not legal, financial, or professional advice. Consult qualified professionals before making decisions.</p>
<h2>4. External Links</h2>
<p>Links to government portals and other websites are for convenience. We are not responsible for their content or availability.</p>
<h2>5. Beware of Fraud</h2>
<p>Government scheme applications are <b>free</b>. Never pay agents, download unknown APKs, or share bank/OTP details. Apply only through <b>.gov.in</b> portals. Report fraud: <b>Cyber Crime Helpline 1930</b> or <a href="https://cybercrime.gov.in">cybercrime.gov.in</a></p>
<h2>6. Advertisements</h2>
<p>Google AdSense ads may appear. We do not endorse advertised content and are not responsible for ad-related issues.</p>
<h2>7. Limitation of Liability</h2>
<p>Sarkari Yojna Mitra and Quimztech Solutions shall not be liable for any damages from using this website's information.</p>
<h2>8. Contact</h2>
<p><b>Email:</b> <a href="mailto:quimztech@gmail.com">quimztech@gmail.com</a> · <b>Operator:</b> Quimztech Solutions, Varanasi, UP, India</p>"""
  },
  "terms":{
   "title":"Terms of Use | Sarkari Yojna Mitra",
   "desc":"Sarkari Yojna Mitra terms of use — rules for using this website.",
   "h1":"Terms of Use",
   "body":"""<p><b>Last Updated:</b> July 2, 2026</p>
<p>By using Sarkari Yojna Mitra (<b>sarkariyojnamitra.com</b>), you agree to these terms.</p>
<h2>1. Nature of Website</h2>
<p>Independent informational website for government schemes. Operated by <b>Quimztech Solutions</b>, Varanasi. <b>Not</b> an official government website.</p>
<h2>2. Acceptable Use</h2>
<p>Use lawfully, do not copy/republish without permission, do not introduce malware, do not interfere with operations.</p>
<h2>3. Intellectual Property</h2>
<p>Original content © 2026 Quimztech Solutions. Personal use and link sharing permitted. Bulk copying or scraping prohibited. Government scheme facts are public domain.</p>
<h2>4. Accuracy</h2>
<p>Information provided "as-is". Government policies may change without notice. See <a href="/en/disclaimer">Disclaimer</a>.</p>
<h2>5. Limitation of Liability</h2>
<p>Not liable for any damages from use of this website.</p>
<h2>6. Governing Law</h2>
<p>Indian law applies. Courts in <b>Varanasi, UP</b> have exclusive jurisdiction.</p>
<h2>7. Contact</h2>
<p><b>Email:</b> <a href="mailto:quimztech@gmail.com">quimztech@gmail.com</a> · <b>Operator:</b> Quimztech Solutions, Varanasi, UP, India</p>"""
  },
'''

# Insert Hindi disclaimer+terms BEFORE the Hindi "about" block
hi_about_marker = '  "about":{'
# Find the first occurrence (Hindi section)
hi_pos = sd.find(hi_about_marker)
if hi_pos > 0 and '"अस्वीकरण"' not in sd[:hi_pos+100]:
    sd = sd[:hi_pos] + HI_DISCLAIMER_TERMS + sd[hi_pos:]
    print("  ✅ Hindi disclaimer + terms pages added")
elif '"अस्वीकरण"' in sd:
    print("  ⏭️  Hindi disclaimer already exists — skipping")
else:
    print("  ❌ Could not find Hindi about block — add disclaimer/terms manually")

# Now find the SECOND "about" occurrence (English section) and insert EN disclaimer+terms before it
# After the Hindi insertion, we need to re-find
en_about_start = sd.find(hi_about_marker)  # first is Hindi
if en_about_start >= 0:
    en_about_start = sd.find(hi_about_marker, en_about_start + 100)  # second is English
    if en_about_start > 0 and '"Disclaimer"' not in sd[en_about_start-500:en_about_start]:
        sd = sd[:en_about_start] + EN_DISCLAIMER_TERMS + sd[en_about_start:]
        print("  ✅ English disclaimer + terms pages added")
    elif '"Disclaimer"' in sd:
        print("  ⏭️  English disclaimer already exists — skipping")
    else:
        print("  ❌ Could not find English about block — add manually")

write("schemes_data.py", sd)


# ─────────────────────────────────────────────
# 3. DELETE old raw HTML files (if they exist)
# ─────────────────────────────────────────────
print("\n🗑️  Step 3: Cleaning up old raw files ...")
for f in ["all-schemas.html", "disclaimer.html", "terms.html", "privacy.html"]:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        # Check if it's a raw template file (not generated by generate.py)
        with open(fp, "r", encoding="utf-8") as fh:
            first_line = fh.readline()
        if first_line.startswith("<!--") or "FILE:" in first_line:
            os.remove(fp)
            print(f"  🗑️  Deleted raw file: {f}")
        else:
            print(f"  ⏭️  {f} looks like a generated file — keeping it")
    else:
        print(f"  ⏭️  {f} doesn't exist — OK")


# ─────────────────────────────────────────────
# 4. RUN generate.py
# ─────────────────────────────────────────────
print("\n🏗️  Step 4: Running generate.py to rebuild site ...")
os.chdir(REPO)
result = os.system(f"{sys.executable} generate.py")
if result == 0:
    print("  ✅ Site rebuilt successfully!")
else:
    print("  ❌ generate.py had an error — check above for details")
    sys.exit(1)


# ─────────────────────────────────────────────
# 5. VERIFY
# ─────────────────────────────────────────────
print("\n✅ Step 5: Verification ...")
for f in ["ads.txt", "robots.txt", "disclaimer.html", "terms.html", "privacy.html", "about.html", "contact.html", "sitemap.xml"]:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        size = os.path.getsize(fp)
        print(f"  ✅ {f} exists ({size:,} bytes)")
    else:
        print(f"  ❌ {f} MISSING!")

# Check disclaimer.html is properly generated (should have <header> tag)
dp = os.path.join(REPO, "disclaimer.html")
if os.path.exists(dp):
    with open(dp, "r", encoding="utf-8") as fh:
        content = fh.read()
    if "<header>" in content and "tricolor" in content:
        print("  ✅ disclaimer.html has proper site template (header, CSS)")
    else:
        print("  ⚠️  disclaimer.html might not have full site template")

print("""
═══════════════════════════════════════════════
🎉 ALL DONE! Now run these commands:
═══════════════════════════════════════════════

  git add -A
  git commit -m "SEO: trust pages via build system, ads.txt, AI robots"
  git push origin main

Then wait 1-2 min for Cloudflare to deploy. Verify:
  → https://sarkariyojnamitra.com/ads.txt
  → https://sarkariyojnamitra.com/disclaimer
  → https://sarkariyojnamitra.com/terms
═══════════════════════════════════════════════
""")
