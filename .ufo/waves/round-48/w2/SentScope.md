# SentScope — mado round 48, wave w2: source/read-only and fleet write scope

Seat: `SentScope` (sentinel, leaf). Target: verify no source-checkout writes or campaign tools, and no seat
notes/outputs in the fleet root except the quarantined `tree.json` notice; inspect write-tree/diff receipts and
quarantine. Nothing in this seat modified anything: no lane file, no fleet-root file, no host file, no package
or tool transaction, no lane Git/jj mutation. Scratch `/fast/scratch/hyaku/mado-r48/SentScope/` created and
removed; receipts copied to `.ufo/waves/round-48/w2/SentScope/` first (8 files, 15,478 B; largest 3,937 B).

Axes: (1) host read-only integrity, (2) fleet-root vs lane write separation (write-tree/diff), (3) receipt
fidelity. One defect found (S1, live host write); two scope concerns recorded (S2, S3); the rest checked clear.
No frozen predicate, counter, fixture, claim, or target is changed by this report; nothing here narrows a
clause.

---

## S1 — HIGH — the operator's `xdg-terminal-exec` cache was written during w2, by a wave seat's unsandboxed mutant

**Observed.** `/home/vgpnk/.cache/xdg-terminal-exec` changed between my check at 01:20Z and 01:26:35Z.

| when | size | mtime | inode | sha256 |
|---|---|---|---|---|
| w1 `SentHost/receipts/01-host-cache-before.txt`, `07-…-after.txt` (2026-10-26T23:55–23:56Z) | 190 | 1793047345 | 143468605 | `f497ed057f8aaba24bea21ba652b810c6c2ab754b0b8fe9d9b1645e072a10cac` |
| this seat, 01:20Z | 190 | 1793047345 | 143468605 | `f497ed05…` (same) |
| this seat, 01:26:35Z → 01:30Z and final | **7** | **1793064395** (22:26:35.045 -03) | 143468605 (same inode) | **`c8b104e695a9cfccd3dee34017aabee119c9edbb185bfe3325cdfc4c55940144`** |

Payload (`od -An -c`): `r 4 8 - w 2 \n` — the literal string `r48-w2`.

**Attribution (content + same-second twins).** Three files were written at 22:26:35.045 with that exact payload,
two of them inside one seat's scratch/`/tmp`:

- `/home/vgpnk/.cache/xdg-terminal-exec` (the host cache)
- `/tmp/r48-w2-probe`
- `/fast/scratch/hyaku/mado-r48/MutC1ReadOnly/work/t/r48-w2-probe`

The only writer of the constant `r48-w2` in the wave is `w2/MutC1ReadOnly/mkmutants.py`'s M-WRITE hook:
`:31` `_tgt.append(("homecache", os.path.join(os.environ["HOME"], ".cache", "xdg-terminal-exec")))`,
`:32` `/tmp/r48-w2-probe`, `:33` relative `r48-w2-probe`, `:40` `_fh.write("r48-w2\n")`, plus
`_cache = os.environ.get("XDG_CACHE_HOME")` at `:27-29`. Its receipted probe is sandboxed and contained —
`receipts/probe-M-WRITE.txt:3` `TOOL_STDERR R48PROBE cache=EROFS homecache=EROFS tmp=ok treeroot=EROFS` — so the
host write came from an **unreceipted, unsandboxed invocation of the same mutant** (the seat's HOOKRUN/manual
step) with the operator's real `HOME`; the cwd at that moment was its scratch `work/t` (the relative probe
landed there, not in the fleet root). No receipt records the write; `grep '/home/vgpnk/.cache'` over that
seat's `receipts/` returns nothing.

**Exploit path.** The hook is a live forgery of the resolver cache: it derives the target from ambient
`HOME`/`XDG_CACHE_HOME` and writes it with no sandbox, no path allowlist and no tripwire. Had the payload been a
well-formed cache (md5 line + `END_OF_EXEC_USEP` + command, as the pin parses at `xdg-terminal-exec:179-298`),
the next SUPER+RETURN would have started a different command than a cold run — C1's own threat model executed
against the operator's account. As written the 7-byte body is malformed, so the pin rejects it as invalid and the
warm cache is merely destroyed and will be re-minted by the operator's next hotkey; that is luck, not a guard.

**Impact.**
- Host state mutated in a wave whose premise is read-only; the round-47/pin warm-cache evidence chain is broken
  (`f497ed05…` is gone; only its hash was recorded, the bytes are not restorable from any receipt).
- Any seat whose before/after tripwire spans the wave now compares different worlds: `SentHost`'s "host cache
  untouched: yes" holds for w1 only, and a w1→w2 comparison reads this change as an unknown delta.
- Not a frozen-predicate break: both counters run the tool/model inside sandboxes with `XDG_CACHE_HOME`
  redirected (no clause reads the host cache), so `PRED-C1-r48`/`PRED-C2-r48` are unaffected. Per the w2 rule it
  is a miss-level conformance item for the wave, and the wave may not claim host read-only behaviour.

