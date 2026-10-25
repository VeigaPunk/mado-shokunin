# MutC2Drop — round-34 C2 counter clause-drop mutation probe

Date: 2026-10-24. Seat: mado leaf (w1). Scope: mutation testing of
`.ufo/waves/round-34/c2/count.py` (`PRED-C2-r34-v1`) against its committed
control cards. Mutants live only in
`.ufo/waves/round-34/scratch/MutC2Drop/` (`count.py` pristine copy + `m1.py`–`m4.py`);
the lane counter was never modified.

## Setup

Baseline (`count.py` unmodified), all runs with
`--repo /home/vgpnk/Projects/shokunin/mado-shokunin --frozen .ufo/waves/round-34/c2/frozen.json`:

| Card | Marker lines | Expected | Observed |
|---|---|---|---|
| `SCORECARD.md` | 1 (`:2108` = `line=169`) | MET | `published=169 measured=169 mismatch=0 verdict=TARGET_MET` rc=0 |
| `controls/c2-reachable-card.md` | 1 (`:2108` = `line=169`) | MET | `published=169 measured=169 mismatch=0 verdict=TARGET_MET` rc=0 |
| `controls/c2-junk-card.md` | 1 (`:1` = `line=128`) | MISSED | `published=128 measured=169 mismatch=1 verdict=TARGET_MISSED` rc=1 |

Fetch ground truth (`.ufo/waves/round-32/fetch/S189.bin`, sha256
`eea605dfe5ce09e1f92a67ec478bf61a19894c6e0ee3302c0393521a2ee9540d` — matches pin):

```text
line 128: "    auto             eventString = std::format(\"{}>>{}\\n\", event.event, data.substr(0, 1024));"
line 169: "    const size_t MAX_QUEUED_EVENTS = 64;"   ← leading 4-space indent
```

The quote at line 169 is **indented**; `.strip()` is load-bearing.

## Mutant diffs

### M1 — drop the `line 128 does not` clause

```diff
--- count.py
+++ m1.py
@@ -127,14 +127,11 @@
     blob = read_regular(repo, PINNED_REL)
     digest = hashlib.sha256(blob).hexdigest() if blob is not None else ""
     measured = "absent"
-    line128_is_quote = False
     if blob is not None and digest == PINNED_SHA:
         lines = blob.decode("utf-8", "replace").splitlines()
         if len(lines) >= 169 and lines[168].strip() == QUOTE:
             measured = "169"
-        if len(lines) >= 128 and lines[127].strip() == QUOTE:
-            line128_is_quote = True
-    mismatch = 0 if published == "169" and measured == "169" and not line128_is_quote else 1
+    mismatch = 0 if published == "169" and measured == "169" else 1
```

### M2 — drop the sha256 pin

```diff
--- count.py
+++ m2.py
@@ -125,10 +125,10 @@
             card = card_path.read_text(errors="replace")
             published = published_line(card)
     blob = read_regular(repo, PINNED_REL)
-    digest = hashlib.sha256(blob).hexdigest() if blob is not None else ""
+    digest = ""
     measured = "absent"
     line128_is_quote = False
-    if blob is not None and digest == PINNED_SHA:
+    if blob is not None:
```

### M3 — drop the `last matching line` rule (first match wins)

```diff
--- count.py
+++ m3.py
@@ -79,6 +79,7 @@
     for line in text.splitlines():
         if MARKER in line:
             last = line
+            break
     if not last:
         return "absent"
```

### M4 — drop the strip-equals comparison (exact-match both lines)

```diff
--- count.py
+++ m4.py
@@ -130,9 +130,9 @@
     line128_is_quote = False
     if blob is not None and digest == PINNED_SHA:
         lines = blob.decode("utf-8", "replace").splitlines()
-        if len(lines) >= 169 and lines[168].strip() == QUOTE:
+        if len(lines) >= 169 and lines[168] == QUOTE:
             measured = "169"
-        if len(lines) >= 128 and lines[127].strip() == QUOTE:
+        if len(lines) >= 128 and lines[127] == QUOTE:
             line128_is_quote = True
```

## Results — verbatim outputs

### M1

```text
=== m1 vs SCORECARD.md
PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
rc=0
=== m1 vs .ufo/waves/round-34/controls/c2-reachable-card.md
PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
rc=0
=== m1 vs .ufo/waves/round-34/controls/c2-junk-card.md
PRED-C2-r34-v1 published=128 measured=169 mismatch=1 verdict=TARGET_MISSED
rc=1
```

### M2

```text
=== m2 vs SCORECARD.md
PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
rc=0
=== m2 vs .ufo/waves/round-34/controls/c2-reachable-card.md
PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
rc=0
=== m2 vs .ufo/waves/round-34/controls/c2-junk-card.md
PRED-C2-r34-v1 published=128 measured=169 mismatch=1 verdict=TARGET_MISSED
rc=1
```

### M3

```text
=== m3 vs SCORECARD.md
PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
rc=0
=== m3 vs .ufo/waves/round-34/controls/c2-reachable-card.md
PRED-C2-r34-v1 published=169 measured=169 mismatch=0 verdict=TARGET_MET
rc=0
=== m3 vs .ufo/waves/round-34/controls/c2-junk-card.md
PRED-C2-r34-v1 published=128 measured=169 mismatch=1 verdict=TARGET_MISSED
rc=1
```

### M4

```text
=== m4 vs SCORECARD.md
PRED-C2-r34-v1 published=169 measured=absent mismatch=1 verdict=TARGET_MISSED
rc=1
=== m4 vs .ufo/waves/round-34/controls/c2-reachable-card.md
PRED-C2-r34-v1 published=169 measured=absent mismatch=1 verdict=TARGET_MISSED
rc=1
=== m4 vs .ufo/waves/round-34/controls/c2-junk-card.md
PRED-C2-r34-v1 published=128 measured=absent mismatch=1 verdict=TARGET_MISSED
rc=1
```

## Verdicts

| Mutant | Clause dropped | Result |
|---|---|---|
| M1 | `line 128 does not` | **SURVIVED** — no fixture exercises a fetch whose line 128 is the quote |
| M2 | sha256 pin | **SURVIVED** — committed fetch is immutable to the probe; no drifted-fetch fixture |
| M3 | `last matching line` | **SURVIVED** — every fixture card carries exactly one marker line; first-vs-last indistinguishable |
| M4 | strip-equals | **KILLED** — wrongly `TARGET_MISSED` on both must-MET cards (`measured=absent`; line 169 is indented, strip is load-bearing) |

**Mutants that wrongly MET a card that must miss: none.** The junk card
stayed `TARGET_MISSED` under all four mutants.

## Fixture gaps named

The three survivors expose control-card blind spots, each killable with a
committed fixture:

- **M1** — needs a must-miss case where the fetched content has the quote at
  line 128 while publishing `line=169`. Impossible against the single pinned
  fetch; would need a second fetch fixture or a fetch-side control.
- **M2** — needs a fetch whose bytes differ from `PINNED_SHA` but still put
  the quote at 169 (card publishes 169 → must MISS). Same fixture limitation.
- **M3** — needs a multi-marker card, e.g. `r34-s189-line: line=128` followed
  later by `r34-s189-line: line=169` (baseline: last wins → MET; mutant:
  first wins → MISSED). One line of new control card kills it.
