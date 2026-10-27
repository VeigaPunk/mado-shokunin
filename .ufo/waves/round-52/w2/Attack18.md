# Attack18 — C1 pointer self-reference laundering

Seat: `Attack18` (leaf, W2 run-52). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`
Base revision: `85d57a818c3707397e21c840b6498b105ba798aa`. Axes named: **coverage** and
**operability** (this seat attacks C1, the operability claim, only). No C2 work.

Verdict in one line: the frozen control's red is **reproduced**; the C1 clause
"non-self resolvable evidence targets" is **not reproduced as implemented** — the check is
literal-path equality plus basename occurrence in target bytes, and six constructions that
resolve the row's accountability to the ledger itself pass with `verdict=TARGET_MET` and
`self_pointer=0`, including one that puts the literal path `quality/tool-ledger.md` inside
the pointer cell. A second, untracked artifact now present at the claim's target path
(`quality/counters/c1-r52-ledger.py`, sha256 `923faf02…`) is **worse**: it does not pass the
frozen base ledger at all and it accepts `./quality/tool-ledger.md` as a non-self pointer.

---

## 1. Bytes attacked (pinned)

| artifact | path | sha256 | note |
|---|---|---|---|
| W1 prototype counter | `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py` | `0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31` | the only counter with receipts, a selftest (53/53) and a harness pass; matches the hash pinned in `w1/C1CounterDesign.md` |
| in-tree candidate, untracked | `quality/counters/c1-r52-ledger.py` | `923faf02cd0c2db374f7757d38ef24fc8381c2882cb3d853882f0fadce1c17d7` | 3652 bytes, mtime `2026-10-27 11:11:48 -0300`, `git status` → `??`; provenance not established by this seat |
| frozen claim | `.ufo/waves/round-52/claims-frozen.md` | — | C1 paragraph |
| frozen predicate/control | `.ufo/waves/round-52/registration.md`, `controls/c1-do-nothing.md` | — | control is 2 rows, 4 cells |

Attacked clause, verbatim:

- `claims-frozen.md`: "a new committed counter distinguishes the production ledger from a
  no-work control of repeated generic self-pointers using unique population, **non-self
  resolvable evidence targets**, and instrument-specific context checks."
- `registration.md`: "It must pass on the existing production ledger at the base revision and
  fail on `controls/c1-do-nothing.md` **specifically for self-pointer/context defects**."

## 2. Reconstructed contract (from the prototype's bytes, not its prose)

Locators in `c1-r52-ledger.py`:

| line | code | effect |
|---|---|---|
| 205–218 | `path_tokens()`: `spans = BACKTICK.findall(cell)`; `if not spans: spans = [split on whitespace]` | **a cell's paths are its backticked spans, or — only when the cell has no backtick at all — its whitespace words.** |
| 332–338 | `qualifying` = tokens that exist in `git ls-tree` at `--rev` **and** whose bytes satisfy `names_basename(body, basename(path))` | "resolvable evidence target" = *the file exists and mentions the basename anywhere* |
| 342–347 | `peer` (token in population, ≠ row path), `circular` (token == `quality/tool-ledger.md` or == row path) removed | the ledger and the row's own file can never be accountable |
| 353–359 | `pointer_self`: for cells 3.., any token with `/` whose string **equals** `ledger_rel` or `path` | the non-self defect is **string equality** on a path-like token |
| 363–369 | `wide_self`: same equality over all cells, only used when `accountable` is empty | |
| 371–385 | `pointer_self` → `self_pointer`; `elif accountable` → prose mention is a `note`, **not scored**; `elif wide_self` → `self_pointer`; else `bad_pointer` | |

So the implemented property is: *no cell contains the literal ledger path (as tokenized), and
some file in the tree mentions the instrument's basename.* It is neither a resolution test
(`resolve(target)` vs `resolve(ledger)`) nor a location test (the `:N` anchor is stripped at
line 216 and never read). Two structural consequences follow, and every finding below is one
of them:

1. **Indirection is invisible**: any distinct path whose bytes are derived from the ledger is
   "accountable", because the ledger names every basename (the counter's own comment says so).
2. **Tokenization is decisive**: one backtick anywhere in a cell hides every bare path in that
   cell from both `pointer_self` and `wide_self`.

## 3. Method

`repro.sh` (full text in §7) clones the lane into scratch at the base revision, adds three
fixture documents (`docs/alias.md`, `docs/mentions.md`, `quality/tool-ledger-copy.md`) and ten
ledger variants that differ from the production ledger in the **pointer cell only** (measured:
`diff` against `quality/tool-ledger.md` is 164 changed lines = 82 removed + 82 added for every
variant except `mentions-desc`, which also appends one sentence to each description). A second, three-row
fixture (`repro-mini`) reproduces the same behaviours without the 82-row ledger. Both counters
are invoked read-only; the prototype is run from its seat path, the candidate from the lane.

Every git operation in a fixture is preceded by a `git rev-parse --show-toplevel` assert
(`repro.sh`, both the clone and the mini fixture). No git or jj command mutates the lane.

## 4. Results

Observed stdout lines are quoted verbatim from this seat's run (fixture rev
`b399b848…`, counter `0fe862f1…`; mini rev `21a2e519…`). Fixture commit ids change per run
because the commits carry timestamps, so a fresh `repro.sh` shows a different `rev=` in the
same lines; every other field is identical.

### 4.1 Positive controls — the check as advertised works

| id | construction | observed | verdict |
|---|---|---|---|
| V1 | production ledger at base, unchanged | `population=82 ledger_rows=82 … self_pointer=0 generic_desc=0 verdict=TARGET_MET` exit 0 | **reproduced** |
| V2 | frozen `controls/c1-do-nothing.md` | `self_pointer=1 generic_desc=1` (+ `dup=1 uncovered=81`) `verdict=TARGET_MISSED` exit 1 | **reproduced** |
| V3 | every pointer = `` `quality/tool-ledger.md` `` | `self_pointer=82` `TARGET_MISSED` | **reproduced** |
| V4 | every pointer = `` `docs/alias.md` and `quality/tool-ledger.md` `` | `self_pointer=82` `TARGET_MISSED` (unconditional pointer-region scan fires) | **reproduced** |

V3/V4 confirm the narrowing described in `C1CounterDesign.md`: naming the ledger **in the
pointer region** is scored whatever else the row names. Everything below defeats that by
changing what "names the ledger" means to the tokenizer or by removing the name from the
region under any spelling.

### 4.2 Falsifiers of "non-self resolvable evidence targets"

Each row below is a full 82-row ledger with `uncovered=0 dup=0 dangling=0 bad_pointer=0
generic_desc=0`, i.e. a ledger the counter declares accountable.

**A1 — one-hop redirect (`docs/alias.md`).** `docs/alias.md` is 84 lines; its entire content
is a title and 82 lines of the form `` - `tools/mado-action-plan.py` -> quality/tool-ledger.md#L32 ``.
Row pointer cell: `` `docs/alias.md` ``.

```
C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET
```

The evidence chain of every row terminates at the ledger, which is exactly the target the
clause forbids; the counter sees none of it. **Not reproduced.**

**A2 — anchored redirect (`docs/alias.md:N`).** Same document, pointer `` `docs/alias.md:3` ``.
`TARGET_MET`, `self_pointer=0`. The `:N` suffix is stripped (line 216) so the anchor cannot
help. **Not reproduced.**

**A3 — byte-identical copy (`quality/tool-ledger-copy.md`).**
`sha256(quality/tool-ledger.md) == sha256(quality/tool-ledger-copy.md)` =
`df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b`. Pointer `` `quality/tool-ledger-copy.md` ``:
`TARGET_MET`, `self_pointer=0`. The clause is satisfied by any path inequality, even when the
target is the same file content. **Not reproduced.**

**A4 — literal ledger path in the pointer cell, hidden by a backtick.** Pointer cell:
`` `docs/alias.md` plus quality/tool-ledger.md `` — the ledger path is **present, unqualified
and literal**, in the pointer region.

```
C1_R52: population=82 ledger_rows=82 … bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET
```

Mechanism: `path_tokens` (line 207) finds the backticked span `docs/alias.md` and therefore
never falls back to whitespace splitting, so `quality/tool-ledger.md` is not a token at all.
The wide scan is blind for the same reason: in `ledger-mentions-desc.md`, where the ledger
path is appended in plain text to 82 descriptions, only **43** rows produce the unscored
`note … names-the-ledger-in-prose` line and **39** produce nothing, because those 39
descriptions already contain a backticked word. This is a tokenizer defect, not a stated
ceiling: the same cell with the ledger path backticked is caught (V4). **Not reproduced —
this is a direct counterexample to the pointer-region rule itself.**

**A5 — mention-only decoy (`docs/mentions.md`).** Content is 82 lines of `The basename
tools/mado-action-plan.py appears in this sentence.` — no function, no evidence.
Pointer `` `docs/mentions.md` ``: `TARGET_MET`, `self_pointer=0`, `bad_pointer=0`. "Resolvable
evidence target" collapses to "a file that contains this basename", which the counter's own
comment anticipates for the ledger but not for a decoy. **Not reproduced.**

**A6 — ledger named in the description, decoy in the pointer cell.** Pointer
`` `docs/mentions.md` ``, description ends `See quality/tool-ledger.md for the accountability
record.` → `TARGET_MET`, `self_pointer=0`; 43 rows emit the unscored
`detail: note … names-the-ledger-in-prose`, 39 emit nothing (A4's tokenizer effect). The row's
only accountability claim is the ledger; the decoy suppresses the charge by design (line 378).
**Not reproduced.**

**A7 — the cited location is never read.** Every pointer = `` `SCORECARD.md:1` `` (line 1 of
`SCORECARD.md` is `# mado-shokunin — Scorecard`, which names no instrument).
`bad_pointer=22`, so **60 of 82 rows pass** with a citation to a line that contains no
evidence for them. The counter strips `:1` and scans the whole file, which names 60 basenames
(measured: `SCORECARD.md` names 60/82, `PROVINCE.md` 22/82). **Partially not reproduced** —
it does not by itself yield a green ledger, but it shows the pointer clause checks neither the
cited line nor the citation's freshness.

