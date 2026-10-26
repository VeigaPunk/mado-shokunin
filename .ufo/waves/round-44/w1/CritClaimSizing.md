# CritClaimSizing — round-44 w1 claim sizing (final)

Seat: leaf critic. Scope: attack the round's claim sizing before any data (prompt §6 item 9), against
registration `e2289516` and the frozen counters. Full detail, exact sentences/lines and command outputs:
`.ufo/waves/round-44/w1/CritClaimSizing/findings.md`; control bytes under `.../CritClaimSizing/controls/`,
scorer logs under `.../CritClaimSizing/receipts/`. Scratch `/fast/scratch/hyaku/mado-r44/CritClaimSizing/`
deleted before yield; every cited run's bytes/logs are in the seat dir.

## Verdict: C2 is not control-safe; C1 survives with sizing corrections

**F1 [HIGH] A near-do-nothing control reaches C2's target.** The staged r12 predecessor, re-pointed to lane
ids (`S311→S164`, `S312→S301`) + three pin quotes + the two census lines = 27 lines / 205 words, is
`admitted=1/1 verdict=TARGET_MET` (rev `de2c7ee7`, `receipts/c2-r12-repoint.log`); an 18-line quote-only entry
is also admitted (rev `4fce5c90`, `receipts/c2-minimal-quotes.log`). Both hold **zero** of the five behaviours
C2 names: `scheduleConfigure=0 onAck=0 X11=0 xdg_surface=0 ack_configure=0`
(`receipts/admitted-control-surface-counts.txt`). No PRED-C2-r44 clause recomputes those surfaces from the
pins; clauses b–i+ are structural. Under the registration's own rule ("a hole w1 finds before any data commit
re-registers as v2"), C2 must re-freeze with a clause that binds the five surfaces to pin-computed
phrases/locators, or shrink the claim to the five quotes + two census lines.

**F2 [HIGH] The frozen C2 control set misses the exact cheap variant.** `ctl-c2.txt` (0 of 3) tests the
verbatim r12 copy, which fails only on package ids; the in-round re-grounding the assimilation contract
*requires* (id re-point) flips it to MET (`C2-STAGED-COPY … a:1 b:0 c:0 d:0 e:0 f:1 g:0 h:0 i:0` — all
failures structural). Add F1's control to the receipt; 0-of-N is not earned until F1's clause lands.

**F3 [MEDIUM] C2's ground is legitimate but its after-state is admission, not the claimed coverage.**
`corpus/README.md:301` names "the client's acknowledgement path" open (frontier→core is real), yet 3 of the
6 elements are already in the staged r12 file verbatim (`gkeep-client-size-request-r12.md:24,26,28,43`) and
the five genuinely new ones are unmeasured (F1). Record the coverage as the acknowledgement-path entry (5 pins
bound + 2 census lines), not as the five-surface claim.

**F4 [MEDIUM] C2 predicate text contradicts its code.** Docstring `:49` says "ten pinned receipts" while
`PINS` (`:167`) has five and the code enforces `set(PINS) <= used` (`:604`); inherited clause h (`:107`)
requires own-work receipts `host-gkeep.conf`, `host-clients-r43.json`, `gkeep-ui-excerpt.py` that r44's PINS
does not include and the rebuilt `host_census` (`:382`, check `:388`) does not read. The frozen predicate is
not one sentence across plan/code/receipt. Fix in the re-freeze (rewrite clauses, not a prefix override).

**F5 [MEDIUM] C1 is a contract extension, not a false-report fix — and it is double-booked.** registration:13
calls the round-43 DIFFER "a false report", but `tools/mado-geometry.py:57` says "DIFFER is a report, not a
fault: a user may have resized the window" and the admitted r43 entry (`hyprland-gkeep-geometry-r43.md:46`)
already records the box is handed over only "for a floating, non-fullscreen window"
(`!Fullscreen::controller()->isFullscreen(...)`). The same change is booked as C1 (registration:12) and as
mistake mining (registration:82). Strike the "false report" premise; keep one booking.

