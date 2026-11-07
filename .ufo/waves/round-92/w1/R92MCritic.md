# R92MCritic — attack on the round-92 claims declaration (C1 coverage, C2 operability)

Seat: critic, round 92 v1 wave w1. Target: the DRAFT declaration
`.ufo/waves/round-92/claims-declaration-r92.md` as it stands at 23:1x on 2026-11-06, with the live candidates
`build/mado-xdgmime.c1.py` and `build/check-seat-reports.c2.py`, the two counters, the oracle, the case/battery
generators, and the round-91 set/mutants. Base revision `d992ef7494b054591ee9104df1da49264678df5d`.

**Rank of what follows.** Two things block a freeze on the declared predicate: the C1 candidate contradicts the C1
predicate on four frozen cases (§2), and the C1 sandbox does not stop a tool that carries its own interpreter (§3),
which reaches `DRAFT_TARGET_MET` on every measured leg. C2's battery body is quotable (§4) but its round-91 leg
still rejects the quote tool mechanically; the round-91 leg itself is not frozen (§6.6) and its failure is
misreported as `NOT_MET` rather than `SETUP_ERROR` (§6.7). §7 lists the concrete fixes in rank order.

Everything below is a **DRAFT** run (`--draft-tool` / `--draft-check`, counter rc 3); nothing here is a measurement
and nothing was written under `.ufo/waves/round-92/receipts/`. No lane file was modified; the only lane write is
this report. Scratch `S=/fast/scratch/hyaku/mado-r92/R92MCritic` was removed on exit.

---

## 1. Environment, pins, method

Host: linux 7.2.11, python 3.14.8, bubblewrap 0.13.1, `/usr/bin/sh -> bash` (bash 5.3.020-1), `/usr/bin/xdg-mime`
sha256 `a587107f…15f3f` (xdg-utils 1.2.1-2). Pinned binaries in the counter's order:
`xdg-mime a587107f…`, `bash c14c8f49…`, `grep 19280b0e…`, `gawk 3ac64468…`, `realpath 5f6c63c5…`,
`basename a21add5f…` — all matched at every run (`oracle_agree=128/128` in all nine C1 draft runs).

Control pins used (sha256, current files):
`xdgmime-cases-r92-l1.json d519993c…12d9` (128 cases), `xdgmime-oracle-r92.py e5160399…f87b`,
`fuzz-gen-r92.py 891704bf…5c01`, `gate-defects-battery-r92-l1.json cc0b793d…4638` (32 fixtures),
`r91-c2-argv-r92.json d21b1979…b604`. Draft runs passed a scratch `{"mutants":[]}` file for `--mutants` /
`--draft-check` runs (the counters validate the frozen mutants against the draft bytes; see §6.8).

**Snapshot note.** The controls and candidates were being edited by other seats throughout this review: the C2
battery went 19,629 B / 27 fixtures (22:52) → 20,281 B / 28 (23:01) → 23,247 B / 32 (23:13, sha `cc0b793d…`), the C2
counter was touched at 23:13:21 (sha `268bf151…`), the C1 counter at 23:01:55 (sha `80979ee4…`), and the C1
candidate at 23:04/23:12/23:14 (three hashes below). Every number quoted below names the bytes it was measured on;
the L1 must re-run the two DRAFT legs after the last pre-freeze edit.

Reproduce a C1 draft (own scratch root, own log):

```
python3 -I quality/counters/c1-r92-xdgmime-default.py --repo <lane> --rev d992ef74… --base-rev d992ef74… \
  --cases .ufo/waves/round-92/controls/xdgmime-cases-r92-l1.json --mutants <empty-mutants.json> \
  --oracle …/xdgmime-oracle-r92.py --fuzz-gen …/fuzz-gen-r92.py --expect-cases-sha256 d519993c… \
  --expect-mutants-sha256 <sha of the empty file> --expect-oracle-sha256 e5160399… --expect-fuzz-sha256 891704bf… \
  --expect-bin-sha256 <six digests> --fresh 120 --scratch-root <S>/c1/<name> --draft-tool <tool>
# rc 3 = draft; the verdict line is MADO_XDGMIME_DEFAULT: DRAFT_TARGET_{MET,MISSED}
```