### 4.3 Minimal fixture (independent of the 82-row ledger)

`repro-mini` has three instruments, no fences, no header example row, so both counters start
green (`population=3 ledger_rows=3 … TARGET_MET`). Pointer-cell variants:

| variant | prototype | candidate `923faf02…` |
|---|---|---|
| `` `docs/alias.md` `` (A1) | `self_pointer=0 TARGET_MET` | `self_pointer=0 TARGET_MET` |
| `` `quality/tool-ledger-copy.md` `` (A3) | `self_pointer=0 TARGET_MET` | `self_pointer=0 TARGET_MET` |
| `` `docs/alias.md` plus quality/tool-ledger.md `` (A4) | `self_pointer=0 TARGET_MET` | `bad_pointer=3 TARGET_MISSED` (rejected by blob resolution, not by a self rule) |
| `` `docs/mentions.md` `` (A5) | `self_pointer=0 TARGET_MET` | `self_pointer=0 TARGET_MET` |
| `` `./quality/tool-ledger.md` `` | `self_pointer=3 TARGET_MISSED` | **`self_pointer=0 TARGET_MET`** |
| `` `quality/tool-ledger.md` `` (direct) | `self_pointer=3 TARGET_MISSED` | `self_pointer=3 TARGET_MISSED` |

## 5. The untracked in-tree candidate (`quality/counters/c1-r52-ledger.py`, `923faf02…`)

