# MadoR19.AtkPtrWalkerLiveSurface — breaks

Target: the round-19 appended block in `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/walker-live-surface.md` (heading at `:303`, four bullets at `:305-308`). Tip studied: `01b80946d92b26370d3012a7da655d00dd135154`; file blob `f69b79bdd95590aff98cb620b03f90ea6af5aa53`, sha256 `3e27d415aa6ee85a3679794c87771f49488feca8393278a43f9e47ba2342a6f1`, 307 lines / 20,413 B. The worktree copy hashes to the same blob. The block entered history in `df84807` (`git log -S 'Freshness pointer (round 19, 2026-10-20)'`), unchanged by `01b8094`.

Verdict: **breaks** on one committed sentence (`:305`) and on two classifications in `:306`; the append-only discipline, the line references, and the S090 citation hold.

## Attack results by question

### (a) Were pre-existing bytes changed beyond the documented head `source:` swap? — NO (holds)

Baseline blob `9c54c56:corpus/knowledge/walker-live-surface.md` is 19,203 B, sha256 `2bbb9609283f2d81cd1240d111068205766bfedb03f9245937d23b4bb143f8eb`.

```
$ python3 - <<'EOF'
old = git show 9c54c56:corpus/knowledge/walker-live-surface.md
new = git show 01b8094:corpus/knowledge/walker-live-surface.md
EOF
old bytes 19203 new bytes 20413
new startswith old: True
new[len(old):len(old)+1] b'\n'
appended bytes 1209  sha256 1cf057cffef3279669afd63779650fd26d1272e3c66c1a3d5e61ebe601af46d7
```

Every pre-existing byte survives as an exact prefix; byte 19,203 is the newline that now terminates the former last line, and 1,209 B of block follow. `git diff --numstat 9c54c56 01b8094 -- …/walker-live-surface.md` = `8 1` (the single deletion is the old no-trailing-newline last line, rewritten identically plus `\n`).

This file has no head `source:` line at all (`grep -n '^source:'` → none in either revision), so the documented head-token swap does not apply to it. The only two files whose heads moved are the routes, confirmed in the same range: `walker-route-r18.md` S084→S098 and `theme-route-r18.md` S094→S097 (6 insertions + 1 deletion each, the deletion being the head line), both with an accompanying "Round-19 corrections (append-only)" section. No hidden pre-existing edit in the target file.

### (b) Live/runtime claims about walker 2.17.2, and un-rehash claims — one false sentence, one honest [UNK]

- `:305` "On 2026-10-20 the host package moved to 2.17.2: `/var/log/pacman.log:2929` (S090)" — **supported**. I read the line as file bytes: `[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`. S090 (`corpus/SOURCES.md:102`) records that exact line and itself warns "a log line is not a running-binary fact"; the block uses it only for the package move, so no runtime overclaim.
- `:305` "the host binary bytes are reserved as S096 (row pending, not re-read this round)" — **FALSE** (F1 below).
- `:308` "Not re-measured live this round (host pause): behaviour of the 2.17.2 binary stays [UNK]" — **true**: nothing in this round executed walker, and S096/S090 claim no running-process fact. No sentence anywhere in the block asserts a live 2.17.2 behaviour.
- The false sentence points the other way: it disclaims re-verification that was in fact performed this round.

### (c) Cited line numbers and sections — ALL CORRECT (holds)

Pre-block `2.17.0` occurrences (`git show 9c54c56:… | grep -n '2\.17\.0'`) are exactly `19, 37, 38`; line 6 is the measurement window (`Measured 2026-10-14 18:20:44–18:23:13Z on host plazir27`). Section anchors in the tip: `§1:33`, `§2:49`, `§3:107`, `§4:160`, `§7:267`. The specific objects: `§1` package list `:43` (29 entries), `§2` help sha `:52` (`ca4820a8…`), help-all/gapplication `:93-94`, `§3` L0 offset `:113` (784,064), `§3` L2 user config `:115` (1,336 B, `fecf71fa…`), `§3` GSettings `:147` and unit environment `:154`, `§4` sockets/D-Bus/layer `:162-200`, `§7` boundary table `:267-281`. Every line and section the block cites exists and matches its description.

