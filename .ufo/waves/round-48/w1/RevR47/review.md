# RevR47 — review of the round-47 closure routing (round-48 w1, reviewer seat)

Reviewed: `corpus/lessons/round-47-verifier-spotcheck.md` §6 (D1-D4 + carried) against lane base
`579f694b45c797a9c39761fdb4f9e0a1b71b3585`. That base is `d40189c924e01dc1cbe290474eb4256d343590d4`
(the round-47 tip) plus exactly one commit — the closure itself — which adds only
`corpus/lessons/round-47-verifier-spotcheck.md` (+146, 0 deleted; author `protocol-shokunin`,
2026-10-26T20:33:14-03:00, i.e. the non-author integrator identity). Every routed fix is therefore
round-48 w1 scope; at base none has landed, and this review verifies (a) that each routed defect is
real, (b) that the round-48 routing covers it, and (c) anything the closure missed.

Method: committed bytes via `git show` / `git grep` / `git ls-tree` at `60edb66e`, `d7527d608ad2b2e3…`,
`d40189c9`, `579f694b` (lane) and `6fd13912` (fleet, for `.ufo/reports/round-47/mado.md`), plus
read-only host probes. No lane counter or gate was executed. The resolver ran only with `--print-*`
and `XDG_CACHE_HOME` inside `/fast/scratch/hyaku/mado-r48/RevR47`; no FIFO was offered to the
resolver (it blocks; the rc=124 measurement is cited from committed w2 receipts). No tools installed.
Working-tree `tools/mado-terminal.py` sha256 `b84d5c4f723049c0…6de2222` = the `d40189c9` blob
(verified both sides). Pin re-verified: sha256(`/usr/bin/xdg-terminal-exec`) = `89f2be9a…27ac`,
1499 lines, 23 function definitions — the spotcheck's census holds exactly.

## 1. Routed defects — verdicts

### D1 — post-freeze contract narrowing: CONFIRMED, unfixed at base, routed
- Frozen reference `.ufo/waves/round-47/l1-draft/mado-terminal.py@d7527d608ad2b2e3cc398fdde34db7947b254a1a`
  exists; its out-of-contract sentence (:84-87) lists "-h/--help, an empty-string … locale" and does
  NOT contain "HOME unset", a FIFO, or symlink loops.
