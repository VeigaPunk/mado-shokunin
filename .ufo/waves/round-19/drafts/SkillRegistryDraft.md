# SkillRegistryDraft — SKILL.md gate registry, round 19

Draft only. L1 owns `SKILL.md`; L1 applies these rows. Column shape is the
eight-column shape of the registry header at `SKILL.md:549`
(`name | gate/probe | entry command | verdict map | self-test command / spelling |
pinned-value path | write scope | owner`). No `|` appears inside any cell.

Status at drafting (read-only checks, worktree bytes):

- `.ufo/waves/round-19/landed-check.sh` exists; its header is the exit map used below.
- `anchor-durability.py`, `supersede-sweep.py`, `supersessions.json` and
  `frozen-repin.py` do NOT exist yet under `.ufo/waves/round-19/`. Their rows are
  transcribed from the item contracts in `.ufo/waves/round-19/w1/spec.json`
  (`AnchorDurability`, `SupersedeSweep`, `FrozenRepinScript`). Their self-test cells
  say `contract control, unobserved` and must be reconciled to each landed header
  and `--help` before `SKILL.md` is edited. Any divergence from a landed script wins.
- `fresh-pins.py` and `tw-recall.py` exist and were run read-only at `9c54c56`
  (exit 0, outputs in the round-19 seat report).

## A. Insert after `SKILL.md:571` (`mado-measure-mutants`, the last row of the table)

