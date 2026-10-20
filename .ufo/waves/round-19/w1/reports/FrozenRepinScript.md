# FrozenRepinScript — script written; (a) byte-identical baseline, (b) known misses flip, (c) drop refused

Assigned deliverable: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/frozen-repin.py`
(644 lines, executable, sha256 `7cc8b2cdd7a74c9a2b3131c07b6b4e921d32147fedc58c86afb0027c5688517c`).
No lane file other than this script and this report was written; everything else lives in `/tmp`.

## What it does

CLI: `frozen-repin.py --from SRC --to DIR --tool PATH [--allow-new-findings]`; exit 0 written,
1 refused, 2 usage/could-not-evaluate; first line `MADO_FROZEN_REPIN: <outcome>` then one JSON object
(`schema mado-frozen-repin-verdict-v1`). Behaviour, with anchors:

- Source pin validation (`frozen-repin.py:140`): schema `mado-tripwire-frozen-v1`, `inputs/<name>.jsonl`
  paths only, 64-hex digests, unique input rows, permit a subset of the three tool classes, exit/label
  pair reachable, findings/known files listed, known/expected line overlap refused (the tool's own
  `--frozen` rule), no duplicate JSON keys (`:107`).
- Input copy (`:205`, `:408`): an unlisted `*.jsonl` under `SRC/inputs`, a symlinked `inputs/`, a leaf
  symlink or a digest mismatch is exit 2; every listed input's sha256 is checked against the source pin
  *before* copying, and the staged copy's digest is re-checked after writing.
- Scan: `[sys.executable, "-I", tool, "--scan", "inputs/<name>.jsonl", ...]` (source order; `--permit`
  appended only when the source permit is non-empty), cwd = the private staging directory under DIR's
  parent. Findings are rejected as could-not-evaluate unless the verdict schema/exit/label/unpermitted
  are self-consistent and every scanned file digest equals its pin (`:240`).
- Decision: a source expected finding keyed on `(file, line, class, rule)` that disappears refuses
  (`source_finding_missing`); a finding on a `(file, line)` that is neither expected nor a known miss
  refuses (`finding_on_unexpected_line`) unless `--allow-new-findings` (`:484`-`:487`).
- Output: `expected_findings` = the tool's findings in tool order as `{file, line, class, rule}`;
  `known_misses` = source rows still missed, kept verbatim; `permit`/`expected_exit`/`expected_label`
  from the source permit and the scan verdict. `README.md` first line
  `RECEIPT tool=… tool_sha256=… utc=… argv=…` (`:314`); `provenance.json` is the source object plus
  `repinned_from` (an existing note becomes a list, so re-pins compose).
  Self-check before publication: the staged baseline is replayed with the same tool's `--frozen`
  (`:522`); only `frozen_match`, with matching `tool_sha256` and `expected_sha256`, is accepted.
- No-write guarantee: everything is built in a `mkdtemp` staging dir and published by one
  `os.replace(staging, dst)` (`:593`); a refusal/failure removes staging, so DIR never exists.
  Staging is chmod 0755 (`:448`) because `mkdtemp` is 0700.

## Tests on /tmp (all commands executed)

Fixture tools are copies of `tools/mado-tripwire.py` (sha256 `c1ae45a7573e…13c70cd`, the round-19
draft rebase base).

**(a) Current tool → identical expected, known misses kept**

```
python3 -I .ufo/waves/round-19/frozen-repin.py --from .ufo/waves/round-18/frozen \
  --to /tmp/v-a --tool tools/mado-tripwire.py
```
→ `MADO_FROZEN_REPIN: written`, exit 0; payload `expected_sha256=4f3534ae33d8daba7d8c682e1fc97c283185667c4f3c3c91235cc53498fd2ed9`,
`expected_findings=8`, `known_misses_kept=3`, `counts={"host_mutation":6,"live_probe":1,"package_query":1}`,
`replay=frozen_match`. `cmp /tmp/v-a/expected.json .ufo/waves/round-18/frozen/expected.json` → identical;
`diff -r` of `inputs/` → identical; `python3 -I tools/mado-tripwire.py --frozen /tmp/v-a` →
`MADO_TRIPWIRE_FROZEN: frozen_match`, exit 0. Dir modes: `755 /tmp/v-a`, `644 expected.json`.

**(b) Toy rule on `pacman -Q` inside an eval string → known misses become findings**

Patch (`diff -u`, sha256 `3175a67b7598…a3`):

```
+TOY_PACMAN_Q = re.compile(r"pacman['\"]?\s*,\s*['\"]?-Q|pacman\s+-Q")
 def classify_eval(code, language):
     ...
     hits = []
