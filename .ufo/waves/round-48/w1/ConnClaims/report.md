# ConnClaims — cross-claim pre-freeze checklist (round 48, w1)

Seat: ConnClaims (leaf; no subagent dispatch). Task: read the round-47 registration,
closure and QUALITY 85-95; produce the pre-freeze checklist for round 48.

## 0. Evidence read and verified

- `.ufo/waves/round-48/claims.md` (C1 warm-cache; C2 xkb-keymap-compile-r48; routed D1-D4, R3, R4b, M47-10, CritC1Explain, SentC1Sandbox F1-F4).
- `.ufo/waves/round-47/registration.md` (freeze contents: claims, counters, fixtures, pins, L1 reference, controls, base receipts, separability).
- `corpus/lessons/round-47-verifier-spotcheck.md` (closure; defects D1-D4; carried R3/R4b/M47-10/CritC1Explain/SentC1Sandbox).
- `corpus/QUALITY.md` criteria 85-95 (`:418-504`).
- `corpus/lessons/round-47.md` M47-1..10 (`:73-211`).
- w2 seat reports: `w2/ExecC1Diff.md` (H1/H2/H3), `w2/CritC1Explain.md`, `w2/SentC1Sandbox.md` (F1-F4), `w2/ExecErrataR45.md` (H1 blocker).
- `.ufo/waves/round-46/w1/ScrRoutedAges/ages.md` (age convention).
- Verified: base `579f694b…` is a commit; base `tools/mado-terminal.py:82-85` carries "Cache (out of contract)"; pin `fetch/xdg-terminal-exec` gen_hash `:179-215`, read_cache `:217-298` (line limit 50 at `:239-241`, terminator at `:247-251`, hash+`command -v` check at `:274`), save_cache `:300-332`, background save at `:1457`; round-47 receipt inventory (c1-before/c1-after/c1-tip, c2-*, ctl-c1, h12-check, census, axis).
- W1 drafts observed mid-wave: `.ufo/waves/round-48/l1-draft/lsemu.py` (L1 ls-emulator draft); `w1/ExecAxisBase/receipts/c1-r47-base.txt` is **empty**; `w1/ExecD2Receipt/receipts/session-material-579f694b.txt` records rc=2 because the receipt command resolved `quality/check-session-material.py` against the fleet root, not the lane ($§4).

## 1. What the freeze commit must contain

One commit, after w1 returns and before any data commit (round-47 model, `registration.md:1-7`): base hash,
claims text, the two counters, the finalized fixtures, the pins, the L1 reference, the controls and the base
receipts. Nothing scores a frozen counter in w1.

