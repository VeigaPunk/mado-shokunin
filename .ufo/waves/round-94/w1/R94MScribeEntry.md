# R94MScribeEntry — C1 knowledge entry (draft)

Seat: R94MScribeEntry (scribe), round mado 94, wave w1. Base `a3de997289014e7dbf1d73ae206be1d6f8cdadd0`.
Deliverable: the C1 knowledge entry, drafted at
`.ufo/waves/round-94/build/mime-glob-guess-r94.md` (sha256 `5846a0190c60836f1b48f18b87552539151e35fc76d57dca45bc791460870e8f`,
26 134 B, 327 lines), for the L1 to review and land at `corpus/knowledge/mime-glob-guess-r94.md`.

**Everything in this report and in the entry is DRAFT.** No case file, label file, counter run or
receipt is involved: nothing was frozen, nothing was measured, nothing was written under
`.ufo/waves/round-94/receipts/`.

## 1. What was done

Read the declaration, the sources-open receipt, the two model entries
(`portal-keyfile-bytes-r93.md`, `mime-default-resolution-r91.md`) and the C1 candidate
(`.ufo/waves/round-94/build/mado-mimeglob.c1.py`, sha256 `0700915a…d63e` — pin re-checked and equal to
the assignment). Refetched the five GLib files and the spec page named in the receipt into scratch;
all five GLib digests equal the receipt's two-fetch digests byte for byte. Compiled the oracle and ran
it against the candidate on 101 names over 40 fixture databases (globs2, globs, hand-made and
`update-mime-database`-built caches), then wrote the entry with one source line or one oracle row for
every behavioural statement.

Source re-verification (my fetch vs `.ufo/waves/round-94/receipts/sources-open-r94.txt`):

| file | sha256 (mine) | receipt |
|---|---|---|
| `xdgmimeglob.c` | `38ed8623…0734` | equal |
| `xdgmimecache.c` | `ccda4366…db69` | equal |
| `xdgmime.c` | `afb1c1c1…2410` | equal |
| `gcontenttype-fdo.c` | `8a5b4f47…2d7c` | equal |
| `xdgmimeint.c` | `c2364aa8…2f29` | equal |
| `ar01s02.html` (raw) | `1566c459…3c66` | receipt holds the tags-stripped copy `e00fa00e…c61e`, not the raw HTML — expected, recorded in the entry's front matter |
| `xdg-mime.in` (fetched for §1 scope, HTTP 200) | `11e7d91e…5c7e` | equal to the S508 row in `corpus/SOURCES.md` |

## 2. Commands run (exit codes)

| # | command | rc | result |
|---|---|---|---|
| 1 | `curl -fsS -o <f> https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/xdgmime/{xdgmimeglob,xdgmimecache,xdgmime,xdgmimeint}.c` (+ `gcontenttype-fdo.c`, `ar01s02.html`) | 0 | digests equal to the receipt |
| 2 | `curl -fsS -w '%{http_code}' -o xdg-mime.in …/xdg-utils/-/raw/v1.2.1/scripts/xdg-mime.in` | 0 | HTTP 200, sha256 equal to S508 |
| 3 | `gcc -O1 -o "$S/oracle" .ufo/waves/round-94/controls/mimeglob-oracle-r94.c $(pkg-config --cflags --libs gio-2.0)` | 0 | oracle 16 136 B |
| 4 | `TMPDIR=$S python3 probe.py > probe-rows.txt` (driver in `w1/`) | 1 | 101 rows, **98 agree, 3 tool refusals** (the driver exits 1 when a row is a refusal) |
| 5 | `python3 -I …/build/mado-mimeglob.c1.py --selftest` | 0 | `MADO_MIMEGLOB_SELFTEST: checks=15 failed=0` (DRAFT) |
| 6 | tool `--json` on the host, synthetic names | 0 | `mode=cache`, 3 dirs |
| 7 | `env -i LC_ALL=C HOME=… XDG_DATA_HOME=… XDG_DATA_DIRS=… ./oracle <5 synthetic names>` | 0 | agrees with 6 on every label |
| 8 | cache dump of a generated `mime.cache` (literal list) | 0 | `'makefile' c/three 0x32` — the builder lowercases literal globs |
| 9 | `grep -n "Makefile" /usr/share/mime/globs2` | 0 | `432:50:text/x-makefile:makefile` — the generated text form is lowercase too |
| 10 | `test -e` on `~/.local/share/mime/{,mime.cache,globs2}` and `/usr/local/share/mime` | varied | user dir present with both a cache and a globs2; `/usr/local/share/mime` absent; `/usr/share/mime/mime.cache` present |

