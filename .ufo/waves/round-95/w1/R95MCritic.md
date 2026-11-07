# R95MCritic — C1/C2 falsification (round 95, w1, DRAFT evidence only)

Seat: R95MCritic. S=`/fast/scratch/hyaku/mado-r95/R95MCritic` (deleted on exit). Base `4a2af6817024f6ed47084a5217c1825ae247f4fe`.
All runs below are DRAFT: no counter was run in measured mode, nothing was written under `receipts/`, and no verdict is claimed.
Installs: none (no pacman, uv, npx or binary install).

Predicate under attack: `.ufo/waves/round-95/claims-declaration-r95.md:36-53` (C1) and `:69-78` (C2).
Candidate: `.ufo/waves/round-95/build/mado-mimesniff.c1.py` sha256 `a13b6e0e…cde99d` (declared); the L1 has since
written `.ufo/waves/round-95/build/mado-mimesniff.c1b.py` sha256 `abef00143e306fbdc970cc04b2af576e492e570a2b5d6430bf09f97f6895006c`
(diff: only the `i + value_length` wrap rule). Oracle: `controls/mimesniff-oracle-r95.c` sha256 `99df35f8…124a`, built
`cc -O0 … $(pkg-config --cflags --libs gio-2.0)` (rc 0); host `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`,
`python 3.14.8-1` (never `2.90.1-1` otherwise). Candidate `--selftest`: `checks=23 failed=0` rc 0 (c1 and c1b);
`tools/mado-mimeglob.py --selftest` 19/0 rc 0; `tools/mado-portals.py --selftest` 28/0 rc 0;
`quality/check-selftest-strength.py --selftest` 11/0 rc 0.

## Axes and the base command

Axis moved by C1 is **coverage**: the surface is "bytes (+ name) → (type, uncertain) that GLib answers"; round 94
covered only the name step. Base command (run at the fleet root, read-only):
`git show 4a2af681:tools/mado-mimesniff.py` → `fatal: path … does not exist` (rc 128); `grep -l magic tools/*.py` → no
output, rc 1; `git show 4a2af681:tools/mado-mimeglob.py | sha256sum` → `65f80a6c…2453` (matches the pin). So the axis
is unmoved at base (0/N) and the pinned sibling is the round-94 bytes. C2's axis is **operability** (selftest strength);
base has no kill-set for either tool and the gate on `--kills` absent stops SETUP_ERROR, so its base is 0 of anything.

## C1 counterexamples

### C1-F1 (blocking, defined behaviour) — VT (0x0b) is binary in GLib, text in the candidate

GLib's `looks_like_text` rejects a byte that is `g_ascii_iscntrl` and not `g_ascii_isspace` and not `'\b'`
(`fetch/gcontenttype-fdo.c:532-548`). The installed table gives byte 11 **not** space — probed directly, compiled against
the installed glib: `g_ascii_isspace(0x0b)=0`, `0x0c=1`, `0x08=1`, `0x7f` cntrl-but-not-space (probe source
`isspace.c` in S, `printf("%02x cntrl=%d space=%d")`). The candidate's `looks_like_text`
(`build/mado-mimesniff.c1.py:207-208`; `c1b.py:208-209`) exempts 0x0b: `not any(b < 8 or 14 <= b < 32 or b == 127 …)`.
So a buffer whose first 128 bytes contain 0x0b and no other binary byte is `application/octet-stream 1` in GLib and
`text/plain 0` in the candidate.

- Whole-byte sweep (one valid empty cache in s1, one in s2; oracle `env -i HOME=h LC_ALL=C XDG_DATA_DIRS=s1:s2`,
  candidate `Sniffer([s1/mime, s2/mime]).guess(None, bytes([i]))`, i=0..255): **1 diff** —
  `byte=0b oracle=('application/octet-stream', 1) cand=('text/plain', 0)`. All other 255 bytes agree.
- Reproducing cases (written): `.ufo/waves/round-95/w1/R95MCritic-cases.json`, sha256
  `e67acdf22ef0444f76722bc002e0217eb30e147915019d2972034997c83f0d66`, 5 cases; all labels re-verified against the
  oracle in a materialised `{root}` (rc 0 each). `lltext-01-vt-only` = data `0b`, label `["application/octet-stream",1]`;
  `lltext-02-vt-in-text` = data `61620b6364`, same label; `lltext-03-ff-control` = `0c` → `["text/plain",0]`;
  `lltext-04-bs-control` = `08` → `["text/plain",0]`.
