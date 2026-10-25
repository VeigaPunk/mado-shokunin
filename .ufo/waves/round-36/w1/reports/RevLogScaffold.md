# RevLogScaffold — exact `## Round 36` heading and citation form the pointer gate requires

Seat: reviewer, round 36 wave 1. Scope: last three `LOG.md` round entries (rounds 33–35),
the round-35 `SCORECARD.md` section, and the parsers in `quality/check-evidence-pointers.py`.
All runs were read-only; nothing under `LOG.md`, `SCORECARD.md`, `quality/`, `corpus/`, or
the frozen round-36 tree was touched. Repo inspected at `dbf8b579aeac0f023aaf595770f1cb0049e4baa2`
(detached HEAD; `--branch master` is the gate's ancestor branch).

## 1. What the gate actually parses (quoted parser lines)

Section extraction — `quality/check-evidence-pointers.py:96-104`:

    def sections(text: str, needle: str) -> str:
        out, keep = [], False
        for line in text.splitlines():
            if line.startswith("## "):
                keep = needle.lower() in line.lower()
                continue
            if keep:
                out.append(line)
        return "\n".join(out)

Consequences:
- Only `## ` (exactly two hashes + space) toggles capture. `### ` subheadings are
  **body content** — any backticked path under a `###` line counts as a pointer.
- The match is a case-insensitive substring of the whole heading line:
  `## Round 36 — anything (2026-10-25, attempt 1)` matches needle `"Round 36"`.
- **All** matching `## ` sections concatenate into one blob — a wave-1
  `## Round 36 — SeatX seat scratch` entry folds into the round-36 pointer set too.
- A `## ` heading with no body lines before the next `## ` contributes nothing;
  `setup_ok` requires `.strip()` non-empty, so a bare heading is a MISS.

Setup gate — lines 132–139:

    log = show("LOG.md")
    scorecard = show("SCORECARD.md")
    lesson = show("corpus/lessons/round-36.md")
    setup_ok = bool(
        sections(log, "Round 36").strip()
        and sections(scorecard, "Round 36").strip()
        and lesson.strip()
    )

So `corpus/lessons/round-36.md` must exist and be non-empty at the measured rev, or
`setup=missing-r36-sections` and forced `TARGET_MISSED` regardless of everything else.

Pointer class — lines 45–49, 80–93:

    PTR = re.compile(r"`([^`\n]+)`")
    PATHY = re.compile(r"^(?:\.ufo|corpus|quality|tools|scripts|considerthese)/[^\s]*$")
    PAIR = re.compile(r"^\s*-\s*`([^`]+)`\s*->\s*`([^`]+)`\s*$")
    ...
    def pointerish(token: str) -> bool:
        if not PATHY.match(token) or " " in token:
            return False
        if token.endswith("/") or "*" in token:
            return True
        return "." in token.rsplit("/", 1)[-1]

A token is a checked pointer iff it is inside single backticks AND lane-root-relative under
`.ufo|corpus|quality|tools|scripts|considerthese/` AND contains no space AND
(ends with `/`, or contains `*`, or its last path segment contains a `.`).

Resolution — lines 107–112, against `git ls-tree -r --name-only <rev>` (committed bytes only,
never the working tree):

    if pointer.endswith("/"):
        return any(f.startswith(pointer) for f in files)
    if "*" in pointer:
        return any(fnmatch.fnmatch(f, pointer) for f in files)
    return pointer in files

Closure of the round-35 defect — lines 149–160:

    dangling35 = [p for p in ptr35 if not resolves(p, files)]
    record_intact = all(p in ptr35 for p in SUPERSEDED_POINTERS)
    pairs = [m for m in (PAIR.match(ln) for ln in log36.splitlines()) if m]
    closed = 0
    for old in dangling35:
        for m in pairs:
            if m.group(1).strip() == old and resolves(m.group(2).strip(), files):
                closed += 1
                break
    dangling35_closed = 1 if (record_intact and closed == len(dangling35)) else 0

PAIR lines are read **only from the round-36 LOG sections** (`log36`), never from SCORECARD.
The line is end-anchored: `- \`old\` -> \`new\`` and nothing else — no trailing period,
prose, or second backticked token on that line. `new` must itself `resolves()` at the rev.

## 2. Measured ground truth (commands + quoted output)

`python3 -I quality/check-evidence-pointers.py --repo . --rev HEAD --branch master`:

    PRED-PTR-r36-v1 rev=HEAD pointers_r35=8 dangling_r35=2 dangling_r35_closed=0
    pointers_r36=0 dangling_r36=0 inherited_dirty=0 scratch_tracked=124
    scratch_disposition_ok=0 tip_axis_transcript=0 setup=missing-r36-sections
    verdict=TARGET_MISSED
    dangling_r35: .ufo/waves/round-35/scratch/SimplifyCounter/
    dangling_r35: .ufo/waves/round-35/scratch/MutC1Drop/mutants/

The eight round-35 pointers (verified by re-running `sections`/`pointers`/`resolves` in-process):
RESOLVES `.ufo/waves/round-35/c1/count.py`, `.ufo/waves/round-35/w1/reports/SimplifyCounter.md`,
`.ufo/waves/round-35/w1/reports/MutC1Drop.md`, `corpus/lessons/round-34-verifier-spotcheck.md`,
`corpus/knowledge/idle-lock-never-asked-r12.md`, `.ufo/waves/round-35/registration.md`;
DANGLING the two superseded `scratch/` dirs above.

Where the dangling content actually lives at HEAD (`git ls-tree -r --name-only HEAD`):
- `.ufo/waves/round-35/scratch-evidence/SimplifyCounter/` — `analysis.md`, `count-min.py`
- `.ufo/waves/round-35/scratch-evidence/MutC1Drop/` — `gen_and_run.py`, `results.json`

`corpus/lessons/round-35-verifier-spotcheck.md:233-237` (D5) names this repair: "Append a LOG
correction naming the superseded paths." `scratch_tracked=124` at HEAD and at the frozen
before-receipt; `inherited_dirty` was 10 at freeze, is 0 at HEAD.

## 3. Required form — `## Round 36` in `LOG.md`

Append at end of file (current last entry `## Round 35 — … attempt 2 of 2`, line 2108),
after all existing entries, matching the round-33/34/35 convention:

    ## Round 36 — <theme sentence> (2026-10-25, attempt 1)

    Motivation: `corpus/lessons/round-35-verifier-spotcheck.md` routed ten defects …

    Work: …
    - `.ufo/waves/round-35/scratch/SimplifyCounter/` -> `.ufo/waves/round-35/scratch-evidence/SimplifyCounter/`
    - `.ufo/waves/round-35/scratch/MutC1Drop/mutants/` -> `.ufo/waves/round-35/scratch-evidence/MutC1Drop/`

    Honest notes: …

Constraints the gate enforces on that entry:
- The two PAIR lines must be exactly as written: `- ` + backticked old + ` -> ` + backticked
  new, whole line (regex `^\s*-\s*`([^`]+)`\s*->\s*`([^`]+)`\s*$`). Old sides must be the
  exact dangling strings; the dir-form new sides given above resolve at HEAD
  (prefix-match 2 files each). File-level new sides also work, e.g.
  `- \`.ufo/waves/round-35/scratch/SimplifyCounter/\` -> \`.ufo/waves/round-35/scratch-evidence/SimplifyCounter/count-min.py\``.
- Every other backticked lane path in the entry — including under `### ` subheadings —
  must resolve at the tip: cite only committed files. A dir citation needs its trailing `/`
  and must then prefix-match ≥1 tracked file.
- Do **not** repair by editing the round-35 entry: `record_intact` requires the two
  dangling pointers remain present in the round-35 sections (`SUPERSEDED_POINTERS`,
  lines 50–53). The repair is appended pairs in round 36, never a rewrite.

## 4. Required form — `## Round 36` in `SCORECARD.md`

Append at end of file (file currently ends inside the round-35 section at line 2230):

    ## Round 36 — <theme sentence> (2026-10-25, attempt 1)

    Registration `.ufo/waves/round-36/registration.md` froze both predicates …

    | Claim / axis | Before → after | Counting command | Author verdict |
    |---|---|---|---|
    | C1 … | … | `python3 -I .ufo/waves/round-36/c1/count.py --root . --frozen .ufo/waves/round-36/c1/frozen.json` | … |
    | C2 … | … | `python3 -I quality/check-evidence-pointers.py --repo . --rev <tip>` | … |

    ### Capabilities (round 36)
    …
    ### Sources, saturation, planned
    …

Same pointer rules apply: backticked paths under `### ` subheadings are pointers too.
Commands in backticks (containing spaces) are never pointers — the counting-command column
is safe. A lone backticked path like `` `.ufo/waves/round-36/c1/count.py` `` *is* a pointer
and must be a tracked file at the rev.

## 5. Citation-form rules (what counts, what is invisible)

| Form | Pointer? | Requirement |
|---|---|---|
| `` `corpus/knowledge/x.md` `` | yes | file must exist at rev |
| `` `.ufo/waves/round-36/scratch/Seat/` `` | yes (trailing `/`) | ≥1 tracked file under prefix |
| `` `quality/receipts/axis-*.txt` `` | yes (`*`, fnmatch) | ≥1 tracked file matching |
| `` `.ufo/waves/round-36/w1/reports` `` | **no** — last segment has no `.`, no `/`, no `*` | unchecked (but see next row) |
| `` `.ufo/waves/round-36/w1/reports/` `` | yes — trailing slash | must resolve; the slash is load-bearing |
| `` `dbf8b579aeac0f023aaf595770f1cb0049e4baa2` `` (40-hex) | no — no dot in segment | free to cite |
| `` `python3 -I .ufo/…/count.py --root .` `` | no — contains spaces | free |
| `` `/fast/scratch/mado-r33-k2-receipts/` `` | no — fails PATHY | free (but a dangling outside-tree fact, not a pointer) |
| `` `https://…` `` | no — fails PATHY | free |
| `` `considerthese/2026-10-24.md` `` | yes | must exist at rev |

Trap: the difference between `` `…/reports` `` (unchecked) and `` `…/reports/` `` (checked,
resolves by prefix) is one character. Cite a directory only when it is committed at the rev;
otherwise name a file inside it.

## 6. Adjacent observables in the same gate (out of my heading scope, stated for the seat that writes the records)

- `corpus/lessons/round-36.md` must exist non-empty **and** contain a line matching both
  `.ufo/waves/round-35/scratch` and `tracked paths=(\d+)` where N equals the tracked count at
  rev — 124 at HEAD, re-derive at the round-36 tip (lines 165–172). Note `` `.ufo/waves/round-35/scratch` ``
  without a trailing slash is not pointerish; writing it inside backticks with a trailing
  slash adds a resolving pointer — either form works if the tree stays tracked.
- `quality/receipts/axis-<40hex>.txt` must be committed, `<40hex>` an ancestor of `master`,
  and a line `MADO_AXIS:` containing `mismatched=0` and `rev=<same 40hex>` (lines 174–190).
- `inherited_dirty == 0`: the ten round-35 closure paths must be clean in `git status
  --porcelain` — currently 0 at HEAD; any wave-1 write to those paths re-dirties the counter.
- `ptr36` unions LOG + SCORECARD + lesson pointers (line 147): the lesson's pointers are
  checked too — `corpus/lessons/round-36.md` citations obey the same rules.

## 7. Verdicts

- PASS — heading form identified: `## Round 36 — <theme> (2026-10-25, attempt 1)`, appended
  at EOF in both files, with ≥1 body line before the next `## ` (parser `sections`, lines 96–104).
- PASS — citation form identified: backticked lane-root-relative paths under the six PATHY
  prefixes; file = exact name at rev, dir = trailing `/` + prefix-match, glob = `*` + fnmatch.
- PASS — repair form identified: two end-anchored `- \`old\` -> \`new\`` lines in the round-36
  LOG entry only; old strings are the two measured `dangling_r35` values; resolvable new
  sides verified at HEAD.
- PASS — append-only convention confirmed: rounds 33–35 all append `## ` sections at EOF;
  the r35 record must keep its dangling pointers (`record_intact`), so repair = append, never edit.
- FINDING — `setup` also requires committed `corpus/lessons/round-36.md` non-empty, and the
  same gate pins the lesson's `tracked paths=N` line and the `quality/receipts/axis-<40hex>.txt`
  transcript; heading work alone does not satisfy PRED-PTR-r36-v1.
- FINDING — all `## ` headings containing "round 36" (case-insensitive) fold into one blob:
  wave-1 seat-scratch entries like `## Round 35 — SimplifyCounter seat scratch` did for r35;
  every such entry's pointers count toward `dangling_r36`.

No tools installed; no installs needed. No files modified; this report is the only write.