---

## 2. FREEZE BLOCKER — the C1 candidate contradicts the C1 predicate on four frozen cases

The C1 predicate (`claims-declaration-r92.md:23-25`) says the tool must print, "for every asked type the same line
and exit status as the installed xdg-mime labelled". The frozen case file asks four types that
`build/mado-xdgmime.c1.py` refuses by design; its docstring (`:23-24`) says so: "Scope (refused with rc 2
`unsupported`, never guessed): an asked type with a character outside RFC 6838 restricted-name". The refusal is
raised at `:708` (`raise Unsupported(f"type {fs(mime)!r} has characters outside RFC 6838 restricted-name …`) and
printed at `:753`, and the tool exits 2 (`run_tool` returns `None` → every type of that case is scored wrong).

DRAFT run of the candidate (`--draft-tool build/mado-xdgmime.c1.py`, `--fresh 120`, rc 3):

```
MADO_XDGMIME_DEFAULT: DRAFT_TARGET_MISSED pred=PRED-C1-r92-v1 rev=draft:…/build/mado-xdgmime.c1.py
  cases=128 correct=124 b=16/16 d=39/39 f=19/21 g=4/6 m=36/36 s=10/10 answered=124/128
  fresh=120/120 … oracle_agree=128/128 do_nothing_correct=33 naive_mimeapps_correct=44 glib_resolver_correct=59
  base_tool_correct=0 base_tool=absent tool_sha256=084bce8c…cfec
case f14-invalid-regex WRONG
case f17-star-in-type WRONG
case g05-awk-v-escape WRONG
case g06-awk-v-escape-defaults WRONG
```

