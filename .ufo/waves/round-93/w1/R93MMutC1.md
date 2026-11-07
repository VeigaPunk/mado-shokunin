# R93MMutC1 — C1 frozen mutant set (round 93, w1)

Seat `R93MMutC1`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision
`4c6f723f3dca3a26f9d14475d695fe797e2e972c`. Every run below is **DRAFT** (`--draft`-class
instrument, no receipt written): none of it is a measurement.

Owned and written:

- `.ufo/waves/round-93/controls/portal-mutants-r93.json` — sha256 `a923ef4723ec72475859eaac399beacb86924ef01db0f9019cbf626854e66181`
  (74 frozen mutants, 9 `equivalent_not_counted`, 3 `not_counted_survivors`).
- this report.

## 1. Anchors (the candidate moved twice while this seat ran)

| what | sha256 |
|---|---|
| candidate at dispatch (declared) | `89039e30d329bee82f20c4a32edc9fa72c02774c98364017e131a372c9fb91d3` (= round-92 `build/mado-portals.d1.py`) |
| candidate after the L1's 00:23 patch (NUL C-string view) | `849df12c451e7e9159dad0ee7ceec1e66791a3b69d6e3b8a1f5f85253d6a6e49` |
| **candidate the frozen set is anchored to** (L1 patch 00:26: extra selftest checks) | `e46a861e6a8ab62e26671169e201b953ca629a3861c6dddc74fd89b73b2ac021` |
| frozen case file `.ufo/waves/round-93/controls/portal-cases-r93.json` (364 cases) | `c6fa989ab3888546bed330ff8c9000fb465f6c1d41e910411c144b571e8990c8` |

The candidate changed **during** a running sweep (00:23): the pristine copy hashed `89039e30`, the
restored copy at the end of the same run hashed `849df12c`, so that run intermixed two tool byte
strings. It is discarded as evidence; every number below is from a run whose pristine and restored
copies hash `e46a861e…` and score identically. Any further candidate edit moves the anchors M27/M29/
M31/X01/MB14/MC01–MC05 (the lines the NUL patch introduced) and needs re-anchoring; the other 71
probed mutants sit on bytes the port left alone.

## 2. Detector (same bounded behavioural detector for pristine, each mutant and restored)

`quality/counters/c1-r90-portal-routing.py`'s detector, re-implemented in scratch
(`R93MMutC1/detector.py`): public CLI `python3 -I <tool> --json` inside `bwrap --unshare-all
--clearenv` (LC_ALL=C), read-only `/usr` with `/usr/lib/xdg-desktop-portal`, `dbus-run-session` and
`dbus-daemon` masked, per case; a case is correct iff all 21 interfaces match the oracle's
`picks` **and** `reasons` (`none-key`/`no-backend` read as "no decision line"); `crash` = nonzero
exit or no JSON (not a kill, QUALITY 148). Fixtures are written as **bytes**
(`text.encode("utf-8","surrogateescape")`), which the round-90 counter/oracle do not do
(R92MExecD1 §Caveat); a lone surrogate in a case file is one raw non-UTF-8 byte.

Labels: `portal-cases-r93.json` (364 = 229 round-90 + 71 byte + 64 review) is labelled and pinned in
the file itself. The 71 byte cases and the 64 review cases were also labelled independently in
scratch with `controls/portal-oracle-r93.py` (bytes-aware; `PORTAL_ORACLE cases=71 incomplete=0` and
`cases=64 incomplete=0`, both rc 0, both `host_tail_sha256=4a4cf319…fbf9`); those scratch label
files were only cross-checks and are cited here, never written under `receipts/`.

Baseline: candidate `e46a861e…` answers **364/364** frozen cases (0 wrong, 0 crash); the restored
copy re-scores 364/364 and is byte-identical to the pristine copy.

## 3. How the set was built

**(a) Round-90 set carried forward.** 60 `mutants` + 5 `equivalent_not_counted`.

* Against the **declared** candidate `89039e30`, the stale anchors were exactly 7 — M03, M27, M31,
  M37, X04, X05, X06 (the item says "8"; M29 and X01 were intact at that sha because they shared the
  old `return s[j + 1:].strip(" \t") == ""` line).
* After the L1's NUL patch, M29 and X01 also went stale (that line became the `_next_char` scan), so
  **9** anchors were re-anchored in total, each flipping the same modelled rule:

