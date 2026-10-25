# RevC1Code — review of `quality/counters/c1-r37-event-ground.py` (PRED-C1-r37-v2)

Seat: reviewer, mado round 37 wave 1. Read-only on the lane. Scratch:
`.ufo/waves/round-37/w1/scratch/RevC1Code/probe.py` and its output `probe-out.txt`. The sandbox
`/dev/shm/mado37-RevC1Code/sb` (an object-sharing `git clone --shared` with a sparse checkout of
`corpus/` and `fetch/`, built that way because the tmpfs `usrquota` returned `Disk quota exceeded`
for a full `--no-local` clone) was removed after the run. No tool was installed or updated. LSP
does not apply: the counter is a standalone script with no callers, so the check was done by
reading the code and running it.

## Verdict

**The code implements the docstring sentence faithfully, clause by clause. The sentence is
looser than the registration's intent.** Seven adversarial trees, all built in the sandbox and
committed there, reach `admitted=2/2 verdict=TARGET_MET` exit 0. Two of them are severe:

- an entry that is bound as its own receipt, with invented ids and no source receipt in the tree;
- the round's own must-miss control `c1-token-stub` plus one `**OBS** S189 S201 S212` line, with
  every Gate quote set to a single space.

Both defeat the purpose of Amendment 1. At the real base, the freeze tip and HEAD, the counter
scores 0/2 with exit 1, as registered.

The counter is frozen, so none of these can be fixed under v2. Any fix is a new predicate, and the
registration says C1 then "fails as declared". My recommendation is that whoever admits C1 treat
a `TARGET_MET` as necessary but not sufficient, and check findings F1–F3 by hand on the measured
tip.

## Runs (exact commands, quoted output)

The counter is byte-identical at the freeze tip, at HEAD and in the worktree:

```
893a8aadc80ab19bc163e366d674a8ac32feacd0 1c21f8ba736bf8c17eeab4d485c9101ba98436d17bad4dfe73a66bededb6294f
80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b 1c21f8ba736bf8c17eeab4d485c9101ba98436d17bad4dfe73a66bededb6294f
worktree 1c21f8ba736bf8c17eeab4d485c9101ba98436d17bad4dfe73a66bededb6294f
```

`git diff --stat 893a8aa HEAD -- quality corpus` printed nothing.

**Base:** `python3 -I quality/counters/c1-r37-event-ground.py --repo . --rev b4e47e980bfb0cbc8a4e788f59a41db858751fd8`

```
PRED-C1-r37-v2 entry=corpus/knowledge/event-delivery-limits-r26.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 ids=- ok=0
PRED-C1-r37-v2 entry=corpus/knowledge/event-queue-observability-r37.md a=0 b=0 c=0 d=0 e=0 f=0 g=0 ids=- ok=0
PRED-C1-r37-v2 admitted=0/2 verdict=TARGET_MISSED rev=b4e47e980bfb0cbc8a4e788f59a41db858751fd8 base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
exit=1
```

**Freeze tip:** `--rev 893a8aadc80ab19bc163e366d674a8ac32feacd0` gives the same two entry lines and then:

```
PRED-C1-r37-v2 admitted=0/2 verdict=TARGET_MISSED rev=893a8aadc80ab19bc163e366d674a8ac32feacd0 base=b4e47e980bfb0cbc8a4e788f59a41db858751fd8
exit=1
```

**HEAD** (80b83c8) gives the same result, `admitted=0/2 … exit=1`. This matches the registered
**Before** (`admitted=0/2 verdict=TARGET_MISSED`, exit 1). **PASS.**

## Clause-by-clause: does the code implement the sentence?