- The frozen candidate answers `text/plain 0` on `lltext-01`/`02` (c1 and c1b, rc 0) → a frozen `lltext` case the
  counter must count as a miss. The candidate's own selftest encodes the wrong expectation
  (`c1b.py:468` "s10 VT passes looks_like_text" asserts `ab\x0bcd == ("text/plain",0)`), so `--selftest 23/23`
  cannot catch it. Independent corroboration: `w1/R95MScribeEntry.md` §F1 (same byte, different case file).
  The host leg cannot catch it either: the fallback reads only the first 128 bytes and the host scan found no file
  with 0x0b in the first 128 without another binary byte (ScribeEntry §F1, `R95MScribeEntry-host.out.txt`).

Smallest safe correction (candidate, one token): in `looks_like_text` add `b == 11`:
`return not any(b < 8 or b == 11 or 14 <= b < 32 or b == 127 for b in data)`; and change the `s10` selftest
expectation to `("application/octet-stream", 1)` (or delete it, since the mutant set must kill the boundary).
With that one edit the fuzz below is 0-diff. The frozen generator must also pin the `lltext` boundary bytes
(08, 0b, 0c, 7f, and index-127/128 placement); `0x0b` is not reachable by any host file the list samples.

### C1-F2 (blocking, identity/pin) — the declared sha fails a case the class list names

The declaration pins `a13b…` (`claims-declaration-r95.md:20-21`) and the class list includes `wrap`
(`:39-40`). On `wrap-01-wrapped-sum-above-len` (one matchlet `start=0xFFFFFFF0, length=2, value=32 bytes`, data `ABCD`):
oracle rc 0 `text/plain 0`; **c1 `a13b` exits 3** `UNSUPPORTED matchlet i + value_length passes 2^32` (rc 3);
c1b `abef` answers `text/plain 0` rc 0. So as frozen the declaration contradicts itself: either the pin moves to
`abef…` (and the L1 finding L1-F1 is landed) or the `wrap` class cannot carry this case. Smallest correction: re-pin
the PRED and the candidate table to the c1b bytes and keep the case (it is the one that pins the L1-F1 repair);
the c1b rule (`((i+value_length)&M32) > len` → False, only a wrapped sum ≤ len refuses) is the one my targeted fuzz
found correct (600 wrap-shaped cases, 7 oracle crashes skipped, 0 diffs after the VT fix).

### C1-F3 (predicate hole) — the nesting cap is above the C stack limit

`MAX_NEST = 100000` (`c1.py:88`, `:152-153`; c1b `:89`, `:153-154`) claims "the C recursion overflows" there.
Measured on this host/stack (one magic entry, a chain of D matchlets, data `X`): the oracle survives D=74848 and
crashes (SIGSEGV, rc -11) at **D=74849**; the candidate answers `a/x 0` at every D ≤ 100000 and refuses only above.
So for 74849 ≤ D ≤ 100000 the oracle's label is `["UNSUPPORTED",null]` and the tool answers — a case the `nest` class
can legitimately hold. The boundary is stack-size dependent, so no fixed tool cap can equal it. Smallest safe
correction: freeze a *bound* instead of the crash: (a) the generator emits no magic chain deeper than 512, and the
PRED's named limits say "chain depth > 512 is a declared limit, not a case domain"; (b) the candidate's cap is set to
512 and the docstring stops claiming 100000 is the C overflow point. Do **not** add a deep-chain case: its label flips
with the measurement shell's stack limit and would make the counter SETUP_ERROR at random.

### C1-F4 (blocking, (vi) evasion) — the sibling import leaks ctypes and os

