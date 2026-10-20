# CriticC2 — attack on C2 (rubric V 4/6 → 6/6 via documentary P3/P5 notes)

Seat: MadoR18.CriticC2 (critic, leaf). Wrote only this report. Lab work ran in
`/tmp/criticc2-lab` (fetch-verify forgery) and `/tmp/criticc2-clone` (a git
clone of the lane at `d3a0000` plus one lab commit). Lane reads were read-only
`git` and file-byte reads. Host reads were file bytes only: `/var/log/pacman.log`,
`~/.local/share/omarchy/.git/{HEAD,packed-refs,FETCH_HEAD,logs/HEAD}`,
`~/.local/share/omarchy/{version,bin/*}`, `~/.config/omarchy/current/*`,
`~/.config/walker/config.toml` and `~/.cache/yay/elephant/PKGBUILD`.
I made no web fetches, ran no package command, and installed nothing.

## Verdict

The 6/6 is **denominator closure with a real but narrow gain**. It is not
coverage of observed behaviour. The gain is real in one way: P3/P5 get their
first **sourced, upstream-pinned** routes. Rubric V cannot tell this gain
apart from template conformance. Raw fetch receipts, as checked today, do
**not** defeat an invented row. They only defeat a row that has no receipt
at all. This is fixable without changing the instrument (corrections below).
The claim must then be worded as "sourced documentary route per surface",
and rubric V must be declared saturated.

## Counterexample 1: rubric V is L1-authorable with no receipt and no observation (lab-proved)

In `/tmp/criticc2-clone` at `d3a0000` I added the following, then ran
`python3 .ufo/waves/round-17/measure.py HEAD`:

- **SOURCES row.** One row inside `## Registry`:
  - `S099`, https raw `abenz1267/walker/v2.17.2/src/theme/mod.rs`
  - kind `code`, tier `A`, status `mined`
  - used-by `corpus/knowledge/theme-route-lab.md`
  - no receipt exists for it
- **Note.** `theme-route-lab.md` with `surface: P5` and the four sections (3 lines each).
  - Host declaration: "swaybg is displaying 0-ship-at-sea.jpg on every output right now", "walker 2.17.2 is the running launcher binary".
  - Safe observation: "All theme consumers reloaded successfully".
  - Unexercised behavior: "[UNK] nothing else."

Result: `c2 count 5, score 8.3333`, with P5 covered by
`{'path': 'corpus/knowledge/theme-route-lab.md', 'reason': 'surface: P5', 'sources_ok': ['S099']}`
and `rejected []`.

Three defects show up here:

- **(a) measure.py never reads receipts.** R17-V3 exists only outside the
  instrument. A credited row is whatever L1 types into SOURCES.
- **(b) The T4 keyword `theme` matches walker's launcher-theme code.** A P5
  credit can rest entirely on a walker row: false provenance and the wrong
  surface. This is a live risk this round. `MadoR18.SrcWalkerThemes` fetched
  `walker/v2.17.2/src/theme/mod.rs`, and `resources/themes/default/*`, both of
  which would satisfy P5's T4 test.
- **(c) The required sections are a line floor plus a `[UNK]` substring.**
  Present-tense runtime claims in `## Host declaration` / `## Safe observation`
  are invisible to the instrument.

## Counterexample 2: fetch receipts do not defeat a forged row (lab-proved)

In `/tmp/criticc2-lab` I fabricated a body: "walker reads
~/.config/walker/invented.toml and auto-reloads on save". I wrote a receipt
for it that claims URL `https://raw.githubusercontent.com/abenz1267/walker/v2.17.2/README.md`,
http 200, with the forged body's real sha256 and byte count, plus a SOURCES
fixture row S099 citing that URL. Then I ran:

```
python3 -I .ufo/waves/round-18/fetch-verify.py --fetch-root fetch --sources SOURCES.md --rows S099 --quote 'S099=auto-reloads on save'
FETCH Forger/walker-readme.md ok
ROW S099 receipted
QUOTE S099 ok
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=0      (rc=0)
```

I repeated it with the real `NoteWalker/` receipts merged into the same fetch
root. That directory holds a genuine receipt for the **same URL** with sha
`9755f955d5c4…`. Result: `SUMMARY receipts=28 ok=28 bad=0 … quote_bad=0`.
The checker has no URL→sha consistency rule, so the conflict passes silently.

A receipt is seat-authored JSON, and `body` is any bytes the seat saved.
sha/bytes self-consistency proves storage, not provenance. Copying a host
file into a body defeats a host-byte join too: the omarchy host files are
byte-identical to the tag (below), so a forger could copy them and claim the
URL.

What does carry provenance is **independent re-fetch agreement on a
deterministic URL**. Across all 167 receipts currently in
`.ufo/waves/round-18/fetch/*/receipts.jsonl`:

