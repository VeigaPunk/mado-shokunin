#!/usr/bin/env python3
"""Build .ufo/waves/round-74/w1-spec.json (one v1 wave, 13 seats)."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE = os.path.join(LANE, ".ufo", "waves", "round-74")
REV = "b73db773aaf67c9b26c8cf1a4cd567dec3af11f4"
BASE = "bd5a971532f37df85a78f6f566dd1e649b79de11"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + """
Round mado 74, ONE v1 wave (13 seats). Claims: C1 calibration (the credit rule requires the run's
own echo of a per-run challenge, so a captured summary replayed with its own matching detail lines
earns no credit; the held round-72 rule credits all four replay cases) and C2 operability (the
guard census counts a two-hop object alias and a one-hop `os.environ` alias; the held round-73
classifier misses exactly the four new positives). The L1 holds the planner seat (the validator
rejects `planner` as a swarm role); no planner is dispatched.

Read FIRST:
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/claims-declaration-r74.md
(the frozen claims, predicates, counting commands, kill rules, targets and limits; base
`bd5a971532f37df85a78f6f566dd1e649b79de11`, freeze+instruments
`b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`).

Committed receipts (re-read, do not rewrite):
- `.ufo/waves/round-74/measurement-c1-r74.txt` -> `cases=12 correct=12 base_correct=8
  verdict=TARGET_MET`, rc 0.
- `.ufo/waves/round-74/measurement-c2-r74.txt` -> `population=20 readers=13 guarded=13
  unguarded=0 controls=36/36 base_controls=32/36 verdict=TARGET_MET`, rc 0.
- `.ufo/waves/round-74/control-baseline-r74.txt` (the pre-freeze do-nothing legs: held credit
  8/12, held classifier 32/36).

Hard bounds, every seat:
- Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-74/w1/<your name>/.
  Never edit a committed lane file (production instruments, corpus, SKILL.md, SCORECARD.md,
  LOG.md, README, SOURCES.md); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash, no jj mutation);
  read-only git (`show`, `ls-tree`, `rev-parse`, `status`, `log`) is fine. Never write the fleet
  repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, `scripts/`, `templates/`
  or MANIFEST.json.
- Never message `agent://all`; reply only to your L1 (`MadoR74`) or nothing.
- Scratch: /fast/scratch/hyaku/mado-r74/<your name>/ (create it; pass it explicitly; never use
  /tmp; delete it before you finish, after copying any receipt you cite into your own dir).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps this
  task, first reading /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate) and
  recording tool/version/channel/reason in your report. ALL pacman transactions are PAUSED
  host-wide this run: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or report
  that you needed one; never `pacman -Sy/-S/-Syu/-U/-R`, never restart a host service.
- Read-only host posture: do not probe the compositor, session, services, network services or
  ~/.config; no live-config writes; no credential material in any file.
- Every `Report:` trailer path the validator renders is relative to
  /home/vgpnk/Projects/shokunin/mado-shokunin — write it at
  /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>. End your final output with one line
  `Report: <repo-relative path>` naming the file you actually wrote, then a 3-line summary.
"""

ITEMS = [
    dict(name="R74ExecC1", role="executor", body="""
Independently drive claim C1's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin` and run, with your own scratch dir:
   `python3 -I quality/counters/c1-r74-replay-witness.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c1-replay-cases-r74.json --scratch-root /fast/scratch/hyaku/mado-r74/R74ExecC1/run`
2. Run its `--selftest` with the same scratch root, and the rule's own selftest
   (`quality/counters/c1-r74-witness-rule.py --selftest`).
3. Reconcile with the committed receipt `measurement-c1-r74.txt`: same last line, same rc? Name
   every difference.
4. Read `quality/counters/c1-r74-witness-rule.py:credit` and the twelve modes in
   `quality/counters/c1-r74-replay-witness.py:LANE_TEMPLATE`. For each of the four replay modes,
   state in one sentence which part of the rule refuses it, and confirm from the per-case lines
   (`MADO_R74_SCENARIO`) rather than trusting the summary.
5. Probe one extra shape of your own against the committed rule (a witness printed after the
   summary; a witness on stderr only; two summaries with one witness) by importing the rule with
   `runpy` in a scratch script; report the answer and whether the frozen predicate covers it.