`(vi)` allows one `spec_from_file_location` of `mado-mimeglob.py` and forbids process/socket/ctypes machinery *in the
tool*. The loaded module binds `import ctypes`, `import os`, `import sys` (`tools/mado-mimeglob.py:52-58`), so the
tool can reach them through the module object with no import, no `eval`, no `os.system` text of its own and no
subprocess. Demonstrated forgery (S/forgery/tools/mado-mimesniff.py; full source in §Appendix A): it loads
`mado-mimeglob.py` from its own directory exactly as the carve-out allows, then
`gio = mg.ctypes.CDLL("libgio-2.0.so.0")` and calls `g_content_type_guess` through `mg.ctypes`. Run:
`env -i HOME=h LC_ALL=C XDG_DATA_DIRS=s1:s2 PATH=/nonexistent-empty /usr/bin/python3 -I tools/mado-mimesniff.py --json x.bin`
with a cache carrying priority-90 `a/hi` for `HI` → `{"type":"a/hi","uncertain":0}` rc 0; oracle `a/hi 0`.
It passes (i), (ii) and (iii) by construction and fails none of (vi)'s named patterns; `mg.os.system`/`mg.os.popen`
are equally reachable (and `getattr` is not in (vi)'s forbidden list). `PATH` empty is no obstacle: the oracle path
is absolute, and `CDLL` needs no PATH. This is the exact QUALITY-162 forgery round 94 rejected only because it
imported `ctypes` itself (`.ufo/waves/round-94/controls/forgery-ctypes-gio-r94.py`).

Note also that (vi)'s prose "spec_from_file_location of `mado-mimeglob.py` in its own directory" pins nothing
mechanically: `spec_from_file_location("mado_mimeglob", "/abs/path/to/anything.py")` satisfies the sentence as written.
The repair below pins the exact path expression and the loaded module's name.

Smallest safe correction — replace (vi) with a scoped allowlist plus an audit hook (exact text):
```
(vi) static_no_external_resolver=ok iff the counter
 (a) AST-parses tools/mado-mimesniff.py: every Import/ImportFrom is one of argparse, importlib.util, json, os,
     struct, sys; no Name reference to eval, exec, compile, __import__, getattr, setattr, delattr, vars, globals,
     locals, breakpoint; exactly one importlib.util.spec_from_file_location call, name argument the constant
     "mado_mimeglob", location argument os.path.join(os.path.dirname(os.path.abspath(__file__)),
     "mado-mimeglob.py");
 (b) every attribute access on the module object bound by that call is in {Unsupported, oob, Resolver,
     xdgmime_dirs, g_path_get_basename, esc, _LC_ALL} or is exactly the chain `_libc.setlocale`; any other
     attribute (ctypes, os, sys, subprocess, importlib, __dict__, __class__, …) FAILs;
 (c) runs the tool under a launcher that installs sys.addaudithook and FAILs on subprocess.Popen, os.system,
     os.exec*, os.posix_spawn, socket.__new__ and ctypes.dlopen events, except ctypes.dlopen of the libc
     soname and the one ctypes.util.find_library probe whose argv[0] is /sbin/ldconfig, ldconfig, gcc, cc or ld;
 (d) also carries reads_confined=ok: under the same hook every open() target is under the materialised case root,
     the tool's own copied directory, the Python installation or the tool's temp dir; a read of any lane file
     (the frozen cases JSON, the fresh generator, the oracle, quality/, tools/) FAILs.
```
(d) is not decoration: the frozen cases and the frozen generator are world-readable lane files, so at measurement a
candidate can read `controls/mimesniff-cases-r95.json` and echo labels by matching the bytes, and can import the
generator to precompute the 120 "fresh" answers. No behavioural leg distinguishes that; only the read hook does.
The audit hook also keeps the honest tool working: `mado-mimeglob.py`'s `ctypes.util.find_library("c")` spawns
`/sbin/ldconfig` (absolute path, so the empty PATH does not stop it) — hence the explicit spawn/dlopen allowances.

### C1-F5 (predicate hole) — the fresh leg is not fresh

`(ii)` says "120 fresh seeded cases from the frozen generator". The generator, its seeds and the case file are all
frozen at the same commit as the candidate, so the candidate can embed the 120 answers (a literal table is not
forbidden by (vi)) or, with F4's leak, read the generator at run time. Smallest correction: the counter reads
`seed = os.urandom(16).hex()` at measurement, passes it as `--seed` to the frozen generator (the generator *requires*
`--seed`, no default) and ships no case file; (ii) is regenerated every measurement and never stored in the lane.
`(ii)` must also state the UNSUPPORTED rule: a fresh case whose oracle crashes/hangs within 10 s requires exit 3
(as in (i)); a tool that exits 3 on an oracle-answered case is a miss. `(v)` must also carry the two controls the
item names and the draft omits: a **memoriser** (a table of the frozen labels, octet-stream otherwise) that passes
(i) and must miss (ii), and the Appendix-A **sibling-module wrapper** that must print
`static_no_external_resolver=FAIL`. Without these two, (v) proves only that four weak controls are weak.

### C1-F6 (predicate hole) — the `real` class is not pinned to a real database

The class list requires `real`, and the seat item says the `real` class must use `update-mime-database` on
`packages/*.xml`, but the PRED only counts class membership ≥6. Six `build_cache` fixtures labelled `real` satisfy it.
Smallest correction: the `real` cases store the `packages/*.xml` inputs in `files` and the counter rebuilds the cache
with `update-mime-database` in its scratch and requires the stored `mime.cache` bytes to equal the rebuild
(mismatch = SETUP_ERROR); the receipt prints the rebuild sha. This is the only leg that anchors the tool to a real
`mime.cache` shape rather than the candidate's own builder.

### C1-F7 (predicate hole) — the class list is enumerated but not load-bearing

`classes=20/20, ≥6 each` is satisfiable with six near-duplicates per class; nothing forces a class's cases to exercise
its rule, and the PRED does not say a case's class outside the 20 is refused (QUALITY 160's counter behaviour).
Smallest correction, two conjuncts:
- "no case carries a class outside the 20 (unknown class = SETUP_ERROR), and the counter prints `cases=N` and
  `classes=20/20` with the per-class counts";