| id | rule | find (current bytes) | replace |
|---|---|---|---|
| M03 | value trailing whitespace stripped | `value = s[eq + 1:].lstrip(ASCII_SPACE)` | `value = s[eq + 1:].strip(ASCII_SPACE)` |
| M27 | key names not chomped | `key = v[:eq].rstrip(ASCII_SPACE)` | `key = v[:eq]` |
| M29 | group line with trailing text accepted | `    return p >= len(s)` | `    return True` |
| M31 | duplicate key keeps the first value | `grp[key] = value.split("\x00", 1)[0]` | `grp.setdefault(key, value.split("\x00", 1)[0])` |
| M37 | Encoding compared case-sensitively | `value.encode("utf-8", "surrogateescape").lower() != b"utf-8"` | `value != "UTF-8"` |
| X01 | form feed tolerated after a group header | `while p < len(s) and s[p] in " \t":` | `while p < len(s) and s[p] in " \t\f":` |
| X04 | form feed not skipped as leading whitespace | `while i < len(raw) and raw[i] in ASCII_SPACE:` | `while i < len(raw) and raw[i] in " \t\n\r":` |
| X05 | tab not chugged from a value | `value = s[eq + 1:].lstrip(ASCII_SPACE)` | `value = s[eq + 1:].lstrip(" ")` |
| X06 | locale-suffixed key voids the file | `loc = …` + `if len(loc) > 2 …` | inserts `if "[" in key: raise KeyFileError(…)` |

**(b) Byte-class mutants added (R93MMutC1, `origin` in the file).** 15 frozen:

| id | rule flipped | killed by |
|---|---|---|
| MB01 | `ASCII_SPACE` gains `\v` (0x0B read as space again) | d1-b1-vt-before-group |
| MB02 | `_check_utf8` removed from `string_list` | d1-a5-nonutf8-config-read-key |
| MB04 | descriptor reader decodes strictly | d1-a3-nonutf8-comment-portal |
| MB05 | config reader decodes strictly | d1-a1-nonutf8-comment-config |
| MB10 | `_check_utf8` looks only at the first character | d1-a5-nonutf8-config-read-key |
| MB12 | config reader decodes `errors="replace"` | d1-a5-nonutf8-config-read-key |
| MB13 | descriptor reader decodes `errors="replace"` | g93-portal-group-bracket-cont |
| MB14 | key chomp loses `\f` | b93-ws-ff-before-equals |
| MB15 | value chug loses `\f` | b93-ws-ff-after-equals |
| MB16 | leading line strip loses `\r` | b93-ws-cr-before-key |
| MC01 | line view not cut at NUL | r93-nul-config-group-trailer |
| MC02 | stored value not cut at NUL | r93-nul-config-value-tail |
| MC03 | group-name scan ends at the first `]` | r93-nul-group-trailer-bracket |
| MC04 | continuation bytes not skipped after `]` | g93-group-bracket-cont80 |
| MC05 | value cut at NUL before the Encoding check | r93-encoding-nul-tail |

## 4. Tallies (DRAFT, candidate `e46a861e…`, 364 frozen cases)

- **killed 74 / 81 probed**, all with a well-formed wrong answer (no kill is a crash).
- **equivalent_not_counted 9**: M07, M11, X28, X22, X30 (round-90 arguments carried; X22 find+replace
  re-anchored to the current `grp[key] = value.split("\x00", 1)[0]` line) plus MB03, MB07, MB08, MB09.
- **not_counted_survivors 3** (must not be frozen): X19, MB06, MB11.
- **crash-class 2** — X19 crashes on `mc-n19-unterminated-group` (1 crash; `ValueError: substring not
  found` at `s[1:s.rindex("]")]`, reproduced), MB06 crashes on `r93-encoding-invalid-first-group` and
  `r93-encoding-later-group` (2 crashes). With those two excluded, the sweep produced **0 crashes**.
- Killing case per mutant is in the JSON's provenance via this table (all 74):

