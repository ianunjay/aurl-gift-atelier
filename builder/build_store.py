# -*- coding: utf-8 -*-
"""Builds a complete, production-grade single-file gift storefront HTML."""
import json, re, html as _html, os
HERE=os.path.dirname(os.path.abspath(__file__))
DIST=os.path.join(HERE,"..","dist")
os.makedirs(DIST,exist_ok=True)

rec = json.load(open(os.path.join(DIST,"_records.json"), encoding="utf-8"))
GROUPS = rec["groups"]                      # [{key,label,tag}]
IDEAS  = rec["ideas"]                        # [{id,group_key,group,theme,name,why,price_band,price_label}]
TAG = {g["key"]: g["tag"] for g in GROUPS}

STOP = set("diy set kit premium personalised personalized custom the a an for with and of to your his her".split())

def kw(name):
    s = re.sub(r"\(.*?\)", " ", name)          # drop parentheses
    s = re.sub(r"[/&\-—+|]", " ", s)
    s = re.sub(r"[^A-Za-z0-9 ]", " ", s)
    words = [w for w in s.split() if w.lower() not in STOP]
    return " ".join(words[:4]).strip() or re.sub(r"[^A-Za-z ]"," ",name).strip()[:24]

OCC_LIST = ["Birthday","Anniversary","Wedding","Valentine's Day","Diwali","Rakhi",
            "Housewarming","Retirement","Friendship","Corporate / Farewell",
            "Kids Party","Just Because"]

def occasions(gk, theme, name):
    t = (theme + " " + name + " " + gk).lower()
    o = set()
    if "boys" in gk or "girls" in gk: o |= {"Birthday","Kids Party","Just Because","Diwali"}
    if "teen" in gk: o |= {"Birthday","Friendship","Just Because"}
    if gk in ("men_20_35","women_20_35","men_36_55","women_36_55"):
        o |= {"Birthday","Anniversary","Just Because"}
    if "senior" in gk: o |= {"Anniversary","Retirement","Diwali","Just Because"}
    if gk == "unisex": o |= {"Housewarming","Friendship","Anniversary","Just Because"}
    if gk == "premium": o |= {"Anniversary","Wedding","Corporate / Farewell","Milestone" if False else "Just Because"}
    kws = {
        "wedding":"Wedding","anniversary":"Anniversary","couple":"Valentine's Day",
        "sentimental":"Anniversary","romantic":"Valentine's Day","valentine":"Valentine's Day",
        "faith":"Diwali","devotion":"Diwali","spiritual":"Diwali","diya":"Diwali","pooja":"Diwali",
        "rakhi":"Rakhi","sibling":"Rakhi","friend":"Friendship","cowork":"Corporate / Farewell",
        "farewell":"Corporate / Farewell","housewarming":"Housewarming","home":"Housewarming",
        "kitchen":"Housewarming","plant":"Housewarming","bar":"Housewarming","jewell":"Anniversary",
        "experience":"Anniversary","travel":"Anniversary","retire":"Retirement",
    }
    for k, v in kws.items():
        if k in t: o.add(v)
    o = {x for x in o if x in OCC_LIST}
    return sorted(o) or ["Just Because"]

PRICE_REP = {"A":350,"B":950,"C":2800,"D":7500}
def wow(band, name):
    base = {"A":2,"B":3,"C":4,"D":5}[band]
    flair = any(w in name.lower() for w in
        ["levit","drone","telescope","neon","star-map","star map","projector",
         "massage chair","hot-air","hot air","experience","supercar","yacht","helicopter",
         "vinyl","espresso","robot"])
    return max(1, min(5, base + (1 if flair and band in "AB" else 0)))

items = []
for it in IDEAS:
    items.append({
        "id": it["id"], "gk": it["group_key"], "group": it["group"],
        "tag": TAG[it["group_key"]], "theme": it["theme"], "name": it["name"],
        "why": it["why"], "band": it["price_band"], "pl": it["price_label"],
        "kw": kw(it["name"]), "occ": occasions(it["group_key"], it["theme"], it["name"]),
        "rep": PRICE_REP[it["price_band"]], "wow": wow(it["price_band"], it["name"]),
    })

DATA = json.dumps({"groups": GROUPS, "items": items, "occasions": OCC_LIST},
                  ensure_ascii=False, separators=(",", ":"))