- Landed `tools/mado-terminal.py@d40189c9` :85-88 adds all three ("HOME unset, a FIFO named like a
  desktop file in a later application dir …, symlink loops") and :88 pins the exit-2 refusal;
  `:410 raise OutOfContract("HOME unset")` and `:526-529` (FIFO) implement it.
- `registration.md:30-31` (d40189c9) freezes the C1 contract as "the docstring of
  `.ufo/waves/round-47/l1-draft/mado-terminal.py`" — so the landed docstring diverges from the
  frozen one. D1 is real.
- Not fixed at base: `corpus/lessons/round-47.md` at `579f694b` has no D1/HOME line. Round-48
  `claims.md` routes it ("D1 contract-delta lesson line (and HOME unset in C1's contract)"). But see
  §3.1 — the routed wording itself is defective.

### D2 — `findings=128` without a receipt: CONFIRMED, unfixed at base, routed
- Fleet report at `6fd13912`, `.ufo/reports/round-47/mado.md:104`: "the session-material gate reads
  `findings=128` at the tip (115 at base)".
- `git grep 'findings=128' d40189c9` (lane) → rc 1; at `579f694b` the only lane occurrence is the
  spotcheck lesson itself (:132-133).
- Committed `.ufo/waves/round-47/w1/ExecSessionMarker/receipts/*` carry findings=115 (01-baseline),
  136 (02, 03, 17-claims-check), 139 (09, 12, 12a, 14) plus intermediate marker-on values
  (52/84/86/88/111/61/78/55/92). **128 appears in no committed receipt** — the spotcheck's "115 at
  base, 136/139 at other revisions" is exact.
- Round-48 claims route "D2 session-material receipt at a named revision". Covered.

### D3 — readdir-order blind spot unrouted: CONFIRMED, unfixed at base, routed
- `w2/ExecC1Determinism.md:9-11`: clause f/x are blind to the readdir axis; a tool that sorts
  directory entries "passes all 190 fixtures and all 190 explain checks".
- Committed receipts: `w2/ExecC1Determinism/counts/run-mut-sorted-n4242.txt` =
  `fixtures=190/190 explained=190/190 generated=149/150 … verdict=TARGET_MISSED … nonce=4242`;
  `counts/summary.txt` line 2 = 146/150 (nonce 4747). The nonce clause is the only detector —
  1/150 at 4242, as the spotcheck says.
- Not routed at base: `git grep -i readdir d40189c9 -- corpus/` → no matches; the fleet report
  contains no readdir mention. Round-48 claims route "D3 readdir-order fixtures". Covered.

### D4 — off-by-one locator: CONFIRMED, unfixed at base, routed
- `corpus/knowledge/xdg-terminal-selection-r47.md:95` (byte-identical at d40189c9 and 579f694b)
  cites `terminal-route-r17.md:150-151`; the `[UNK]` text ("Whether the `--dir=` value … is valid at
  / launch time. The helper is not run.") sits at r17 **:149-150**.
- The entry's other r17 locators (:76 and :88 → r17 :144-145) are correct — no second off-by-one.
- Erratum not appended at base; round-48 claims route the erratum. Covered.

## 2. Carried items — verification

- **R3 (session-material synthetic marker): routed and armed.** The ExecSessionMarker seat is
  committed at d40189c9 (`.synthetic` sidecar scheme, `demo/`, 17 receipts); w2 `MutSessionMarker.md`
  and `RevSessionMarker.md` exist, so the routing's "attacked by round-47 w2 MutSessionMarker/
  RevSessionMarker if present" is satisfied. Gate red per fleet report :104.
- **R4b (round-45 errata): routed in exactly the shape w2 proved.** `w2/ExecErrataR45.md`: 6/6
  erratum subjects CONFIRMED; H1 — the drafted E6 bullet names S303 in prose, flipping clause g and
  both frozen `PRED-C2-r45` counters to TARGET_MISSED (committed receipts: baseline and
  `block-fixed.md` variants MET, both verbatim variants MISSED); the landable form is
  `block-fixed.md` (38 lines) + the H2 leading blank line + the H3 prose fix (the `CONFIG_LEGACY`
  enumerator is removed from `ConfigManager.hpp`, the case/selection from `ConfigManager.cpp`).
  Round-48 claims route "R4b … in a form that keeps the frozen round-45 counter verdict". Covered.
- **M47-10 (fixture schema v2): routed.** `w2/MutC1Fixtures.md`: 22 mutants, 9 genuine blind spots
  with verified kills/probes; schema gaps named there: no PATH field (#7), no file mode (#8),
  non-regular `*.desktop` paths unbuildable, nonce-fragile kill (#5). Round-48 claims route
  "M47-10 (fixture schema v2: H1/H2 cases)" (H1/H2 = `w2/ExecC1Diff.md`'s two root causes). See
  §3.3 — the declared v2 fields still cannot express three of the routed kill classes.
- **w2/CritC1Explain.md: routed** ("explain `cmd=` compared"). Committed report: the rsplit mutant
  that drops the third printed item scores MET 190/190 at nonce 4700; the counter's clause x
  (`c1-r47-terminal.py:277-290`) mutates only the first `.desktop` token.
- **w2/SentC1Sandbox.md F1-F4: routed.** F1-F3 falsify clause-i wording (writable `/fast` stub
  chain and host paths visible via `/proc/1/cmdline`; `/usr/bin` present and writable; host
  hostname/identity) — registration-text fixes; F4 — a tool-created `<root>/.rw/obs` aborts the
  count with `FileExistsError` at `c1-r47-terminal.py:279`, exit 1, no verdict line; remediation
  `mkdtemp` + `O_EXCL|O_NOFOLLOW`, OSError ⇒ clause-x failure. The new warm-cache counter must
  inherit the F4 fix (§3.3).

## 3. Defects not in the closure (new findings)

### 3.1 MEDIUM — the routed D1 fix wording drops the pin's HOME-unset condition
Spotcheck §6.1 routes "model HOME unset as the pin does (exit 1, empty stdout)"; round-48
`claims.md` repeats it unconditionally ("HOME unset is modelled as the pin does (round-47 closure
D1: pin exit 1, empty stdout)"). Measured on the host pin (`--print-cmd`, scratch cache):

| probe | env (HOME unset in all) | pin rc | pin stdout |
|---|---|---|---|
| A | `env -i PATH=…` (no XDG vars) | 1 | empty — `line 148: HOME: unbound variable` |
| C | XDG_CONFIG_HOME+XDG_DATA_HOME set, XDG_CACHE_HOME unset | 1 | empty — `line 172: HOME: unbound variable` |
| B | XDG_CACHE_HOME+XDG_CONFIG_HOME+XDG_DATA_HOME all set | **0** | **`alacritty`** |

The r47 tool refuses every HOME-unset environment (exit 2, `tools/mado-terminal.py:410`,
unconditional). This host's session sets all three XDG vars, so on the host's own session shape
"HOME unset ⇒ pin exit 1, empty stdout" is **false** — the pin prints a selection. If the w1
implementation bakes the literal wording, the C1 warm-cache tool models exit 1 where the pin
succeeds, i.e. D1's fix re-introduces a divergence class. Freeze-time fix: state the condition —
the pin exits 1 with empty stdout iff HOME is unset **and** any of XDG_CACHE_HOME /
XDG_CONFIG_HOME / XDG_DATA_HOME is unset (first `${VAR:-"${HOME}/…}"` default expansion, :148 /
:172); with all three set it runs normally without HOME. (ExecC1Diff H3 stated the condition; the
closure and the round-48 claims dropped it.) Raw outputs: `probes/` in this seat dir.

### 3.2 LOW — the spotcheck cites the frozen reference by a non-resolving path
§6.1 names "the frozen reference `l1-draft/mado-terminal.py@d7527d60`". At `d7527d608ad2…` the
committed path is `.ufo/waves/round-47/l1-draft/mado-terminal.py` (`registration.md:30` uses the
full path; `git cat-file -e d7527d608ad2…:l1-draft/mado-terminal.py` fails, the full path is
present). Content unaffected.

### 3.3 MEDIUM (freeze-time) — the declared fixture schema v2 cannot express three routed kill classes
The v2 extension in round-48 claims (mtime; prime; after.files/exec_add/exec_remove/env/mtime;
literal cache) still materializes regular text files only and the r47 counter force-sets PATH per
case. Concretely: MutC1Fixtures #7 (empty PATH element = cwd) is unkillable without a PATH field;
#8 (unreadable list ⇒ errexit exit 1) without a mode field; and ExecC1Diff H1's directory /
symlink-to-/dev/null shadow of a same-id valid file in a higher-preference dir without non-regular
path support. The tool's H1 fix is real at tip (§4), but its regression is invisible to schema v2
as declared. D3's two-valid-candidates case IS expressible (two `.desktop` files in one dir).
For the new counter: clause x must compare `cmd=` (CritC1Explain) **and** `cache=`
(MutC1Fixtures #9 — equally unchecked in r47), and SentC1Sandbox F4's remediation must carry over;
F1-F3's clause-i wording should be restated as the enumerated mount set before predicates freeze.

## 4. Closure facts re-derived (all held; no further defects found)
- Closure topology: `d40189c9..579f694b` = one commit, spotcheck lesson only; `registration.md` and
  all round-47 artifacts byte-unchanged at base; `.ufo/waves/round-48/` is empty at `579f694b`
  (claims.md is working-tree only — expected pre-integration).
- knowledge 63 → 64 (60edb66e → d40189c9); SOURCES S-rows 262 → 276, still 276 at base, top row
  S339, no S340 — matches the round-48 claims' "registry 276 rows, tops at S339".
- Pin identity and census exact (sha256, 1499 lines, 23 functions).
- H1 fix at tip re-measured live: valid `foot.desktop` in the XDG_DATA_DIRS dir + empty **directory**
  `foot.desktop` in the XDG_DATA_HOME dir → pin rc=1 (`line 985: read: 0: read error: Is a
  directory`), landed tool rc=1, stdout empty on both — agreement on the sharp shape. ExecC1Diff's
  disagreement was measured against the frozen l1-draft; the landed tool carries the fix,
  consistent with `receipts/h12-check.txt` and the spotcheck's hermetic claim. No contradiction in
  the closure on this point.

## 5. Residual risk and verification gaps
- Lane counters, gates and controls were not executed (reviewer standard); their committed receipts
  were read, not re-run (`h12-check.txt`, `ctl-c1.txt` exist at d40189c9).
- `census-after` (W04 ×17) not re-run; the session-material gate not re-run ("red" taken from the
  report line; R3's own seats are working it).
- No live FIFO or symlink-loop probe against the resolver (it blocks on the former; committed H1c
  receipts relied on).
- The fleet report's id-guard numbers (reg 262 / staged 147 / 70 collisions) not re-derived.
- The HOME-unset matrix covers the three HOME-defaulting vars; other HOME reads inside the resolver
  (e.g. after a cache hit) were not separately exercised.
- My scratch dir `/fast/scratch/hyaku/mado-r48/RevR47` is deleted after this review; probe outputs
  were copied to `probes/` here first. No tools installed; no host, compositor, or lane-tracked-file
  writes outside this seat dir and the seat report.
