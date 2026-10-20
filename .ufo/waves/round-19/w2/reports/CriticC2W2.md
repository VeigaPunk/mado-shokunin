# CriticC2W2 — partial

**Verdict.** The C2 counter result holds and the S096 bytes hold. The words around them overclaim in six places:

- **Counter.** 13/13 reproduces at tip `01b80946`. The baseline is 2/13.
- **S096.** Every number in the row matches my own independent re-read of the file bytes.
- **Gate re-pin.** The PASS is honestly narrowed and the selftest exercises both pin arms.

What does **not** hold is "13/13 sourced on S096":

- Only **6/13** files cite S096 as a recorded row.
- **2/13** credited pointers say S096 is "reserved / not yet recorded / pending". That is false at the tip, and S096's own `used-by` lists both of those files.
- **5/13** cite only S090, which is a round-18 row.
- The pre-registered "and the upstream release" condition is met by **3/13**.

There are also four wording defects: SKILL says "sole version literal", which the file bytes falsify; the gate states a live-run outcome nobody observed; the gate attributes 2.17.2 to SKILL "Version pins", which still reads 2.17.0; and the gate labels the 298 L packaged config.toml as a "help table".

Axes: **F** freshness (the C2 counter), **P** provenance/honesty, **G** gate signal, **H** harm.

## 1. Re-run of the claim command

```
$ python3 -I .ufo/waves/round-19/fresh-pins.py 01b80946d92b26370d3012a7da655d00dd135154
"denominator": 13, "current": 13, "score": 10.0
$ python3 -I .ufo/waves/round-19/fresh-pins.py 9c54c56 → 2 13 ['corpus/README.md', 'corpus/knowledge/walker-route-r18.md']
$ python3 -I .ufo/waves/round-19/supersede-sweep.py 17661e0 → files=13 pointed=2 stale=11, exit 1
$ python3 -I .ufo/waves/round-19/supersede-sweep.py 01b80946… → files=13 pointed=13 stale=0, exit 0
```

- The worktree `tools/mado-verify.sh` sha256 is `1036d100…`, which equals the tip blob.
- `git diff --stat` against the tip over corpus/SKILL/tools/SCORECARD is empty.
- The SKILL registry control at `SKILL.md:573` ("17661e0 must print 11 STALE of 13") is now observed true.

## 2. S096 — independent re-read (file bytes only; nothing executed)

All of the following match the values in `corpus/SOURCES.md:108` field for field:

| Fact | Command | Observed |
|---|---|---|
| binary digest | `sha256sum /usr/bin/walker` | `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` |
| size / mtime | `stat -c '%s %y'` | `7039912`, `2026-10-08 11:14:32 -0300` |
| version literals | python `open().read()` + `re.finditer` | `2.17.2` ×1 at **856302**; `2.17.0` ×0; `2.17.1` ×0; `version2.17` at 856295 |
| context | same | `…Reloadstruct Action with 6 elementsversion2.17.2\ntoggle exact search%RES` |
| BuildID | `readelf -n` | `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99` |
| `.rodata` | `readelf -S -W` | off `0x0b6900`, size `0x074654` (856302 falls inside) |
| `.comment` | `readelf -p .comment` | GCC 16.2.1 20260810; rustc 1.99.0 (b940084d7 2026-09-28); LLD 23.1.1 |
| desc | `sha256sum`, `grep` | `5c0d9d89…0928`; `%VERSION%` 2.17.2-1; BUILDDATE 1791468872 = 2026-10-08T14:14:32Z; INSTALLDATE 1792498606 = 2026-10-20T12:16:46Z |
| packaged digest | python `gzip.open(…/mtree)` | `./usr/bin/walker … size=7039912 sha256digest=25240650…3096` (equals the on-disk binary) |
| log | `stat`, `sha256sum`, `sed -n 2929p` | 244,858 B, `27bbd0b5…6ffc`; `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)` |

On provenance:

- S096 is **opened this round**. It is absent at `9c54c56` and `17661e0` (`grep S096` on SOURCES returns nothing) and first appears at `df84807`.
- S090 dates to round 18 (`git log -S'| S090 |'` → `4c103b5 round-18: wave-1 integration`).
- The S096 row correctly refuses runtime claims (field 8): "no running-process fact is claimed — `walker --version` was not executed".

## 3. Findings

### F1 — Two credited pointers deny that S096 exists, while S096's `used-by` lists them (P; the counter credits them) — breaks "sourced on S096"

- **The pointers.** `corpus/knowledge/remaining-planes-census.md:338` says "the binary-bytes row S096 is reserved and not yet recorded". `corpus/knowledge/walker-live-surface.md:305` says "the host binary bytes are reserved as S096 (row pending, not re-read this round)".
- **The row exists at the tip.** `corpus/SOURCES.md:108` is the S096 row, and its `used-by` (field 12) names `corpus/knowledge/walker-live-surface.md` and `corpus/knowledge/remaining-planes-census.md`.
- **The counter credits both lines.** The `fresh-pins.py` tip output lists `remaining-planes-census.md` `pointer_lines [338, 340]` and `walker-live-surface.md` `[305]`, credited through the `S090` token on the same line.
- **What the counter proves.** Its `S###` arm (`fresh-pins.py:28`, `POINTER`) would credit these lines even if S096 were absent, so a hit proves "some row token" on the line, not "the row that supports this claim". (ReopenS096 made the same point independently; its report is `.ufo/waves/round-19/w2/reports/ReopenS096.md`.)
- **Cause.** These texts were true when the seats wrote them; the seats' w1 reports confirm the row did not exist yet (`w1/reports/PtrRemainingPlanesCensus.md:41`, `PtrWalkerLiveSurface.md:18`). Wave-1 CriticC2 §3 item 3 required S096 to land "in the same commit as the four notes that cite it". It landed, but the two "reserved/pending" clauses were never updated. Two files in the 13/13 now state something false about the register.

### F2 — "Sourced on S096" is 6/13; the pre-registered wording is met by 3/13 (P/F)

Tokens added per file, from `git diff 9c54c56 01b80946 -- <f> | grep '^+' | grep -oE '\bS[0-9]{3}\b'`:

- **S096 cited as a recorded row (6):** SKILL.md, corpus/README.md (`:137`), walker-deep.md (`:622`), walker-deep-r9.md (`:403`), walker-route-r18.md (`:328`), tools/mado-verify.sh.
- **S096 named but denied (2):** remaining-planes-census.md and walker-live-surface.md (see F1).
- **S090 only (5):** arc-synthesis.md `:392`, closeout-r11.md `:299`, config-health-report-r3.md `:1009`, waybar-walker-plane.md `:479`, waybar-walker-semantics.md `:467`. S090 is a round-18 log row, not "a SOURCES row opened this round for the host walker bytes".
- **The pre-registration** (`SCORECARD.md:1099-1105`) says every file "gains an in-file dated pointer … citing a SOURCES row opened this round for the host walker bytes … **and the upstream release**". Only SKILL.md (S073), walker-deep.md (S073) and walker-route-r18.md (S072–S079 on its head line) add an upstream-release row. That is 3/13.

The counter (`fresh-pins.py:12-15`: any `S###` on a line with `2.17.2`) is the frozen instrument, and it legitimately reads 13/13. The extra prose condition is not what the counter measures. The closure must report both numbers and must not merge them.

All five S090-only pointers are truthful. None of them claims a binary read: `arc-synthesis.md:393` routes the `25240650…` digest through walker-route-r18 and says "not re-measured here". So F2 is a scope overclaim in the claim text, not a false statement in those files.

### F3 — README's credit is incidental and was already present at baseline (F)

- `corpus/README.md` is credited only through `:44`, the round-18 index row ("Walker v2.17.2 … S072–S091"). That row is identical at 9c54c56, where `fresh-pins.py 9c54c56` already counts README as current.
- The real round-19 pointer, `:136-141`, splits its tokens across lines: `:137` has S096 but no `2.17.2`, and `:138` has `2.17.2` but no S###. It would score **0** on its own. Simulation on the tip bytes: hits `[44]`, and hits excluding `:44` = `[]`.
- `supersede-sweep.py` credits README the same way, through its span rule (`S072–S091` covers S090, `supersede-sweep.py:19-22,46`).
- README does carry an honest dated pointer, so the semantic 13 survives. But the C2 delta is **11 files moved**, not 13, and README's credit is a baseline coincidence. Wave-1 CriticC2 §1 already noted this, and the tip leaves it as it was.