Write `<your dir>/R74ExecC1.md`. `Report: .ufo/waves/round-74/w1/R74ExecC1/R74ExecC1.md`.
"""),
    dict(name="R74ExecC2", role="executor", body="""
Independently drive claim C2's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin` and run:
   `python3 -I quality/counters/c2-r74-shapes.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 --base-rev bd5a971532f37df85a78f6f566dd1e649b79de11 --controls .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root /fast/scratch/hyaku/mado-r74/R74ExecC2/run`
2. Run its `--selftest` with the same scratch root (pass `--controls` too).
3. Reconcile with `measurement-c2-r74.txt`: same last line, same rc? Name every difference.
4. From the `MADO_R74_CONTROL leg=base ... correct=no` lines, list exactly which four cases the
   held round-73 classifier misses, and confirm each is one of the eight appended cases.
5. Read `twohop_guard`, `object_alias_map`, `canonical_dotted`, `environ_alias_names` and
   `environ_alias_guard` in `quality/counters/c2-r74-shapes.py`. For each of the four new
   positives, state in one sentence the dominance bound it exercises, and say which of the four
   new negatives would break if that bound were dropped.
6. Independently count the population with `git ls-tree -r --name-only <rev> -- quality` filtered
   to `quality/check-*.py` and state whether 20 readers / 13 guarded reproduce.
Write `<your dir>/R74ExecC2.md`. `Report: .ufo/waves/round-74/w1/R74ExecC2/R74ExecC2.md`.
"""),
    dict(name="R74ExecHarm", role="executor", body="""
Run the round's harm watch and write the receipt.

1. `bash tools/mado-verify.sh --selftest` (expect `MADO_SELFTEST: 460/460`, exit 0).
2. `python3 -I quality/check-index.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`
   (expect indexed=89/89 missing=0 dangling=0 duplicates=0 at this commit, exit 0).
3. `python3 -I quality/check-tool-ledger.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4 --scratch-root <yours>`
   (expect 127 rows, 0 uncovered at this commit; the two new instruments are not yet registered —
   report that as the expected pre-registration state, do not edit the ledger).
4. `python3 -I quality/check-axis-scores.py --repo . --rev b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`
   and report its verdict.
5. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
   — paste the exit code and the last line.
6. Frozen-instrument identity: `git rev-parse bd5a9715:<p> b73db773:<p>` for
   `quality/counters/c1-r72-landing-controls.py`, `quality/counters/c1-r73-summary-mutants.py`,
   `quality/counters/c2-r73-shapes.py`, `tools/mado-verify.sh`, `quality/landing-counters.sh`;
   every pair must be identical.
7. Report the numbers with their commands and exit codes in `<your dir>/harm-watch-r74.txt`, then
   write `<your dir>/R74ExecHarm.md` naming any deviation. If a check fails, report it exactly;
   do not repair it.
`Report: .ufo/waves/round-74/w1/R74ExecHarm/R74ExecHarm.md`.
"""),
    dict(name="R74ScribeC1", role="scribe", body="""
Draft (do not commit) the C1 knowledge entry the L1 will apply.

Read `.ufo/waves/round-74/claims-declaration-r74.md` § C1, `measurement-c1-r74.txt`,
`control-baseline-r74.txt`, `quality/counters/c1-r74-witness-rule.py` and
`quality/counters/c1-r74-replay-witness.py`. Also read the fetched source
`.ufo/waves/round-74/fetch/secrets.rst.1` around `token_hex` (line 78-84).

Write `<your dir>/replay-witness-credit-r74.md` in the corpus entry shape used by
`corpus/knowledge/control-set-mutant-kill-r73.md`: `source:` line first (cite `S450` and the
own-work receipts), then `verified-at:` (`b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`), then
`recheck:` (the counting command), then the rule in one paragraph, the twelve-case table (name,
mode, expectation, which rule refuses it), the measured before→after with the exact contract
lines, the declared limits, and the open wiring question (the frozen round-72 harness is not
edited). Every number carries its command. No claim beyond the receipts.
`Report: .ufo/waves/round-74/w1/R74ScribeC1/replay-witness-credit-r74.md`.
"""),
    dict(name="R74ScribeC2", role="scribe", body="""
