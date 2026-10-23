# ConnSiblings — sibling-overlap scan (mado round 26, wave w1)

**Member:** `MadoR26.ConnSiblings` (UFO-FSD connector, leaf).  
**Lane:** `/home/vgpnk/Projects/shokunin/mado-shokunin`.  
**Scope:** read-only scan of `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/lessons`, `corpus/knowledge`, and `.ufo/waves` for overlaps with this round's two moves: (1) an isolated headless nested-compositor oracle, (2) static resolvers checked against a live program's own output. No lane files edited except this report. No tools run beyond grep/read.

## 1. Method and bounds

Searched the fleet with `grep -rn`/`grep -rli` over `corpus/lessons`, `corpus/knowledge`, and `.ufo/waves` for: `nested compositor`, `tinywl`, `bubblewrap`, `coredump`, `host safety`/`host-safety`, `oracle`, `do-nothing`, `label-keyed`, `label/position-keyed`. Each hit below was opened and read for context before citation. Runtime, binary, and scratch trees under `.ufo/waves/*/runtime` and `corpus/live` were excluded (they are copies, not lessons). Overlaps are grouped by the two moves plus the control-failure shapes that both counters' control waves depend on.

## 2. Move 1 — isolated headless nested-compositor oracle

### 2.1 The move itself and its pre-round-26 origin (mado, in-lane)

- `mado-shokunin/.ufo/waves/round-25/c1/count.py:45` — round-25's counter "starts nested Hyprland instances (wayland backend, windows on the live session)" on the operator's live session. That is the defect this round's isolated oracle fixes.
- `mado-shokunin/.ufo/waves/round-25/registration.md` (attempt-3 section) + `mado-shokunin/corpus/lessons/round-25.md:22` (M25-1) — the self-model oracle mistake: expected tables taken from the counter's own line model. The round-26 registration §"Host safety first" (lines 8–32) converts this into the bubblewrap + tinywl method: `--unshare-all --clearenv`, private `XDG_RUNTIME_DIR`, only `/dev/dri/renderD129`, `prlimit --core=0 --as=8000000000`, `dispatch exit` termination, and the `HOST_SAFETY hyprland_coredumps_before=… after=… delta=…` receipt line. Pilot result: coredump count stayed 1335 → 1335.
- `mado-shokunin/.ufo/waves/round-13/w1/Safety.md:99` — "With a nested or second compositor, the globals would be attributed to Hyprland 0.56.2 `efb5099…` (false provenance)." Directly supports the move's isolation invariant: a second compositor breaks provenance. Reuse: keep the `hyprctl -j instances` count == 1 and socket == `$WAYLAND_DISPLAY` guard (Safety.md:101) in any future probe.
- `mado-shokunin/corpus/lessons/round-25-verifier-spotcheck.md:10` — the round-25 spot-checker did not run the counter because "count.py starts nested Hyprland on the live session." Reuse: the round-26 sandboxed counter is now runnable by non-author reviewers; the spot-check's refusal was the correct host-safety stance and should remain the default for any un-sandboxed counter.

### 2.2 Host-safety and coredump lessons from sibling lanes (reuse + conflict)