# ---------------------------------------------------------------- HTML/CSS/JS
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="Aurl · The Gift Atelier — 1,200 curated, non-generic gift ideas for every age and personality, with live images, multiple India buy-links, wishlist and detailed gift pages."/>
<meta name="theme-color" content="#141310"/>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%23141310'/%3E%3Ctext x='50' y='50' font-size='58' text-anchor='middle' dominant-baseline='central'%3E%F0%9F%8E%81%3C/text%3E%3C/svg%3E"/>
<title>Aurl · The Gift Atelier — 1,200 curated gifts (India)</title>
<style>
:root{
  --bg:#F5F2EC; --card:#FFFFFF; --ink:#141310; --mut:#615c48; --soft:#8f8a70;
  --line:#E7E1D2; --line2:#EFEADD; --accent:#111; --pop:#C9F24C; --pop-ink:#1b2207;
  --gold:#9c7636; --heart:#ff4d6d; --chip:#F0EBDD; --ok:#2e8b57;
  --sh:0 12px 34px rgba(26,22,10,.10); --sh-s:0 4px 14px rgba(26,22,10,.07);
  --r:20px; --r-s:14px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Segoe UI',-apple-system,system-ui,Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.5}
a{color:inherit;text-decoration:none}
img{display:block;max-width:100%}
button{font-family:inherit}
.app{max-width:1240px;margin:0 auto;padding:0 20px 90px}
:focus-visible{outline:3px solid var(--pop);outline-offset:2px;border-radius:8px}

/* ---------- Header ---------- */
.hdr{position:sticky;top:0;z-index:60;background:rgba(245,242,236,.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.hdr .row{max-width:1240px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:14px}
.brand{display:flex;align-items:center;gap:11px;cursor:pointer}
.brand .mark{width:38px;height:38px;border-radius:12px;background:var(--ink);color:var(--pop);display:grid;place-items:center;font-weight:800;font-size:18px}
.brand b{font-size:19px;letter-spacing:-.3px;display:block;line-height:1}
.brand small{font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--mut)}
.hsearch{flex:1;min-width:120px;display:flex;align-items:center;gap:9px;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:10px 16px;box-shadow:var(--sh-s)}
.hsearch input{border:0;outline:0;background:transparent;width:100%;font-size:14.5px;color:var(--ink)}
.hbtn{width:44px;height:44px;border-radius:13px;background:var(--card);border:1px solid var(--line);display:grid;place-items:center;font-size:18px;cursor:pointer;position:relative;box-shadow:var(--sh-s);color:var(--ink)}
.hbtn:hover{border-color:var(--ink)}
.badge{position:absolute;top:-6px;right:-6px;min-width:18px;height:18px;padding:0 5px;border-radius:9px;background:var(--pop);color:var(--pop-ink);font-size:10.5px;font-weight:800;display:grid;place-items:center}

/* ---------- Hero ---------- */
.hero{margin:22px 0 10px;padding:30px;border-radius:26px;position:relative;overflow:hidden;color:#fff;background:linear-gradient(135deg,#141310,#2c2717 70%);box-shadow:var(--sh)}
.hero h1{margin:0 0 10px;font-size:clamp(24px,4vw,34px);line-height:1.1;letter-spacing:-.6px;font-weight:800;max-width:640px}
.hero h1 em{font-style:normal;color:var(--pop)}
.hero p{margin:0;color:#d9d4c2;max-width:560px;font-size:14.5px}
.hero .blob{position:absolute;right:-50px;top:-50px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle at 30% 30%,var(--pop),transparent 62%);opacity:.45;filter:blur(4px)}
.hero .stats{display:flex;gap:26px;margin-top:18px;flex-wrap:wrap}
.hero .stats div{font-size:12.5px;color:#cfcab8}
.hero .stats b{display:block;font-size:22px;color:#fff}

/* ---------- Controls ---------- */
.rail{display:flex;gap:9px;overflow-x:auto;padding:16px 2px 8px;scrollbar-width:none}
.rail::-webkit-scrollbar{display:none}
.cpill{flex:0 0 auto;padding:10px 16px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-size:13.5px;font-weight:600;cursor:pointer;white-space:nowrap;box-shadow:var(--sh-s);transition:.15s}
.cpill .n{color:var(--soft);margin-left:6px;font-weight:600}
.cpill.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.cpill.on .n{color:var(--pop)}
.filters{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:6px 0 4px}
.sel{position:relative}
.sel select{appearance:none;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 38px 11px 14px;font-size:13.5px;color:var(--ink);cursor:pointer;box-shadow:var(--sh-s)}
.sel::after{content:'▾';position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--soft);pointer-events:none;font-size:12px}
.reset{margin-left:auto;background:var(--ink);color:#fff;border:0;border-radius:12px;padding:11px 16px;font-size:13.5px;font-weight:600;cursor:pointer}
.reset:hover{opacity:.9}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 2px;min-height:4px}
.chip{display:inline-flex;align-items:center;gap:7px;background:var(--chip);border:1px solid var(--line);border-radius:999px;padding:6px 10px 6px 12px;font-size:12.5px;color:var(--ink)}
.chip button{border:0;background:transparent;cursor:pointer;font-size:14px;line-height:1;color:var(--mut)}
.chip button:hover{color:var(--heart)}
.resbar{display:flex;align-items:baseline;justify-content:space-between;margin:14px 4px 8px}
.resbar h2{margin:0;font-size:20px;letter-spacing:-.3px}
.resbar span{font-size:13px;color:var(--mut)}

/* ---------- Grid + cards ---------- */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:18px;margin-top:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column;box-shadow:var(--sh-s);transition:.18s;position:relative}
.card:hover{transform:translateY(-4px);box-shadow:var(--sh);border-color:#dfd8c6}
.thumb{aspect-ratio:4/3;position:relative;background:var(--line2);overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;transition:.4s}
.card:hover .thumb img{transform:scale(1.05)}
.price{position:absolute;left:12px;top:12px;background:rgba(255,255,255,.94);backdrop-filter:blur(3px);color:var(--ink);font-size:11.5px;font-weight:800;padding:6px 11px;border-radius:999px;box-shadow:var(--sh-s)}
.fav{position:absolute;right:12px;top:12px;width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.94);border:0;display:grid;place-items:center;font-size:16px;cursor:pointer;color:#cfc7b2;box-shadow:var(--sh-s);transition:.15s;z-index:2}
.fav:hover{transform:scale(1.1)}
.fav.on{color:var(--heart)}
.cbody{padding:14px 15px 15px;display:flex;flex-direction:column;flex:1}
.eyebrow{font-size:10.5px;letter-spacing:.7px;text-transform:uppercase;color:var(--soft);font-weight:800}
.cbody h3{margin:6px 0 6px;font-size:15.5px;line-height:1.32;letter-spacing:-.2px}
.cbody p{margin:0;color:var(--mut);font-size:12.7px;flex:1}
.cfoot{display:flex;align-items:center;justify-content:space-between;margin-top:13px}
.stars{color:var(--gold);font-size:12.5px;letter-spacing:1px}
.go{font-size:12.5px;font-weight:700;color:var(--ink)}
.card:hover .go{color:var(--gold)}
.loadwrap{display:flex;justify-content:center;margin:30px 0 6px}
.loadmore{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 26px;font-size:14px;font-weight:700;cursor:pointer;box-shadow:var(--sh-s)}
.loadmore:hover{border-color:var(--ink)}
.empty{text-align:center;color:var(--mut);padding:70px 20px}
.empty .big{font-size:44px;margin-bottom:8px}

/* ---------- Detail ---------- */
.detail{padding-top:18px}
.crumb{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--mut);margin-bottom:16px;flex-wrap:wrap}
.crumb a{color:var(--mut)} .crumb a:hover{color:var(--ink)}
.back{display:inline-flex;align-items:center;gap:7px;background:var(--card);border:1px solid var(--line);border-radius:11px;padding:9px 14px;font-size:13.5px;font-weight:600;cursor:pointer;box-shadow:var(--sh-s)}
.back:hover{border-color:var(--ink)}
.dtop{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:34px;align-items:start}
.gallery .main{aspect-ratio:4/3;border-radius:22px;overflow:hidden;background:var(--line2);box-shadow:var(--sh-s);border:1px solid var(--line)}
.gallery .main img{width:100%;height:100%;object-fit:cover}
.gthumbs{display:flex;gap:10px;margin-top:12px}
.gthumbs button{flex:1;aspect-ratio:1/1;border-radius:13px;overflow:hidden;border:2px solid transparent;background:var(--line2);cursor:pointer;padding:0}
.gthumbs button.sel{border-color:var(--ink)}
.gthumbs img{width:100%;height:100%;object-fit:cover}
.dinfo .eyebrow{font-size:11px}
.dinfo h1{margin:8px 0 12px;font-size:clamp(22px,3vw,30px);line-height:1.15;letter-spacing:-.5px}
.metarow{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.tagpill{font-size:12px;font-weight:700;padding:6px 12px;border-radius:999px;background:var(--chip);border:1px solid var(--line)}
.tagpill.price{background:var(--ink);color:#fff;border-color:var(--ink)}
.tagpill.wow{color:var(--gold)}
.lead{font-size:15.5px;color:#38352b;margin:0 0 18px}
.priceguide{background:var(--line2);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin-bottom:18px}
.priceguide .k{font-size:11.5px;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);font-weight:800}
.priceguide .v{font-size:19px;font-weight:800;margin-top:2px}
.priceguide .sub{font-size:12.5px;color:var(--mut);margin-top:3px}
.buyhdr{font-size:12px;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);font-weight:800;margin:0 0 10px}
.buys{display:grid;gap:10px}
.buy{display:flex;align-items:center;gap:12px;justify-content:space-between;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:13px 16px;font-weight:700;font-size:14.5px;box-shadow:var(--sh-s);transition:.15s}
.buy:hover{border-color:var(--ink);transform:translateX(2px)}
.buy .l{display:flex;align-items:center;gap:12px}
.buy .dot{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;font-size:15px;background:var(--chip)}
.buy .arr{color:var(--soft);font-weight:800}
.dact{display:flex;gap:10px;margin-top:16px}
.dact button{flex:1;border-radius:14px;padding:14px;font-size:14.5px;font-weight:700;cursor:pointer;border:1px solid var(--line);background:var(--card);box-shadow:var(--sh-s);display:flex;align-items:center;justify-content:center;gap:9px}
.dact .wl.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.dact button:hover{border-color:var(--ink)}
.sections{margin-top:44px;display:grid;grid-template-columns:1fr;gap:14px;max-width:920px}
.sec{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px 24px;box-shadow:var(--sh-s)}
.sec h3{margin:0 0 12px;font-size:17px;letter-spacing:-.2px;display:flex;align-items:center;gap:9px}
.sec p{margin:0 0 8px;color:#403c30;font-size:14.5px}
.sec ul{margin:6px 0 0;padding-left:20px}
.sec li{margin:6px 0;color:#403c30;font-size:14.3px}
.occwrap{display:flex;gap:8px;flex-wrap:wrap}
.occ{background:var(--chip);border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:13px;font-weight:600;cursor:pointer}
.occ:hover{border-color:var(--ink)}
.facts{width:100%;border-collapse:collapse}
.facts td{padding:11px 4px;border-bottom:1px solid var(--line2);font-size:14px;vertical-align:top}
.facts td:first-child{color:var(--mut);width:42%;font-weight:600}
.related h3{margin:40px 4px 4px;font-size:20px}

/* ---------- Toast ---------- */
.toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;padding:13px 20px;border-radius:14px;font-size:14px;font-weight:600;box-shadow:var(--sh);opacity:0;pointer-events:none;transition:.25s;z-index:100}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toTop{position:fixed;right:20px;bottom:22px;width:48px;height:48px;border-radius:15px;background:var(--ink);color:var(--pop);border:0;font-size:20px;cursor:pointer;display:none;box-shadow:var(--sh);z-index:55}

footer{border-top:1px solid var(--line);margin-top:40px;padding:26px 4px;color:var(--mut);font-size:12.5px;text-align:center}

@media (prefers-reduced-motion: reduce){
  *{transition:none!important;scroll-behavior:auto!important;animation:none!important}
  .card:hover{transform:none} .card:hover .thumb img{transform:none}
}
@media(max-width:820px){
  .dtop{grid-template-columns:1fr;gap:22px}
  .brand small{display:none}
}
@media(max-width:520px){
  .app{padding:0 14px 80px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
  .cbody p{display:none}
  .hero{padding:22px}
}
</style>
</head>
<body>
<header class="hdr">
  <div class="row">
    <div class="brand" onclick="location.hash='#/'">
      <span class="mark">A</span>
      <span><b>Aurl</b><small>Gift Atelier</small></span>
    </div>
    <label class="hsearch"><span aria-hidden="true">🔍</span>
      <input id="q" type="search" placeholder="Search 1,200 gifts — telescope, star map, spa, coding…" aria-label="Search gifts"/>
    </label>
    <button class="hbtn" id="surpriseBtn" aria-label="Surprise me with a random gift" title="Surprise me" onclick="surprise()">🎲</button>
    <button class="hbtn" id="wishBtn" aria-label="Open wishlist" onclick="location.hash='#/wishlist'">♥<span class="badge" id="wishCount">0</span></button>
  </div>
</header>

<main class="app" id="view" aria-live="polite"></main>

<div class="toast" id="toast" role="status"></div>
<button class="toTop" id="toTop" aria-label="Back to top">↑</button>
<footer>Aurl · The Gift Atelier — a curated demo storefront · 12 recipient groups × 100 = 1,200 ideas · prices are indicative bands · buy links open real Indian retailers.</footer>

<script>
const DB = __DATA__;
DB.byId = {}; DB.items.forEach(i=>DB.byId[i.id]=i);
const PRICE_SHORT={A:'₹0–500',B:'₹500–1.5k',C:'₹1.5–5k',D:'₹5k+'};
const PRICE_FULL={A:'Under ₹500',B:'₹500 – ₹1,500',C:'₹1,500 – ₹5,000',D:'₹5,000 and above'};

/* ---------- utils ---------- */
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function stars(n){return '★★★★★'.slice(0,n)+'☆☆☆☆☆'.slice(0,5-n);}
function debounce(fn,ms){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),ms);};}

let TOAST_T;
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(TOAST_T);TOAST_T=setTimeout(()=>t.classList.remove('show'),1900);}

/* ---------- imagery ---------- */
function imgKw(it){return it.kw.split(/\s+/).slice(0,2).join(',')||'gift';}
function liveImg(it,i){return 'https://loremflickr.com/600/450/'+encodeURIComponent(imgKw(it))+'?lock='+(it.id*9+i);}
const FBCACHE={};
function hue(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))%360;return h;}
function glyph(theme){const t=theme.toLowerCase();const m=[
 [['robot','coding'],'🤖'],[['stem','science','discovery'],'🔬'],[['build','construction'],'🧩'],
 [['space','nature'],'🪐'],[['art','making'],'🎨'],[['music','performance','pop'],'🎵'],
 [['game','puzzle','social'],'♟️'],[['book','story','reading','learning','leisure'],'📚'],[['early years'],'🧸'],
 [['wellness','mindful','self-care'],'🧘'],[['fitness','movement','sport','outdoor','adventure'],'🏋️'],
 [['jewell','watch'],'💍'],[['fashion','bag','style','dress','clothing'],'👜'],
 [['home','decor','room','aesthetic','comfort'],'🛋️'],[['kitchen','gourmet','food','baking','foodie'],'🍽️'],
 [['bar','tasting'],'🥃'],[['travel'],'✈️'],[['experience','milestone','anniversary'],'🎟️'],
 [['tech','gadget','edc','utility','gaming'],'🎧'],[['groom'],'🧴'],[['desk','office','wfh','study'],'🖥️'],
 [['health','mobility','monitoring'],'🩺'],[['faith','spiritual','devotion'],'🪔'],
 [['sentimental','keepsake','nostalgia','personalised'],'🎁'],[['sustainable'],'🌱'],[['plant','green'],'🪴'],
 [['couple'],'💞'],[['friend'],'🫶'],[['sibling','family'],'👪'],[['cowork'],'🏆'],[['housewarming'],'🏠'],
 [['quirky'],'✨'],[['subscription'],'📦'],[['skill','side-hustle'],'🛠️'],
 [['collectible','luxury','premium','big-ticket'],'💎'],[['hobby','hobbies'],'🎯'],[['fandom'],'⚽']];
 for(const[k,e]of m)if(k.some(x=>t.includes(x)))return e;return '🎁';}
