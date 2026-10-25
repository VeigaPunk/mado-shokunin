# LabratClockSkew — c1-r38 clause-k date/recheck parsing: does it accept malformed dates?

**Role:** leaf labrat (wave 1, round 38). Scope: the `verified-at` DATE_RE and the
`recheck` RECHECK_RE of `quality/counters/c1-r38-event-ground.py` (PRED-C1-r38-v3),
plus the identical pair in `quality/counters/c2-r38-request-ground.py`.
**Read-only on every lane production file.** All probes ran in `/tmp/mado38-LabratClockSkew/`.
**Verdict: the DATE_RE accepts malformed (non-calendar) dates and the frozen 19-control
discrimination manifest cannot detect that.**

---

## 1. The two regexes under attack (exact, quoted)

`quality/counters/c1-r38-event-ground.py:103-104`:

```python
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)$")
```

Byte-identical pair in `quality/counters/c2-r38-request-ground.py:100-101`.

Consumption site, `c1-r38-event-ground.py:208-213` (clause k):

```python
        # k: header values actually parse
        ver = [l.split(":", 1)[1].strip() for l in head if re.match(r"^[-* ]*verified-at *:", l)]
        rec = [l.split(":", 1)[1].strip() for l in head if re.match(r"^[-* ]*recheck *:", l)]
        c["k"] = int(bool(ver) and bool(rec)
                     and all(DATE_RE.match(v.split()[0] if v.split() else "") for v in ver)
                     and all(RECHECK_RE.match(r.split()[0] if r.split() else "") for r in rec))
```

Two facts about the consumption site that matter for the probe:

1. `DATE_RE`/`RECHECK_RE` are **shape** matchers, not calendar matchers. `\d{2}` matches
   `00` and `13`; there is no range check on month or day and no `datetime` call anywhere
   in the lane's `quality/` tree for corpus entries (grep for `strptime|fromisoformat`
   returns only `tools/mado-assessment.py:79` and `quality/check-control-receipts.py:178`,
   neither of which reads corpus `verified-at:` values).
2. Only `v.split()[0]` — the **first whitespace token** — is tested. Anything appended after
   the token is not inspected, so `verified-at: 2026-13-45 whatever` passes unchanged.

---

## 2. Unit-level probe (exact strings, exact verdicts)

Command (sandbox, lane untouched):

```
python3 - <<'EOF'
import re
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|on-[a-z-]+)$")
...
EOF
```

### 2.1 DATE_RE — which strings pass

```
'2026-10-25' -> MATCH
'2026-13-45' -> MATCH      <-- month 13
'0000-00-00' -> MATCH      <-- year 0, month 0, day 0
'2026-00-01' -> MATCH
'2026-01-00' -> MATCH
'2026-02-30' -> MATCH      <-- Feb 30
'9999-99-99' -> MATCH
'2026-1-1' -> no
'26-10-25' -> no
'2026-10-25T00:00:00' -> no
'2026-10-250' -> no
'abcd-ef-gh' -> no
'2026-10-25 ' -> no
'' -> no
'2026-13-45x' -> no
```

The same strings against the stdlib ground truth:

```
2026-13-45 -> INVALID calendar date: month must be in 1..12, not 13
0000-00-00 -> INVALID calendar date: year must be in 1..9999, not 0
2026-02-30 -> INVALID calendar date: day 30 must be in range 1..28 for month 2 in year 2026
9999-99-99 -> INVALID calendar date: month must be in 1..12, not 99
2026-10-25 -> real calendar date
```

**Result: the DATE_RE accepts every non-calendar date of the requested shape.** The regex
answers "does this have the glyph pattern of a date", never "is this a date".

### 2.2 RECHECK_RE — which strings pass

```
'on-release' -> MATCH      <-- requested: PASSES
'90d' -> MATCH            <-- requested: PASSES
'on-change' -> MATCH      <-- requested: PASSES
'whenever' -> no          <-- requested: REJECTED
'on-' -> no
'on-Whatever' -> no
'90D' -> no
'1d' -> MATCH
'0d' -> MATCH
'-5d' -> no
'90' -> no
'on' -> no
'release' -> no
'on-every-release' -> MATCH
'2026-13-45' -> MATCH     (a malformed date also satisfies RECHECK_RE's date branch)
'every-90d' -> no
'90 days' -> no
'on_ change' -> no
'whenever-change' -> no
```