- `mori-shokunin/corpus/lessons/2026-10-15-oracle-honesty-crash-masking.md:1`–`:22` — a masked crash (`|| true`) and a genuine repair produce the identical tally (`matched=10 total=27`) when fixtures read only last-commit epoch/mtimes. Reuse: the round-26 oracle must self-assert preconditions (exec-line stripping, instance termination) rather than rely on a green tally; the `HOST_SAFETY` before/after coredump line is exactly such a self-assertion. Conflict: none, but mori's lesson is about fixture setup crashes, not compositor crashes — do not conflate "no coredump delta" with "fixtures valid"; the two must be checked separately.
- `mori-shokunin/corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md:19`–`:35` — identity leak: case id in path/env lets a no-logic SUT print the expected row and score 27/27. Reuse: round-26's M25-2 repair (random mkdtemp case dirs, shuffled run order) is the direct descendant; the registration's "label-free case paths" (R1) is the same countermeasure. Conflict: mori's fix also added shape-invariance (same bytes under two random names → identical grade/stdout); mado's counter does not yet have a shape-invariance case for animation tables — a gap mado should close if a label-keyed control ever approaches the target.
- `tsukuroi-shokunin/corpus/lessons/round-33.md:51` and `:42` — host observation: "the boot-0 coredump count rose from 265 to 1603 between about 07:14Z and 07:44Z" during the round, and `MutR1CounterV4` found "the unmodified tip failed that view in the same minute because the host's boot-0 coredump count was climbing." Reuse: mado's before/after coredump check is necessary but not sufficient — a climbing host count can make a live view fail even with no mado-caused coredump; the counter's `delta=…` must be read, not just "stayed equal." Conflict: tsukuroi's coredumps come from the host's own boot-0 crashes (not mado's nested compositors); mado's pilot kept delta 0, but a concurrent tsukuroi-class storm on the host would invalidate a before/after comparison even with perfect isolation. Mitigation: run mado counters when host coredump rate is stable, or pin the comparison to mado's own instance PIDs.
- `tsukuroi-shokunin/corpus/lessons/round-32.md:36`–`:47` — K11 (label-noise floor) met the target by routing on wrong statistics in fixtures plus cached host constants (clusters 2; total errors minus 52); the thinned live view changed only the coredump count, so a kill-events constant survived it. Reuse: this is the exact failure shape a future animation-table label-keyed control would exploit (constant keyed on one class the live view varies); mado's C1 label-keyed control is capped at 37/41 for exactly this reason. Conflict: mado's live view varies both node set and bezier set, which is stronger than tsukuroi's single-class thinning — but only if both are actually compared; verify the counter compares full sets, not counts.
- `tsukuroi-shokunin/corpus/lessons/round-33.md:29`–`:33` — holds (provider safety-filter refusals) for open adversarial search items X01/X02; the read-side limit (a target that learns it is traced through procfs, S181) stays a named, unscored limit. Reuse: mado's C1/C2 counters already run tools in bubblewrap with cleared env and no `/run`; the procfs read-side limit (S181) is the same boundary mado relies on. Conflict: none, but mado should not claim procfs is closed — it is a named limit, not a solved one.

## 3. Move 2 — static resolvers checked against a live program's own output

### 3.1 Sibling lanes that used a running program as the oracle (ConnOracleGaps inventory)

`mado-shokunin/.ufo/waves/round-25/a3w1/reports/ConnOracleGaps.md:23`–`:30` already inventoried three sibling patterns mado should reuse:

- `kaidoku-shokunin/corpus/lessons/round-31.md:39` — "a row for node:sqlite / libsqlite3 builds (host readers used as oracle and probe, not learning sources)." Reuse: kaidoku's discipline of distinguishing oracle/probe (runtime) from learning source (pinned bytes) — mado's C1/C2 should keep the same split: Hyprland is the oracle, wiki/Hyprland source is the learning source. Conflict: kaidoku's host readers run on the real host database; mado's oracle runs in a sandbox — the host-reader pattern would break mado's isolation. Use only the sandboxed oracle.
- `tsukuroi-shokunin/corpus/lessons/round-30.md:72` — "CriticCounterV2 installed cmarkgfm 2025.10.22 from PyPI with uv pip into a private venv under its scratch directory (renderer oracle)." Reuse: the private-venv-under-scratch pattern for installing an oracle dependency without touching the host; mado's tinywl build under `/fast/scratch/hyaku/mado-r26/wlroots` follows the same containment. Conflict: tsukuroi installs a Python package; mado builds a C binary — the uv-pip channel does not apply to wlroots/tinywl, but the scratch-containment rule does.
- `mori-shokunin/corpus/lessons/2026-10-15-forgeable-oracle-visible-fixtures.md:1` — forgeable oracle visible fixtures (covered in 2.2 above). Reuse: the forgery probe (a stub that reads identity and prints the expected shape) as a standing control in every counter. Mado's C1/C2 control waves should include an explicit forgery probe, not only do-nothing/junk/label-keyed shapes.

### 3.2 Control-failure shapes: do-nothing and label-keyed controls meeting a counter

These are the shapes the round-26 control waves (K1*/K2*) must kill; sibling lanes already documented them.

- `mado-shokunin/corpus/lessons/round-25-verifier-spotcheck.md:72`–`:75` — controls under v4: K4LabelKeyed 37/41 (best), K4EncodedTable 31/41, K4EasyOnly 4/41; none `TARGET_MET`. The round-26 K1 label/position-keyed control must reproduce this ceiling or lower; if it meets 41/41, the counter is broken (M25-2).
- `chousa-shokunin/corpus/lessons/round-29.md:28` — "v1 label-keyed control `QUOTE_REOPEN_MATCH=82/82` without fetching … design v2 added 48 page-sampled items drawn at run time; the same control fell to 106/130." Reuse: the run-time-drawn (not committed) item set is the countermeasure that kills label-keyed controls; mado's 40 generated cases are already run-time-drawn, which is why label-keyed stops at 37/41. Conflict: chousa's items are pages sampled at run time; mado's are config cases generated at run time — same principle, different substrate. No conflict.
- `kake-shokunin/corpus/lessons/round-35.md:7`–`:81` and `round-35-verifier-spotcheck.md:96` — round 34 was rejected because a do-nothing control met each declared counter; "No do-nothing control reaches the target" is now a binding addendum §9 rule. Reuse: mado's registration already lists do-nothing as a named control shape; ensure the receipt explicitly shows it below target, not just "exit 1."
- `kama-shokunin/corpus/lessons/round-26.md:79` — "data dispatched with the shortcut-control slot unfilled; the counter is met by a shortcut found after data … by hiding a source literal … with a `\u00XX` escape and letting `server-common.cpp:1375` echo it." Reuse: this is the unicode-escape echo shape; mado's embed_hits scan (≥12-char arg/description strings) must be checked against escape-decoded strings, not raw bytes, or a `\u00XX`-hidden literal survives. Conflict: mado's embed check is a plaintext substring scan; kama's attack shows plaintext scans miss encoded forms. This is a real residual risk for C2's embed_hits=0 claim.
- `mori-shokunin/corpus/lessons/round-34.md:90`–`:95` — the pre-data battery (16 controls) missed a label-keyed, harness-keyed shortcut that met P-C1-A1 after data; QUALITY 99 was the fix. Reuse: mado's C1 control list (registration §Controls) does not include a harness-keyed (mountinfo/paths/mtimes) control that reads the case identity from the sandbox; M25-2 is the known channel. The round-26 R1 repair (random case dirs) closes the mountinfo channel but not a fixture-content-keyed channel — add a content-keyed forgery probe.
- `mado-shokunin/corpus/lessons/round-24-verifier-spotcheck.md:134` — "the same mismatch is present at base (do-nothing 1/12): reported, not caused." Reuse: baseline-mismatch reporting discipline — a control that fails at base is a base property, not a regression.

### 3.3 Static-vs-live agreement checks (mado's own prior art)

- `mado-shokunin/corpus/knowledge/hyprctl-verification-layer.md:158` (per registration §C1) — the animations row is "agreement at count level; directive→entry expansion `[INF]`." The round-26 C1 move closes this `[INF]`. Reuse: keep the count-level agreement as a separate, weaker claim so the new entry-level claim is not conflated with it.
- `mado-shokunin/corpus/lessons/round-25.md:76`–`:83` — residual `{{…}}` left literal (9/10 hand-made trees agree) and reads outside `--home` stay stated limits. Reuse: C2 must not regress round-25 behaviour (the 20 V3 cases are the no-harm half); the `{{…}}` handling is the new capability, not a rewrite.

## 4. Conflicts and risks to carry into the report

1. **Host coredump drift (tsukuroi) vs. mado's before/after check.** Mado's pilot held delta 0, but a concurrent host coredump storm (tsukuroi 265→1603) would make the comparison meaningless. Mitigation: compare against mado's own instance PIDs, not the global count, or run when host rate is stable.
2. **Plaintext embed scan vs. encoded forms (kama).** `embed_hits=0` is a plaintext audit; a `\u00XX`-hidden literal (kama's attack) survives. Describe embed_hits as a plaintext audit only (M25-3 residual), and add an escape-decoded scan as a second, non-gating check.
3. **Label-keyed via fixture content, not identity (mori).** R1 (random case dirs) closes the mountinfo channel but not a content-keyed forgery. Add a shape-invariance case and a content-keyed forgery probe to C1.
4. **Procfs read-side limit (tsukuroi S181) is unsolved.** Mado relies on bubblewrap clearing env and hiding `/run`; procfs initial-environment reads are a named limit, not a closed boundary. Do not claim otherwise.
5. **Oracle as host reader vs. sandbox (kaidoku).** Reuse kaidoku's oracle/probe split, but never run the oracle on the host — only through `harness/oracle.py`.

## 5. Proposed move (non-obvious synthesis)

Synthesize the three strongest sibling patterns into one addition that improves C1's coverage axis without harming operability:

- From **mori**: add a **forgery probe** to the C1 counter — a stub control that reads whatever identity it can see (case dir name, fixture bytes, env) and prints the expected animation table shape; the counter must reject it. This is the only probe that finds the label-keyed class, and it is not currently in mado's control list.
- From **mori**: add a **shape-invariance case** to C1 — the same config bytes under two random directory names must yield identical node/bezier sets and stdout. This kills name-keyed (and invocation-order) sniffers.
- From **kama**: extend the **embed scan** to run over escape-decoded strings (JSON `\u00XX`, `##` escapes, `{{…}}` contents) as a second, reported-but-non-gating check, so a hidden literal is at least visible even if not counted in embed_hits.

Net effect: C1's coverage moves from "agreement at count level + entry expansion" to "entry expansion that is also identity-blind and shape-invariant," which is the property the round-25 mori lessons showed is necessary and not sufficient. No change to the frozen counter's target (41/41) or to C2's 51/51; the additions are controls and checks, not new acceptance criteria, so no axis is harmed.

## 6. Verification (read-only, no runs performed)

- All citations above were verified by direct `read` of the named files; line numbers are from the committed bytes at the fleet tip.
- No counter, harness, corpus, tool, or source file was edited; only this report was written.
- No git/jj write command was run; no nested compositor, hyprctl write verb, or live-compositor action was performed.
- Tooling: none installed or upgraded for this scan.

## 7. Verdict line

`CONNECTOR ConnSiblings: 12 overlaps (4 nested-compositor/host-safety, 5 static-resolver/oracle, 3 control-failure-shape); 5 risks; proposed move = forgery-probe + shape-invariance case for C1 + escape-decoded embed scan for C2. No edits.`
