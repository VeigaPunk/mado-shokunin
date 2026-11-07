# R94MCritic — falsification of `claims-declaration-r94.md` (C1, C2) before the freeze

Seat: R94MCritic (critic, leaf). Round 94 / hyaku run 15 / attempt 1, wave w1. Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `a3de997289014e7dbf1d73ae206be1d6f8cdadd0`. I read no frozen input that does not exist yet (cases / mutants /
kill-sets / counters were still absent when this review ran), so every number below is a **DRAFT** run: labels say DRAFT,
nothing here is a measurement of a claim, and nothing was written under `.ufo/waves/round-94/receipts/`.

Pins I verified before using them (all match the seat context):

```
4e7fff9e…fd88  tools/mado-xdgmime.py            2532ccb5…1a5e  tools/mado-mime.py
2d6f1219…a61b  quality/check-selftest-strength.py  00befb3e…16f9  quality/selftest-kills/check-seat-reports.json
0700915a…d63e  .ufo/waves/round-94/build/mado-mimeglob.c1.py   9c4337b3…6b11  controls/mimeglob-oracle-r94.c
```

## Axes named

| axis | counting rule (as I used it) | this round's move |
|---|---|---|
| **coverage** (claim surface) | correct (type, uncertain) answers / frozen cases, plus fresh-leg and host-leg agreement — C1 counter | name → type is genuinely new: no lane tool and no corpus note answers it (§4.1) |
| **operability** (C2) | selftest checks whose single-check neutralisation the gate flags, /29 | 2 of the lane's tools get a kill-set; 34 of 36 do not (§C2-F2) |
| **provenance / identity** | frozen inputs pinned by sha256, candidate = frozen candidate | pins are complete for every C1 input; the *controls* are not pinned (§C1-F4) |
| **separability** | each claim's counter at the other claim's revision | holds; both counter file sets are disjoint (§5) |

## 1. C1 — what the draft predicate can and cannot reject

**Q1.1 Can a do-nothing / naive-extension-map / label-memorising table / oracle-exec meet PRED-C1-r94-v1?**
do-nothing and the naive map: no (they are conjunct (v), and on my fixtures the naive map is right on 5/12 and 6/12
names respectively — DRAFT). Label memorisation: no, the fresh leg (ii) builds *random layouts*, so a table over the
frozen names knows no type for a new glob; the host leg (iii) is a second independent surface. **Oracle-exec: yes.**
Nothing in the predicate rejects it — see C1-F2, which is the strongest counterexample I found.

**Q1.2 Is the frozen set's class coverage load-bearing?**
Not by anything the predicate measures. Clause (i) reads “the frozen set holds both modes (text and cache) and every
class named in the case file” — the class list is *read from the case file*, so the clause is a tautology no data can
falsify (C1-F1). Empirically at least one class is control-dead once the mutant leg is ignored (C1-F3): `fgets`.

