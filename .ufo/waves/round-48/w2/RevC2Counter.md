# RevC2Counter — C2 counter falsification (round 48, wave w2)

STATUS: complete. The frozen C2 counter (`quality/counters/c2-r48-xkb-entry.py`, `PRED-C2-r48`, sha256
`4a0e6924eada0d12c70b4ce6e681a118896b93532e280ea3c15cc148b794a9f1`, 42,256 B, byte-equal to the l1-draft
copy) was run on the lane's intended C2 data candidate and on 95 mutants/probes built from it, inside a
scratch replay tree at base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`. The candidate is admitted by all nine
clauses. Every required attack surface (S340-S350 pin, digest, source ID, recheck, quote/range, entry step
locator, receipt positive digest, negative rc, README row, held row, absent-ground term) is exercised; every
family produces misses in its declared clause except the two enforcement gaps and the cosmetic case itemised
under **Findings**, where each admitted mutant is recorded as a potential false admission. The predicate,
target, base, fixtures and claims were not changed or narrowed.

## Verdict on the intended data candidate

```
PRED-C2-r48 xkb-keymap-compile-r48.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1
PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=180636090330fe4c74ae856766bba47e5ec77101
```

- rev `180636090330fe4c74ae856766bba47e5ec77101` (commit whose parent is `579f694b`), base `579f694b`; entry,
  11 rows S340-S350, README row, 14 round-48 fetch pins, the receipt and its generator overlaid from
  `.ufo/waves/round-48/l1-draft/` and `.ufo/waves/round-48/{fetch,receipts,tools}/`.
- clause f: receipt `xkbcli-compile-keymap-r48.txt`, version 1.13.2, sha prefix `efd487a39920`, three probes.
- clause r: live replay `replay=ok sha=efd487a39920 neg=(1,1,0) ver=1.13.2` on this host (libxkbcommon
  1.13.2-1, xkeyboard-config 2.48-1, xkbcli 1.13.2).
- clause i at the candidate: `all_absent_at_base=1 present_at_rev=3/4`.

Two further runs fix the ends: scoring the base revision itself is `clause=a entry_absent` (`admitted=0/1`,
rc 1), and scoring the candidate with `--base` pointing at itself is `SETUP precondition_failed
entry_present_at_base` (rc 2).

## Method and bounds

- Scratch `/fast/scratch/hyaku/mado-r48/RevC2Counter/`: a `git clone --bare --shared` of the lane; the
  candidate tree is the base tree plus overlay, built with `git hash-object` / `git mktree` /
  `git commit-tree`. No index and no working tree (the lane index exceeds the seat's 1 MiB/file guard), so no
  checked-out clone is ever written. `git -C <clone> rev-parse --absolute-git-dir` and
  `--is-bare-repository` were asserted equal to the clone path / `true` before the first commit.
- `corpus/SOURCES.md` and `corpus/README.md` are read with `git show 579f694b:<path>`. The lane working tree
  carried uncommitted C2 integration at scoring time (`M corpus/SOURCES.md`, `M corpus/README.md`,
  `?? corpus/knowledge/xkb-keymap-compile-r48.md`); the mirror deliberately uses the committed base bytes, as
  the freeze requires. All other overlay bytes are the l1-draft files (digests in
  `RevC2Counter/provenance.txt`).
- Each mutation is one commit whose parent is the candidate commit; the counter is invoked as
  `python3 -I quality/counters/c2-r48-xkb-entry.py --repo <bare clone> --rev <variant>` with `TMPDIR` inside
  the seat scratch (the counter removes its own replay sandbox). Nothing in the lane was written except this
  report and `w2/RevC2Counter/`.
- Every writer shell ran `ulimit -f 2048`; the largest file produced is `summary.json` at 144,733 B; total
  evidence is 604 KiB (well under 2 GB). No package transaction, no compositor/service change, no input
  injection, no terminal launch; beyond `git`/`python3` the only host binary executed is read-only `xkbcli`
  through the counter's clause r. No install was needed or performed.
- Mutation commit identity lives only inside the scratch bare clone (`user.name=t`, `user.email=t@t`, local
  config); the clone is removed after the evidence copy.

## Attack matrix

98 result rows: the candidate, 95 mutants/probes, the base-revision run and the setup check.
"clauses flipped" is relative to the candidate's all-ones vector; a letter named there was observed as
`<letter>:0` in that run. Full per-run clause vectors and revision ids are in `RevC2Counter/matrix.tsv`;
every run's complete output is in `RevC2Counter/logs/<variant>.log`.


### Intended candidate

1 variant(s); admitted: `pos`

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `pos` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=180636090330fe4c74ae856766bba47e5ec77101 |


### Clause a - new ground / precondition

2 variant(s); admitted: none

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `a-rev-base-direct` | miss | - | PRED-C2-r48 xkb-keymap-compile-r48.md clause=a entry_absent |
| `a-entry-at-base` | SETUP | - | PRED-C2-r48 SETUP precondition_failed entry_present_at_base corpus/knowledge/xkb-keymap-compile-r48.md |


### Clause b - provenance head and registry rows

19 variant(s); admitted: none

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `b-recheck-S340` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S340 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S341` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S341 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S342` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S342 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S343` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S343 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S344` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S344 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S345` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S345 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S346` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S346 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S347` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S347 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S348` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S348 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S349` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S349 tier=A kind=code status=mined opened=2026-10-26 used=1 recheck=later |
| `b-recheck-S350` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S350 tier=A kind=own-work status=mined opened=2026-10-26 used=1 recheck=later |
| `b-opened-S340` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S340 tier=A kind=code status=mined opened=2026-10-25 used=1 recheck=on-release |
| `b-tier-S340` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S340 tier=D kind=code status=mined opened=2026-10-26 used=1 recheck=on-release |
| `b-status-S340` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S340 tier=A kind=code status=draft opened=2026-10-26 used=1 recheck=on-release |
| `b-usedby-S340` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S340 tier=A kind=code status=mined opened=2026-10-26 used=0 recheck=on-release |
| `b-ghost-head` | miss | b,c,d,e,g | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S351 rows=0 |
| `b-rowid-missing` | miss | b,c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b id=S340 rows=0 |
| `b-verified-at` | miss | b | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b ids=11 outside_head=0 verified=2026-10-25 recheck=on-release ok=0 |
| `b-head-short` | miss | b,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=b ids=2 outside_head=0 verified=2026-10-26 recheck=on-release ok=0 |


