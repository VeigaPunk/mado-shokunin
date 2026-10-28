# R55RevC3 — report (round 55, wave w1, reviewer C3 attack)

Deliverable: `.ufo/waves/round-55/w1/R55RevC3/c3-attack.md` (full analysis). Receipts in the same directory:
`c3check.py`, `c3check.out`, `passpressed-all.txt`, `pass-callers.txt`, `efb-fetch-sha256.txt`, `lane-r55-files-at-freeze.txt`.
Scratch `/fast/scratch/hyaku/mado-r55/R55RevC3/` (tarball + extracted tree) removed before yield. No tracked files,
no git/jj mutations, no commits, no host reads or hyprctl calls, no hold-out path touched, no subagents.

## What I did

1. Read `claims-frozen.md`, `registration.md`, `frozen-tables.json` (c3 block), the round-52 pin and the base errata entry.
2. Verified the 13 Q rows with my own script (`c3check.py`) against `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`.
3. Fetched the pinned upstream files (`curl raw.githubusercontent.com/hyprwm/Hyprland/efb50993…/src/...`) for ConfigActions.cpp,
   ConfigActions.hpp, KeybindManager.cpp, KeybindManager.hpp, DispatcherTranslator.cpp, and the full tarball
   (`codeload.github.com/hyprwm/Hyprland/tar.gz/efb50993…`, sha256 5b05ce7b…, 50812454 bytes) into scratch.
4. Grepped the full tree for every `m_passPressed` write and every `pass(3-arg)` / `sendKeyState` call site.
5. Ran the lexical P23 leg on three junk propositions plus the actual P19 sentence.

## Commands and decisive output

```
$ python3 -I c3check.py        (in scratch; reads lane frozen-tables.json and the round-52 pin)
pin_sha256 a83abeb5…7637 frozen a83abeb5…7637 MATCH
pin_has_CR False pin_ends_nl True pin_bytes 71407
Q01 L1554 stripped_eq=True ... Q13 L1576 stripped_eq=True      (all 13 True)
Q_RESULT ALL_OK
LEG_P23 J1 token-salad: ok missing=none
LEG_P23 J2 false-claim-with-tokens: ok missing=none
LEG_P23 J3 unrelated: bad missing=['m_passPressed','== 1','== 0','PRESSED','RELEASED','otherwise|any other|else']
exit=0

$ sha256sum efb ConfigActions.cpp  -> a83abeb5…7637   (identical to round-52 pin)
$ grep -rn m_passPressed (efb tree) -> 18 lines; writers: ConfigActions.hpp:114 (=-1), KeybindManager.cpp:804 (=sc<int>(pressed)),
  :814 (=-1), ConfigActions.cpp:1606/1608/1615 (sendKeyState), DispatcherTranslator.cpp:615/617/624 (sendkeystate)
$ P19 actual sentence (base errata line 17) -> bad (missing == 0, RELEASED, alternative)
$ P19 + " RELEASED == 0 else" -> ok   (padding passes the lexical leg while the sentence stays false)
```

Pinned function: `Actions::pass(uint32_t modMask, uint32_t key, …)` at ConfigActions.cpp:1530. Else arm (1566–1574) sends
keyboard PRESSED then RELEASED (1568–1569) and pointer PRESSED then RELEASED (1571–1572). P19's "PRESSED only when
m_passPressed == 1" is false. The only value reaching the else arm in the full tree is -1 (see c3-attack.md §3–§4).

## Findings (severity order)

1. **P19 falsity confirmed for the else arm.** Lines 1566–1569 send PRESSED and then RELEASED, not PRESSED only. The
   correction must say press-then-release for any value other than 0 or 1. (Expected; confirms routed defect 1.)
2. **Lexical `p23` leg admits a false proposition.** J2 ("the else arm sends nothing … any other value is dead code") passes
   all tokens. Padding the real P19 sentence with `RELEASED == 0 else` turns it `ok`. The leg is presence-only; the
   `p23=ok` line is not evidence of correctness. Declared limit exists; the w2 sentence audit must carry the truth test.
   Severity: contract weakness, not a wrong frozen value.
3. **Source-scope limit for any `m_passPressed` sentence.** The S371 row covers lines 1530–1616 only. The value set
   {-1,0,1} and the caller paths (hyprctl dispatch, KeybindManager long-press lines 131/154, Lua `dsp_sendShortcut`) are
   tarball-derived and need registry rows. Without them the P23 may not say "reached by" or "only -1/0/1".
   The round-52 pins for KeybindManager.cpp, DispatcherTranslator.cpp and ConfigActions.hpp are byte-identical to the
   tarball, so those writers are pin-backed; HyprCtl.cpp and the Lua file are not in any pin.
4. **Ambiguity in C3-CTL-1 expectations.** It names `rows`+`p23` as missed but omits `readme`, which also misses at base
   (corpus/README.md:81 names the errata file without P23). It also names `rows` where the leg grammar is `rows:<id>`.
   The harness contract must say subset or exact set.
5. **Not runnable at freeze.** `quality/counters/c3-r55-p19.py` and `quality/check-r55-controls.py` are absent at
   `54dacbd` (only the three round-55 contract files are present under `round-55/`). The C3 predicate and control
   harness did not run; the P19 line and `controls=6/6` are unverified by me.

## Bound on what P23 may say about `S.m_passPressed` (summary; full list in c3-attack.md §6)

MAY: the 1530 function sends modifier state, branches on `m_passPressed`; `== 1` → PRESSED only; `== 0` → RELEASED only;
any other value → keyboard PRESSED then RELEASED for `key - 8` (pointer PRESSED then RELEASED for mouse).
MUST NOT: "only when == 1"; "PRESSED alone" in the else arm; that -1/0/1 is the protocol-wide set; that a physical key or
keybind reaches the else arm (keybind window 804–814 sets 0/1); any caller path not backed by a registry row; anything
about client delivery, focus or compositor behaviour; anything about `pass(std::optional<PHLWINDOW>)` at 1465–1505, which
has its own else arm.

## Could not verify

- Runtime reachability of the else arm (hyprctl dispatch, long-press, Lua outside keybind window): source-derived only; nothing
  was run or dispatched.
- C3 counter and controls (absent at freeze; not run).
- The sentence-to-pin entailment of any proposition beyond the lexical leg (the w2 audit's job).
- HyprCtl.cpp, LuaBindingsDispatchers.cpp and KeybindManager lines 120–160 were read from the tarball, not a committed pin.

## Installs

None. Tools used: curl, tar, sha256sum, python3 -I, grep. No pacman, no uv, no npm.