The four reproducers (fixture in the oracle's case schema; oracle = xdg-mime 1.2.1 on the host):

| case | fixture (files, env is the standard `{ROOT}/cfg|etc|data|share`, `XDG_CURRENT_DESKTOP=Hyprland`) | xdg-mime (`oracle.run_one`) | candidate |
|---|---|---|---|
| `f14-invalid-regex` | `share/applications/defaults.list`: `[Default Applications]\ntext/[=br.desktop;\n`; type `text/[` | `{'default': None, 'rc': 0}` | rc 2, stderr `unsupported: type 'text/[' has characters outside RFC 6838 …` |
| `f17-star-in-type` | `share/applications/mimeinfo.cache`: `[MIME Cache]\ntext/plain=st.desktop;\n`; type `text/p*lain` | `{'default': 'st.desktop', 'rc': 0}` | rc 2, same |
| `g05-awk-v-escape` | `cfg/mimeapps.list`: `…\ntext/x\tz=a.desktop\n` (literal TAB); `data/applications/a.desktop` Exec=`a %U`, `bin/a` 0755; type `text/x\tz` (backslash-t) | `{'default': 'a.desktop', 'rc': 0}` | rc 2, same |
| `g06-awk-v-escape-defaults` | `share/applications/defaults.list`: `[Default Applications]\ntext/xtz=t.desktop;\n`; type `text/x\tz` | `{'default': 't.desktop', 'rc': 0}` | rc 2, same |

This is not a sandbox artefact: the same four cases fail in the host run with the same stderr. It is the
declaration's "every frozen case" vs the candidate's documented scope — a direct contradiction that the freeze must
resolve one way or the other. Note the timeline: `xdgmime-cases-r92-l1.json` mtime 22:52:56, the candidate mtime
23:12:57 and still changing while I ran: the candidate hashes I measured were `b6497a0a…`, `ffc366c7…` and
`084bce8c…` (mtime 23:14:43, the last run), with `b5c79e4d…` on disk between two runs. All tested versions refuse
the same four cases. Re-run this DRAFT immediately before the freeze commit.

Smallest safe correction: implement the two real behaviours the oracle demonstrates — (a) grep BRE metacharacters
in the asked type are passed to the BRE matcher (`text/p*lain` matches `text/plain`), and (b) gawk's `-v`
backslash processing turns `text/x\tz` into `text/x<TAB>z` before matching (which is why `text/x\tz` hits the
literal-TAB line in g05 and the `text/xtz` line in g06) — or, if the L1 wants the narrower scope, remove exactly
those four cases from the frozen file **before** the freeze and change the declaration's "every frozen case" to the
reduced count (and say the reduction out loud). The current state is the one outcome the freeze must not accept:
predicate says all, candidate says 124.

### 2b. Second freeze blocker — the mutant list (and its generator) is stale against the candidate

Independent of the four cases, the current candidate cannot even be *scored* with the current mutants. The
candidate's pathname-expansion test was refactored from `if not any(ch in word for ch in b"*?["):` to
`if not re.search(rb"(?:^|[^\\])(?:\\\\)*[*?[]", word):` (`build/mado-xdgmime.c1.py:182`); the mutant `M32` in
`xdgmime-mutants-r92-l1.json` (mtime 22:52:54) and in `gen-c1-mutants-r92.py` (mtime 23:07:23) still anchors the old
line. Reproductions:

```
$ python3 .ufo/waves/round-92/controls/gen-c1-mutants-r92.py build/mado-xdgmime.c1.py $S/regen/mut.json
M32: find occurs 0 times
rc=1                       # the generator cannot regenerate the frozen file either

$ python3 -I quality/counters/c1-r92-xdgmime-default.py … --mutants <file with only M32> --draft-tool build/mado-xdgmime.c1.py
… MADO_XDGMIME_DEFAULT: SETUP_ERROR mutant M32: find occurs 0 times
rc=2                       # the counter's real setup branch, c1-r92-xdgmime-default.py:270-271
```

Every other anchor is fine (C2 17/17, r91 55/55, C1 38/39). Smallest safe correction: update `M32` in the
generator to the new line (`if not re.search(rb"(?:^|[^\\])(?:\\\\)*[*?[]", word):` → the mutant's wrong belief,
e.g. treat a backslash-quoted metacharacter as globbed), regenerate `xdgmime-mutants-r92-l1.json` from the frozen
candidate bytes, and re-pin `--expect-mutants-sha256`. Do this *after* the last candidate edit — the mutant list is
generated from those bytes, and the candidate changed four times during this review.

---

## 3. C1's sandbox hides the host's interpreters, not one the tool carries — DRAFT_TARGET_MET by a forgery

I built three forgery classes and ran each through the C1 counter as a draft tool (rc 3 each):

| draft tool | mechanism | cases (128) | fresh (120) | controls | verdict |
|---|---|---|---|---|---|
| `c1-none.py` | answers `None`/0 everywhere | 33 | 45 | do_nothing 33, naive 44, glib 59, base absent 0 | MISSED |
| `c1-shellout.py` | execs `/usr/bin/xdg-mime`; falls back to `sh`/`bash`/`dash`/`zsh`/`ksh`/`mksh`/`busybox`/`fish`, perl `system`, `os.system` | 33 | 50 | same | MISSED |
| `c1-shellcopy.py` | embeds a copy of `/usr/bin/xdg-mime`'s text, runs it with each host shell | 33 | 16 (fresh 60) | same | MISSED |
| `c1-table.py` | label table keyed by the fixture bytes/env/types; `None` otherwise | **128** | **47** | same | MISSED |
| `c1-bundled3.py` | embeds `/usr/bin/bash` (installed as `sh`, so POSIX mode as the shebang path runs it) **and** the xdg-mime text; writes both into the fixture root and runs the script | **128** | **120** | same | **DRAFT_TARGET_MET** |

`c1-bundled3.py` summary (rc 3):

```
MADO_XDGMIME_DEFAULT: DRAFT_TARGET_MET pred=PRED-C1-r92-v1 rev=draft:…/forge/c1-bundled3.py
  base_rev=d992ef74… cases=128 correct=128 b=16/16 d=39/39 f=21/21 g=6/6 m=36/36 s=10/10 answered=128/128
  fresh=120/120 fresh_seed=2322750778 mutants=0 killed=0 crashed_not_killed=0 oracle_agree=128/128
  do_nothing_correct=33 naive_mimeapps_correct=44 glib_resolver_correct=59 base_tool_correct=0 base_tool=absent
  tool_sha256=8a725d3a…244b
```

The tool is 1,659,682 bytes; it contains no domain model at all. It answers every frozen case and every fresh case
because it *is* xdg-utils' own script running on a shell it shipped. The declaration's control wording
(`claims-declaration-r92.md:59-60`, "a shell-out forgery (calls `/usr/bin/xdg-mime` — hidden by the sandbox)") is
literally true — that forgery scores 33 — but the sandbox's universal claim (`:23-24`, "hides xdg-utils, every shell
binary and the lane repository") is false for the class: it hides the host's copies, not a copy the tool carries.
The label-table forgery confirms the other half: the frozen case leg alone cannot distinguish a table (128/128); only
the fresh leg does (47/120), and the fresh leg cannot distinguish a table from a shipped interpreter (120/120).

What actually stands against this class at measurement is not the sandbox but the **mutant list**: the frozen C1
mutants are a hand-written list of 39 domain beliefs (`gen-c1-mutants-r92.py`), each `find` must occur exactly once
in the measured bytes (`c1-r92-xdgmime-default.py:265-267`), and each mutant must produce a *well-formed wrong
answer* (`killed == mutants`). The generator refuses bytes that do not contain all 39 anchors, so a cheat submitted
*as the candidate* would have to embed the 39 anchor strings too; if it puts them in dead code, its 39 mutants
survive and the predicate misses it; if it makes them live, they are a real model of the 39 beliefs, which is the
intent. That is the load-bearing defence — not the shell mask. Say so in the declaration.

Smallest safe correction (either is enough, both are cheap):
1. Add a bytes clause to `PRED-C1-r92-v1` and check it in the counter before scoring: the measured tool is at most
   64 KiB, contains no ELF/Mach-O/PE magic (`\x7fELF`, `MZ`, `\xcf\xfa\xed\xfe`), and no base64/hex run longer than
   8 KiB that decodes to such magic. The honest candidate is 29 KiB; the forgery is 1.66 MB. One `len(tool_bytes)`
   and a `b"\x7fELF" in tool_bytes` plus a decoded-blob scan.
2. If no bytes clause is wanted, move the sentence from "the sandbox hides … every shell binary" to the round's
   *named limits* ("the sandbox hides the host's shells and xdg-utils; a tool that ships its own interpreter is
   rejected only by the mutant anchors") and add this forgery to the pre-freeze control receipts as a *known
   MET-scoring control* — which the current control clause (`each control … fewer than the case count`) cannot host,
   because it scores all of them. That is the tell: the clause as written can only hold controls that are not
   proxy-complete.

---

## 4. C2's battery body is quotable — met=32/32, and the new classes have no held-out leg

`quality/counters/c2-r92-gate-defects.py:192` materialises fixture *i* under `<work>/b%03d`, and
`run_check` (`:94-102`) invokes the check with no sandbox: `cwd` is inherited (the lane when the counter is run
from the lane) and the environment is only `PATH/HOME/LC_ALL/GIT_CONFIG_NOSYSTEM`. The check can therefore read
`.ufo/waves/round-92/controls/gate-defects-battery-r92-l1.json`, and the fixture index is in its own `--repo`
argument. I wrote `c2-quote.py`: it reads the battery, takes `fixtures[int(bNNN)].expect`, and prints exactly the
stored `rc`, SR-id lines, `contains` strings, summary and line padding — no gate logic. DRAFT run (rc 3,
battery `cc0b793d…`):

```
MADO_GATE_DEFECTS: DRAFT_TARGET_MISSED pred=PRED-C2-r92-v1 rev=draft:…/forge/c2-quote.py
  fixtures=32 met=32 F1=9/9 F2=5/5 F3=3/3 F4=3/3 F5=4/4 P=8/8 selftest=ok:SEAT_REPORTS_SELFTEST: checks=1 failed=0
  mutants=0 killed=0 base_met=8 always_ok_met=3 always_refuse_met=12 r91_counter=NOT_MET
r91: MADO_SEAT_REPORTS: SETUP_ERROR mutant K01: find occurs 0 times
```

The two built-in control shapes through the same counter (rc 3 each):
always-OK `met=3` (F3=1/3, P=2/8 — the one clean-round F3 fixture and the two P fixtures whose expected stdout is
only a summary line), always-refuse `met=12` (F1=9/9, F4=3/3; every F1/F4 expectation is `rc=2` plus one of the
two substrings, so a tool that refuses everything with that message meets all twelve). Base check `met=8`. So the
new F1–F5 behaviour is covered by 32 on-disk fixtures whose
expectations the check can read, and by **no fresh leg**: `PRED-C2-r92-v1` has none, and the round-91 fresh
generator's vocabulary (R91MResidC2 §4) contains none of F1–F5 (no symlinked dispatch, no duplicate `--round`, no
spaced/newline/non-UTF-8 seat name, no FIFO, no escaping parent link). The only held-out pressure is the round-91
leg, which exercises the *old* rules.

What saves the full predicate today is mechanical, not semantic: the r91 leg applies its 55 frozen mutants to the
measured bytes, and my quote tool does not contain those anchors, so the r91 counter returns SETUP_ERROR (above) and
the r92 counter maps that to `r91_counter=NOT_MET`. A tool that implements the round-91 gate honestly (passing 59
set rows, 55 mutants, 60 fresh) *and* quotes the round-92 battery for the five new classes would pass every leg
except its own frozen mutants (17 in the current generator); whether it survives those depends on where the L1
anchors them.

Smallest safe correction: give C2 a held-out leg of its own — a round-92 fresh generator over exactly the F1–F5
vocabulary (symlinked dispatch at wave 1/2/all; duplicate and triple `--round`; spaced/newline/non-UTF-8/tab seat
names; FIFO dispatch worktree and `--all`; parent/grandparent symlink leaving the repo and a sibling with the repo
prefix), expected results derived from the generator's own writes (not from running the check), seeded by the
measured check's sha256 — and/or run the check in the same bwrap sandbox C1 uses (`--tmpfs lane`, `--unshare-net`)
so the battery is unreadable. The fresh generator is the stronger fix: it also tests the *new* rules, which is the
only thing the claim is about.

---

## 5. Sandbox reachability — what actually holds (C1)

Probe run under the counter's own `sandbox_argv()` (bwrap `--ro-bind / /`, masks, lane tmpfs, `--unshare-net/pid`):

| vector | result |
|---|---|
| `/usr/bin/xdg-mime` exec / read | `PermissionError: [Errno 13]`, `stat` size 0 (masked with `/dev/null`) |
| `/bin/sh -c`, `/usr/bin/bash -c`, `shell=True` | `PermissionError … '/bin/sh' / '/usr/bin/bash'` |
| `/usr/bin/env sh -c`, `env -S sh` | rc 126, `env: 'sh': Permission denied` |
| `sh` via PATH | `PermissionError … 'sh'` (PATH=/nonexistent) |
| busybox | absent on the host; masked if present |
| perl `system("echo hi; echo bye")`, backtick pipe, `system('/bin/sh',…)` | no shell reached (empty output / no-op) |
| python `os.system` | 32512 (shell exit 127) |
| lua `os.execute('echo hi; echo bye')`, `io.popen` | no shell reached (nil pipe) |
| nested `bwrap --dev-bind / / -- /usr/bin/bash` | `bwrap: execvp /usr/bin/bash: Permission denied` |
| lane repository | empty listing (tmpfs) |
| pacman cache | readable, but contains **no** bash and **no** xdg-utils package (497 entries; only `-Ql`/man pages carry xdg-utils) |
| **bundled interpreter** | **works** — see §3 |

So the mask is sound for the host's material, `/usr/bin/sh -> bash` is caught because the mask uses
`os.path.realpath`, and the only escape found is the one the tool carries itself. (`/usr/bin/perl`, `/usr/bin/gawk`,
`/usr/bin/python3`, `/usr/bin/lua` remain reachable; none of them can start shell text without `/bin/sh`.)

---

## 6. Predicate text vs counter code vs receipt label, clauses, separability, axis naming, the round-91 leg

6.1 **Same sentence?** C1: the declaration (`:22-31`) and the counter docstring (`:1-20`) are substantively the
same; the counter adds how the tool is run ("fixture tree + whole environment + working directory = the fixture
root + the MIME types asked") and the crash-only annotation "(QUALITY 148)" — the declaration omits both. C2: the
declaration (`:44-53`) and the counter docstring (`:4-14`) agree on every conjunct (fixtures/rc/ids/contains/
summary/fields/lines/ASCII/timeout, selftest `checks=N failed=0`, mutants fewer-or-selftest-change, controls, r91
leg). No receipt exists yet (`receipts/` holds census/draft/sources only), so the receipt label cannot be compared;
both counters print `pred=PRED-C1-r92-v1` / `PRED-C2-r92-v1`, matching the declaration's label. The receipt prefix
the counters print (`MADO_XDGMIME_DEFAULT:` / `MADO_GATE_DEFECTS:`) is not named in the declaration — worth naming at
the freeze so the receipt is recognisable as the counter's own line.

6.2 **Universal clauses.** C1 "every shell binary" — false for a shipped binary (§3); "hides … the lane
repository" — true; "every frozen case" — currently false for the candidate (§2); "every frozen mutant" — the 39
anchors are checked against the candidate's bytes before scoring, and **one is stale today** (`M32`, §2b): the
counter stops with `SETUP_ERROR`, so the leg is not merely weak, it currently cannot run. C2 "every fixture of the
frozen battery" — quotable (§4); "the round-91 *frozen* C2 counter" — false, the code is read from the working
tree (§6.6).

6.3 **The target a do-nothing control reaches.** C1: `do_nothing_correct=33/128` (25.8 %; groups d 20/39, m 8/36)
and `naive_mimeapps_correct=44/128`; the declaration's control clause only requires `< cases`, so 33 or 44 or 127
would all pass. C2: base `8/32`, always-OK `3/32`, always-refuse `12/32` (37.5 %). The clauses are true but weak;
they cannot express "a control that reaches the frozen leg entirely" (the label table, 128/128), which is why the
do-nothing bullets at `:59-62` are evidence outside the predicate rather than part of it.

6.4 **Axis naming.** C1 = coverage is right in the lane's own sense: it is a capability acquisition (before: no
lane tool models `defapp_generic` — `git grep -l defapp_generic d992ef74 -- tools corpus` is empty; `tools/mado-
xdgmime.py` absent at base; `tools/mado-mime.py` present). The premise that xdg-open uses this path checks out:
`/usr/bin/xdg-open:988-991` (`open_generic_xdg_mime` → `default="$(xdg-mime query default "$filetype")"`, called
from `open_generic` at `:1015`/`:1085`). C2 = operability is right: the claim is the gate's behaviour (base 8/32 →
32/32). Caveat: C1's Count is a capability count, not the SCORECARD's admitted-note reachability formula; the
declaration already labels it "(capability acquisition)", so no fix, but the SCORECARD row for round 92 must use
the same phrase or the coverage axis will look like it moved on the rubric's own metric.