**Result: `on-release`, `90d`, `on-change` pass; `whenever` fails.** The `on-[a-z-]+`
branch is a literal prefix test, so `on-` + any lowercase-hyphen word passes —
`on-every-release` is as acceptable as `on-change`, and `on-foo` would be too. `whenever`
fails only because it lacks the `on-` prefix; the counter's docstring
(`c1-r38-event-ground.py:20-22`, clause k: "`recheck:` carries an ISO date, an `NNd`
count, or a `on-*` cadence") does not claim `whenever`, so its rejection is by-design, not
a defect. `0d` passing is already recorded by the lane (LOG.md, RevC1v3 F4: "`RECHECK_RE`
accepts `0d`").

---

## 3. End-to-end probe on the real lane entries (C1, in a sandbox clone)

Sandbox: `git clone -q --no-local <lane> /tmp/mado38-LabratClockSkew/sb`. Each variant
rewrites the `verified-at:`/`recheck:` header of
`corpus/knowledge/event-delivery-limits-r26.md`, commits, and rescores with the **real**
counter at the **real** base `b4e47e980bfb0cbc8a4e788f59a41db858751fd8`:

```
python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev HEAD --base b4e47e98...
```

| variant | clause k | verdict |
|---|---|---|
| `verified-at: 2026-10-25` / `recheck: 90d` (baseline) | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2026-13-45` / `recheck: 90d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 0000-00-00` / `recheck: 90d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2026-02-30` / `recheck: 90d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 9999-99-99` / `recheck: 90d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2099-12-31` / `recheck: 90d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 1999-01-01` / `recheck: 90d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2026-10-25` / `recheck: on-release` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2026-10-25` / `recheck: 90d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2026-10-25` / `recheck: on-change` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2026-10-25` / `recheck: whenever` | `k=0` | `admitted=1/2 verdict=TARGET_MISSED` |
| `verified-at: 2026-10-25` / `recheck: 0d` | `k=1` | `admitted=2/2 verdict=TARGET_MET` |
| `verified-at: 2026-10-25` / `recheck: x` (the v2 crib) | `k=0` | `admitted=1/2 verdict=TARGET_MISSED` |

Verbatim baseline line, for the record:

```
PRED-C1-r38-v3 admitted=2/2 verdict=TARGET_MET rev=b6c1d3124555d7d4c38bc467d85d5efa4a65c053 base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
```

**Result: malformed dates, year-0 dates, far-future dates and far-past dates all leave
the C1 counter at `admitted=2/2 verdict=TARGET_MET`.** `whenever` is the only one of the
four requested `recheck` strings that is rejected.

---

## 4. The requested crafted sandbox: a fake date at base `b4e47e9` with a crafted Gate/row

The ask was to construct a sandbox entry carrying a fake date at base `b4e47e9` and score
it with the real counter plus a crafted Gate line and registry row. Done, and it is the
sharpest result of this probe.

**Construction** (all in `/tmp/mado38-LabratClockSkew/sb2`, a clone checked out at the base
`b4e47e980bfb0cbc8a4e788f59a41db858751fd8`):

- The eight pinned receipt bytes were copied into the tree at their pinned paths
  `.ufo/waves/round-37/fetch/…` (digest check confirmed: all eight `sha_match=True`).
- `corpus/lessons/round-37.md` was **written from scratch** with a `## Gate` section whose
  `GATE` lines were crafted against the counter's own `PINS` table — path and sha256 taken
  from `c1-r38-event-ground.py:74-89`, quotes drawn from the real receipt bytes and
  filtered through the counter's own `quote_floor_ok` (≥3 words or ≥24 chars, not a bare
  token).
- `corpus/SOURCES.md` got crafted 11-cell `## Registry` rows (`mined` in cell 7, the entry
  path in cell 10) for the ids the crafted entries cite, with the base rows for `S189`
  and `S201` re-used-by-amended rather than duplicated (so clause j stays satisfied).
- `corpus/README.md` got two crafted `## Coverage map` rows naming the two entries.
- The two target entries were written with **fake dates** and **real Gate quotes**:
  `corpus/knowledge/event-delivery-limits-r26.md` → `verified-at: 2026-13-45`,
  `recheck: on-release`; `corpus/knowledge/event-queue-observability-r37.md` →
  `verified-at: 0000-00-00`, `recheck: 90d`.

**Score with the real counter:**

```
$ cd /tmp/mado38-LabratClockSkew/sb2 && python3 -I <lane>/quality/counters/c1-r38-event-ground.py --repo . --rev HEAD --base b4e47e980bfb0cbc8a4e788f59a41db858751fd8
PRED-C1-r38-v3 entry=corpus/knowledge/event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S189,S201,S212 lineage=7/4 ok=1
PRED-C1-r38-v3 entry=corpus/knowledge/event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 h=1 j=1 k=1 l=1 ids=S213,S214,S215,S216,S217 lineage=3/2 ok=1
PRED-C1-r38-v3 admitted=2/2 verdict=TARGET_MET rev=5436332690f8a9cb88cc0c902617d073638511ae base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
EXIT=0
```

Headers at the scored revision:

```
corpus/knowledge/event-delivery-limits-r26.md:4:verified-at: 2026-13-45
corpus/knowledge/event-delivery-limits-r26.md:5:recheck: on-release
corpus/knowledge/event-queue-observability-r37.md:4:verified-at: 0000-00-00
corpus/knowledge/event-queue-observability-r37.md:5:recheck: 90d
```

**FAIL (as a calibration instrument): a corpus whose two verification dates are
`2026-13-45` and `0000-00-00` — neither a real date — is admitted `2/2 TARGET_MET`, exit 0,
by the real counter with a crafted Gate section and crafted registry rows.**
Clause k is green (`k=1`) on both entries: the counter asserts the entries were verified on
a date that does not exist.

Note the base precondition held for this construction: `git grep -l -e MAX_QUEUED_EVENTS
-e "overflowed event queue" -e "debug:disable_logs" -e m_logsEnabled <base> -- corpus/knowledge/`
returned exit 1 (no hits), so the counter's `ground_held_at_base` setup guard did not fire.

---

## 5. The same defect in the C2 domain counter

`c2-r38-request-ground.py:100-101` carries the identical pair; its clause b
(lines 196-200) consumes them the same way. Probe (sandbox clone of the lane at HEAD):

| variant (on `corpus/knowledge/hyprctl-flags-r28.md`) | verdict |
|---|---|
| `verified-at: 2026-13-45` (all three C2 entries) | `admitted=3/3 verdict=TARGET_MET` |
| `verified-at: 2099-12-31` | `admitted=3/3 verdict=TARGET_MET` |
| `verified-at: 1999-01-01` | `admitted=3/3 verdict=TARGET_MET` |
| `verified-at: 2026-13-45 whatever` | `admitted=3/3 verdict=TARGET_MET` |
| `verified-at: 0000-00-00` | `admitted=3/3 verdict=TARGET_MET` |
| `recheck: 0d` | `admitted=3/3 verdict=TARGET_MET` |

```
PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=da77852346dd8776dd994ff4862dbf878a119bc5 base=f6e3247f73152a39afb86066af48f3cedf95fb0a
```

**FAIL, same shape: the coverage-claim counter admits a corpus whose verification dates
are non-calendar.** The `c2-r38-eventq.py` counter has no date clause at all
(grep for `DATE_RE|RECHECK|verified-at|recheck` in it returns nothing), so it is unaffected.

---

## 6. The frozen 19-control manifest cannot see this

This is the finding that makes the defect live rather than theoretical: the round-38
discrimination gate is the artifact that certifies "19/19 discriminating", and it has no
control that exercises clause k's *value* parsing.

Mutation test, run with the lane's own gate and the lane's own frozen manifest, using a
**copy** of the counter in `/tmp` (the lane counter is never edited):

```
# /tmp/mado38-LabratClockSkew/mut-date.py  (copy of the lane counter)
DATE_RE = re.compile(r"^.*$")  # MUTANT: accepts any string as a date

$ python3 -I quality/check-r38-discrimination.py --c1 /tmp/mado38-LabratClockSkew/mut-date.py \
    --c2 quality/counters/c2-r38-eventq.py --manifest .ufo/waves/round-38/controls/manifest.json \
    --rev master --sandbox-root /tmp/mado38-LabratClockSkew/dsc
...
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
EXIT=0
```

A counter that accepts **any** string as a date still scores **19/19**. The gate is blind
to the date clause.

The gate is not vacuous in general — a counter that rejects every real date is caught:

```
# /tmp/mado38-LabratClockSkew/mut-neg.py
DATE_RE = re.compile(r"^(?!x)x$")  # MUTANT: rejects every real date
...
control=c1-live instrument=c1 expected=TARGET_MET observed=TARGET_MISSED ok=0
MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED
EXIT=1
```

So the manifest constrains the date clause from **above** (a date must parse) but not from
**below** (the date must be a real calendar date, or must not be fabricated). The manifest's
only date-adjacent control is `c1-clause-b`, which **deletes** the `verified-at:` line
entirely — the absence case, which is not the hole.

Unmutated baseline for comparison (lane instruments, frozen manifest):

```
MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET
EXIT=0
```

---

## 7. Findings

| # | item | verdict | evidence |
|---|---|---|---|
| F1 | `DATE_RE` accepts malformed dates (`2026-13-45`, `0000-00-00`, `2026-02-30`, `9999-99-99`) | **FAIL** | §2.1, §3, §4 — `k=1`, `admitted=2/2 TARGET_MET` |
| F2 | Crafted sandbox at base `b4e47e9` with fake dates + crafted Gate/row is admitted 2/2 by the real counter | **FAIL** | §4 — `rev=5436332…`, `admitted=2/2 verdict=TARGET_MET`, exit 0 |
| F3 | The frozen 19-control manifest cannot detect a relaxed date regex (`^.*$` → 19/19) | **FAIL** | §6 — `correct=19/19 verdict=TARGET_MET` |
| F4 | Same `DATE_RE`/`RECHECK_RE` defect in `c2-r38-request-ground.py`; malformed date → `admitted=3/3` | **FAIL** | §5 |
| F5 | `RECHECK_RE` accepts `on-release`, `90d`, `on-change`; rejects `whenever` | **PASS (by design)** | §2.2, §3 — `whenever` → `k=0`, `TARGET_MISSED`; the docstring claims only ISO date / `NNd` / `on-*` |
| F6 | `RECHECK_RE` accepts `0d` (a zero-day recheck) | **FAIL (already known)** | §3 — `k=1`, `TARGET_MET`; already in `LOG.md` as RevC1v3 F4 |
| F7 | `on-[a-z-]+` is a prefix test, so any `on-<lowercase>` word passes (e.g. `on-every-release`, `on-foo`) | **PASS (documented shape)** | §2.2 — the clause only promises `on-*` |
| F8 | Only the first whitespace token of the header value is tested (`verified-at: 2026-13-45 whatever` passes) | **PASS (shape)** | §2.1, §5 — `v.split()[0]` at line 212 |
| F9 | No mitigating date validation anywhere in the lane's `quality/` tree | **confirmed** | grep `strptime\|fromisoformat` → only `tools/mado-assessment.py:79`, `quality/check-control-receipts.py:178`, neither reads corpus `verified-at:` |

**Scope note.** This is a *shape-vs-semantics* defect in the header-value clause, not a
break of the pin/digest binding (clauses d/h) or the lineage floor (clause l) — those held
in every probe. It is the same accept-path tradeoff the frozen registration already
declares as a residual ("fully fabricated self-consistent artifacts still pass"), but the
date clause is the one place where the counter's own docstring promises more than it
delivers: it says "`verified-at:` carries a YYYY-MM-DD date" and "an ISO date", which a
reader takes to mean a real date, while the implementation checks only glyph shape.

**Suggested repair (not applied — the lane is read-only for this seat, and round 38 is
frozen; route to round 39):** parse the date with `datetime.date.fromisoformat` (or
`re` + explicit month/day ranges) instead of a shape regex, bound it to the round's
window if the corpus's `verified-at` semantics require that, and add a manifest control
that scores a `verified-at: 2026-13-45` entry as `TARGET_MISSED` under clause `k` — the
manifest currently has no clause-k value control, which is why F3 holds.

---

## 8. Reproduction commands (all lane-read-only)

```bash
# 0. sandbox (never the lane)
mkdir -p /tmp/mado38-LabratClockSkew
git clone -q --no-local /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado38-LabratClockSkew/sb

# 1. real counter at the real base
cd /tmp/mado38-LabratClockSkew/sb
python3 -I quality/counters/c1-r38-event-ground.py --repo . --rev HEAD \
  --base b4e47e980bfb0cbc8a4e788f59a41db858751fd8

# 2. malformed-date variant on the real entries (see §3 loop)
#    rewrite the verified-at header, commit, rescore

# 3. manifest blindness (counter copy in /tmp; lane counter never edited)
cp <lane>/quality/counters/c1-r38-event-ground.py /tmp/mado38-LabratClockSkew/mut-date.py
#    edit DATE_RE -> re.compile(r"^.*$")
cd <lane>
python3 -I quality/check-r38-discrimination.py \
  --c1 /tmp/mado38-LabratClockSkew/mut-date.py \
  --c2 quality/counters/c2-r38-eventq.py \
  --manifest .ufo/waves/round-38/controls/manifest.json --rev master \
  --sandbox-root /tmp/mado38-LabratClockSkew/dsc
```

**Tools installed:** none. No `pacman`, `uv tool`, `npm -g`, or `cargo install` was
needed; every probe used the system `python3` (3.14) and `git` already present.
**Lane mutation:** none. All commits were made in `/tmp/mado38-LabratClockSkew/sb{,2,3}`
with `git -c user.name=s -c user.email=s@i commit`; `git status --short` in the lane shows
only peer-written report files under `.ufo/waves/round-38/w1/reports/`.
