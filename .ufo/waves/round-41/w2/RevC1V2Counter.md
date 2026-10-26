# Seat RevC1V2Counter — Attack on `PRED-C1-r41-v2` (`quality/counters/c1-r41-globals-v2.py`)

Full report and PoCs: `.ufo/waves/round-41/w2/RevC1V2Counter/findings.md`.
Target: `quality/counters/c1-r41-globals-v2.py` (frozen at v2 registration `294c667901a8c7b7165ba849d03cba9a24c14fa4`, scored against data commit `07f2641696b5ac73de1404ea737a9f27e9819aa1` and base `ab2bfaab661c846d1de9d58c01651cd156a13949`). No lane files or git state were mutated.

## Summary of Findings & 4 PoC Cheats Scoring `39/39 TARGET_MET`

All four PoC cheats (`poc1`–`poc4`) were built from the v2 reference (`c1/ctl-ref-tool-v2.py.txt`) and scored with:
```
python3 -I quality/counters/c1-r41-globals-v2.py --repo . \
  --rev 07f2641696b5ac73de1404ea737a9f27e9819aa1 \
  --nonce c0ffee00deadbeef \
  --tool .ufo/waves/round-41/w2/RevC1V2Counter/<poc>.py
```
Every one of the four achieves `fixtures=39/39 tool=present verdict=TARGET_MET` (`clauses=a:1 b:1 b2:1 b3:1 g:1`, exit 0):

1. **HIGH — Clauses b, b2, and b3 are jointly defeated by a 4-line zero-test `selftest()` (`poc1_selftest_b2_b3_bypass.py`, `39/39 TARGET_MET`)**
   - Attacks `c1-r41-globals-v2.py:128-139, 1061-1133`.
   - Clause `g` bans `__file__` and `sys.argv[0]`, but allows `selftest.__code__.co_filename` (as well as `sys.argv[:1][0]`).
   - In `b` and `b3["comment"]`, line 1 of the file starts with `#!/usr/bin/env python3` (`ls[0][:1] == b"#"`). In `b3["unparse"]`, `ast.unparse` strips `#!` but appends an unindented `B3_NEUTRAL_<nonce> = 1` at the last line (`ls[-1][:1] != b" "`). In all 6 `b2` mutants (`mutate_source`, line 1071), `ast.unparse(tree)` strips `#!` AND leaves the last line indented (`    sys.exit(main())`, so `ls[-1][:1] == b" "`).
   - A 4-line `selftest()` checking `ls[0][:1] == b"#" or ls[-1][:1] != b" "` runs **zero** tests, passes `b` (`50/50`), kills `6/6` `b2` mutants (`forced_dead=1`), and passes both `b3` neutrality variants (`comment` and `unparse`).

2. **HIGH — Clause b2's forced-site rule and exact-name exclusion are evaded by nesting inside `selftest(argv=None)` (`poc2_b2_nest_decoy.py`, `39/39 TARGET_MET`)**
   - Attacks `c1-r41-globals-v2.py:130-136, 1035-1058` (`function_sites`).
   - `function_sites()` excludes `selftest`, `main`, `usage`, and all functions nested inside `selftest`. Moving the entire real implementation (`classify`, `parse`, `report`, `resolve_program`, `read_live`, `read_file`, `run`) inside `def selftest(argv=None):` and leaving a single 12-comparison dummy `guard()` holding `_ = "MADO_GLOBALS: sessions="` at module top level makes `function_sites()` 100% blind to the real tool (`sites=12 killed=6/6 forced_dead=1` on `guard()` alone). Also, chained comparisons (`a == b == True`, `len(node.ops) > 1`) are ignored by `function_sites()` (`line 1054`).

