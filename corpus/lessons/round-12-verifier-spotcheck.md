# round-12 — non-author verification and spot-check (orchestrator, kaika)

Written by the integrator, not the lane (CORPUS.md: corrections and outside reviews are new
files; the lane owns `round-12.md`). Verifiers were fresh agents dispatched by the orchestrator
after the round landed at `8dbfc93cb`; full reports are committed in the fleet repo at
`.ufo/waves/kaika-w3/mado-review.md` and `mado-critic.md`.

## Spot-check (LEARNING.md — at least one admit and one reject)

| decision | sample | verifier | result |
|---|---|---|---|
| admit | U1 `window-rule-effects-getprop.md` (Hyprland 0.56 `hyprctl getprop`, read-only) — reviewer re-opened S017/S018/S024/S012 and local anchors; agree | W3ReviewMado | agree |
| reject | S012 rejected — agree; S030 (same URL as S017) — disagree with its admission: the lane rejected S030 in place in `8dbfc93`, moved its used-by to S017, and logged the reason — the disagreement became the correction | W3ReviewMado | agree |

## Adjudication

ADMITTED after post-review fixes `8dbfc93`. Per-axis: calibration improved (QUALITY criteria citing a lesson 0/5→11/16 — 9/16 rest on the lane's own mistakes; a citation count, not judgment quality), freshness improved conditionally (gate file-plane FAIL+UNKNOWN 1→0, 29/29 — holds only if the operator confirms `~/Projects/gkeep` stays; L0), coverage improved (U1–U3 sourced ground 0/7→3/7; capability `sources-registry`, 39 rows, census ok with one W04), operability unchanged, depth and adjacency unscored. Selftest 268→269, regression PASS after re-cut, live gate CLEAN. Trends: expansion improved, quality improved, discernment improved (narrow; 1+1 sample plus the S030 correction). Debts: four anchors owed a page revision (search log); misplaced LOG paragraph was routed back to the lane log (`aeb33b5`).
