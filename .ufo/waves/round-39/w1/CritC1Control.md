# CritC1Control — C1 do-nothing control (UFO-FSD critic)

Role: leaf critic, C1 calibration control. Summary: the re-registration is the ONLY delta.
Red-before reproduces exactly (18/19, exit 1); green is the same landed-pair green that existed
since b6c1d31 and was never a claim until the round-39 freeze declared it (no frozen predicate
in the checker or the manifest itself).

## Environment
- Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
- HEAD (tip): `457d1b125932c1e0d797061a2156b917bcd7edaa` (round-39 freeze commit); base parent
  `08be4eb7fd13358ed29b096e8924005d46ac409c`.
- No tool installs (no new tools needed; system `python3 -I` + read-only git).
- No lane files written except this report; all scratch in /tmp.

## Method (all runs sandboxed by the checker itself)
Checker `quality/check-r38-discrimination.py` clones the lane (`git clone --shared`) into a
scratch root, sparse-checks-out corpus/tools/quality/.ufo/waves/round-38, checks out `--rev`,
applies each control's writes, commits with sandbox identity, and runs the counters against the
sandbox HEAD. The lane is never mutated (git status confirmed clean before/after; only the
round-39 wave's own untracked files exist).

- Counters at tip: `quality/counters/c1-r38-event-ground.py`, `quality/counters/c2-r38-eventq.py`
- Counters unchanged base→tip: `git diff 08be4eb 457d1b1 -- <both counters>` → empty.
- Old frozen manifest bytes: git blob `93f168c671fbca43df72abea86ba236f52396a36` (round-38
  frozen `controls/manifest.json`), extracted to `/tmp/critc1-manifest-old.json`; sha256
  `14c49d9fec35dc9bc307fbdd5c732e2ce80fabeaadfe3327b9121f50b9553edb` == the committed copy
  `.ufo/waves/round-39/receipts/manifest-frozen-r38.json` (byte-identical).
- New manifest: `.ufo/waves/round-39/c1/manifest.json`; sha256
  `96965518dc8ad98b52b28b406d66841758c80fd75610f9b94e0239b8adf838c8` == git blob
  `ec347320fff6e3f5559c39ee8439824d00c7a10b` == round-38 landed manifest at b6c1d31.

## RED control — old frozen manifest × current counters at tip
Command:
```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/check-r38-discrimination.py \
  --c1 quality/counters/c1-r38-event-ground.py \
  --c2 quality/counters/c2-r38-eventq.py \
  --manifest /tmp/critc1-manifest-old.json --rev HEAD \
  --sandbox-root /tmp/critc1-sb-red --out /tmp/critc1-red.txt
echo $?   # -> 1
```
Output: `MADO_R38_DISCRIMINATION: controls=19 correct=18/19 verdict=TARGET_MISSED`, exit 1.
Sole failure: `control=c1-duprow instrument=c1 expected=TARGET_MISSED observed=TARGET_MET ok=0`
(the append-at-file-end duplicate is outside the counter's `## Registry` parser).
`diff /tmp/critc1-red.txt .ufo/waves/round-39/receipts/c1-redbefore.txt` → IDENTICAL (matches
the committed before receipt).

## GREEN run — new manifest × current counters at tip
Same command with `--manifest .ufo/waves/round-39/c1/manifest.json` (no other change).
Output: `controls=19 correct=19/19 verdict=TARGET_MET`, exit 0.
`diff /tmp/critc1-green.txt .ufo/waves/round-39/w1/ExecC1After/after-freeze.txt` → IDENTICAL.

## Only delta between red and green
Structural JSON comparison (python) of the two manifests:
- Same 19-control id set; for every control `instrument`/`expect`/`clause`/`rev`/`base`
  identical; same `note`, same `frozen_at`.
- The single functional difference is `c1-duprow`'s first write: old = `{"op":"append",
  path:"corpus/SOURCES.md"}` (row appended at file end); new = `{"op":"py",...}` code that
  inserts the duplicate S189 row *after the S217 line* (inside `## Registry`).
Counters are byte-identical in both runs. ⇒ the manifest bytes are the only delta; the repair
is exactly the duprow write relocation.

## No frozen predicate — why a green run alone is not a claim
1. The checker performs ZERO freeze/registration validation: `grep -iE 'frozen|registr|claim|declar' quality/check-r38-discrimination.py` hits only docstring prose; `main()` does `json.load(open(a.manifest))` and scores whatever file it is given. The verdict line `TARGET_MET` does not record that the manifest is the registered predicate.
2. `.ufo/waves/round-39/c1/manifest.json` first appears in history at the freeze commit:
   `git log --oneline --diff-filter=A -- .ufo/waves/round-39/c1/manifest.json` → only
   `457d1b1`. Before the freeze there was no round-39 manifest to run at all.
3. The identical green result already existed since `b6c1d31` (round-38 manifest fix) as the
   *landed* pair (blob ec34732 present at b6c1d31) and was NOT a claim during round 38 — the
   round-38 declared predicate froze the OLD manifest (18/19 red). Registration.md routed defect
   #1 states this verbatim: “The round-38 pair as frozen failed (frozen × frozen = 18/19); the
   landed pair's 19/19 is a new predicate, re-registered here with a fresh freeze.” So the same
   checker output was a non-claim before registration; freezing is a repo/registration act, not
   a checker property.

## Verdict
- Re-registration is the only delta: old pair still red (18/19, exit 1, sole c1-duprow miss),
  new pair green (19/19, exit 0) — counters untouched at base and tip.
- A green run of the new manifest without the freeze commit would print the same TARGET_MET and
  would not be a claim: no frozen predicate exists outside the registration (the checker and the
  manifest are both inert w.r.t. registration status).
- No counterexample found; no correction needed. Control receipt = the red/green transcripts
  above (byte-identical to committed c1-redbefore.txt and after-freeze.txt).
