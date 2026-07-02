#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PATCH FIX: Add missing Hindi disclaimer+terms static pages
Run: python patch_fix.py
"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh:
        return fh.read()

def write(f, content):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh:
        fh.write(content)

sd = read("schemes_data.py")

# Check if Hindi static disclaimer actually exists (not just footer disclaimer text)
# The static page would have "disclaimer":{ with title, desc, h1, body
has_hi_disclaimer_page = '"disclaimer":{\n   "title":"अस्वीकरण' in sd or '"disclaimer":{\n   "title":"\\u0905' in sd

if has_hi_disclaimer_page:
    print("Hindi disclaimer page already exists — skipping")
else:
    print("Adding Hindi disclaimer + terms pages...")

    HI_BLOCK = '''  "disclaimer":{
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

    # Find the FIRST "about":{ in the file (Hindi section)
    # We need to find it inside the "static":{ block of the Hindi T
    # Search for the pattern where "about" comes after "privacy" closing
    
    # Strategy: find all occurrences of '  "about":{' and insert before the FIRST one
    marker = '  "about":{'
    pos = sd.find(marker)
    
    if pos > 0:
        sd = sd[:pos] + HI_BLOCK + sd[pos:]
        write("schemes_data.py", sd)
        print("  ✅ Hindi disclaimer + terms added to schemes_data.py")
    else:
        print("  ❌ Could not find about block — manual edit needed")
        sys.exit(1)

# Now rebuild
print("\n🏗️  Rebuilding site ...")
os.chdir(REPO)
result = os.system(f"{sys.executable} generate.py")
if result == 0:
    print("  ✅ Site rebuilt successfully!")
else:
    print("  ❌ Error — check above")
    sys.exit(1)

# Verify
print("\n✅ Verification:")
for f in ["disclaimer.html", "terms.html", "en/disclaimer.html", "en/terms.html"]:
    fp = os.path.join(REPO, f)
    if os.path.exists(fp):
        sz = os.path.getsize(fp)
        print(f"  ✅ {f} ({sz:,} bytes)")
    else:
        print(f"  ❌ {f} MISSING")

print("""
══════════════════════════════════════
🎉 DONE! Now run:

  git add -A
  git commit -m "SEO: trust pages fix"
  git push origin main
══════════════════════════════════════
""")
