# ExecRerunC1 — w2 attack report (final)

Seat: ExecRerunC1 (leaf, Godspead). Lane: mado-shokunin (round 41, inline v1 wave w2).
Target attacked: **C1 data-tip claim** — `tools/mado-globals.py` at data commit
07f2641696b5ac73de1404ea737a9f27e9819aa1: `fixtures=39/39 TARGET_MET (base 0/39)`.

**Verdict: no defect found on the DATA. Predicate re-run confirms the claim on 5
independent runs (4 at REV incl. `--tool` control, 1 at BASE), exit codes as declared.
No fixture or clause is nonce-dependent; the only nonce-selected variation is which
comparison sites get mutated in clause b2 (all killed).**

## 1. Environment / preconditions
- python3 3.14.8, bwrap, prlimit, git 2.56.0 present. No tool installs needed (none performed).
- `git -C <lane> rev-parse --verify --quiet 07f264…^{commit}` → `07f2641696b5ac73de1404ea737a9f27e9819aa1`;
  `git cat-file -t 07f264…:tools/mado-globals.py` → `blob`.
- Precondition: `git show ab2bfa…:tools/mado-globals.py` → rc=128 (absent at base).
- Working tree vs 07f264: `git diff --stat 07f264… -- tools/mado-globals.py` → **empty** (the
  live run below exercised bytes identical to the committed tool; status shows only untracked w2 files).

## 2. sha256 — committed tool vs reference (DATA)
```
git show 07f264…:tools/mado-globals.py | sha256sum   → 286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e
sha256sum .ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt → 286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e
```
**Byte-identical** (sha256 equality).

## 3. Counter re-runs (all with absolute paths, `-I`)
Command (X = nonce):
`python3 -I <lane>/quality/counters/c1-r41-globals-v2.py --repo <lane> --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 --nonce X`

| run | nonce | exit | clause line | final line |
|---|---|---|---|---|
| n1 | 0a5707ca377abefd | 0 | a:1 b:1 b2:1 b3:1 g:1 | fixtures=39/39 tool=present verdict=TARGET_MET rev=07f264… nonce=0a5707ca377abefd |
| n2 | aa778b53b4e44a3d | 0 | same | fixtures=39/39 … verdict=TARGET_MET … nonce=aa778b53b4e44a3d |
| n3 | 10f9b53c4e391fff | 0 | same | fixtures=39/39 … verdict=TARGET_MET … nonce=10f9b53c4e391fff |
| tool | 5e9c2d1a8b4f7e30 (`--tool /tmp/committed-tool.py` = committed bytes) | 0 | same | fixtures=39/39 … verdict=TARGET_MET … nonce=5e9c2d1a8b4f7e30 |
| base | 0a5707ca377abefd (`--rev ab2bfa…`) | 1 | a:0 b:0 b2:0 b3:0 g:0 | fixtures=0/39 tool=absent verdict=TARGET_MISSED rev=ab2bfa… nonce=0a5707ca377abefd |

Base run confirms the "base 0/39" half of the claim.

## 4. Clause and fixture lines (identical in n1/n2/n3/tool runs, modulo b2 mutant sites)
Full retained output: `run-n1.out`, `run-n2.out`, `run-n3.out`, `run-tool.out`, `run-base.out` (seat dir).
Representative (run-n1, 51 lines):