- "each class kills at least one counted mutant that no other class's cases kill (`class_kills[X] ≥ 1`); the counter
  prints `class_kills` and fails the class conjunct on a zero". A decorative class then cannot survive, and the `lltext`
  class must carry the boundary byte (F1) because the VT mutant is killed only there.

## C2 counterexample

### C2-F1 (blocking, metric) — (ii) is label coverage; a label-only kill-set reaches 47/47 and misses a real weakening

`(ii)` forces each check to pass and asks the gate to print WEAK. Any exact-set kill-set that covers the label does
that: the forced check stops failing, so the mutant's FAIL list differs from `must_fail` (or the mutant survives).
Demonstrated on `tools/mado-mimeglob.py` (copy; gate `quality/check-selftest-strength.py`, rc recorded):

| run | gate output |
|---|---|
| green weakening (t05 drops the `uncertain` component): `("t05 weight orders two types", g(b"x.dup", ["a/mime"])[0] == "app/hi")`; unmutated weakened tool: `checks=19 failed=0` | — |
| label-only kill (production `a.sort(key=lambda x: -x[1])` → `…x[1]`, changes only the type; `must_fail` = `"t05 weight orders two types"`), weakened tool, `--allow-sha-drift` | **rc 0 `SELFTEST_STRENGTH: OK … kills=1 held=1 survived=0 wrong_check=0`** |
| same kill, forced-pass neutralisation `… == ("app/hi", 1)` → `… == True` | rc 1 `WEAK … survived=1` |
| same kill, unmutated tool | rc 0 `OK … held=1` |
| witness kill (production `uncertain: 1` → `0` only, `must_fail=["t05 …","t12 equal weight keeps file order"]`), weakened tool | rc 1 `WEAK … wrong_check=1` |
| tautology weakening (`… == g(b"x.dup", ["a/mime"])`), label-only kill | rc 1 `WEAK … survived=1` |

Read: the label-only set scores the forced-pass leg (so `0/47 → 47/47`) and still misses the drop-component
weakening; a panel made only of round-94's "expected replaced by observed" tautologies is fully flagged by label-only
sets. QUALITY 161's exact counterexample is reachable, so **47/47 forced-pass is not the strength axis**; the headline
must be `hand_flagged` over a panel of green, component-dropping weakenings.
Smallest correction: see C2-F2/F3 and the PRED-C2 text in §Freeze-ready repairs.

### C2-F2 (blocking, panel provenance) — the panel is authored by the seat whose kill-sets it judges

`(iii)` says "each frozen hand weakening of the panel"; the panel is R95MExecCounterC2's file (`controls/selftest-panel-r95.json`),
the same seat writes the counter, and the named limit (`claims-declaration-r95.md:91-92`) admits "panel weakenings and
closing kills from the same wave (design set)". A tautology-only panel then yields (ii)+(iii) = 47/47 as above.
Smallest correction: the panel file's sha256 is written into the declaration **before** the kill-sets are finalised;
the panel is the union of (a) R95MMutC1's green weakenings, (b) the nine attack-seat pairs below (all verified green
against the unmodified tools), and (c) at least one drop-a-component pair per check whose result is a tuple/list;
the counter refuses a panel sha that is not the pinned one. Closing kills must carry a witness mutant per panel entry
(changing the dropped component); a panel entry that no mutant can witness is a setup error, not a silent pass.