**Smallest remediation.**
1. Seat rule: hook-bearing mutants run **only** inside the counter's `Box`; an unsandboxed `--selftest` of a
   mutant is a setup error (the mutant's own `HOME`/`XDG_CACHE_HOME`-derived targets must not exist outside).
2. Freeze `SentHost` G2 (size + mtime_ns + inode + sha256 before/after) into every w2 C1 seat spec and make a
   change a hard abort, not a note.
3. Record this delta in the closure as a known host change; do not have a seat "restore" the cache by running the
   resolver ambient (that writes again) — let the operator's next hotkey re-mint it, then pin the new hash.
4. Re-word any round text that asserts the host cache was untouched across the whole round.

---

## S2 — MEDIUM — a 227 MB executable landed in a PATH directory during the round (`~/.local/bin/agy`, 22:05:23)

`/home/vgpnk/.local/bin/agy` — 227,840,232 B, mode 755, mtime 2026-10-26 22:05:23.59 -03, ELF PIE x86-64 stripped,
sha256 `40349135371a8ed1f1af1e9f8b741de99174ae9fce6380b96c2d1f543480af7a`; a previous-generation sibling
`agy.1793063119693176144.old` (223,736,040 B) dates from Oct 22. `/usr/bin` and `/usr/local/bin` have zero new
files in the window; pacman's last transaction is 2026-10-25T13:12 (pre-round); no uv tool directory was added.

**Scope concern.** The campaign host guard forbids creating/modifying anything in `~/.local/bin` or any PATH
directory. No mado r48 artifact mentions `agy` (the only textual hits are this seat's own receipts), and every w1
seat reports "no install", so this is not attributable to a mado seat from artifacts — but a 227 MB binary that
appears mid-round is exactly what a "campaign tools" check exists to exclude, and the w2 window itself opened at
22:18. **Smallest remediation:** the orchestrator names the installer in the run ledger (operator/harness install
vs. a seat) so the closure can either exclude it or record a host-guard breach; no seat should attribute it.

---

## S3 — LOW — the two "revived r47 seat edit" diff receipts name changes that exist nowhere, and no write-tree receipt exists

- `receipts/m48-revived-r47-seat-edit.diff` and `-2.diff` target only `.ufo/waves/round-47/w1/ScrRows.md` and
  `.ufo/waves/round-47/w1/ExecCounterC1.md` (appended "Provenance note (L1 IRC…)" / "Priming a warm cache…"
  sections). Neither text is in the worktree **or** in `HEAD`: grep counts 0/0, `git log --all -S` finds no
  commit, both files' last commit is r47's `9bddd6ac`, and neither path is in the freeze commit `3e6c848a`.
  Read as "applied", the receipts are false provenance; read as "pending", they must land before the closure or
  be withdrawn. They do not touch any held byte (the r46 entry diff vs base is 0 lines).
- There is **no** receipt named `write-tree` (0 matches in `receipts/` and in the 41 w1 seat receipt dirs). The
  write-tree evidence I could produce is the fleet root's own: `git write-tree` = `HEAD^{tree}` =
  `929230890c5b4bd5ed3ccd2841a886d58f04a220` at `6f3bcb71`, `git ls-files -m` empty, `git status` empty.
- The lane's 9 uncommitted tracked modifications (+1813/−64) are covered by **no** diff receipt. One is a
  *published* gate: `quality/check-session-material.py` `+992/−31`, modified in the worktree while w1's
  `SentPrivacy` scores it at base/tip revisions and publishes it as QUALITY 85. If the gate is to be widened
  (SentPrivacy's remediation), the change needs its own diff receipt and a base/tip re-score; if not, it should
  not sit uncommitted through the freeze.

---

## Quarantine and fleet-root write scope — checked, clean (two manifest gaps)

- `.tower/` is gitignored (`git ls-files .tower | wc -l` = 0), so quarantine never enters history; the fleet root
  is clean at `HEAD 6f3bcb71` (write-tree == HEAD tree), and `tree.json` is not tracked now nor in any commit
  (`git ls-files | grep -c tree.json` = 0; `git log --all -- tree.json` empty; no `tree.json` at depth ≤2).
- The four round-near quarantine dirs and their content:

| dir | content | manifest | attribution (driver notice, `.scratch/goal-20261026-hyaku-run9.md`) |
|---|---|---|---|
| `fleet-root-strays-20261026T1956` | `=1239` (16 B), `=3900` (49 B), `T` (0 B) | **NONE** | unattributed shell-redirect misparse, cwd = fleet root |
| `…T2010` | `p.err` (0 B), `p.out` (62 B, `QUOTE S115 … spans/S115-1.txt`) | **NONE** | chousa r52 w1 seat, cwd = fleet root |
| `…T2055` | `tree.json` (347,495 B) | SHA256SUMS → `fdb0b7a4…` **verifies OK** | mado r48 w1 seat (shape inference), cwd = fleet root |
| `…T2114` | `fx/A2-uppercase-fsid-sysfs/…/scrub_speed_max` | SHA256SUMS + TREE.txt → **verifies OK** | tsukuroi r44 w1 C1 scrub-arm seat, cwd = fleet root |

- **The permitted tree.json notice exists**: commit `0caf3154` ("hyaku run 9: record tree.json fleet-root
  misroot (mado r48)") appends to `.scratch/goal-20261026-hyaku-run9.md` that tree.json (347,495 B, GitHub tree
  dump of `hyprwm/Hyprland efb50993…`) appeared at 20:44 with cwd = fleet root, was moved bytes-unchanged to
  `…T2055` (sha256 in `SHA256SUMS`) and "told MadoR48". Content check by this seat agrees: the quarantined
  file's own `sha` field is `efb50993780079460b0cbed1363e2166a2de1d9f`, the commit only the w1 Hyprland-keymap
  scouting slice pinned. No w1 receipt records writing it; `ScoutXkbSpecs` explicitly denies it and
  `ScoutHyprKeymap` claims "nothing outside the seat dir", so attribution remains shape-based — recorded as such,
  not asserted.
- **Two manifests missing** (`T1956`, `T2010`): those strays have no recorded hash, so the quarantine preserves
  bytes without proving they are the bytes that were moved. Cheapest fix: write `SHA256SUMS` when moving, as the
  other two dirs do.
- Other lanes' fleet-root activity (`Mo51CritEntail12`/`Mo51ConnSiblings` at 19:50, the tsukuroi r44 host process
  leak at ~21:13) is noticed in the same goal file and is not this wave's; the `.ufo/reports/round-49/kama.md`
  and `…/round-44/kengaku.md` files present at those moments are in-flight lane reports, correctly left alone.

---

## Source/read-only — checked, clean

- Host XKB sources and resolver untouched: `/usr/share/xkeyboard-config-2` (mtime 2026-10-03), `/usr/share/X11/xkb`
  (2026-06-21), `/usr/include/xkbcommon` (2026-10-03), `/usr/bin/xdg-terminal-exec` (2026-09-18); **zero** paths
  under those trees newer than 2026-10-26 19:00. User XKB paths `/home/vgpnk/.config/xkb`, `/home/vgpnk/.xkb`,
  `/etc/xkb` all absent (the last was already absent in `SentHost`).
- No package/tool transaction in the window (pacman log's last pair `transaction started/completed` is
  2026-10-25T13:12); no new `/usr/bin` or `/usr/local/bin` file; no uv tool dir added.
- Lane writes are confined to `mado-shokunin`: 9 tracked modifications, untracked paths only under
  `.ufo/waves/round-4{5,8}/`, `corpus/`, `quality/`; no mado w1 output cites another lane's absolute path (the
  only fleet-root reference, `ExecIdGuard`'s `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-48.md`, is a
  **read** of the §10 text it quotes); held C2 bytes: `hyprland-input-devices-r46.md` diff vs base = 0 lines.
- Fleet-root commits during the round are driver commits only (lane prompts/reports, rounds ledger, `.scratch`
  goal); the sole fleet-root file modified by the driver in this window is `MANIFEST.json` (22:13, committed) and
  `.ufo/l0-questions.md` (21:56, committed).

## Not a finding / checked clear

- `/tmp` residue in the window is mostly other lanes' (kasegi `kas-*`, the `round-close-selftest-*` fleet close,
  chousa/kaidoku scratch) plus this wave's two `r48-w2` twins; the `/tmp` sweep is `SentScratch`'s seat, not
  duplicated here. `/tmp/mado-terminal-selftest.*` is absent.
