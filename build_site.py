#!/usr/bin/env python3
"""Regenerate the data embedded in index.html from the CSVs.

    python3 build_site.py

The page states counts, draws two charts and lists all 76 coded items. None of
that is typed into the HTML by hand: it is written between the BUILD:DATA
markers from `coded.csv`, `corpus/corpus.csv` and `corpus/sampling-log.json`.

That matters because the codebook is still being revised. When a code is renamed,
merged or dropped, this script is re-run and the page follows. Hand-maintained
numbers in a page whose whole argument is "check the data yourself" would be the
one error the study cannot afford.
"""
from __future__ import annotations

import collections
import csv
import json
import re
import sys

CORPUS = "corpus/corpus.csv"
CODED = "coded.csv"
SCREENING = "screening.csv"
LOG = "corpus/sampling-log.json"
PAGE = "index.html"

START = "<!--BUILD:DATA-->"
END = "<!--/BUILD:DATA-->"


def build() -> dict:
    rows = {r["item_id"]: r for r in csv.DictReader(open(CORPUS, encoding="utf-8"))}
    coded = list(csv.DictReader(open(CODED, encoding="utf-8")))
    screening = list(csv.DictReader(open(SCREENING, encoding="utf-8")))
    log = json.load(open(LOG, encoding="utf-8"))

    funnel = {s["stage"]: s["items"] for s in log["funnel"]}
    retrieved = funnel["items retrieved (posts + comments)"]
    in_corpus = funnel["items included in corpus"]
    read = sum(1 for r in screening if r["reason"] != "below-recall-gate")

    items = []
    for c in coded:
        row = rows[c["item_id"]]
        items.append({
            "id": row["item_id"],
            "code": c["code"],
            "who": row["author"],
            "year": row["created_utc"][:4],
            "thread": row["title"],
            "text": row["text"],
        })
    items.sort(key=lambda i: (i["code"], i["year"], i["id"]))

    per_code = collections.Counter(i["code"] for i in items)
    threads = {code: len({rows[i["id"]]["thread_id"] for i in items if i["code"] == code})
               for code in per_code}
    codes = [{"id": code, "items": n, "threads": threads[code]}
             for code, n in per_code.most_common()]

    # The funnel, as four sequential stages with what each one removed. Built
    # from the log rather than restated, so the page cannot claim a drop the
    # sampling record does not show.
    excl = {e["reason"]: e["count"] for e in log["exclusions"]}
    drops = collections.Counter(r["reason"] for r in screening if r["decision"] == "drop")
    stages = [
        {"label": "retrieved by search", "n": retrieved, "lost": None},
        {"label": "in corpus", "n": in_corpus,
         "lost": "%s repeats of an earlier query, %s comments under 200 characters"
                 % (excl.get("already retrieved under an earlier query", 0),
                    excl.get("comment shorter than 200 characters", 0))},
        {"label": "read individually", "n": read,
         "lost": "%s below the published recall gate" % drops.get("below-recall-gate", 0)},
        {"label": "coded", "n": len(items),
         "lost": "%s read and judged not to be an account of anyone deciding anything"
                 % (drops.get("off-topic", 0) + drops.get("technical-only", 0)
                    + drops.get("no-account", 0) + drops.get("link-only", 0))},
    ]

    return {
        "items": items,
        "codes": codes,
        "stages": stages,
        "threads": len({rows[i["id"]]["thread_id"] for i in items}),
        "corpusThreads": len({r["thread_id"] for r in rows.values()}),
        "years": sorted({i["year"] for i in items}),
    }


def main() -> int:
    data = build()
    page = open(PAGE, encoding="utf-8").read()
    if START not in page or END not in page:
        print("markers %s / %s not found in %s" % (START, END, PAGE), file=sys.stderr)
        return 2

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # </script> inside a string would close the host element early.
    payload = payload.replace("</", "<\\/")
    block = ('%s\n<script id="study-data" type="application/json">%s</script>\n%s'
             % (START, payload, END))
    page = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block,
                  page, flags=re.S)
    open(PAGE, "w", encoding="utf-8").write(page)

    print("%d items, %d codes, %d threads → %s"
          % (len(data["items"]), len(data["codes"]), data["threads"], PAGE))
    for s in data["stages"]:
        print("  %-22s %6s" % (s["label"], format(s["n"], ",")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
