# Attack14 — round 52 w2

Seat: `Attack14` (critic, attack wave w2, item #14). Lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin`, frozen base
`85d57a818c3707397e21c840b6498b105ba798aa`. Claim attacked: **C2 — coverage:
proposition-bound dispatcher source entry**, specifically the no-work control half of the
frozen predicate — claims-frozen.md C2 sentence *"A no-work control at base must miss because
target entry is absent"* and registration.md frozen controls *"C2 no-work control is the frozen
base revision, with the target new entry absent"* plus *"the new counter must name a separate
target slug and prove absent at base"*. Target artifact: the W1 draft counter
`.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py` (965 lines, sha256
`55452a3d…79fb`), its receipts, and the lane state at/after base. This is an attack, not a
vote; no non-author judgment is claimed.

## Verdict up front

**The no-work control at base is reproduced and stands** — every falsifier I could construct
against it failed: the counter at `--rev 85d57a81…` reports `TARGET_MISSED` exit 1 for the
counter's named slug and for the slug the entry has actually landed at; uncommitted working-tree
forgery cannot green it (scoring reads only git objects at the pinned rev); the setup gate
refuses to score *any* path that exists at base, so a pass at the frozen base is structurally
unreachable. **But two adjacent premises of the claim table are attacked as NOT yet
established:** (1) the counter's `ENTRY_DEFAULT` names `hyprland-synthetic-key-dispatch-r52.md`
while the entry that has actually landed in the lane working tree (uncommitted, observed
2026-10-27 mid-flight) is `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` — the "separate
target slug" the counter names and proves absent at base is not the slug that will land; (2)
run against the landed bytes (staged as a commit in a scratch clone), the counter fails 3/5
clauses (`anchor_no_fetch_root` on all four registry rows, `P16:quote_not_at_pin`,
`id_not_referenced`) — so the *production-pass* side of C2 is not demonstrated by the current
landed bytes, and the base control is the only half of the claim with live evidence behind it.

Reproduced: base no-work control **yes** (T1, T1b, T3, T6, T10). Falsified: **no** — with the
two premise gaps above named for the L1/integration seat.

## Axes

| axis | this seat's move | direction |
|---|---|---|
| coverage | verifies the C2 base control misses at base; shows the counter's named slug ≠ landed slug and that landed bytes currently fail (b)-parsed/(c)/(d)/(e) | guards the claim's intent (no axis credit claimed) |
| operability | none | unchanged |
| freshness / others | no substrate, host, service, fleet, sibling or lane file touched; lane read-only; scratch clone only, removed | no harm claimed, none observed |

## Attack battery (each: attacked clause, exact command/locator, observed result, verdict)

All counter runs: `python3 -I .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py
--repo <repo> --rev <rev> [--entry <path>] --work /fast/scratch/hyaku/mado-r52/Attack14/w-*`.
Scratch (`/fast/scratch/hyaku/mado-r52/Attack14/`, receipts + one clone) was removed on finish;
key outputs inlined below. Clone mutations were preceded by `git rev-parse --show-toplevel`
asserting the clone root. No network, no package query, no live read/probe/screenshot, no
install (python3 stdlib only; RULES.md not reached).

### T1 — base control reproduction, counter's named slug (attacked: "no-work control must miss")

Command: counter `--repo <lane> --rev 85d57a818c3707397e21c840b6498b105ba798aa` (defaults).

Observed (exit 1):
```
C2_R52: meta rev=85d57a818c3707397e21c840b6498b105ba798aa base=85d57a818c37 entry=corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md …
C2_R52: a ok=0 entry=absent
C2_R52: b ok=0 skipped=entry-absent
C2_R52: c ok=0 skipped=entry-absent
C2_R52: d ok=0 skipped=entry-absent
C2_R52: e ok=0 skipped=entry-absent
C2_R52: clauses=abcde clauses_met=0 admitted=0/1 verdict=TARGET_MISSED rev=85d57a818c3707397e21c840b6498b105ba798aa
```
Verdict: **reproduced** — byte-identical in shape to the W1 seat's `receipts/r-base.txt`; the W1
control receipt is trustworthy.

### T1b — base control at the actually-landed slug (attacked: "must name a separate target slug and prove absent at base")

Command: counter `--repo <lane> --rev <base> --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md`.

Observed: exit 1, same all-clause-missed `TARGET_MISSED` (`a ok=0 entry=absent`). The lane
working tree currently holds an uncommitted landed entry at this slug (see "Landed state"
below); at the frozen *commit* it is absent, and the counter proves it.

Verdict: **reproduced for the landing slug** — but only because this seat passed `--entry`;
the counter's own default names the other slug (see T4a).

### T2 — frozen-control premises, direct git evidence (attacked: "target entry absent at base")

Read-only, lane at base `85d57a81…`:
- `git ls-tree -r --name-only <base> | grep -i synthetic` — no `hyprland-synthetic-*` entry
  path anywhere (only unrelated old fixture files); `git ls-tree -r --name-only <base> --
  corpus/knowledge/` lists hyprland entries only through
  `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`.
- `git show <base>:corpus/README.md | grep -c synthetic-key-dispatch-r52` → **0** (no index row).
- `git show <base>:corpus/SOURCES.md | grep -cE '^\| S37[0-9]'` → **0**; registry tops out at
  S369 (`S360…S369` present).
- `git cat-file -e <base>^{commit}` → present; `git rev-parse HEAD` in the lane → `85d57a81…`
  (tip is the frozen base; the W1 `r-tip.txt` premise still holds).

Verdict: **premises confirmed independently** — absent entry, absent index row, absent rows
S370+, base present, tip == base.

### T3 — worktree forgery falsifier (attacked: control soundness against no-work greening)

Setup: scratch clone of the lane at base; copied the *entire landed working-tree state*
(entry file, modified `corpus/README.md`, modified `corpus/SOURCES.md`, all of
`.ufo/waves/round-52/fetch/`) into the clone **without committing**; ran the counter
`--rev <base>` (default entry).

Observed: exit 1, `a ok=0 entry=absent`, `TARGET_MISSED` — byte-for-byte the T1 outcome even
though a fully-conformant-looking tree sat in the worktree.

Why: the counter scores only `git show <rev>:<path>` objects (`show()` at counter lines
156-157; `clause_a` 489-502; registry via `show` in `clause_c` 535-538; pins via
`git ls-tree -r <rev>` in `pin_index` 590-599). Nothing scored is read from the working tree.

Verdict: **falsifier attempt failed — control sound.** A no-work actor cannot green the base
run with uncommitted content; only a commit at the scored rev matters, and the frozen base
commit is immutable.

### T4a — committed landed state vs the counter's default entry (attacked: "counter names a separate target slug")

The lane working tree (observed mid-flight, uncommitted): new untracked
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md`; ` M corpus/README.md` (adds the index
row for that slug); ` M corpus/SOURCES.md` (adds S370–S373, `mined`, opened `2026-10-27`,
used-by naming the landed slug); untracked `.ufo/waves/round-52/fetch/` (4 pins +
SHA256SUMS whose digests match the registry rows' cited SHA256 values).

Setup: committed this state as one commit `e934f7f75666f91fac235010aecad79fac332f27` in the
scratch clone; ran the counter at that rev **with default entry**.

Observed: exit 1 — `a ok=0 entry=absent`, `TARGET_MISSED`. The counter looked for
`corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md` (its `ENTRY_DEFAULT`, counter line
95), which nobody is landing.

Verdict: **premise gap confirmed.** The claim table's "the new counter must name a separate
target slug" is satisfied only for a path that will not land; as drafted, the counter would
false-**negative** at the post-landing tip (operability harm at scoring time, not a control
failure). Smallest correction: integration sets `ENTRY_DEFAULT` to the landed slug (or always
passes `--entry`); the W1 report already flagged this one-constant risk.

### T4b — committed landed state vs the correct slug (attacked: "production pass" adjacency; clause isolation at a landed rev)

Command: counter `--repo <clone> --rev e934f7f7… --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md`.

Observed (exit 1):
```
C2_R52: a ok=1 index_row=`knowledge/hyprland-synthetic-dispatch-r52.md` (round 52;…
C2_R52: b ok=1 propositions=18 ids=18 forms=table
C2_R52: c ok=0 rows_bound=0/18 distinct_rows=0 miss=P01:anchor_no_fetch_root,P02:anchor_no_fetch_root,P03:anchor_no_fetch_root,P04:anchor_no_fetch_root
C2_R52: d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 policy=whitespace-collapsed pins_prior_equal=4/17 miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
C2_R52: e ok=0 prose_rows=4 prop_rows=4 manifest_rows=0 miss=P01:id_not_referenced,P02:id_not_referenced,P03:id_not_referenced,P04:id_not_referenced
C2_R52: clauses=abcde clauses_met=2 admitted=0/1 verdict=TARGET_MISSED
```
Three distinct defects in the landed bytes vs the draft counter's contract:
1. **(c) `anchor_no_fetch_root` on every row** — the landed registry anchor cells read e.g.
   `DispatcherTranslator.cpp:531-627 @ efb50993780079460b0cbed1363e2166a2de1d9f; r52 fetch
   SHA256 7248cbb8…` (SOURCES.md working-tree diff); `clause_c` (lines 563-566) requires the
   literal fetch root (`.ufo/waves/round-52`) in the anchor cell. The W1 counter seat
   documented exactly this requirement and the W1 entry seat was told; the landed rows do not
   comply. The base control does not hinge on this, but the production pass does.
2. **(d) P16 pin grammar** — landed pin cell `Hyprland-ConfigActions.cpp:1554-1558,1576`
   tries to cite two disjoint ranges; `parse_pin_cell` (lines 442-466) matches `1554-1558` and
   *silently drops* the trailing `,1576`, so the quote (mods call at :1554 + key call +
   clear at :1576, verified present in the pinned bytes) cannot appear contiguously in the
   cited span → `quote_not_at_pin`. Parsing hazard worth its own note: trailing garbage in a
   pin cell is ignored rather than rejected (17/18 quotes bound; the one miss is the pin
   grammar, not a wrong quote — the bytes at `.ufo/waves/round-52/fetch/
   Hyprland-ConfigActions.cpp:1554-1558,:1576` support the proposition).
3. **(e) `id_not_referenced` P01–P04** — the landed entry does not draw those proposition ids
   anywhere outside the map (no "What the evidence licenses"-style table).

Also printed: `pins_prior_equal=4/17` — all four bound pins byte-identical to round-51 staged
copies (diagnostic by design; the repeated-URL rows S370≡S365, S371≡S367, S373≡S364 and the
QUALITY.md rule-17 distinct-scope review remain open per W1 `C2PinAudit` finding 2 and
`C2Novelty` — outside this seat's control scope, gate the production verdict).

Verdict: **not a control falsifier** (base still misses), but the C2 "production pass" is
currently failing against the landed bytes 3/5; the claim's only live evidence today is the
base MISS. The W1 `r-green`/`r-draft-fixed` receipts prove a synthetic fixture and the W1
sibling draft pass — per the orchestrator's standing note, that is not landing.

### T5 — round-51 slug guard (attacked: "separate target slug" enforcement)

Command: counter `--entry corpus/knowledge/hyprland-dispatcher-dispatch-r51.md --rev <base>`.

Observed: exit 2, `setup error: target entry must differ from the round-51 entry:
hyprland-dispatcher-dispatch-r51.md` (guard at counter lines 947-948). Verdict: **enforced**
(basename equality; case-variant slugs would bypass the string guard but still fail — git path
lookup is case-sensitive, so a case-aliased run reports `entry=absent`, exit 1; cosmetic only,
not a control hole).

### T6 — setup gate makes a base pass structurally unreachable (attacked: control isolation)

`main()` lines 952-954: `show(repo, BASE, entry_path) is not None → Setup("base … already
holds …")`. Tested with three existing-at-base paths, all `--rev <base>`:
- `--entry corpus/knowledge` (a tree): exit 2, `base 85d57a818c37 already holds corpus/knowledge`;
- `--entry corpus/knowledge/` (trailing slash): exit 2, same gate;
- `--entry corpus/README.md`: exit 2, same gate;
- and any existing knowledge entry (e.g. `waybar-walker-plane.md`): exit 2, same gate.

So at the frozen base the counter either (a) refuses to run — for anything that exists there —
or (b) runs only against absent paths and then fails clause (a). No base content can be scored
at base at all. Verdict: **the strongest available evidence the control cannot false-green**;
it also means the trivial "skip" shape of the T1 receipt is by construction, not by luck.

### T7/T8 — hygiene gates (attacked: control pollution by the runner)

- `--work <clone>/inside`: exit 2, `scratch dir inside the scored repository` (refusal in
  `scratch_dir`, lines 841-858) — the counter cannot write into the scored repo.
- `--rev deadbeef…` (unresolved): exit 2, `rev does not resolve to a commit`.

Verdict: **enforced.**

### T9 — the distrusted old receipt's premise (attacked: registration's reason the old receipt can't serve)

Command: `python3 -I quality/counters/c2-r51-dispatch-entry.py --repo <lane> --rev <base>`.

Observed: exit 0, `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET
rev=85d57a81…` — the old counter passes at the frozen base because the *round-51 entry* exists
there (`a ok=1`, `b ok=1 rows=6/2 pins=6`). The wave receipt `receipts/c2-base.txt` shows the
same (its work dir `/fast/scratch/hyaku/mado-r52/L1/c2-base` shows L1 already re-ran it).

Verdict: **premise confirmed independently** — the old base receipt measures the r51 target,
not the r52 target's absence; the new counter's T1 MISS is the first control receipt that
actually measures what C2's no-work control requires.

### T10 — tip-is-base still true (attacked: W1 r-tip premise freshness)

`--rev HEAD` on the lane resolves to `85d57a81…` and produces the identical T1 MISS (exit 1).
Verdict: **reproduced.**

## Landed state (observed, not written by this seat)

`git status --short` in the lane during this attack: ` M corpus/README.md`, ` M
corpus/SOURCES.md`, ` M quality/tool-ledger.md`, `?? .ufo/waves/round-52/`, `??
corpus/knowledge/hyprland-synthetic-dispatch-r52.md`. The C2-relevant part is the landed entry
+ index row + S370–S373 + `.ufo/waves/round-52/fetch/` (sha256 digests in
`fetch/SHA256SUMS` match the rows' cited values). Provenance: not the W1 `C2EntryDraft` bytes
(different slug, different proposition set, different pin staging root) — consistent with a
post-W1 integration/data pass. This seat adapted to it as ground truth; nothing here was
created or modified by me.

## Addendum — integration state observed before yield (lane kept moving; adapted, not authored by this seat)

At report time the lane working tree additionally held untracked
`quality/counters/c2-r52-proposition-entry.py` (integrated counter, sha256 `5c7fb820…` —
different bytes from the W1 draft `55452a3d…`: minified, `--work` now required, new `--base`
parameter defaulting to the frozen base) plus `quality/counters/c1-r52-ledger.py` and
`corpus/lessons/round-52.md`. Re-ran the control against the *integrated* counter:

- `--repo . --rev 85d57a81… --work <scratch>` (default entry): `C2_R52: entry=absent
  verdict=TARGET_MISSED`, **exit 1**;
- same with `--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md`: identical MISS,
  **exit 1**.

So the base no-work control reproduces on the canonical artifact as well, and its integrated
`--entry` default still names `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md` — the
T4a named-slug/landed-slug gap persists at integration as of this writing; corrections 1–6
below still apply unchanged.

## Smallest safe corrections (for the L1/integration seat)

1. **Aim the counter**: set `ENTRY_DEFAULT` to the landed slug (or pass `--entry
   corpus/knowledge/hyprland-synthetic-dispatch-r52.md` at every run), then re-run the base
   control (must stay `TARGET_MISSED` exit 1) and the landed rev (currently fails c/d/e).
2. **Registry anchor shape**: make S370–S373 anchor cells name the fetch root literally
   (e.g. `.ufo/waves/round-52/fetch/Hyprland-….cpp:… @ efb50993…`), as the W1 counter seat
   specified — one-line-per-row edit in `corpus/SOURCES.md`.
3. **P16 pin**: either split into two propositions or extend the counter's pin grammar for
   disjoint ranges; cheapest is splitting the proposition (mods-then-key ordering at
   :1554-1558, clear at :1576).
4. **(e) ids**: cite P01–P04 outside the map (a "What the evidence licenses" table, the house
   pattern).
5. **Pin-cell hygiene (counter hardening, optional)**: reject pin cells whose text after the
   line spec is not empty/`@ rev` — today `…:1554-1558,1576` is silently truncated (T4b);
   a louder parse note would have pointed at the defect directly.
6. **Before any TARGET_MET is claimed**: the repeated-URL distinct-scope review for
   S370/S371/S373 (QUALITY.md rule 17) and an outside source-truth sample over the landed
   entry remain open (W1 `C2PinAudit` finding 2, `C2EntryQuality`, `C2Novelty`); the base
   control result does not bear on them.

None of 1–6 weakens the T1/T1b/T3/T6 control result: at the frozen base, with the target
entry absent from the commit, the counter misses, and nothing short of committing the entry
into the base commit itself can change that.

## Dissent / limitations

- The counter attacked is the W1 **seat draft** (not committed to `quality/counters/`); if
  integration edits it (e.g. for correction 5), the base control must be re-run — the commands
  above are the re-run recipe.
- T4b stages the lane's *uncommitted* landing state as a scratch commit to make it scoreable;
  the true landing commit may differ. If it does, T4b's clause details are stale but the T4a
  slug-mismatch finding stands until the counter's named slug equals the landed slug.
- T4b does not sample source truth for the landed entry's 18 quotes; it reports structural
  outcomes only. Entailment/truth stays with the outside non-author reviewer, as the frozen
  claim requires.
- The base control "misses" trivially (entry absent), and clauses b–e are skipped at base by
  construction (T6); discrimination at non-base revs rests on W1's green/mutant receipts plus
  this seat's T4b — that division matches the frozen predicate, which demands only
  base-miss for the no-work control.
- No tracked lane file, fleet file, sibling seat, PATH dir, host state or package surface was
  read (beyond lane source/git objects) or written; the only writes were this report and the
  removed scratch dir. No tool installed.

## Deliverables

All evidence is inlined above; reproduction commands are given per attack. Scratch
`/fast/scratch/hyaku/mado-r52/Attack14/` (clone, receipts, probe dirs) removed on finish;
disk guard fine (582G free).

Report trailer:

```
seat=Attack14 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
attacked=claims-frozen.md C2 "A no-work control at base must miss because target entry is absent";
registration.md frozen controls "C2 no-work control is the frozen base revision, with the target new entry absent"
and "the new counter must name a separate target slug and prove absent at base";
artifact=.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py (draft counter)
t1_base_miss=reproduced exit=1 TARGET_MISSED (default slug, rev=85d57a81…)
t1b_base_miss_landed_slug=reproduced exit=1 TARGET_MISSED (--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md)
t2_premises=entry/index-row/S370-S373 absent at base; tip==base; confirmed via git ls-tree/show/cat-file
t3_worktree_forgery=control sound; full landed state uncommitted -> still TARGET_MISSED exit=1 (scoring reads git objects at rev)
t4a_slug_mismatch=confirmed; counter ENTRY_DEFAULT names hyprland-synthetic-key-dispatch-r52.md, landed file is hyprland-synthetic-dispatch-r52.md;
committed landed state + default entry -> TARGET_MISSED (entry=absent) at e934f7f7…
t4b_landed_vs_counter=clauses_met=2/5 at e934f7f7…: c miss=anchor_no_fetch_root (all rows), d miss=P16:quote_not_at_pin (disjoint-range pin cell truncated), e miss=id_not_referenced (P01-P04)
t5_slug_guard=enforced exit=2 (round-51 basename)
t6_base_holds_gate=enforced exit=2 for tree path, trailing-slash path, corpus/README.md, and any existing base entry
t7_scratch_refusal=enforced exit=2; t8_unresolved_rev=enforced exit=2
t9_old_counter_at_base=TARGET_MET exit=0 (independent confirmation of why receipts/c2-base.txt is distrusted for C2)
t10_head_is_base=reproduced exit=1 TARGET_MISSED
i1_integrated_counter_base=TARGET_MISSED exit=1 (quality/counters/c2-r52-proposition-entry.py, default entry; sha256 5c7fb820…, --base parameter)
i2_integrated_counter_base_landed_slug=TARGET_MISSED exit=1 (integrated counter, --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md); integrated default entry still the key-dispatch slug (T4a gap persists at integration)
reproduced=yes (base no-work control); falsified=no
premise_gaps=counter named slug != landed slug; landed bytes fail 3/5 clauses vs draft counter; distinct-scope review S370/S371/S373 and truth sample still open
installs=none (python3 stdlib only; RULES.md not reached)
report=.ufo/waves/round-52/w2/Attack14.md
```
