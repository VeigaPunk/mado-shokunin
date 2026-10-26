# ExecRerunC1 — w2 findings (trailer)

Seat: **ExecRerunC1** (leaf). Target: **C1 data-tip claim** — `tools/mado-globals.py`
at 07f2641696b5ac73de1404ea737a9f27e9819aa1, `fixtures=39/39 TARGET_MET (base 0/39)`.
Verdict: **no defect found on the DATA**; re-run confirms the claim.

## Attacks and evidence
1. **Committed bytes vs frozen reference (DATA)**: `git show 07f264…:tools/mado-globals.py`
   sha256 = `286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e` =
   sha256(`.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt`) → **byte-identical**. Working tree
   has no diff vs 07f264 for the tool.
2. **Re-run, 3 fresh nonces** (`python3 -I <lane>/quality/counters/c1-r41-globals-v2.py --repo <lane> --rev 07f264… --nonce N`):
   - N=0a5707ca377abefd → exit 0, `a:1 b:1 b2:1 b3:1 g:1`, `fixtures=39/39 tool=present verdict=TARGET_MET`
   - N=aa778b53b4e44a3d → exit 0, same clauses, same 39/39 TARGET_MET
   - N=10f9b53c4e391fff → exit 0, same clauses, same 39/39 TARGET_MET
3. **`--tool` control on committed bytes** (N=5e9c2d1a8b4f7e30): exit 0, same 39/39 TARGET_MET.
4. **Base claim**: `--rev ab2bfa…` → exit 1, `a:0 b:0 b2:0 b3:0 g:0`, `fixtures=0/39 tool=absent verdict=TARGET_MISSED` → "base 0/39" holds.
5. **Nonce-dependence**: normalized diff of n1/n2/n3 differs ONLY in clause-b2 mutant-site lines
   (nonce-selected sites; always `sites=18 killed=6/6 forced_dead=1`). All 39 fixture lines are
   `ok=1` and identical across all four REV runs → **no fixture/clause flips**.
6. **Selftest in owned clone**: `D=$(mktemp -d); git clone -q <lane> "$D/lane"` (toplevel verified
   = `$D/lane`), `git checkout -q 07f264…` detached, clean; `python3 -I "$D/lane/tools/mado-globals.py" --selftest`
   → `MADO_GLOBALS_SELFTEST: 63/63 passed`, exit 0. `rm -rf "$D"`.
7. **Live receipt**: `python3 -I <lane>/tools/mado-globals.py --live --diff` → exit 0, verdict=OK,
   sessions=2 (latest pid=1952, interfaces=63, `hyprland_focus_grab_manager_v1` class=focus-grab
   present), DIFF from=1 to=2.

## Clauses/fixtures (all four REV runs)
clause=b rc=0 selftest=63/63 · clause=b2 sites=18 killed=6/6 forced_dead=1 ·
clause=b3 comment rc=0 63/63 ok=1, unparse rc=0 63/63 ok=1 ·
fixtures: gen0..gen7, diff0, diff1, expect0, expectmiss0, nosess0, nosess1, unreadable0,
usage0, badexpect0, toolarge0, live0, live1, livefail0, liveenv0, livewritable0, livelarge0,
vernum0, hostbyte0, levelcase0, expectlatest0, sortclass0, pidzeros0, bootpersist0,
asciidigits0, unicodename0, fifo0, dir0, livehang0, livenopath0, unrec0, mixed0 — **ok=1 for all 39**.
Full outputs: `.ufo/waves/round-41/w2/ExecRerunC1/run-n{1,2,3}.out`, `run-tool.out`, `run-base.out`;
full report: `.ufo/waves/round-41/w2/ExecRerunC1/report.md`.

No tool installs; no mutating git/jj; no pacman/host changes; read-only journal verb only.