3. **HIGH — The `0111` execute-only ELF live stub's embedded journal is extractable via `LD_PRELOAD` before `main()` runs, and `../mk/ran` is writable by the tool (`poc3_stub_preload_oracle.py`, `39/39 TARGET_MET`)**
   - Attacks `c1-r41-globals-v2.py:94-98, 517-604` (`STUB_C`, `build_stub`, `execute`, `judge`).
   - Although the stub binary is `0o111` (`--x--x--x`), `os.stat(prog)` still reveals its mode (`0o111` vs `0o131` for `livewritable0`) and file size (`16408` for `livefail0`, `16464` for `livehang0`, `16488` for `ok`, `16544` for `livelarge0`).
   - Because `/usr/bin/gcc` is available in the sandbox and the stub is dynamically linked, `poc3` compiles a 12-line C constructor (`/tmp/d.so`) and runs the stub with `LD_PRELOAD=/tmp/d.so` (with no argv, pipe stdin, and `MADO_CANARY=1` still in env). The constructor reads `.rodata` (`P[]`) from `/proc/self/maps` and calls `_exit(0)` **before `main()` ever executes**, bypassing all `argv`, `stdin`, `environ`, and `sleep(3600)` checks in `STUB_C`.
   - Because `execute()` (`line 597`) mounts `rw=[mark]` at `<d>/mk` (`0o777`) while `cwd` is `<d>/fx`, the tool simply touches `../mk/ran` directly (`open("../mk/ran", "wb").close()`), satisfying `judge(..., ran=True)`.

4. **HIGH — Clause g misses 8+ standard Python constructs (`eval`, `os.execv`, `os.system`, `/proc`) and multiple docstring sentences have no fixture or contradict `STUB_C` (`poc4_clause_g_and_contract_gaps.py`, `39/39 TARGET_MET`)**
   - Attacks `c1-r41-globals-v2.py:43, 84-96, 139-148, 533-537, 974-1017`.
   - **Clause g bypasses (`imports_ok == True`):**
     - `from os import execv as _os_execv, system as _os_system` (`ast.ImportFrom` never checks `node.names`).
     - `import os as _os, sys as _sys` (`ast.Attribute` only checks `node.value.id in ("os", "sys")`).
     - `sys._getframe().f_globals['__bui'+'ltins__'].__dict__['ev'+'al']` (frame/function `__globals__`/`gi_frame`/`tb_frame` reflection reaches `globals()` and `eval`).
     - `os.__dict__['sys'+'tem']` and `object.__getattribute__(os, 'sys'+'tem')`.
     - `sys.argv[:1][0]`, `sys.argv[-len(sys.argv)]`, `next(iter(sys.argv))`, and `selftest.__code__.co_filename`.
     - `b"/proc/self/maps"` and `"/pr" + "oc"` (`STR_DENY`/`STR_EQ_DENY` only check single `str` constants).
   - **RLIMIT_NPROC (`line 99-100, 303`):** `prlimit --nproc=1:1` blocks `fork`/`clone` (`EAGAIN`), but does **not** block `execve` (`os.execv` via `from os import execv` succeeds under `--nproc=1:1`), and `--selftest` runs with `nproc=False`.
   - **Docstring vs `STUB_C` / fixture gaps (all broken simultaneously in `poc4` while still scoring `39/39 TARGET_MET`):**
     - Docstring line 43 specifies `[+-][0-9]{2}:[0-9]{2}` in `TS`, but every fixture hardcodes `-03:00` (`lines 396, 801-802`); dropping `+` from `ADVERT` still scores `39/39`.
     - Docstring lines 84–85 forbid `other-writable` (`S_IWOTH`) programs, but `livewritable0` only tests `0o131` (`S_IWGRP`); dropping `stat.S_IWOTH` still scores `39/39`.
     - Docstring lines 88, 95–96 state `stdin` must be `/dev/null` (`a character device, not a pipe`), but `STUB_C` line 533 only checks `S_ISFIFO(st.st_mode)`; passing a directory fd (`os.open('.', os.O_RDONLY)`) as `stdin` still scores `39/39`.
     - Docstring lines 88–89 state the stub runs with `PATH`, `XDG_RUNTIME_DIR`, `DBUS_SESSION_BUS_ADDRESS`, `LC_ALL`, but `STUB_C` lines 534–537 only reject unlisted keys; passing an empty `env={}` to the stub still scores `39/39`.
     - Docstring line 90 (`spawn failure`) and line 36 (`unreadable` `0o000` regular file or char device) have no fixture; `score_livehang0` (`line 923`) uses `timeout=100` instead of checking the docstring's 30 s cap.
   - **Opaque names (`line 565-566`):** `opaque(name)` hides plaintext fixture names behind `sha256(NONCE:name)[:12]`, which is not invertible without `NONCE`, though `/tmp/mado-c1r41v2-<rand>` still lists `[opaque(fixture), opaque("real")]` and `judge()` (`line 601`) ignores its `file_mode` parameter and leaves `STUB_FILE` (`line 514`) and `import base64` (`line 164`) as dead code.

## Tooling
None installed or updated (host `python3`, `gcc`, `bwrap`, `prlimit`, `git` used read-only).
