# R54Seat09 — C2 prose reconnaissance (scribe, wave 1)

- Seat: `R54Seat09` · role `scribe` · wave `w1` · round 54 · 2026-10-27
- Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin` · base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`
- Assignment (item 9): *Source/lesson prose reconnaissance: verify opened uwsm pins and frozen C2 quotations from committed files, identify host join evidence limits, report exact quote/lines; do not draft committed entry.*
- Attacked predicate: **PRED-C2-r54 clauses (b) and (c)** (`claims-frozen.md` § C2), against the **C2 fixture inventory** of `registration.md` (rows S375–S377, frozen host set).
- Nothing in the lane was edited by this seat. No counter was built or run (C2 counter does not exist at base). No host read, no network, no git/jj mutation, no delegation.

## 0. Lane state observed at recon time

```
$ git rev-parse HEAD
e25149fec8152a3aabd2b18a0ee8663b23cf65aa
$ git status --porcelain
 M corpus/README.md
 M corpus/SOURCES.md
?? .ufo/waves/round-54/
?? corpus/knowledge/uwsm-app-environment-r54.md
$ sha256sum corpus/knowledge/uwsm-app-environment-r54.md corpus/SOURCES.md corpus/README.md
5a23af426b3db1eac4f05e0b84150c4f3d63dbd5fb320b67a04d12b523cdd3f1  corpus/knowledge/uwsm-app-environment-r54.md
fc2d79fee3e298a3c05abdad98205421bebfe31e71bec7c7c02c0de8d6dc983d  corpus/SOURCES.md
8f13d30f6de7fdef13a61578bec3128d3885f0d0434351b1c03441bf16096d4d  corpus/README.md
```

The C2 entry (`corpus/knowledge/uwsm-app-environment-r54.md`, mtime 14:07, 2,229 B) and the README/SOURCES edits **appeared in the working tree during this recon**; `git status` was clean apart from `.ufo/waves/round-54/` when this seat started. They are **untracked/uncommitted**, i.e. not this seat's writes and not "committed files". All quote verification below is therefore against (i) the working-tree pins in `.ufo/waves/round-54/fetch/` and (ii) the `HEAD`-tracked registry/index for the base state.

Base mechanical state (confirms `claims-frozen.md` "Before"):

```
$ git show HEAD:corpus/README.md | grep -cE '^\| `knowledge/'
69
$ git show HEAD:corpus/SOURCES.md | grep -oE '^\| S3[0-9][0-9]' | tail -1
| S374
$ git ls-files .ufo/waves/round-54 | wc -l
0
$ git ls-files .ufo/waves/round-52/fetch | wc -l
6
```

Working tree now shows 70 index rows (`grep -cE '^\| `knowledge/' corpus/README.md` → `70`) and rows S375–S377 at `corpus/SOURCES.md:325-327`; README index row at `corpus/README.md:82`.

## 1. Pins: presence, bytes, hashes, commit pin

```
$ cd .ufo/waves/round-54/fetch && sha256sum uwsm-0.27.1-README.md uwsm-0.27.1-main.py uwsm-0.27.1-uwsm-app.1.scd
1874fb8368f6956ebdadd1db0780ea26104f3dd3bf95cca4609ab7c77c9b597a  uwsm-0.27.1-README.md
7dd6363244c101c7a0e7641684e29b6a13905e98f9fc3a4c81421e536a976c72  uwsm-0.27.1-main.py
3982503d6445017eb55e9b68446c422b0a07a45a5d9a471b02ecc4cdb8a6f5eb  uwsm-0.27.1-uwsm-app.1.scd
$ wc -c uwsm-0.27.1-README.md uwsm-0.27.1-main.py uwsm-0.27.1-uwsm-app.1.scd
 49717 uwsm-0.27.1-README.md
199361 uwsm-0.27.1-main.py
  2309 uwsm-0.27.1-uwsm-app.1.scd