### F4 — "the binary's sole version literal" is false as file bytes (P)

- `SKILL.md:1856` says "the binary's sole version literal is 2.17.2 (S096)". `:1860` says "the sole version literal `2.17.2` at file offset 856,302". `:1864` says "the 2.17.2 binary's sole version literal sits at 856,302".
- The file bytes contain 257 x.y.z occurrences (64 distinct). Non-`0.` examples include `2.12.1`, `2.2.5`, `2.3.4`, `2.8.5`, `1.99.0`, `23.1.1` and `26.4.0`. Examples: `yaml-rust2-0.10.4/src/…`, `scoped-tls-1.0.1/src/lib.r…`. The regex was `(?<![0-9.])\d+\.\d+\.\d+(?![0-9.])` over `open('/usr/bin/walker','rb')`.
- `SKILL.md:1855` correctly says "the only **walker** version literal". S096 field 8 says "no `2.17.0` literal survives". The three later bullets drop the qualifier.
- Fix: write "sole walker version literal" (the draft at `drafts/SkillPins-erratum.md:109` had "sole walker version literal").

### F5 — The gate states a runtime outcome nobody observed (G/P)

- `tools/mado-verify.sh:101-102` says "…the old pin **failed every live run** from that transaction onward."
- No live gate receipt exists after round 12. `grep -rn 'live\.walker\.version +(PASS|FAIL)' .ufo --include=*.txt` finds only `.ufo/evidence/round-12/before-live.txt:30` and `gate-live-after.txt:30` (`PASS 2.17.0 (pin matches)`). The host pause forbids live runs this round.
- "Every live run" may have been zero runs. Its truth also depends on what an unexecuted `walker --version` prints, which S096 explicitly refuses to claim.
- Fix: write "would FAIL any live run from that transaction onward [INFERENCE: no live run since round 12]".

### F6 — Pin authority: the gate cites SKILL "Version pins" for a value SKILL does not hold (P; duplicate authority)

- The pins plane at `tools/mado-verify.sh:65-67` says "walker 2.17.2 (S096 host rodata + S090 pacman.log:2929, round 19; **SKILL.md "Version pins"**)".
- `SKILL.md:23` still reads "walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified `hyprctl version`)". That is correct by design: the erratum at `SKILL.md:1856` says "the pin line names what was measured, not what is installed".
- So two pins now carry two meanings. SKILL's pin means measurement provenance and holds 2.17.0. The gate's pin means installed identity and holds 2.17.2.
- The narrowed PASS detail (`:3296`) and the comments at `:57-61`, `:3282-3287` and `:3554-3556` state the gate's meaning honestly. Only the parenthetical attribution at `:66-67` is wrong for walker.
- Fix: replace it with "SKILL.md "Version pins" for Hyprland/waybar; walker's SKILL pin stays 2.17.0 = measured version (erratum :1856)".

### F7 — The gate mislabels a dated artefact (P, low)

- `tools/mado-verify.sh:59-60` says "the 298 L packaged **help table**".
- In MADO-R3-1 (= `waybar-walker-semantics.md`, per `corpus/README.md:17`), the 298-line item is `/etc/xdg/walker/config.toml` (`waybar-walker-semantics.md:234`: "packaged default | `/etc/xdg/walker/config.toml` | 298 lines"). It is not help text.
- `:1921` ("the 298 L packaged table") and `:3286` say it correctly.
- Fix: write "packaged config.toml (298 L)".

### F8 — S096 `used-by` is incomplete (P, low)