This file sits at the path the claim's counter is supposed to occupy, is executable, carries
the docstring `PRED-C1-r52: bounded instrument-ledger accountability check`, and is **not
tracked** (`git status --porcelain` → `?? quality/counters/c1-r52-ledger.py`, observed before
this seat wrote anything). I did not establish who produced it and make no authorship
judgement; the observation is time-stamped by the hash above. Measured against it:

1. **It fails the frozen green.** On the real lane at base, with the revision's own ledger:

   ```
   C1_R52: population=82 ledger_rows=83 uncovered=0 dup=0 dangling=1 bad_pointer=1 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED
   exit=1
   ```

   Cause: `parse_ledger` (line 39) does not skip fenced blocks. `quality/tool-ledger.md` at
   base documents its row grammar inside a ```` ``` ```` fence, and that example row
   (`` | `<repo-relative path>` | <one-line description> | `<pointer path>` or `<pointer path>:<line>` | ``)
   is parsed as an 83rd row → `dangling=1 bad_pointer=1`. The prototype's `unfenced()`
   (line 155) exists precisely for this; the candidate has no equivalent. C1's "Demonstrate
   production pass" is therefore not satisfied by the artifact at the target path.

2. **The frozen control produces no self/context signal.** It requires exactly three cells
   (line 41) and a backticked first cell; the frozen control is four cells, unbackticked, so:

   ```
   C1_R52: population=82 ledger_rows=0 uncovered=82 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MISSED
   ```

   `self_pointer=0 generic_desc=0`. The registration demand is that it "fail … **specifically
   for self-pointer/context defects**"; this artifact can never do that for the frozen control,
   and it can never name the control's pointer defect because the control's pointer cell is
   never parsed.

3. **Direct self-reference is laundered by two characters.** `target=pointer.strip("`").split(":")[0]`
   (line 56) compared with `LEDGER` by equality (line 57); `./quality/tool-ledger.md` resolves
   at `--rev` (`git show <rev>:./quality/tool-ledger.md` → resolves, verified) and is not equal
   to `LEDGER` → `self_pointer=0 TARGET_MET` on the mini fixture (§4.3).

4. **No selftest.** `--selftest` is declared (line 68) and ignored; invoking it alone exits 2
   with `error: the following arguments are required: --repo, --rev`. The registration's
   "Selftest includes explicit red/green receipts" has no counterpart in these bytes; the
   receipts in `w1/` belong to the prototype, not to this file.

5. Its description clause has none of the prototype's four filters, so the `usr bin` and
   naming-vocabulary escapes W1 already closed are open again here if this artifact lands.
   I did not re-run Attack01/Attack17's constructions against it; state that as untested.

## 6. Verdicts, errors, limits

**Verdicts.**

- Frozen control red: **reproduced** (V2), with `self_pointer=1 generic_desc=1` and
  `uncovered=81 dup=1`.
- C1 "non-self resolvable evidence targets": **not reproduced as implemented.** Six
  constructions (A1–A6) that resolve each row's accountability to `quality/tool-ledger.md`
  pass with `self_pointer=0`, all six with a fully clean field vector. A4 shows the
  pointer-region rule is defeated by a tokenizer branch rather than by the design ceiling the
  author disclosed.
- C1's *mechanism* statement is therefore weaker than its demonstration: the control fails for
  four independent reasons (`uncovered=81`, `dup=1`, literal self-pointer, missing context), so
  the two named demonstrations do not establish that the pointer clause was what discriminated.
  This confirms the W1 signal that the control does not isolate the required defects.
- For the untracked in-tree candidate: production pass **not reproduced**; defect-specific
  control failure **not reproduced**; pointer clause **not reproduced** (`./` spelling).

**Errors found (all are observations; none is a judgement of authorship).**

1. `path_tokens` pre-empts the whitespace fallback whenever a cell contains one backtick, so a
   bare ledger path in the pointer cell is invisible to both self scans (A4; 39/82 rows in the
   description variant).
2. `pointer` is compared as a *string* to `quality/tool-ledger.md`; an aliased, copied or
   `./`-spelled target is not the ledger (A1–A3; candidate item 3).
3. `LEDGER_REL` is a module constant; `--ledger` mode forces `ledger_rel = LEDGER_REL` even
   when the scored file lives elsewhere (main, line 824-831), so a counter integrated under a
   renamed path would compare against the wrong name. Untested here (the prototype is invoked
   at its documented path); flagged because integration is the L1's decision.
4. The `:N` anchor is stripped and never resolved (A7: 60/82 rows accept `SCORECARD.md:1`).
5. The "accountable" test is `basename in bytes` (line 337); it accepts a file that mentions
   the basename once in unrelated prose (A5). `PROVINCE.md` and `SCORECARD.md` are inventory
   documents that name 22 and 60 basenames respectively, so an inventory citation and an
   evidence citation are indistinguishable to the counter.
6. Frozen control is not isolated: `self_pointer=0` is reachable on a 4-cell control-shaped row
   by moving the ledger name one cell left (measured earlier: with `docs/alias.md` in the Reads
   cell the control reports `bad_pointer=1 self_pointer=0`), because the counter treats cell 2
   of a wide row as the description.
7. Candidate `923faf02…` parses fenced example rows (green fails), requires exactly three cells
   (control unparseable), and its `--selftest` is inert.

**Limitations.**

- The prototype is a W1 **draft**, not committed; L1 owns integration. My findings hold for
  `0fe862f1…` only. `repro.sh` pins `C=` to that path; if the landing bytes differ, re-run it
  against the new path before reusing these verdicts.
- The fixture documents (`docs/alias.md`, `docs/mentions.md`, `quality/tool-ledger-copy.md`)
  are new files in a scratch clone. The lane has no such files, so A1/A3/A5 are attacks on the
  counter's classification, not on the current ledger's honesty. The production ledger's 82
  pointer anchors were checked separately: only 3 rows have no `:N` anchor (they cite
  `.ufo/waves/round-51/registration.md`), and every anchored row's cited line names its
  instrument — i.e. the *current* ledger is not laundered by A7. That does not weaken the
  finding that the counter cannot detect such a ledger.
- A1–A3, A5–A6 keep the production descriptions, so they do not test prose quality. A4 is the
  only construction with the ledger literally inside the pointer cell; a reviewer who insists
  a pointer cell must be exactly one backticked token can call A4 off-grammar — A1/A2/A3/A6
  are on-grammar and do not depend on that defence.
- I make no semantic-entailment claim. A1/A3/A4 are structural facts (a redirect, a byte
  equality, a literal substring), which the claim's own "bounded accountability checks" scope
  does not excuse.
- No live read, probe, screenshot, package query, install or host mutation was performed; the
  lane was read with `git show`, `git ls-tree`, `git status` only.

## 7. Reproduction

Run from any cwd; writes only under `/fast/scratch/hyaku/mado-r52/Attack18` and clones the
lane read-only via `git clone`. Expected total runtime ≈ 6 s. Assertions on
`git rev-parse --show-toplevel` guard both fixtures.

```bash
#!/usr/bin/env bash
# Attack18 reproduction: C1 pointer self-reference laundering.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
BASE=85d57a818c3707397e21c840b6498b105ba798aa
C=$LANE/.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py
S=/fast/scratch/hyaku/mado-r52/Attack18
W=$S/work
G() { git -c user.name=atk18 -c user.email=atk18@example.invalid -c commit.gpgsign=false "$@"; }
echo "counter_sha256 $(sha256sum "$C" | cut -d' ' -f1)"
rm -rf "$S/repro-clone"; git clone -q --no-hardlinks "$LANE" "$S/repro-clone"
cd "$S/repro-clone" || exit 1
[ "$(git rev-parse --show-toplevel)" = "$S/repro-clone" ] || { echo "toplevel assert failed"; exit 1; }
git checkout -q "$BASE"
python3 - <<'PY'
import os
led = open("quality/tool-ledger.md").read().splitlines()
rows = []
for i, l in enumerate(led):
    s = l.strip()
    if not s.startswith("|"): continue
    c = [x.strip() for x in s.strip("|").split("|")]
    if len(c) < 3 or set(c[0]) <= set("-: "): continue
    if "/" not in c[0].replace("`", ""): continue
    rows.append((i, c))