### (d) Does every cited S### support the sentence? — S090 yes; S096 inverted (F1)

S090 supports the move sentence. S096 is cited in a parenthetical that denies its existence; the row exists at `corpus/SOURCES.md:108`, status `mined`, opened `2026-10-20`, and its `used-by` column names this very note (`…, corpus/knowledge/walker-live-surface.md, …`). See F1.

## Findings

### F1 — BREAKS: "S096 row pending, not re-read this round" is false at the integrated tip

Committed text, `walker-live-surface.md:305`: "the host binary bytes are reserved as S096 (row pending, not re-read this round)".

Evidence against:

1. The row exists at tip `01b8094:corpus/SOURCES.md:108` — `| S096 | host walker version binding — /usr/bin/walker (compiled-in rodata literal) + /var/lib/pacman/local/walker-2.17.2-1/desc + /var/log/pacman.log | … | mined | 2026-10-20 | … |` — with the binary sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096` and literal offset 856,302, and with `corpus/knowledge/walker-live-surface.md` in its `used-by` column. `S091` (`corpus/SOURCES.md:103`) independently records the same host bytes.
2. The block and the row landed in the **same commit** `df84807` (`git log -S 'Freshness pointer (round 19, 2026-10-20)' -- …/walker-live-surface.md` → `df84807`; `git log -S 'S096 | host walker version binding' -- corpus/SOURCES.md` → `df84807`). The contradiction is internal to one commit, not later drift.
3. The bytes were re-read this round, by me and by wave 1: `sha256sum /usr/bin/walker` → `2524065…d93096`; `stat` → 7,039,912 B, mtime 2026-10-08 11:14:32 -0300; `python3` `open('/usr/bin/walker','rb')` → `find(b'2.17.2') = 856302`, `find(b'2.17.0') = -1`, `b'2.17.2\n'` at 856,302. Wave-1 receipts: `HostWalkerBytes.md:20-35` (same three facts), `DeltaWalkerConfig.md` §1 (host binary `cmp`-identical to the 2.17.2 package binary).
4. The wave-1 authoring note is explicit that the deviation was a snapshot of a moment before S096 existed: `PtrWalkerLiveSurface.md:18` — "No such read happened this round, and `grep -n "S096" corpus/SOURCES.md` returns no row (S096 is reserved only)." Integration then added the row without reconciling the block (the same integration re-wrote the other notes' pointers to say S096 *was* read: `walker-deep.md:622`, `walker-deep-r9.md:403`).

Consequence for C2: `fresh-pins.py` (rerun at tip) scores 13/13, score 10.0, with this file's `pointer_lines [305]` — the checker's regex `2\.17\.2.*\bS\d{3}\b` accepts the line even though its semantic claim is that S096 has no row. This is the mutant class named in `corpus/lessons/round-19.md:18` ("a bare `# S096 2.17.2` line passes"); here it is worse than bare — it contradicts the source row. For this file, C2's "sourced on S096" is mechanically credited but textually denied.

### F2 — BREAKS (classification): the §2 help/capture shas are GLib-bound, not walker-version-bound

Committed text, `:306`: "Version-bound, therefore dated to the 2.17.0 build: … §2 help text and its sha256 `ca4820a8…` with the help-all and gapplication captures".

Wave-1 measurements say the opposite about the binding:

- `DeltaWalkerCli.md:101` — the 838-byte walker option-description run is byte-identical between the released 2.17.0 and 2.17.2 binaries (same sha256 `e429efc3…`; only offsets 819,030 → 832,855 moved). The walker half of the help text did **not** change with the version.
- `DeltaWalkerCli.md:229` — the `--help` sha `ca4820a8…` is "stale by construction" because "framing comes from GLib, which moved 2.88.3→2.90.1 (`pacman.log:2554`)". I re-read that log line: `[2026-10-20T09:16:29-0300] [ALPM] upgraded glib2 (2.88.3-1 -> 2.90.1-1)` (also `gtk4 1:4.22.4-1 -> 1:4.24.1-1` at `:2641`).
- `DeltaWalkerCli.md:231` — the help-all/help-gapplication framing strings "`Show all help options` / `Enter GApplication service mode…` occur 0× in both walker binaries, 1× in host `libglib`/`libgio` 2.90.1".

So the captures are bound to the host GLib/GIO (rendered bytes = walker strings + GLib framing), not to the 2.17.0 *walker* build the block names. The practical warning ("do not treat this sha as current") remains true, but the stated cause is falsified by the round's own evidence: the changed dependency is GLib, upgraded in the same pacman transaction. Whether a fresh run's sha actually differs is `[INFERENCE]` from the source/binary split; per DeltaWalkerCli the new value is `[UNK]` without execution (forbidden by the host pause).

### F3 — BREAKS (minor classification): the 29-entry package list is version-invariant, not version-bound

Committed text, `:306`: "Version-bound, therefore dated to the 2.17.0 build: … §1 package file list (29 entries) …".

Both cached packages carry an identical payload list:

```
$ for v in 2.17.0 2.17.2; do bsdtar -tf /var/cache/pacman/pkg/walker-$v-1-x86_64.pkg.tar.zst \
    | grep -v '^\.' | sort > /tmp/pk-$v.txt; done
$ diff /tmp/pk-2.17.0.txt /tmp/pk-2.17.2.txt   → (no output) "PAYLOAD LIST IDENTICAL"
$ wc -l /tmp/pk-2.17.0.txt /tmp/pk-2.17.2.txt  → 29 / 29
$ grep -c '/$' /tmp/pk-2.17.2.txt              → 10
```

29 payload entries in both (10 dirs + 19 files, including the 16 theme files) — exactly the list shape the note pins at `:43`. Nothing about the list moved between 2.17.0-1 and 2.17.2-1; only file *contents* moved (`/etc/xdg/walker/config.toml` 13,220 B `5b4e47b7…` → 13,743 B `3c5c6867…`, which I hashed on the host: `3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b`). Lumping the invariant list under "version-bound" overstates staleness; the packaged-config half of the same clause is correctly version-bound. (The three extra tar members `.BUILDINFO`, `.MTREE`, `.PKGINFO` are package metadata, not `pacman -Ql` entries.)

### F4 — PARTIAL: the dated inventory omits the note's own §1 live-state rows

`:307` dates `§3` config/GSettings/unit-environment, `§4` PIDs/sockets/D-Bus/layer and `§7` boundary state. But the note's primary live rows sit in `§1` and are not in either bullet:

- `:39` `process | PID 1203471 /usr/bin/walker --gapplication-service, started Wed 2026-10-14 13:11:08 -03`
- `:40` `unit | … MainPID=1203471, ActiveState=active / SubState=running`
- `:42` `elephant peer | PID 1203474 …, unit elephant.service MainPID=1203474 active/running; no session-bus name`

The 2026-10-20 transaction ran `walker-restart.hook` twice (`/var/log/pacman.log:3062` 09:18:25, `:3123` 09:31:04, read as file bytes; S090 records both), so PID 1203471 and the unit `ActiveState` are plausibly stale [INFERENCE: a restart hook is not proof of a new PID]. Sibling pointers make exactly this class explicit — `waybar-walker-plane.md:481` ("Process and unit state, dated and superseded: walker PID 1808 … restart hooks … make that PID likely stale"), `walker-deep-r9.md:404`, `arc-synthesis.md:394`. The block is not literally false (it says "None of *these* is re-asserted" of its own list), but its inventory is incomplete for a note that carries live rows: nothing prevents a reader from taking `§1:39-42` as current. This is the "sweep every mention" gap of `corpus/lessons/round-19.md:18`, one level down from the file-level C2 metric.