Attack-seat pairs (exact `find` → `replace`, each leaves `checks=19|28 failed=0`; all nine verified):
```json
[
 {"tool":"tools/mado-mimeglob.py","id":"crit-mg-w01-t05-drop-uncertain",
  "find":"(\"t05 weight orders two types\", g(b\"x.dup\", [\"a/mime\"]) == (\"app/hi\", 1))",
  "replace":"(\"t05 weight orders two types\", g(b\"x.dup\", [\"a/mime\"])[0] == \"app/hi\")"},
 {"tool":"tools/mado-mimeglob.py","id":"crit-mg-w02-t14-drop-uncertain",
  "find":"(\"t14 basename only\", g(b\"dir.txt/f.c\", [\"a/mime\"]) == (\"text/x-c\", 0))",
  "replace":"(\"t14 basename only\", g(b\"dir.txt/f.c\", [\"a/mime\"])[0] == \"text/x-c\")"},
 {"tool":"tools/mado-mimeglob.py","id":"crit-mg-w03-t04-drop-uncertain",
  "find":"(\"t04 deepest suffix wins\", g(b\"x.tar.gz\", [\"a/mime\"]) == (\"app/x-tgz\", 0))",
  "replace":"(\"t04 deepest suffix wins\", g(b\"x.tar.gz\", [\"a/mime\"])[0] == \"app/x-tgz\")"},
 {"tool":"tools/mado-mimeglob.py","id":"crit-mg-w04-t12-drop-uncertain",
  "find":"(\"t12 equal weight keeps file order\", g(b\"f.two\", [\"a/mime\"]) == (\"t/one\", 1))",
  "replace":"(\"t12 equal weight keeps file order\", g(b\"f.two\", [\"a/mime\"])[0] == \"t/one\")"},
 {"tool":"tools/mado-portals.py","id":"crit-pt-w01-reason-dropped",
  "find":"chk(\"default list falls to second backend\", r.resolve(FC) == ([\"gtk\"], \"default config\"))",
  "replace":"chk(\"default list falls to second backend\", r.resolve(FC)[0] == [\"gtk\"])"},
 {"tool":"tools/mado-portals.py","id":"crit-pt-w02-backends-dropped",
  "find":"chk(\"interface key beats default none\", r.resolve(FC) == ([\"kde\"], \"interface specific config\"))",
  "replace":"chk(\"interface key beats default none\", r.resolve(FC)[1] == \"interface specific config\")"},
 {"tool":"tools/mado-portals.py","id":"crit-pt-w03-desktops-second-dropped",
  "find":"chk(\"desktops dropped/lowercased\", current_desktops(\"KDE::bad/x:GNOME-Classic\") == [\"kde\", \"gnome-classic\"])",
  "replace":"chk(\"desktops dropped/lowercased\", current_desktops(\"KDE::bad/x:GNOME-Classic\")[:1] == [\"kde\"])"},
 {"tool":"tools/mado-portals.py","id":"crit-pt-w04-string-list-second-conjunct",
  "find":"chk(\"string list trailing empty dropped\", string_list(\"a;b;\") == [\"a\", \"b\"] and string_list(\"a;;b\") == [\"a\", \"\", \"b\"])",
  "replace":"chk(\"string list trailing empty dropped\", string_list(\"a;b;\") == [\"a\", \"b\"])"},
 {"tool":"tools/mado-portals.py","id":"crit-pt-w05-cr-value-dropped",
  "find":"chk(\"final CR without LF is kept\", parse_keyfile(\"[g]\\na=b\\r\\nc=d\\r\") == {\"g\": {\"a\": \"b\", \"c\": \"d\\r\"}})",
  "replace":"chk(\"final CR without LF is kept\", parse_keyfile(\"[g]\\na=b\\r\\nc=d\\r\")[\"g\"][\"c\"] == \"d\\r\")"}
]
```
The witness mutants for these entries (what must be added to the closing kill-set) are: for every `drop-uncertain`
pair a production edit that changes only `uncertain` on the same case (e.g. `return {"type": types[0], "uncertain":
1, "types": types}` → `…: 0, …` with `must_fail` = the labels it fails on the *original* tool: for t05/t12 the pair
`["t05 …", "t12 …"]`); for the portals pairs a production edit that changes only the dropped component (the reason
string, the backend list, the second desktop token, the second list conjunct, the `c` value).

### C2-F3 (predicate hole) — (iv) and (vii) are vacuous as written