function fb(theme){if(FBCACHE[theme])return FBCACHE[theme];const h=hue(theme),g=glyph(theme);
 const svg="<svg xmlns='http://www.w3.org/2000/svg' width='600' height='450'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='hsl("+h+",68%,86%)'/><stop offset='1' stop-color='hsl("+((h+42)%360)+",62%,74%)'/></linearGradient></defs><rect width='600' height='450' fill='url(#g)'/><text x='50%' y='53%' font-size='150' text-anchor='middle' dominant-baseline='middle'>"+g+"</text></svg>";
 const u='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);FBCACHE[theme]=u;return u;}
function imgFail(el){el.onerror=null;el.src=fb(el.dataset.th);}

/* ---------- buy links ---------- */
function buyLinks(it){
  const q=encodeURIComponent(it.kw+' gift');
  const t=(it.theme+' '+it.name).toLowerCase();
  const L=[
    {n:'Amazon.in',  e:'🛒', u:'https://www.amazon.in/s?k='+q},
    {n:'Flipkart',   e:'🛍️', u:'https://www.flipkart.com/search?q='+q},
  ];
  if(/personal|sentiment|caricature|engrav|keepsake|photo|neon|name|custom/.test(t))
    L.push({n:'IGP (personalised)',e:'🎁',u:'https://www.igp.com/search?q='+q});
  else if(/experience|voucher|staycation|spa|adventure|tasting|getaway|retreat|cruise|balloon/.test(t))
    L.push({n:'WonderGifts (experiences)',e:'🎟️',u:'https://www.wondergifts.in/'});
  else if(/gadget|tech|edc|charger|speaker|lamp|levit|drone|gaming|utility/.test(t))
    L.push({n:'Bigsmall (gadgets)',e:'⚡',u:'https://www.bigsmall.in/search?q='+q});
  else if(/toy|kids|stem|robot|coding|craft|puzzle|building|early years|dress-up/.test(t))
    L.push({n:'FirstCry (kids)',e:'🧸',u:'https://www.firstcry.com/search?q='+q});
  else if(/jewell|fashion|bag|watch|scarf|necklace|bracelet/.test(t))
    L.push({n:'Myntra',e:'👗',u:'https://www.myntra.com/'+encodeURIComponent(it.kw.replace(/\s+/g,'-').toLowerCase())+'?rawQuery='+q});
  L.push({n:'Compare on Google',e:'🔎',u:'https://www.google.com/search?tbm=shop&q='+q});
  return L;
}

/* ---------- buying tips ---------- */
function tips(it){
  const t=it.theme.toLowerCase(), T=[];
  if(/stem|science|discovery/.test(t))T.push('Match the recommended age range to the child.','Prefer kits with a clear illustrated manual and reusable parts.','Check if refills or extra consumables are available.');
  else if(/robot|coding/.test(t))T.push('Confirm whether it needs an app, tablet or PC.','Screen-free block coding suits under-10s; real code suits 10+.','Check the battery type and whether cells are included.');
  else if(/build|construction/.test(t))T.push('Check piece count and difficulty vs. the child’s patience.','Sturdier wood/metal builds last longer than thin plastic.','Small parts can be a choking hazard for under-3s.');
  else if(/art|making|craft|jewellery craft/.test(t))T.push('Look for non-toxic, washable materials.','Kits that make a keepsake feel more rewarding.','Check that enough supplies are included to finish the project.');
  else if(/music|performance/.test(t))T.push('Beginner-friendly instruments hold tuning and are forgiving.','A bundled lesson book or app speeds up the first wins.','Consider volume/headphone options for home peace.');
  else if(/game|puzzle|social/.test(t))T.push('Check the player count and average play time.','Read the age rating for rules complexity.','Replayability matters more than box size.');
  else if(/book|story|reading/.test(t))T.push('Confirm the reading age and format (print / audio / e-reader).','Personalised or series books get re-read the most.','Large-print editions help older or younger eyes.');
  else if(/wellness|mindful|self-care/.test(t))T.push('Check materials for skin sensitivity and washability.','Rechargeable devices beat disposable-battery ones long term.','Look for a warranty on any electronic wellness gadget.');
  else if(/fitness|movement|sport|outdoor|adventure/.test(t))T.push('Match resistance/weight or size to their fitness level.','Read reviews on durability for anything load-bearing.','Check storage size for home-gym pieces.');
  else if(/jewell|watch/.test(t))T.push('Verify metal type (hypoallergenic if sensitive skin).','Personalised pieces need extra lead time — order early.','Check the return/exchange window for sizing.');
  else if(/fashion|bag|style|clothing/.test(t))T.push('Confirm size, colour and material before buying.','Check the fabric-care and return policy.','Neutral tones are the safest style-gift bet.');
  else if(/home|decor|room|aesthetic|comfort/.test(t))T.push('Measure the space so the piece fits the room.','Check bulb type/voltage for any lighting.','Match the finish to their existing décor.');
  else if(/kitchen|gourmet|food|baking|foodie/.test(t))T.push('Check dietary needs/allergens for edible gifts.','For appliances, confirm capacity and warranty.','Look at the freshness/shelf-life for hampers.');
  else if(/bar|tasting/.test(t))T.push('Confirm the recipient drinks before gifting spirits.','Glassware + accessories make a safe non-alcohol alternative.','Check delivery rules for alcohol in your state.');
  else if(/travel/.test(t))T.push('Universal adapters and TSA-friendly sizes travel best.','Check warranty for luggage and electronics.','Lightweight, durable materials win for frequent flyers.');
  else if(/experience|milestone|anniversary/.test(t))T.push('Check the voucher validity and city coverage.','Confirm it’s exchangeable if plans change.','Read what’s included vs. paid add-ons.');
  else if(/tech|gadget|edc|gaming|utility/.test(t))T.push('Check compatibility with their phone/OS.','Prefer fast-charging and a decent warranty.','Read recent reviews for real-world battery life.');
  else if(/groom/.test(t))T.push('Check skin/scent sensitivities before fragrances.','Rechargeable trimmers beat disposable ones.','A gift set is a safer bet than a single guess.');
  else if(/desk|office|wfh|study/.test(t))T.push('Check desk size and cable-reach before buying.','Ergonomic pieces should match their setup height.','Neutral, matte finishes suit most workspaces.');
  else if(/health|mobility|monitoring/.test(t))T.push('Prefer large, clear displays for older users.','Check clinical validation/warranty for medical devices.','Simple one-button operation is a real feature.');
  else if(/faith|spiritual|devotion/.test(t))T.push('Confirm the tradition and specifics they follow.','Quality of materials matters for daily-use ritual items.','Preloaded devotional audio is a thoughtful touch.');
  else if(/plant|green/.test(t))T.push('Match the plant to their light and care level.','Self-watering pots help forgetful gift-getters.','Check pot drainage and included care guide.');
  else if(/subscription/.test(t))T.push('Confirm it auto-renews or is a fixed term.','Check coverage/availability in their city.','Gift the length that suits the relationship.');
  else if(/sentimental|keepsake|nostalgia|personalised/.test(t))T.push('Order early — personalisation needs lead time.','Double-check names, dates and spellings.','Send high-resolution photos for the best print.');
  else T.push('Compare seller ratings and the return policy.','Read recent reviews for real-world quality.','Check delivery time to your pincode.');
  T.push('Compare the prices across the buy options below before ordering.');
  return T;
}
function whoFor(it){
  let s='Ideal for '+it.group.toLowerCase()+' — '+it.tag.toLowerCase()+'.';
  if(/personal|custom|engrav|name|photo|caricature/.test(it.name.toLowerCase()))
    s+=' It’s personalisable, so it feels made-just-for-them.';
  return s;
}
function personalisable(it){return /personal|custom|engrav|name|photo|caricature|star.?map|monogram/.test(it.name.toLowerCase());}
function expandedOverview(it){return 'A standout in the '+it.theme.toLowerCase()+' category. '+it.why+' '+whoFor(it)+' '+(personalisable(it)?'Because it can be personalised, it feels made-just-for-them rather than picked off a shelf — exactly the kind of detail people remember.':'It’s a considered, non-generic choice that stands apart from default gifts and gets remembered long after the wrapping is gone.');}
const PAIR=[['stem|science|robot|coding|building','a themed storybook or a display shelf to show off what they build','kids display shelf'],['art|craft|making|jewellery craft','a quality frame or a storage box for the finished pieces','photo frame'],['music','a padded stand or a songbook to speed up the first tunes','music stand'],['book|reading|story','a cosy reading light and a bookmark set','reading light'],['wellness|self-care|mindful','a scented candle and herbal tea for the full ritual','scented candle'],['fitness|sport|movement|outdoor|adventure','an insulated bottle and a quick-dry gym towel','insulated bottle'],['jewell|watch','a velvet jewellery box for safe keeping','jewellery box'],['fashion|bag|style|clothing','a matching accessory or a fabric-care kit','accessory'],['home|decor|kitchen|gourmet|foodie|baking','a bottle of wine or gourmet treats to round out the hamper','gourmet hamper'],['bar|tasting','premium snacks or a set of coasters','coasters'],['travel','a passport holder and packing cubes','packing cubes'],['experience|milestone|anniversary','a handwritten card and a keepsake frame for the memory','keepsake frame'],['tech|gadget|edc|gaming','a fast-charging cable or a protective case','charging cable'],['grooming','a signature fragrance or a travel wash-bag','wash bag'],['faith|spiritual|devotion','fresh incense and a brass diya set','brass diya'],['plant|green','a decorative planter and plant-care tools','planter'],['sentimental|keepsake|nostalgia|couple|friend|family','premium gift wrap and a heartfelt card','gift wrap']];
function pairWith(it){const t=(it.theme+' '+it.name).toLowerCase();for(const[k,txt,q]of PAIR){if(new RegExp(k).test(t))return{txt,q};}return{txt:'premium gift wrap and a heartfelt handwritten card',q:'gift wrap card'};}
function delivery(it){return personalisable(it)?'Personalised items usually ship in about 4–8 days — order early, and choose express at checkout if it’s last-minute.':'Most sellers deliver in about 2–6 days across India, with same or next-day options in many metros.';}
function proTip(it){if(it.band==='D')return 'For a premium gift like this, add a short handwritten note — it multiplies the impact for almost nothing.';if(personalisable(it))return 'Double-check names, dates and spellings before confirming — personalised items usually can’t be returned.';return 'Add their favourite treat or a card to make even a simple gift feel personal and complete.';}
function tagsFor(it){const first=it.kw.split(/\s+/)[0];const s=[it.theme,it.occ[0],personalisable(it)?'Personalisable':'Ready to gift'];if(first&&!it.theme.toLowerCase().includes(first.toLowerCase()))s.unshift(first);return [...new Set(s)].slice(0,4);}
function jumpSearch(q){Object.assign(state,{group:'all',theme:'',price:'',occ:'',q:q});location.hash='#/';}

/* ---------- wishlist ---------- */
const WKEY='aurl_wishlist_v1';
function loadWish(){try{return new Set(JSON.parse(localStorage.getItem(WKEY)||'[]'))}catch(e){return new Set()}}
let WISH=loadWish();
function saveWish(){try{localStorage.setItem(WKEY,JSON.stringify([...WISH]))}catch(e){}}
function toggleWish(id){id=+id;if(WISH.has(id)){WISH.delete(id);toast('Removed from wishlist');}else{WISH.add(id);toast('Added to wishlist ♥');}saveWish();syncWish();if(location.hash==='#/wishlist')renderWishlist();}
function syncWish(){document.getElementById('wishCount').textContent=WISH.size;
  document.querySelectorAll('[data-wish]').forEach(b=>{const on=WISH.has(+b.dataset.wish);b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);
    if(b.classList.contains('wl')){const s=b.querySelector('span');if(s)s.textContent=on?'In wishlist':'Add to wishlist';}});}
