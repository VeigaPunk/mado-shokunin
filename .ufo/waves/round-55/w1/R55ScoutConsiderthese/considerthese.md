# R55 scout — considerthese 2026-10-25 / 2026-10-26 against the round-55 frozen work

Seat: R55ScoutConsiderthese (leaf; no dispatch). Read-only. `considerthese/*.md` not edited.
Frozen work in scope: C1 (keyboard repeat/numlock entry), C2 (`tools/mado-kbdopts.py`), C3 (append-only P19 correction), the freeze-order checker (mistake-fix item, not a claim).

Sources read: `considerthese/2026-10-26.md` (lines 45-52, "Self-improvement suggestions (proposals only; not acted on)"), `considerthese/2026-10-25.md` (lines 44-51, same header), `.ufo/waves/round-55/claims-frozen.md`, `.ufo/waves/round-55/registration.md`.

Caveat on the header: both sections are labelled "not acted on", but the repo records a mining for 9 of the 12 items (section 2). The labels are stale; the per-item status below is from the repo, not from the header.

## 1. Proposals marked "proposals only; not acted on" (12 items)

Each item: line 1 = can this round's frozen work honestly implement or evidence it; line 2 = repo status (grep and file reads, not the header).

**26-1 · privacy check on new receipts** (`2026-10-26.md:47`)
- Frozen work: no. No C1–C3 counter or the freeze-order checker scans receipts for home paths, keyring or ssh names. Observed: the committed pin `fetch/host-input.conf` is byte-identical to live `~/.config/hypr/input.conf` (`cmp` SAME_BYTES, 1584 B) and has no `/home` or `vgpnk` string, but that is host config, which the proposal's shape list does not target.
- Repo: mined in r45 (`lessons/round-45.md:81` → `quality/check-session-material.py` + QUALITY 85); admitted in r50 with the same-day scan half still open (`lessons/round-50.md:48-51`); r48 `M48-8` measured the gate missing 16 of 19 synthetic shapes and scanning `.ufo/` only.

**26-2 · running ledger of live-state tools** (`2026-10-26.md:48`)
- Frozen work: partly. C2 adds one live-state tool (`tools/mado-kbdopts.py`), so it needs a ledger row. No C1–C3 counter records last-live-run freshness: the C2 harness runs on committed pins, including `fetch/host-input.conf` and `fetch/host-getoption.json`.
- Repo: a draft ledger was refused in r47 (`lessons/round-47.md:336`); `quality/tool-ledger.md` + `quality/check-tool-ledger.py` landed in r51; r51 says freshness "remains open" (`lessons/round-51.md:20`).

**26-3 · track routed defects until they close** (`2026-10-26.md:49`)
- Frozen work: no. The freeze-order checker reads freeze-commit and wave-registry times, not routed items.
- Repo: mined in r46 as QUALITY 90 (`corpus/QUALITY.md:454-459`, `w1/ScrRoutedAges/ages.md`); r53 mined it again and says it "does not claim a general age-tracking ledger" (`lessons/round-53.md:34`).

**26-4 · re-run one tool myself, read-only** (`2026-10-26.md:50`)
- Frozen work: yes, but only C2, and only after C2 reaches TARGET_MET. Its inputs are `~/.config/hypr/input.conf` and `hyprctl getoption … -j`, both on this seat's host allowlist; `registration.md:62-63` says the tool reads only the named files, starts no process, opens no socket and writes nothing. Caveat: the frozen fixture F02 reads committed copies, so a live re-run is a separate act.
- Repo: no mining record found (grep for `2026-10-26` with "proposal 4" and for "re-run … tool … myself": zero hits). Earlier live tools are not re-runnable by this seat: `tools/mado-options.py:10` walks `DIR/.config/hypr/hyprland.conf` and the sourced tree, which is outside the allowlist.

**26-5 · report the domain-to-meta ratio daily** (`2026-10-26.md:51`)
- Frozen work: no. C1 is one domain entry and C2/C3 are a tool and a correction; no frozen daily ratio exists in the round.
- Repo: same ground as 25-1 (below): QUALITY 82 and `quality/ratio-domain-meta.py`. The daily-number habit is not evidenced.

**26-6 · lead with round-level outcomes** (`2026-10-26.md:52`)
- Frozen work: no. This is reflection format; no counter can check it.
- Repo: mined in r48 as QUALITY 99 with `quality/check-round-outcome-first.py` (`lessons/round-48.md:186-187`).

**25-1 · track the domain-versus-meta ratio as a running number** (`2026-10-25.md:46`)
- Frozen work: no; same as 26-5.
- Repo: mined in r44 as QUALITY 82 with `quality/ratio-domain-meta.py` (provenance `ratio-domain-meta.py:4`; `lessons/round-44.md:248`).