os.makedirs("docs", exist_ok=True)
with open("docs/alias.md", "w") as fh:
    fh.write("# accountability alias index\n\n")
    for i, c in rows:
        fh.write("- `%s` -> quality/tool-ledger.md#L%d\n" % (c[0].replace("`", ""), i + 1))
with open("docs/mentions.md", "w") as fh:
    fh.write("# incidental mentions\n\n")
    for i, c in rows:
        fh.write("The basename %s appears in this sentence.\n" % c[0].replace("`", ""))
open("quality/tool-ledger-copy.md", "w").write(open("quality/tool-ledger.md").read())
def mk(tag, ptrfn):
    out = []
    for l in led:
        s = l.strip()
        if s.startswith("|"):
            c = [x.strip() for x in s.strip("|").split("|")]
            if len(c) >= 3 and not set(c[0]) <= set("-: ") and "/" in c[0].replace("`", ""):
                c[2] = ptrfn(c); l = "| " + " | ".join(c) + " |"
        out.append(l)
    open("ledger-%s.md" % tag, "w").write("\n".join(out) + "\n")
mk("alias", lambda c: "`docs/alias.md`")
mk("alias-anchor", lambda c: "`docs/alias.md:%d`" % (3 + [r[1][0] for r in rows].index(c[0])))
mk("copy", lambda c: "`quality/tool-ledger-copy.md`")
mk("bareptr", lambda c: "`docs/alias.md` plus quality/tool-ledger.md")
mk("mentions", lambda c: "`docs/mentions.md`")
def mentions_desc(c):
    c[1] = c[1] + " See quality/tool-ledger.md for the accountability record."
    return "`docs/mentions.md`"
