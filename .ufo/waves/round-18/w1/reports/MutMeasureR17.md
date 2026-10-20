# MutMeasureR17 — committed-data sensitivity of rubric V

Observed: 2026-10-20T15:44:12Z. Seat: `MadoR18.MutMeasureR17`.

## Result

**No requested guard weakening changes `c2.count` at either assigned revision.** Nine isolated mutants cover all six guard groups (the source eligibility join is also split into its three component checks). All nine survive at both revisions: **0 killed, 18 survived, 0 inconclusive revision/mutant comparisons**.

Every pristine, mutated, and restored execution returns rc 0 with `c2.count = 4`, `c2.score = 6.6667`, covered provinces P1/P2/P4/P6, uncovered P3/P5, no rejected notes, and all seven legacy U routes. Eight mutants produce byte-identical stdout to pristine at each revision. The composite source-eligibility bypass M03d additionally admits S030 into one existing P1 entry's `sources_ok`; it still does **not** change the province count.

This is a coverage finding for the assigned count detector, not evidence that these guards are unnecessary. "Survived committed revisions" below means the two revisions explicitly requested, not an exhaustive scan of repository history. No synthetic corpus, stronger detector, contract change, integration, lane gate, or unrelated runtime was used.

## Axes and detector

- **Sensitivity:** does one guard weakening change the real committed-data `c2.count`?
- **Repeatability:** the same command is run on pristine, mutated, and restored bytes for each mutant/revision pair.
- **Isolation/restoration:** separate scratch script per mutant, committed corpus read from an isolated /tmp clone, exact source-byte restoration, and no lane source modification.

Instrument: `.ufo/waves/round-17/measure.py`, SHA-256 `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc` (11971 bytes). Python: `Python 3.14.8`.

| Revision argument | Resolved committed input | Pristine count |
|---|---|---:|
| `d9a5a18` | `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98` | 4 |
| `f71ccbe` | `f71ccbe525c7d140e50d37af8973ed23329c2729` | 4 |

Scratch clone: `/tmp/mado-r18-mutmeasure-n5eaz8yx/repo`. Created by `git clone --no-hardlinks --no-checkout` from the lane. No git/jj writes occurred in the lane; no jj command was run.

The script's original `REPO = Path(__file__).resolve().parents[3]` is unchanged. Each copy lives at `<scratch clone>/.ufo/waves/<mutant-id>/measure.py`, so every phase reads the clone's pinned commit objects rather than current worktree files.

For every row, the detector command is:

```text
python3 -I /tmp/mado-r18-mutmeasure-n5eaz8yx/repo/.ufo/waves/<mutant-id>/measure.py <revision>
```

Each subprocess has a 30-second deadline and captures stdout/stderr. Independent revision/path runs use a six-worker thread pool; all pristine runs finish before mutation, all mutated runs finish before restoration, and all restored runs finish before recording results. Restoration runs in a `finally` block. The requested detector compares parsed `c2.count` to the successful pristine value of 4: a count change kills the mutant, an unchanged count survives, and an unsuccessful baseline or non-repeatable restoration is inconclusive. The counter itself always exits 0 for a valid measurement; rc is not used as a substitute for count comparison.

There were 54 per-mutant phase executions (9 mutants × 2 revisions × 3 phases), plus two preliminary pristine executions. All 56 completed with rc 0 and empty stderr. No baseline failure, timeout, or parse failure occurred.

## Mutation matrix

Counts are **pristine → mutated → restored**. Every table cell records actual execution, not an inferred result.