**25-2 · count dead attempts and dirty closures from the watchdog digests** (`2026-10-25.md:47`)
- Frozen work: no. The freeze-order checker reads the same class of input (wave-registry `createdAt` against freeze-commit committer time) but counts neither attempts nor dirty closures. Shared input, no shared claim.
- Repo: mined in r40 as a table (`lessons/round-40.md:146-149`) and in r43 as `M43-6`, which became QUALITY 81 (`corpus/QUALITY.md:409`, attempts from driver `launch` lines, dirty half a null channel).

**25-3 · watch M37-5 by name** (`2026-10-25.md:48`)
- Frozen work: no. C2's `ctl/lookup-committed.py` is a lookup-table control of the same class, but it does not discharge M37-5, which concerns the round-37 counters.
- Repo: mined in r38 (`.ufo/waves/round-38/w1/reports/ScoutConsiderThese.md`, item 3, verdict COVERED with a finding) and served by the r39 C1 re-registration (`lessons/round-39.md:80-82`). Its premise ("round 38 may land it") is already past.

**25-4 · ask whether `mado-eventq.py` should run on a schedule** (`2026-10-25.md:49`)
- Frozen work: no. The only route to visible drops is enabling logs (`debug:disable_logs`), which is a host config change; the seat allowlist forbids it and no C1–C3 claim touches eventq.
- Repo: no mining record found (grep for the proposal and `debug:disable_logs` finds only the r37/r38 fact lines). Unmined by this grep.

**25-5 · verify one fact first-hand per day** (`2026-10-25.md:50`)
- Frozen work: partly. The counters prove quote identity at a pin line, not that a sentence is entailed by its quote (`claims-frozen.md:32-34`). A first-hand open by this seat: `sed -n '1282,1283p' fetch/Hyprland-InputManager.cpp` prints `pKeyboard->m_repeatRate  = std::max(0, REPEATRATE);`, which matches the frozen anchor, and `sha256sum -c fetch/SHA256SUMS.txt` returns OK on all ten pins.
- Repo: mined in r41 as QUALITY 76 (`lessons/round-41.md:277`); its precursor 24-5 was mined in r33 (`lessons/round-33.md:28-30`).

**25-6 · shorten the window to what is new** (`2026-10-25.md:51`)
- Frozen work: no. Editorial format; no counter.
- Repo: no mining record found.

## 2. Cheapest single in-province item to mine this round: 26-4

Pick: **26-4, "re-run one tool myself, read-only"**, mined as one paragraph in this round's lesson and nothing else. It is the only unmined item that round 55 can ground without a host write, a new config read or new code.

Located quotes (what 26-4 points at):
- `.ufo/waves/round-55/registration.md:62-63`: "`tools/mado-kbdopts.py` — read-only; reads only the files named by `--config` and `--getoption`; starts no process, opens no socket, writes nothing."
- The seat host allowlist (this brief): `~/.config/hypr/input.conf`; `hyprctl getoption input:repeat_rate|input:repeat_delay|input:numlock_by_default -j`; `hyprctl devices -j`; `hyprctl version`. The `input.conf` bytes match the committed pin (`cmp` SAME_BYTES).
- Contrast, the existing live tool: `tools/mado-options.py:10`: "graph of DIR/.config/hypr/hyprland.conf depth-first in line order" — reads files outside that allowlist, so this seat cannot re-run it.

Why this one is cheapest: it needs no new code (the frozen contract text is the evidence), no host write, and no read beyond the allowlist. The other candidates cost more: 25-4 needs a log-config change the host forbids; 26-1's open same-day half needs the gate repaired first (M48-8: 16 of 19 synthetic shapes missed); 25-5 is already mined (QUALITY 76).

Limit to state in the lesson: the re-run is evidence only after C2 reaches TARGET_MET, and the frozen harness reads committed copies. Until a live run, the lesson must say the host numbers are relayed from `fetch/`.

## 3. Defects and ambiguities

1. Stale header on both files: "proposals only; not acted on" is wrong for 9 of 12 items (mined: 26-1, 26-2, 26-3, 26-5, 26-6, 25-1, 25-2, 25-3, 25-5). Not edited (operator file).
2. Duplicates: 26-5 restates 25-1, and 25-5 restates 24-5. Both pairs were counted as separate proposals in the files.
3. 25-3's premise is stale: its "check whether round 38 lands it" happened in r38 and was closed in r39.
4. "Unmined" for 25-4, 25-6 and 26-4 is from grep only (pattern `considerthese/2026-10-2[56]`, the proposal number, and key terms). Not exhaustive across `.ufo/waves/`.
5. Observed for L1 (not a claim): the committed `fetch/host-input.conf` is a host-config copy in a repository the file itself calls public. The privacy gate's home-path shapes do not flag it; whether that matters is an L1 decision.

## 4. Not verified

- Did not run `mado-kbdopts.py` (not built) or `check-session-material.py` (not a claim of this seat).
- Did not run any `hyprctl` command beyond the allowlist; did not read any hold-out path.
- QUALITY numbers were taken from the grep lines shown; each was read at the cited line, not re-derived.