| Item | Code (file:line) | Result |
|---|---|---|
| a | `c["a"] = int(body is not None and show(repo, base, path) is None)` :127 | PASS |
| b: first 15 lines only | `head = body.splitlines()[:15]` :129 | PASS (probe `header-at-line16` → `b=0 … TARGET_MISSED`, rc=1) |
| b: ids from all `source:` lines in the head | `src_lines = [l for l in head if re.match(r"^[-* ]*source *:", l)]` :130; `ids = sorted(set(re.findall(r"\bS\d{3,}\b", " ".join(src_lines))))` :131 | PASS (probe `uncited-late-source`: a `source: S999` past line 15 is ignored, still `ids=S189,S201,S212`) |
| b: verified-at / recheck | :133–134 | PASS |
| c: 11 cells, status, used-by split | `any(len(r) == 11 and r[7] == "mined" and path in [u.strip() for u in r[10].split(",")]` :136 | PASS. Index 7 is `status` and index 10 is `used-by` in the header `\| id \| source \| kind \| tier \| scope \| anchor \| teaches \| status \| opened \| recheck \| used-by \|`. All 201 Registry rows at the freeze have 11 cells (`201 11`), with no duplicate ids. |
| `## Registry` / `## Gate` exact match | `if re.match(r"^ {0,3}## ", line): inside = line.strip() == heading` :70–71 | PASS. Unit probe: `'## Registry' rows= 1`, `'## Registry ' rows= 1`, `'##  Registry' rows= 0`, `'## Registry (v2)' rows= 0`, `'### Registry' rows= 0`, `'    ## Registry' rows= 0`, `'## Gate — corroboration' gate-section-lines= 0`, `'## Gate ##' gate-section-lines= 0`. The match is not fence-aware (see F6). |
| d: quote matched on bytes | `blob = show(repo, rev, rpath, binary=True)` :145; `len(quote.split()) <= 25 and quote.encode() in blob` :147 | PASS. The match is on the receipt's raw bytes; the quote comes from the lesson decoded as UTF-8 with `replace`. All five receipts are valid UTF-8 with 0 CR bytes (`S189.bin 6479 utf8-ok 0` … `S214.bin 1789 utf8-ok 0`), so decoding cannot make the match differ. No lower bound exists (F2). |
| e: README first cell | `l.strip().strip("\|").split("\|")[0]` :120; `base_name in cell` :156 | Matches "names … in its first cell" as a substring test (F7) |
| f | `t in body and any(t.encode() in b for b in receipts)` :157 | PASS. `receipts` holds only Gates that passed d (:148–149), which is stricter than "binds" and harmless. |
| g | `stated = stated or quote in body` :150; `any("**OBS**" in l and re.search(rf"\b{i}\b", l) for l in lines)` :152 | Implements the sentence, but the sentence is defeatable (F2, F3) |
| Precondition | `base_files = git(repo, "ls-tree", "-r", "--name-only", base, …)` :102; `for path in base_files.split():` :104; `raise Setup("ground_held_at_base …")` :109 | Fires on normal names (`SETUP ground_held_at_base corpus/knowledge/held-r1.md:MAX_QUEUED_EVENTS`, exit=2). Holds at the real base: `git grep -l -F <t> b4e47e9 -- corpus/knowledge` gives 0 files for each of the four tokens. Has a filename hole (F4). |
| GIT_* scrub | `ENV = {k: v … if not k.startswith("GIT_")}` :49; `env=ENV` :57 | PASS (see the evidence below) |
| Exit code matches verdict | `return 0 if verdict == "TARGET_MET" else 1` :165; `except Setup … sys.exit(2)` :171–173 | PASS on normal paths; diverges on unhandled errors (F5) |

**GIT_* evidence.** Unscrubbed, `GIT_DIR=$S/.git git -C . rev-parse HEAD` printed the sandbox
commit `b0d011d5…`, so the variable would redirect git. With `GIT_DIR`, `GIT_WORK_TREE`,
`GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_CONFIG_PARAMETERS` and `GIT_NAMESPACE` all pointing
elsewhere, the counter still printed `admitted=0/2 verdict=TARGET_MISSED rev=893a8aad…`, exit=1,
which is identical to the clean run. A sandbox-only rev with `GIT_DIR=sandbox` gave
`SETUP unresolvable revision`, exit=2, so the environment did not leak.

**Exit-code paths.** Each of these gave `SETUP unresolvable revision` with exit 2:

- bogus `--rev deadbeef`;
- a non-repo `--repo`;
- `--rev <tree>`.

A missing `--rev` gave the argparse usage error with exit 2.

## Findings (by severity)

### F1 — HIGH: a receipt can be any committed file, including the entry itself, so C1 meets with no source evidence

**Sentence:** clause d requires only that "the receipt is committed at REV" with a matching sha256. **Code:** `blob = show(repo, rev, rpath, binary=True)` :145. Nothing ties `rpath` to `.ufo/waves/round-37/fetch/`, to the S-id's Registry anchor, or to the ids the registration names. The registration's **Sourced** bullet says both entries rest on "S189, S201 re-opened; S212, S213, S214 new", each binding "a committed receipt"; neither the docstring nor the code enforces that.

