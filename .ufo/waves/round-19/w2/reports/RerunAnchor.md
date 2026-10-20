# MadoR19.RerunAnchor — breaks

Claim attacked: the anchor-durability arm (R18-V1/R18-V4 repair) — QUALITY
criterion 27's runnable check at tip `01b80946d92b26370d3012a7da655d00dd135154`:
red at `9c54c56` (`FLAGGED S084 S094`, exit 1), green at tip (`flagged=0`,
exit 0). Checker bytes: `.ufo/waves/round-19/anchor-durability.py` sha256
`9e66dce8c6af26df13769ce47fdaa3ff1464296d3929ea80bf13ee6aa77bc9e4`, identical in
the worktree and in `git show 01b80946:…`.

**Result: the literal red→green command reproduces exactly. The predicate it
prints — `ROW <id> durable` / `durable=N` — is false for constructible rows, and
for classes its own docstring and criterion 27 forbid.** Six classes are outside
the limit the lane declares for this tool; one more row can be deleted from the
census entirely, leaving exit 0.

## 1. Both revs, exactly as the ticket specifies

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ python3 -I .ufo/waves/round-19/anchor-durability.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d >/tmp/anchor_base.txt 2>&1; echo "BASE_EXIT=$?"
BASE_EXIT=1
ROW S084 UNPINNED_ALIAS — source path segment latest and anchor names no 40-hex commit, tag or dated version; also sha256 0291cfe6… is a page digest, not shown to rotate (receipts: 6 records, 1 digests)
ROW S094 PER_FETCH_DIGEST — 5 distinct 200 digests for https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black (3b18a612… ≠ 50c1ac25…; matched by credited digest 50c1ac25…)
SUMMARY rev=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d mined=80 durable=78 per_fetch_digest=1 unpinned_alias=1 flagged=2 receipt_files=49 bad_receipt_lines=0
FLAGGED S084 S094

$ python3 -I .ufo/waves/round-19/anchor-durability.py 01b80946d92b26370d3012a7da655d00dd135154 >/tmp/anchor_tip.txt 2>&1; echo "TIP_EXIT=$?"
TIP_EXIT=0
$ grep -E '^SUMMARY' /tmp/anchor_tip.txt
SUMMARY rev=01b80946d92b26370d3012a7da655d00dd135154 mined=81 durable=81 per_fetch_digest=0 unpinned_alias=0 flagged=0 receipt_files=57 bad_receipt_lines=0
```

`grep -c '^ROW'` gives 81 at tip and 80 at baseline; the two named historical
rows are the only flags at baseline. That part holds: the rotation arm does fire
on committed receipts (control S907 below re-fires it), and `S097`/`S098` pass.

## 2. Attack: rows that are not durable and print `durable`

Method: four clones of the lane in `/tmp` (`anchorlab`, `anchorlab2`,
`anchorlab3`, `anchorlab4`), rows appended after the `| S098 |` registry line,
committed, then the lane's checker run with `MADO_LANE=<clone>` against the
clone's rev. No lane file was edited. Rows are 11-column mined rows; only
source/anchor differ, the other cells are fixed filler
(`code|docs | A | anchor-lab probe | … | mined | 2026-10-20 | 90d | anchor-lab`).

| probe | source | anchor (abridged) | printed verdict (verbatim) |
|---|---|---|---|
| S901 | `raw.githubusercontent.com/basecamp/omarchy/main/install.sh` | `raw script sha256 <64>; accessed on 2026-10-20` | `durable — alias segment main pinned by date 2026-10-20` |
| S902 | `…/omarchy/main/LICENSE` | `sha256 <64>; upstream license Apache-2.0` | `durable — alias segment main pinned by version 2.0` |
| S903 | `github.com/basecamp/omarchy/blob/main/themes/matte-black/colors.toml` | `git object id 4b825dc642cb6eb9a060e54bf8d69288fbee4904; rendered page sha256 <64>` | `durable — alias segment main pinned by 40-hex commit 4b825dc642cb6eb9a060e54bf8d69288fbee4904…` |
| S904 | `…/omarchy/develop/install.sh` | `raw bytes sha256 <64>` | `durable — sha256 with no enumerated page class or pinned ref` |
| S908 | `gitlab.com/basecamp/omarchy/-/raw/file.sh?ref=develop` | `raw bytes sha256 <64>` | `durable — sha256 with no enumerated page class or pinned ref` |
| S911 | `https://docs.rs/serde/latest/serde/` | `page HTML sha256 <64>; serde 1.0.228` | `durable — alias segment latest pinned by version 1.0.228; …` |
| S913 | `…/omarchy/main/install.sh` | `raw bytes sha256 <64>; served over HTTP/1.1` | `durable — alias segment main pinned by version 1.1` |
| S914 | `…/omarchy/main/README.md` | `raw bytes sha256 <64>; 2026-10-20` | `durable — alias segment main pinned by date 2026-10-20` |
| S916 | `…/omarchy/trunk/x.sh` | `raw bytes sha256 <64>` | `durable — sha256 with no enumerated page class or pinned ref` |
| S921/S922 | `github.com/basecamp/omarchy/releases/tag/v3.8.4` | `release notes sha256 <64>; tag v3.8.4` / `release notes sha256 <64>` | `durable — sha256 over raw bytes at ref v3.8.4` |

