#!/usr/bin/env python3
"""Verify that every quote in FINDINGS.md really is a quote.

    python3 check_quotes.py

This is the check a hostile reader runs first, so it may as well be automated and
run by anyone. For each quoted passage it confirms two things:

  1. the item id it is attributed to exists in the corpus, and
  2. the quoted words actually appear in that item's text.

The second is the one that matters. An id that resolves proves only that a row
exists; it is entirely possible to attach a real id to a sentence nobody wrote,
and tightening a quote until it reads better is an easy thing to do by accident.

Quote format in FINDINGS.md:

    > the quoted text, which may
    > run to several lines
    > — A12 · [44012345](https://news.ycombinator.com/item?id=44012345)

Exit status is non-zero if anything fails to verify.
"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata

CORPUS = "corpus/corpus.csv"
FINDINGS = "FINDINGS.md"

ATTRIBUTION = re.compile(r"^—\s*(\S+)\s*·\s*\[(\d+)\]")


def normal(text: str) -> str:
    """Collapse the differences that survive copying text between documents.

    Markdown editors and forum software disagree about quote marks, dashes and
    line breaks. None of those differences make a quote unfaithful, and treating
    them as failures would train everyone to ignore this script's output.
    """
    text = unicodedata.normalize("NFKD", text)
    text = (text.replace("‘", "'").replace("’", "'")
                .replace("“", '"').replace("”", '"')
                .replace("—", "-").replace("–", "-"))
    return re.sub(r"\s+", " ", text).strip().casefold()


def quotes(markdown: str):
    """Yield (quoted_text, author, item_id) for each attributed block quote."""
    block: list[str] = []
    for line in markdown.splitlines():
        if line.startswith(">"):
            body = line[1:].strip()
            match = ATTRIBUTION.match(body)
            if match:
                yield " ".join(block), match.group(1), match.group(2)
                block = []
            elif body:
                block.append(body)
            continue
        block = []


def main() -> int:
    corpus = {row["item_id"]: row for row in csv.DictReader(open(CORPUS, encoding="utf-8"))}
    markdown = open(FINDINGS, encoding="utf-8").read()

    checked = failed = 0
    for text, author, item_id in quotes(markdown):
        checked += 1
        row = corpus.get(item_id)
        if row is None:
            print("MISSING  %s — no such item in the corpus" % item_id)
            failed += 1
            continue
        if row["author"] != author:
            print("AUTHOR   %s — attributed to %s, corpus says %s"
                  % (item_id, author, row["author"]))
            failed += 1
            continue
        if normal(text) not in normal(row["text"]):
            print("NOT A QUOTE  %s — the quoted words are not in that item" % item_id)
            print("    quoted: %s" % text[:90])
            failed += 1
            continue
        print("ok  %s  %s" % (item_id, text[:60].replace("\n", " ")))

    if not checked:
        print("no attributed quotes found — check the quote format", file=sys.stderr)
        return 2
    print("\n%d/%d quotes verified against the corpus" % (checked - failed, checked))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