Draft (do not commit) the C2 knowledge entry the L1 will apply.

Read `.ufo/waves/round-74/claims-declaration-r74.md` § C2, `measurement-c2-r74.txt`,
`control-baseline-r74.txt`, `quality/counters/c2-r74-shapes.py` (`twohop_guard`,
`environ_alias_guard`) and the fetched sources `.ufo/waves/round-74/fetch/simple_stmts.rst.1`
(lines 160-165) and `os.rst.1` (lines 196-198).

Write `<your dir>/guard-carrier-twohop-environ-alias-r74.md` in the corpus entry shape used by
`corpus/knowledge/guard-carrier-global-environ-r73.md`: `source:` first (cite `S451`, `S452` and
the own-work receipts), `verified-at:` (`b73db773aaf67c9b26c8cf1a4cd567dec3af11f4`), `recheck:`
(the counting command), then the two carrier shapes with their dominance bounds, the eight new
cases with expectations, the population 20/13/13/0 and the 36/36-vs-32/36 measurement, the
declared limits (line order, one edge, no `del` cancellation in the generic flow). Every number
carries its command.
`Report: .ufo/waves/round-74/w1/R74ScribeC2/guard-carrier-twohop-environ-alias-r74.md`.
"""),
    dict(name="R74ScoutSources", role="scout", body="""
Re-open and verify the three sources this round cites, and prove the registry guards.

1. Fetch each three times into your own dir and compare digests (byte-identical required):
   `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/secrets.rst`,
   `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`,
   `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/os.rst`.
   Report size + sha256 for each, and whether they match
   `.ufo/waves/round-74/fetch/*.1` (secrets `289ff11e…`, simple_stmts `d4320642…`, os
   `2d0f2892676e1cf9547be2bd94cfe2a6221dddea82d52cb2475d4a3d819b2ae5`).
2. Locate each quote with `grep -n` and state line numbers and word counts (≤25):
   secrets.rst `token_hex` "Return a random text string, in hexadecimal…";
   simple_stmts.rst "If the target is an attribute reference: …";
   os.rst "This mapping may be used to modify the environment as well as query the environment."
3. The round-73 spot-check routed D1: `corpus/SOURCES.md` S448 records a false sha256
   (`2d0f2892676e1cf9f0d8e61c63a2e70a86f0e0a5cdb6b06dd7b7d2c9b8b88a4e`). Sweep every lane mention
   (`grep -rn`), state the true digest, and draft the exact superseding row text (S452) whose
   `teaches` opens `supersedes S448 — `.
4. Id-collision guard proof: build a scratch registry with an indented `  | S450 |` row plus the
   staged S450 id, run the 0–3-space extractor, and show `collisions` is nonempty; then run the
   same extractor over the real registry (max id S449) and the three proposed ids and show no
   collision. Paste the commands and outputs.
Write `<your dir>/R74ScoutSources.md`. `Report: .ufo/waves/round-74/w1/R74ScoutSources/R74ScoutSources.md`.
"""),
    dict(name="R74ScoutFrontier", role="scout", body="""
Read the frontier inputs and report what the next round can stand on.

1. Read `considerthese/` (newest file first, 2026-10-28) and name at most ONE still-unimplemented
   proposal that fits this round's instrument ground; quote the file:line and say how the lane's
   own bar (PROVINCE/QUALITY) grounds it. If nothing fits, say so with the sweep.
2. Read `corpus/lessons/round-73-verifier-spotcheck.md` § Routed defects and disposition D1–D7
   against the round-74 declaration's dispositions: which are actually closed by files in this
   round's tree (check the paths), which are still open, and which are operator-owned.
3. Read `corpus/README.md` § Frontier (the round-73 bullet) and `SCORECARD.md` § Planned (round
   74) and state, in one sentence each, which planned item this round lands and which it does not.