**Q1.3 Is the axis named by the surface (coverage: name → type) and unmoved at base?** Yes, and I checked the negative:
`git show a3de9972:tools/mado-mimeglob.py` → `fatal: path … does not exist`, rc 128; `grep -l "def selftest" tools/*.py`
lists no name→type tool (`mado-mime.py` and `mado-xdgmime.py` are type→app in their own docstrings);
`grep -ril "globs2\|mimeglob\|g_content_type_guess" corpus/knowledge/` → no file. So C1 is a real new surface, not a
second authority over an existing one. The declaration should still name the *counting rule* (it is the counter's
case fraction, not the SCORECARD's note-navigation rubric) so the axis row cannot be read as the fleet rubric.

### C1-F1 — PRED-C1 (i)'s class clause is a tautology (repair: freeze the class list in the predicate)

Counterexample: a frozen case file containing only classes `simple`, `nomatch`, `slash` and `mode` satisfies
“every class named in the case file” verbatim; the clause cannot fail, so the 21-class list in the seat schema carries
no force at measurement.
Evidence: declaration, PRED-C1-r94-v1 (i), text quoted above; the seat schema's class list is the only other place the
21 names occur, and the predicate does not read it.
Impacted axis: coverage (the claim's coverage is asserted, not measured).
Smallest safe correction (freeze-ready): replace “every class named in the case file” with the explicit list and a
count — “…and holds, for each of the 21 classes `dirs mode literal simple full fold cs deep weight dupe order multi
nomatch slash bytes fgets v1 noglobs cachefmt mixed`, at least 6 cases; the counter prints `classes=21/21` and fails
(`TARGET_MISSED`) on any class with <6 cases or any class name it does not know.”

### C1-F2 — no conjunct rejects a tool that execs GLib / the oracle (repair: a static conjunct plus a PATH-isolated leg)

Counterexample: `.ufo/waves/round-94/w1/R94MCritic/evidence/wrapper-tool.py` — 40 lines, `subprocess.run([ORACLE, *names])`
on the compiled oracle, same CLI, same JSON. DRAFT result: **0 mismatches on 12 text-fixture names, 0 on 9 cache/mixed
names, 0 on 300 names across 20 seeded random layouts — 321 names in all** (`evidence/transcript.txt` §D). It satisfies (i), (ii), (iii)
and (v) *by construction*, and (iv) degenerates: a wrapper has no modelled rule to flip, so the mutant leg can only
mutate argument plumbing (e.g. drop `XDG_DATA_HOME`) — those are killed trivially, so (iv) passes too. The only thing
standing between this and the claim is `--expect-tool-sha256`, i.e. the L1's choice of candidate bytes — a provenance
lock, not a property of the tool. **Behavioural conjuncts can never separate a re-implementation from a wrapper**
(it is correct wherever the oracle is), so the predicate needs a structural conjunct.
Impacted axes: coverage (the capability would be “call GLib”, which the lane already does not accept elsewhere),
provenance.
Smallest safe correction (freeze-ready) — add conjunct (vi) and print it in the verdict line:

```
(vi) static: the counter parses tools/mado-mimeglob.py with ast and asserts
     (a) no import of subprocess|socket|multiprocessing|pty|shutil|urllib|http|xmlrpc|ctypes.util.find_library("gio…");
     (b) no attribute chain os.system|os.popen|os.exec*|os.spawn*|os.posix_spawn*;
     (c) every ctypes.CDLL/CDLL target string is libc (the tool may use libc for fnmatch(3)/setlocale);
     (d) the source bytes contain none of "g_content_type_guess", "gio ", "xdg-mime", "mimetype", "file --mime";
     runtime: every case (i) is re-run with PATH=<an empty scratch dir> and must answer identically.
     Print `static_no_external_resolver=ok|FAIL`; FAIL ⇒ TARGET_MISSED.
```
(The candidate passes (a)-(d) as frozen: it imports argparse/ctypes/json/os/struct/sys and loads libc only.)

### C1-F3 — no minimum on the mutant set and no class→mutant link (repair: counts + a unique-killer matrix)

Counterexample (DRAFT, reproducible in `evidence/repro.sh` §C): fixture `dh/mime/globs2` =
`50:text/x-lf:*.lf:` + `x`×240 + `,cs` (262 bytes, one line). Oracle and candidate: `A.LF` → `text/x-lf`/0. The
candidate with the fgets rule flipped (`nl = data.find(b"\n", i, i + 254)` → `nl = data.find(b"\n", i)`) → `A.LF` →
`application/octet-stream`/1. So the class has a live discriminator — but **the naive map with folding also answers
`text/x-lf`/0**, and the do-nothing control is wrong on every non-octet-stream case anyway. With no mutant for the
fgets rule, class `fgets` is dead weight that the predicate still counts as covered. The predicate says only “every
frozen mutant … makes at least one frozen case wrong”, which a one-mutant file satisfies; the ≥40 rule list lives in
R94MMutC1's seat prompt, which is not the predicate.
Impacted axis: coverage (a class can silently retire while the verdict stays TARGET_MET).
Smallest safe correction (freeze-ready): add to (i)/(iv): “the frozen mutant file holds ≥40 mutants with
`equivalent_not_counted` ≤ 10, and the counter builds a `class × mutant` kill matrix and prints
`unique_killer_classes=K/21`; a class with no case that is the *only* killer of some frozen mutant is a miss unless the
declaration names it in a frozen `classes_without_own_mutant` list (max 3).”

### C1-F4 — the controls are prose, so their strength is unpinned (repair: freeze the control sources with sha256)

Counterexample: control (v) says “the naive extension map (last `.ext` → highest-weight type in the dirs' `globs2`,
uncertain 0)”. It does not say whether the extension is case-folded. On the same 12 names (`evidence/transcript.txt`
§C) the exact variant equals the oracle on **5/12**, the folded variant on **6/12**, and on the `fgets` discriminator
above the exact variant is *wrong* (so the case kills the control) while the folded variant is *right* (so the case
kills nothing). A control whose bytes are chosen after the data are visible can be made as weak as needed, and (v) only
requires the control to *miss*, so weakness never shows.
Impacted axes: coverage, discernment.
Smallest safe correction: freeze each control as a file (`controls/c1-controls-r94.py` with `--mode do-nothing|naive`,
pinned by sha256 in the counter's `--expect-controls-sha256`), state in the declaration that the naive control folds the
extension with ASCII lowercasing and takes the highest weight (first on ties), and require in (v) that the naive control
is right on at least one class and wrong on at least `simple`, `deep`, `cs`, `literal` (i.e. the control is strong
enough to be interesting).

### C1-F5 — the host leg is not reproducible without the host DB hashes (repair: print them)

Conjunct (iii) runs a frozen name list against the *live* oracle under the host environment. The names are pinned, the
databases are not: `/usr/share/mime/mime.cache` and any `~/.local/share/mime/mime.cache` can change between freeze and
measurement and the leg would silently lose coverage. DRAFT: on this host the leg ran in **cache** mode over 220 names
synthesised from `/usr/share/mime/globs2` (40 patterns × 3 case variants + 100 non-matches): **0 mismatches**.
Smallest safe correction: the counter prints `sha256` of every host `mime.cache`/`globs2` it actually loaded, and the
verdict line carries `host_db=<sha256 prefix of /usr/share/mime/mime.cache>`; no equality pin (it is a live leg), but a
changed hash is visible in the receipt.

## 2. C2 — what the draft predicate can and cannot reject

**Q2.1 Is 0/29 → 29/29 reachable by a do-nothing or by forgery?**
do-nothing: no. It flags iff the selftest result line changes; with a check neutralised the line is still
`checks=12 failed=0` and no FAIL lines are printed (`transcript.txt` §F), so it flags 0 — as declared. **Forgery: yes,
with two kills for a twelve-check tool.** DRAFT (`transcript.txt` §E, driver `evidence/forge2.py`):

```
X1 = replace `        if mime in (b"--help", b"--manual"):` by `        return None, 0\n<same line>`  -> 9 FAIL labels
X2 = replace `        out = self.defapp_generic(mime)` by `        return b"a.desktop", 0`           -> 6 FAIL labels
kill-set = 2 kills, must_fail = those two sets (union = all 12 labels)
gate on the unmodified tool : SELFTEST_STRENGTH: OK … kills=2 held=2 survived=0 wrong_check=0     (rc 0)
12 single-check neutralisations, gate each time: WEAK rc 1                                          -> 12/12 flagged
```
So the 29/29 count is satisfiable by ~2 kills per tool and proves nothing per check: it is a matching-set property, not
29 distinct assertions. The gate's own docstring intends the opposite (“weakening any check that catches it is seen”); a
kill naming *all* checks defeats that intent, because every check is then *required* to fail.
The loosenings in conjunct (iii) are what actually force discrimination — I verified the pair:
`q("text/plain") == ("a.desktop", 0)` widened to `q("text/plain") in (("a.desktop", 0), ("c.desktop", 0))` →
under the 2 universal kills the gate prints **OK rc 0 (missed)**; under a kill whose `must_fail` is exactly
`["m03 list: second id installed"]` it prints **WEAK rc 1 wrong_check=1 (caught)**.
Impacted axis: operability (the capability is real but the count overstates it), discernment (the SCORECARD row would
read “29/29”).
Smallest safe correction (freeze-ready), pick one and freeze it:
(a) **singleton kills** — add to (i): “for each of the 29 labels L there is a kill with `must_fail` exactly `[L]`
(`must_fail` a string or a 1-element list), the 29 `find` strings are distinct, and the counter prints
`singleton_labels=29/29`; a label with no singleton kill may be declared in a frozen `residual` list, printed, and
subtracted from both sides of the before→after”; or
(b) keep list-kills and restate the claim honestly: “every label is named by some frozen kill's `must_fail` set” and
drop the per-check count from the before→after; and in either case widen (iii) from “≥6 hand weakenings per tool” to
“≥1 widening per label, i.e. 29 panel entries, each a loosening (not a neutralisation) of that label's assertion”.

**Q2.2 Is “gate unchanged” + two JSON files a real operability move or bookkeeping?**
For: the routed defect 2 of round 93 (`corpus/lessons/round-93-verifier-spotcheck.md:180-182`) names exactly this gap —
the gate is wired for `quality/check-seat-reports.py` only — and a kill-set is not bookkeeping: it is a committed,
mutation-tested statement about one tool's assertions, and the gate turns it into a verdict (OK/WEAK, rc 0/1). The
instrument exists and fails correctly (my pair above shows it catching a widening the 2-kill forgery misses).
Against: no lane *code* changes, so nothing new is executable; the deliverable is data for an instrument that already
existed; and after the round 2 of the 36 lane scripts that define `def selftest` are guarded
(`grep -l "def selftest" tools/*.py quality/*.py | wc -l` → 36), while routed defect 2 lists seven tools and stays open for five of them —
`tools/mado-verify.sh`, `tools/mado-portals.py`, `tools/mado-mako.py`, `quality/check-receipt-presence.py`,
`quality/check-selftest-strength.py` itself — plus, after this round, the new C1 tool (C2-F2).
Verdict: a real but narrow operability move — it is the first *reusable* kill-set beyond the round-93 one, and the
capability row must say “guards three tools”, not “the lane's selftests are guarded”. See C2-F2/F3.

**Q2.3 Separability of C1/C2?** Holds (see §5).

### C2-F2 — the round lands a new unguarded selftest (repair: extend the C2 kill-sets to the C1 tool, 29 → 44)

Counterexample: C1 lands `tools/mado-mimeglob.py` with a **15-check** selftest
(`python3 -I …/mado-mimeglob.c1.py --selftest` → `MADO_MIMEGLOB_SELFTEST: checks=15 failed=0`, rc 0 — DRAFT), and its
`failed = [n for n, ok in checks if not ok]` line is at candidate line 549, i.e. exactly the neutralisable shape. The
round's own C2 claim guards `mado-xdgmime.py` and `mado-mime.py` and leaves the newest selftest unguarded at birth — the
same routed defect, one round later. The tool lands in C1's commit, *before* C2's, so C2 can legally pin it.
Smallest safe correction: C2's kill-sets cover three tools (`mado-xdgmime.py` 12, `mado-mime.py` 17,
`mado-mimeglob.py` 15), predicate counts become 44, and the capability row reads “guards the three tools whose selftests
the default-application plane depends on”; if the L1 prefers 29, the new tool must be named in the named-limits block
with the reason (it is *less* defensible than guarding it: the tool is the round's own new surface).

### C2-F3 — the gate cannot guard itself (name it, or add a self-kill-set)

Counterexample: `quality/check-selftest-strength.py` has its own `--selftest` (11 checks, in every harm receipt) and no
kill-set; the C2 claim's conjunct (vi) only checks that it exits 0. A weakened assertion inside the gate's own selftest
is exactly the class of defect the round is fixing, and it would make every other kill-set's verdict untrustworthy.
Smallest safe correction: either add `quality/selftest-kills/check-selftest-strength.json` (11 checks, same schema) and
say so, or write into the named-limits block: “the gate's own selftest is not kill-set-guarded (self-application gap);
its 11 checks are only re-run”.

### C2-F4 — “0/29” is not something the counter can print (state the measurement's shape)

The C2 counter at the base/C1 revision stops `SETUP_ERROR rc 2` because the kill-sets are absent (verified: at base
`quality/selftest-kills/` holds only `check-seat-reports.json`). So the “before” of `0/29` is the **do-nothing control's**
count (verified §F: it flags nothing), not a counter measurement. The declaration should say
“before = the do-nothing instrument on the same 29 neutralisations, 0/29 (it is control (v)); after = the gate, 29/29”
so no one reads the before as a run of the counter.

## 3. What stands (do not over-correct)

1. The surface is new and the candidate is correct on everything I probed (DRAFT): 12/12 text-mode names,
   7/7 cache-mode, 2/2 mixed (a globs2-only dir next to a cache dir is correctly ignored), **85/85** names over 5
   random cache layouts built with `update-mime-database`, **220/220** host-mode names, and the `dirs`
   classes (`XDG_DATA_HOME` set-empty; `XDG_DATA_DIRS` with leading/trailing/double empty elements skip the empties).
   `--selftest` 15/15. Names with `/` and a `*.d/Makefile`-shaped glob agree with the oracle (both basename) — the
   candidate's `g_path_get_basename` is not a divergence on that class.
2. Provenance of the sources is honest on the lines I spot-checked against `receipts/sources-open-r94.txt`:
   `xdgmimeglob.c:643` fgets-255, `xdgmime.c:645-646` caches-only, `xdgmimecache.c:414-415` low-8-bits weight and
   `0x100` cs, `gcontenttype-fdo.c:597-603` trailing `/` → inode/directory uncertain — all as the candidate's docstring
   cites them.
3. The C1 counter's construction is sound where it is specific: `git show <rev>:tools/…` + sha pin, oracle re-run with
   `oracle_drift` → SETUP_ERROR, exit 3 counted as not answered, `crashed_not_killed` distinguished from killed.
4. The C2 counter derives labels from each tool's `checks` tuples and requires `count == checks=N` — correct, and it is
   why the forgery above is visible at all (the labels are enumerable without trusting the kill-set).

## 4. Freeze-ready summary of the repairs (smallest set that closes the counterexamples)

| id | repair | closes |
|---|---|---|
| C1-F1 | replace “every class named in the case file” with the enumerated 21-class list + ≥6 cases each, printed as `classes=21/21` | tautology |
| C1-F2 | conjunct (vi): ast scan (no subprocess/socket/…, ctypes→libc only, no `g_content_type_guess`/`gio`/`xdg-mime` bytes) + PATH-isolated re-run | oracle-exec wrapper (0/321 mismatch in evidence) |
| C1-F3 | ≥40 non-equivalent mutants, `class × mutant` unique-killer matrix printed, ≤3 named class exemptions | control-dead classes (fgets) |
| C1-F4 | freeze the control sources with `--expect-controls-sha256`; pin the naive map's folding | prose controls, 5/12 vs 6/12 |
| C1-F5 | print the host DB sha256s in the host leg | non-reproducible host leg |
| C2-F1 | singleton kills per label (29/29) or restate the count; widen the panel to ≥1 widening per label | 2-kill forgery (12/12 with 2 kills) |
| C2-F2 | add the C1 tool to the kill-sets (44) or name it as residual | new unguarded selftest |
| C2-F3 | name the gate's own unguarded selftest, or guard it (11 more) | self-application gap |
| C2-F4 | state that 0/29 is the do-nothing control's count | misreadable before-value |

## 5. Separability

File sets are disjoint: C1 = `tools/mado-mimeglob.py` + `.ufo/…/round-94/controls/{mimeglob-cases,mimeglob-mutants,
mimeglob-host-names,mimeglob-fresh}*` + `quality/counters/c1-r94-mimeglob.py`; C2 = `quality/selftest-kills/*.json` +
`quality/counters/c2-r94-selftest-kills.py` + `controls/selftest-panel-r94.json`. Neither counter reads the other's
files; C1's tool sha pin is independent of C2's kill-set sha pins; the two tools C2 pins are unchanged this round, so
C2's kill-sets are valid at both revisions. The declared route — C1 measured at its own commit, C2 at its own, C2 at
the C1 commit → SETUP_ERROR because the kill-sets land with C2 — is consistent with the tree at base
(`quality/selftest-kills/` = `check-seat-reports.json` only). If C2-F2 is applied, C2 must still be measured at the C2
commit (after C1), which keeps the order intact; the declaration should say so in one line.

## 6. Not tested / residuals of this review

- I did not run the C1 or C2 counters (they do not exist yet) nor the frozen case/mutant/kill-set files (absent). Every
  number above is DRAFT on fixtures I built; none of it is a claim measurement.
- I did not test cache-mode `__NOGLOBS__`, malformed-cache fallback, or the >10-matches cap; those classes are
  unverified by me and rest on the case seat.
- The 5 random cache layouts I ran are small (5 types each); wide host coverage of GLib's cache quirk-space is the
  fresh leg's job.
- The `fgets` singleton-mutant feasibility claim (C1-F3) assumes the case seat can place `cs` past byte 254 as I did;
  my fixture shows it works and gives a clean one-name discriminator.

## 7. Evidence, tooling, scratch

- Evidence bundle (scripts + transcript, all reproducible read-only against the lane):
  `.ufo/waves/round-94/w1/R94MCritic/evidence/{repro.sh,transcript.txt,wrapper-tool.py,naive.py,forge2.py,forged-kills-xdgmime.json}`.
  `bash repro.sh` exits 0 and regenerates every output quoted here; it writes only under
  `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r94/critic-repro`.
- Installs/upgrades: **none** (gcc, pkg-config, glib2 2.90.1-1, shared-mime-info 2.5.1-2, python3 were already present).
  `update-mime-database` ran only on directories inside my scratch; no host mime directory was touched; no credential
  material read; no real home file name printed.
- Scratch `$HYAKU_SCRATCH/mado-r94/R94MCritic` and the repro scratch were removed after the evidence was copied into
  `.ufo/waves/round-94/w1/R94MCritic/evidence/`.
