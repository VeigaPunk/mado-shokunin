# Mado round 24 — Frontier step 3: lesson mistake draft

Seat: `MadoR24.ScribeLessonMistake` (scribe; evidence and recommendation only).

## Behavior

- Read round-24 registration and swept the round-23 lesson's existing M23-1–M23-7 rows and append-only correction, plus `round-23-verifier-spotcheck.md` §7.
- The seven §7 defects are explicitly routed in round-24 registration items 1–7. The earlier lesson already records M23-1–M23-7. I found no additional unrouted mistake in those two sources.
- Investigated the post-close-report candidate by comparing the inherited report copies with the round-23 data tip `fa819d56` and closure commit `8e5d936`. This produced one draft mistake below.

## Findings

`fa819d56` is committed at `2026-10-22T09:12:44-03:00`; closure commit `8e5d936` is `2026-10-22T09:19:50-03:00`. The non-author closure report records completion at `2026-10-22T09:13:47-03:00` (`corpus/lessons/round-23-verifier-spotcheck.md:15-16`). The inherited reports have later filesystem mtimes:

| inherited file | mtime (-0300) | at `fa819d56` | inherited SHA-256 |
|---|---|---|---|
| `r23-post-close-ConnSibling.md` | 2026-10-22 09:23:01 | Present; blob SHA-256 `d3aa17ff30ecfeb8e0df145537816b69927ad7d18b390189391b713f0362bb6a` | `49f83ae43f9223bb867478857d2f6fcd712de8ea8cc3b1943dad30706543af30` |
| `r23-post-close-ScribeProvinceScope.md` | 2026-10-22 09:27:35 | Present; blob SHA-256 `dbc0d1e5ce58f07eb2b61a34428e2b565996c4baf1d30ab0fc1c5d92ec616656` | `491656d1926b0ca2edaaeac3a219746db98cce72deaad06c6a72d8571752dcef` |
| `r23-post-close-ScribeRejectSweep.md` | 2026-10-22 09:14:54 | Absent at both `fa819d56` and `8e5d936` | `ca60c55f40b552ebfaeda96bd8c5d1f4bb4eba5114bf9ed1cc214be5510ef355` |

The first two inherited copies are not byte-identical to their committed report blobs. `ScribeRejectSweep` was a registered round-23 seat (`w1-assignments.json`, `w1-spec.json`) but its report is absent from both round-23 commits. The closure §7 items do not mention this report-finalization gap. **Observation:** the post-close artifacts and committed report set differ. **[INFERENCE]** A reviewer closing on the committed tip could not establish that the later inherited report versions were the versions reviewed at closure; the lane lacked an effective final-report completeness/identity gate for this evidence set.

### Draft row for `corpus/lessons/round-24.md` (not applied)

| id | class | evidence pointer | captured-by | fix / demonstrated boundary |
|---|---|---|---|---|
| M24-1 | report chronology / provenance | `.ufo/waves/round-24/inherited/r23-post-close-*.md` compared with round-23 tip `fa819d56` and closure commit `8e5d936`; see the timestamps and hashes above. `ScribeRejectSweep` is absent at both commits; the other two inherited copies differ from the blobs at `fa819d56`. | Round-24 scribe sweep (this report), by checking the assigned report paths, commit contents, and mtimes; not captured in round-23 closure §7. | Before closure, enumerate every assigned report at the declared final revision and require both presence and a SHA-256 match between its committed blob and the submitted final copy. This proposed fail-closed check is shown able to fail on this exact sample: `ScribeRejectSweep` is absent, and `ConnSibling` plus `ScribeProvinceScope` fail byte comparison against their `fa819d56` blobs. This is an observed failure condition, not a gate implemented or run. |

## Commands and outcomes

All Git commands below ran only in the scratch clone `/fast/scratch/hyaku/mado-r24/r23lane`; `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset. No Git or jj write command ran in the lane or fleet repository.

- Clone: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 60 git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin /fast/scratch/hyaku/mado-r24/r23lane` → `Cloning into '/fast/scratch/hyaku/mado-r24/r23lane'...` / `done.`
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 10 git -C /fast/scratch/hyaku/mado-r24/r23lane show -s --format='%H%n%cI%n%s' fa819d56` → `fa819d561d613cf3cfd8f58ed763e1ca57ab5eb4`; `2026-10-22T09:12:44-03:00`; `round-23: large raw wave receipts`.
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 10 git -C /fast/scratch/hyaku/mado-r24/r23lane show -s --format='%H%n%cI%n%s' 8e5d936` → `8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`; `2026-10-22T09:19:50-03:00`; `round-23 verifier spot-check (integrator, hyaku): non-author admit/reject`.
- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 10 git -C /fast/scratch/hyaku/mado-r24/r23lane ls-tree -r --name-only fa819d56 -- .ufo/waves/round-23/w1/reports` → includes `ConnSibling.md` and `ScribeProvinceScope.md`; no `ScribeRejectSweep.md`.
- For each of the three report paths, `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 10 git -C /fast/scratch/hyaku/mado-r24/r23lane cat-file -e REV:path` at `fa819d56` and `8e5d936` → ConnSibling and ScribeProvinceScope present at both; ScribeRejectSweep absent at both.
- For ConnSibling and ScribeProvinceScope, `git show fa819d56:path | sha256sum`, `sha256sum <inherited path>`, and `git show fa819d56:path | cmp -s - <inherited path>` → hashes differ and each comparison prints `content=differs`.
- `timeout 10 stat -c '%n|%y|%s' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/inherited/r23-post-close-*.md` → mtimes and byte counts shown in the table above (ConnSibling 22535 B; ProvinceScope 49928 B; RejectSweep 26815 B).
- `sha256sum` on the two current round-23 report paths and their inherited copies → the current paths match the `fa819d56` blob hashes above; the inherited copies have the differing hashes in the table. Current-path mtimes are 2026-10-23 00:11:26 -0300 and are not used as historical evidence.

## Gates, touched surfaces, and limits

- No build, test, lint, formatter, counter, or host probe was run; this is a documentation-only draft and main-agent verification remains outstanding.
- No packages or tools were installed or updated. No host display, compositor, service, or `~/.config` state was changed. No subagents were spawned and no `agent://all` message was sent.
- Lane file written: this report only. The report and lesson candidates were read; `corpus/lessons/round-24.md` was not created or edited. A read-only Git clone was created at `/fast/scratch/hyaku/mado-r24/r23lane` for historical inspection.
- Out of scope: the alternative round-24 one-character `agent://all` message candidate was not investigated. No external sources were opened.
- Limits: mtime and hash establish timing/identity differences, not authorship intent or the substantive correctness of later report text. The closure gate described in the draft is a recommendation, not an existing or executed check.

Verdict: **DRAFT ONLY** — one post-tip report chronology/provenance mistake is evidenced; no change to `corpus/lessons/round-24.md` was made.

Report: `.ufo/waves/round-24/w1/reports/ScribeLessonMistake.md`