4. Sibling overlap: search sibling lane corpora read-only (`grep -rl` over
   /home/vgpnk/Projects/shokunin/*-shokunin/corpus) for "nonce", "challenge", "witness",
   "GIT_NO_REPLACE_OBJECTS", "guard census"; report any lane that holds the same ground and the
   path. Do not write outside your dir.
Write `<your dir>/R74ScoutFrontier.md`. `Report: .ufo/waves/round-74/w1/R74ScoutFrontier/R74ScoutFrontier.md`.
"""),
    dict(name="R74RevC1", role="reviewer", body="""
Attack the C1 rule. Read `quality/counters/c1-r74-witness-rule.py` and
`.ufo/waves/round-74/controls/c1-replay-cases-r74.json`, then build at least eight new fixtures in
your own dir (import the rule with `runpy`) and report each as accept/reject plus whether the
frozen predicate says so:

- witness printed after the summary line;
- witness on stderr only, summary on stdout;
- two summaries (`2/2` then `1/2`) with one witness;
- a witness line with trailing spaces or CRLF;
- an uppercase or 17-hex witness token;
- a summary with `p > n`;
- a captured block whose detail lines are genuine but whose witness is stale (the round-72 limit);
- the same nonce replayed by two different children (can the rule tell?).

For every disagreement between the rule and the frozen sentence, name the defect class and the
exact line. Do not edit any committed file. Write `<your dir>/R74RevC1.md`.
`Report: .ufo/waves/round-74/w1/R74RevC1/R74RevC1.md`.
"""),
    dict(name="R74RevC2", role="reviewer", body="""
Attack the C2 classifier. Read `twohop_guard`, `object_alias_map`, `canonical_dotted`,
`environ_alias_names`, `environ_alias_guard` and `has_guard` in
`quality/counters/c2-r74-shapes.py`, then build at least eight new fixtures in your own dir and
report `classify`'s answer against the declared bound:

- an alias rebound between store and launch (`r = cfg.runner; r.env[KEY] = "1"; r = other; …`);
- two aliases of the same dotted path (`a = cfg.runner; b = cfg.runner`);
- `dict(env, PATH="/usr/bin")` and `{**env, "X": "y"}` after a store;
- a store on a two-level attribute chain (`r.cfg.env[KEY]`);
- `r = cfg.runner` at module level, store inside a function, launch in another function;
- an `os.environ` alias shadowed by a function parameter;
- `del env[KEY]` (the declared unmodelled gap — confirm it is still counted);
- a store into an alias whose RHS is `os.environ.copy()`.

For each: does the classifier's answer follow the declared bound? Name every false accept or false
reject with the source line. Do not edit any committed file. Write `<your dir>/R74RevC2.md`.
`Report: .ufo/waves/round-74/w1/R74RevC2/R74RevC2.md`.
"""),
    dict(name="R74Critic", role="critic", body="""
Falsify the two claims. Work from committed bytes only.

1. Re-derive the target arithmetic from the receipts: C1 `cases=12 correct=12 base_correct=8`;
   C2 `population=20 readers=13 guarded=13 unguarded=0 controls=36/36 base_controls=32/36`. For
   each, count the per-case `correct=no` lines in the base leg and name them.
2. Are the twelve C1 cases distinct? Extract each mode's output by running the fixture lanes
   yourself (build them from `LANE_TEMPLATE` in a scratch dir) and report any two modes with
   byte-identical output. Same for the eight new C2 cases (name, src) — any duplicate?
3. Does the held leg really run the held rule? Verify `--base-rev` resolves to
   `bd5a9715…` and that `git show bd5a9715:quality/counters/c1-r72-landing-controls.py` and
   `…:quality/counters/c2-r73-shapes.py` are the files the counter loads; report their sha256.
4. Freeze order: the declaration, the frozen sets, the pre-freeze baseline and both instruments
   landed in ONE commit (`b73db77`). Say whether that weakens the "frozen before data" claim, and
   what receipt proves the order (the baseline's held legs). Name any counterexample where a
   do-nothing control meets the target.
5. Padding: are any of the 36 C2 cases carried byte-identically from round 73 (hash-checked)? Are
   any new cases not load-bearing (identical answer under both rules)? Name them.
Write `<your dir>/R74Critic.md` with a verdict per claim (`stands`/`fails`) and the evidence.
`Report: .ufo/waves/round-74/w1/R74Critic/R74Critic.md`.
"""),
    dict(name="R74Mutant", role="mutation-tester", body="""
Mutation-test the two new instruments' decision rules.

Build four mutations of the C1 rule and four of the C2 guards in your own dir (copy the committed
file, apply one literal substitution each, assert it applies exactly once), then score each mutant
with the frozen case sets:

- C1-M1: drop the witness comparison (`return token is not None`);
- C1-M2: accept any parsed witness token, not the challenge (`return token is not None and len(token) == 16`);
- C1-M3: compare the FIRST witness line instead of the last;
- C1-M4: drop the `count_fails` check.
- C2-M1: canonicalise only when the call side crosses the alias (drop `crossed_store`);
- C2-M2: ignore the replacement set in `twohop_guard`;
- C2-M3: treat any Name alias as an `os.environ` alias;
- C2-M4: drop the `del` cancellation in `environ_alias_guard`.

For each mutant, count how many of the frozen cases it gets wrong (use the same scoring as the
counters: 12 cases / 36 cases) and state whether the frozen set would kill it (score < target).
Name any mutant the set does NOT kill — that is the finding. Do not edit committed files.
Write `<your dir>/R74Mutant.md` with the kill matrix.
`Report: .ufo/waves/round-74/w1/R74Mutant/R74Mutant.md`.
"""),
    dict(name="R74Conn", role="connector", body="""
Cross-claim and cross-lane pattern finding.

1. Name the shared pattern of this round's two claims (a control set certifies an instrument only
   if it separates a named mutation/limit of that instrument) and check whether the round's
   evidence actually instantiates it: for C1, which case is the sole separator of the missing
   witness check? For C2, which case is the sole separator of each new carrier? Read the per-case
   lines and the mutation evidence if present; say where the evidence is thin.
2. Name at least two other mado instruments that have never been mutation-scored or limit-scored
   (`quality/check-freeze-order.py`, `quality/check-control-receipts.py`,
   `quality/check-deliverables.py` are candidates — verify their history with read-only git
   before naming one), so the next rounds' claim candidates are grounded.
3. Sibling overlap: does another lane already hold the challenge/witness or guard-carrier ground?
   Search read-only and report paths, or say the sweep found none.
Write `<your dir>/R74Conn.md`. `Report: .ufo/waves/round-74/w1/R74Conn/R74Conn.md`.
"""),
    dict(name="R74Sentinel", role="sentinel", body="""
Boundary and safety audit of the round's new instruments and wave.

1. Static audit of `quality/counters/c1-r74-witness-rule.py`,
   `quality/counters/c1-r74-replay-witness.py` and `quality/counters/c2-r74-shapes.py`: enumerate
   every write, every spawned process and every environment key they touch; confirm no `/tmp`
   hardcoding (QUALITY/scratch discipline), no network, no compositor/service/config access, no
   credential material.
2. Check the committed measurement receipts and the wave's own reports for session material
   (window titles, hostnames, user paths beyond the declared roots, tokens).
3. Verify the scratch discipline: no committed tool writes outside a caller-declared scratch root;
   `absolute_scratch` refuses `/tmp`, `/var/tmp`, `/dev/shm` and symlinks (run the refusal).
4. Confirm the round wrote no config tree, no compositor state, no sibling repo, no fleet file:
   `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain` and
   `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only), reporting any mado
   round-74 misroot.
Write `<your dir>/R74Sentinel.md` with one line per check and any defect.
`Report: .ufo/waves/round-74/w1/R74Sentinel/R74Sentinel.md`.
"""),
]


def main():
    items = []
    for item in ITEMS:
        prompt = (GODSPEED + "\nYour name: %s. Your only write directory: %s/.ufo/waves/round-74/w1/%s/. "
                  "Scratch: /fast/scratch/hyaku/mado-r74/%s/.\n" % (item["name"], LANE, item["name"],
                                                                   item["name"]))
        prompt += item["body"]
        items.append({"name": item["name"], "role": item["role"], "prompt": prompt})
    spec = {"wave": "w1", "reportDir": ".ufo/waves/round-74/w1", "context": CONTEXT, "items": items}
    path = os.path.join(WAVE, "w1-spec.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1)
        fh.write("\n")
    print(path, len(items), "items")


if __name__ == "__main__":
    main()
