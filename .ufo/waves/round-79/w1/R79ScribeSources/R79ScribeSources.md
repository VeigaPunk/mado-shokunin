# R79ScribeSources — SOURCES frontier bookkeeping (round 79, wave 1)

Seat: R79ScribeSources (scribe). Lane: mado-shokunin. Round 79, ONE v1 wave.
Contract: `.ufo/waves/round-79/claims-declaration-r79.md` § Frontier step (§2b) — the frozen source of
truth for what this round opens. Freeze `5eb8f20fe291603c74973fa94cc55723ac8089a4`; base
`e4b153dfa4a67ca56f7ec65cb6639082451626a7`.

Scope of this file: prose drafts only — two registry rows, the in-place `used-by` cells, and the
census. I wrote no tracked file, ran no mutating `git`/`jj` command, took no host probe, ran no
counter, and fetched nothing from the network. Every source fact below is read from the pinned
bytes under `.ufo/waves/round-79/fetch/`; every registry fact from `corpus/SOURCES.md`.

## §0 State: what is at the freeze and what is already in the working tree

`corpus/SOURCES.md` is dirty in the working tree before this seat drafts anything:

| state | command | observed |
|---|---|---|
| freeze bytes | `git show 5eb8f20f…:corpus/SOURCES.md` (896 lines) | no `S465`/`S466`/`S467` row; sha256 `f7b9d46b4cc15706b62b36f91dab4e5ff088a4973cfda83d6e21de77381ae54c` |
| working tree | `wc -l corpus/SOURCES.md`; `sha256sum corpus/SOURCES.md` | 900 lines; sha256 `a5216b27239428a0c68f10d4130eecd364dbfea35b6eb71d0bdd799d287948c9` |
| already landed there | `grep -nE '^\| S46[567] ' corpus/SOURCES.md` | `corpus/SOURCES.md:417` S465, `:418` S466, `:419` S467; `git diff --stat corpus/SOURCES.md` → `8 insertions(+), 4 deletions(-)` |

So this seat's "two new rows" are already present as another seat's landed draft; my job is the
verification below plus the two precision repairs (F2) and the one attribution decision (F4). The
snapshot hash above is the state I measured; the file can move again as siblings integrate.

## §1 Deliverable 1 — the two rows, in the registry's 11-column shape

Shape (contract v1, `CORPUS.md` § SOURCES.md): `id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by`. Below is the row text **as verified** (one row = one line, no
`|` inside any cell). Two parentheticals here are my repair of the landed bytes — `:652-655 (quote
:654 …)` in S465's anchor and `(quote :48)` in S466's — and both are explained in F2; delete them if
the L1 wants the landed text byte-for-byte.

```text
| S465 | Hyprland v0.56.2 — src/output/Monitor.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/output/Monitor.cpp | code | A | mado compositor plane: the static reserved area a monitor rule applies and the usable box the layer plane is arranged in (round-79 C1) | applyMonitorRuleSoft :652-655 (quote :654 setStatic), logicalBoxMinusReserved :1772-1774 @ efb5099 (fetched 2026-11-04, sha256 9cf88e15…, 112738 B) | m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea); | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-reserve-r79.md |
| S466 | Hyprland v0.56.2 — src/desktop/reserved/ReservedArea.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/reserved/ReservedArea.cpp | code | A | mado compositor plane: the static band and every dynamic contribution are summed into one reserved area (round-79 C1) | calculate :43-51 (quote :48), setStatic :69-74, addType :101-112 @ efb5099 (fetched 2026-11-04, sha256 0a52e145…, 3339 B) | m_bottomRight += e.bottomRight; | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-reserve-r79.md |
```

Cell-by-cell, against the seat's requirement list:

| requirement | S465 | S466 | evidence |
|---|---|---|---|
| id | `S465` | `S466` | next unused at the freeze: the last row is `S464` at `corpus/SOURCES.md:415` in the freeze bytes, `:416` in the working tree |
| source (title — path — URL) | `Hyprland v0.56.2 — src/output/Monitor.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/output/Monitor.cpp` | `Hyprland v0.56.2 — src/desktop/reserved/ReservedArea.cpp — https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/src/desktop/reserved/ReservedArea.cpp` | URL is the pinned commit `efb5099`, not `main` |
| kind | `code` | `code` | both are source files |
| tier | `A` | `A` | primary source for the scope; tier scoped to `scope`, never global |
| scope | static reserved area + usable box (round-79 C1) | static + dynamic summation into one reserved area (round-79 C1) | distinct from S457 (arrange), S458 (reply), S459 (parent/child box) — see F3 |
| anchor | `applyMonitorRuleSoft :652-655 (quote :654 setStatic), logicalBoxMinusReserved :1772-1774 @ efb5099 (fetched 2026-11-04, sha256 9cf88e15…, 112738 B)` | `calculate :43-51 (quote :48), setStatic :69-74, addType :101-112 @ efb5099 (fetched 2026-11-04, sha256 0a52e145…, 3339 B)` | commit pin + access date + digest + size, as S457–S464 do |
| teaches | `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea);` | `m_bottomRight += e.bottomRight;` | the located quote **is** the teaches cell, the shape S457/S458/S459/S462/S464 already use for code rows |
| status | `mined` | `mined` | `mined` = cited by ≥1 path in `used-by`; the r79 entry cites both (its `source:` line) |
| opened (access date) | `2026-11-04` | `2026-11-04` | matches the anchor's `fetched 2026-11-04` |
| recheck | `on-release` | `on-release` | Hyprland after v0.56.2 |
| used-by | `corpus/knowledge/bar-footprint-reserve-r79.md` | same | the file exists (7,987 B, untracked at measurement) |

Quote verification — byte identity, location, length:

| row | quote | found | file:line | words |
|---|---|---|---|---|
| S465 | `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea);` | `grep -cF` → 1 | `.ufo/waves/round-79/fetch/S465.bin:654` | 1 |
| S466 | `m_bottomRight += e.bottomRight;` | `grep -cF` → 1 | `.ufo/waves/round-79/fetch/S466.bin:48` | 3 |

Digest and size verification (`sha256sum .ufo/waves/round-79/fetch/S465.bin .ufo/waves/round-79/fetch/S466.bin`,
compared with `fetch/sha256-r79.txt`):

| row | sha256 (full) | manifest prefix | bytes | manifest/row agree |
|---|---|---|---|---|
| S465 | `9cf88e154eb5dae676c79d37b5b055ca6134838857cecdbb89a3b747a6821927` | `9cf88e15…` | 112738 | yes |
| S466 | `0a52e145ed2bdfddfa2b2e658ef2d326a01e86b2266d8af0f015915452a6e0db` | `0a52e145…` | 3339 | yes |

Line anchors re-read in the pinned bytes (not recited):

| anchor element | file:line | content |
|---|---|---|
| `applyMonitorRuleSoft` signature | `S465.bin:652` | `bool CMonitor::applyMonitorRuleSoft(Config::CMonitorRule&& pMonitorRule) {` |
| the copy | `S465.bin:654` | `m_reservedArea.setStatic(m_activeMonitorRule.m_reservedArea);` |
| `logicalBoxMinusReserved` | `S465.bin:1772-1774` | signature, `return m_reservedArea.apply(logicalBox());`, `}` |
| `calculate` | `S466.bin:43-51` | resets to `m_initialTopLeft`/`m_initialBottomRight`, adds every `m_dynamicReserved` entry |
| `setStatic` | `S466.bin:69-74` | copies the initial box and calls `calculate()` |
| `addType` | `S466.bin:101-112` | clamped per-type accumulation + the `const CReservedArea&` overload at `:110` |

## §2 Deliverable 2 — in-place registry changes, old → new

Only the `used-by` cell changes; the contract allows `status`, `recheck` and `used-by` to change in
place, each logged old→new in the round lesson. I checked programmatically that no other cell of these
rows moved (field-by-field comparison of the freeze bytes against the working tree; the only changed
field is column 12).