| name | gate/probe | entry command | verdict map | self-test command / spelling | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| mado-anchor-durability | probe | `python3 -I .ufo/waves/round-19/anchor-durability.py REV [--rows S###,...]` (reads `git show REV:corpus/SOURCES.md`; screens `mined` rows only; prints one `ROW <id>` line per screened row with its verdict tag and reason) | 0 no flagged row; 1 at least one row tagged PER_FETCH_DIGEST or UNPINNED_ALIAS (summary line printed; the probe does not decide defect versus false positive, a reviewer does); 2 usage or could-not-evaluate (unreadable REV or SOURCES.md) | — (contract control, unobserved until landed: REV `17661e0fa83f978fb659f5bb8fef47f0969f6945` must flag S094 PER_FETCH_DIGEST and S084 UNPINNED_ALIAS) | `corpus/SOURCES.md` at REV; receipts at REV under `.ufo/waves/round-1[0-9]/fetch/*/receipts.jsonl` (digest-collision arm only); rule constants in the script header | reads committed bytes via `git show` only; writes nothing | mado |
| mado-supersede-sweep | probe | `python3 -I .ufo/waves/round-19/supersede-sweep.py REV [--ledger PATH]` (for each owned file in ledger scope that contains the `old` value: prints `STALE <path>` unless the file holds a line with the `new` value and a ledger row id; prints `POINTED <path>` otherwise) | 0 no STALE line; 1 at least one `STALE <path>`; 2 usage, bad REV or unreadable ledger | — (contract control, unobserved until landed: REV `17661e0fa83f978fb659f5bb8fef47f0969f6945` must print 11 STALE of 13, the set `fresh-pins.py` also reports at that REV) | `.ufo/waves/round-19/supersessions.json` (ledger id `walker-2.17.2`: old `2.17.0`, new `2.17.2`, rows S090 and S096, scope `corpus/knowledge/*.md`, `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `tools/*`); default `--ledger` path [UNK] until landed | reads committed bytes via `git show` only; writes nothing | mado |
| mado-landed-check | probe | `bash .ufo/waves/round-19/landed-check.sh LANE_DIR HASH...` (resolves the remote tip live with `git -C LANE_DIR ls-remote origin refs/heads/master`; prints one `LANDED`, `LOCAL_ONLY` (with reason) or `MISSING` line per HASH) | 0 every HASH LANDED (object present and ancestor of the live remote tip); 1 any LOCAL_ONLY or MISSING; 2 usage or could-not-evaluate (not a directory or repo, no origin, no refs/heads/master on origin, ls-remote failure, ancestry error) | — (no committed selftest; the author's controls are a `/tmp` clone with a bare `/tmp` remote: commit ahead, behind, unknown hash) | none; the remote tip is read live from `origin`, never from a cached remote-tracking ref | network read (`git ls-remote origin`); no fetch, no git write, never invokes jj | mado |
| mado-frozen-repin | probe (writes a caller-selected DIR; see note D1) | `python3 -I .ufo/waves/round-19/frozen-repin.py --from .ufo/waves/round-18/frozen --to DIR --tool PATH [--allow-new-findings]` (copies pinned inputs byte-exact after a sha256 check, runs `--scan` in DIR, writes DIR/expected.json schema `mado-tripwire-frozen-v1` and DIR/README.md with a RECEIPT first line) | 0 DIR written; 1 refused, no write (a source expected finding disappears, or a finding lands on a line that is neither expected nor a known miss, unless `--allow-new-findings`); 2 usage or could-not-evaluate (pinned input digest mismatch, unreadable source, malformed expected.json) | — (contract controls, unobserved until landed: the current tool gives an identical expected.json with known misses kept; a `/tmp` tool copy with a toy rule flagging `pacman -Q` inside strings turns known misses into findings; a mutant dropping a finding exits 1) | `.ufo/waves/round-18/frozen/expected.json` and its input digests (source pins); DIR is caller-selected and outside the lane | writes only the caller-selected DIR (DIR-exists rule [UNK] until landed); reads round-18 frozen inputs; writes no lane file | mado |
| mado-tw-recall | probe | `python3 -I .ufo/waves/round-19/tw-recall.py REV` (fixed denominator: the 6 incident (file, line) pairs of `.ufo/waves/round-18/frozen/expected.json` at 9c54c56; runs REV's `tools/mado-tripwire.py --scan` on the pinned inputs; score = 10 x detected / 6) | 0 JSON printed (any score, 0 included; no pass/fail verdict); 2 could-not-evaluate (usage, unknown REV, pinned input digest mismatch, `git show` failure, scan rc outside 0/1 or no verdict line) | — (the fixed denominator and digest pins are its only controls; precision on control lines is not measured) | `.ufo/waves/round-18/frozen/expected.json` and its input digests at `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`; REV's tool sha256 printed as provenance | reads committed bytes via `git show`; writes only a temp dir it removes | mado |
| mado-fresh-pins | probe | `python3 -I .ufo/waves/round-19/fresh-pins.py REV` (fixed denominator: the 13 owned files at 9c54c56 that contain `2.17.0`; a file is current at REV when a line holds `2.17.2` and an `S###` token; score = 10 x current / 13) | 0 JSON printed (any score, 0 included; no pass/fail verdict); 2 could-not-evaluate (usage, unknown REV, `ls-tree` or `git show` failure) | — (the fixed denominator and the pointer regex are its only controls; row-id validity is not checked) | `PIN_REV` `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`, `OLD` `2.17.0` and `POINTER` regex in the script | reads committed bytes via `git ls-tree` and `git show` only; writes nothing | mado |

## B. Append-only note for the `mado-tripwire` row (`SKILL.md:563`)

The `mado-tripwire` row is NOT edited. Append this paragraph after the
Round-17 tripwire limit paragraph (worktree `SKILL.md:584-594`):

> Round-19 class note (append-only; the `mado-tripwire` row above stands as
> written). The tool at 9c54c56 declares `CLASSES = ("host_mutation",
> "package_query", "live_probe")` (`tools/mado-tripwire.py:61`). Two new
> classes are PENDING L1 DECISION and are not in force: (1) an installer class,
> spelled `tool_install` in the round-18 draft `.ufo/waves/round-18/drafts/TwInstallerChannels.patch`
> (`CLASSES` at patch line 22; `classify_installer` returns `tool_install` for
> uv, uvx, pip, pipx, npx, npm global and cargo install forms) — the round-19
> spec names it `installer`; the spelling is undecided; (2) `vcs_write`, which
> has no draft class token in `.ufo/waves/round-18` or `.ufo/waves/round-19`
> and is named only in the round-19 spec and dispatch. Until L1 applies a
> class patch, the verdict map above and the `--permit` vocabulary (derived
> from `CLASSES`) hold as written. When a class lands, L1 appends a new
> paragraph that names the class and extends the verdict map's class list; the
> existing row is not rewritten.

## C. Round-19 screen and counter limits (append after the Round-17 tripwire limit paragraph)

> Round-19 screen and counter limits. `mado-anchor-durability`,
> `mado-supersede-sweep` and `mado-fresh-pins` are text screens. A line that
> carries `2.17.2` and an `S###` token passes even when the cited row is wrong;
> no screen checks that a row supports the claim. `mado-supersede-sweep` matches
> the literal substring `old`, so a longer string containing it also matches.
> `mado-anchor-durability` judges URL and receipt shape only: it does not fetch
> or re-hash bytes, and a flagged row is a review candidate, not a defect
> verdict. `mado-landed-check` reads the live remote tip over the network and
> reports landedness at that moment only; with no network it exits 2. It never
> fetches. `mado-frozen-repin` regenerates `expected.json` from the tool's own
> findings; its refusal rules guard disappearance of expected findings and new
> findings on unlisted lines only, so a pin re-taken from an edited tool moves
> with that edit. `mado-tw-recall` scores recall on six incident lines, credits
> a finding of any class, and reports no precision. Both counter scores
> (`mado-tw-recall`, `mado-fresh-pins`) are measurements, never admission.

## D. Notes for L1 (not registry text)

1. Kind vocabulary: the six rows use `probe` as the spec asks. `mado-frozen-repin`
   writes a caller-selected DIR and generates the pin it later checks. A gate that
   writes its own pin is circular, so it stays a probe. L1 may instead add a
   `writer` kind; the row text is otherwise unchanged.
2. Invocation: the contracts give bare script names. Rows use `python3 -I` (the
   convention of `fresh-pins.py`, `tw-recall.py` and every round-18 row) and
   `bash` for `landed-check.sh`. Reconcile with each landed header.
3. Class spelling: `tool_install` (round-18 patch) versus `installer` (round-19
   spec) is an open L1 decision. `vcs_write` has no draft yet.
4. Placement: section A goes after the last row (`SKILL.md:571`); section B goes
   after the Round-17 tripwire limit paragraph; section C goes after section B's
   paragraph. Existing rows, including `mado-tripwire` at `:563`, stay byte-identical.
5. Denominators: `mado-fresh-pins` (13) and `mado-tw-recall` (6) are pinned at
   `9c54c56`; the rows say so. Do not re-derive them from a later revision.
