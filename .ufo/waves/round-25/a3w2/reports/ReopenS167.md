# ReopenS167 — fresh reopen of S167's pinned URL and registry-move review

Seat: MadoR25A3.ReopenS167, round 25 wave a3w2, 2026-10-23. Leaf: no subagents, no
host state touched, no nested Hyprland, no tools installed (tooling directive: nothing
to install — curl/prlimit/git read-only sufficed).

## 1. Fresh fetch

Command (fetch to scratch only; no lane writes):

```sh
mkdir -p /fast/scratch/hyaku/mado-r25a3/reopen && timeout 60 prlimit --as=4000000000 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/advanced-configuration/using-hyprctl.md' -o /fast/scratch/hyaku/mado-r25a3/reopen/S167.bin && sha256sum /fast/scratch/hyaku/mado-r25a3/reopen/S167.bin && wc -c -l /fast/scratch/hyaku/mado-r25a3/reopen/S167.bin
```

Output:

```text
95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0  /fast/scratch/hyaku/mado-r25a3/reopen/S167.bin
 295 8239 /fast/scratch/hyaku/mado-r25a3/reopen/S167.bin
```

Row anchor (corpus/SOURCES.md:179): `sha256:95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0, 8239 B`. Fresh bytes are 8239 B with that exact sha256 — **byte-identical**. Also identical to the a3w1 report's fetch `.ufo/waves/round-25/a3w1/reports/WikiUsingHyprctl.md` (same sha256, 295 lines).

## 2. Quote verification (verbatim, from the fresh bytes)

I read lines 243-262 and 284-295 of the fresh `/fast/scratch/hyaku/mado-r25a3/reopen/S167.bin` directly (raw) and compared the a3w1 report's four located quotations byte-for-byte:

| line | verbatim content of fresh fetch | report quote |
|---|---|---|
| 249 | `binds                - lists all registered binds` | ✓ exact |
| 256 | `instances            - lists all running instances of Hyprland with their info` | ✓ exact |
| 289 | `hyprctl -j monitors` | ✓ exact |
| 293 | `- \`j\` - output in JSON` | ✓ exact |
| 294 | `- \`i\` - select instance (id or index in hyprctl instances)` | ✓ exact |

All five lines (the report's quote 4 spans 293-294) sit inside the row's declared anchor ranges `238-262` and `284-295`. Note the a3w1 report had checked its quotes with whitespace-normalized substring matching; this reopen checks them verbatim against fresh bytes and they pass strictly.

## 3. Registry move: used-by change instead of a duplicate row

State history of S167's used-by cell (read via read-only `git show <rev>:corpus/SOURCES.md`, outputs to scratch):

- `41cc04c8` (a3w1 base) line 179: `corpus/knowledge/rule-attribution-r24.md`
- `459dd17f` (a3w1 lane commit) line 179: `corpus/knowledge/rule-attribution-r24.md`
- working copy now (SOURCES.md:179): `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md`

So the change this round is exactly: `corpus/knowledge/rule-attribution-r24.md` → `corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md`.

The used-by change is the right move under the registry's own rules:

1. **Header rule** (corpus/SOURCES.md:7-8): "Only `status`, `recheck` and `used-by` change in place, each logged old→new in that round's lesson." Extending `used-by` in place is the sanctioned operation; the a3w1-drafted row would have been a whole new row for an already-registered source.
2. **Contract Rule 2, append-only** (kaika `SOURCES-CONTRACT-v1.md:49-51`): same three fields change in place; a *correction* is a new row only via `supersedes S0NN —`. The a3w1 draft was not a correction — same URL, same blob, same sha256 — so it is not even the superseding-row case.
3. **used-by semantics** (contract :40-41): used-by holds "repo-relative paths of the knowledge entries or lessons citing the row". `bind-table-r25.md` will cite S167, so gaining the path is the defined mechanism for recording the new citation.
4. **QUALITY criterion 17** (corpus/QUALITY.md:34): repeated canonical URLs across active rows must be screened and duplicates rejected/merged. Adding a second row with the identical pinned URL is the exact-duplicate case; the precedent pair S030/S045 (duplicate of S017's current-wiki scope) was rejected. Extending S167's used-by is the "merge" branch of that criterion.
5. **Anchor containment**: the bind-table topics the a3w1 seat located (lines 249, 256, 289, 293-294) all fall inside S167's already-registered anchor ranges (192-200, 238-262, 284-295). No anchor expansion is needed, so there is no anchor-side reason for a second row either.
6. The a3w1 report itself reached the same boundary: its draft is marked "Draft only; do not append a second registry row without resolving the existing S167 entry" after noting the exact URL/sha duplication with S167 (and that S016's live-wiki URL is a different identity, so no collision there).

Verdict on the registry move: the integrator correctly took the merge path.

## 4. Pending obligations observed (not defects of the move)

- `corpus/knowledge/bind-table-r25.md` **does not exist yet** (checked this reopen), while S167 is `mined` and now cites it in used-by. The contract's own census ("mined rows whose used-by paths do not exist — must print nothing", SOURCES-CONTRACT-v1.md:79-80) fails until that knowledge entry lands, which is the C1 data seat's deliverable this wave. If the wave closes without that file, the registry is left in a census-red state.
- The required old→new log of the used-by change belongs in round 25's lesson (`corpus/lessons/round-25.md` does not exist yet; latest is round-24). Expected line to record: `S167 used-by: corpus/knowledge/rule-attribution-r24.md → corpus/knowledge/rule-attribution-r24.md, corpus/knowledge/bind-table-r25.md`.

## Verdict

REOPEN S167: agree — fresh fetch reproduces the row's anchor byte-for-byte (8239 B, sha256 95d8b842…c417f0); all a3w1 located quotes are verbatim at their lines inside the row's anchor; a used-by extension is the header-sanctioned move for a same-URL re-citation, with the knowledge entry itself and the round-25 old→new log still owed this round.