```
M01 d01-host-replica            M02 d12-desktop-invalid-token-file-ignored  M03 g03-trailing-space-value
M04 g08-escape-s                M05 d01-host-replica            M06 n06-iface-none-with-backend-first
M08 n04-iface-key-beats-default-none  M09 d01-host-replica      M10 n05-None-capital-is-a-name
M12 u01-gtk-by-dbusname-not-filename  M13 s01-default-star      M14 p08-name-order-uppercase-first
M15 x02-user-iface-override     M16 f01-desktop-file-without-preferred     M17 a07-settings-key-suppresses-default
M18 x12-settings-none-after-collect    M19 d01-host-replica      M20 x06-dup-source-data-home-wins
M21 g09-invalid-escape-voids-file      M22 g10-key-before-group-voids      M23 f03-empty-preferred-group
M24 x09-data-home-config        M25 p02-foreign-interface-voids         M26 p05-dotted-basename
M27 g01-spaces-around-equals    M28 g04-crlf                    M29 g15-group-trailing-garbage-voids
M30 p01-invalid-dbusname-skipped       M31 g06-duplicate-key-last-wins     M32 d06-desktop-two-hypr-first
M33 x02-user-iface-override     M34 w01-usein-invalid-escape-default    M35 mc-n02-double-cr
M36 w10-final-cr-no-lf-value    M37 w06-encoding-utf8-lower-ok          M38 w08-encoding-in-later-group-ignored
X01 mc-n01-ff-after-group       X04 mc-n04-ff-leading-ws        X05 mc-n05-tab-after-equals
X06 mc-n06-locale-key-inert     X07 mc-n07-locale-key-chars     X08 mc-n08-nonascii-desktop
X09 mc-n09-empty-desktop-token  X10 mc-n10-sort-both-match      X11 s01-default-star
X12 mc-n12-plain-escape         X13 mc-n13-busname-256          X14 mc-n14-bad-iface-name
X15 mc-n15-empty-iface-element  X17 mc-n17-default-case-key     X18 g09-invalid-escape-voids-file
X20 mc-n20-empty-group-name     X21 mc-n21-group-control-char   X23 mc-n23-star-prefix
X24 k01-iface-key-kde-filechooser      X25 a05-settings-dup-entries    X26 a06-settings-usein-all
X27 d06-desktop-two-hypr-first  X29 mc-n29-tab-escape           MB01 d1-b1-vt-before-group
MB02 d1-a5-nonutf8-config-read-key      MB04 d1-a3-nonutf8-comment-portal       MB05 d1-a1-nonutf8-comment-config
MB10 d1-a5-nonutf8-config-read-key      MB12 d1-a5-nonutf8-config-read-key      MB13 g93-portal-group-bracket-cont
MB14 b93-ws-ff-before-equals    MB15 b93-ws-ff-after-equals     MB16 b93-ws-cr-before-key
MC01 r93-nul-config-group-trailer        MC02 r93-nul-config-value-tail          MC03 r93-nul-group-trailer-bracket
MC04 g93-group-bracket-cont80   MC05 r93-encoding-nul-tail
```

## 5. Findings routed to the L1 (no contract change made)

1. **X19 is now crash-shaped, not killable.** The NUL patch put `s[1:s.rindex("]")]` behind
   `_is_group_line`; a mutant that accepts an unterminated `[group` line reaches `rindex` and raises
   `ValueError: substring not found` (uncaught → rc 1). QUALITY 148 says a crash is not a kill, so X19
   is out of the frozen set (`not_counted_survivors`). The rule remains covered by M29 and by case
   `mc-n19-unterminated-group`, which the candidate passes.
2. **MB06 (Encoding compare without surrogateescape) is inadmissible, not merely unkilled.** Its only
   observable difference is `UnicodeEncodeError` on a non-UTF-8 Encoding value (it crashes on
   `r93-encoding-invalid-first-group` / `r93-encoding-later-group`). It cannot be frozen under QUALITY
   148 whatever cases are added.
3. **MB11 is a real coverage gap with a concrete fix.** Narrowing `_check_utf8` to 0x80–0xF4 survives
   because the only 0xF5–0xFF read value (`b93-aff-config-readkey`, `default=kde\udcff`) falls to
   gtk-last-resort either way. A distinguishing case: `FileChooser=kde\udcff` + `default=gnome` with a
   gnome backend implementing FileChooser (candidate voids the config → gtk-last-resort; mutant keeps
   it → gnome/default-config). Not added here: R93MExecCasesC1 owns the case file.