### Clause c - pin binding, URL refs, anchors

30 variant(s); admitted: `c-pin-mode-S340`

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `c-pinbytes-S340` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 pin_sha_mismatch=xkbcommon-rules.c |
| `c-pinbytes-S341` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S341 pin_sha_mismatch=xkbcommon-xkbcomp.c |
| `c-pinbytes-S342` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S342 pin_sha_mismatch=xkbcommon-include.c |
| `c-pinbytes-S343` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S343 pin_sha_mismatch=xkbcommon-context.c |
| `c-pinbytes-S344` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S344 pin_sha_mismatch=xkbcommon-context-priv.c |
| `c-pinbytes-S345` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S345 pin_sha_mismatch=xkbcommon-meson_options.txt |
| `c-pinbytes-S346` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S346 pin_sha_mismatch=xkeyboard-config-rules-evdev |
| `c-pinbytes-S347` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S347 pin_sha_mismatch=xkeyboard-config-symbols-br |
| `c-pinbytes-S348` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S348 pin_sha_mismatch=xkbcommon-tools-compile-keymap.c |
| `c-pinbytes-S349` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S349 pin_sha_mismatch=xkbcommon-messages-codes.h |
| `c-pinbytes-S350` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S350 pin_sha_mismatch=xkbcli-compile-keymap-r48.txt |
| `c-digest-S340` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 pin_sha_mismatch=xkbcommon-rules.c |
| `c-digest-S341` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S341 pin_sha_mismatch=xkbcommon-xkbcomp.c |
| `c-digest-S342` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S342 pin_sha_mismatch=xkbcommon-include.c |
| `c-digest-S343` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S343 pin_sha_mismatch=xkbcommon-context.c |
| `c-digest-S344` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S344 pin_sha_mismatch=xkbcommon-context-priv.c |
| `c-digest-S345` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S345 pin_sha_mismatch=xkbcommon-meson_options.txt |
| `c-digest-S346` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S346 pin_sha_mismatch=xkeyboard-config-rules-evdev |
| `c-digest-S347` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S347 pin_sha_mismatch=xkeyboard-config-symbols-br |
| `c-digest-S348` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S348 pin_sha_mismatch=xkbcommon-tools-compile-keymap.c |
| `c-digest-S349` | miss | c,d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S349 pin_sha_mismatch=xkbcommon-messages-codes.h |
| `c-digest-S350` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S350 pin_sha_mismatch=xkbcli-compile-keymap-r48.txt |
| `c-url-branch-S340` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 url_branch_ref:https://raw.githubusercontent.com/xkbcommon/libxkbcommon/main/src/xkbcomp/rules. |
| `c-url-noref-S340` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 url_ref_not_pinned:https://raw.githubusercontent.com/xkbcommon/libxkbcommon/src/xkbcomp/rules.c |
| `c-url-unrelated-S347` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S347 pin_name_unrelated=bound:xkeyboard-config-symbols-br:symbols/de |
| `c-pin-missing-S340` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 pin_missing=xkbcommon-rules.c |
| `c-anchor-range-S340` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 range_out_of_pin=xkbcommon-rules.c:1259-9999/2126 |
| `c-anchor-otherpin-S340` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 range_other_pin=xkbcommon-context.c |
| `c-ownwork-kind-S350` | miss | c | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S350 no_url |
| `c-pin-mode-S340` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=9ba2d482ed18d9a8074540c123de06f3c9f25e36 |


