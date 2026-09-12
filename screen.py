#!/usr/bin/env python3
"""Apply and audit the relevance screen.

    python3 screen.py report      # what the screen kept and dropped, by reason
    python3 screen.py kept        # the screened corpus, as CSV on stdout

The screen decides which retrieved items are *about the phenomenon* — someone
giving an account of proceeding past a security warning — rather than merely
containing the words. `screening.csv` holds one row per retrieved item with the
decision and the reason, and is committed, so the screen can be argued with
instead of taken on trust.

Why it is not a keyword rule: that was tried first. A phrase screen is precise
about words and blind to meaning. It kept link posts titled "Preventing Alert
Fatigue" with no body text, and protocol arguments about certificate pinning,
while missing every account written in wording the list did not anticipate. The
result of that attempt is kept in `corpus-lexical-screen/` so the failure is
inspectable rather than asserted.
"""
from __future__ import annotations

import collections
import csv
import sys

CORPUS = "corpus/corpus.csv"
SCREENING = "screening.csv"

KEEP = "keep"

# The reasons an item is dropped. Fixed set, so the screen cannot quietly grow a
# new rationale per awkward item.
REASONS = {
    "below-recall-gate": "did not contain any term on the published recall list, "
                         "so was never read individually",
    "off-topic": "not about security warnings at all",
    "technical-only": "discusses certificates or alerts as a technical subject, "
                      "with no account of a person deciding anything",
    "no-account": "mentions warnings but gives no reasoning, experience or stance",
    "link-only": "a post with no body text, or only a link",
}

# A keep that the recall gate had excluded. Recorded rather than quietly
# promoted, because each one is a measured false negative in the gate.
OUTSIDE_GATE = "kept-though-below-gate"


def load():
    corpus = {r["item_id"]: r for r in csv.DictReader(open(CORPUS, encoding="utf-8"))}
    screening = list(csv.DictReader(open(SCREENING, encoding="utf-8")))
    return corpus, screening


def report() -> int:
    corpus, screening = load()
    decisions = collections.Counter(r["decision"] for r in screening)
    reasons = collections.Counter(r["reason"] for r in screening if r["decision"] != KEEP)

    missing = set(corpus) - {r["item_id"] for r in screening}
    extra = {r["item_id"] for r in screening} - set(corpus)

    print("screened   %d of %d retrieved items" % (len(screening), len(corpus)))
    print("kept       %d" % decisions[KEEP])
    print("dropped    %d\n" % (len(screening) - decisions[KEEP]))
    for reason, n in reasons.most_common():
        print("  %-20s %4d   %s" % (reason, n, REASONS.get(reason, "?")))

    escaped = sum(1 for r in screening
                  if r["decision"] == KEEP and r["reason"] == OUTSIDE_GATE)
    if escaped:
        print("\n%d kept item(s) had failed the recall gate. Each is a measured "
              "false negative\nin the gate, and the true rate is unknown because "
              "un-gated items were not read." % escaped)

    bad = sorted(set(reasons) - set(REASONS))
    problems = 0
    if missing:
        print("\nUNSCREENED: %d items were retrieved but never judged" % len(missing))
        problems += 1
    if extra:
        print("\nPHANTOM: %d screened ids are not in the corpus" % len(extra))
        problems += 1
    if bad:
        print("\nUNDECLARED REASONS: %s" % ", ".join(bad))
        problems += 1
    if not problems:
        print("\nEvery retrieved item has a decision, and every reason is declared.")
    return 1 if problems else 0


def kept() -> int:
    corpus, screening = load()
    writer = csv.DictWriter(sys.stdout, fieldnames=list(next(iter(corpus.values()))))
    writer.writeheader()
    for row in screening:
        if row["decision"] == KEEP and row["item_id"] in corpus:
            writer.writerow(corpus[row["item_id"]])
    return 0


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "report"
    sys.exit({"report": report, "kept": kept}.get(command, report)())