**Probe `self-receipt`** (sandbox tree with 0 files under `fetch/`):

- The lesson binds each entry as its own receipt: `GATE S990 receipt=corpus/knowledge/event-delivery-limits-r26.md sha256=194d99ab… quote="this sentence is evidence for S990 only because it says so"`.
- Each entry holds its two tokens, that sentence and `**OBS** S990: …`.
- SOURCES gets two invented `mined` rows, and the README gets two rows.

The counter printed:

```
case=self-receipt rc=0
  … event-delivery-limits-r26.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S990 ok=1
  … event-queue-observability-r37.md a=1 b=1 c=1 d=1 e=1 f=1 g=1 ids=S991 ok=1
  PRED-C1-r37-v2 admitted=2/2 verdict=TARGET_MET
```

Clauses d, f and g all close on the entry's own bytes. A related gap: an S-id can bind another
id's receipt, because the Gate digest is never compared with the Registry anchor's sha256 prefix.

**Hand check at admission:** the cited ids are a subset of {S189, S201, S212, S213, S214}, and
every Gate `receipt=` path is under `.ufo/waves/round-37/fetch/`.

### F2 — HIGH: no lower bound on the quote, so clause g is beaten by the v1 token stub plus one line

**Sentence:** clause d says "the quote has at most 25 words"; clause g says the body "carries one of that id's located Gate quotes verbatim". **Code:** `GATE_RE … quote="(.+)"` :48 accepts `" "`; `len(quote.split()) <= 25` :147 gives 0 words; `quote.encode() in blob` and `quote in body` :150 are both trivially true.

**Probe `space-quote`:** `controls.wire(stated=False)` is exactly the frozen must-miss
`c1-token-stub`. Each lesson line reads, for example,
`GATE S189 receipt=.ufo/waves/round-37/fetch/S189.bin sha256=eea605df…540d quote=" "`. The whole
E1 body is:

```
source: S189, S201, S212
verified-at: 2026-10-25
recheck: 90d

body naming MAX_QUEUED_EVENTS and overflowed event queue.
**OBS** S189 S201 S212
```

The counter printed `a=1 b=1 c=1 d=1 e=1 f=1 g=1` for both entries, then
`admitted=2/2 verdict=TARGET_MET` with rc=0. **Probe `one-char-quote`** (`quote="e"`) gives the same
result. Amendment 1 exists so that this stub misses; with v2 it is one line away from meeting.

**Hand check at admission:** each Gate quote is a substantive located line, as in the controls'
`QUOTES` (for example `const size_t MAX_QUEUED_EVENTS = 64;`), not a fragment.

### F3 — MEDIUM: any line containing `**OBS**` counts as an observation line, including the `source:` header

**Code:** `"**OBS**" in l and re.search(rf"\b{i}\b", l)` :152 is a substring test anywhere in the
line, anywhere in the body. **Probe `obs-on-source-line`:** the header reads
`source: S189, S201, S212 **OBS**`, the body has only `quoted: \`…\`` lines and no observation
line. The counter printed `g=1` for both entries, `admitted=2/2 verdict=TARGET_MET`, rc=0. The
sentence asks for "an `**OBS**` line naming the id"; a header line carrying the marker is not
one.

### F4 — MEDIUM (latent): the precondition skips base files whose names contain a space or non-ASCII

**Code:** `ls-tree -r --name-only` without `-z` :102, followed by `base_files.split()` :104. A
space splits the name into two bogus paths. With git's default `core.quotePath`, a non-ASCII name
comes back C-quoted. In both cases `show()` returns None, which becomes `""`, and the file is
silently never scanned.

**Probe:** a base commit adds a token-holding file under three names.

| Base file name | Counter result |
|---|---|
| `held-r1.md` | `SETUP ground_held_at_base corpus/knowledge/held-r1.md:MAX_QUEUED_EVENTS`, exit=2 |
| `held r1.md` | `admitted=2/2 verdict=TARGET_MET`, exit=0 |
| `held-é.md` | `admitted=2/2 verdict=TARGET_MET`, exit=0 |