| Mutant | Guard | d9a5a18 counts | f71ccbe counts | Count verdict at both |
|---|---|---|---|---|
| `M01-head-window` | Head-lines window | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M02-exact-surface` | Exact surface line | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M03a-status` | Source join: status | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M03b-tier` | Source join: tier | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M03c-used-by` | Source join: used-by | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M03d-any-registered` | Source join: composite eligibility bypass | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M04-upstream-keyword` | Upstream surface keyword | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M05-facet-floor` | Facet non-blank-line floor | 4 → 4 → 4 | 4 → 4 → 4 | survived |
| `M06-unknown-marker` | [UNK] marker inside Unexercised behavior | 4 → 4 → 4 | 4 → 4 → 4 | survived |

### The one non-count output difference

M03d changes `c2.provinces.P1.entries[0].sources_ok` in `corpus/knowledge/hyprland-config-era-r12.md` from S021–S029 to S021–S030. This happens at both revisions. All province booleans, counts, scores, rejected lists, and U-route values remain unchanged. A full-JSON equality detector would distinguish this mutant on these inputs; the assigned **c2-count** detector does not. The status, tier, and used-by omissions tested individually do not change even full stdout.

The other eight guard weakenings change neither `c2` nor any other emitted bytes for the relevant revision. Consequently these two committed corpora do not provide a count-changing negative control for any requested guard weakening. This probe does not establish R17-V5's stronger "shown able to fail" property; it records the gap without relaxing rubric V.

## Exact isolated mutations and hashes

For **every** mutant, the pristine SHA-256 and restored SHA-256 are `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc`. Mutated SHA-256 values below differ from that pristine hash. Diffs use the pristine instrument's line numbers.

### M01-head-window

Remove the `[:HEAD_LINES]` slice; scan the entire note for source, surface, and legacy declarations instead of its first 15 lines.

Mutated SHA-256: `5d9e39f96cd755c388f97d07f54f9ed395bdca56a21a2369d277abd71e89bf08`.

```diff
--- pristine/measure.py
+++ M01-head-window/measure.py
@@ -182,7 +182,7 @@
     if not path.endswith('.md'):
         continue
     text = source(path)
-    head = text.splitlines()[:HEAD_LINES]
+    head = text.splitlines()
 
     src_tokens = set()
     for line in head:
```

### M02-exact-surface

Replace `re.fullmatch` with `re.search` in surface parsing; allow a valid province token followed by extra text.

Mutated SHA-256: `df2e4b1169112c82a0fef8e8781d0a4884cda00bd3f536fdf01546473d927084`.

```diff
--- pristine/measure.py
+++ M02-exact-surface/measure.py
@@ -196,7 +196,7 @@
     for line in head:
         if line.startswith('surface:'):
             # T2: exact single-token form only; anything else is malformed.
-            m = re.fullmatch(r'surface: (P[1-6])', line.rstrip())
+            m = re.search(r'surface: (P[1-6])', line.rstrip())
             surfaces.add(m.group(1) if m else 'MALFORMED')
         if line.startswith('covers:'):
             covers.update(re.findall(r'U[1-7]\b', line))
```

### M03a-status

Omit `row[8] == 'mined'`; retain tier A and the used-by join.

Mutated SHA-256: `f6188f577db68932c4ee451e10d2b8191ad34ab44b7f207604b946cab176acbc`.

```diff
--- pristine/measure.py
+++ M03a-status/measure.py
@@ -128,7 +128,7 @@
 def mined_a(sid, path):
     """Row exists, status mined, tier A, used-by names this entry path."""
     row = registry.get(sid)