function wishClick(ev,id){ev.preventDefault();ev.stopPropagation();toggleWish(id);}

/* ---------- filter state ---------- */
const state={group:'all',theme:'',price:'',occ:'',sort:'featured',q:'',shown:0,page:48,list:[]};
function computeList(){
  let l=DB.items.slice();
  if(state.group!=='all')l=l.filter(i=>i.gk===state.group);
  if(state.theme)l=l.filter(i=>i.theme===state.theme);
  if(state.price)l=l.filter(i=>i.band===state.price);
  if(state.occ)l=l.filter(i=>i.occ.includes(state.occ));
  if(state.q){const q=state.q.toLowerCase();l=l.filter(i=>(i.name+' '+i.why+' '+i.theme+' '+i.group).toLowerCase().includes(q));}
  const s=state.sort;
  if(s==='price-asc')l.sort((a,b)=>a.rep-b.rep);
  else if(s==='price-desc')l.sort((a,b)=>b.rep-a.rep);
  else if(s==='wow')l.sort((a,b)=>b.wow-a.wow||a.rep-b.rep);
  else if(s==='name')l.sort((a,b)=>a.name.localeCompare(b.name));
  state.list=l;state.shown=0;
}

/* ---------- card ---------- */
function cardHTML(it){
  return '<a class="card" href="#/gift/'+it.id+'" aria-label="'+esc(it.name)+'">'
    +'<div class="thumb"><img loading="lazy" data-th="'+esc(it.theme)+'" alt="'+esc(it.name)+'" src="'+liveImg(it,0)+'" onerror="imgFail(this)">'
    +'<span class="price">'+PRICE_SHORT[it.band]+'</span>'
    +'<button class="fav'+(WISH.has(it.id)?' on':'')+'" data-wish="'+it.id+'" aria-label="Save to wishlist" aria-pressed="'+WISH.has(it.id)+'" onclick="wishClick(event,'+it.id+')">♥</button></div>'
    +'<div class="cbody"><div class="eyebrow">'+esc(it.theme)+'</div>'
    +'<h3>'+esc(it.name)+'</h3><p>'+esc(it.why)+'</p>'
    +'<div class="cfoot"><span class="stars" title="Wow rating">'+stars(it.wow)+'</span><span class="go">View →</span></div></div></a>';
}