4. **plain_string and locale classes are structurally unobservable through routing.**
   `_check_utf8` on DBusName (MB03) and every locale-suffix variant (MB07/MB08/MB09) cannot change a
   pick: an invalid-UTF-8 DBusName fails `is_bus_name` anyway, and the readers never strip a locale
   suffix, so a kept `x[C]`/`x[en]` never matches `x`. They are documented as equivalents, not claimed
   as coverage — consistent with R92MExecD1 §(d).
5. **Candidate drift under a concurrent wave.** The candidate changed at 00:23 and again at 00:26
   while this seat was sweeping (see §1). A mutant set anchored to a moving target silently becomes a
   `SETUP_ERROR find occurs 0 times` at measurement. The L1 should freeze the candidate bytes and this
   file in the same commit.
6. **The item's "8 stale" is 7 at the declared sha** (M03 M27 M31 M37 X04 X05 X06); M29/X01 went stale
   only with the NUL patch. Recorded so the next round's delta line is exact.

## 6. Commands run (all DRAFT; scratch `S=$HYAKU_SCRATCH/mado-r93/R93MMutC1`, TMPDIR="$S")

1. `python3 build_mutants.py mutants-draft.json` → `BUILT mutants=69 not_once=[]`, rc 0.
2. `python3 run_mutants.py mutants-draft.json results-draft.json` (245 = 229+16 cases) → rc 0;
   `BASELINE cases=245 ok=245 … sha=89039e30…`, `RESTORED … same_as_baseline=True`.
3. `portal-oracle-r93.py --cases portal-bytes-cases-r93-unlabelled.json --label r93-labelled.json` →
   rc 0, `PORTAL_ORACLE cases=71 incomplete=0`.
4. candidate `89039e30` on those 71 → 71 ok / 0 wrong / 0 crash.
5. `run_mutants.py mutants-draft2.json` on 316 → rc 0; 66 killed / 7 survived / 0 crashes.
6. `run_mutants.py mutants-draft3.json` on `portal-cases-r93.json` (300 cases at the time) → rc 0 but
   **invalid**: pristine `89039e30`, restored `849df12c` (candidate drifted mid-run, §1).
7. `build_mutants.py mutants-draft4.json` after re-anchoring → `BUILT mutants=76 not_once=[]`, rc 0.
8. `portal-oracle-r93.py --cases portal-review-cases-r93-unlabelled.json --label review-labelled.json`
   → rc 0, `PORTAL_ORACLE cases=64 incomplete=0`.
9. candidate `849df12c` on those 64 → 64 ok.
10. `run_mutants.py mutants-draft5.json` on 428 (364 + the 64 review cases twice) → rc 0, baseline
    `e46a861e` 428/428, 73 killed.
11. `run_mutants.py mutants-draft5.json` on 364 → rc 0; `BASELINE cases=364 ok=364 … sha=e46a861e…`,
    `RESTORED … ok=364 same_as_baseline=True`; 73 killed / 7 survived.
12. `build_mutants.py mutants-final.json` (MB16 restored; the MC edit had dropped it) →
    `BUILT mutants=81 not_once=[]`, rc 0.
13. `run_mutants.py mutants-final.json` on 364 → rc 0; `BASELINE … 364/364`, `RESTORED …
    same_as_baseline=True`, **74 killed / 7 survived / 2 crash-class mutants**.
14. `assemble.py …` → `WROTE … mutants=74 equivalent=9 survivors=3`, rc 0; every `find` in `mutants`
    and `equivalent_not_counted` occurs exactly once in `e46a861e…` (validated, rc 0).
15. `run_mutants.py <the written portal-mutants-r93.json>` on 364 → see §7.

Installs: none (pacman transactions paused host-wide by the orchestrator ruling; nothing was needed —
`bwrap`, python 3.14.8 and the round-93 oracle were already present).

## 7. Deliverable self-check

The written `portal-mutants-r93.json` was re-run as an artifact (not from the draft) against the 364
frozen cases: 74/74 frozen mutants killed, 0 survived, no crash-only mutant, baseline and restored
both 364/364 from the same bytes (`e46a861e…`).

Scratch `/fast/scratch/hyaku/mado-r93/R93MMutC1` was deleted on exit after the cited outputs were
copied into this report; no file outside this seat's write scope was touched.