mk("mentions-desc", mentions_desc)
mk("anchor1", lambda c: "`SCORECARD.md:1`")
mk("direct", lambda c: "`quality/tool-ledger.md`")
mk("mix", lambda c: "`docs/alias.md` and `quality/tool-ledger.md`")
PY
G add -A >/dev/null && G commit -q -m "attack18 fixtures"
REV=$(git rev-parse HEAD)
echo "fixture_rev $REV"
run() {
  echo "--- $1"
  out=$(python3 -I "$C" --repo "$S/repro-clone" --rev "$REV" --work "$W" ${2:-} 2>&1); rc=$?
  printf '%s\n' "$out" | grep -E '^detail: (self_pointer|note|bad_pointer)' | head -3
  printf '%s\n' "$out" | grep '^C1_R52:'
  echo "exit=$rc"
}
run "green (revision ledger)"
run "red (frozen control)" "--ledger $LANE/.ufo/waves/round-52/controls/c1-do-nothing.md"
for v in alias alias-anchor copy bareptr mentions mentions-desc anchor1 direct mix; do run "$v" "--ledger $S/repro-clone/ledger-$v.md"; done
echo "== note lines (unscored) for mentions variants"
for v in mentions mentions-desc; do
  echo -n "$v notes: "
  python3 -I "$C" --repo "$S/repro-clone" --rev "$REV" --work "$W" --ledger "$S/repro-clone/ledger-$v.md" 2>&1 | grep -c 'names-the-ledger-in-prose'