```

- All three recomputed digests equal the committed `SHA256SUMS.txt` rows **and** the sha256 cells carried by the landed S375–S377 registry rows. Byte counts equal `fetch/README.txt`'s table (49,717 / 199,361 / 2,309). Holds.
- Commit pin `0727985c9bae655bda488f87f99ea69a6ac1c003` appears in `fetch/README.txt`, in all three landed `source` URLs, and in all three landed `anchor` cells. Internally consistent. **The upstream identity of that commit (that it is tag `v0.27.1`) was not re-verifiable offline** — network reads are outside this seat's fence. `[INFERENCE]` only from `fetch/README.txt`.
- Pins are **not committed**: `git ls-files .ufo/waves/round-54` → `0`, versus `6` for the round-52 C1 pin set. See F6.

## 2. Frozen C2 quotations — verbatim test matrix

Test: exact substring occurrence in the named pin under three normalizations — `raw` (byte-exact), `nl` (interior `\n`+indent → one space, the only normalization `registration.md` authorizes, and only for C1), `nl+emph` (`nl` plus removal of `*` and `` ` ``).

```
#### FROZEN registration quotes
S375 words=24 pin=uwsm-0.27.1-README.md
   raw=0 nl-collapse=1 nl+emph=1
S376 words=11 pin=uwsm-0.27.1-uwsm-app.1.scd
   raw=0 nl-collapse=0 nl+emph=1
S377 words=3 pin=uwsm-0.27.1-main.py
   raw=1 nl-collapse=1 nl+emph=1
```

Pin bytes at the located lines (`repr`, non-ASCII scan clean — no chars > U+007E, no tabs):

```
uwsm-0.27.1-README.md:117  '- Difference between environment state before and after preparation is exported'
uwsm-0.27.1-README.md:118  '  into systemd user manager (and D-Bus activation environment if reference D-Bus'
uwsm-0.27.1-README.md:119  '  implementation is used)'
uwsm-0.27.1-uwsm-app.1.scd:60  "*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon"
uwsm-0.27.1-main.py:3714   '            unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"'
uwsm-0.27.1-main.py:3716   '            unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}@{random_hex(8)}.{app_unit_type}"'
```

Readings:

- **S375 frozen quote** — 24 words (≤25 cap holds). Not byte-exact; verbatim **only** after newline-collapse, because the README hard-wraps the sentence across three lines. It **spans lines 117–119**, not 117–118 (F3).
- **S376 frozen quote** — 11 words. Not byte-exact and not verbatim even after newline-collapse, because the pin is scdoc-emphasized: `*uwsm-app*`. It becomes verbatim **only if the counter strips emphasis markers** — a transformation no frozen text authorizes for C2 (F2).
- **S377 frozen quote** — 3 words by `split()` (`unit_name`, `=`, rest), byte-exact, and **unique**: the only other near-match is line 3716, which differs by `@` before `random_hex(8)` and does not contain the frozen string. Holds.

## 3. Landed artifacts found mid-recon (not this seat's writes)

Landed teaches cells and strict verbatim test:

```
#### LANDED row quote cells
S375 words=11 pin=uwsm-0.27.1-README.md
   raw=0 nl-collapse=0 nl+emph=0
S376 words=11 pin=uwsm-0.27.1-uwsm-app.1.scd
   raw=0 nl-collapse=0 nl+emph=1
S377 words=11 pin=uwsm-0.27.1-main.py
   raw=0 nl-collapse=0 nl+emph=0
```

- `corpus/SOURCES.md:325` teaches cell: `Difference before and after preparation is exported into systemd user manager` → **0 occurrences in the pin under all three normalizations**. The pin reads `Difference between environment state before and after preparation is exported`; the cell drops `between environment state` and joins the wrap. It is a compression, not a located quote → clause (b) quote leg **fails as landed** (F1).
- `corpus/SOURCES.md:326` teaches cell: `uwsm-app client sends arguments to uwsm's app daemon via a pipe` → matches only after emphasis stripping, same single transformation as the frozen quote. Passes only under an emphasis-normalizing counter (F2).
- `corpus/SOURCES.md:327` teaches cell: `unit name includes desktop and command substrings and random hexadecimal text` → **paraphrase, 0 occurrences under all normalizations** → clause (b) quote leg **fails as landed** (F1).
- Entry prose (working tree, `corpus/knowledge/uwsm-app-environment-r54.md`):
  - `:9` — `(S375; pinned README lines 117–118)` → line range is **wrong**; the sentence ends at 119 (F3).
  - `:9` also asserts the environment difference is exported "to the systemd user manager (and the D-Bus activation environment …)" — entailed by the pin, subject to the wrap normalization above.
  - `:13` — `main.py:3714` location correct; the "eight random hexadecimal characters" gloss is an inference from the **call** `random_hex(8)`: `random_hex` is imported at `main.py:47-62` (`from uwsm.misc import (… random_hex …)` at `:59`), and **`uwsm/misc.py` is not in the pin set** (`ls .ufo/waves/round-54/fetch/` → `README.txt`, `SHA256SUMS.txt`, the three pinned files). The function body/return width is outside the three pins (F8).