- Every receipt verifies: 0 bad sha, bytes or missing.
- Raw tag URLs fetched by several seats agree byte-for-byte, for example:
  - `omarchy/v3.8.4/bin/omarchy-theme-set`: 5 seats, all `79069c8018a7…`
  - `walker/v2.17.2/README.md`: 3 seats, all `9755f955d5c4…`
  - `walker/v2.17.2/resources/config.toml`: 3 seats, all `3c5c6867d021…`
  - `swaybg/v1.2.2/swaybg.1.scd`: 2 seats, all `68ed5503298f…`
- Receipt mix: 113 raw-tag, 14 api.github.com, 40 HTML/other.
- GitHub HTML tree pages carry per-request tokens (`nonce`/`request-id`, 3
  hits each in `NoteTheme/omarchy-themes-tree.html` and
  `swaybg-v1.2.2-tree.html`), so their sha cannot be reproduced by re-fetch.
- `codeload…/tar.gz/refs/tags/v2.17.2` archive bytes are not guaranteed
  stable either.

Those receipts must not be the T4-satisfying (credited) evidence.

## Counterexample 3: the P3/P5 gaps were template gaps, and older observed notes are now stale

The lane already holds **observed** walker and theme work. None of it is
creditable because it has no head `source:`/`surface:` lines:

- `walker-deep.md:27-28` observed `walker --version` → `2.17.0` and
  `elephant version` → `2.21.0` (round 5).
- `walker-deep-r9.md:58` holds a byte-level `2.17.0\n`.
- `theme-wallpaper-plane.md:157-158` observed swaybg PID 1203358 with argv
  `-i …/current/background -m fill`.

So C2 does not take P3/P5 from "unknown" to "known". It adds upstream sourcing
to surfaces that were observed under now-superseded versions. File reads of
`/var/log/pacman.log` show today's upgrades:

- `:2929` `upgraded walker (2.17.0-1 -> 2.17.2-1)`, inside the `pacman -Syu`
  transaction of `:2462`.
- `:3092` `pacman -U … /home/vgpnk/.cache/yay/elephant/elephant-2.22.1-1-…pkg.tar.zst`:
  a local AUR build, not a repo package.
  - `:3107ff` `upgraded elephant-* (2.21.0-1 -> 2.22.1-1)`.
  - The `-debug` packages installed at `:3093ff` were removed at `:3132-3147`.
- `walker-restart.hook` ran at `:3062` and `:3123`. That is a package hook
  line, not proof that any restart succeeded.

The NoteWalker item text says "so you do not contradict" `walker-deep-r9.md`
/ `walker-live-surface.md`. Read literally, it pushes the scribe to smooth
over the drift. The correct move is explicit supersession: the r5/r7/r9
observations are dated observations of 2.17.0/2.21.0, and the binary running
now is `[UNK]`.

## Positive evidence the notes can legitimately use (file bytes, not behaviour)

Host omarchy files are byte-identical to the `v3.8.4` tag bodies already
receipted:

| Host file | sha256 prefix (host = receipt body) |
|---|---|
| `bin/omarchy-theme-set` | `79069c8018a7` |
| `bin/omarchy-theme-bg-next` | `ee4828127755` |
| `default/hypr/autostart.conf` | `acb6a6686203` |
| `bin/omarchy-launch-walker` | `fd9e93f830bc` |
| `bin/omarchy-restart-walker` | `9ac82d0c1370` |
| `config/walker/config.toml` | `fecf71fa4253` |

`~/.config/walker/config.toml` is also `fecf71fa4253…`, which equals omarchy's
default byte-for-byte.

Checkout identity, read as `.git` bytes:

- `HEAD` = `ref: refs/heads/master`
- `packed-refs:2` gives `refs/heads/master` = `8fcc9d6048af…`
- `packed-refs:508` gives `refs/tags/v3.8.4` = `8fcc9d6048af…`
- `FETCH_HEAD` agrees.
- `api.github.com` (receipt in `MadoR18.HostOmarchyCheckoutTag`) resolves the
  tag to the same commit. The repo now redirects to `omacom/omarchy`.

Trap: `~/.local/share/omarchy/version` reads `3.8.3`, and so does the tag's
own `version` file (receipt body `omarchy-v3.8.4-version.txt`). Version the
checkout by tag commit, never by the `version` file.

Elephant build input: `~/.cache/yay/elephant/PKGBUILD:13-14` pins
`${url}/archive/refs/tags/v${pkgver}.tar.gz` with sha256 `3d1d0d4c55ae…`.
This anchors build input, not the installed binary.

Host theme declarations:

- `~/.config/omarchy/current/theme.name` = `matte-black`
- `background` → `…/current/theme/backgrounds/0-ship-at-sea.jpg`
- mtimes 2026-10-03

These are consistent with `theme-wallpaper-plane.md:74-75`.

## What the notes must contain

1. **Head.** Every cited row is an upstream raw tag/commit URL with a
   deterministic body. For P5, the T4-satisfying row is an omarchy theme/bg
   script (`omarchy-theme-set`, `-bg-next`, `-bg-set`) or swaybg
   (`swaybg.1.scd`/`main.c`), **never** a walker theme row. For P3, at least
   one row is walker or elephant upstream at `v2.17.2`/`v2.22.1`. The
   omarchy-launch-walker row may be supplementary only.