Clone revs: `/tmp/anchorlab` `536967d6ecc7a8f41cd0cf0e301d2810cc6ab1d7` (EXIT 1,
`SUMMARY mined=90 durable=88 … flagged=2`, `FLAGGED S907 S909` — both are my
own controls, not probes: S907 (the `docs.rs/latest` URL credited with a fetched
digest → `PER_FETCH_DIGEST`) and S909 (the same URL with no pin → `UNPINNED_ALIAS`
plus the same observed variance); none of S901–S906, S908 fired);
`/tmp/anchorlab2` `144dc67768cc223fde51a6d74ff7ff7312dd1c04` (EXIT 0,
`mined=87 durable=87 … flagged=0`); `/tmp/anchorlab3`
`14d0a2e48c537a52f9a2781e161171dc92737923` (EXIT 0, `durable=83`, S921/S922 as
quoted).

Why these are not durable — each is a pin the criterion does not allow:

1. **Access date with a preposition** (S901). `pin_token` says in its own
   docstring that an access date "dates the observation, never the source, and
   is not a pin" (`.ufo/waves/round-19/anchor-durability.py:111-117`), and the
   exclusion at `:122-125` is
   `re.search(r"(?:accessed|opened|read|fetched)\s*$", lead)`. The `$` anchor
   means only the exact strings `accessed`/`opened`/`read`/`fetched` are
   excluded; `accessed on `, `opened on `, `fetched on ` are not. Verified
   directly: `'accessed on 2026-10-20'` → not excluded, `'fetched 2026-10-20'`
   → excluded. So spelling the access date the ordinary English way converts
   the script's own documented non-pin into a pin, and any `/main/` row passes.
2. **Any `N.N` is a version** (S902, S913). `TAG_RE` at `:78` is
   `(?<![\w.])v?\d+\.\d+(?:\.\d+)*(?![\w.])`, applied to the whole anchor at
   `:126-128` with no relation to the source. `Apache-2.0` → `version 2.0`,
   `HTTP/1.1` → `version 1.1`. A licence id or a protocol version is accepted
   as the source revision.
3. **40-hex is a commit without asking git** (S903). `:118-120` returns on the
   first `HEX40` in the anchor and prints `40-hex commit`. The script's only git
   call on a repo is `rev-parse` of the lane rev (`:371`); there is no
   `cat-file`, no lookup in the cited project. The probe uses the git *empty
   tree* id: `git cat-file -t 4b825dc642cb6eb9a060e54bf8d69288fbee4904` →
   `tree`. A tree (or blob, or any hex string) is certified as a commit pin.
4. **The alias allowlist is four words** (S904, S908, S916). `:70`
   `ALIAS_SEGMENTS = ("latest", "main", "master", "HEAD")`. A source on
   `develop`, `trunk`, `dev`, `nightly`, or a branch named in a query
   (`?ref=develop`) is not an alias at all, so the alias arm never runs and the
   fallback at `:305-311` returns `durable` with the reason
   `sha256 with no enumerated page class or pinned ref` — the printed reason
   itself states that nothing is pinned.
5. **An HTML page digest re-labelled as raw bytes** (S921/S922). A
   `releases/tag/vX` page matches neither `PAGE_URL_RE` (`:73-75`: only
   `api.github.com`, `docs.rs`, `github.com/<o>/<r>/(tree|blob)/`) nor
   `PAGE_TOKEN_RE` (`:71`) when the anchor says "release notes" instead of
   "tree/blob/html". `ref_segment` then finds the tag segment and `:302`
   prints `sha256 over raw bytes at ref v3.8.4`. The bytes are an HTML page,
   and because the page-note branch never fired, the disclosure that would have
   said "page digest, not shown to rotate" is suppressed. This is R18-V1's
   defect class (HTML body as anchor) labelled with the most durable-sounding
   reason in the script.