Word caps on landed cells: 11 / 11 / 11 — all ≤25, no breach.

## 4. Host join evidence limits (primary finding)

Frozen host set (`registration.md` § C2): `~/.local/share/omarchy/default/hypr/autostart.conf:1..:6`, `~/.config/hypr/bindings.conf:2`, `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`.

Literal-presence test over the landed entry text:

```
#### host-join literal matches in entry: 0 / 8
    ~/.local/share/omarchy/default/hypr/autostart.conf:1 -> False | basename form: False
    … (2,3,4,5,6 likewise False / False)
    ~/.config/hypr/bindings.conf:2                -> False | basename form: True
    ~/.local/share/omarchy/bin/omarchy-toggle-idle:9 -> False | basename form: True
```

Entry `:17` reads: ``The host's read-only Omarchy default `autostart.conf` declares six `exec-once = uwsm-app -- …` launches at lines 1–6 … The user `bindings.conf:2` … `omarchy-toggle-idle:9` …`` — bare filenames, en-dash range `lines 1–6`, no `:N` anchors on the six autostart lines.

Therefore:

1. **Under the frozen literal strings the entry has 0/8 host-join matches** → clause (c) fails.
2. **Under basename normalization it has exactly 2/8** — the frozen floor, with zero margin: `bindings.conf:2` and `omarchy-toggle-idle:9`. The six autostart anchors still match nothing because the entry never writes `autostart.conf:1..6`.
3. **The counter's host-join matching rule is undefined** in both frozen files (literal full path? basename? `file:line` regex?). Two defensible readings give `0` and `2` — pass/fail flips on an unwritten rule (F4).

Truth channel for these joins does not exist in the lane:

- No committed capture of the three **host** files. The only committed omarchy default-autostart artifact is `.ufo/waves/round-18/fetch/NoteTheme/omarchy-autostart-v3.8.4.conf`, and it cannot corroborate the frozen `:1-6` set — its lines are
  ```
  1 exec-once = uwsm-app -- hypridle
  2 exec-once = uwsm-app -- mako
  3 exec-once = ! omarchy-toggle-enabled waybar-off && uwsm-app -- waybar
  4 exec-once = uwsm-app -- fcitx5 --disable notificationitem
  5 exec-once = uwsm-app -- swaybg -i ~/.config/omarchy/current/background -m fill
  6 exec-once = /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1
  7 exec-once = omarchy-first-run
  8 exec-once = omarchy-powerprofiles-init
  9 exec-once = uwsm-app -- omarchy-hyprland-monitor-watch
  ```
  i.e. line 6 is **not** an `uwsm-app` launch and `omarchy-hyprland-monitor-watch` is at line **9**. Using that pin as evidence would *contradict* the frozen `:1-6` claim; it is also upstream omarchy **v3.8.4**, not the host's installed default.
- `corpus/knowledge/hyprland-config-plane.md:30` documents a **different** file — the user `~/.config/hypr/autostart.conf` (210 B, **5** lines, 2026-10-13) — while asserting the default file starts hypridle at `:1` (`:190`). It neither captures nor anchors the frozen default `:1-6`.
- Clause (c) is **citation-presence only** ("the entry carries at least two host join citations"). No frozen clause requires the citations to be true, and no seat may read the host. The host joins are therefore an **attestation of `fetch/README.txt`'s pre-freeze L1 read** ("Host join points read-only at the same time"), not independently verifiable evidence. This is a disclosed limit, but the predicate's wording must not be read as host-truth (F5).

## 5. Distinct tests run (vs sibling scribe seats 07/08)

1. **Normalization-cost matrix** (raw / newline-collapse / emphasis-strip) applied to *both* the frozen registration quotes and the landed teaches cells, producing a per-quote minimal transformation — this is the input the counter must implement or reject.
2. **Registered location span vs actual span** (S375 `:117-118` vs 117–119; S376 `:60`; S377 `:3714`).
3. **Literal vs basename host-join matching**, quantifying the pass/fail flip (0 vs 2).
4. **`source:`-line scope test**: the entry's `source: S375–S377` names a *range*; literal `S376` occurs in the file only at entry `:9` (body), not on the provenance line. `{S375,S376,S377}` literal-presence over the whole file → all three present; over the `source:` line alone → `S376` absent (F7).
5. **Pin commitment test** (`git ls-files` r54 = 0 vs r52 = 6) — no sibling recon angle needs it, and it changes what "committed files" can mean for clause (b).