**F6 [MEDIUM] C1's target is a small local patch / a committed answer key, and its published number does not
move.** A 12-added-line patch already reproduces all 26 fixtures byte-exactly (`fixtures=26/26`, `TARGET_MISSED`
only on clause b, `selftest=73/73`); a 30-added-line patch is `TARGET_MET` (`selftest=80/80`, `b4 15/15`,
`receipts/c1-patch17.log`); installing the committed reference (one `cp`, rev `7acbf9c0`) is `TARGET_MET`
(`receipts/c1-ref-installed.log`). Operability's published fraction is `check-index.py --selftest` 12/12
(`axis-base.txt`), untouched by C1. Declare a bounded operability sub-axis with a number
(e.g. 0/2 → 2/2 verdict words; 0/26 → 26/26 fixtures; selftest 73 → ≥80).

**F7 [MEDIUM] C1's declared SKILL/PROVINCE surface has no clause.** registration:47 claims the SKILL/PROVINCE
rows; `grep -c "SKILL\|PROVINCE" quality/counters/c1-r44-geometry-states.py` → `0` — the counter reads only the
tool and `c1-r42`. A tool-only landing passes while `SKILL.md:270-277`'s verdict table and the round-43
capability row stay stale. Add a clause or scope C1 to the tool and leave D3 to the frontier-step fixes.

**F8 [LOW] C1's b4 "state teeth" label overstates its mechanism.** `state_sites` (`:265`) counts every
comparison in any function whose body contains a "fullscreen" string; my patch gained 15 sites (5 in `report`,
unrelated to state) and all 15 died on the pre-existing 73-case selftest. Narrow the site selection or relabel.

**F9 [MEDIUM] The lowest-axis argument is unsupported for C2 and vacuous for C1.** `axis-base.txt` derives only
3 axes (navigation, calibration, operability) and checks published==derived; it has no coverage row, so it
cannot ground C2's coverage claim, and C1 changes no published number. SCORECARD saturation is 9.0 / N=3 with a
round-43 capability inside the window (nudge not waived), so the obligation stands and needs explicit numbered
sub-axes. Add the coverage row / new sub-axis, or name each claim's before→after score.

**F10 [PASS] Separability holds.** C1's instrument reads the tool + `c1-r42`; C2's reads entry/registry/lesson/
README/pins — disjoint. My C2-only commits left the tool byte-identical (`e3c2e471…`), and the C1 controls score
without C2 bytes. Caveat: because C1's documentation half is unmeasured (F7), partial C1 is undetectable.

## Asked-item ledger

1. Cheapest controls: README-only → C1 14/26 MISSED, C2 0/1 MISSED. 12-line patch → C1 26/26 fixtures, MISSED
   (b). 30-line patch → C1 MET (minimum implementation, ~30 lines). r12 re-point / quote-only → C2 MET.
2. C1 surface: the tool's per-client verdict vocabulary + summary line; extension of the round-43 capability,
   not a bug fix (F5); needs a new sub-axis (F6/F9) and no mistake-mining double book.
3. C2 ground: new per README:301, but 3/6 elements are the predecessor's and the counter measures none of the
   new five (F1/F3).
4. Universal clauses: C1's contract values are fully enumerated (`FS_POOL`/`fsvals0` incl. list/dict/bool/
   float; clause r guards byte-identity) — no defect there; C2 has two text/code contradictions (F4); C1's b4
   label overstates (F8); registration:16's universal over "published axes" is not enumerated (F9).
5. Lowest-axis argument against `axis-base.txt`: F9.
6. Separability: F10 PASS.

No tools installed; no pacman transaction; no host/compositor mutation; read-only git only; all fixture git
work in a scratch clone (`git rev-parse --show-toplevel` = scratch dir, recorded in
`receipts/fixture-facts.txt`), deleted at exit.
