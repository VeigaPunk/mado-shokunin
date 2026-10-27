# ScrCorrections — round-49 w1: correction lines for N1/N2/N3/N5

seat `.ufo/waves/round-49/w1/ScrCorrections/` · lane `mado-shokunin` · 2026-10-27
base `03e4ae76aff7a4be59cb69970dd553baa319695a` (01:21:55 -0300) · lane HEAD during reads
`5f37c1b87b3ce5e438d19284e32b2e46fd548a92` · **0 tracked files modified**, 8 new paths, all inside this seat's scope.

Deliverable: `.ufo/waves/round-49/w1/ScrCorrections/corrections.md` — four append-only correction lines (N1, N2, N3, N5),
each naming its target `file:line`, carrying its counting command and pasted output, plus the append-candidate text for
the L1 to paste. Nothing in the lane was edited: the L1 is the only integrator.

## Behavior

For each routed round-48 closure item I re-ran the counting command or the fetch in this seat and recorded what came
back, including the two places where the spot-check's own premise did not reproduce.

| item | target | what this seat found | status |
|---|---|---|---|
| N1 | `.ufo/reports/round-48/mado.md:37` | untracked `*.synthetic` surplus is **47** = 45 (`round-45/w1/RevengerOmarchy`) + 2 (`round-46/w1`: `CritW2Gate.md.synthetic`, `CritW2Gate/report.md.synthetic`); zero sidecars outside those two waves; 100 `*.synthetic` paths are *tracked* from earlier rounds, so the two sets are disjoint by path | correction stands; number reproduces |
| N2 | `.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:4` (+ lesson line at `corpus/lessons/round-48.md:263`) | `host_cache_untouched_sha256=c8b104e6…40144` **equals** `printf 'r48-w2\n' \| sha256sum`, and that payload is 7 bytes — the M48-10 mutant's bytes, not a clean control | correction stands; digest identity exact |
| N3 | `corpus/lessons/round-48.md:425` | the Gate holds **12 admit blocks** (`:55`-`:66`, S340-S351) and **3 reject blocks** (`:71`-`:73`); the line's "five gate decisions (three admits, two rejects)" is stale pre-gate template text; the closure sampled 6 of 15 | correction stands; counts computed twice, independent routes |
| N5 | `corpus/SOURCES.md:295` (S346), `:296` (S347) | the files-API form returns the pinned bytes — rules.in 15768 B `16389776…ffa3`, symbols/br 19592 B `8cf65550…f35e`, both `cmp`-equal to `.ufo/waves/round-48/fetch/` — **but** the `-/raw/` premise behind the item did not reproduce: 5 consecutive `-/raw/` requests (normal, `Python-urllib/3.13`, empty UA) all returned HTTP 200 `text/plain` with the same pinned bytes | remedy verified; premise contradicted |

**The N5 finding is the one that changes a frozen decision.** The spot-check recorded `-/raw/` as "now returns an
anti-bot HTML page". From this host on 2026-10-27 it does not, under any of three User-Agents, five times. Recording the
API form as the *only* working route would freeze an unverified premise. The append line therefore carries the API form
as a verified **equivalent fallback**, and states that `-/raw/` must be re-tested before being declared broken. I did not
characterise *why* the round-48 fetch saw HTML (egress, rate, or a transient interstitial) — five requests over ~5
minutes is not a rate-limit study, and I say so rather than guess.

**N1's unscoped number is not citable during a live wave.** `git status --porcelain -uall | wc -l` read 59, then 70,
inside three minutes of this seat's work, entirely from round-49 w1 seats writing. All 23 non-synthetic untracked paths
at the last read were `round-49/w1` writes created after base. Only the scoped 47 is durable; the append line says so.

## Gates

None scored. No frozen counter, predicate, fixture or control was run or touched — those freeze after w1 returns. The
four items are non-claim routed defects; each is closed by a correction line plus a reproducible command, not by a
pass/fail counter.

## Touched surfaces

Created (all untracked, all in scope):
- `.ufo/waves/round-49/w1/ScrCorrections.md` (this report)
- `.ufo/waves/round-49/w1/ScrCorrections/corrections.md` (deliverable)
- `.ufo/waves/round-49/w1/ScrCorrections/n1-untracked-count.txt` `9cedf78a…` — N1 counts, incl. the two-wave boundary check and the live-wave caveat
- `.ufo/waves/round-49/w1/ScrCorrections/n2-cache-digest.txt` `a4bfc79a…` — N2 digest equality and byte count
- `.ufo/waves/round-49/w1/ScrCorrections/n3-gate-counts.txt` `9b8f0889…` — N3 admit/reject counts, locators, `:49` prose cross-check, sampled-row cross-check
- `.ufo/waves/round-49/w1/ScrCorrections/n5-gitlab-files-api.txt` `408035d9…` — N5 API fetches, `cmp` against pins, and the `-/raw/` counter-evidence
- `.ufo/waves/round-49/w1/ScrCorrections/api-rules.in` `16389776…ffa3` — fetched pin, S346
- `.ufo/waves/round-49/w1/ScrCorrections/api-symbols-br` `8cf65550…f35e` — fetched pin, S347

Read-only, unmodified: `corpus/lessons/round-48.md`, `corpus/lessons/round-48-verifier-spotcheck.md`, `corpus/SOURCES.md`,
`.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt`, `.ufo/waves/round-48/fetch/xkeyboard-config-*`,
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/mado.md`.

## Findings

1. **N1 reproduces at 47, and the count is wave-sensitive.** Durable number 47; `wc -l` on the whole tree is not a
   citable number inside a live round.
2. **N2 reproduces exactly.** The field name and its content point opposite ways; the append line makes the receipt a
   witness to M48-10 instead of a clean-state control. The spot-check's separate mtime observation is untouched by this.
3. **N3 is 15 gate decisions, not 5: 12 admits, 3 rejects; 6 sampled.** Confirmed two ways — by block regex and by the
   Gate's own `Admitted: rows S340-S351` prose at `:49`.
4. **N5: remedy verified, premise contradicted.** This is the finding most likely to matter for the freeze: the API
   fallback is real and byte-exact, but its stated *reason* is not reproducible today. A counter built on "`-/raw/` is
   broken" would score the wrong thing.
5. **Nothing was upgraded into execution evidence.** N2 is a digest identity, not an observation of the operator's
   cache — I neither read nor wrote `~/.cache/xdg-terminal-exec`, and both the report and corrections.md say so. N5's
   anti-bot question is left open, not resolved.

## Out of scope (by assignment, not claimed)

N4 (round-48 v2 matrix text rows), M48-8, M48-10's own fix, M48-13, `w2/SentScratch`, the `registration-v2.md` residuals,
and every C1/C2 claim. The disposition of the 47 sidecars (commit vs remove) is the L1's decision; this seat only counts
them.

## Safety

No `git`/`jj` mutation (read-only `rev-parse`/`log`/`status`/`ls-files`/`cat-file` only). No pacman, no service or
compositor call, no `xkbcli`, no GUI. No write to `~/.cache`, `~/.config`, `~/.local` or any home state — the N2 check is
a digest of a literal string, deliberately not a read of the operator cache. All network fetches are `curl` GETs of
pinned tag refs into the seat dir; no branch URLs. Scratch `/fast/scratch/hyaku/mado-r49/ScrCorrections` created, used
with `ulimit -f 65536`, and removed; no `/tmp` path is cited. No tool installed or upgraded this seat.