2. **`## Upstream contract`.** Each claim carries a `<receipt body>:<line>`
   anchor and a ≤25-word verbatim quote, and names the tag→commit.
3. **`## Host declaration`.** Only file-byte facts, each with sha256 plus a
   path:line anchor:
   - the six byte-equalities above;
   - theme.name, background symlink, walker config;
   - versions as "last logged transaction" with `pacman.log:N`, including the
     elephant AUR `-U` origin and the walker `-Syu` origin.
4. **`## Safe observation`.** States which file-byte reads were made and which
   probe classes are forbidden by the host pause. Contains no outcome of any
   run.
5. **`## Unexercised behavior`.** `[UNK]` for each of:
   - running walker/elephant binary version, and whether the walker-restart
     hook succeeded;
   - elephant providers that are active (config-declared providers in
     `~/.config/elephant/*.toml` vs installed packages vs active);
   - live swaybg/wallpaper display and theme application/reload of every
     consumer;
   - whether AUR/repo builds match tag source.

   It must also explicitly mark the r5/r7/r9 observations as pre-upgrade and
   superseded.

## What the notes must refuse to claim

- Anything in present tense about processes, display, reload, firing, or the
  running version.
- That a `pacman.log` line equals installed or running state.
- That host-byte equality with a tag proves runtime behaviour.
- That the tag source equals the AUR or repo binary.
- That an older OBS row is current.

## Smallest safe corrections (instrument unchanged)

1. **fetch-verify.py, URL→sha conflict rule.**
   - If one URL has receipts with ≥2 distinct sha256 → `URLCONFLICT <url>`, exit 1.
   - For every credited row, require ≥1 matched receipt whose URL is
     `raw.githubusercontent.com/<o>/<r>/<tag|commit>/…`.
   - For the T4-satisfying row, require receipts from ≥2 distinct seats with
     the same sha (already true for the walker README/config and omarchy
     theme-set/bg-next).
   - HTML/codeload/docs.rs receipts stay supplementary.
   - Shown able to fail: the merged lab above would print `URLCONFLICT` for
     `walker/v2.17.2/README.md`.
2. **Closure command pinned in the C2 result text.**
   - Run `measure.py REV` and list `c2.provinces.P3/P5.entries[].sources_ok`.
   - Then run `fetch-verify.py --sources corpus/SOURCES.md --rows <exactly those ids> --quote 'S0xx=<gate quote>'…`
     at the result revision; it must exit 0.
   - Also assert that the P5 T4 row's source cell names omarchy theme/bg or
     swaybg, not walker.
3. **Runtime-claim tripwire for the two notes.** Use a lexical deny-list
   outside `## Unexercised behavior`:
   - pattern: `is running|running (binary|process|daemon|launcher)|is displaying|currently (running|shown|displayed|active)|right now|reloaded successfully|was applied|PID \d+|is active`
   - a hit fails unless the line carries `[UNK]`, a dated or round cite, or a
     quoted `<body>:<line>` upstream quote.
   - Calibration: 4 hits on the lab note; 0 on the admitted
     `idle-lock-route-r17.md` and `terminal-route-r17.md`.
   - Known false-positive class: verbatim upstream quotes, for example
     `SrcWalkerReadme.md:58` "elephant is running before starting Walker".
     Hence the quote exemption.
4. **SCORECARD wording.**
   - Say "rubric V 6/6 = each province has ≥1 sourced, receipt-backed
     documentary route; observed coverage unchanged; P4/P5/P3/P6 routes are
     documentary".
   - Declare rubric V **saturated** after this round. U-route is already
     saturated at 7/7. Any further coverage claim needs a new rubric, e.g.
     receipted host-byte joins, or observed-behaviour rows once the host
     pause lifts. Otherwise the coverage axis reads as finished: premature
     saturation.
5. **R17-V3 symmetry.** P4/P6 were credited in round 17 without receipts. If
   `FetchBackfillR17` finds any sha mismatch or missing quote for
   S056-S058/S063-S069, the 6/6 must be restated with the affected province
   flagged. Do not report the 6/6 while it rests on unreceipted P4/P6 rows.

## Impacted axes

- **Coverage.** The claim's meaning: false-provenance risk on P5 via T4
  `theme`, and premature saturation.
- **Calibration.** fetch-verify passes a forgery. If cited as R17-V3's fix
  without correction 1, that is a new instance of R17-V5: an instrument
  claimed to bite that does not.
- **Freshness.** Walker and elephant drift today (2.17.0→2.17.2,
  2.21.0→2.22.1) against the r5/r9 observed notes.
- **Repo hygiene (minor, harm-watch).** `.ufo/waves/round-18/fetch/` is
  already 8.9 MB; no single body is over 1 MiB.

## Tradeoff vs fixable

- Fixable this round: corrections 1-5.
- A tradeoff the judge must reject if left as is: crediting 6/6 as coverage
  when the only new evidence is documentary, without the saturation
  declaration (correction 4).

Labs are disposable: `/tmp/criticc2-lab`, `/tmp/criticc2-clone`. Tool
installs: none.