/* ---------- render grid (storefront) ---------- */
function renderGrid(){
  const g=DB.groups.find(x=>x.key===state.group);
  const title=state.group==='all'?'All gifts':g.label;
  const controls=
    '<section class="hero"><div class="blob"></div>'
    +'<h1>Find the <em>perfect</em> gift.<br/>1,200 ideas, zero guesswork.</h1>'
    +'<p>Curated, non-generic gifts for every age and personality — filter by recipient, theme, budget and occasion, then buy from trusted Indian stores.</p>'
    +'<div class="stats"><div><b>1,200</b>curated ideas</div><div><b>12</b>recipient groups</div><div><b>120</b>themes</div></div></section>'
    +'<div class="rail" id="rail"></div>'
    +'<div class="filters">'
      +'<div class="sel"><select id="fTheme" aria-label="Filter by theme"></select></div>'
      +'<div class="sel"><select id="fPrice" aria-label="Filter by budget">'
        +'<option value="">Any budget</option><option value="A">Under ₹500</option><option value="B">₹500–1,500</option><option value="C">₹1,500–5,000</option><option value="D">₹5,000+</option></select></div>'
      +'<div class="sel"><select id="fOcc" aria-label="Filter by occasion"><option value="">Any occasion</option>'
        +DB.occasions.map(o=>'<option value="'+esc(o)+'">'+esc(o)+'</option>').join('')+'</select></div>'
      +'<div class="sel"><select id="fSort" aria-label="Sort">'
        +'<option value="featured">Sort: Featured</option><option value="wow">Wow factor</option>'
        +'<option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option>'
        +'<option value="name">A → Z</option></select></div>'
      +'<button class="reset" id="fReset">Reset</button>'
    +'</div>'
    +'<div class="chips" id="chips"></div>'
    +'<div class="resbar"><h2 id="resTitle">'+esc(title)+'</h2><span id="resCount"></span></div>'
    +'<div class="grid" id="grid"></div>'
    +'<div class="loadwrap" id="loadwrap"></div>';
  document.getElementById('view').innerHTML=controls;

  // recipient rail
  const rail=document.getElementById('rail');
  const mk=(key,label,n,on)=>{const b=document.createElement('button');b.className='cpill'+(on?' on':'');b.dataset.key=key;
    b.innerHTML=esc(label)+' <span class="n">'+n+'</span>';
    b.onclick=()=>{state.group=key;state.theme='';renderGrid();};rail.appendChild(b);};
  mk('all','All',DB.items.length,state.group==='all');
  DB.groups.forEach(g=>mk(g.key,g.label,DB.items.filter(i=>i.gk===g.key).length,state.group===g.key));

  // theme options (depend on group)
  const pool=state.group==='all'?DB.items:DB.items.filter(i=>i.gk===state.group);
  const themes=[...new Set(pool.map(i=>i.theme))].sort();
  const ft=document.getElementById('fTheme');
  ft.innerHTML='<option value="">All themes</option>'+themes.map(t=>'<option value="'+esc(t)+'">'+esc(t)+'</option>').join('');
  ft.value=state.theme; document.getElementById('fPrice').value=state.price;
  document.getElementById('fOcc').value=state.occ; document.getElementById('fSort').value=state.sort;
  document.getElementById('q').value=state.q;

  ft.onchange=e=>{state.theme=e.target.value;apply(false);};
  document.getElementById('fPrice').onchange=e=>{state.price=e.target.value;apply(false);};
  document.getElementById('fOcc').onchange=e=>{state.occ=e.target.value;apply(false);};
  document.getElementById('fSort').onchange=e=>{state.sort=e.target.value;apply(false);};
  document.getElementById('fReset').onclick=()=>{Object.assign(state,{group:'all',theme:'',price:'',occ:'',sort:'featured',q:''});renderGrid();};

  computeList();paintChips();paintPage();syncWish();
}
function paintChips(){
  const c=document.getElementById('chips');if(!c)return;const chips=[];
  const g=DB.groups.find(x=>x.key===state.group);
  if(state.group!=='all')chips.push(['Recipient: '+g.label,()=>{state.group='all';state.theme='';renderGrid();}]);
  if(state.theme)chips.push(['Theme: '+state.theme,()=>{state.theme='';apply(false);}]);
  if(state.price)chips.push(['Budget: '+PRICE_FULL[state.price],()=>{state.price='';apply(false);}]);
  if(state.occ)chips.push(['Occasion: '+state.occ,()=>{state.occ='';apply(false);}]);
  if(state.q)chips.push(['Search: “'+state.q+'”',()=>{state.q='';document.getElementById('q').value='';apply(false);}]);
  c.innerHTML='';
  chips.forEach(([label,fn])=>{const d=document.createElement('span');d.className='chip';
    d.innerHTML=esc(label)+' <button aria-label="Remove filter">×</button>';
    d.querySelector('button').onclick=fn;c.appendChild(d);});
}
function paintPage(){
  const grid=document.getElementById('grid');if(!grid)return;
  const end=Math.min(state.shown+state.page,state.list.length);
  let html='';for(let i=state.shown;i<end;i++)html+=cardHTML(state.list[i]);
  grid.insertAdjacentHTML('beforeend',html);state.shown=end;
  document.getElementById('resCount').textContent=state.list.length+' gift'+(state.list.length!==1?'s':'');
  const lw=document.getElementById('loadwrap');
  if(state.list.length===0){grid.innerHTML='<div class="empty"><div class="big">🎁</div><p>No gifts match those filters.<br>Try removing one or hit Reset.</p></div>';lw.innerHTML='';return;}
  if(state.shown<state.list.length){lw.innerHTML='<button class="loadmore" id="more">Load more ('+(state.list.length-state.shown)+' left)</button>';
    document.getElementById('more').onclick=()=>{paintPage();syncWish();};}
  else lw.innerHTML='';
  syncWish();
}
function apply(full){ // recompute + repaint grid section only
  if(full!==false && !document.getElementById('grid')){renderGrid();return;}
  const grid=document.getElementById('grid');
  computeList();grid.innerHTML='';document.getElementById('loadwrap').innerHTML='';
  // refresh theme list if group changed handled in renderGrid; here keep
  paintChips();paintPage();
  const g=DB.groups.find(x=>x.key===state.group);
  document.getElementById('resTitle').textContent=state.group==='all'?'All gifts':g.label;
  // update rail active
  document.querySelectorAll('.cpill').forEach(p=>p.classList.toggle('on',p.dataset.key===state.group));
}