### 1.1 `registration.md` v1
- Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`; round shape (w1 build, w2 falsify; a hole w2 finds before data may re-register as v2; after data, kill rule).
- Lowest-axis rule: axis table tied at maximum (`receipts/axis-tip.txt` `checked=3 mismatched=0`), so no axis lowest; **quality** is the trend furthest behind (closure: `unprovable-but-better`); C1 is the quality-trend/operability move, C2 the sourced expansion.
- Premise corrections from w1 (round-47 model: `CritPremise` F1-F3 in `registration.md:14-26`) — fold w1 findings into the registration before freeze, e.g. anything w1 finds on `ls -LRl` emulation scope, cache-priming waits, or the xkb entry's boundaries.
- Routed-items section: D1-D4, R3, R4b, M47-10, `CritC1Explain`, `SentC1Sandbox` F1-F4 — each with its landing requirement and a named receipt (see §3).

### 1.2 C1 — `quality/counters/c1-r48-terminal-cache.py` (PRED-C1-r48)
Clauses (mirroring PRED-C1-r47 plus the warm-cache surface):
- a tool present; s selftest `N/N`, N ≥ 30, run inside the sandbox.
- f fixtures (schema v2, final form, §1.3) in two variants (A `LANG=C.UTF-8`, B `LANG=en_US.UTF-8`), materialized twice (oracle tree / tool tree, identical bytes, separate roots), tool stdout+rc == oracle; oracle result == recorded `expect`, else setup error.
- g nonce cases judged by the oracle at count time (cold ones as round 47, plus generated warm cases: a primed-cache tree where the oracle recomputes its own `md5sum` over `ls -LRl` at count time).
- x explain: last `MADO_TERM:` line must carry `selected= path= cmd= cache=`; the `cache=` verdict is exactly `absent|hit|stale|invalid|disabled`; `--observed` compare must cover **all three** captured items (id, path, command line) — mutating any one must give DIFFER (fixes `CritC1Explain`); HOME unset in-contract: exit 1, empty stdout (fixes closure D1).
- i isolation: rewrite the clause wording to an **enumerated mount set plus "no host path outside it is bound"**, and test the mount list (fstype/source/mountpoint/ro), not path absence (fixes `SentC1Sandbox` F1-F3); record accepted residuals (hostname, `/usr/lib` host subtree, `/dev` devtmpfs, `PWD` injection).
- r strace `trips=0` over every tool run (selftest, fixtures, generated).
- Robustness (fixes F4): the observed capture is written via `tempfile.mkdtemp(dir=<root>/.rw)` + `O_CREAT|O_EXCL|O_NOFOLLOW` opens; any `OSError` there is a clause-x failure for that fixture, never a count abort.
- Drift check: oracle is this host's bash/find/awk/tr/ls/md5sum at count time (`ls` now also judge-critical for the cache hash); `FIXTURES_SHA256`, `PIN_SHA256` pinned in the counter.

### 1.3 C1 fixtures — `quality/counters/c1-r48-fixtures.json` (schema v2, final)
Round-47 schema (id, class, env with `$ROOT`, files, exec, args, expect) **plus**:
- `mtime` (epoch seconds applied to every materialized file and dir)
- `prime: {args: [...]}` (cold run before the scored run; wait for the background save to finish — bounded poll on the cache file)
- `after: {files: {<path>: <text>|null}, exec_add: [...], exec_remove: [...], env: {...}, mtime: <epoch>}` (applied after priming, then mtimes re-pinned)
- `cache: "<literal cache text, $ROOT substituted>"` (malformed caches; no priming)
- `expect` ALWAYS produced by running the real pinned script (never typed), 3 identical runs.
Required classes (from the w1 spec/claims and round-47 closure):
- warm-hit where the warm answer DIFFERS from the cold one: edits that keep size and mtime minute; removed TryExec stub while exec[0] still resolves; changed `--dir`/`--title` args applied over cached arg names; cache with valid hash/terminator used to answer print modes.
- invalidation: mtime/size/name/dir change; `XDG_CURRENT_DESKTOP` change; exec[0] gone (line-2 `command -v` fails); bad hash.
- malformed: missing terminator (`:247-251`), line limit (line 50 returns 1, `:239-241`), non-hex hash.
- disabled: `XTE_CACHE_ENABLED=false`; `/disable_cache` present.
- M47-10 regression classes (from `ExecC1Diff.md`): non-regular `*.desktop` paths in a higher-preference applications dir (directory, symlink → /dev/null, dangling symlink, **FIFO**) and option-like `Exec[0]`/`TryExec` words (`-p -v -V -- -pv -pV -vp`, table in `ExecC1Diff.md:115-117`).
- D3 readdir-order class: two valid candidates in one dir, with an **expected order** taken from the three identical pin runs (the counter must materialize in that order).

### 1.4 C2 — `quality/counters/c2-r48-xkb-entry.py` (PRED-C2-r48)
Clauses (mirror c2-r47-terminal-entry.py):
- a entry new at REV (`corpus/knowledge/xkb-keymap-compile-r48.md`); b provenance head ≥ 2 `source: S###` ≥ S340, rows mined/opened 2026-10-26/used-by the entry; c every cited row pin-bound (fetch copy under `.ufo/waves/round-48/fetch/`, digest equal; ref-pinned tag/commit, no branch); d every quote verbatim inside its pin at its stated range; e ≥ 6 numbered chain steps each with a script/tool locator; f the live read-only receipt (`live-xkbcli-host-r48.txt`: `xkbcli_sha256=`, output lines, rc 0/1/0+warning cases) and the entry line naming it; g one README index row covering the head ids; h held rows S318/S319 byte-equal to base and the Hyprland-fallback mapping implemented by citing the held entry's step 4 (never re-claiming); i census terms absent at base (`receipts/c2-ground-base.txt`) and ≥ 2 present at REV.
- Host-fact block: the L1 fact table (libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1, the five `xkbcli compile-keymap` rc/warning rows, include paths searched) committed as a receipt so the counter never queries the host.