6.5 **Separability.** C1's counter reads only `<rev>:tools/mado-xdgmime.py` (`:62-75`, `:212-216`) plus the base
`tools/mado-mime.py` and the pinned controls/oracle/fuzz/cases — no C2 file. C2's counter reads
`<rev>:quality/check-seat-reports.py` (`:173`) plus the r91 leg (`:247-252`), which reads the *working-tree*
`quality/counters/c2-r91-seat-reports.py` (relative path, `cwd=lane`), the pinned r91 set/mutants, the lane's git
history (8 revision rows) and `quality/check-receipt-presence.py` at the measured rev. The declaration's
"Each counter reads only its own file at the measured revision" (`:64-66`) is therefore false for C2. Separability
in the *dependency* sense still holds (neither counter reads the other's file), and at the current tree the r91
counter is identical to `HEAD` (`git diff --stat HEAD -- quality/counters/c2-r91-seat-reports.py` empty), so the
defect is latent, not active. The literal cross-commit runs are not yet possible (no round-92 commits exist); at the
round-91 pair the mechanism the declaration relies on is the same: `git cat-file -e
54a0683c:quality/check-seat-reports.py` → rc 128 (absent) and `git cat-file -e 0e09349e:tools/mado-xdgmime.py` → rc
128, so each counter at the other's round-91 commit would print `SETUP_ERROR` — which is what the round-91 SCORECARD
row records for C2 at `54a0683c`.

6.6 **Is the round-91 leg frozen?** Its *data* is (set `9a05fa8a…`, mutants `7cf06df7…`, both sha-pinned in
`r91-c2-argv-r92.json` `d21b1979…`), its *code* is not: `c2-r92-gate-defects.py:247` executes
`r91_argv[0]` = `"quality/counters/c2-r91-seat-reports.py"` resolved against the lane working tree, and there is no
`--expect-r91-counter-sha256`. Any working-tree edit to that counter (or to `quality/check-receipt-presence.py`
when the leg is run in draft mode, which the r91 counter reads from `HEAD`, `c2-r91-seat-reports.py:323`) changes
the C2 result without changing any pinned byte. Fix: resolve the r91 counter from `<rev>:` (or pin its sha and
fail setup on mismatch), and read `check-receipt-presence.py` from `a.rev` in every mode.

6.7 **Does an anchor change make it SETUP_ERROR?** Not at the r92 level. The r91 counter validates every mutant's
`find` against the measured bytes and returns 2 with `MADO_SEAT_REPORTS: SETUP_ERROR mutant K01: find occurs 0
times` when the candidate no longer contains an anchor; the r92 counter then only looks at the line's second token
(`c2-r92-gate-defects.py:250-252`) and records `r91_counter=NOT_MET`, so the r92 verdict is `TARGET_MISSED` (rc 1),
not `SETUP_ERROR` (rc 2). Observed three times in my drafts (§4). This conflates "the measured tool regressed the
round-91 rules" with "the harness pins no longer match the measured bytes"; the second is a setup error and should
be reported as one. The current candidate is safe: all 55 r91 anchors occur exactly once in
`build/check-seat-reports.c2.py` (sha `176fc066…`), and the standalone leg DRAFT-run (rc 3) is
`MADO_SEAT_REPORTS: DRAFT_TARGET_MET … expectations=59 met=59 fresh=60/60 fresh_seed=393199718
selftest=ok:checks=23 failed=0 mutants=55 killed=55 base_met=0 always_ok_met=5 always_missing_met=0
receipt_presence_met=11 check_sha256=176fc066…663a`.

6.8 **Draft-path constraints (documentation, not defects).** `--draft-tool` / `--draft-check` score the draft
bytes as the candidate but still validate the *frozen* mutants against them (`:270-271` / `:233`), so any
draft tool other than the frozen candidate needs an empty mutants file — exactly what the w1 draft rule says, but
worth stating in the counter help. C2's draft mode additionally forwards `--draft-check` to the r91 leg, which
cannot apply its 55 anchors to a non-derived check; a draft check that lacks them always shows `r91_counter=NOT_MET`.
The real C2 candidate does contain them (§6.7), so this only affects throwaway draft tools.

---

## 7. Concrete fixes, ranked

1. **C1 / freeze blocker** — reconcile the candidate and the frozen cases (§2). Either implement the BRE
   metacharacter pass-through and the gawk `-v` backslash processing (the oracle is ground truth) or drop `f14`,
   `f17`, `g05`, `g06` before the freeze and correct the declaration's case count and "every frozen case" wording.
   **Then regenerate the mutants** (§2b): update `M32` in `gen-c1-mutants-r92.py` to the refactored glob test,
   regenerate `xdgmime-mutants-r92-l1.json` from the frozen candidate bytes, and re-pin its sha. Re-run the candidate
   DRAFT immediately before freezing; the file changed four times during this review.
2. **C1 / predicate** — add the tool-bytes clause (≤64 KiB, no ELF magic, no >8 KiB decode-to-ELF blob) to
   `PRED-C1-r92-v1` and the counter, or move the sandbox sentence to named limits and record the bundled-interpreter
   forgery as a known MET-scoring control (§3). Also fix the stale premise: `56/123` → the measured `59/128`
   (`claims-declaration-r92.md:18-20`), and `cases=128` in the declaration.
3. **C2 / held-out** — add a round-92 fresh generator over the F1–F5 vocabulary (seeded by the check's sha) and/or
   sandbox the check (hide the lane + battery) so the fixture index/expectations are not readable (§4).
4. **C2 / Count** — `claims-declaration-r92.md:55` says "base `d992ef74` → all"; the measured base control meets
   **8/32** (base_met=8). Write "8/32 → 32/32" so the "before" is a number.
5. **C2 / r91 leg** — read the r91 counter from `<rev>` (or pin its sha), and map its `SETUP_ERROR` first line to
   the r92 counter's own setup error instead of `NOT_MET` (§6.6–6.7).
6. **C2 / wording** — the declaration's separability sentence must name the r91 leg as an external read, or the
   leg must be pinned so the sentence becomes true (§6.5).
7. **C1 / wording** — name the receipt prefix in the declaration, and cite the crash-only QUALITY-148 rule that
   the counter docstring carries and the declaration does not (§6.1).

---

## 8. What holds (verified positively, so a freeze does not need to re-litigate it)

- **Oracle reproduces every stored label**: `oracle_agree=128/128` in all nine C1 draft runs; the fresh leg is
  labelled by the same oracle (120/120 for the honest candidate and for the bundled forgery).
- **C1 before-state**: `tools/mado-xdgmime.py` absent at `d992ef74`; `tools/mado-mime.py` present;
  `git grep -l defapp_generic d992ef74 -- tools corpus` empty; xdg-open 1.2.1 really calls `xdg-mime query default`
  (§6.4).
- **C1 case groups** are populated (b 16, d 39, f 21, g 6, m 36, s 10) and the honest candidate's fresh leg is
  **120/120**; the only frozen-case gap is the four refusals of §2.
- **C2 candidate**: DRAFT `met=32/32` (F1 9/9, F2 5/5, F3 3/3, F4 3/3, F5 4/4, P 8/8), `selftest=ok:checks=23
  failed=0`, controls 8/3/12, and the r91 leg TARGET_MET (§6.7). Anchor integrity: C2 17/17 and r91 55/55 `find`
  strings occur exactly once in the current candidate; C1 is 38/39 (M32 stale, §2b).
- **Host sandbox**: all host shells and xdg-utils binaries are masked (§5); the pacman cache carries no bash or
  xdg-utils package.
- **The controls the declaration names do work as stated**: shell-out 33/128 (fresh 50/120), label table 128/128
  (fresh 47/120 — the fresh leg defeats it, exactly as `claims-declaration-r92.md:59-61` says), naive 44, GLib 59,
  base absent 0; C2 always-OK 3, always-refuse 12, base 8 (all < 32).

## 9. Dead steps, installs, scratch

- Dead step (expected, not a defect): the first C2 draft batch aborted with
  `MADO_GATE_DEFECTS: SETUP_ERROR sha256 mismatch …/gate-defects-battery-r92-l1.json: 73ae3bde… != c923ac17…` —
  the battery was regenerated by another seat at 23:01:29 while I was reading the earlier hash; it moved again at
  23:13:30 (27 → 28 → 32 fixtures, sha `cc0b793d…`). Re-ran with the current pin (32 fixtures), and the mutant-anchor
  demonstration above uses a one-mutant scratch file for M32. This is the live control churn the freeze will end.
- Dead step: `python3 -I build/mado-xdgmime.c1.py --selftest` exits 2 (`error: the following arguments are
  required: types`) — the C1 candidate has no `--selftest`; `PRED-C1-r92-v1` does not require one, so no finding.
- Harness iterations (not lane defects): my first bundled forgery scored 126/128 / 118/120 because it invoked
  `bash script` (non-POSIX mode) and mapped an empty stdout to `None`; installing the same bytes as `sh` and copying
  the oracle's `run_one` parsing (`xdgmime-oracle-r92.py:63-70`) gave 128/128 / 120/120. That difference is itself
  evidence that the oracle's parsing (empty stdout → `None`, one trailing newline stripped, empty string preserved
  when stdout is `"\n"`) is the exact contract the candidate must match.
- Installs: none. pacman untouched (read-only `-Ql` only); no network.
- Scratch `S=/fast/scratch/hyaku/mado-r92/R92MCritic` (forgeries, probe scripts, logs) deleted on exit; all
  evidence quoted above is in this file. Only lane write: this report.
