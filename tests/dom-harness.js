/*
 * Runtime smoke tests for the built storefront.
 *
 * The site ships as one HTML file with all logic in a single <script>. This
 * test extracts that script, runs it against a tiny DOM stub, then exercises
 * the filtering, routing, wishlist, and detail-page code across all 1,200
 * items. It checks for thrown exceptions and a few invariants.
 *
 * Run:  node tests/dom-harness.js
 * Needs: dist/Aurl_Gift_Atelier.html (run the two Python builders first).
 */
const fs = require("fs");
const path = require("path");

const htmlPath = path.join(__dirname, "..", "dist", "Aurl_Gift_Atelier.html");
if (!fs.existsSync(htmlPath)) {
  console.error("Build the site first: python builder/build_data.py && python builder/build_store.py");
  process.exit(2);
}
const html = fs.readFileSync(htmlPath, "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const app = scripts[scripts.length - 1];

// ---- minimal DOM / browser stub ----
function makeEl() {
  const el = {
    children: [], style: {}, dataset: {}, _html: "", value: "", textContent: "",
    classList: {
      _s: new Set(), add(x){this._s.add(x)}, remove(x){this._s.delete(x)},
      toggle(x,f){f===undefined?(this._s.has(x)?this._s.delete(x):this._s.add(x)):(f?this._s.add(x):this._s.delete(x))},
      contains(x){return this._s.has(x)}
    },
    setAttribute(){}, getAttribute(){return null}, removeAttribute(){},
    appendChild(c){this.children.push(c);return c}, insertAdjacentHTML(){},
    addEventListener(){}, focus(){}, click(){},
    querySelector(){return makeEl()}, querySelectorAll(){return []},
    get innerHTML(){return this._html}, set innerHTML(v){this._html = String(v)}
  };
  return el;
}
const reg = {};
global.document = {
  getElementById: id => reg[id] || (reg[id] = makeEl()),
  createElement: () => makeEl(),
  querySelector: () => makeEl(), querySelectorAll: () => [],
  addEventListener(){}, body: makeEl()
};
global.window = { addEventListener(){}, scrollTo(){}, scrollY: 0 };
global.location = { hash: "", origin: "file://", pathname: "/x.html" };
global.history = { length: 1, back(){} };
global.navigator = { clipboard: { writeText: () => Promise.resolve() } };
let store = {};
global.localStorage = {
  getItem: k => store[k] || null, setItem: (k, v) => (store[k] = v), removeItem: k => delete store[k]
};
global.confirm = () => true;
global.setTimeout = f => { try { f && f(); } catch (e) {} };
global.clearTimeout = () => {};
global.scrollTo = () => {};

const failures = [];
const epilogue = `
;(function(){
  function T(name, fn){ try{ fn(); console.log("ok   " + name); }
    catch(e){ failuresRef.push(name + " :: " + e.message); console.log("FAIL " + name + " :: " + e.message); } }
  T("render storefront", () => renderGrid());
  T("filter by theme", () => { state.theme = DB.items[0].theme; apply(false); state.theme = ""; });
  T("filter by price", () => { state.price = "C"; computeList(); state.price = ""; });
  T("filter by occasion", () => { state.occ = "Birthday"; computeList(); state.occ = ""; });
  T("search finds results", () => { state.q = "telescope"; computeList(); if(!state.list.length) throw new Error("no results"); state.q = ""; });
  T("detail page (valid id)", () => renderDetail(DB.items[500].id));
  T("detail page (bad id) recovers", () => renderDetail(999999));
  T("every item has 3-4 buy links", () => { DB.items.forEach(i => { const n = buyLinks(i).length; if(n < 3 || n > 4) throw new Error("id " + i.id + " has " + n); }); });
  T("every item has >=4 buying tips", () => { DB.items.forEach(i => { if(tips(i).length < 4) throw new Error("id " + i.id); }); });
  T("every item has occasions", () => { DB.items.forEach(i => { if(!i.occ || !i.occ.length) throw new Error("id " + i.id); }); });
  T("expanded overview present", () => { DB.items.forEach(i => { if(expandedOverview(i).length < 40) throw new Error("id " + i.id); }); });
  T("pair-with present", () => { DB.items.forEach(i => { const p = pairWith(i); if(!p.txt || !p.q) throw new Error("id " + i.id); }); });
  T("delivery + pro tip present", () => { DB.items.forEach(i => { if(!delivery(i) || !proTip(i)) throw new Error("id " + i.id); }); });
  T("tags present (max 4)", () => { DB.items.forEach(i => { const t = tagsFor(i); if(!t.length || t.length > 4) throw new Error("id " + i.id); }); });
  T("render ALL 1200 detail pages", () => { DB.items.forEach(i => renderDetail(i.id)); });
  T("wishlist add / remove", () => { toggleWish(DB.items[3].id); toggleWish(DB.items[4].id); if(WISH.size!==2) throw new Error("size " + WISH.size); toggleWish(DB.items[3].id); if(WISH.size!==1) throw new Error("remove failed"); });
  T("wishlist persists to storage", () => { if(!localStorage.getItem("aurl_wishlist_v1")) throw new Error("not saved"); });
  T("wishlist page renders", () => renderWishlist());
  T("HTML is escaped in cards", () => { const bad = {id:1,gk:"x",group:"O'B & <b>",tag:"t",theme:"A/B & 'c'",name:'N "q" <x>',why:"w's & <i>",band:"B",pl:"x",kw:"a b",occ:["Birthday"],rep:900,wow:3}; const h = cardHTML(bad); if(/<b>|<x>|<i>/.test(h)) throw new Error("unescaped"); });
  T("image fallback is inline SVG", () => { const el = {dataset:{th:"STEM & Science"},src:"",onerror:1}; imgFail(el); if(!el.src.startsWith("data:image/svg")) throw new Error("no fallback"); });
  T("names unique within each group", () => { const seen={}; DB.items.forEach(i => { const k = i.gk + "|" + i.name; if(seen[k]) throw new Error("dup " + k); seen[k]=1; }); });
})();
`;

global.failuresRef = failures;
eval(app + epilogue);

console.log("\n" + (failures.length ? failures.length + " FAILURE(S)" : "All checks passed."));
process.exit(failures.length ? 1 : 0);