6. **`latest` + a version named only in prose** (S911). This is S084's shape —
   `docs.rs/xdg/latest/…` was `UNPINNED_ALIAS` — re-passing because the anchor
   now names a version (`serde 1.0.228`). The URL still serves whatever
   `latest` is at fetch time, so the credited digest is not shown to belong to
   that version [INFERENCE: this is the same defect M2 records, with the
   version written into the prose rather than into the URL].

None of these is the limit the lane declares for the tool. QUALITY criterion 27
(`corpus/QUALITY.md:174-181` at `01b80946`) says only: "it reads the anchor text;
it cannot tell a reproducible page that has never been fetched twice" and
"PER_FETCH_DIGEST needs ≥2 distinct committed 200 digests". Every probe above is
an anchor-text false pin or a missing alias word — a shape the tool claims to
judge ("it judges URL and receipt shape only").

## 3. Lane-resident: the tip's only mined alias row is certified by a date

At tip exactly one mined row takes the alias arm:

```
ROW S005 durable — alias segment main pinned by date 2026-01-16
```

`S005` (`git show 01b80946:corpus/SOURCES.md` line 17) is
`https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md`
with anchor `README.md §Protocol phases @ main 3dac056d (2026-01-16, last commit
touching README.md)` — a `/main/` blob page, dated, naming an abbreviated commit
and **no sha256 anywhere**, and there is no receipt for the URL at any round
(`git grep -h "wayland-protocols" 01b80946 --
'.ufo/waves/*/fetch/*/receipts.jsonl' | wc -l` → 0). The checker credits it by the date because the date branch
(`:121-125`) runs before the abbreviated-commit branch (`:129-135`), so the
`3dac056d` in the same anchor is never even parsed, and nothing here verifies
that it is a commit in that project. Whether the row discharges criterion 27's
"commit-pinned bytes with their sha256" is a judgement call [INFERENCE], but the
printed reason misstates its pin, and this is the only live alias row whose
green the tip's `flagged=0` rests on.

## 4. What legitimately passes and must not be counted as falsification

The ticket's first example — a GitHub blob page digest with one receipt — does
print `durable`:

```
S905  https://github.com/basecamp/omarchy/blob/v3.8.4/README.md   (1 receipt, 1 digest)
ROW S905 durable — sha256 83ae9987… is a page digest, not shown to rotate (receipts: 1 records, 1 digests)
S906  …/blob/v3.8.4/install.sh  (0 receipts)
ROW S906 durable — sha256 fae7cfc3… is a page digest, not shown to rotate (receipts: 0 records, 0 digests)
```

This is the pre-declared limit (QUALITY.md:178-180), so it is not a
falsification of the claim — but it is still counted in `durable=81`, which is
why the summary number cannot be read as "81 reproducible anchors". The same is
true at tip for live rows S063/S064, whose anchors are wiki HTML page digests
(`corpus/SOURCES.md` rows S063/S064; run prints `durable — … page digest …`).
A spelling-level blind spot in the rotation arm: a page fetched under two URL
keys (bare and `?plain=1`) with one digest each is *not* "shown to rotate"
because `rotation_match` (`:217-236`) keys on exact URL string and on a credited
digest; my S915 pair (digests A at `…/SECURITY.md`, B at `…/SECURITY.md?plain=1`)
printed `durable … not shown to rotate (receipts: 1 records, 1 digests)`. This
is suggestive only — A and B are different rendered views, so it does not by
itself prove the document rotated [INFERENCE].

## 5. A non-durable row can be removed from the census (exit 0)

`parse_rows` drops any row whose cell count is not 11 (`:315-324`) and `main`
prints it to **stderr only** (`:386`); dropped rows never enter `rows`, are
never evaluated, and do not affect the exit code.

Control pair, identical except for one character, `/tmp/anchorlab4`:

