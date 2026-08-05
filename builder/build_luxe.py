# -*- coding: utf-8 -*-
import json, os
HERE=os.path.dirname(os.path.abspath(__file__))
DIST=os.path.join(HERE,"..","dist")
os.makedirs(DIST,exist_ok=True)

d = json.load(open(os.path.join(DIST,"_records.json"), encoding="utf-8"))
DATA_JS = json.dumps({"ideas": d["ideas"], "groups": d["groups"],
                      "priceLabels": d["price_labels"]}, ensure_ascii=False)

html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Luxe Gifts — 1,200 Curated Ideas</title>
<style>
  :root{
    --bg:#F4F1EA;          /* warm ivory canvas */
    --card:#FFFFFF;
    --ink:#16150F;         /* near-black */
    --mut:#8C876F;         /* warm grey */
    --line:#E7E1D3;
    --accent:#C7F24C;      /* lime pop */
    --accent-ink:#1c2107;
    --chip:#F1ECDF;
    --shadow:0 10px 30px rgba(30,26,10,.08);
    --shadow-s:0 4px 14px rgba(30,26,10,.06);
  }
  *{box-sizing:border-box}
  html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:'Segoe UI',-apple-system,system-ui,Roboto,Arial,sans-serif;-webkit-font-smoothing:antialiased}
  .app{max-width:1160px;margin:0 auto;padding:0 18px 90px}

  /* Top bar */
  .top{position:sticky;top:0;z-index:40;background:rgba(244,241,234,.86);backdrop-filter:blur(12px);
    padding:16px 0 12px;border-bottom:1px solid var(--line)}
  .bar{display:flex;align-items:center;gap:14px}
  .brand{display:flex;align-items:center;gap:10px;font-weight:800;font-size:20px;letter-spacing:-.3px}
  .brand .dot{width:34px;height:34px;border-radius:11px;background:var(--ink);display:grid;place-items:center;color:var(--accent);font-size:18px}
  .brand small{display:block;font-weight:500;font-size:10.5px;letter-spacing:2px;color:var(--mut);text-transform:uppercase;margin-top:1px}
  .cart{margin-left:auto;width:44px;height:44px;border-radius:14px;background:var(--card);border:1px solid var(--line);
    display:grid;place-items:center;font-size:18px;box-shadow:var(--shadow-s);position:relative}
  .cart b{position:absolute;top:-6px;right:-6px;background:var(--accent);color:var(--accent-ink);font-size:10px;
    font-weight:800;min-width:18px;height:18px;border-radius:9px;display:grid;place-items:center;padding:0 4px}

  /* Hero */
  .hero{margin:20px 0 6px;padding:26px 26px 24px;border-radius:26px;position:relative;overflow:hidden;
    background:linear-gradient(135deg,#16150F 0%,#2a2718 100%);color:#fff;box-shadow:var(--shadow)}
  .hero h1{margin:0 0 8px;font-size:30px;line-height:1.12;letter-spacing:-.6px;font-weight:800;max-width:640px}
  .hero h1 em{font-style:normal;color:var(--accent)}
  .hero p{margin:0;color:#d9d4c2;font-size:14.5px;max-width:560px}
  .hero .blob{position:absolute;right:-40px;top:-40px;width:220px;height:220px;border-radius:50%;
    background:radial-gradient(circle at 30% 30%,var(--accent),transparent 62%);opacity:.5;filter:blur(6px)}
  .hero .mini{display:flex;gap:22px;margin-top:16px}
  .hero .mini div{font-size:12.5px;color:#cfcab8}
  .hero .mini b{display:block;font-size:20px;color:#fff;font-weight:800}

  /* Search */
  .search{margin:16px 0 4px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
  .field{flex:1;min-width:230px;display:flex;align-items:center;gap:10px;background:var(--card);
    border:1px solid var(--line);border-radius:16px;padding:13px 16px;box-shadow:var(--shadow-s)}
  .field input{border:none;outline:none;background:transparent;font-size:15px;width:100%;color:var(--ink)}
  .field .ic{font-size:16px;color:var(--mut)}
  select{appearance:none;background:var(--card);border:1px solid var(--line);border-radius:16px;
    padding:13px 40px 13px 16px;font-size:14px;color:var(--ink);box-shadow:var(--shadow-s);cursor:pointer;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%238C876F' stroke-width='3'><path d='M6 9l6 6 6-6'/></svg>");
    background-repeat:no-repeat;background-position:right 15px center}
  .reset{background:var(--ink);color:#fff;border:none;border-radius:16px;padding:13px 18px;font-size:14px;font-weight:600;cursor:pointer;box-shadow:var(--shadow-s)}

  /* Category pills */
  .cats{display:flex;gap:9px;overflow-x:auto;padding:14px 2px 6px;scrollbar-width:none}
  .cats::-webkit-scrollbar{display:none}
  .pill{flex:0 0 auto;padding:10px 16px;border-radius:999px;background:var(--card);border:1px solid var(--line);
    color:var(--ink);font-size:13.5px;font-weight:600;cursor:pointer;white-space:nowrap;transition:.15s;box-shadow:var(--shadow-s)}
  .pill .n{color:var(--mut);font-weight:600;margin-left:5px}
  .pill.active{background:var(--ink);color:#fff;border-color:var(--ink)}
  .pill.active .n{color:var(--accent)}

  .rowhead{display:flex;align-items:baseline;justify-content:space-between;margin:20px 4px 6px}
  .rowhead h2{margin:0;font-size:19px;letter-spacing:-.3px}
  .rowhead span{font-size:13px;color:var(--mut)}

  /* Grid + cards */
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin-top:6px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:22px;overflow:hidden;
    display:flex;flex-direction:column;box-shadow:var(--shadow-s);transition:.18s}
  .card:hover{transform:translateY(-4px);box-shadow:var(--shadow)}
  .thumb{height:150px;position:relative;display:grid;place-items:center;font-size:52px}
  .thumb .price{position:absolute;top:12px;left:12px;background:rgba(255,255,255,.92);backdrop-filter:blur(4px);
    color:var(--ink);font-size:11.5px;font-weight:800;padding:6px 11px;border-radius:999px;box-shadow:var(--shadow-s)}
  .thumb .fav{position:absolute;top:12px;right:12px;width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.92);
    display:grid;place-items:center;font-size:14px;cursor:pointer;box-shadow:var(--shadow-s);border:none;color:#c9c3af}
  .thumb .fav.on{color:#ff5a7a}
  .body{padding:14px 15px 16px;display:flex;flex-direction:column;flex:1}
  .body .th{font-size:10.5px;letter-spacing:.7px;text-transform:uppercase;color:var(--mut);font-weight:800}
  .body h3{margin:6px 0 6px;font-size:15.5px;line-height:1.3;letter-spacing:-.2px}
  .body p{margin:0;color:var(--mut);font-size:13px;line-height:1.5;flex:1}
  .cardfoot{display:flex;align-items:center;justify-content:space-between;margin-top:13px}
  .gtag{font-size:11px;color:var(--mut);font-weight:600}
  .add{width:38px;height:38px;border-radius:12px;background:var(--accent);border:none;color:var(--accent-ink);
    font-size:20px;font-weight:800;cursor:pointer;display:grid;place-items:center;transition:.15s}
  .add:hover{transform:scale(1.08)}
  .add.done{background:var(--ink);color:var(--accent)}

  .empty{text-align:center;color:var(--mut);padding:70px 20px;font-size:15px}
  footer{text-align:center;color:var(--mut);font-size:12px;padding:26px 10px}
  .toTop{position:fixed;right:18px;bottom:20px;width:48px;height:48px;border-radius:16px;background:var(--ink);
    color:var(--accent);border:none;font-size:20px;cursor:pointer;display:none;box-shadow:var(--shadow);z-index:50}
  @media(max-width:520px){.hero h1{font-size:25px}.thumb{height:130px;font-size:44px}}
</style>
</head>
<body>
<div class="top">
  <div class="app" style="padding-bottom:0">
    <div class="bar">
      <div class="brand"><span class="dot">◆</span><div>Luxe&nbsp;Gifts<small>Curated store</small></div></div>
      <div class="cart">🛍️<b id="cartN">0</b></div>
    </div>
  </div>
</div>

<div class="app">
  <section class="hero">
    <div class="blob"></div>
    <h1>Find the <em>perfect</em> gift.<br/>1,200 ideas, zero guesswork.</h1>
    <p>Curated, non-generic gifts for every age and personality — filtered by theme and budget, buyable online in India.</p>
    <div class="mini">
      <div><b>1,200</b>curated ideas</div>
      <div><b>12</b>demographics</div>
      <div><b>120</b>themes</div>
    </div>
  </section>

  <div class="search">
    <label class="field"><span class="ic">🔍</span>
      <input id="q" type="search" placeholder="Search gifts — 'telescope', 'star map', 'spa', 'coding'…"/>
    </label>
    <select id="theme"><option value="">All themes</option></select>
    <select id="price">
      <option value="">Any budget</option>
      <option value="A">₹0–500</option>
      <option value="B">₹500–1,500</option>
      <option value="C">₹1,500–5,000</option>
      <option value="D">₹5,000+</option>
    </select>
    <button class="reset" id="reset">Reset</button>
  </div>

  <div class="cats" id="cats"></div>

  <div class="rowhead">
    <h2 id="rowTitle">All groups</h2>
    <span id="count"></span>
  </div>

  <div class="grid" id="grid"></div>
  <div class="empty" id="empty" style="display:none">No gifts match those filters. Try Reset.</div>
</div>

<button class="toTop" id="toTop">↑</button>
<footer>Luxe Gifts · demo store · 12 demographics × 100 ideas = 1,200 · Luxeshop-inspired UI. Prices are indicative bands.</footer>

<script>
const DB = __DATA__;
const PMAP={A:'₹0–500',B:'₹500–1.5k',C:'₹1.5–5k',D:'₹5k+'};
const FAV=new Set(); let CART=0;
let state={group:'all',theme:'',price:'',q:''};

/* thumbnail: soft duo-tone gradient by theme hash + glyph */
function hueOf(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))%360;return h;}
function glyph(t){t=t.toLowerCase();const m=[
 [['robot','coding'],'🤖'],[['stem','science','discovery'],'🔬'],[['build','construction'],'🧩'],
 [['space','nature'],'🪐'],[['art','making'],'🎨'],[['music','performance'],'🎵'],
 [['game','puzzle'],'♟️'],[['book','story','reading','learning'],'📚'],[['early years'],'🧸'],
 [['wellness','mindful'],'🧘'],[['fitness','movement','sport','outdoor','adventure'],'🏋️'],
 [['jewell','watch'],'💍'],[['fashion','bag','style','dress','clothing'],'👜'],
 [['home','decor','room','aesthetic'],'🛋️'],[['kitchen','gourmet','food','baking','foodie'],'🍽️'],
 [['bar','tasting'],'🥃'],[['travel'],'✈️'],[['experience'],'🎟️'],
 [['tech','gadget','edc','utility','pop'],'🎧'],[['groom'],'🧴'],[['desk','office','wfh','study'],'🖥️'],
 [['health','comfort','mobility','monitoring'],'🩺'],[['faith','spiritual','devotion'],'🪔'],
 [['sentimental','keepsake','personalised','nostalgia','anniversary','milestone'],'🎁'],
 [['sustainable'],'🌱'],[['plant','green'],'🪴'],[['couple'],'💞'],[['friend'],'🫶'],
 [['sibling','family'],'👪'],[['cowork'],'🏆'],[['housewarming'],'🏠'],[['quirky'],'✨'],
 [['subscription'],'📦'],[['skill','side-hustle'],'🛠️'],[['collectible','luxury','premium','big-ticket'],'💎'],
 [['hobby','hobbies'],'🎯'],[['fandom'],'⚽']];
 for(const[keys,e]of m)if(keys.some(k=>t.includes(k)))return e;return '🎁';}

const cats=document.getElementById('cats'),grid=document.getElementById('grid'),
 themeSel=document.getElementById('theme'),countEl=document.getElementById('count'),
 emptyEl=document.getElementById('empty'),rowTitle=document.getElementById('rowTitle');

/* pills */
addPill('all','All groups',DB.ideas.length,true);
DB.groups.forEach(g=>addPill(g.key,g.label,DB.ideas.filter(i=>i.group_key===g.key).length,false));
function addPill(key,label,n,active){
  const p=document.createElement('div');p.className='pill'+(active?' active':'');p.dataset.key=key;
  p.innerHTML=label+' <span class="n">'+n+'</span>';
  p.onclick=()=>{state.group=key;rowTitle.textContent=label;refreshThemes();
    document.querySelectorAll('.pill').forEach(x=>x.classList.remove('active'));p.classList.add('active');render();};
  cats.appendChild(p);
}
function refreshThemes(){
  const pool=state.group==='all'?DB.ideas:DB.ideas.filter(i=>i.group_key===state.group);
  const th=[...new Set(pool.map(i=>i.theme))].sort();
  themeSel.innerHTML='<option value="">All themes</option>'+th.map(t=>`<option>${t}</option>`).join('');
  state.theme='';
}
function render(){
  let l=DB.ideas.slice();
  if(state.group!=='all')l=l.filter(i=>i.group_key===state.group);
  if(state.theme)l=l.filter(i=>i.theme===state.theme);
  if(state.price)l=l.filter(i=>i.price_band===state.price);
  if(state.q){const q=state.q.toLowerCase();l=l.filter(i=>(i.name+' '+i.why+' '+i.theme+' '+i.group).toLowerCase().includes(q));}
  countEl.textContent=l.length+' gift'+(l.length!==1?'s':'');
  emptyEl.style.display=l.length?'none':'block';
  grid.innerHTML='';const f=document.createDocumentFragment();
  l.forEach(i=>{
    const h=hueOf(i.theme);const c=document.createElement('div');c.className='card';
    c.innerHTML=`<div class="thumb" style="background:linear-gradient(150deg,hsl(${h} 70% 88%),hsl(${(h+40)%360} 65% 80%))">
        <span class="price">${PMAP[i.price_band]}</span>
        <button class="fav" data-id="${i.id}">♥</button>
        <span>${glyph(i.theme)}</span>
      </div>
      <div class="body">
        <div class="th">${i.theme}</div>
        <h3>${i.name}</h3>
        <p>${i.why}</p>
        <div class="cardfoot">
          <span class="gtag">${i.group}</span>
          <button class="add" title="Add to cart">+</button>
        </div>
      </div>`;
    f.appendChild(c);
  });
  grid.appendChild(f);
}
/* interactions */
document.getElementById('q').addEventListener('input',e=>{state.q=e.target.value;render();});
themeSel.addEventListener('change',e=>{state.theme=e.target.value;render();});
document.getElementById('price').addEventListener('change',e=>{state.price=e.target.value;render();});
document.getElementById('reset').addEventListener('click',()=>{
  state={group:'all',theme:'',price:'',q:''};
  document.getElementById('q').value='';document.getElementById('price').value='';
  document.querySelectorAll('.pill').forEach(x=>x.classList.remove('active'));
  cats.firstChild.classList.add('active');rowTitle.textContent='All groups';refreshThemes();render();
});
grid.addEventListener('click',e=>{
  const add=e.target.closest('.add');
  if(add){add.classList.add('done');add.textContent='✓';CART++;document.getElementById('cartN').textContent=CART;
    setTimeout(()=>{add.classList.remove('done');add.textContent='+';},700);return;}
  const fav=e.target.closest('.fav');
  if(fav){fav.classList.toggle('on');}
});
const tt=document.getElementById('toTop');
window.addEventListener('scroll',()=>{tt.style.display=scrollY>600?'block':'none';});
tt.onclick=()=>scrollTo({top:0,behavior:'smooth'});
refreshThemes();render();
</script>
</body>
</html>"""

html = html.replace("__DATA__", DATA_JS)
open(os.path.join(DIST,"GiftGrid_Luxe.html"),"w",encoding="utf-8").write(html)
print("wrote GiftGrid_Luxe.html", len(html), "bytes")