No install was needed or performed: `gcc`, `pkg-config gio-2.0`, `curl`, `python3` and
`update-mime-database` (used only on scratch directories) were already present. One read-only package
query was made (`pacman -Q glib2 shared-mime-info` → `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`,
rc 0); no pacman transaction, no service change.

## 3. What the entry asserts (and the evidence class of each part)

- §2.1 dirs — S505 `xdgmime.c:217-300`; rows `e8`, `e8b`, `e8c`, `e8d`, `e8e`. The one statement not
  reproducible by run is the literal `"/mime/"` for an empty `XDG_DATA_HOME` (needs root); it is cited
  to the source line and marked `[UNVERIFIED]` in the entry, as instructed.
- §2.2 mode — S505 `xdgmime.c:129-211`, `:639-651`; S516 `:127`, `:60-62`; rows `e5`, `e14`, `e15`,
  `e19`.
- §2.3 text lookup — S515 `:420-500`, `:537-560`, `:628-720`, `:377-390`, `:392-417`, `:463-467`,
  `:469-480`; rows `e1`, `e2`, `e3`, `e4`, `e9`, `e11`, `e18`, `e21`, `e31`, `e32`.
- §2.4 cache lookup — S516 `:669-730`, `:574-616`, `:414-424`, `:414-415`, `:468-469`, `:555-556`;
  rows `e6`, `e12`, `e23`, `e29`.
- §2.5 guess — S518 `:568-690`; rows `e1`, `e6`, `e16`, `e17`, `e18`.
- §3 departures D1–D9 — each is a spec sentence from S517 next to the GLib line and a row: D1 `e2`,
  D2 `e6`/`e6b`, D3 `e1`(`x.dup`), D4 `e4`/`e24`/`e25`, D5 `e17`, D6 `e3`/`e6`/`e26`/`e26b`, D7 `e12`,
  D8 `e1`/`e32`/`e6` + the cache dump, D9 `e16`.
- §4 operator consequences — §2.1/§2.2 (dead `globs2`, dead `packages/`, stale cache), the host
  `mode=cache` run, and the host `.png` ambiguity (see F5 below).
- §6 limits — sniffing, the C-locale `fnmatch`, the `HOME`-unset divergence (candidate:574), the
  `*`-glob and non-UTF-8 refusals (candidate:249, :240), unsorted hand-made cache lists, format-level
  weights, and "nothing is frozen".

## 4. Findings for the L1 (each with a reproducing input and the oracle's label)

**F1 — `__NOGLOBS__` is not implemented by GLib at all.** `grep -n NOGLOBS` over the four GLib files
returns nothing. Reproduction: two dirs, `s1/mime/globs2 = "50:text/x-diff:*.patch"`, `s2/mime/globs2
= "0:text/x-diff:__NOGLOBS__\n50:text/x-diff:*.d2"`, text mode; name `a.patch` → oracle
`text/x-diff	0`. Deletion only happens inside one `update-mime-database` build (`e25`: a package with
`<glob-deleteall/>` and `*.diff` gives `a.patch` → `application/octet-stream	1`), and even then it
does not remove another directory's glob (`e24`: `a.patch` → `dl/x	0`). The declaration's sentence
"`__NOGLOBS__` deletion" is therefore right in effect but easy to over-read: the *reader* has no
deletion branch.

**F2 — the per-cache suffix scope is observable and should be in the frozen set.** Two caches, one
with `*.gz` (weight 20) and one with `*.tar.gz` (weight 50), name `x.tar.gz`: cache mode →
`c/two	1`; the same two globs as `globs2` files → `c/two	0`. Without a two-cache overlapping-suffix
case, a model that collapses the per-cache union into one deepest match passes every other case.

**F3 — `update-mime-database` lowercases literal globs, so literal case behaviour is mode-dependent.**
The dump of a generated cache holds `'makefile'` for `<glob pattern="Makefile">`, and
`/usr/share/mime/globs2:432` holds `50:text/x-makefile:makefile`. In text mode a mixed-case literal is
effectively case-sensitive (`e1`: `MAKEFILE` → `application/octet-stream	1` with a stored
`Makefile`, while a stored `makefile` gives `text/x-make	0`, `e32`). The frozen `literal` class should
carry both modes and a mixed-case literal.