```
S931  source …/omarchy/main/bootstrap.sh  anchor "raw bytes sha256 <64>; command is curl sh"
S932  same source,  anchor "raw bytes sha256 <64>; command is `curl | sh`"      ← the pipe

rev b47a7fa18618cdde520ac9106ae2d989ddf75c42 (both rows):
ROW S931 UNPINNED_ALIAS — source path segment main and anchor names no 40-hex commit, tag or dated version
SUMMARY rev=b47a7fa18618cdde520ac9106ae2d989ddf75c42 mined=82 durable=81 per_fetch_digest=0 unpinned_alias=1 flagged=1 receipt_files=57 bad_receipt_lines=0
FLAGGED S931
malformed: line 112 S932 (not 11 columns)          (stderr)
EXIT 1   ← from S931 only

rev fa75cb63a6f16f61bdb6280a69c559bff41c59a1 (S931 removed, S932 alone):
SUMMARY rev=fa75cb63a6f16f61bdb6280a69c559bff41c59a1 mined=81 durable=81 per_fetch_digest=0 unpinned_alias=0 flagged=0 receipt_files=57 bad_receipt_lines=0
malformed: line 111 S932 (not 11 columns)          (stderr)
EXIT 0
```

The `fa75` rev still holds 82 rows with status `mined` (`grep -c '| mined |'`),
yet the summary says `mined=81 … flagged=0`, exit 0 — byte-for-byte the tip's green
shape. `--rows S932` does not recover it either: `could_not_evaluate: absent row
S932`, exit 2 (`:392`). A producer can therefore hide an unpinned alias row
with a literal `|` in an inline code span, which is ordinary prose in this
corpus.

## 6. Verdict

- Literal claim (red at `9c54c56`, green at `01b80946`, both named rows): **holds**.
- What the green *means* — "81 durable anchors / criterion 27 discharged":
  **breaks**. Six independent shape classes outside the declared limit print
  `durable`, including a class that reproduces S084 with the version in prose and
  a class that reproduces R18-V1's HTML-body anchor under the label "raw bytes at
  ref". One more class removes rows from the census while keeping exit 0.

The tool is a two-pattern screen (rotation over committed receipts; four alias
words with a loose pin token). It is a useful tripwire for the two historical
rows it caught; it is not a durability certificate, and any consumer that reads
`durable=81` / `flagged=0` as criterion 27 being met is over-reading it.

An uncommitted wave-2 append to the worktree already records part of this from
another seat (`corpus/QUALITY.md:206-215`, not mine, not committed at `01b80946`):
"prints `durable` when no rule fires — not proof of reproducibility … reads any
`N.N` in the anchor as a pin … knows only the alias words
`latest`/`main`/`master`/`HEAD`". My runs are independent confirmation of those
three and add: the `accessed on <date>` bypass of the docstring, the 40-hex
object-id/commit confusion, the HTML-page-as-raw-bytes label, the malformed-row
census escape with a control pair, and the `docs.rs/latest` + prose-version
re-pass.

## Limits

- Row injection was done in `/tmp` clones only; the probes are synthetic rows I
  wrote, not lane rows. The lane's own rows were not modified; its only mined
  alias row at tip is S005 (§3), examined read-only. No network fetch was
  performed; source URLs were not contacted.
- `S911`'s judgement that `/latest/` + a prose version is "not durable" is my
  reading of M2's defect class, not a fetched proof that docs.rs served a
  different version [INFERENCE].
- The S915 `?plain=1` observation is a URL-key granularity note only; the two
  bodies are different views, so it is not proof of rotation [INFERENCE].
- The malformed-row escape is demonstrated with `|` inside an inline code span;
  I did not enumerate all ways a real row can acquire an extra cell.
- Baseline/tip runs used the worktree checker, byte-identical to the tip blob
  (sha256 above). `corpus/QUALITY.md` in the worktree has uncommitted wave-2
  appends by another seat; criterion 27 was read from `git show
  01b80946:corpus/QUALITY.md:174-181`.
- `/tmp` clones are ephemeral; the probes are reproducible from the row table
  above. Each `<64>` was `sha256(<row id>)` (S921/S922: `sha256('S921')` /
  `sha256('S922')`; S915: `sha256('S915-a')` / `sha256('S915-b')`), and where a
  receipt was needed it repeats the same digest under the row's URL (S905: one
  record; S915: one record per URL spelling). The S907/S909 controls share the
  live `docs.rs/xdg/latest/…` URL, which already carries a 200 receipt at tip;
  the lab adds two digests, and the three distinct values fire the rotation arm
  for S907 and the alias+rotation arms for S909. Append the
  11-cell lines after `| S098 |`, `git add -A && git commit`, then
  `MADO_LANE=<clone> python3 -I <lane>/.ufo/waves/round-19/anchor-durability.py <clone-rev>`.

## Installs

none.
