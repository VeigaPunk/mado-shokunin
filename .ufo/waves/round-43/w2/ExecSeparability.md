# Seat ExecSeparability — round 43 w2

**Target attacked:** registration `## Separability` (freeze `b2e2efd6e268920d31f3c32cf52dc097dd6e1d22`) and
`registration-v2.md` `## Separability (unchanged)` (freeze `496340dd53fabd800be42e8fb19090f35e2c235c`), at the data
commit `1959770657f1f8665097c1aed4be6c1cbb07139f` (base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`).

**Status: DONE. Verdict: causal separability HOLDS — I could not break it in either direction.** One prose defect
(F1, low) and one provenance observation (F2, outside this target) are reported; neither changes a claim's score.

**Evidence:** `.ufo/waves/round-43/w2/ExecSeparability/receipt.txt` — verbatim transcript of
`bash .ufo/waves/round-43/w2/ExecSeparability/reproduce.sh` (exit 0; replayed, and the four scratch commit hashes
came out identical in the first and last replay, `5437b3ee`/`6686fe20`/`21d2a1a1`/`265ff109`). Every command and
final line the task asked for is in that file.

---

## 1. Method

One shared scratch clone (`git clone -q --shared` into `/fast/scratch/hyaku/mado-r43/ExecSeparability`, toplevel
asserted `= $D` before the first commit), four scratch commits made **only** with `-C "$D"` plus
`-c user.name=t -c user.email=t@t.invalid` and fixed dates `2026-10-26T12:00:00 +0000`, so the hashes are stable
across replays. No lane file, no lane index, no lane ref was touched.

```
$ D=$(mktemp -d -p /fast/scratch/hyaku/mado-r43/ExecSeparability); git clone -q --shared <lane> $D
git -C $D rev-parse --show-toplevel -> /fast/scratch/hyaku/mado-r43/ExecSeparability/tmp.KicFmXJLoz
TOPLEVEL_OK
```

## 2. The four scored cells

| cell | rev | what the commit removes | counter | final line (verbatim from receipt) |
|---|---|---|---|---|
| control | `1959770` | nothing (data commit as landed) | C1 | `PRED-C1-r42: fixtures=37/37 tool=present verdict=TARGET_MET rev=1959770657…` exit 0 |
| control | `1959770` | nothing | C2 v2 | `PRED-C2-r43-v2: admitted=1/1 verdict=TARGET_MET rev=1959770657…` exit 0 |
| **(a)** | `5437b3ee4241b59e7a5cd2aea4405549669a3345` | `tools/mado-geometry.py` (417 lines) | C2 v2 | `admitted=1/1 verdict=TARGET_MET rev=5437b3ee…` exit 0 |
| **(b)** | `6686fe2080c25d773871d878b2d6221a7aac0b37` | entry + lesson deleted; `SOURCES.md`, `README.md` at base | C1 | `fixtures=37/37 tool=present verdict=TARGET_MET rev=6686fe20…` exit 0 |
| (c) extra | `21d2a1a17149ee6b8af3012f88f47fd6000d0ed5` | **all** C2 content: `corpus/` at base, `PROVINCE.md`/`SKILL.md` at base, `quality/check-locators.py` deleted, `fetch/` pins deleted — 18 files, −4750 lines | C1 | `fixtures=37/37 tool=present verdict=TARGET_MET rev=21d2a1a1…` exit 0 |
| (d) extra | `265ff109f96f674da30d9415b74c29bb8e01133d` | all C1 evidence: tool + `receipts/` + `ctl/` — 80 files, −3037 lines | C2 v2 | `admitted=1/1 verdict=TARGET_MET rev=265ff109…` exit 0 |

(a) is the assigned attack on C2 and (b) the assigned attack on C1; both survive. (c) and (d) are stricter versions of
the same two attacks that I added because the assigned pair only removes part of each footprint: C1 survives with the
*whole* C2 content tree absent, and C2 survives with C1's tool, C1's receipts and the shared control runners absent.

**Control for the method (cell e):** with the worktree at `expA` (no `tools/mado-geometry.py` on disk) the C1 counter
still reports `tool=present` for rev `1959770` — so the counters score **commits**, not the worktree, and the cells
above are not artefacts of a dirty tree. `WORKTREE_TOOL=absent` / `fixtures=37/37 tool=present verdict=TARGET_MET`.

## 3. Why it holds: disjoint read sets (static, revision-addressed)

C1's counter (`quality/counters/c1-r42-geometry.py`) can read exactly one path from the repo:

```
108: TOOL = "tools/mado-geometry.py"
963: if git(repo, "show", "%s:%s" % (base, TOOL)) is not None:
965: src = … git(repo, "show", "%s:%s" % (rev, TOOL))
c1 mentions of corpus/ or lessons or README: 0
```

C2's counter (`quality/counters/c2-r43-gkeep-entry-v2.py`) reads:

```
119: ENTRIES = ("corpus/knowledge/hyprland-gkeep-geometry-r43.md",)
120: LESSON = "corpus/lessons/round-43.md"
121: FETCH = ".ufo/waves/round-43/fetch/"
619/620: registry(show(repo, rev|base, "corpus/SOURCES.md"))
621/622: show(repo, rev, LESSON) ; show(repo, rev, "corpus/README.md")
489: blob = show(repo, rev, path) if path.startswith(FETCH)
c2 mentions of tools/ or mado-geometry: 0
```

`{tools/mado-geometry.py}` ∩ `{entry, SOURCES.md, README.md, lesson, fetch/*}` = ∅. The two read sets are disjoint
*because of the constants*, not because of the data.

**Enforcement, not just discipline.**
- Per registration the tool "sees neither the lane, nor this counter, nor /home" — the sandbox binds
  `--ro-bind /usr`, `--tmpfs /tmp` and, for fixture runs, only `ro=[os.path.dirname(tool)]`
  (`c1-r42-geometry.py:154-164`, `:885`). A C1 tool that *wanted* to read a C2 file could not.
- C2 has exactly one child-process site, `subprocess.run(["git", "-C", repo, *args])` at `:169`, used only by
  `show`/`resolve`. `PRED-C2-r43-v2` cannot execute `tools/mado-geometry.py` even if it were named.
- The two counters also use different fixed bases (`62dd798bb08401a8697383552edcc36f109344fa` for C1 clause a,
  `a35cfdf…` for C2), so neither's "absent at BASE" precondition rides on the other claim's round.

## 4. Findings

### S1 — SUPPORT: separability holds in both directions, measured

Attacks: `registration.md` § Separability ("…so C2 never runs C1's tool and C1 reads no C2 file"), quoted at
`b2e2efd:.ufo/waves/round-43/registration.md` (fragment verified by `QUOTE … :: 1` in the receipt). Evidence: cells
(a)–(d) above plus the disjoint read sets in §3. No hole in the causal claim.

**C1 provenance sentence re-verified** (it is separability-adjacent and free to check): the tool at the data commit
hashes to `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`, byte-identical to
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (`receipt.txt`, last two lines). The C1 target also reproduced at
`1959770` under nine distinct nonces this seat, always `37/37`.

### F1 — DEFECT (prose, low): the file-footprint half of the Separability sentence is false at the data commit

`registration.md` (b2e2efd) states, quoting 6 words: `C1 touches \`tools/mado-geometry.py\` only (plus receipts).`
The data commit contradicts "only" in both directions:

- **C1 documentation lands outside the tool and outside receipts.** `PROVINCE.md:32` is the C1 tool's read-surface row
  (fragment "the bytes of one or more caller-supplied Hyprland config files" → `QUOTE … :: 1`); `SKILL.md:158`
  (decision row) and `:225` (probe row) plus the subsection `### Rule size versus reported size` at `SKILL.md:246`
  document the tool's how-to; `corpus/README.md:298` names the instrument ("instrumented by the read-only join", → `:: 1`);
  `corpus/lessons/round-43.md:11-14` describes C1's landing ("C1 lands `tools/mado-geometry.py`", → `:: 1`). Of those
  files, two — `corpus/README.md` and `corpus/lessons/round-43.md` — are named by the same sentence as **C2's**; the
  other two (`PROVINCE.md`, `SKILL.md`) are named by neither claim.
- **C2's footprint is wider than the sentence's four items.** The data commit also lands, for C2,
  `PROVINCE.md:32`, `SKILL.md:158/:225/:246-`, `corpus/QUALITY.md:401-409` (criteria 77-81),
  `quality/check-locators.py` (405 lines), `quality/counters/c2-r43-gkeep-entry-v2.py`, `ctl/` (two 382-line
  runners, three forgeries) and `fetch/` (ten pins). `registration-v2.md` repeats the narrowing:
  `C1 touches \`tools/mado-geometry.py\` only; C2 the entry, rows S290-S299, the lesson \`## Gate\` and the README
  index.` followed by `index. v2 reads` / `no C1 file.` (both fragments `:: 1`; the sentence wraps at "v2 reads").

**Severity: LOW, no axis harmed.** The sentence's *causal* half is exactly right (§3, cells a–d); the false half is a
file-set claim, and no predicate reads `PROVINCE.md`, `SKILL.md`, `QUALITY.md` or `README.md` prose as evidence — both
targets stay met with those files reverted to base (cell c). So the round's *result* is not at risk; its *statement of
separability* is overstated.
**Flip condition:** if any future C1 or C2 predicate reads a shared prose file (`PROVINCE.md`, `SKILL.md`,
`corpus/README.md`, a lesson) as evidence, then the file sets genuinely overlap and Separability must be restated as a
read-set theorem ("the counter opens exactly these paths") rather than a file-ownership theorem. The correct sentence
for this round is the read-set one in §3.

### F2 — OBSERVATION (outside this target; likely RerunC1Data / RerunC2Data territory): the two after-data receipts do not exist at the rev they attest

The card cites `measured at 1959770657…: … (receipts/c1-after-data.txt)` and the C2 equivalent. Neither path exists at
that commit — `git cat-file -e 1959770:<path>` is absent for both; `git log --diff-filter=A` puts both in `a47efeb`
("after-data receipts" commit, one commit above the data). By contrast `receipts/live-geometry-host.txt` **is** at the
data commit.

This is a citation-location imprecision, not a false measurement: I reproduced both numbers at `1959770` in my clone
(`37/37`, `admitted=1/1`), so the attested measurement is real. It matters only because a reader checking the claim at
the data rev cannot open the receipt there. I did not treat it as a separability defect and I did not score it.

## 5. Risks and limits

- My four scratch commits exist only inside the deleted scratch clone; they are replayable (`reproduce.sh`, fixed
  dates → same four hashes), not citable as commits elsewhere. `SCRATCH_GONE` after the run.
- I did not run C1's 46-control suite or C2's 74-control suite; other seats own those. My work is *only* the
  independence question.
- Not tested: a single mutation that changes both claims' inputs at once. It cannot be constructed from either
  counter's read set, and cell (c) (both prose trees at base) is the closest available joint mutation.
- The counters are nonce-randomised; every C1 verdict above reproduced across ≥9 distinct nonces, so the results are
  not one lucky lattice.

## 6. Files changed

No lane file edited. New files, all inside my seat directory:
- `.ufo/waves/round-43/w2/ExecSeparability/receipt.txt` — the transcript (commands + final lines).
- `.ufo/waves/round-43/w2/ExecSeparability/reproduce.sh` — the deterministic driver that produced it.
- `.ufo/waves/round-43/w2/ExecSeparability.md` — this report.

Tooling: nothing installed (standard `git`, `python3 -I`, `bwrap` from `/usr/bin`). Scratch:
`/fast/scratch/hyaku/mado-r43/ExecSeparability` (outside the lane and outside the fleet tree), created by the driver
and removed by its `trap` on exit — `du -sh` reports `SCRATCH_GONE` after the run.
