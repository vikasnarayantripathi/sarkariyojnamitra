#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SESSION 1: PREMIUM DESIGN SYSTEM
Emerald + Gold + Neutral palette (Stripe/Linear discipline)
Replaces the entire CSS block in generate.py. Class names unchanged = zero breakage.
Run: python design_system.py
"""
import os, sys

REPO = os.path.dirname(os.path.abspath(__file__))

def read(f):
    with open(os.path.join(REPO, f), "r", encoding="utf-8") as fh: return fh.read()
def write(f, c):
    with open(os.path.join(REPO, f), "w", encoding="utf-8") as fh: fh.write(c)

NEW_CSS = r'''
*{margin:0;padding:0;box-sizing:border-box}
:root{
 --o:#0B6E4F;--o2:#12845F;--gold:#C9A227;--goldbg:#FBF6E7;
 --ink:#0F1B17;--mut:#5A6B64;--bg:#F6F9F7;--line:#E2E9E5;--card:#fff;
 --shadow:0 1px 2px rgba(15,27,23,.04),0 8px 24px rgba(15,27,23,.06)
}
html{scroll-behavior:smooth}
body{font-family:'Mukta',system-ui,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;font-size:16.5px;-webkit-font-smoothing:antialiased}
.tricolor{height:3px;background:linear-gradient(90deg,#FF9933 33%,#fff 33% 66%,#138808 66%)}
a{color:inherit;text-decoration:none}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
::selection{background:#D6EAE2}
/* static pages */
.static{padding:34px 0 56px;max-width:760px}
.static h1{font-size:1.9rem;margin-bottom:20px;letter-spacing:-.01em}
.static h2{font-size:1.22rem;margin:28px 0 10px}
.static p{margin-bottom:13px;color:#26332D}
.static ul{margin:8px 0 18px 22px}
.static li{margin-bottom:6px}
.static a{color:var(--o);text-decoration:underline;text-underline-offset:3px}
/* header */
header{background:rgba(255,255,255,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.hd{display:flex;align-items:center;gap:12px;padding:13px 0}
.logo{display:flex;align-items:center;gap:11px;font-weight:700}
.logo .box{width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,var(--o),var(--o2));display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(11,110,79,.25)}
.logo b{font-size:1.1rem;line-height:1.2;letter-spacing:-.01em}
.logo small{display:block;font-size:.68rem;color:var(--mut);font-weight:500}
nav{margin-left:auto;display:flex;align-items:center;gap:20px}
nav a{color:var(--mut);font-weight:600;font-size:.92rem;transition:color .15s}
nav a:hover{color:var(--o)}
.lang{border:1px solid var(--line);color:var(--o);background:#fff;border-radius:8px;padding:5px 14px;font-weight:700;font-size:.84rem;transition:.15s}
.lang:hover{background:var(--o);color:#fff;border-color:var(--o)}
.burger{display:none}
/* hero */
.hero{background:linear-gradient(180deg,#fff 0%,var(--bg) 100%);padding:52px 0 36px;text-align:center;border-bottom:1px solid var(--line)}
.badge{display:inline-flex;align-items:center;gap:7px;background:var(--goldbg);border:1px solid #EBDCAF;color:#8A6D14;font-weight:600;font-size:.8rem;padding:6px 14px;border-radius:999px;margin-bottom:18px}
.hero h1{font-family:'Tiro Devanagari Hindi',serif;font-size:2.25rem;line-height:1.28;margin-bottom:13px;letter-spacing:-.01em}
.hero h1 span{color:var(--o)}
.hero p{color:var(--mut);max-width:660px;margin:0 auto 26px;font-size:1.02rem}
.search{display:flex;max-width:600px;margin:0 auto;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);transition:border-color .15s}
.search:focus-within{border-color:var(--o)}
.search input{flex:1;border:0;padding:15px 18px;font-size:1rem;font-family:inherit;outline:none;background:transparent}
.search button{border:0;background:var(--o);color:#fff;font-weight:700;padding:0 24px;cursor:pointer;font-size:.94rem;font-family:inherit;transition:background .15s}
.search button:hover{background:#095C42}
.stats{display:flex;justify-content:center;gap:38px;margin-top:28px;flex-wrap:wrap}
.stat b{display:block;font-size:1.55rem;color:var(--o);font-variant-numeric:tabular-nums}
.stat span{font-size:.78rem;color:var(--mut);font-weight:500;letter-spacing:.02em}
/* sections */
section{padding:40px 0}
.sec-h{text-align:center;margin-bottom:26px}
.sec-h h2{font-family:'Tiro Devanagari Hindi',serif;font-size:1.65rem;letter-spacing:-.01em}
.sec-h p{color:var(--mut);font-size:.92rem;margin-top:4px}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:26px}
.chip{border:1px solid var(--line);background:#fff;color:var(--mut);border-radius:999px;padding:7px 16px;font-size:.85rem;font-weight:600;cursor:pointer;font-family:inherit;transition:.15s}
.chip.on,.chip:hover{background:var(--o);color:#fff;border-color:var(--o)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:19px;display:flex;flex-direction:column;transition:border-color .15s,transform .15s,box-shadow .15s;cursor:pointer}
.card:hover{transform:translateY(-2px);box-shadow:var(--shadow);border-color:#B9CFC6}
.card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.ic{font-size:1.65rem}
.lvl{font-size:.66rem;font-weight:700;padding:3px 10px;border-radius:999px;letter-spacing:.03em}
.lvl.c{background:#E8F0FE;color:#1A56C4}.lvl.up{background:#E7F3EE;color:var(--o)}.lvl.st{background:#E7F3EE;color:var(--o)}
.card h3{font-size:1.03rem;margin-bottom:2px;letter-spacing:-.005em}
.card .sub{font-family:'Tiro Devanagari Hindi',serif;color:var(--mut);font-size:.86rem;margin-bottom:11px}
.ben{background:var(--goldbg);border:1px solid #F0E4BC;border-radius:9px;padding:7px 12px;font-size:.85rem;margin-bottom:13px}
.ben b{color:#8A6D14;font-variant-numeric:tabular-nums}
.more{margin-top:auto;color:var(--o);font-weight:700;font-size:.85rem}
.empty{text-align:center;color:var(--mut);padding:34px;display:none}
/* finder */
.finder{background:#fff;border:1px solid var(--line);border-radius:18px;padding:30px;max-width:780px;margin:0 auto;box-shadow:var(--shadow)}
.finder h2{font-family:'Tiro Devanagari Hindi',serif;font-size:1.45rem;text-align:center}
.finder>p{text-align:center;color:var(--mut);font-size:.9rem;margin-bottom:20px}
.fq{font-weight:700;margin:16px 0 9px;font-size:.95rem}
.opts{display:flex;flex-wrap:wrap;gap:8px}
.opt{border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 15px;font-size:.87rem;font-weight:600;cursor:pointer;font-family:inherit;transition:.15s}
.opt:hover{border-color:#B9CFC6}
.opt.on{background:var(--o);color:#fff;border-color:var(--o)}
.fres{margin-top:20px;display:none}
.fres .lbl{font-weight:700;margin-bottom:10px}
.fres a{display:block;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:11px 14px;margin-bottom:8px;font-weight:600;transition:.15s}
.fres a:hover{border-color:var(--o);background:#EDF5F1}
/* tools */
.tools{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:14px}
.tool{border:1px solid var(--line);border-radius:14px;padding:19px;position:relative;background:#fff;transition:.15s}
.tool:hover{border-color:#B9CFC6;box-shadow:var(--shadow)}
.tool .tag{position:absolute;top:13px;right:13px;font-size:.6rem;color:var(--mut);background:var(--bg);padding:2px 9px;border-radius:999px;font-weight:600;letter-spacing:.04em}
.tool .e{font-size:1.7rem}
.tool h3{margin:9px 0 5px;font-size:1.03rem}
.tool p{color:var(--mut);font-size:.85rem;margin-bottom:12px}
.tool a{color:var(--o);font-weight:700;font-size:.86rem}
/* alert */
.alert{background:var(--goldbg);border:1px solid #EBDCAF;border-left:3px solid var(--gold);border-radius:12px;padding:14px 18px;font-size:.88rem;margin:0 auto;max-width:1040px;color:#57450E}
.adwrap{margin:28px auto;max-width:1040px;min-height:90px;background:#FAFBFA;border:1px dashed var(--line);border-radius:12px;display:flex;align-items:center;justify-content:center;color:#B9C4BE;font-size:.78rem}
/* footer */
footer{background:#0C1F19;color:#9DB5AC;padding:40px 0 22px;font-size:.9rem}
.fgrid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:28px;margin-bottom:24px}
footer h4{color:#fff;margin-bottom:13px;font-size:.98rem}
.flogo{display:flex;align-items:center;gap:10px;margin-bottom:11px}
.flogo .box{width:34px;height:34px;border-radius:9px;background:linear-gradient(135deg,var(--o2),#1AA37A);display:flex;align-items:center;justify-content:center}
.flogo b{color:#fff;font-size:1.03rem}
footer ul{list-style:none}footer li{margin-bottom:7px}
footer a{transition:color .15s}footer a:hover{color:#E8C55A}
.disc{border-top:1px solid #1C332B;padding-top:16px;font-size:.77rem;color:#7A948A}
.copy{text-align:center;margin-top:13px;font-size:.77rem;color:#5F7A6F}
/* scheme page */
.crumb{font-size:.82rem;color:var(--mut);padding:16px 0}
.crumb a:hover{color:var(--o)}
.updated{font-size:.8rem;color:var(--mut);margin:-.4rem 0 1rem}
.sp-hero{background:#fff;border:1px solid var(--line);border-radius:16px;padding:26px;margin-bottom:20px;box-shadow:var(--shadow)}
.sp-hero .ic{font-size:2.5rem}
.sp-hero h1{font-size:1.75rem;margin:9px 0 3px;letter-spacing:-.01em}
.sp-hero .sub{font-family:'Tiro Devanagari Hindi',serif;color:var(--mut);margin-bottom:15px}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:11px;margin-top:10px}
.fact{background:var(--bg);border:1px solid var(--line);border-radius:11px;padding:11px 14px}
.fact span{font-size:.7rem;color:var(--mut);display:block;font-weight:600;letter-spacing:.03em}
.fact b{font-size:.95rem;font-variant-numeric:tabular-nums}
.block{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px 24px;margin-bottom:16px}
.block h2{font-family:'Tiro Devanagari Hindi',serif;font-size:1.32rem;margin-bottom:14px;color:var(--o)}
.block p{color:#26332D}
.block ul{list-style:none;margin-top:4px}
.block li{padding:8px 0 8px 30px;position:relative;border-bottom:1px solid #EFF4F1}
.block li:last-child{border-bottom:0}
.block li:before{content:"✓";position:absolute;left:0;top:8px;color:#fff;background:var(--o);width:19px;height:19px;border-radius:50%;font-size:.68rem;display:flex;align-items:center;justify-content:center}
.steps{counter-reset:s}
.steps li:before{content:counter(s);counter-increment:s;background:var(--gold);color:#fff;font-weight:700}
.faq{border-bottom:1px solid #EFF4F1;padding:13px 0}.faq:last-child{border:0}
.faq b{display:block;margin-bottom:4px}
.faq span{color:var(--mut);font-size:.92rem}
.cta-apply{display:inline-block;background:var(--o);color:#fff;font-weight:700;padding:13px 26px;border-radius:11px;margin-top:6px;transition:.15s;box-shadow:0 2px 10px rgba(11,110,79,.28)}
.cta-apply:hover{background:#095C42;transform:translateY(-1px)}
.related{display:grid;grid-template-columns:repeat(auto-fill,minmax(215px,1fr));gap:12px}
.related a{background:#fff;border:1px solid var(--line);border-radius:11px;padding:13px 15px;font-weight:600;font-size:.9rem;transition:.15s}
.related a:hover{border-color:var(--o);background:#F2F8F5}
@media(max-width:760px){
 nav{gap:12px}.hero h1{font-size:1.65rem}.fgrid{grid-template-columns:1fr}
 nav a:not(.lang){display:none}
 body{font-size:16px}
 .hero{padding:38px 0 28px}
 section{padding:30px 0}
}
'''

print("SESSION 1: Applying premium emerald+gold design system ...")
gen = read("generate.py")

# Find CSS block: CSS = r""" ... """
start = gen.find('CSS = r"""')
if start < 0:
    print("ERROR: CSS block not found")
    sys.exit(1)

end = gen.find('"""', start + 10)
if end < 0:
    print("ERROR: CSS block end not found")
    sys.exit(1)
end += 3

old_block = gen[start:end]
new_block = 'CSS = r"""' + NEW_CSS + '"""'
gen = gen[:start] + new_block + gen[end:]
write("generate.py", gen)
print("  Done: CSS block replaced (%d chars -> %d chars)" % (len(old_block), len(new_block)))

# Rebuild
print("\nRebuilding site ...")
os.chdir(REPO)
r = os.system(sys.executable + " generate.py")
if r == 0:
    print("  Site rebuilt OK — all 192+ pages now premium emerald+gold!")
else:
    print("  ERROR")
    sys.exit(1)

print("""
DONE! Preview locally first:
  start index.html
(browser me kholke design dekho)

Theek lage toh:
  git add -A
  git commit -m "Design: premium emerald+gold system"
  git push origin main
""")
