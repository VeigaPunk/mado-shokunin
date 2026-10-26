# CritC2Cheat (round 44, w1) - forgeries against the C2 predicate

Seat: `w1/CritC2Cheat`. Deliverable: `.ufo/waves/round-44/w1/CritC2Cheat/forgeries.md`. Frozen
predicate `quality/counters/c2-r44-gkeep-size-request.py` at `e2289516a9a857f55cda7be635933e89b931c3da`,
base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`. The counter, the pins, the registry, the lesson and the
L1 draft were read only; this seat wrote only `w1/CritC2Cheat/` and this report. Nothing in the lane was
mutated, no git index touched outside the throwaway clones, no package transaction, no host read beyond
none at all (no compositor call was needed).

## Result in one line

The frozen counter admits **9 of 9** forged entry+registry+lesson sets (`frozen-all.txt`); a patched copy
with four tightenings (`T1-T4`, `tighten.diff`) admits only the grounded baseline and rejects
**5 of the 9**; the remaining **4 are residuals** the counter cannot close.

| variant | frozen | tightened | class |
|---|---|---|---|
| F0-BASE (L1 draft registered on S164+S298-S301, grounded) | MET | MET | baseline |
| F1-CLAIM-INVERSION (true GTK quote, inverted claim) | MET | MET | residual (non-author reading) |
| F2-FORGED-PIN (held S164 cites a doctored `Hyprland-Window.cpp`; census becomes `xdg_setSize=0`) | MET | MISSED | **defect d**, closed by T1 |
| F3-LOCATION-DRIFT (pinned bytes, 1.49→1.48 and gkeep commit→all-zero URLs) | MET | MISSED | **defect e**, closed by T2 |
| F4-SIZE-REQUEST-PROSE (true census, prose calls `set_size_request(420, 500)`) | MET | MISSED | **defect h**, closed by T3 |
| F5-DEFAULT-SIZE-PROSE (true census, prose asserts `set_default_size(800, 600)`) | MET | MISSED | **defect h**, closed by T3 |
| F6-OVERCLAIM-TABLE (protocol answer, no id named) | MET | MET | residual |
| F7-CONTENT-FREE-SHELL (17-line entry reaches the target) | MET | MET | residual (coverage not measured) |
| F8-REGISTRY-ANCHOR-LIE (`scope`/`teaches` cells assert a falsehood) | MET | MET | residual (cells 3-6 of a new row unread) |
| F9-REGISTRY-ANCHOR-OUT-OF-RANGE (anchor `gdktoplevel-wayland.c:9999-10005`, receipt 2964 lines) | MET | MISSED | **defect**, closed by T4 |

## The four fixable defects (smallest safe correction)

1. **d pins new ids only** - `c2-r44-gkeep-size-request.py:496-499` (`pin_ok = True`; `if i in new_ids:`);
   clause i's coverage test compares names: `:603` (`used = set(os.path.basename(...))`). The docstring at
   `:31-32` promises the held receipt "must be byte-equal to be counted by i+" - the code does not do it.
   F2 replaces the pinned `Hyprland-Window.cpp` for held S164 and the census clause h then recomputes
   `xdg_setSize=0 x11_configure=0` from the forgery and blesses it: the inverted central fact of C2 is
   admitted. T1 (4 lines): apply the existing digest test to every cited id. F0 stays MET.
   Inheritance: the same branch at `c2-r43-gkeep-entry-v2.py:490-492`, `c2-r42-gkeep-entry.py:410-412`,
   `c2-r41-focus-entry-v2.py:367-369` - four rounds of C2 counters carry it.
2. **e binds names, not provenance** - clause e compares the location's last path component with the
   receipt basename; e+ pins only Hyprland URLs to the commit. A 1.49 receipt cited as 1.48, or a pinned
   gkeep file cited at commit `0000…`, is admitted. T2: keep each pin's URL and require it for pin-named
   receipts. F0 stays MET; F3 goes `e:0`.
3. **h does not read the entry's own prose** - the census lines are true and required, but another line may
   deny them (`set_size_request(420, 500)` with `size_request_calls=0`; `set_default_size(800, 600)` with
   `default_size=420x500`). T3 (~20 lines in clause h): any other unfenced line's `set_size_request(`,
   `set_default_size(W, H)`, `xdg_setSize=`, `x11_configure=` must agree with the censused numbers. F0
   stays MET (its S301 line quotes `420, 500`; "no `set_size_request` call" has no parens); F4/F5 go `h:0`.
4. **registry anchor ranges are unchecked** - a new row's `anchor` cell can point past EOF. T4 (12 lines,
   new ids): the anchor must name the gated receipt's basename and stay inside its line count. F0 stays MET;
   F9 goes `e:0`. This adds a format requirement to the registry row, so it is an extra-window change.

## The four residuals (no tightening that keeps a genuine entry admitted)

- **F1, F6** claim-to-quote binding: a true quote at a true locator beside a claim it does not support (the
  inversion in prose, or a decision table that names no id so `all_body_lines_bound` never fires). Any
  lexical "always/must" detector grades hedging style, not grounding.
- **F7** content coverage: a 17-line entry (5 bound quotes + the 2 census lines, 7 facts of ~20 the claim
  names) reaches the target. A line/word floor is defeated by padding; another computed census line is
  bookkeeping and would change the genuine entry's format; "quote must be load-bearing" is a lexical
  approximation a forger writes to. Content needs a different instrument.
- **F8** registry prose: cells 3-6 of a new row are never read by PRED-C2-r44, so a false `scope`/`teaches`
  beside a truthful anchor is admitted. T4 closes only the locator half (F9).

## Support finding for the claim (not an attack)

Registration says "No positive control exists at the freeze". One does: the L1 draft
`.ufo/waves/round-44/l1-draft/entry.md` (69 lines) registered on S164+S298-S301 scores
`admitted=1/1 TARGET_MET` at fixture commit `b996e119571af6e45bb74c61aae12fc6d0436c47`; the five quotes
recompute to the locators the draft states (`1687`, `455`, `1150`, `681`, `475`) and the census recomputes
to `xdg_setSize=1 x11_configure=1`. So C2's target is reachable with the provisional ids and pin quotes,
and the four registry rows + five GATE lines I used are a working registration pattern for the builder.
The larger rot holes named in the closure (D1-D7) were out of this seat's scope.

## Evidence (all paths relative to the lane root)

- `.ufo/waves/round-44/w1/CritC2Cheat/forgeries.md` - the deliverable, per-forgery lines + clause + fix.
- `w1/CritC2Cheat/frozen-all.txt`, `frozen-<VARIANT>.txt` - frozen counter verdicts (9/9 admitted).
- `w1/CritC2Cheat/c2-r44-tightened.py`, `tighten.diff`, `tight-all.txt`, `tight-<VARIANT>.txt` - T1-T4 and
  the patched scores (F0 MET; F2/F3/F4/F5/F9 MISSED; F1/F6/F7/F8 MET).
- `w1/CritC2Cheat/fixtures/`, `fixtures-manifest.md` - the committed forged bytes and their commits.
- `w1/CritC2Cheat/verify-quotes.txt` - 25 locator checks, PASS, every quoted line recomputed by grep
  (`evidence-lines.txt` holds the raw grep output).
- `w1/CritC2Cheat/harness.py`, `collect.py`, `tighten.py`, `verify-quotes.py` - reproduction.

Reproduce end to end:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-44/w1/CritC2Cheat/harness.py     # 10 fixtures under /fast/scratch/hyaku/mado-r44/CritC2Cheat
python3 -I .ufo/waves/round-44/w1/CritC2Cheat/collect.py
python3 -I .ufo/waves/round-44/w1/CritC2Cheat/tighten.py
python3 -I .ufo/waves/round-44/w1/CritC2Cheat/verify-quotes.py
```

## Checks the integrator should run

- Frozen C2 on the data commit and the tip (the target and the kill rule are the integrator's call).
- If T1-T4 are adopted: re-score the genuine entry under the patched copy before re-registration; T1/T2/T3
  keep it MET, T4 needs its registry anchors to carry `<receipt basename>:<a>[-<b>]` ranges inside the
  receipt (the draft's four rows already do).
- C1 is untouched by this seat: PRED-C2-r44 reads no tool and no fixture wrote `tools/mado-geometry.py`.

## Tooling

None installed. `python3` 3.14 stdlib only; `git` for the throwaway clones. Fixture clones lived under
`/fast/scratch/hyaku/mado-r44/CritC2Cheat/` and were deleted after `collect.py` copied their committed
bytes into this seat's `fixtures/`; the receipt paths above are seat-local.