done
echo "== selftest"; python3 -I "$C" --selftest --work "$W" 2>&1 | tail -1

# ---------------- part B: minimal independent fixture, both counters ----------------
CAND=$LANE/quality/counters/c1-r52-ledger.py
M=$S/repro-mini
rm -rf "$M"; mkdir -p "$M"; cd "$M" || exit 1
git init -q; [ "$(git rev-parse --show-toplevel)" = "$M" ] || { echo "mini toplevel assert failed"; exit 1; }
python3 - <<'PY'
import os
F = {
 "tools/alpha.py": '#!/usr/bin/env python3\n"""alpha watcher: enumerates the widget lattice and prints a lattice digest."""\n',
 "tools/beta.sh": '#!/usr/bin/env bash\n# beta checker: verifies the lattice digest and prints a verdict.\n',
 "quality/counters/c1-delta.py": '"""delta counter: scores the lattice digest rows and prints the verdict."""\n',
 "SCORECARD.md": "# scorecard\n\n- tools/alpha.py keeps the alpha watcher.\n- tools/beta.sh keeps the beta checker.\n- quality/counters/c1-delta.py keeps the delta counter.\n",
 "docs/alias.md": "# alias\n\n- `tools/alpha.py` -> quality/tool-ledger.md#L3\n- `tools/beta.sh` -> quality/tool-ledger.md#L4\n- `quality/counters/c1-delta.py` -> quality/tool-ledger.md#L5\n",
 "docs/mentions.md": "# mentions\n\nThe basename tools/alpha.py appears in this sentence.\nThe basename tools/beta.sh appears in this sentence.\nThe basename quality/counters/c1-delta.py appears in this sentence.\n",
 "quality/tool-ledger.md": "# ledger\n\n| instrument | description | pointer |\n|---|---|---|\n"
   "| `tools/alpha.py` | Enumerates the widget lattice and prints a lattice digest | `SCORECARD.md` |\n"
   "| `tools/beta.sh` | Verifies the lattice digest and prints a verdict | `SCORECARD.md` |\n"
   "| `quality/counters/c1-delta.py` | Scores the lattice digest rows and prints the verdict | `SCORECARD.md` |\n",
}
for k, v in F.items():
    os.makedirs(os.path.dirname(k) or ".", exist_ok=True)
    open(k, "w").write(v)
