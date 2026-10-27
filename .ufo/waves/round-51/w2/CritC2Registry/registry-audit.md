# C2 registry audit — S364–S369

Axes: **coverage + operability** (scoped to requested registry attack). Verdict is advisory; frozen claims remain unchanged.

## Frozen source-registry contract checks

At C2 data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`, `corpus/SOURCES.md:313–318` contains S364–S369. The registry header at line 11 has the eleven named columns `id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by`; separators account for 13 awk fields (`NF=13`). Independent row parse found all six target rows have 11 cells, no embedded/literal pipe in a cell, and unique IDs (global duplicate-ID list empty). The relevant metadata is consistently `kind=code`, `tier=A`, `status=mined`, `opened=2026-10-27`, `recheck=on-release`, and `used-by=corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` (which is intended to exist at the integrated revision, not necessarily in the pre-integration data commit).

Reproduction for frozen bytes and shape:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show a0e34387b30538372a1bb219eb3ccdc74013d458:corpus/SOURCES.md > /fast/scratch/hyaku/mado-r51/CritC2Registry/SOURCES.md
python3 -c 'from pathlib import Path; import re,collections; p=Path("/fast/scratch/hyaku/mado-r51/CritC2Registry/SOURCES.md"); ls=p.read_text().splitlines(); rs=[(i+1,l) for i,l in enumerate(ls) if re.match(r"^\\| S\\d{3,} \\|",l)]; ids=[re.match(r"\\| (S\\d+) \\|",l).group(1) for _,l in rs]; print("duplicate_ids",[(k,v) for k,v in collections.Counter(ids).items() if v>1]); print("S364-S369",[(n,l.split("|",2)[1].strip(),l.count("|")-1) for n,l in rs if int(re.match(r"\\| S(\\d+)",l).group(1)) in range(364,370)])'
```

**Contract-shape result: PASS.** `w1/ScrRowsDispatch/rows.md` §§1–3, especially lines 23–52 and quote-grep transcript lines 56–129, documents the row design, quoted pins, and pipe-free quotes. The current rows are structurally consistent with that source record.

## Frozen census at the revision

Replayed the lane census against a detached worktree checked out at the requested revision:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin worktree add --detach /fast/scratch/hyaku/mado-r51/CritC2Registry/tree a0e34387b30538372a1bb219eb3ccdc74013d458
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

Observed exit **0**, final `mado ok`, 23 warnings total: **22 W04 duplicate-URL-across-scopes** and **1 W01 tier-C mined-used-by**. No E01–E12 errors, including no E01 malformed rows, E03 duplicate IDs, or E04 duplicate URL+scope errors. Exact stdout is preserved in scratch `actual-census.txt` during the run; the target rows generate precisely three W04 lines:

- `S364`: URL `.../src/managers/KeybindManager.cpp`, shared with earlier scope S352. `w1/ScrRowsDispatch/rows.md:208–211` explicitly disclosed this warning.
- `S366`: URL `.../src/debug/HyprCtl.cpp`, shared with S018/S158/S307/S320. This adds one W04 beyond the two projected in the row draft; the draft's §5 line 211 says “exactly two new warnings,” while §5 lines 222–224 treats S366 as the minimum C2 evidence row. It does not disclose this third warning as a row effect. This is a **warning-count/provenance misstatement**, not a malformed-row or fatal census defect.
- `S368`: URL `.../src/config/legacy/ConfigManager.cpp`, shared with S162/S303/S317/S353. `rows.md:210–211` explicitly disclosed this warning.

The remaining 19 W04 entries predate S364–S369 (IDs S030, S042, S045, S097, S119–S121, S303, S307, S317–S318, S320–S321, S324, S326–S327, S332, S353–S354). W01 is S277, likewise unrelated to these new rows. They are warnings, not errors, and exit 0 is consistent with the census script contract (`scripts/sources-census.sh:24–33`).

## Judgment and smallest correction

**Rows S364–S369: PASS** for the specified contract checks (11 columns, required metadata fields, pipe-free cells, unique IDs); the frozen census itself also exits 0 without structural or duplicate-ID errors. **MISS** only for the W1 source-row report's claim that exactly two new W04 warnings were expected: the actual frozen census identifies three new warning rows, S364, S366, and S368. The census does not make these warnings “clean”; it emits them explicitly and classifies them as non-fatal W04. C2's SOURCES predicate does not require zero W04, so this discrepancy does not falsify the C2 frozen predicate by itself.

Smallest safe future correction: amend the explanatory row-count/accounting text in a later authorized record to name S366's already-existing HyprCtl URL collision and give the correct count of three new warnings. Do not alter the frozen claim or its counter. No row mutation is recommended by this audit.