### 1.5 Pins, reference, controls, base receipts
- Pins: `fetch/xdg-terminal-exec` (same `89f2be9a…` pin); new pins fetched by C2 seats under `fetch/` with sha256 + tag/commit URL, never a branch.
- Reference: `l1-draft/mado-terminal.py` (extended) frozen; its docstring is the contract identity. **Currently `l1-draft/` holds only `lsemu.py`** — the extended tool reference must land by freeze (or the registration must name where the contract text lives). `l1-draft/lsemu.py` (if part of the instrument) must be frozen too.
- Controls (`ctl/run-c1-controls-v4.py`): REF met; BASE, STUB, EXIT1, CONST, DELEGATE-SH, SUBPROC-EMBED, EMBED-EXECV, CTYPES-EXECVE, SOCKET-AND-REF, EXPLAIN-CANNED, EXPLAIN-ALWAYS-AGREE, one-rule-undone variants — **plus warm-cache cheats**: a tool that writes the cache file, a tool that forks the real resolver on the cache path, a stale-answer table, an ls-date-format-imitation, a cache-only shortcut that ignores invalidation. Every cheat the attacking wave builds must be a control (QUALITY 86, `QUALITY.md:420`); complete battery receipt per QUALITY 87 (`:422-430`). C2 controls include the forgery suite for a tree-reading counter (QUALITY 88, `:432-442`).
- Base receipts (all at rev `579f694b`): `c1-before-base.txt` (`fixtures=0/N … tool=absent verdict=TARGET_MISSED`), `c2-before-base.txt` (`admitted=0/1`), `c2-ground-base.txt` (grep exit 1), `census-before.txt`, `fetch-sha256.txt`, axis receipts, and a **h12-style warm-cache parity receipt** (pin-judged cache cases, diff 0).

### 1.6 Session-material gate (R3) and quality criteria
- Install the drafted synthetic marker (round-47 `w1/ExecSessionMarker`, attacked by w2) and register the gate with a **clean-state receipt at the revision it scores** plus a planted-defect receipt that still trips (QUALITY 93, `:480-488`); replace the waiver sentence at `SKILL.md:770` (M47-3).
- New quality criteria, if any, must be grounded in lessons/round-47.md mistakes (M47-1..10) and each have a red-before read (QUALITY 91-95 pattern).

## 2. Separability proofs (land in the freeze)

- C1 reads only `tools/mado-terminal.py` (plus the pinned judge inside the counter); C2 reads only the entry, rows, README row, pins and receipts. The C2 positive control is an entry-only tree (no tool) and is admitted; a tool-only tree has no entry (C2 clause a). Shown both ways on the landed bytes by a w2 seat (round-47 model, `registration.md:80-84`; M47-9, `round-47.md:200-203`).
- The C1 counter loads its pinned model (ls emulator, if used by the scoring path) from a copy under `--work`, never by in-process import from the scored tree (QUALITY 95, `:498-503`); its receipt carries a before/after inventory of the scored tree.
- The fixture builder (`ctl/build-fixtures-v2.py`) runs the pin, never the tool; `expect` is a pin product, so C1 cannot be satisfied by a fixture-narrowed tool that diverges from the judge.
- C2 must never run `tools/mado-terminal.py` (round-47 C2 separability, `registration.md:25-26`).

## 3. Closure defects — recurrence and how to make each impossible

