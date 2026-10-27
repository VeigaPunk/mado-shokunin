# C2 clause (c): novelty mutation probes

Probe scope: exercise the frozen C2 counter at the data revision `a0e34387b30538372a1bb219eb3ccdc74013d458` on the actual entry and a scratch clone. Clause (c) has an entry-body minimum of 300 unique word-8-grams and requires maximum per-file entry-shingle coverage `<=30%` against base knowledge and candidate paths. The counter tokenizes lowercase ASCII `[a-z0-9]{2,}`; it does not remove stopwords. Candidate enumeration is by path prefix `.ufo/waves/round-*/candidate/` and does not impose a file extension.

## Execution

Scratch driver: `/fast/scratch/hyaku/mado-r51/MutC2Novelty/probe.py`; disposable clone: `/fast/scratch/hyaku/mado-r51/MutC2Novelty/clone`. Clone `HEAD` was checked as the specified data revision. Driver ran the executable `python3 -I .../c2-r51-dispatch-entry.py --repo <clone> --rev HEAD`, with `TMPDIR=/fast/scratch/hyaku/mado-r51/MutC2Novelty`.

| Input | Observed final line / exit | Clause (c) interpretation |
|---|---|---|
| Pristine entry | `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458`; 0 | Baseline succeeds; not a killed mutant. |
| Sentence-line order reversed | same final line; 0 | Survives. Sentence order does not alter the shingle set (line reversal is even less disruptive than semantic paraphrase). |
| Inserted repeated stopword `the` throughout | same final line; 0 | Survives. This exact insertion does not change set-based word-8-grams enough to cross threshold; stopwords are retained but repeated-token shingle sets saturate. |
| Replaced ` - ` with Unicode em dash | same final line; 0 | Survives. ASCII tokenization treats punctuation separators as equivalent; overlap remains below threshold. |
| Wrapped whole entry in fenced block | same final line; 0 | Survives. This particular candidate remains admitted; `body_text` strips fenced text for the entry body, but clauses a/b/d still see entry text. Not evidence that arbitrary fenced text changes are ignored; it shows no kill for this wrapping mutation. |
| “Extension candidate” (entry unchanged; preliminary label only) | same final line; 0 | Same as baseline. |
| Added identical entry as `.ufo/waves/round-51/candidate/novelty-probe.weird` | same final line; 0 | Survives; expected detector should reject clause (c), since the candidate duplicates the whole entry. This is a concrete miss: `CAND_RE = ^\.ufo/waves/round-[^/]+/candidate/.+` accepts this path, but enumeration uses `git ls-tree` at `--rev HEAD`; scratch-created uncommitted candidate bytes are not in that revision and thus are absent from the scored baseline. This establishes revision-snapshot exclusion of uncommitted candidates, not an extension filter. |

## Verdict and boundary

Pristine baseline PASS; all six attempted variations yielded `TARGET_MET`, so none was killed by the overall detector. These results do **not** quantify exact overlap percentages: the counter only reports the top three comparison overlaps for a passing entry, and the captured final-line-only driver discarded its detail lines. The target remains the frozen predicate; this is an advisory coverage/operability finding, not an amendment.

The assignment's “tokenized source metadata” surface is not shown to affect clause (c): source metadata is excluded by `body_text` only for lines beginning with `source`, `ground`, `held`, `verified-at`, `recheck`, `lane`, or `pin`, and the scratch probe did not mutate cited metadata independently. Fenced blocks were tested only by wrapping, not moving meaningful prose out of fences. No claim is made that these untested variants evade the threshold. Candidate extension matching itself appears broad by source inspection, but a committed unusual-extension candidate fixture was not tested; the only extension probe was uncommitted and therefore not visible to the pinned `HEAD` enumerator.

Commands/evidence: `python3 probe.py` in the scratch directory (output captured in the session); counter implementation ranges `quality/counters/c2-r51-dispatch-entry.py:434-486`, especially tokenization lines 449-453 and candidate snapshot enumeration 467-474. No lane files were edited.