-    return (row is not None and row[8] == 'mined' and row[4] == 'A'
+    return (row is not None and row[4] == 'A'
             and used_by(row, path))
 
 
```

### M03b-tier

Omit `row[4] == 'A'`; retain mined status and the used-by join.

Mutated SHA-256: `0913a7513052637f8040be948d615a189bfdcfc7e142b19fbd3eb7671c334271`.

```diff
--- pristine/measure.py
+++ M03b-tier/measure.py
@@ -128,7 +128,7 @@
 def mined_a(sid, path):
     """Row exists, status mined, tier A, used-by names this entry path."""
     row = registry.get(sid)
-    return (row is not None and row[8] == 'mined' and row[4] == 'A'
+    return (row is not None and row[8] == 'mined'
             and used_by(row, path))
 
 
```

### M03c-used-by

Omit the used-by membership check; retain mined status and tier A.

Mutated SHA-256: `99ba4ef621c112ef5c9c6bb17dc48b112a9a9c4cba1f7eccfeef436a60ff6d92`.

```diff
--- pristine/measure.py
+++ M03c-used-by/measure.py
@@ -128,8 +128,7 @@
 def mined_a(sid, path):
     """Row exists, status mined, tier A, used-by names this entry path."""
     row = registry.get(sid)
-    return (row is not None and row[8] == 'mined' and row[4] == 'A'
-            and used_by(row, path))
+    return (row is not None and row[8] == 'mined' and row[4] == 'A')
 
 
 # --- C2 coverage: declared rubric V, provinces P1..P6 -----------------------
```

### M03d-any-registered

Replace the composite eligibility predicate with `row is not None`; any registered cited row becomes eligible. This is an additional whole-predicate bypass, not a stack of the three independently tested mutants.

Mutated SHA-256: `8990fa7086c0d5d9eea76e2288593e68153775d17d0021efc11be45d396848ab`.

```diff
--- pristine/measure.py
+++ M03d-any-registered/measure.py
@@ -128,8 +128,7 @@
 def mined_a(sid, path):
     """Row exists, status mined, tier A, used-by names this entry path."""
     row = registry.get(sid)
-    return (row is not None and row[8] == 'mined' and row[4] == 'A'
-            and used_by(row, path))
+    return row is not None
 
 
 # --- C2 coverage: declared rubric V, provinces P1..P6 -----------------------
```

### M04-upstream-keyword

Remove only the source/scope surface-keyword predicate; retain eligible source rows, docs/spec/code kind, and https.

Mutated SHA-256: `b49a9bc920fb22c8e48712d43d130f72cf715f178f2f81d3ed1d15bf00522318`.

```diff
--- pristine/measure.py
+++ M04-upstream-keyword/measure.py
@@ -253,9 +253,7 @@
         (only_surface,) = tuple(surfaces) if len(surfaces) == 1 else ('',)
         upstream = [s for s in ok_sources
                     if registry[s][3] in ('docs', 'spec', 'code')
-                    and 'https://' in registry[s][2]
-                    and any(k in (registry[s][2] + ' ' + registry[s][5]).lower()
-                            for k in SURFACE_KEYWORDS.get(only_surface, ()))]
+                    and 'https://' in registry[s][2]]
         if not upstream:
             rejected.append({
                 'path': path,
```

### M05-facet-floor

Set `FACET_MIN_LINES` from 3 to 0; required headings and [UNK] remain required.

Mutated SHA-256: `aab0fd4195d6d551290ada155fef17519fa8e08de075fb959f83e9e1a43fb2f9`.

```diff
--- pristine/measure.py
+++ M05-facet-floor/measure.py
@@ -150,7 +150,7 @@
     'P5': ('theme', 'wallpaper', 'hyprpaper', 'swaybg'),
     'P6': ('hypridle', 'hyprlock', 'idle', 'session-lock'),
 }
-FACET_MIN_LINES = 3  # T5: each required section carries content
+FACET_MIN_LINES = 0  # T5: each required section carries content
 REQUIRED_HEADINGS = ('## Upstream contract', '## Host declaration',
                      '## Safe observation', '## Unexercised behavior')
 HEAD_LINES = 15
```

### M06-unknown-marker

Replace the [UNK] token requirement with a non-empty-body check; arbitrary non-empty unexercised text now qualifies.

Mutated SHA-256: `1164f288c3a75384dd692c1f2b5726011e967709035480dd64e1ff7e884eb8d0`.

```diff
--- pristine/measure.py
+++ M06-unknown-marker/measure.py
@@ -224,7 +224,7 @@
                 'reason': 'missing required headings: ' + ', '.join(missing),
             })
             continue