| defect | round-47 evidence | recurrence risk | make impossible this round |
|---|---|---|---|
| D1 post-freeze contract narrowing | landed docstring added "HOME unset"/FIFO/symlink-loops exclusions; frozen reference listed none; tool exits 2 where pin exits 1 (`round-47-verifier-spotcheck.md:126-131`) | any landed-vs-frozen docstring drift repeats | freeze embeds the exact contract text (reference docstring) in registration and the counter/control compares the landed tool's docstring bytes to the reference at data commit (hash); any divergence = miss, requiring re-registration v2 before data; HOME unset is modelled as the pin (in-contract) |
| D2 unreceipted numbers | report's session-material `findings=128` has no committed receipt; tip-era receipts read 136/139 at other revisions (`:132-135`) | any report figure without a same-revision receipt | report numbers are emitted by the instrument at the tip revision and the receipt is committed beside them; a L1 lint greps each numeric claim to a committed receipt line; ages/deferral counts derived by one command (QUALITY 94, `:490-496`) |
| D3 unrouted readdir-order blind spot | w2 found `sorted()` walk scores 190/190; only nonce catches it (1/150); not routed (`:136-138`; `ExecC1Determinism.md:10`) | counter blind spots stay invisible if not routed | every w2 seat finding appears in the round lesson's routed section or an explicit no-action note (script: seat names in w2 results ⇒ ids in lesson §6); M47-10 ordered-dir fixtures land in schema v2 (two valid candidates in one dir, expected order from 3 pin runs) |
| D4 locator off-by-one | `xdg-terminal-selection-r47.md` Limits cites `:150-151`, text sits at `:149-150` (`:139-140`) | hand-typed locators drift | erratum line appended; locator-verification script (`verify-locators.sh` pattern) runs over every citation in the new entry before data commit; locators computed (`grep -n`), never typed |
| M47-10 fixture gap | H1/H2 invisible to the frozen counter (no non-regular paths, no option-like Exec words) (`ExecC1Diff.md:100-103,137-138`; `round-47.md:205-210`) | gap persists if schema v2 does not carry the classes | §1.3 classes are mandatory in the finalized schema; H1/H2 regression fixtures scored under f |
| CritC1Explain | explain `cmd=` not compared; capture differing only in the third item reports AGREE | `--observed` false-AGREE survives | counter compares all three items; per-item mutation cases (id/path/cmd) each require DIFFER |
| SentC1Sandbox F1-F4 | clause i wording falsified (`/fast` stub, `/usr/bin` writable, host identity); F4 `FileExistsError` aborts the count with no verdict line | isolation claims stay untestable; a tool can DoS grading | §1.2 i (enumerated mounts) and robustness (mkdtemp + O_NOFOLLOW, OSError ⇒ clause-x fail, never abort) |
| R3 | marker drafted, attacked, **not installed** (4th age) | gate stays red with standing waiver | install marker; clean-state receipt at scoring revision + planted-defect receipt (QUALITY 93) |
| R4b | drafted erratum block turns frozen round-45 counter to TARGET_MISSED (`ExecErrataR45.md:29-62`) | any errata append that renames a cited id without quote/locator drops `all_body_lines_bound` | append `block-fixed.md` (single-token fix, blank line); before landing, re-run the frozen round-45 counters (`c2-r45-monitor-entry.py` and `-v2`) on the post-append tree — must stay `admitted=1/1 TARGET_MET`; codify as the rule for every errata onto a frozen entry |

## 4. Fresh w1 observations (must be resolved before freeze)

- `w1/ExecAxisBase/receipts/c1-r47-base.txt` is currently **empty** — the before-receipts (counter absent at base, TARGET_MISSED) must be populated by a real run at rev `579f694b`.
- `w1/ExecD2Receipt/receipts/session-material-579f694b.txt` shows rc=2: the receipt command used a relative path from the fleet root (`python3 -I quality/check-session-material.py …` resolved to `/home/vgpnk/Projects/shokunin/quality/…`). Receipt commands must use the absolute lane path; this is a D2-class landing bug to catch before freeze.
- `l1-draft/` holds only `lsemu.py`; the extended reference tool (whose docstring is the C1 contract) is not drafted yet — freeze cannot ship without it.

## 5. Verification the checklist itself demands (for the L1)

- Every fixture's `expect` from 3 identical pin runs (run at count time in the same bwrap sandbox).
- `git diff --numstat` base→freeze: append-only on held surfaces (QUALITY/LOG/SOURCES held rows/SKILL except documented registry sentence); 0 removed lines.
- Counter self-invocation: counters pass selftest; run once with `--help`-style checks before freeze.
- Non-author re-read: closure spot-check re-runs the C1 live AGREE from committed bytes and re-fetches pins (round-47 closure did both).
