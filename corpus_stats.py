#!/usr/bin/env python3
"""Descriptive counts for the corpus and the coding, printed for the write-up.

    python3 corpus_stats.py

Deliberately limited to counts *about the corpus* — how many items, how many
threads, how they are distributed across codes. None of these are frequencies in
the population, and the write-up must not present them as such: a code applied to
forty items means forty items in this corpus, not that forty per cent of anyone
does anything.
"""
from __future__ import annotations

import collections
import csv
import os

CORPUS = "corpus/corpus.csv"
CODED = "coded.csv"


def main() -> None:
    rows = list(csv.DictReader(open(CORPUS, encoding="utf-8")))
    print("corpus")
    print("  items            %d" % len(rows))
    print("  threads          %d" % len({r["thread_id"] for r in rows}))
    print("  posts            %d" % sum(1 for r in rows if r["kind"] == "post"))
    print("  comments         %d" % sum(1 for r in rows if r["kind"] == "comment"))
    print("  distinct authors %d" % len({r["author"] for r in rows if r["author"]}))
    years = collections.Counter(r["created_utc"][:4] for r in rows if r["created_utc"])
    print("  by year          %s" % ", ".join("%s: %d" % y for y in sorted(years.items())))

    lengths = sorted(len(r["text"]) for r in rows)
    if lengths:
        print("  median length    %d characters" % lengths[len(lengths) // 2])

    if not os.path.exists(CODED):
        print("\nno coded.csv yet")
        return

    coded = list(csv.DictReader(open(CODED, encoding="utf-8")))
    by_code = collections.Counter(c["code"] for c in coded)
    items_coded = {c["item_id"] for c in coded}
    print("\ncoding")
    print("  items with at least one code   %d of %d" % (len(items_coded), len(rows)))
    print("  code applications              %d" % len(coded))
    print("  codes in use                   %d" % len(by_code))
    print("\n  %-34s %5s %7s" % ("code", "items", "threads"))
    item_thread = {r["item_id"]: r["thread_id"] for r in rows}
    for code, n in by_code.most_common():
        threads = {item_thread.get(c["item_id"]) for c in coded if c["code"] == code}
        print("  %-34s %5d %7d" % (code, n, len(threads)))

    # A code carried by one or two loud threads is a property of those threads,
    # not of the corpus. Spread is the honest way to see that, so it is printed
    # next to the count rather than left for someone to work out.
    print("\n  Read the thread column before the item column. A code spread across "
          "\n  many threads is a pattern; one concentrated in a single thread is an "
          "\n  argument that happened once.")


if __name__ == "__main__":
    main()