**F4 — the candidate refuses two constructs the oracle answers, so the C1 predicate as drafted is
unsatisfiable if either enters the frozen set.** (a) a bare `*` glob: tool exit 3
`UNSUPPORTED … simple glob with an empty suffix`, oracle `application/octet-stream	1` (`e27`,
`dh/mime/globs2 = "50:app/star:*"`); (b) a `globs2` line with an invalid UTF-8 byte: tool exit 3 for
*every* name in that directory, oracle `text/ok	0` for `a.ok` (`e30`). Both are refusals, not wrong
answers, which the declaration permits — but clause (i) says "on every frozen case the tool's (type,
uncertain) equals the oracle's", and a refusal has no (type, uncertain). Either keep these two
constructs out of `mimeglob-cases-r94.json` / the fresh generator / the host name list, or amend the
predicate to treat exit 3 as a miss. This is the one place where the draft declaration and the tool
disagree, and the L1 must decide before the freeze.

**F5 — on this host a `.png` name is already uncertain.** DRAFT host run: tool `mode=cache`, 3 dirs;
`image.png` and `IMAGE.PNG` → `image/png	1` from both the oracle and the tool, and the tool's `types`
array is `["image/png", "image/apng"]` (two types carry `*.png` in the host databases). The host-name
clause compares tool against the live oracle, so it is safe, but any expectation written by hand as
"`.png` → certain" would be wrong.

**F6 — the candidate's `HOME`-unset substitution is a source-level divergence, unreachable from a case
file.** Candidate:574 (`env.get("HOME", "/")`) feeds `xdgmime_dirs` (:448-451), so with both
`XDG_DATA_HOME` and `HOME` unset it searches `/.local/share/mime/`, where C (S505:244-263) adds no
first directory at all. Observable only if `/.local/share/mime` exists; marked `[UNVERIFIED]` in the
entry. Not a blocker.

**F7 — no label disagreement was found otherwise.** 98 of 101 rows agree on (type, uncertain); the
three exceptions are F4's refusals. The candidate models the text/cache phase structure, the
`cs`/ASCII-fold rules, the weight merge and sort, the cache weight encoding, the cache version gate
and the guess's 0/1/many cases as GLib 2.90.1 executes them on this host (DRAFT).

## 5. Gates

None. No counter was run (the C1 counter is not mine and does not exist yet), no frozen case file was
touched, no `--expect-*` sha256 was produced, and no receipt was written. Every run above is labelled
DRAFT.

## 6. Touched surfaces

Written (only these):

- `.ufo/waves/round-94/build/mime-glob-guess-r94.md` — the drafted entry (mine).
- `.ufo/waves/round-94/w1/R94MScribeEntry.md` — this report.
- `.ufo/waves/round-94/w1/R94MScribeEntry-probe.py` (sha256 `9891e31c…a93f`) and
  `.ufo/waves/round-94/w1/R94MScribeEntry-rows.txt` (sha256 `ef3174ec…26c5`, 104 lines / 101 rows) —
  the driver and its output, copied out of scratch as the evidence the entry cites.

Not touched: `tools/`, `quality/`, `corpus/`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`,
`MANIFEST.json`, the declaration, the candidate, the oracle, any other lane file, `.ufo/state/`,
`.scratch/`, the fleet root, sibling repos. No git or jj command was run anywhere (read-only or
otherwise). No file under `~/.local/bin` or any PATH directory was created or modified.

## 7. Out of scope (deliberately not done)

- Building the frozen case file, the fresh generator, the host name list, the mutants, the counters or
  the kill-sets — other seats' files.
- Any scoring, any freeze, any commit, any receipt, any `SCORECARD.md`/`LOG.md`/lesson edit.
- Any read of credential material or any listing of real file names from the user's home; the host
  reads were `/usr/share/mime/globs2:432`, existence tests on the three mime directories, and the
  session's own `HOME`/`XDG_*` values.
- Launching any application, restarting any service, or running any pacman transaction.

## 8. Scratch

`S=$HYAKU_SCRATCH/mado-r94/R94MScribeEntry` (held the oracle binary, the six source files, the 40
fixture roots and the driver) was removed after the driver and its output were copied into
`.ufo/waves/round-94/w1/`. Nothing of this seat remains on disk outside the lane.