-        if '[UNK]' not in unex:
+        if not unex.strip():
             rejected.append({
                 'path': path,
                 'declared': sorted(surfaces),
```

## Actual output receipts

Outputs are deduplicated by exact stdout bytes, not by count. Each phase row below identifies the actual captured output. All rc values are 0 and all stderr values are the empty string (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). The four complete unique stdout bodies follow the table; each ends with one newline.

| Mutant | Revision | Pristine output | Mutated output | Restored output | Actual rc P/M/R |
|---|---|---|---|---|---|
| `M01-head-window` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M01-head-window` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |
| `M02-exact-surface` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M02-exact-surface` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |
| `M03a-status` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M03a-status` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |
| `M03b-tier` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M03b-tier` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |
| `M03c-used-by` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M03c-used-by` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |
| `M03d-any-registered` | `d9a5a18` | B-D | J-D | B-D | 0/0/0 |
| `M03d-any-registered` | `f71ccbe` | B-F | J-F | B-F | 0/0/0 |
| `M04-upstream-keyword` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M04-upstream-keyword` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |
| `M05-facet-floor` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M05-facet-floor` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |
| `M06-unknown-marker` | `d9a5a18` | B-D | B-D | B-D | 0/0/0 |
| `M06-unknown-marker` | `f71ccbe` | B-F | B-F | B-F | 0/0/0 |

### Output B-D

Exact stdout SHA-256: `b5b5c4d35fd5c3ceee571a481f3282a4b4d5a219a5bbba750adbbb513b233e25`.

```json
{
  "schema": "mado-measure-r17-v1",
  "rev": "d9a5a18",
  "commit": "d9a5a18e17cd3a68b52148fcc01c4a30e340ba98",
  "c1": {
    "criteria": 23,
    "lesson_cited": 15,
    "score": 6.5217
  },
  "c2": {
    "count": 4,
    "score": 6.6667,
    "provinces": {
      "P1": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/hyprland-config-era-r12.md",
            "reason": "legacy covers: U2 -> P1",
            "sources_ok": [
              "S021",
              "S022",
              "S023",
              "S024",
              "S025",
              "S026",
              "S027",
              "S028",
              "S029"
            ]
          },
          {
            "path": "corpus/knowledge/window-rule-effects-getprop.md",
            "reason": "legacy covers: U1 -> P1",
            "sources_ok": [
              "S002",
              "S016",
              "S017",
              "S018",
              "S019",
              "S020"
            ]
          }
        ]
      },
      "P2": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/waybar-observation-boundaries-r16.md",
            "reason": "legacy covers: U7 -> P2",
            "sources_ok": [
              "S053",
              "S054"
            ]
          }
        ]
      },
      "P3": {
        "covered": false,
        "entries": []
      },
      "P4": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/terminal-route-r17.md",
            "reason": "surface: P4",
            "sources_ok": [
              "S056",
              "S057",
              "S058",
              "S059",
              "S060",
              "S071"
            ]
          }
        ]
      },
      "P5": {
        "covered": false,
        "entries": []
      },
      "P6": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/idle-lock-route-r17.md",
            "reason": "surface: P6",
            "sources_ok": [
              "S063",
              "S064",
              "S065",
              "S066",
              "S067",
              "S068",
              "S069"
            ]
          }
        ]
      }
    },
    "rejected": [],
    "u_routes": 7,
    "u_routes_seen": [
      "U1",
      "U2",
      "U3",
      "U4",
      "U5",
      "U6",
      "U7"
    ]
  },
  "c3": {
    "tool_present": true,
    "sha256": "962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072"
  }
}
```

### Output B-F

Exact stdout SHA-256: `ace73300874ea4f77291a50167cad87d180ad402717c952fb9537af815714529`.

```json
{
  "schema": "mado-measure-r17-v1",
  "rev": "f71ccbe",
  "commit": "f71ccbe525c7d140e50d37af8973ed23329c2729",
  "c1": {
    "criteria": 23,
    "lesson_cited": 15,
    "score": 6.5217
  },
  "c2": {
    "count": 4,
    "score": 6.6667,
    "provinces": {
      "P1": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/hyprland-config-era-r12.md",
            "reason": "legacy covers: U2 -> P1",
            "sources_ok": [
              "S021",
              "S022",
              "S023",
              "S024",
              "S025",
              "S026",
              "S027",
              "S028",
              "S029"
            ]
          },
          {
            "path": "corpus/knowledge/window-rule-effects-getprop.md",
            "reason": "legacy covers: U1 -> P1",
            "sources_ok": [
              "S002",
              "S016",
              "S017",
              "S018",
              "S019",
              "S020"
            ]
          }
        ]
      },
      "P2": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/waybar-observation-boundaries-r16.md",
            "reason": "legacy covers: U7 -> P2",
            "sources_ok": [
              "S053",
              "S054"
            ]
          }
        ]
      },
      "P3": {
        "covered": false,
        "entries": []
      },
      "P4": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/terminal-route-r17.md",
            "reason": "surface: P4",
            "sources_ok": [
              "S056",
              "S057",
              "S058",
              "S059",
              "S060",
              "S071"
            ]
          }
        ]
      },
      "P5": {
        "covered": false,
        "entries": []
      },
      "P6": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/idle-lock-route-r17.md",
            "reason": "surface: P6",
            "sources_ok": [
              "S063",
              "S064",
              "S065",
              "S066",
              "S067",
              "S068",
              "S069"
            ]
          }
        ]
      }
    },
    "rejected": [],
    "u_routes": 7,
    "u_routes_seen": [
      "U1",
      "U2",
      "U3",
      "U4",
      "U5",
      "U6",
      "U7"
    ]
  },
  "c3": {
    "tool_present": true,
    "sha256": "7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7"
  }
}
```

### Output J-D

Exact stdout SHA-256: `ca077a66bae5c0a3cd2a049b0bed25c4f712e9ea98bae4f1bb6cae9ac8167976`.

```json
{
  "schema": "mado-measure-r17-v1",
  "rev": "d9a5a18",
  "commit": "d9a5a18e17cd3a68b52148fcc01c4a30e340ba98",
  "c1": {
    "criteria": 23,
    "lesson_cited": 15,
    "score": 6.5217
  },
  "c2": {
    "count": 4,
    "score": 6.6667,
    "provinces": {
      "P1": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/hyprland-config-era-r12.md",
            "reason": "legacy covers: U2 -> P1",
            "sources_ok": [
              "S021",
              "S022",
              "S023",
              "S024",
              "S025",
              "S026",
              "S027",
              "S028",
              "S029",
              "S030"
            ]
          },
          {
            "path": "corpus/knowledge/window-rule-effects-getprop.md",
            "reason": "legacy covers: U1 -> P1",
            "sources_ok": [
              "S002",
              "S016",
              "S017",
              "S018",
              "S019",
              "S020"
            ]
          }
        ]
      },
      "P2": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/waybar-observation-boundaries-r16.md",
            "reason": "legacy covers: U7 -> P2",
            "sources_ok": [
              "S053",
              "S054"
            ]
          }
        ]
      },
      "P3": {
        "covered": false,
        "entries": []
      },
      "P4": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/terminal-route-r17.md",
            "reason": "surface: P4",
            "sources_ok": [
              "S056",
              "S057",
              "S058",
              "S059",
              "S060",
              "S071"
            ]
          }
        ]
      },
      "P5": {
        "covered": false,
        "entries": []
      },
      "P6": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/idle-lock-route-r17.md",
            "reason": "surface: P6",
            "sources_ok": [
              "S063",
              "S064",
              "S065",
              "S066",
              "S067",
              "S068",
              "S069"
            ]
          }
        ]
      }
    },
    "rejected": [],
    "u_routes": 7,
    "u_routes_seen": [
      "U1",
      "U2",
      "U3",
      "U4",
      "U5",
      "U6",
      "U7"
    ]
  },
  "c3": {
    "tool_present": true,
    "sha256": "962919cec38ab81de0dea109c25e5ec610b53f5b2142b79c5cb9eed7d5aaa072"
  }
}
```

### Output J-F

Exact stdout SHA-256: `d5a2868f382fa70f5e13e41e9e4b1c7c845905fbe5102f68d0b4720da2bae0bf`.

```json
{
  "schema": "mado-measure-r17-v1",
  "rev": "f71ccbe",
  "commit": "f71ccbe525c7d140e50d37af8973ed23329c2729",
  "c1": {
    "criteria": 23,
    "lesson_cited": 15,
    "score": 6.5217
  },
  "c2": {
    "count": 4,
    "score": 6.6667,
    "provinces": {
      "P1": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/hyprland-config-era-r12.md",
            "reason": "legacy covers: U2 -> P1",
            "sources_ok": [
              "S021",
              "S022",
              "S023",
              "S024",
              "S025",
              "S026",
              "S027",
              "S028",
              "S029",
              "S030"
            ]
          },
          {
            "path": "corpus/knowledge/window-rule-effects-getprop.md",
            "reason": "legacy covers: U1 -> P1",
            "sources_ok": [
              "S002",
              "S016",
              "S017",
              "S018",
              "S019",
              "S020"
            ]
          }
        ]
      },
      "P2": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/waybar-observation-boundaries-r16.md",
            "reason": "legacy covers: U7 -> P2",
            "sources_ok": [
              "S053",
              "S054"
            ]
          }
        ]
      },
      "P3": {
        "covered": false,
        "entries": []
      },
      "P4": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/terminal-route-r17.md",
            "reason": "surface: P4",
            "sources_ok": [
              "S056",
              "S057",
              "S058",
              "S059",
              "S060",
              "S071"
            ]
          }
        ]
      },
      "P5": {
        "covered": false,
        "entries": []
      },
      "P6": {
        "covered": true,
        "entries": [
          {
            "path": "corpus/knowledge/idle-lock-route-r17.md",
            "reason": "surface: P6",
            "sources_ok": [
              "S063",
              "S064",
              "S065",
              "S066",
              "S067",
              "S068",
              "S069"
            ]
          }
        ]
      }
    },
    "rejected": [],
    "u_routes": 7,
    "u_routes_seen": [
      "U1",
      "U2",
      "U3",
      "U4",
      "U5",
      "U6",
      "U7"
    ]
  },
  "c3": {
    "tool_present": true,
    "sha256": "7a98720ed3c0ea1676714381a9289a65dd2a416f98b764e2b52517f81ef31fe7"
  }
}
```

## Restoration and scope

After all mutations, `sha256sum` reported `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc` for **all eleven** files: the original lane instrument, the untouched preliminary scratch copy at `.ufo/waves/round-17/measure.py`, and all nine mutant paths. Each restored detector stdout equals its own pristine stdout byte-for-byte at both revisions. Every mutated scratch file was restored to the exact pristine bytes; no mutant is left active.

The only lane file written by this seat is this report. The scratch clone and restored copies remain under the isolated /tmp path named above. No production tool, corpus note, registry row, rubric, lesson, or sibling source was edited. No web fetch, host/package/service/compositor command, credential read, transcript read, or tool installation/update was performed. No lane build, test suite, or gate was invoked.

**Scope conclusion:** all six requested guard groups survive the assigned real-commit count detector, including three individual source-join checks and the whole-predicate bypass. The composite bypass's metadata difference is preserved in the receipts rather than mislabeled as a count kill.