+    if TOY_PACMAN_Q.search(code):
+        hits.append(("package_query", "pacman:-Q", "pacman", "pacman -Q"))
```

Run with `--tool /tmp/r19-toys/tool-toy.py --to /tmp/v-b` → exit 0, `written`, `expected_findings=11`,
`package_query=4`, `known_misses_kept=0`, `known_misses_dropped=[r14-source-safety:2, r14-source-safety:3,
r13-root:4]`; `/tmp/v-b/expected.json` has `known_misses: []` and the three new
`("inputs/…jsonl", 2|3|4, package_query, pacman:-Q)` rows; `tool-toy.py --frozen /tmp/v-b` →
`frozen_match`, exit 0. (The toy rule also fires on r13-global-capture:1, an *expected* line, producing
one duplicate key there — the line rule permits it; `new_findings_accepted=0`.)

**(c) Mutant that drops a finding → refusal, no DIR**

Patch: `hits = [h for h in hits if h[1] != "wayland-info"]` injected before the append loop
(sha256 `bdd03bb530f8…b832`). Run → exit 1, `MADO_FROZEN_REPIN: refused`,
`refusals=[{"kind":"source_finding_missing","rows":[{"class":"live_probe","file":"inputs/r13-global-capture.jsonl",
"line":1,"rule":"wayland-info"}]}]`, `scan_exit=1`, `expected_findings=7`, `target_written=false`;
`/tmp/v-c` absent; no `/tmp/.frozen-repin-*` residue.

## Additional checks (executed)

- **New line without the flag**: toy adding `git ls-remote` at `classify_shell` depth 0
  (sha256 `93bf12ba8361…9e4c`) → exit 1, `finding_on_unexpected_line` naming
  `r15-libinput-events:3` and `r14-review-source-bar:4`, DIR absent. Same tool with
  `--allow-new-findings` → exit 0, 10 findings, the 2 rows in `new_findings_accepted`, 3 known misses
  kept, README line `findings on lines that were neither expected nor a known miss: 2 (accepted by
  --allow-new-findings)`; `--frozen` replay succeeds.
- **Usage**: no args → stderr usage + `MADO_FROZEN_REPIN: could_not_evaluate`, exit 2; `--help` → exit 0.
- **Non-empty target**: `/tmp/r19-repin-nonempty/sentinel` kept, exit 2, message
  `--to exists and is not empty`.
- **Tampered source**: one appended byte to a copied `r13-root.jsonl` → exit 2
  `source input does not match its pin: inputs/r13-root.jsonl`, target absent.
- **Second-generation re-pin** (`/tmp/v-a` → `/tmp/v-a2`): exit 0, `cmp` expected.json identical,
  `provenance.json.repinned_from` becomes a 2-element list with both source expected digests.
- **Byte-stability**: expected.json is written as `json.dumps(..., indent=2, ensure_ascii=True) + "\n"`,
  which reproduces the round-18 file byte-for-byte, so (a) is an exact identity, not a set comparison.

## Notes for L1

- On the current tool the produced baseline equals round-18's byte-for-byte, i.e. the three known
  misses are still missed: re-pinning alone does not move C3's 3/6 — the drafts/toy rule do.
  Regenerating a round-19 baseline is `python3 -I .ufo/waves/round-19/frozen-repin.py --from
  .ufo/waves/round-18/frozen --to .ufo/waves/round-19/frozen --tool tools/mado-tripwire.py`; the
  target must not already exist (exit 2 if non-empty), and the README RECEIPT then pins the tool digest.
- The refusal rule is the only recall guard: `expected_findings` is by construction the tool's own
  output, so a tool that silently loses a finding on a *new* line cannot be caught here except by the
  expected/known line rule. The README states this limit for readers.

## Limits

- Exercised only the round-18 five-input baseline and three `/tmp` tool mutants; non-empty `permit`,
  `permitted_only`/`clean` sources, `--permit` forwarding, and the 300 s tool timeout were not
  exercised (the permit path is straightforward but unrun — [INFERENCE] it composes).
- The scan is invoked with `sys.executable` (`/usr/bin/python3`), not the literal token `python3`;
  the recorded argv is exact and the interpreter is the same one running the script.
- `CLASSES` is pinned to the three classes of this tool; a tool that adds a class would be rejected as
  could-not-evaluate rather than written (deliberate, keeps the output replayable).
- No build/lint/selftest of the real tool, no live gate, no host command beyond reads in the lane and
  `/tmp` scratch. Round-18 provenance line claims, SOURCES rows and the tripwire drafts were read only
  as inputs, not audited.

## Installs

none.