This has no effect at the real base: none of the 50 names under `corpus/knowledge` at b4e47e9
contains a space, non-ASCII, `"` or `\` (`grep -c` gave `0`), and `git grep` confirms all four
tokens are absent. It is still a divergence from "no corpus/knowledge/ file at BASE contains any
frozen surface token".

### F5 — LOW: an unhandled error exits 1, which collides with `TARGET_MISSED`

The docstring says "Setup or usage errors exit 2" (:30). With git missing from `PATH`, the counter
ends with `FileNotFoundError: [Errno 2] No such file or directory: 'git'` and exit=1. No verdict
token is printed, but the exit code is the same as a measured miss. Any other unexpected exception
behaves the same way. A caller that reads only the exit code (as `controls.py` and a kill-rule
check might) cannot tell a crash from a miss. This is safe-side, since it never fakes a
`TARGET_MET`.

### F6 — LOW: section parsing is not fence-aware, and nested headings are mishandled

**Probe `gate-in-foreign-fence`:** the GATE lines sit inside a fenced "example" under `## Notes`,
with `## Gate` itself inside that fence. The counter printed `admitted=2/2 verdict=TARGET_MET`.
Unit probes of the same parser:

- a `## x` inside a fence ends `## Registry` early (`rows= 0`);
- an H1 after `## Registry` does not end the section (`rows= 1`);
- an indented GATE line is accepted because of `line.strip()` at :116 (`indented GATE accepted (strip): True`).

### F7 — LOW: the README test is a substring test on the first cell

**Code:** `base_name in cell` :156. **Probe `readme-retired-cell`:** first cells
`` `knowledge/event-delivery-limits-r26.md.retired` `` and `` `old-knowledge/event-queue-observability-r37.mdx` ``
gave `e=1` and `admitted=2/2 verdict=TARGET_MET`. Also, `||` at the start of a row collapses the
empty first cell (`'||knowledge/x.md| y |'` → first cell `knowledge/x.md`). A substring test is
needed because real rows carry suffixes such as `(MADO-1)`, but it is looser than "names
`knowledge/<basename>`".

### F8 — LOW: duplicate Registry rows for one id are accepted

**Code:** `rows.setdefault(m.group(1), []).append(cells)` in `registry_rows` together with `any(…)` at :136. **Probe `dup-row-refused`:** a second, colliding `| S189 | … | refused | … | - |` row, and C1 still gave `admitted=2/2 verdict=TARGET_MET`. This round's assimilation carries an id-collision renumber map, so a collision would pass clause c unnoticed.

### Informational (safe-side or latent; no action under v2)

- **Exact Gate heading versus convention.** Exact `## Gate` excludes headings like round-36's
  `## Gate — corroboration of S211 …` (`corpus/lessons/round-36.md:307`). An author following that
  convention gets a false negative. Authors must use a bare `## Gate`.
- **Escaped pipes.** A `\|` inside a Registry cell yields 12 cells (`escaped pipe cells: [12]`),
  so clause c fails safe. All freeze rows are 11 cells.
- **Line counting.** `str.splitlines()` also breaks on `\x0c`, `\x1c` and `\u2028`
  (`… counts … as breaks: 4`), so "first 15 lines" can be fewer newline-separated lines than 15.
  This is conservative.
- **No ancestry check.** Nothing checks that REV descends from BASE: the F4 runs scored a sibling
  commit against an unrelated base.
- **Case-sensitive headers.** `source:`, `verified-at:` and `recheck:` are matched
  case-sensitively. The package entry's header uses lowercase `source:`, `verified-at:` and
  `recheck:` at lines 6–8, so it parses, but it cites `S214` (Waybar `workspaces.cpp`), and that
  number collides with this round's S214 (`Logger.cpp`). Re-grounding has to renumber it.

## Residual risk and verification gaps

- F1–F3 are not code-versus-sentence divergences: the frozen v2 sentence admits them. Under the
  registration's rule they can only be closed by a v3 predicate, which ends the v2 claim. The
  admitting seat has to apply the two hand checks named under F1 and F2.
- I did not score the real round-37 entries: neither target exists at HEAD yet (`a=0` at HEAD).
- No probe covered a symlink or directory at the target path: `git show rev:path` on a tree exits
  0, so clause a would treat it as existing. This is untested.
- A global gitconfig reached through `HOME` is not scrubbed (only `GIT_*` is). I found no config
  that changes `show`, `ls-tree` or `rev-parse` output except `core.quotePath`, which F4 already
  covers.