| row | old `used-by` (freeze `5eb8f20f`) | new `used-by` (drafted) | entry cites it? | state |
|---|---|---|---|---|
| S457 | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md,corpus/knowledge/bar-footprint-reserve-r79.md` | yes — entry `source:` names `S457` (`:2673-2700`) | landed in working tree |
| S458 | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md,corpus/knowledge/bar-footprint-reserve-r79.md` | yes — `S458` (`reserved` print `:281-282`) | landed in working tree |
| S459 | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md,corpus/knowledge/bar-footprint-reserve-r79.md` | yes — `S459` (`:19-35`, `:53-60`) | landed in working tree |
| S461 | `corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` | **unchanged** | **no** — the entry's `source:` line does not name S461 | landed unchanged (F4) |
| S303 | `corpus/knowledge/hyprland-monitor-rule-r45.md` | `corpus/knowledge/hyprland-monitor-rule-r45.md,corpus/knowledge/bar-footprint-reserve-r79.md` | yes — `S303` (`addreserved` fields `:1319-1341`) | landed in working tree |

Why S303 qualifies — its anchor covers the `addreserved` argument mapping:
anchor `Hyprland-legacy-ConfigManager.cpp:1293-1387 handleMonitor`; the branch is
`…/Hyprland-legacy-ConfigManager.cpp:1319` (`} else if (ARGS[1] == "addreserved") {`), the mapping is
`:1323` (`area = {std::stoi…ARGS[2]), …ARGS[5]), …ARGS[3]), …ARGS[4])}` under the comment at `:1322`
(`// top, right, bottom, left`), store at `:1331`, add at `:1341` — all inside `:1293-1387`. The
constructor it feeds is `S466.bin:14-15`, `CReservedArea(double top, double right, double bottom,
double left)`, so the written field order TOP, BOTTOM, LEFT, RIGHT maps to
`ARGS[2]=TOP, ARGS[3]=BOTTOM, ARGS[4]=LEFT, ARGS[5]=RIGHT`. This is the "argument mapping" the seat
condition names.

S461 option B, only if the entry is amended to cite it: new `used-by` =
`corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md,corpus/knowledge/bar-footprint-reserve-r79.md`.
As written the entry does not cite S461, so adding it would record a citation the entry does not make
(a `reference-drift` shape). My recommendation is the landed state: unchanged.

Separator style follows the register: comma, no space (`corpus/SOURCES.md:409`). Order: the new path
appended last.

## §3 Deliverable 3 — census, at the freeze and at the drafted state

Commands are the frozen `CORPUS.md` § Census block verbatim; the only substitution is the input path
(freeze snapshot instead of the working file). Both runs used `bash`, `awk`/`grep`/`sort`/`uniq` only.

### §3.1 At the freeze

Input: `git show 5eb8f20f…:corpus/SOURCES.md` written to
`/fast/scratch/hyaku/mado-r79/R79ScribeSources/SOURCES-at-freeze.md` — 896 lines, sha256
`f7b9d46b4cc15706b62b36f91dab4e5ff088a4973cfda83d6e21de77381ae54c` (`sha256sum`).

```sh
F=/fast/scratch/hyaku/mado-r79/R79ScribeSources/SOURCES-at-freeze.md
#   = git show 5eb8f20fe291603c74973fa94cc55723ac8089a4:corpus/SOURCES.md
#   (the L1 re-runs this block with "$F" → corpus/SOURCES.md for the landed state)

# rows (spacing-tolerant)
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$F"
# malformed rows — 11 columns means NF=13; must print 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' "$F"
# tier histogram
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$F"
# status histogram
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' "$F"
# duplicate ids — must print nothing
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' "$F" | sort | uniq -d
```

| check | observed output | rc |
|---|---|---|
| rows | `401` | 0 |
| malformed rows | `0` | 0 |
| tier histogram | `A=386 B=7 C=8 ` | 0 |
| status histogram | `mined=378 queued=10 rejected=13 ` | 0 |
| duplicate ids | *(empty)* | 0 |