/* ---------- render detail ---------- */
function renderDetail(id){
  const it=DB.byId[id];
  if(!it){location.hash='#/';return;}
  const links=buyLinks(it);const tp=tips(it);
  const ov=expandedOverview(it),pw=pairWith(it),dl=delivery(it),pt=proTip(it),tags=tagsFor(it);
  const gallery=
    '<div class="gallery"><div class="main"><img id="mainImg" alt="'+esc(it.name)+'" data-th="'+esc(it.theme)+'" src="'+liveImg(it,0)+'" onerror="imgFail(this)"></div>'
    +'<div class="gthumbs">'+[0,1,2,3].map(i=>
        '<button class="'+(i===0?'sel':'')+'" data-i="'+i+'" aria-label="View image '+(i+1)+'"><img loading="lazy" data-th="'+esc(it.theme)+'" alt="" src="'+liveImg(it,i)+'" onerror="imgFail(this)"></button>').join('')
    +'</div></div>';
  const buys='<div class="buys">'+links.map(l=>
    '<a class="buy" href="'+l.u+'" target="_blank" rel="noopener noreferrer"><span class="l"><span class="dot">'+l.e+'</span>'+esc(l.n)+'</span><span class="arr">↗</span></a>').join('')+'</div>';
  const on=WISH.has(it.id);
  const facts=[
    ['Category',it.theme],
    ['Best for',it.group+' · '+it.tag],
    ['Budget band',PRICE_FULL[it.band]],
    ['Wow rating','<span class="stars">'+stars(it.wow)+'</span> ('+it.wow+'/5)'],
    ['Personalisation',personalisable(it)?'Yes — can be customised':'Optional'],
    ['Where to buy',links.map(l=>esc(l.n)).join(', ')],
    ['Good occasions',it.occ.map(esc).join(', ')],
  ];
  const related=DB.items.filter(x=>x.id!==it.id && (x.theme===it.theme))
      .concat(DB.items.filter(x=>x.id!==it.id && x.gk===it.gk && x.theme!==it.theme))
      .slice(0,6);

  document.getElementById('view').innerHTML=
    '<div class="detail">'
    +'<div class="crumb"><button class="back" onclick="goBack()">← Back</button>'
      +'<a href="#/">Home</a><span>/</span>'
      +'<a href="#/" onclick="jumpGroup(\''+it.gk+'\');return false;">'+esc(it.group)+'</a><span>/</span>'
      +'<span>'+esc(it.theme)+'</span></div>'
    +'<div class="dtop">'+gallery
      +'<div class="dinfo"><div class="eyebrow">'+esc(it.theme)+'</div>'
        +'<h1>'+esc(it.name)+'</h1>'
        +'<div class="metarow"><span class="tagpill price">'+PRICE_SHORT[it.band]+'</span>'
          +'<span class="tagpill wow">'+stars(it.wow)+' Wow</span>'
          +'<span class="tagpill">'+esc(it.group)+'</span></div>'
        +'<p class="lead">'+esc(it.why)+'</p>'
        +'<div class="occwrap" style="margin:0 0 16px">'+tags.map(tg=>'<button class="occ" onclick="jumpSearch(\''+esc(tg).replace(/'/g,"\\'")+'\')">#'+esc(tg)+'</button>').join('')+'</div>'
        +'<div class="priceguide"><div class="k">Typical price</div><div class="v">'+PRICE_FULL[it.band]+'</div>'
          +'<div class="sub">Indicative range across Indian retailers — compare below for the best deal.</div></div>'
        +'<p class="buyhdr">Buy it from</p>'+buys
        +'<div class="dact"><button class="wl'+(on?' on':'')+'" data-wish="'+it.id+'" aria-pressed="'+on+'" onclick="toggleWish('+it.id+')">♥ <span>'+(on?'In wishlist':'Add to wishlist')+'</span></button>'
          +'<button onclick="shareItem('+it.id+')">↗ Share</button></div>'
      +'</div>'
    +'</div>'
    +'<div class="sections">'
      +'<div class="sec"><h3>🎁 Why it makes a great gift</h3><p>'+esc(ov)+'</p></div>'
      +'<div class="sec"><h3>🎀 Pair it with</h3><p>Make it feel complete — pair this with '+esc(pw.txt)+'.</p><div class="occwrap"><a class="occ" href="https://www.amazon.in/s?k='+encodeURIComponent(pw.q)+'" target="_blank" rel="noopener noreferrer">Shop pairing idea ↗</a></div></div>'
      +'<div class="sec"><h3>🗓️ Perfect for these occasions</h3><div class="occwrap">'
        +it.occ.map(o=>'<button class="occ" onclick="jumpOcc(\''+esc(o).replace(/'/g,"\\'")+'\')">'+esc(o)+'</button>').join('')+'</div></div>'
      +'<div class="sec"><h3>🔍 What to look for when buying</h3><ul>'+tp.map(x=>'<li>'+esc(x)+'</li>').join('')+'</ul></div>'
      +'<div class="sec"><h3>📋 Quick facts</h3><table class="facts">'
        +facts.map(f=>'<tr><td>'+f[0]+'</td><td>'+f[1]+'</td></tr>').join('')+'</table></div>'
      +'<div class="sec"><h3>📦 Good to know</h3><ul><li><b>Delivery:</b> '+esc(dl)+'</li><li><b>Pro tip:</b> '+esc(pt)+'</li><li><b>Budget flexibility:</b> most ideas here have cheaper and more premium versions — use the buy links to find the tier that fits.</li></ul></div>'
    +'</div>'
    +'<div class="related"><h3>You may also like</h3><div class="grid">'
      +related.map(cardHTML).join('')+'</div></div>'
    +'</div>';

  // gallery thumb switching
  document.querySelectorAll('.gthumbs button').forEach(b=>b.onclick=()=>{
    document.querySelectorAll('.gthumbs button').forEach(x=>x.classList.remove('sel'));
    b.classList.add('sel');
    const m=document.getElementById('mainImg');m.onerror=()=>imgFail(m);m.src=liveImg(it,+b.dataset.i);});
  syncWish();window.scrollTo({top:0});
}
function shareItem(id){const it=DB.byId[id];const url=location.origin+location.pathname+'#/gift/'+id;
  if(navigator.share){navigator.share({title:it.name,text:it.why,url}).catch(()=>{});}
  else{navigator.clipboard?.writeText(url).then(()=>toast('Link copied to clipboard'),()=>toast('Copy failed'));}}
function goBack(){if(history.length>1)history.back();else location.hash='#/';}
function surprise(){const it=DB.items[Math.floor(Math.random()*DB.items.length)];toast('🎲 A little inspiration…');location.hash='#/gift/'+it.id;}
function jumpGroup(gk){Object.assign(state,{group:gk,theme:'',price:'',occ:'',q:''});location.hash='#/';}
function jumpOcc(o){Object.assign(state,{group:'all',theme:'',price:'',occ:o,q:''});location.hash='#/';}

/* ---------- wishlist page ---------- */
function renderWishlist(){
  const ids=[...WISH];const list=ids.map(id=>DB.byId[id]).filter(Boolean);
  let html='<div class="detail"><div class="crumb"><button class="back" onclick="location.hash=\'#/\'">← Continue browsing</button>'
    +'<a href="#/">Home</a><span>/</span><span>Wishlist</span></div>'
    +'<div class="resbar"><h2>Your wishlist</h2><span>'+list.length+' saved</span></div>';
  if(!list.length){
    html+='<div class="empty"><div class="big">♡</div><p>Your wishlist is empty.<br>Tap the heart on any gift to save it here.</p>'
      +'<div class="loadwrap"><button class="loadmore" onclick="location.hash=\'#/\'">Browse gifts</button></div></div>';
  }else{
    html+='<div class="filters" style="margin:4px 0 10px"><button class="reset" style="margin-left:0" onclick="clearWish()">Clear all</button></div>';
    html+='<div class="grid">'+list.map(cardHTML).join('')+'</div>';
  }
  html+='</div>';
  document.getElementById('view').innerHTML=html;syncWish();window.scrollTo({top:0});
}
function clearWish(){if(confirm('Remove all saved gifts?')){WISH.clear();saveWish();syncWish();renderWishlist();toast('Wishlist cleared');}}

/* ---------- router ---------- */
function route(){
  const h=location.hash;
  if(h.startsWith('#/gift/')){renderDetail(+h.split('/')[2]);}
  else if(h==='#/wishlist'){renderWishlist();}
  else{renderGrid();}
}
window.addEventListener('hashchange',route);

/* header search works from any view */
document.getElementById('q').addEventListener('input',debounce(function(e){
  state.q=e.target.value;
  if(location.hash.startsWith('#/gift')||location.hash==='#/wishlist'){location.hash='#/';/* route()->renderGrid reads state.q */}
  else apply(false);
},220));

/* back-to-top */
const tt=document.getElementById('toTop');
window.addEventListener('scroll',()=>{tt.style.display=scrollY>640?'block':'none';});
tt.onclick=()=>scrollTo({top:0,behavior:'smooth'});

route();
</script>
</body>
</html>"""

out = TEMPLATE.replace("__DATA__", DATA)
open(os.path.join(DIST,"Aurl_Gift_Atelier.html"), "w", encoding="utf-8").write(out)
print("wrote Aurl_Gift_Atelier.html", len(out), "bytes; items:", len(items))