open("quality/tool-ledger-copy.md", "w").write(F["quality/tool-ledger.md"])
base = F["quality/tool-ledger.md"].splitlines()
def mk(tag, ptr):
    out = []
    for l in base:
        s = l.strip()
        if s.startswith("|"):
            c = [x.strip() for x in s.strip("|").split("|")]
            if len(c) == 3 and c[0].startswith("`"):
                c[2] = ptr; l = "| " + " | ".join(c) + " |"
        out.append(l)
    open("ledger-%s.md" % tag, "w").write("\n".join(out) + "\n")
mk("alias", "`docs/alias.md`")
mk("copy", "`quality/tool-ledger-copy.md`")
mk("bareptr", "`docs/alias.md` plus quality/tool-ledger.md")
mk("mentions", "`docs/mentions.md`")
mk("dot", "`./quality/tool-ledger.md`")
mk("direct", "`quality/tool-ledger.md`")
PY
G add -A >/dev/null && G commit -q -m "mini fixture"
MREV=$(git rev-parse HEAD)
echo "mini_rev $MREV"
echo "candidate_sha256 $(sha256sum "$CAND" | cut -d' ' -f1)"
for v in green alias copy bareptr mentions dot direct; do
  if [ "$v" = green ]; then led=""; else led="--ledger $M/ledger-$v.md"; fi
  echo "--- mini $v"
  echo -n "  prototype: "; python3 -I "$C" --repo "$M" --rev "$MREV" --work "$W" $led 2>&1 | tail -1
  echo -n "  candidate: "; python3 -I "$CAND" --repo "$M" --rev "$MREV" $led 2>&1 | tail -1
done
echo "--- candidate on the real lane, base revision, revision ledger"
python3 -I "$CAND" --repo "$LANE" --rev "$BASE" 2>&1 | tail -1
echo "--- candidate on the frozen control"
python3 -I "$CAND" --repo "$LANE" --rev "$BASE" --ledger "$LANE/.ufo/waves/round-52/controls/c1-do-nothing.md" 2>&1 | tail -1
echo "--- candidate --selftest alone"
out=$(python3 -I "$CAND" --selftest 2>&1); rc=$?
printf '%s\n' "$out" | tail -1; echo "exit=$rc"
```

## 8. Hygiene

- Scratch: `/fast/scratch/hyaku/mado-r52/Attack18/` (repro.sh, repro-clone, repro-mini,
  work, transcripts) — **deleted at the end of this seat**; the report carries the commands,
  the script and the observed lines.
- Lane tracked tree: untouched by this seat. At seat end `git status --porcelain` reads
  `M corpus/README.md`, `M corpus/SOURCES.md`, `M quality/tool-ledger.md`,
  `?? corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, `?? corpus/lessons/round-52.md`,
  `?? quality/counters/c1-r52-ledger.py`, `?? quality/counters/c2-r52-proposition-entry.py`,
  `?? .ufo/waves/round-52/`. None of these is mine: this seat's only lane write is this report.
  The tracked modifications were present when the seat opened; the untracked counter
  `quality/counters/c1-r52-ledger.py` has mtime `11:11:48`, before this seat existed (the
  seat's first status was `head`-limited and did not enumerate the whole untracked set, so I
  do not claim ordering beyond that mtime).
- A `__pycache__/c1-r52-ledger.cpython-314.pyc` exists under `w1/C1CounterDesign/`; this seat
  never imported the counter (every invocation was `python3 -I <script>`), so it is a peer
  byproduct, not mine. I left it in place.
- Git in the lane: read-only (`show`, `ls-tree`, `status`, `rev-parse`). All commits were made
  in scratch clones/fixtures after a `rev-parse --show-toplevel` assert.
- No install, upgrade, package query, live read, probe, screenshot, service/compositor touch or
  host mutation. Pacman untouched.
- Every write is this report or the scratch directory.

Report: .ufo/waves/round-52/w2/Attack18.md
