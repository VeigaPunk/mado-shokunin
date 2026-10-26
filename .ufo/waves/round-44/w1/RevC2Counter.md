# RevC2Counter — C2 counter attack (round 44, w1) — FINAL

Status: COMPLETE 2026-10-26. Counter `quality/counters/c2-r44-gkeep-size-request.py` NOT edited.
Full findings: `.ufo/waves/round-44/w1/RevC2Counter/findings.md`. Builder + logs in the same dir
(`build_fix.py`, `log-honest.txt`, `log-forged_s164.txt`, `log-hidden_line.txt`,
`log-hidden_line_control.txt`, `log-false_url.txt`). Scratch deleted after the copy.

## Diff classification (r43-v2 → r44; 6 hunks, rest byte-identical)
docstring 3-35 · constants 145-149 (PRED/BASE/ENTRIES/LESSON/FETCH) · constants 167-172 (PINS 9→5,
sha256s verified equal to lane fetch/) · constants 176 (STAGED drops gkeep-size-to-real-size-r11) ·
clause h 382-409 (host_census rebuilt) · clause-h exclusion 561-563 (entry_lines prefixes).

## Findings
- **F1 HIGH — held-id receipt substitution.** Clause d applies the PINS digest check only to NEW ids
  (counter :496-499); clause i (:603) checks basename coverage only, although the docstring (lines
  26-28) claims a held id's receipt "must be byte-equal to be counted by i+". Fixture `forged_s164`:
  forged 8-line `Hyprland-Window.cpp` at fetch/ (sha256 ae0db5c0… ≠ pin d735d454…), gate on held S164
  with the forged sha, census flips to `hyprland sendWindowSize xdg_setSize=0 x11_configure=0`
  (truth 1/1), S164 claim asserts the opposite of the forged body → **admitted=1/1, exit 0**.
- **F2 MEDIUM — census-prefix filter hides claim lines.** `entry_lines` (:559-563) exempts every
  `gkeep client `/`hyprland sendWindowSize ` line from the g+ universal binding (all_body_lines_bound
  :354); the real census lines carry no S tokens, so the exemption is pure hiding channel. Fixture
  `hidden_line`: extra line 14 `gkeep client follow-up: per S164 …` with no quote/locator → 1/1;
  control without the prefix → g:0, 0/1 (filter is the sole enabler).
- **F3 LOW — false provenance URL for non-Hyprland pins.** Clause e binds location↔receipt by basename
  containment only; the raw.githubusercontent prefix check fires only for `hyprland-` receipt names.
  Fixture `false_url`: S301 location `https://example.com/docs/ui.py` with the genuine pinned receipt
  → 1/1.
- **F4 INFO** — `#`-comment stripping in .py strips inside strings (gkeep-ui.py:145
  `foreground="#202124"`); on the real pin raw==stripped (set_default_size 420,500 ×1, application_id
  org.omarchy.gkeep ×1, set_size_request 0) — no effect today; a docstring/string `set_size_request(`
  would be counted as a "call" (label) though the docstring defines occurrences.
- **F5 INFO** — sendWindowSize body bound sound on the real pin: first lone `}` at line 1754 is the
  function's closing brace; X=1 Y=1 true (whole-file 2/3); fragile to a column-0 `}` or signature
  whitespace drift.
- **F6 INFO** — census without receipts: structurally impossible (byname ⊆ receipts_raw; clause i
  requires all five pin basenames). No bypass.
- **F7 INFO** — `host_census` params `new_ids`/`reg_rev` dead in r44.

## Verification exercised
Five git fixtures built and scored with the frozen counter (`python3 -I … --repo <D> --rev <rev>
--base <base>`): honest 1/1 (baseline validates harness), forged_s164 1/1 (F1), hidden_line 1/1 (F2),
hidden_line_control 0/1 (F2 control), false_url 1/1 (F3). All verdicts reproduced on a second run.
PINS sha256s verified against lane `.ufo/waves/round-44/fetch/` (all five match).

## Tooling record
No tools installed or updated (none needed; python3 stdlib only). No pacman, no host-service or
compositor mutation, no writes outside the seat dir; scratch `/fast/scratch/hyaku/mado-r44/RevC2Counter`
deleted.
