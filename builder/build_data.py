# -*- coding: utf-8 -*-
"""Turn the Python idea files into the data artifacts the site consumes.

Outputs (into ../dist):
  _records.json        normalized records + group metadata (used by build_store.py)
  gift_ideas_1200.json same data, pretty-printed, for anyone who wants the raw set
  gift_ideas_1200.csv  flat spreadsheet export
"""
import json, csv, os
import data_part1, data_part2, data_part3, data_part4, data_part5, data_part6, data_part7
from data_part1 import DATA, GROUPS_META

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "..", "dist")
os.makedirs(DIST, exist_ok=True)

PRICE_LABEL = {"A": "Rs 0-500", "B": "Rs 500-1,500",
               "C": "Rs 1,500-5,000", "D": "Rs 5,000+"}

# 1. validate every group has exactly 100 ideas
print("Count check")
total = 0
for key, label, tag in GROUPS_META:
    n = len(DATA.get(key, []))
    total += n
    print(f"  {label:26s} {n:4d}  {'ok' if n == 100 else 'MISMATCH ' + str(n)}")
print(f"  {'total':26s} {total:4d}")
assert total == 1200, "expected 1200 ideas"

# 2. normalize
records, gid = [], 1
for key, label, tag in GROUPS_META:
    for (name, theme, band, why) in DATA[key]:
        records.append({"id": gid, "group_key": key, "group": label,
                        "theme": theme, "name": name, "why": why,
                        "price_band": band, "price_label": PRICE_LABEL[band]})
        gid += 1

# 3. no duplicate names inside a group
from collections import Counter, defaultdict
byg = defaultdict(list)
for r in records:
    byg[r["group"]].append(r["name"])
dups = sum(1 for g, n in byg.items() for k, v in Counter(n).items() if v > 1)
print("Duplicate names within a group:", dups)
assert dups == 0, "found duplicate names"

groups_json = [{"key": k, "label": l, "tag": t} for (k, l, t) in GROUPS_META]

json.dump({"groups": groups_json, "price_labels": PRICE_LABEL, "ideas": records},
          open(os.path.join(DIST, "_records.json"), "w", encoding="utf-8"),
          ensure_ascii=False)

json.dump({"groups": groups_json, "price_labels": PRICE_LABEL, "ideas": records},
          open(os.path.join(DIST, "gift_ideas_1200.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

with open(os.path.join(DIST, "gift_ideas_1200.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "group", "age_demographic_tag", "theme",
                "gift_idea", "why_unique", "price_band", "price_range"])
    for r in records:
        tag = next(t for (k, l, t) in GROUPS_META if k == r["group_key"])
        w.writerow([r["id"], r["group"], tag, r["theme"], r["name"],
                    r["why"], r["price_band"], r["price_label"]])

print("Wrote _records.json, gift_ideas_1200.json, gift_ideas_1200.csv to dist/")