- Field 12 lists walker-deep, walker-deep-r9, walker-live-surface, remaining-planes-census, tools/mado-verify.sh and SKILL.md.
- It omits `corpus/knowledge/walker-route-r18.md` (`:328` "file bytes, S096") and `corpus/README.md` (`:137`). Both cite S096 as a recorded row.
- It does include the two files that deny the row (F1).

### F8b — The lesson's GATE quote compresses the offset (P, low; corroborated by ReopenS096)

- `corpus/lessons/round-19.md:41` says "`/usr/bin/walker` byte 856,302: "version2.17.2"".
- My byte read puts the run `version2.17.2\n` (14 B: 856,295–856,308, LF at 856,308) at **856,295**, and the digits `2.17.2` at **856,302** (§2; search pattern `version2.17` hit 856,295). The quoted run therefore does not start at the cited byte.
- `drafts/HostWalkerBytes-row.md:16-17` keeps the precise form ("digits at 856,302, LF at 856,308"), per ReopenS096. The lesson line dropped it in compression, so this is a compression error, not a fabrication.
- Fix: write "byte 856,302: `2.17.2` (run `version2.17.2\n` starts at 856,295)".

### F9 — One selftest assertion is vacuous (G, low; code reading only)

- `tools/mado-verify.sh:1291` runs `st_not_has "WL: no row still names the old 2.17.0 pin" "$wl_out" "2.17.0"`. At that point `wl_out` holds only the WL3 (absent-binary) output: a version FAIL "not on PATH" plus the services PASS.
- On the WL1 PASS output the same assertion would fail, because the PASS detail itself contains "claims measured on **2.17.0** 2026-10-14 stay dated".
- The real coverage of the pin value comes from WL1 (a 2.17.2 stub gives PASS) and WL2 (a 2.17.1 stub gives FAIL), and that coverage holds. The `st_not_has` adds a counted assertion with no discriminating power.
- `WL0` (`:1258-1259`) compares the constant with itself. It guards against an accidental edit but is not evidence; its label correctly says "not a host read".

## 4. Gate re-pin — the ruling

**Honest in its row semantics.** Reasons:

- The PASS detail is "installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096".
- The FAIL path names both the new pin and the printed value.
- The absent binary FAILs.
- The selftest drives all three arms under a replaced PATH (`:1229-1294`), so no host walker or systemctl call is possible.
- `grep '"2\.17\.0"' tools/mado-verify.sh` = 0 code pins remain. The only `2.17.0` strings are comments and the PASS caveat, so wave-1 CriticC2's review check (b) is met.
- No regression or other tool consumes the old "pin matches" text (`grep -rn 'pin matches|live\.walker\.version' tools scripts`, excluding the gate, returns nothing).
- The re-pinned PASS remains an **[INFERENCE]**: it predicts that a live run would print `2.17.2` from the literal `version2.17.2\n`. A live run could still FAIL if the print differs. That is fail-closed, not a false PASS.

**What stops it from being fully honest:** F5 (an unobserved runtime claim in a comment), F6 (wrong attribution to SKILL Version pins) and F7 (mislabel). All three are comment text. None of them changes a row status.

## 5. What the SCORECARD row and the report must refuse to say

1. Not "the walker corpus is current" or "walker facts refreshed". The truthful form is **13/13 pointed, 0 walker facts re-measured on 2.17.2**: help text, flags, sockets, D-Bus, the `--version` print, `pacman -Qkk` and the running PID are all still dated 2026-10-14 / 2.17.0.
2. Not "13/13 sourced on S096" and not "every file cites a row opened this round". Truthful: S096 is cited as recorded in 6/13, denied in 2/13 (F1) and absent in 5/13 (S090, a round-18 row). The pre-registered "and the upstream release" is met in 3/13.
3. Not "13 files moved". 11 moved (2→13), and README's credit is the baseline `:44` index row (F3).
4. Not "`walker --version` prints 2.17.2" and not "the running walker is 2.17.2". Neither was executed or probed. S090 is a log line and S096 is file bytes.
5. Not "the gate's walker row passes" or "the gate confirms 2.17.2". No live run happened. The new PASS is an untested [INFERENCE], and the last observed live result is the round-12 `PASS 2.17.0`.
6. Not "the binary's sole version literal is 2.17.2" (F4). Write "sole **walker** version literal; zero `2.17.0`".
7. Not "selftest stub moved" as if a stub had pre-existed. The WL0–WL3 scenario is new this round (wave-1 CriticC2 §5.2: none existed at 17661e0). Say "selftest gained WL0–WL3".
8. Not "S096 independently re-opened" unless this report or another non-author re-read is cited. The lesson's GATE line (`corpus/lessons/round-19.md:41`) records an L1 re-read only. This report is a non-author byte-for-byte re-read (§2) that agrees on every field.

