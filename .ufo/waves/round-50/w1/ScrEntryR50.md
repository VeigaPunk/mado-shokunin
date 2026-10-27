# ScrEntryR50 — round-50 bind-entry candidate

STATUS: complete. This is a scoped draft for L1 integration; no tracked lane file was changed.

## Behavior and result

Prepared `hyprland-bind-key-match-r50.md` from the round-49 candidate, re-pointing the host receipt and source-pin paths to round 50, setting `Round: 50` and `verified-at: 2026-10-27`, and retaining provenance rows S352-S363 plus held S318/S319. The host counts and raw-JSON digest are the required `<<total>>`, `<<named>>`, `<<code>>`, `<<mouse>>`, `<<switch>>`, and `<<sha256>>` placeholders for L1 to fill from `binds-live-r50.txt`. The entry retains `## Limits` with eight bullets and replaces the stale Shift-dead premise with the source-based reading that the bind comparison state never receives modifiers; its host paragraph states Shift binds are not dead.

`verify-quotes.py` checks all inline quotes/locators against fetch pins and row citations, requires a verified quote on every numbered step, and checks all seven clause-j topics at their implementing source lines. Command:

```sh
python3 -I .ufo/waves/round-50/w1/ScrEntryR50/verify-quotes.py \
  --entry .ufo/waves/round-50/w1/ScrEntryR50/hyprland-bind-key-match-r50.md \
  --fetch .ufo/waves/round-49/fetch \
  --rows .ufo/waves/round-49/candidate/rows.md \
  --output .ufo/waves/round-50/w1/ScrEntryR50/quotes-verified.txt
```

Observed output: `pins=22 row_cited_pins=22 numbered_steps=17 quotes=86 verified_quotes=86`; state, case, mask, code-form, zero-mod-sym-state, depressed-mask and option-read all `PASS`; final `PASS`.

## Evidence and gates

Read-only live capture (with `HOME` and all XDG state dirs under `/fast/scratch/hyaku/mado-r50/ScrEntryR50/work`):

- `hyprctl version` → Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f`.
- `hyprctl binds -j` → 90,401 bytes; SHA-256 `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`.
- `hyprctl getoption input:resolve_binds_by_sym -j` → `int=0`, `set=false`.
- Shape-only calculations: 192 total, named 142, code 42, mouse 6, switch 2, catch-all 0; keycode set has 14 values (`10-21`, `61`, `201`); modifier histogram is recorded in `binds-shape-r50.txt`. No raw JSON, device names, titles, dispatcher arguments or command text are present in the seat receipt. The measured digest matches the round-49 live capture's stated digest.

A scratch diagnostic used a shared clone and the round-49 counter; before its first commit, `git -C "$D" rev-parse --show-toplevel` matched `$D`. After inserting the candidate rows inside the Registry section (before `## Paths`), the counter reported `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:0 j:1 r:1`. Thus the relevant b/c/d/e/j quote and row-pin clauses passed; i remained 0 because this diagnostic clone did not include the separate admitted-row gate evidence. An initial scratch setup placed rows after the Registry section and correctly reported missing registry rows; moving them into Registry fixed that setup error. This was a round-49-counter diagnostic, not a round-50 frozen-counter score.

## Touched surfaces and limits

Only these scoped files were written:

- `.ufo/waves/round-50/w1/ScrEntryR50/hyprland-bind-key-match-r50.md`
- `.ufo/waves/round-50/w1/ScrEntryR50/verify-quotes.py`
- `.ufo/waves/round-50/w1/ScrEntryR50/quotes-verified.txt`
- `.ufo/waves/round-50/w1/ScrEntryR50/binds-shape-r50.txt`
- this report: `.ufo/waves/round-50/w1/ScrEntryR50.md`

Round-50 fetch pins and `.ufo/waves/round-50/receipts/binds-live-r50.txt` were not yet present during this seat's work. The quote check therefore used the round-49 fetch bytes (the task says the round-50 pins are expected byte-equal; `ExecFetchR50` is checking that) and the existing held round-46 pins/rows. Its PASS is provisional on that byte-equality check. The entry deliberately names round-50 paths and leaves the six host values as L1 placeholders. L1 still must integrate the candidate and fill those values from the round-50 live receipt.

No tracked files, registry, README, counter, or shared receipt paths were modified. No package/tool installation, host-service mutation, GUI launch, input injection, compositor dispatch, or home-state write was performed. The scratch clone and temporary raw host JSON were under the mandated scratch root and were removed before completion.