rc note: `grep -c` prints `0` **and** exits 1 when nothing matches, so a green rc 0 on the rows line is
itself evidence that rows exist. The duplicate-id pipeline's rc is `uniq`'s (always 0), so the empty
stdout — not the rc — is the signal. The awk histograms' key order is awk-defined; compare them as
multisets, not strings.

### §3.2 At the drafted state (working tree, unchanged by me)

Input: `corpus/SOURCES.md` — 900 lines, sha256
`a5216b27239428a0c68f10d4130eecd364dbfea35b6eb71d0bdd799d287948c9`. Same five commands with
`"$F"` replaced by `corpus/SOURCES.md`, plus the frozen enum/tier-inflation check and the
`used-by`-existence check from the same block.

| check | observed output | rc |
|---|---|---|
| rows | `404` | 0 |
| malformed rows | `0` | 0 |
| tier histogram | `A=388 B=8 C=8 ` | 0 |
| status histogram | `mined=380 queued=10 rejected=14 ` | 0 |
| duplicate ids | *(empty)* | 0 |
| enum violations / tier inflation | *(empty)* | 0 |
| mined rows whose `used-by` paths do not exist | *(empty)* | 0 |

Reconciliation: `401 + 3 = 404` rows (S465, S466 code/A/mined; S467 docs/B/rejected);
`A 386+2=388`, `B 7+1=8`, `C 8+0=8`; `mined 378+2=380`, `rejected 13+1=14`, `queued 10+0=10`. The
three new rows account for every delta.

### §3.3 The line the L1 must paste