### Clause d - quotes and ranges

6 variant(s); admitted: none

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `d-quote-word` | miss | d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=d quote_not_in_pin line=35 pin=xkbcommon-context-priv.c q='Options can be empty, so respect this if passe |
| `d-quote-range-out` | miss | d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=d locator_out_of_pin=xkbcommon-context-priv.c:9999-9999/226 line=35 |
| `d-quote-range-shift` | miss | d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=d quote_out_of_range line=35 pin=xkbcommon-context-priv.c q='Options can be empty, so respect that if pas |
| `d-quote-lane-locator` | miss | d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=d quote_locator_unresolved=corpus/knowledge/hyprland-input-devices-r46.md:69 line=19 |
| `d-quote-long` | miss | d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=d quote_too_long words=30 line=48 |
| `d-uncited-pin` | miss | d | PRED-C2-r48 xkb-keymap-compile-r48.md clause=d pin_not_cited_by_row=xkbcommon-meson.build line=36 |


### Clause e - numbered steps and locators

4 variant(s); admitted: none

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `e-step-unloc` | miss | e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=e step_without_pin_range line=36 uncited=[] |
| `e-step-outofrange` | miss | d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=e step_without_pin_range line=43 uncited=[] |
| `e-steps5` | miss | e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=e steps=5 <6 |
| `e-step-uncited` | miss | d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=e step_without_pin_range line=37 uncited=['xkbcommon-meson.build', 'xkbcommon-meson.build', 'xkbcommon-me |


### Clause f - the committed host receipt

8 variant(s); admitted: none

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `f-digest-receipt-only` | miss | f,r | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f entry_disagrees=.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt ver=1 pos=1 sha=0 neg=[True, |
| `f-negrc-layout-receipt` | miss | f | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f receipt_probe_bad=unknown layout(rc_values=[0]) |
| `f-negrc-variant-receipt` | miss | f | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f receipt_probe_bad=unknown variant(rc_values=[0]) |
| `f-negrc-option-receipt` | miss | f | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f receipt_probe_bad=unknown option(rc_values=[1]) |
| `f-receipt-absent` | miss | f,r | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f receipt_missing=.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt |
| `f-receipt-mode` | miss | f | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f receipt_missing=.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt |
| `f-receipt-short` | miss | f,r | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f receipt_short=.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt:14 |
| `f-entry-version` | miss | f | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f entry_disagrees=.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt ver=0 pos=1 sha=1 neg=[True, |


### Clause g - README index row

7 variant(s); admitted: `g-cells`

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `g-row-absent` | miss | g | PRED-C2-r48 xkb-keymap-compile-r48.md clause=g readme_rows=0 |
| `g-row-duplicate` | miss | g | PRED-C2-r48 xkb-keymap-compile-r48.md clause=g readme_rows=2 |
| `g-redirect` | miss | g | PRED-C2-r48 xkb-keymap-compile-r48.md clause=g readme_redirect_word |
| `g-other-knowledge` | miss | g | PRED-C2-r48 xkb-keymap-compile-r48.md clause=g readme_names_other=['knowledge/hyprland-input-devices-r46.md'] |
| `g-missing-id` | miss | g | PRED-C2-r48 xkb-keymap-compile-r48.md clause=g readme_missing_ids=['S350'] |
| `g-cells` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=dc704636994a6b263a1a9d64ae091ec639c11cd4 |
| `g-fenced` | miss | g | PRED-C2-r48 xkb-keymap-compile-r48.md clause=g readme_rows=0 |


### Clause h - held ground

5 variant(s); admitted: none

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `h-held-row` | miss | h | PRED-C2-r48 xkb-keymap-compile-r48.md clause=h held_row_moved=S318 |
| `h-held-row-delete` | miss | b,h | PRED-C2-r48 xkb-keymap-compile-r48.md clause=h held_row_moved=S318 |
| `h-held-pin-ik` | miss | d,h | PRED-C2-r48 xkb-keymap-compile-r48.md clause=h held_pin_sha_mismatch=Hyprland-IKeyboard.cpp |
| `h-held-pin-cv` | miss | h | PRED-C2-r48 xkb-keymap-compile-r48.md clause=h held_pin_sha_mismatch=Hyprland-ConfigValues.cpp |
| `h-held-entry` | miss | h | PRED-C2-r48 xkb-keymap-compile-r48.md clause=h held_entry_moved=corpus/knowledge/hyprland-input-devices-r46.md |


### Clause i - ground-absent census

3 variant(s); admitted: `i-ground-two-terms`

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `i-ground-two-terms` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=69aa414b7acaf5ad4220531a08c60d8b1b558883 |
| `i-ground-rev-census` | miss | i | PRED-C2-r48 xkb-keymap-compile-r48.md clause=i ground_vacuous=1/4 |
| `i-ground-all-terms` | miss | d,f,r | PRED-C2-r48 xkb-keymap-compile-r48.md clause=d quote_locator_unresolved=xkbcommon-tools-compilekeymap.c:587 line=63 |


### Alternate-pin probes

4 variant(s); admitted: `p-alt-same-basename`, `p-tamper-selfconsistent`, `p-selfpin-ownwork`

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `p-alt-same-basename` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=0b022739d13339e585c2d4ce9818a60ed891dff8 |
| `p-tamper-selfconsistent` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=0149cd613453c20678b8d380995ecf1e1a44263f |
| `p-alt-ambiguous-stem` | miss | c,d,e | PRED-C2-r48 xkb-keymap-compile-r48.md clause=c id=S340 anchor_no_range |
| `p-selfpin-ownwork` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=ae65b51b6d37f40fe382c7dbad6bea4322fe01b3 |


### Receipt replay / relabel probes

3 variant(s); admitted: `r-untrusted-receipt-body`

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `r-untrusted-receipt-body` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=ac99b1c3586c9821b2e320e80575224217abf5dd |
| `r-relabel-digest-both` | miss | r | PRED-C2-r48 xkb-keymap-compile-r48.md clause=r positive_replay_failed rc=0 sha=efd487a39920 |
| `r-alt-run-receipt` | miss | f | PRED-C2-r48 xkb-keymap-compile-r48.md clause=f receipt_no_keymap_sha=.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt |


### Permitted / boundary probes

6 variant(s); admitted: `x-url-commit-admitted-S340`, `x-digest-label-admitted-S340`, `x-quote-600-invisible`, `x-e-boundary-admitted`, `x-digest-extra-admitted`, `x-recheck-future-admitted`

| variant | verdict | clauses flipped vs candidate | counter evidence |
|---|---|---|---|
| `x-url-commit-admitted-S340` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=737d69d2665777d348da0500a493884eed3b32b1 |
| `x-digest-label-admitted-S340` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=bdf661b4847f1d5fbbfba99daa01d0dca908b72c |
| `x-quote-600-invisible` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=50a1db1ca9ae8a80d1573c80751285d9066b5062 |
| `x-e-boundary-admitted` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=1750420ec64c34df858d17d71fb875f91298df6a |
| `x-digest-extra-admitted` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=15bf1884862a3c09c6623a73b571a0317f45f21f |
| `x-recheck-future-admitted` | ADMIT | - | PRED-C2-r48: admitted=1/1 verdict=TARGET_MET rev=73cda5bc432fd48ae08892b2abfdca7fc26d0db4 |


## Findings: potential false admission

These trees are **admitted** by the frozen counter. Each is classified as (i) a declared residual, (ii) an
enforcement gap between the frozen registration text and the counter, or (iii) cosmetic. The intended
candidate itself conforms to the registration on every point below; these are mutant-side holes.

1. **Gap — pin mode is not enforced (registration clause c says "mode 100644").** `c-pin-mode-S340` scores
   `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 r:1 admitted=1` with
   `.ufo/waves/round-48/fetch/xkbcommon-rules.c` at mode `100755` (rev
   `9ba2d482ed18d9a8074540c123de06f3c9f25e36`). `clause_c` only resolves `pins.get(name)` bytes and never
   calls `ls_mode`; clause f *does* check the receipt's mode, so the asymmetry is real, not a harness
   artifact. This is the one required attack whose declared clause did not miss.
2. **Gap — a quote span over 600 characters is invisible to clause d.** `x-quote-600-invisible` replaces the
   cited span `expanded_value->matched = true;` with 26 repetitions (624 characters, 27 words) at the same
   locator `xkbcommon-rules.c:1297`; the counter reports `clause=d quotes=17` (one fewer than the candidate's
   18) and admits (rev `50a1db1ca9ae8a80d1573c80751285d9066b5062`). The 25-word cap never applies because
   `QUOTE_RE` caps the span at 600 characters, so an over-long quote is silently dropped rather than refused.
   A 30-word span of short words (`d-quote-long`) *is* caught (`quote_too_long`); the hole is specifically the
   >600-character shape.
3. **Residual (declared) — a tampered pin with a matching row digest is admitted.**
   `p-tamper-selfconsistent` appends `/* round-48 local note */` to `fetch/xkbcommon-rules.c` and rewrites
   S340's `sha256:` to the new digest; all nine clauses stay green (rev
   `0149cd613453c20678b8d380995ecf1e1a44263f`). This is the declared trust-root residual ("the committed copy
   and the row's digest are bound to each other; neither is independently re-hashed here"), and the mutated
   bytes still carry every cited quote at its line.
4. **Residual (declared) — a self-authored "pin" can be quoted as ground.** `p-selfpin-ownwork` commits
   `fetch/self-note.md` (a local note plus the entry's own first 2,000 bytes), adds its digest and receipt path
   to the own-work row S350, and quotes `mado round 48 note` at `self-note.md:2`; admitted,
   `clause=d quotes=19` (rev `ae65b51b6d37f40fe382c7dbad6bea4322fe01b3`). Clause d's lane-document refusal
   applies to locators, not to bytes a row binds as a fetch pin.
5. **Residual (declared) — an untrusted/relabelled receipt body is admitted.** `r-untrusted-receipt-body`
   rewrites the capture date, changes `symbols/zz` to `symbols/qq` and the include-path census (`3 include
   paths` -> `1 include path`) while leaving the version, `host.keymap` digest and every rc label intact;
   admitted (rev `ac99b1c3586c9821b2e320e80575224217abf5dd`). The bound is narrow: the positive digest
   relabelled in receipt *and* entry is caught by r (`r-relabel-digest-both`, `positive_replay_failed`), a
   receipt built from a different run is caught by f (`r-alt-run-receipt`, `receipt_no_keymap_sha`), and any
   changed rc label is caught by f (three `f-negrc-*` probes). f/r bind version, digest and rc labels, not
   receipt prose — matching the declared "clause f reads the receipt's own labels" residual, but worth naming
   in the freeze notes because the receipt is the round's provenance artifact.
6. **Residual (declared) — a fabricated 40-hex commit ref is accepted.** `x-url-commit-admitted-S340`
   replaces S340's URL ref `xkbcommon-1.13.2` with forty `d`s; admitted (rev
   `737d69d2665777d348da0500a493884eed3b32b1`). The registration already declares that a commit hash is
   accepted without proving repository membership.
7. **Cosmetic — a README row without its closing pipe is admitted.** `g-cells` removes the trailing `|`;
   `clause_g` still parses three cells and admits (rev `dc704636994a6b263a1a9d64ae091ec639c11cd4`). The
   intended row has the closing pipe, so the candidate is unaffected.
8. **Note — `recheck: 2999-12-31` is accepted** (`x-recheck-future-admitted`, rev
   `73cda5bc432fd48ae08892b2abfdca7fc26d0db4`); `recheck_ok` validates ISO form only. The candidate's
   `on-release` is within the stated contract; this bounds what "valid recheck" means.
9. **Note — clause i's presence half is corpus-wide, not entry-bound.** `i-ground-two-terms` strips
   `xkeyboard-config-2.48` and `XKB-595` from the entry only and is admitted (rev
   `69aa414b7acaf5ad4220531a08c60d8b1b558883`) because the README index row and the S340/S349/S350 notes still
   carry them. The isolated i miss (`i-ground-rev-census`, `clause=i ground_vacuous=1/4 ... all_absent_at_base=0
   present_at_rev=1/4`, rev `b0b3027ecb8ad60c06ab55b918ecf08b45a4c0e7`) required rewriting the S346/S347 URL
   refs from the `xkeyboard-config-2.48` tag to a 40-hex commit plus five row notes and the README prose; with
   only the entry mutated, i cannot fail. Practical reading: for a tree that already satisfies c and f, i is
   (near-)entailed, so i's discriminating content is its base-absence half.

## Cascades (deliberate and observed)

- Pin byte/digest mutations flip c **and** the d/e citations that lean on the now-unbound pin
  (`pin_not_cited_by_row`, `step_without_pin_range`); S350's receipt pin flips c alone (nothing quotes it).
- `b-ghost-head` / `b-rowid-missing` / `b-head-short` also flip c/d/e (cited ids lose their rows);
  `h-held-row-delete` also flips b (`ghost_ids=['S318']`); `h-held-pin-ik` also flips d (the tampered
  `Hyprland-IKeyboard.cpp` still holds the quoted line, but the held citation is no longer trusted).
- `e-step-outofrange` (a single-locator step taken out of range) flips d and e; `e-step-uncited` flips d and e;
  `e-step-unloc` and `e-steps5` flip e alone.
- `f-digest-receipt-only`, `f-receipt-absent` and `f-receipt-short` flip f and r (r cannot replay what is
  missing or wrong); the three `f-negrc-*`, `f-entry-version` and `f-receipt-mode` flip f alone.
- `i-ground-all-terms` (also removing `compile-keymap` from the entry) flips d, f and r — it deletes the
  receipt citation and pin locators, not just the census term; it is a diagnostic, not an i control.

## Expected acceptances (control sanity)

`x-digest-extra-admitted` (an unrelated extra digest appended; c only requires the pin's digest to be among
the row's digests), `x-e-boundary-admitted` (a step locator at exactly the pin's last line,
`xkeyboard-config-rules-evdev:747`) and `p-alt-same-basename` (an extra same-basename copy under `fetch/alt/`;
exact-name resolution still selects the cited pin) all admit, as designed. The ambiguous-stem probe
`p-alt-ambiguous-stem` (real pin moved to `fetch/libxkbcommon/rules.c`, decoy at `fetch/alt/rules.c`) misses on
c (`anchor_no_range`), d and e, so duplicate stems are not a laundering path.

## Required-surface coverage

| surface | variants | declared miss | observed |
|---|---|---|---|
| S340-S350 pin bytes (one per row) | 11 `c-pinbytes-*` | 11 | `pin_sha_mismatch` (c), cascade d/e |
| S340-S350 recorded digest (one per row) | 11 `c-digest-*` | 11 | `pin_sha_mismatch` (c), cascade d/e |
| source ID (head ghost, row id missing, head < 3 sources) | 3 | 3 | `ghost_ids`, `rows=0`, `ids=2` (b) |
| recheck (one per row) | 11 `b-recheck-*` | 11 | b:0 |
| opened / verified-at / tier / status / used-by | 5 | 5 | b:0 |
| quote word, range out, shifted range, lane locator, >25 words | 5 | 5 | d:0 |
| entry step locator (unlocated, out-of-range single-locator, step count, uncited) | 4 | 4 | e:0 |
| receipt positive digest (receipt only; receipt+entry) | 2 | 2 | f:0 / r:0 |
| receipt negative rc (layout, variant, option) | 3 | 3 | f:0 (`rc_values=[0]` / `rc_values=[1]`) |
| README row (absent, duplicate, redirect, other knowledge, missing id, fenced) | 6 | 6 | g:0 |
| held ground (row bytes, row delete, both held pins, r46 entry) | 5 | 5 | h:0 |
| absent-ground term | 3 | 1 isolated (`i-ground-rev-census`) | i:0; see finding 9 |
| untrusted/relabelled receipt | 3 | 2 | r:0, f:0; body relabel admitted (finding 5) |
| alternate pin, same filename | 4 | 2 | as in findings 1-4 and the ambiguous-stem probe |

## Evidence retained

Under `.ufo/waves/round-48/w2/RevC2Counter/`:

- `matrix.tsv` — every variant: declared clause, rc, clause vector, flipped clauses, first counter line, revision id.
- `summary.json` — the same rows verbatim from the harness, with up to ten counter lines captured per run.
- `logs/<variant>.log` — the complete counter output for each of the 98 rows (candidate, mutants/probes, base run, setup check).
- `provenance.txt` — lane/base revisions, counter sha256/bytes and byte-equality with the l1-draft copy, overlay file digests, all 14 fetch-pin digests, tool versions, the mirror/scoring commands, `ulimit` and size accounting.
- `harness.py` — the mutation harness (mirror construction, variants, evidence capture); not lane code.

## Host safety, budgets, tooling

No lane Git/jj mutation, no commit or push, no registry/counter/entry/report edit, no sibling-lane or
fleet-repo write. No package transaction (nothing installed; `git` 2.56.0, Python 3.14.8, `xkbcli` 1.13.2
already present). No compositor, service or host-config mutation, no input injection, no GUI/terminal launch.
Scratch removed after the evidence copy; the lane writes are this report and `w2/RevC2Counter/` only.

## Blockers

None. The counter is runnable on this host (clause r live replay passes), the candidate admits, and every
declared mutation family was exercised. The enforcement gaps and the declared-residual admissions are recorded
for the L1's pre-data freeze decision; this seat did not narrow or repair the predicate.
