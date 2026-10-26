# CritC1Explain — C1 clause x falsification

Axes: C1 operability, specifically correctness/operator trust of explain and `--observed`.

## Result

Scored three one-line mutants against the frozen counter at base `d7527d608ad2b2e3cc398fdde34db7947b254a1a`. The exact full invocations are below; each used an isolated clone under `/fast/scratch/hyaku/mado-r47/CritC1Explain/tree`, asserted clone top-level before commit, committed only the candidate tool, and ran with a distinct `--work` directory and fixed nonce.

1. **Passes (bad): discard final cmd line before observed comparison.** Candidate changed only `mine = run_print(...)[0] if ok else ""` at reference line 851 to `mine = run_print(...)[0].rsplit("\n", 1)[0] + "\n" if ok else ""`. It claims AGREE while failing to compare the final printed command line (third output item). Counter result: `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, clause x `explained=190/190`, revision `80248c097ed2a5fb6374bb8f4a87fd688bdd05ad`, nonce 4700. Thus the frozen test sees good capture and a mutation of the *first* `.desktop` token only; it never alters the third cmd item, leaving a command-line false-AGREE undetected. **Smallest safe correction:** add an observed negative capture with only line 3 changed (and assert DIFFER/1); maintain exact three-item comparison.

2. **Rejected: ignore command line entirely in observed compare.** Changed only `mine == observed` at reference line 852 to `mine.splitlines()[:2] == observed.splitlines()[:2]`. Result `explained=25/190`, target missed; the existing negative capture changes first item and fails as well. This confirms clause x catches a broad regression, not the narrow third-item hole above.

3. **Rejected: return success for DIFFER.** Changed only `rc = 0 if verdict == "AGREE" else 1` at reference line 853 to `rc = 0 if verdict == "AGREE" or verdict == "DIFFER" else 1`. Result `explained=25/190`, target missed; the existing bad capture detects it.

## Commands

For pass candidate, after the clone and top-level assertion:

```sh
python3 -c 'from pathlib import Path; p=Path("/fast/scratch/hyaku/mado-r47/CritC1Explain/candidate.py"); s=p.read_text(); old="mine = run_print(env, [\"--print-id\", \"--print-path\", \"--print-cmd\"])[0] if ok else \"\""; new="mine = run_print(env, [\"--print-id\", \"--print-path\", \"--print-cmd\"])[0].rsplit(\"\\n\", 1)[0] + \"\\n\" if ok else \"\""; assert old in s; p.write_text(s.replace(old,new,1))'
cp /fast/scratch/hyaku/mado-r47/CritC1Explain/candidate.py /fast/scratch/hyaku/mado-r47/CritC1Explain/tree/tools/mado-terminal.py
git -C /fast/scratch/hyaku/mado-r47/CritC1Explain/tree add tools/mado-terminal.py
git -C /fast/scratch/hyaku/mado-r47/CritC1Explain/tree -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-terminal.py --repo /fast/scratch/hyaku/mado-r47/CritC1Explain/tree --rev HEAD --work /fast/scratch/hyaku/mado-r47/CritC1Explain/work --nonce 4700
```

The two rejected variants used the same steps, replacing `candidate.py`, candidate work path, and nonce with `work2`/4701 and `work3`/4702 respectively; `work4`/4703 was the DIFFER-exit mutant. Captured outputs were in `score.txt` through `score4.txt` under that scratch root; counter output above is direct. The counter run writes only to explicit scratch `--work`. No host resolver, compositor, terminal or GUI was launched.

**Operator-important hole:** a capture differing only in the command-line (third printed item) can be reported AGREE by a tool that still scores TARGET_MET. Registration says the capture's three printed items must equal tool `(id, path, command line)`; counter code at `quality/counters/c1-r47-terminal.py:277-290` mutates only first `.desktop`, while reference comparison is exact (`l1-draft/mado-terminal.py:851-853`). Add third-item-only mismatch case before data lands.