```
PRED-C1-r41-v2 clause=b rc=0 selftest=63/63
PRED-C1-r41-v2 clause=b2 mutant=0 site=report:153 killed=1 forced
PRED-C1-r41-v2 clause=b2 mutant=1 site=read_live:218 killed=1
PRED-C1-r41-v2 clause=b2 mutant=2 site=report:142 killed=1
PRED-C1-r41-v2 clause=b2 mutant=3 site=parse:108 killed=1
PRED-C1-r41-v2 clause=b2 mutant=4 site=read_file:251 killed=1
PRED-C1-r41-v2 clause=b2 mutant=5 site=read_file:242 killed=1
PRED-C1-r41-v2 clause=b2 sites=18 killed=6/6 forced_dead=1
PRED-C1-r41-v2 clause=b3 variant=comment rc=0 selftest=63/63 ok=1
PRED-C1-r41-v2 clause=b3 variant=unparse rc=0 selftest=63/63 ok=1
PRED-C1-r41-v2 fixture=gen0 ok=1 ok
PRED-C1-r41-v2 fixture=gen1 ok=1 ok
PRED-C1-r41-v2 fixture=gen2 ok=1 ok
PRED-C1-r41-v2 fixture=gen3 ok=1 ok
PRED-C1-r41-v2 fixture=gen4 ok=1 ok
PRED-C1-r41-v2 fixture=gen5 ok=1 ok
PRED-C1-r41-v2 fixture=gen6 ok=1 ok
PRED-C1-r41-v2 fixture=gen7 ok=1 ok
PRED-C1-r41-v2 fixture=diff0 ok=1 ok
PRED-C1-r41-v2 fixture=diff1 ok=1 ok
PRED-C1-r41-v2 fixture=expect0 ok=1 ok
PRED-C1-r41-v2 fixture=expectmiss0 ok=1 ok
PRED-C1-r41-v2 fixture=nosess0 ok=1 ok
PRED-C1-r41-v2 fixture=nosess1 ok=1 ok
PRED-C1-r41-v2 fixture=unreadable0 ok=1 ok
PRED-C1-r41-v2 fixture=usage0 ok=1 ok
PRED-C1-r41-v2 fixture=badexpect0 ok=1 ok
PRED-C1-r41-v2 fixture=toolarge0 ok=1 ok
PRED-C1-r41-v2 fixture=live0 ok=1 ok
PRED-C1-r41-v2 fixture=live1 ok=1 ok
PRED-C1-r41-v2 fixture=livefail0 ok=1 ok
PRED-C1-r41-v2 fixture=liveenv0 ok=1 ok
PRED-C1-r41-v2 fixture=livewritable0 ok=1 ok
PRED-C1-r41-v2 fixture=livelarge0 ok=1 ok
PRED-C1-r41-v2 fixture=vernum0 ok=1 ok
PRED-C1-r41-v2 fixture=hostbyte0 ok=1 ok
PRED-C1-r41-v2 fixture=levelcase0 ok=1 ok
PRED-C1-r41-v2 fixture=expectlatest0 ok=1 ok
PRED-C1-r41-v2 fixture=sortclass0 ok=1 ok
PRED-C1-r41-v2 fixture=pidzeros0 ok=1 ok
PRED-C1-r41-v2 fixture=bootpersist0 ok=1 ok
PRED-C1-r41-v2 fixture=asciidigits0 ok=1 ok
PRED-C1-r41-v2 fixture=unicodename0 ok=1 ok
PRED-C1-r41-v2 fixture=fifo0 ok=1 ok
PRED-C1-r41-v2 fixture=dir0 ok=1 ok
PRED-C1-r41-v2 fixture=livehang0 ok=1 ok
PRED-C1-r41-v2 fixture=livenopath0 ok=1 ok
PRED-C1-r41-v2 fixture=unrec0 ok=1 ok
PRED-C1-r41-v2 fixture=mixed0 ok=1 ok
PRED-C1-r41-v2 clauses=a:1 b:1 b2:1 b3:1 g:1
PRED-C1-r41-v2: fixtures=39/39 tool=present verdict=TARGET_MET rev=07f2641696b5ac73de1404ea737a9f27e9819aa1 nonce=0a5707ca377abefd
```

## 5. Nonce-dependence analysis
Normalized diff (strip `nonce=` and `mutant=N site=`; files run-n1/n2/n3):
- **Only lines 2–7 (clause b2 mutant reports) differ**, and only in the *site* selected
  (report:153/152/142/135, read_live:218/222/226/228, parse:108/103, read_file:242/251,
  resolve_program:170, run:269/271) — expected, since b2's 6 sites are chosen by
  `sha256("mut:"+nonce)`.
