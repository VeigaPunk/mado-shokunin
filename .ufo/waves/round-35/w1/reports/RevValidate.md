# RevValidate — item-10 gate holds: mirror validates exit 0; escaped pipe caught, alphabetic prose recheck slips through

Seat: validator (leaf, no dispatch). Date: 2026-10-24.
Question: does the normalized append block (eight rows S203–S210 + three entries) pass
`sources-census.sh validate --file <mirror>/corpus/SOURCES.md` with exit 0 before the real
append, and would an escaped pipe or a prose recheck have been caught?

## Verdict

**Pass.** The mirror validates exit 0 with zero findings attributable to the eight rows.
An escaped pipe in a row **is caught** (E01, exit 1). A prose recheck is caught **only if it
contains punctuation or digits** (E09); an alphabetic prose phrase like `after the next
hypridle release` is accepted as a "symbolic cadence" and exits 0 — a real gap.

## Contract check — verbatim

```sh
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-35/scratch/RevValidate/corpus/SOURCES.md
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	ok	.../.ufo/waves/round-35/scratch/RevValidate/corpus/SOURCES.md
EXIT=0
```

The seven W04s are identical on the real corpus baseline (`validate --file
corpus/SOURCES.md` → same 7 lines, exit 0); they are pre-existing duplicates across scopes,
non-fatal, and not raised by the append block. **No E-code was raised against S203–S210.**

## Mirror construction

Under `.ufo/waves/round-35/scratch/RevValidate/`:

- `corpus/` — full copy (E11 checks `used-by` of every `mined` row, not just the new ones;
  `--file` resolves paths against `dirname(SOURCES.md)/..`, i.e. the mirror root).
- Eight golden rows inserted at `corpus/SOURCES.md:205-212`, inside `## Registry`
  (heading at :9, `## Paths` at :206→now later) — **not** appended at EOF.
- Three golden entries → `corpus/knowledge/idle-lock-{never-asked-r12,chain-armed-r14,offered-in-the-bar-r15}.md`
  — required by E11; all eight rows are `mined` with `used-by` pointing at them.
- Used-by closure outside `corpus/` also copied (all mirrored paths verified present):
  `tools/mado-{binds,verify,wsrules}.{py,sh}`, `quality/check-index.py`, `SKILL.md`,
  `.ufo/waves/round-{29,30}/registration.md`.
- `.ufo/waves/round-35/fetch/` receipts (8) copied for anchor-path parity; the census
  itself does not check anchors, only `used-by`.

## Findings the census raised

On the normalized block: none. Rows S203–S210 produced zero E/W lines. Ids are unique
(E03 clean), kind/tier/status enums clean, `opened=2026-10-24` not future (E08 clean),
rechecks (`on-change`, `on-request`, `90d`) all valid (E09 clean), all `used-by` targets
present (E11 clean), and the rows are host-path sources, so no URL duplicate checks fire
(`url_of` only matches `https?://`).

## Adversarial probes — would it have been caught?

| Probe | Mutation | Result | Caught? |
|---|---|---|---|
| A — escaped pipe | extra row S211 with `\|` inside the source cell | `E01 S211 fields=12`, exit 1 | **YES** |
| B1 — alphabetic prose recheck | S211 `recheck = after the next hypridle release` | `ok`, exit 0 | **NO** |
| B2 — punctuated prose recheck | S211 `recheck = ~6 months (by 2027-04)` | `E09 S211 recheck=~6 months (by 2027-04)`, exit 1 | **YES** |
| B3 — free-text recheck line | plain sentence inside `## Registry`, no leading `\|` | `ok`, exit 0 | **NO** |
| C — tail-of-file append | the eight golden rows at EOF (after `## Leads`) | `E12` ×8 (`S203 row outside Registry section` … `S210`), exit 1 | YES — wrong-place append is caught |

Mechanics, confirmed against `sources-census.sh`:

- **Escaped pipe → E01.** `row_pass` uses `gawk -F'|`; no escape handling anywhere. A
  `\|` still delimits, inflating NF to 14 (`fields=12` = NF−2). Corollary: **no cell may
  contain a pipe character at all, escaped or not** — a legitimate `\|` in prose is also
  rejected. Good for blocking malformed rows, mildly stricter than Markdown.
- **Prose recheck → E09 only partially.** Valid = ISO date, `[0-9]+d`, or
  `symbolic(s) = /^[A-Za-z][A-Za-z0-9 _-]*$/` (`sources-census.sh:582`). That regex admits
  any letter-led string of words — `after the next hypridle release` passes as a
  "symbolic cadence". Punctuation (`~`, `(`, `-`-led dates mid-string are fine; `~`/`(`/`)`
  are not) or a leading digit breaks it → E09. So a contract-degenerate but alphabetic
  recheck survives validation; the gate is lexical, not semantic.
- **Non-table prose inside Registry → invisible.** The parser only reads lines matching
  `^ {0,3}\|`; a free-text recheck note is ignored entirely — no E12 (that code only fires
  on row-shaped `| S###` lines *outside* `## Registry`).

## Operational note for the append itself

"Append" means append **at the end of the `## Registry` table** (before `## Paths` at
line 206 in the current file). A naive EOF append trips E12 on all eight rows (Probe C).
The mirror's insertion at :205–212 is the normalized shape the exit-0 verdict binds to.