## 6. Smallest safe corrections

- `remaining-planes-census.md:338`: replace "the binary-bytes row S096 is reserved and not yet recorded" with "the binary bytes are recorded as S096 (file bytes; not re-read by this block)". Make the matching change at `walker-live-surface.md:305` ("reserved as S096 (row pending…)"). The blocks are same-round pointer text, so an in-place correction is acceptable. Alternatively, append a dated correction line.
- `SKILL.md:1856,1860,1864`: "sole version literal" → "sole walker version literal".
- `tools/mado-verify.sh:102`: mark the "failed every live run" statement as [INFERENCE]. At `:66-67`, scope the "SKILL.md Version pins" attribution to Hyprland/waybar. At `:60`: "help table" → "config.toml".
- S096 `used-by`: add walker-route-r18.md and corpus/README.md.
- Optional: point `:1291` at the WL1 output with a pattern that excludes the caveat (for example `"pin matches"` or `'(2.17.0 (pin'`), or drop it.

The C2 number (13/13 = 10.0000) stands as the frozen counter reads it. The corrections change only what the closure is allowed to call that number.

## Limits

- I did not run the gate in any mode, including `--selftest`. F9 comes from reading the code, not from execution, and the 443/443 count was not re-checked here.
- I did not diff walker v2.17.0 against v2.17.2 sources, and I fetched nothing from the web.
- Host reads were file bytes only: `sha256sum`, `stat`, `readelf`, python `open()`/`gzip.open()` on `/usr/bin/walker`, `/var/lib/pacman/local/walker-2.17.2-1/{desc,mtree}` and `/var/log/pacman.log`. I ran no walker, pacman, systemctl or other host operation.
- I checked whether the "reserved/pending" clauses (F1) were corrected in any wave-2 draft only against the committed tip and worktree. Wave-2 drafts that have not landed are [UNK].
- Whether a live `walker --version` prints exactly `2.17.2` is [UNK]. It is a strong [INFERENCE] from the `version2.17.2\n` rodata run, given that round 9 observed print equal to literal for 2.17.0.

## Worktree delta (observed after review; uncommitted; HEAD still `01b80946`)

At first read, the worktree equalled the tip. Afterwards, peers' wave-2 edits landed uncommitted in corpus/, SKILL.md and tools/. The findings above judge the **committed tip**. What the worktree now shows (I read it; I wrote nothing):

- **F1:** both "reserved/pending" lines are still in place. Append-only corrections follow them: `remaining-planes-census.md:347` and `walker-live-surface.md:312` ("S096 is a recorded mined row (landed in `df84807`)"). `MadoR19.ReopenS096` found the same F1 independently (its report: `.ufo/waves/round-19/w2/reports/ReopenS096.md`).
- **F4:** the original bullets at `SKILL.md:1856/1860/1864` are unchanged, and a correction is appended at `SKILL.md:1893`.
- **F5:** `tools/mado-verify.sh:105` now reads "would FAIL a live run … ([INFERENCE]; no …".
- **F6:** `:67` is reworded to put walker after the SKILL "Version pins" attribution. I did not re-judge it.
- **F7:** `:60` now reads "298 L packaged default config (/etc/xdg/walker/config.toml)".
- **F8:** the S096 used-by column is unchanged in the worktree (it still omits walker-route-r18.md and corpus/README.md).
- **F2, F3, F9:** not addressed in the worktree as far as I read.
- None of this is committed. The §5 refusals apply to whatever commit the SCORECARD row cites.

## Installs

none