## 6. Findings

| id | severity | finding | evidence |
|---|---|---|---|
| F1 | blocking for C2 clause (b) as landed | S375 and S377 teaches cells are compressions/paraphrases, not located quotes; S375 drops `between environment state`, S377 occurs nowhere in the pin. Under any verbatim rule these two legs fail. | §2/§3 matrices; `SOURCES.md:325,327` |
| F2 | blocking for a strict counter | The **frozen** S376 quote is not byte-verbatim (`*uwsm-app*`); C2 is unsatisfiable unless the counter strips emphasis — a normalization neither frozen file authorizes (the only authorized normalization is C1's single-space newline collapse). | `uwsm-app.1.scd:60` repr; `registration.md` "Counter form" |
| F3 | registration/fixture defect | Frozen/landed location `README.md:117-118` is wrong; the quote ends on line **119** (`implementation is used)`). | §2 raw lines 117–119 |
| F4 | counter contract gap | Host-join matching rule undefined; literal full-path = 0/8, basename = 2/8 → clause (c) flips. Also `autostart.conf:1..6` never written in `:N` form. | §4 |
| F5 | evidence limit (disclosed) | Host joins are unverifiable in-lane: no committed host capture; round-18 v3.8.4 pin contradicts `:1-6`; clause (c) tests citation presence, not truth. | §4 |
| F6 | freeze completeness | The round-54 pins are untracked (`git ls-files … round-54` → 0) while round-52's are tracked (6). A `--repo . --rev <rev>` counter in C1 is evaluated against git objects; C2's clause (b) names the same pins. If the counter reads git objects at `--rev`, the pins must be committed at the scored rev; if it reads the working tree, the `--rev` contract is weaker than C1's. Neither frozen file says which. | §1 |
| F7 | clause (a) ambiguity | Entry opens `source: S375–S377` (en-dash range). If the counter tests the provenance line for the literal IDs, `S376` is missing; whole-file test passes. | §5.4 |
| F8 | evidence limit | "eight random hexadecimal characters" is an inference from `random_hex(8)`; `uwsm/misc.py` is not pinned, so the return width is outside the three pins. | `main.py:47,59,3714`; `ls fetch/` |
| F9 | mechanical consistency | Round-52 pin manifest is `SHA256SUMS`; round-54 is `SHA256SUMS.txt`. A shared digest reader must accept both names, or each counter hardcodes its own. | `ls .ufo/waves/round-52/fetch`, `ls .ufo/waves/round-54/fetch` |

No predicate was changed, no frozen file was edited. F1–F9 are report-only; the canonical judge decides.

## 7. Verified holds (positive)

- Three pin digests + byte counts + internal commit string consistency (§1).
- S377 frozen quote: byte-exact, unique at `main.py:3714` (§2).
- Word caps ≤25 on all frozen quotes (24/11/3) and all landed teaches cells (11/11/11).
- Entry provenance trio order (`source:`, `verified-at:`, `recheck:`) opens the file at lines 1–3; `verified-at: 2026-10-27` and `recheck: on-release` present.
- Registry index movement consistent with harm-watch intent: `HEAD` 69 index rows → working tree 70; last registry id `S374` → `S377`.

## 8. Out of scope / not verified

- C1 (`PRED-C1-r54`, errata counter, round-52 pins) — other seats' assignment; not touched here.
- Running any counter (`quality/counters/c2-r54-uwsm-entry.py` does not exist at base; `ls quality/counters | grep -c r54` → no r54 file).
- Host truth of the six autostart lines, `bindings.conf:2`, `omarchy-toggle-idle:9` — host reads forbidden.
- Upstream tag identity of `0727985c…` — network forbidden; internal consistency only.
- Whether the landed entry/rows stay as observed (they are uncommitted and were written concurrently during this recon).

## 9. Scratch

All commands ran with `cd` into explicit absolute paths; scratch `/fast/scratch/hyaku/mado-r54/R54Seat09` held only `qcheck.py` and `vcheck.py`, removed before yield. No filesystem writes outside this report and that scratch dir. No tools installed or updated (nothing to report).

Report trailer: `.ufo/waves/round-54/w1/R54Seat09.md`