- Every fixture line (gen0..gen7, diff0, diff1, expect0, expectmiss0, nosess0, nosess1,
  unreadable0, usage0, badexpect0, toolarge0, live0, live1, livefail0, liveenv0,
  livewritable0, livelarge0, vernum0, hostbyte0, levelcase0, expectlatest0, sortclass0,
  pidzeros0, bootpersist0, asciidigits0, unicodename0, fifo0, dir0, livehang0,
  livenopath0, unrec0, mixed0) is `ok=1` in all four REV runs — **no fixture flips**.
- clause=b (63/63), clause=b3 variants, clauses line, and final verdict identical everywhere.

## 6. Selftest in owned clone at data commit
```
D=$(mktemp -d) && git clone -q <lane> "$D/lane" && git -C "$D/lane" rev-parse --show-toplevel
# → /tmp/tmp.EF3QGBTWso/lane (== $D/lane)
git -C "$D/lane" checkout -q 07f264… ; git status --porcelain | wc -l → 0 (clean detached)
python3 -I "$D/lane/tools/mado-globals.py" --selftest
# → MADO_GLOBALS_SELFTEST: 63/63 passed ; SELFTEST_EXIT=0
rm -rf "$D"
```

## 7. Live run (`--live --diff`, once)
`python3 -I <lane>/tools/mado-globals.py --live --diff` (working-tree file == committed bytes per §1):
- exit **0**; `journalctl` resolved (/usr/bin/journalctl -rwxr-xr-x root, regular, not group/other-writable).
- Sessions: n=1 boot=- pid=1918 first/last 2026-10-25T13:16:45-03:00 interfaces=8 adverts=15;
  n=2 boot=7ab69ee4149c4811a3faf6c08c9d119b pid=1952 first/last 13:36:24 interfaces=63 adverts=63.
- Latest session includes `hyprland_focus_grab_manager_v1 ver=1 class=focus-grab` (C1's key
  capability), `wp_security_context_manager_v1` (sandbox), all class-table names present.
- `MADO_GLOBALS_DIFF: from=1 to=2 added=<63 globals> removed=- ver_changed=-`.
- Final: `MADO_GLOBALS: sessions=2 latest_pid=1952 interfaces=63 classes=capture:2,clipboard:3,focus-grab:1,idle:2,input-capture:3,input-synthesis:3,other:38,output-control:4,sandbox:1,session-lock:2,toplevel-control:4 expected_missing=- ignored=0 verdict=OK`.

## 8. Findings
1. **DATA (supports the claim; no defect)**: committed tool is byte-identical to the frozen v2
   reference (`ctl-ref-tool-v2.py.txt`, sha256 `286c051f…`), and the working tree has no diff
   vs 07f264 for it.
2. **PREDICATE behavior (supports the claim)**: 4 independent runs at 07f264 (3 fresh nonces +
   `--tool` control on committed bytes) all exit 0 with `fixtures=39/39` and
   `TARGET_MET`; base ab2bfa… exits 1 with `fixtures=0/39`, `tool=absent`, `TARGET_MISSED`.
3. **Nonce-dependence**: none for fixtures/clauses a,b,b3,g; b2 mutates different sites per
   nonce but always kills 6/6 with the forced site dead (18 sites total, ≥12 required).
4. **Selftest** on the committed bytes in a clean detached clone: `63/63 passed`, exit 0.
5. **Host receipt**: live run succeeds (exit 0, verdict=OK), focus-grab global present.

No defect found; nothing to fix before the round lands. No open predicate defect found.

## 9. Safety / scope notes
- Only read-only git used (show/rev-parse/cat-file/diff/status/clone/checkout -q in /tmp clone; no
  mutating git/jj anywhere).
- No pacman/package transactions; no host/compositor mutation; no Wayland-client or socket
  connections; only read-only `journalctl --user -u xdg-desktop-portal-hyprland` (via the tool's
  own `--live` path) was used. `hyprctl`/`wayland-info` not run.
- No tools installed (none needed).
- All counter runs were executed from the fleet root cwd with absolute lane paths; the counters
  wrote nothing into the lane (their scratch lives under /tmp and is removed by the counter).
- Full run outputs preserved: `run-n1.out`, `run-n2.out`, `run-n3.out`, `run-tool.out`, `run-base.out`.