## Independent reruns (commands and key output)

```
$ git -C … rev-parse 01b8094:corpus/knowledge/walker-live-surface.md
f69b79bdd95590aff98cb620b03f90ea6af5aa53          # == worktree git hash-object
$ sha256sum corpus/knowledge/walker-live-surface.md
3e27d415aa6ee85a3679794c87771f49488feca8393278a43f9e47ba2342a6f1

$ git show 9c54c56:…/walker-live-surface.md | grep -n '2\.17\.0'
19, 37, 38
$ git show 01b8094:corpus/SOURCES.md | grep -n 'S096 | host walker version binding'
108

$ sed -n '2929p;2554p;2641p;3062p;3123p' /var/log/pacman.log
[2026-10-20T09:16:29-0300] [ALPM] upgraded glib2 (2.88.3-1 -> 2.90.1-1)
[2026-10-20T09:16:33-0300] [ALPM] upgraded gtk4 (1:4.22.4-1 -> 1:4.24.1-1)
[2026-10-20T09:16:46-0300] [ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)
[2026-10-20T09:18:25-0300] [ALPM] running 'walker-restart.hook'...
[2026-10-20T09:31:04-0300] [ALPM] running 'walker-restart.hook'...

$ sha256sum /usr/bin/walker /etc/xdg/walker/config.toml
25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096  /usr/bin/walker
3c5c6867d0216d0c86437a9c413cff4608da514c53e50b1bc412f4965d750a8b  /etc/xdg/walker/config.toml
$ python3 -c "d=open('/usr/bin/walker','rb').read(); print(len(d), d.find(b'2.17.2'), d.find(b'2.17.0'))"
7039912 856302 -1

$ python3 -I .ufo/waves/round-19/fresh-pins.py 01b8094…
current 13 / 13, score 10.0; row walker-live-surface current=True pointer_lines=[305]
```

(Line order in the first log excerpt is ascending in the file; reproduced here by line selection. The exact line→content mapping shown above was read from the cited line numbers: 2554, 2641, 2929, 3062, 3123.)

## What holds

- Append-only: pre-existing 19,203 bytes are an exact byte prefix; no head `source:` edit in this file; only the two route files have the documented token swap.
- Line and section references: correct (19/37/38, line 6, §1/§2/§3/§4/§7, specific rows).
- S090: supports the package-move sentence and is used within its own stated scope (a log line, not a runtime fact).
- The final `[UNK]` bullet is honest and consistent with the host pause.

## Limits

- No walker, pacman, systemctl, journalctl, busctl, hyprctl or gsettings execution; host data are file bytes only (`sha256sum`, `stat`, `sed`, `bsdtar -t`, Python `open`). Help output was not rendered, so the "new sha" stays `[UNK]`; F2 rests on the committed wave-1 source/binary split (`DeltaWalkerCli.md`) plus my independent reads of `pacman.log:2554` and the packages, and the causal step "GLib 2.90.1 changes the rendered sha" is `[INFERENCE]`, not measured.
- F3's "the 2.17.2 `pacman -Ql` list is also 29" is `[INFERENCE]` from the identical payload lists, not from reinstalling the package; the note's own 2.17.0 count (29) matches the 2.17.0 payload exactly.
- "row pending" may have been true at the moment the wave-1 seat wrote it (`PtrWalkerLiveSurface.md:18` documents that intent); the judgment is on the integrated tip, where the row exists in the same commit.
- I did not audit the other twelve pointer files; `remaining-planes-census.md:338` carries the same stale "S096 … reserved and not yet recorded" wording at the tip, which corroborates that the integration failed to reconcile the two waves rather than a one-off typo, but it is outside this seat's target.
- No network fetches were made; no receipts apply.

## Installs

none.
