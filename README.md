# Aurl · The Gift Atelier

A single HTML file that turns 1,200 curated gift ideas into a browsable store. Open it in any browser. No server, no build step for the reader, works offline behind a firewall.

## The problem I was solving

Most "gift ideas" lists are useless. They're generic (mug, wallet, watch), they lump everyone into "for him / for her," and they stop at the idea. You still have to go figure out where to buy it, whether it suits a 9-year-old or a 60-year-old, and what to check before you spend.

I wanted the opposite: a set of specific, non-obvious ideas, sorted by who they're actually for, where each idea opens into a real page that tells you why it lands, when to give it, what to watch for, and where to buy it in India.

## What it does

- **1,200 ideas, 12 recipient groups, 100 each.** Kids, teens, adults by age, seniors, a unisex "anyone" set, and a premium set above Rs 5,000.
- **Faceted browsing.** Filter by recipient, theme (120 of them), budget band, and occasion. Sort by featured, wow factor, price, or A to Z. Active filters show as chips you can remove one at a time.
- **Every tile opens its own page.** Real URL via hash routing, working back button. Each page has an image gallery, a wow rating, three to four buy links, an expanded overview, a "pair it with" suggestion, matching occasions, a "what to look for when buying" checklist, a quick-facts table, and delivery plus pro-tip notes.
- **Wishlist that works.** Heart any gift, it saves to `localStorage` and survives a refresh. A wishlist page lists everything you saved, with remove and clear-all.
- **Live images with a safety net.** Each card loads a keyword photo. If the network is blocked, it falls back to a generated SVG tile so nothing ever looks broken.
- **Surprise me.** One button drops you on a random gift page when you don't know where to start.

## Who it's for

Anyone stuck on "what do I get them." The recipient groups do the first cut for you, then the filters narrow it in a few clicks. It also works as a content source: the same 1,200 records ship as JSON and CSV if you want to feed a real store, a quiz, or a newsletter.

## How it's built

The pipeline is deliberately dull, which is the point. Python owns the data, the browser owns the experience, and they meet through one JSON blob.

1. `builder/data_part1.py` through `data_part7.py` hold the ideas as plain Python lists. Each idea is a tuple: name, theme, price band, and one line on why it's a good gift.
2. `builder/build_data.py` validates the set (asserts 100 per group, zero duplicate names inside a group), normalizes it, and writes `dist/_records.json`, `dist/gift_ideas_1200.json`, and `dist/gift_ideas_1200.csv`.
3. `builder/build_store.py` reads that JSON, derives the extra fields at build time (occasions, wow score, keyword for image and buy-link search, buying tips, pairing suggestion), and inlines everything into one self-contained HTML file at `dist/Aurl_Gift_Atelier.html`.

The browser side is vanilla JavaScript: a hash router, a filter and sort function, incremental rendering (48 cards at a time so 1,200 items don't stall the page), and the wishlist. No framework, no bundler, no dependencies.

`builder/build_luxe.py` is an earlier, simpler theme kept for reference. You can ignore it.

## Run it

You need Python 3 and Node (Node only for the test).

```bash
# from the repo root
python builder/build_data.py     # writes dist/_records.json + json + csv
python builder/build_store.py    # writes dist/Aurl_Gift_Atelier.html
open dist/Aurl_Gift_Atelier.html # or just double-click it
```

Or with npm:

```bash
npm run build
npm test
```

## Repo layout

```
builder/
  data_part1.py … data_part7.py   the 1,200 ideas, as source
  build_data.py                   validates + exports json/csv + _records.json
  build_store.py                  builds the storefront HTML
  build_luxe.py                   older alternate theme (optional)
tests/
  dom-harness.js                  runtime tests against the built HTML
dist/
  Aurl_Gift_Atelier.html          the product
  gift_ideas_1200.json            raw data, pretty-printed
  gift_ideas_1200.csv             flat export
```

## Testing

`tests/dom-harness.js` extracts the app's script from the built HTML, runs it against a small DOM stub, and exercises the real code paths: filtering, search, routing, the wishlist, and rendering. It renders all 1,200 detail pages and checks that none throw, that every item has three to four buy links, at least four buying tips, an overview, occasions, and that card output escapes HTML.

```bash
node tests/dom-harness.js
# 22 checks, expected: "All checks passed."
```

I ran three adversarial review rounds before shipping: one for functional bugs, one for design and accessibility, one from a shopper's point of view. Fixes from each round are in `build_store.py`, and the test count grew as I went.

## Decisions and tradeoffs

A few calls I made on purpose, so you're not surprised:

- **No live price scraping.** I chose not to scrape a rupee price for each of the 1,200 items. There's no stable public API, and any number I scraped would be wrong within days. A stale price is worse than no price. Instead, each gift shows a budget band plus three to four buy links so you compare the real price yourself when you're ready to order.
- **Buy links are searches, not exact product URLs.** Every gift links to a search on Amazon.in, Flipkart, and Google Shopping, plus one category-appropriate retailer (IGP for personalized, Bigsmall for gadgets, FirstCry for kids, Myntra for fashion, WonderGifts for experiences). Search links stay alive as catalogs change. Deep links to a single SKU rot.
- **Images are illustrative.** Cards pull a keyword photo from LoremFlickr, not the actual product. Good enough to make browsing feel real, honest about not being a catalog.
- **One file, on purpose.** The whole app is a single HTML file so you can email it, host it anywhere, or run it with no internet. The cost is a 464 KB file with data inlined. For 1,200 items that's fine.

## What I'd build next

- A quiz-style gift finder (three questions to a shortlist) on top of the same data.
- A "share my wishlist" link that encodes saved IDs in the URL.
- Real product links and prices for a top-100 subset, refreshed on a schedule, kept separate from the evergreen ideas.
- Split the price band into low / typical / premium once there's a reliable price source.

## License

MIT. The ideas and copy are yours to use, edit, and ship.