Paste the **rows** line with its output, and the malformed line, as one command pair (this is the
minimum evidence that the registry grew by exactly three well-formed rows):

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md && awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
```

observed here: `404` then `0`. If a single line is budgeted, paste only the rows command —
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `404`. Do **not** paste the
runs above with the scratch path: substitute `corpus/SOURCES.md`, because the freeze snapshot is not a
landed file.

## §4 Findings

**F1 — the two rows are not at the freeze; they are a dirty working-tree draft.** `git show
5eb8f20fe291603c74973fa94cc55723ac8089a4:corpus/SOURCES.md | grep -nE '^\| S46[56] '` → no output;
`grep -nE '^\| S46[56] ' corpus/SOURCES.md` → `corpus/SOURCES.md:417`, `:418`.
`git status --porcelain` → ` M corpus/SOURCES.md`. Consequence: the freeze census (§3.1, 401 rows) is
the before state; any "rows grew" sentence in the report must name the after state (§3.2, 404 rows)
and the dirty tree.

**F2 — S465's anchor starts one line after the function signature.** The landed row and the entry's
`source:` line (`corpus/knowledge/bar-footprint-reserve-r79.md:3`) both say `applyMonitorRuleSoft
:653-655`; `S465.bin:652` is
`bool CMonitor::applyMonitorRuleSoft(Config::CMonitorRule&& pMonitorRule) {`, `:653` is
`m_activeMonitorRule = std::move(pMonitorRule);`, `:654` is the quoted `setStatic` line. The
declaration names the function without a line, so nothing frozen carries the offset. Recommended
repair (already applied in §1's row text): `applyMonitorRuleSoft :652-655 (quote :654 setStatic)`;
the entry's `source:` line should take the same correction when it is next touched (I did not edit it).
S466 needs only the optional `(quote :48)` marker; its three ranges are exact.

**F3 — both new rows duplicate a held row's URL and byte digest, at a separate scope.** `S465` shares
its URL and digest (`9cf88e15…`, 112738 B) with `S306` (`corpus/SOURCES.md:255`, the monitor-rule
output row); `S466` shares URL and digest (`0a52e145…`, 3339 B) with `S459` (`corpus/SOURCES.md:410`).
Command: `grep -oE '^\| S[0-9]+ \|[^|]*src/output/Monitor.cpp[^|]*' corpus/SOURCES.md | sed -E 's/^(\| S[0-9]+).*/\1/'`
→ `| S306`, `| S465`; same shape for `src/desktop/reserved/ReservedArea.cpp` → `| S459`, `| S466`.
This is the documented separate-scope pattern (precedent `S451`/`S447`, `S452`/`S448` in the round-74
note) and will print the maintained parser's `W04` duplicate-URL warning; the frozen census block does
not test URLs, so §3 does not show it. Not a defect — record it in the round lesson so the warning is
expected.

**F4 — S461 was named in the seat brief but is not cited by the entry, so its `used-by` is unchanged.**
Command: `awk -F'|' '$2 ~ /^ S461 $/ {print $12}' corpus/SOURCES.md` →
`corpus/knowledge/bar-footprint-r77.md,corpus/knowledge/bar-footprint-margins-r78.md` at both the
freeze and the working tree. The entry's `source:` line names S465/S466/S457/S458/S459/S303 only
(`corpus/knowledge/bar-footprint-reserve-r79.md:3-6`). Two honest options, both in §2: leave S461
(landed) or amend the entry first. Adding the path without the citation would be a false attribution.

**F5 — `sha256-r79.txt` cannot verify its own last line.** `.ufo/waves/round-79/fetch/sha256-r79.txt:10`
records `a9806336…  .ufo/waves/round-79/fetch/sha256-r79.txt`;
`sha256sum .ufo/waves/round-79/fetch/sha256-r79.txt` → `d940cbd29f53aaf9a91553bf962cff289f4e17c2264a927d7831f73717608e28`;
`head -n -1 sha256-r79.txt | sha256sum` → `54013a03acc5670a30fa5f1b2741b1f869979db8ed3a4fcfcb9a735ca53af514`.
Neither the full file nor the file minus that line hashes to the recorded value. The two per-file
lines I relied on (S465, S466) match their bytes exactly, so nothing load-bearing here depends on the
self-line — but the manifest should not carry a self-entry it cannot satisfy. Reported, not repaired
(frozen instrument).

**F6 — the positive checks that passed (no finding, recorded as evidence).** `NF=13` for S465, S466,
S467 (`awk -F'|' '/^\|[[:space:]]*S46[567][[:space:]]*\|/ {print $2" NF="NF}' corpus/SOURCES.md`);
`grep -cF` byte-identity for both quotes; digest and size equal to the manifest; the enum /
tier-inflation and `used-by`-existence censuses empty (§3.2); the entry's citations all fall inside the
cited rows' anchors — S457 `:2673-2700` ⊂ its own anchor, S458 `:281-282` ⊂ `:281-282`, S459 `:19-35`
and `:53-60` ⊂ its anchor (read in `S466.bin`, which is byte-identical to `S459.bin` by digest), S303
`:1319-1341` ⊂ `:1293-1387`, S465 `:653-655`/`:1772-1774` and S466 `:43-51`/`:69-74`/`:101-112` as
tabled in §1. Text-level comparison only; no re-fetch.

## §5 Limits and files

Not done, by design or by bound: no tracked file written, no `git`/`jj` write, no commit, no counter
run, no network fetch (the pinned bytes are the evidence), no host probe (none was needed for
registry prose). The two rows and the five `used-by` cells are verified against
`5eb8f20f`-time bytes; the working tree is dirty and may move again as siblings integrate, so the L1
should re-run §3.3 after the last integration rather than trusting the `404` above.

Files written by this seat (all inside its bounds):

| path | what |
|---|---|
| `.ufo/waves/round-79/w1/R79ScribeSources.md` | this report (the scoped findings file) |
| `.ufo/waves/round-79/w1/R79ScribeSources/R79ScribeSources.md` | the same report, copied into the seat's write dir |
| `.ufo/waves/round-79/w1/R79ScribeSources/sources-rows-r79.append` | the two row lines only, ready to append |
| `.ufo/waves/round-79/w1/R79ScribeSources/used-by-pairs-r79.txt` | the five old→new `used-by` cells |

Scratch `/fast/scratch/hyaku/mado-r79/R79ScribeSources/` was created for the freeze snapshot and is
deleted before this seat finishes; the freeze input is reproducible as
`git show 5eb8f20fe291603c74973fa94cc55723ac8089a4:corpus/SOURCES.md` (896 lines, sha256 `f7b9d46b…`).