`(iv)` "each frozen neutral edit → OK" is satisfied by zero neutral edits. `(vii)` names the first-draft kill-sets but
no sha, so they can be tuned after the panel is known.
Smallest corrections: `(iv)` requires ≥2 neutral edits per tool, each changing the tool's sha and each printing OK rc 0
(round 94's six neutral edits are the model); `(vii)` pins both first-draft files' sha256 in the declaration and says
they flag strictly fewer **panel** weakenings than the frozen kill-sets.

### C2-F4 (reporting) — the "before" is not a measurement

`0/47` is "no kill-set; do-nothing instrument" (`:77-78`), i.e. the instrument does not exist; QUALITY 161's before is
the round's first-draft kill-sets' `hand_flagged`. Smallest correction: `Before → after: first-draft kill-sets
hand_flagged=F/47 (measured, F printed) → frozen hand_flagged=47/47`, and keep the do-nothing/always-OK/always-WEAK as
controls only.

## Separability

Holds as drafted, with one condition: C1 must be measured at its own commit with `tools/mado-mimeglob.py` at the
round-94 sha (verified `git show 4a2af681:tools/mado-mimeglob.py | sha256sum` = pin), and C2's kill-set pins that same
sha; C2 never edits either tool. C1's counter at the C2 commit re-runs, because C2 adds only
`quality/selftest-kills/*.json`; C2's counter at the C1 commit stops SETUP_ERROR because its kill-sets are absent.
The F4/F5 repairs are C1-only (they change C1's counter and the tool's `--selftest`, not C2).

## Impacted axes

- C1 **coverage**: F1 (a frozen `lltext` case is answered wrongly), F2 (the declared sha fails `wrap`), F3 (`nest` has
  no frozen bound), F6/F7 (the class list and `real` are not load-bearing), F4/F5 (a wrapper/memoriser can pass all
  behavioural legs). F1 and F2 force a candidate edit and a re-pin; F4/F5/F6/F7 change the counter, not the tool.
- C2 **operability**: F1 (the metric), F2 (panel provenance), F3 (vacuous legs), F4 (before). None of these changes a
  tool; they change the PRED and the counter.
- Declaration **identity/provenance**: the pin `a13b…` must become `abef…` (F2) or the `wrap` class must drop the
  case; the panel sha and the first-draft shas must be frozen before measurement (F2/F3).

## Appendix A — the (vi) forgery (full source; reproducible in S/forgery/tools/mado-mimesniff.py)

```python
import importlib.util, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mado_mimeglob", os.path.join(here, "mado-mimeglob.py"))
mg = importlib.util.module_from_spec(spec); spec.loader.exec_module(mg)
gio = mg.ctypes.CDLL("libgio-2.0.so.0")
gio.g_content_type_guess.restype = mg.ctypes.c_char_p
gio.g_content_type_guess.argtypes = [mg.ctypes.c_char_p, mg.ctypes.c_void_p, mg.ctypes.c_size_t,
                                      mg.ctypes.POINTER(mg.ctypes.c_int)]
name = None
for i, a in enumerate(sys.argv):
    if a == "--name": name = sys.argv[i + 1]
files = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (name or "",)]
with open(files[-1], "rb") as fh: data = fh.read()
u = mg.ctypes.c_int(0)
t = gio.g_content_type_guess(os.fsencode(name) if name else None, data, len(data), mg.ctypes.byref(u))
print(json.dumps({"mode": "cache", "dirs": [], "results": [{"file": files[-1], "name": name,
      "type": t.decode(), "uncertain": 1 if u.value else 0, "sniffed": t.decode(), "prio": 0, "types": []}]}))
```
Run (empty PATH, absolute interpreter): rc 0, `{"type":"a/hi","uncertain":0}`; oracle `a/hi\t0`.

## Appendix B — fuzz coverage used (all DRAFT)

- Synthetic-cache fuzz: random priorities (0, 1, 10, 50, 79, 80, 81, 100, 2^31, 2^31+5, 0xFFFFFFFF), random
  matchlets (start 0..6, length 0..3, values 0..3 bytes incl. 0x7f/0x0b, masks, 1–2 child levels), aliases, parents,
  globs, two caches, names {NULL, x.dup, x.one, x.two, x.amb, d/, "", zz.none}; seeds 1/400 and 7/800 → **0 diffs**
  after the VT fix (`fuzz.py`), 0 before on all inputs without 0x0b in the first 128 bytes.
- Wrap-shaped fuzz (random start near 2^32, value_length up to 2^32-1, data 0–5 bytes): 600 cases, 7 oracle crashes
  skipped, **0 diffs** with c1b+VT fix; the 3 pre-fix diffs were all VT.
- Nesting bisection: survives 74848, crashes 74849; at 100001 oracle rc -11 while c1/c1b answer `a/x 0`.
- Single-byte sweep: 1 diff (0x0b).