- `/fast/scratch/hyaku/mado-r48/L1c1-*` dirs are the L1's own C1 scratch (work dirs outside the repo, as the
  counter requires), not seat leaks.
- `xdg-terminal-exec` itself was not executed by this seat; the host cache was read (stat/sha256 only) to measure
  S1, never written.

## Reproduce (lane root; read-only except the scratch copies)

```
git -C /home/vgpnk/Projects/shokunin write-tree; git -C … rev-parse HEAD^{tree}; git -C … status --porcelain=v1
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --stat; git -C … diff 579f694b -- corpus/knowledge/hyprland-input-devices-r46.md | wc -l
sha256sum /home/vgpnk/.cache/xdg-terminal-exec; od -An -c /home/vgpnk/.cache/xdg-terminal-exec
stat -c 'size=%s mtime=%Y inode=%i' /home/vgpnk/.cache/xdg-terminal-exec
for d in /home/vgpnk/Projects/shokunin/.tower/quarantine/*/; do (cd "$d" && sha256sum -c SHA256SUMS); done
find /usr/share/xkeyboard-config-2 /usr/share/X11/xkb /usr/include/xkbcommon -newermt '2026-10-26 19:00' | wc -l
git -C /home/vgpnk/Projects/shokunin show 0caf3154   # the tree.json misroot notice
```

Receipts (this seat, `.ufo/waves/round-48/w2/SentScope/`): `01-fleet-writetree.txt`, `02-lane-inventory.txt`,
`03-quarantine.txt`, `04-host-readonly.txt`, `05-tmp-scratch.txt`, `06-host-cache-mutation.txt`,
`07-diff-receipts.txt`, `08-extra.txt`.
