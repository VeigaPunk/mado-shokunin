# ExecC1IndepB — w2 falsify, C1 independent rebuild (mado round 47, hyaku run 9, 2026-10-26)

Status: **done — candidate TARGET_MET on 3 counts (2 nonces on the L1's filesystem, 1 nonce on tmpfs);
base rev MISSED on the same counter and work dir.** Three *contract* holes found and measured: the
docstring of the L1 reference is **not sufficient on its own** to reach `TARGET_MET`; each hole is closed
by the fixtures, and each costs fixtures when implemented the way the docstring reads (measured below).
Artefacts: `.ufo/waves/round-47/w2/ExecC1IndepB/` (candidate + receipts). Report: this file.

## 1. What was built

`tools/mado-terminal.py` (candidate), 1239 lines, sha256
`f7fb0c0465193b36ab97c431ebecd113b50aa63175da3631516a36e6a5ed0991`, seat copy
`.ufo/waves/round-47/w2/ExecC1IndepB/mado-terminal.py`, scored in a throwaway clone
(`git clone --shared --no-checkout` → `checkout --detach d7527d60…` → one commit `9017d32de5ac…`
adding only `tools/mado-terminal.py`). No lane git/jj mutation, no host write.

Derivation (disclosed in full): I read the contract docstring
(`.ufo/waves/round-47/l1-draft/mado-terminal.py:2-88`) and the pinned resolver
(`.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256 `89f2be9a…`, all 1499 lines), plus the public
counter body (`quality/counters/c1-r47-terminal.py`) to know the sandbox, and the fixture records to know
the target. What I did **not** read: the bodies of the reference implementation (its `split_ifs`,
`read_split`, `printf_b`, `tokenize`, `strip_fields`, `Resolver`, `selftest`). The reference's module
constant block (`:89-120`, `USEP/SPACE/TOK_SPECIAL/BASH_BUILTINS/BASH_KEYWORDS/SCRIPT_FUNCTIONS`) was
shown by the declaration view I used to find the docstring, and my candidate reuses those tables; the
algorithms are derived from the script.

Behaviour: `print` models the cold-cache selection and reproduces the resolver's stdout bytes and exit
status (byte strings end to end, `os.write(1, …)`, so no re-encoding anywhere); `explain [--observed FILE]` traces the lists
and candidates and prints the `MADO_TERM:` line, with `AGREE`/`DIFFER` against a captured
`--print-id --print-path --print-cmd`; `--selftest` runs 54 hermetic cases through the model (order
independent: no case relies on readdir order for its expected value).

## 2. Score (measured, receipts in `rec/`)

| count | rev | nonce | work fs | result |
|---|---|---|---|---|
| `count-base.txt` | `d7527d60…` (frozen, no tool) | 4711 | xfs | `fixtures=0/190 … tool=absent verdict=TARGET_MISSED`, exit 1 |
| `count-nonce4711.txt` | candidate `9017d32d…` | 4711 | xfs | `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0 |
| `count-nonce1.txt` | candidate | 1 | xfs | same, `TARGET_MET`, exit 0 |
| `count-tmpfs.txt` | candidate | 987654321 | tmpfs (`/dev/shm`) | same, `TARGET_MET`, no fixture drift, exit 0 |

Full line, candidate/nonce 4711:
`PRED-C1-r47: fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET rev=9017d32de5ac7db59e1bc2e65842bc518f24f634 nonce=4711`

The tmpfs count matters: the fixtures' fallback order comes from readdir order, so a count whose `--work`
sits on a create-ordered filesystem could have drifted into `SETUP`; measured: **no drift** on xfs and on
tmpfs, so the recorded `expect` values are not order sensitive for this fixture set.

## 3. Holes in the contract (docstring), each measured to cost fixtures

### F1 — tokenizer / field-strip failure does not reject; the partial, unstripped words survive

Docstring, `l1-draft/mado-terminal.py:65-66`: Exec is "escape-expanded, tokenized by the shell-quoting
rules of x:561-692, its field codes stripped (x:694-740), and its first word must be found by
`command -v` (reject otherwise)". The obvious reading — a tokenizer or strip failure rejects the entry —
is wrong:

* `fetch/xdg-terminal-exec:958-960` calls `de_tokenize_exec` / `de_strip_fields` and checks neither status;
* both write their result **into** `XTE__EXEC_USEP` as they go, and `de_strip_fields` assigns only at its
  end (`:738`), so an early `return 1` (`:729-730`, "unknown % field") leaves the *tokenized* value;
* the whole call sits in `check_entry_key … && continue` (`:997`), so `set -e` is inert there and the
  failure only makes the key line "not continue".
* A failed tokenizer also keeps the prefix it already parsed: `:623-624` (`Encountered unquoted
  character` → return 1) and `:683` (`Double quote was not closed`) both leave the partial word list.

Receipts: fixture `t5-field-unknown` (`Exec=alacritty %z` → `rc=0`, stdout keeps `%z`) and
`t13-two-file-fields` (`%f %F` → both kept), `l1-strip-fields-failure-keeps-tokens`; clause g's KEYS
`Exec={n} %f %u` exercises it too. Independence check: the counter's own control
`V-STRIP-FAIL-EMPTIES` = `fixtures=187/190 … generated=147/150` (`receipts/ctl-c1.txt`), and my
docstring-literal build (reject on strip failure) = `fixtures bad=6 explained bad=3`
(`rec/docstring-literal-strip.txt`: `t5-field-unknown`, `t13-two-file-fields`,
`l1-strip-fields-failure-keeps-tokens`).

### F2 — the `IFS=<non-whitespace> read -r a b` trailing-delimiter rule is undocumented

Docstring `:44` says only "split at the first ':' into id and action with bash `read` rules"; `:78` names
`printf %b` for the *content* of delimiters but nothing about how an option value is split off. bash drops
**one lone trailing delimiter** and keeps two (`a=b=` → `b`, `a=b==` → `b==`, `a===` → `==`; measured on
the host's bash 5.x in POSIX mode). The rule decides:

* `--title=x=` → title `x` (delimiters read at `fetch/xdg-terminal-exec:1246`, `:1299`, `:1307`,
  `:1238`), fixture `l1-title-trailing-equals` (`rc=0`, `foot --title x`);
* `/execarg_default:<id>:-x:` → `-x` (`:407`), fixture `l1-execarg-default-trailing-colon`;
* the list-line split (`:436`) for an `id:action:x` line.

Receipts: fixture `l1-title-trailing-equals`, `l1-execarg-default-trailing-colon`; control
`V-READSPLIT-NOSTRIP` = `fixtures=188/190`; my docstring-literal build (no trailing-delimiter rule) =
`fixtures bad=4` (`rec/docstring-literal-readsplit.txt`: exactly those two fixtures). Clause g is *not*
affected (its `ARGVS` carry no `=`-terminated option value), so an implementer who gets this wrong still
sees `generated=150/150` and only loses 2 fixtures.

### F3 — "`command -v` finds aliases" is a POSIX-mode property, not stated as one

Docstring `:71`: "`command -v` finds aliases (ids registered in step 4 and not yet tried)". True **for the
judge**, but only because the counter binds `/bin/sh` to the host bash
(`quality/counters/c1-r47-terminal.py:141`) and bash reports aliases for `command -v` only in POSIX mode:
`/bin/sh -c 'alias aa="x=1"; command -v aa'` → rc 0, while `bash -c '…'` → rc 1 (measured). An
implementer who checks the claim with `bash` instead of `/bin/sh` concludes the opposite — I did, and lost
fixture `l1-tryexec-alias-of-untried-id` (`rc=0`, `foot.desktop`; the alias is a *different, still
untried* id: `TryExec=kitty.desktop`). Note the flip side, which the docstring does state and the script
enforces: the entry's own id is already `unalias`ed before it is read (`:1083-1085`), so `TryExec=<own id>`
fails. Receipts: fixture `l1-tryexec-alias-of-untried-id`; control `V-NO-ALIASES` = `fixtures=189/190`;
my docstring-literal build = `fixtures bad=2 explained bad=1`
(`rec/docstring-literal-noalias.txt`).

### F4 — minor: the fallback list needs find's *preorder descent*, not just "readdir order"

Docstring `:50` says "directory entries in readdir order". The order of `XTE__FALLBACK_ENTRY_IDS` also
depends on `find -L` descending into a subdirectory **at the point it is met** (preorder, in readdir
order): with `applications/vendor/kitty.desktop` created before `applications/foot.desktop`, find emits
`vendor/kitty.desktop` first, and prepending (`:790`) then puts `foot.desktop` ahead of it. My first walker
(yield files, then descend) was wrong; preorder is what matches. Fixtures pass with preorder
(`subdirectory-ids`, `odd-paths`), so this is derivable from "find", but the docstring does not say it and
a sorting walker would break the fallback order silently.

### F5 — predicate note (not a scoring hole): `cmd=` in `MADO_TERM:` is not judged

Clause x parses `selected=`, `path=`, verdict and rc from the last `MADO_TERM:` line
(`quality/counters/c1-r47-terminal.py:268`); `cmd=` (docstring `:19`) is never compared, so a tool may
print `cmd=-` always. The printed command itself is judged by clauses f/g, so this is cosmetic; flagged
only so it is not read as a coverage claim.

## 4. Contract statements I verified as exactly right (and that a naive model gets wrong)

* loop-status rejection (docstring `:67`) — `fetch/xdg-terminal-exec:989` (`[Desktop Entry]` with an
  action asked) and `:1014` (`[` group while Exec not allowed) leave the while-loop status 1, so the entry
  is rejected; fixtures `l1-loop-status-*`; control `V-NO-LOOPSTATUS` 188/190.
* key carryover across entries without `reset_keys` (docstring `:68-70`); control `V-NO-CARRYOVER` 189/190.
* the `/./` path fold (docstring `:76`); control `V-NO-PATH-FOLD` 102/190.
* `+id` / `-id` exclusion and the first-word-wins lists (docstring `:46-48`); control `V-NO-EXCLUSION` 185/190.
* key lines matched on their **whole** text, so `CategoriesX=` counts (docstring `:59`); fixture
  `categories-prefix-key`, control `V-CATEGORIES-EXACT` (g 146/150).
* the applications dir keeping its trailing `/` (so the find start is `<dir>/applications/.` and the
  `/./` fold has something to fold) is implied by docstring `:49` and needed for the `-path` match; my
  model reproduces it from `fetch/xdg-terminal-exec:168`.

## 5. Recommendation to the L1 (before the data commit — a v2 re-registration is cheap now)

Add three sentences to the contract docstring (no counter change, no fixture change, no narrowing):

1. after `:66`: "a tokenizer or field-strip failure does not reject the entry: the partially tokenized,
   unstripped words are kept and only `command -v <first>` decides;"
2. after `:44` (and for the `=` options): "bash `read` drops one lone trailing delimiter of the last field
   and keeps two (`a=b=`→`b`, `a=b==`→`b==`);"
3. after `:71`: "alias lookup in `command -v` is the POSIX-mode behaviour of the judge's `/bin/sh`
   (bash-as-`sh`); the entry's own id is already unaliased when it is read."

Optional: state find's preorder descent (`:50`) and drop or judge `cmd=` (`:19`).

The candidate reaches `TARGET_MET` as written, so C1 itself is not at risk from these holes; the risk they
carry is a *seat* cost: any future from-docstring rebuild loses 3–6 fixture slots (measured above) and
must rediscover the rules from the fixtures, which is what happened here.

## 6. Residuals and limits of this evidence

* One host, one bash (5.x) as `/bin/sh`; 3 counts, 2 nonces on xfs + 1 on tmpfs. Not exercised: the warm
  cache, `-h/--help`, an empty argv element (declared out of contract), a filesystem whose readdir order
  differs from xfs/tmpfs.
* `--selftest` is a real model check (54 cases) but clause s judges only its printed line (declared
  residual of the registration, not re-measured here).
* My docstring-literal variants are my own patches of my candidate (reject-on-strip-failure,
  no-trailing-delimiter rule, aliases invisible); they are an independent reading of the contract, not the
  L1's controls, and they agree with the L1's `V-*` controls on which fixtures fail.
* All 38 quotes/locators in this report are re-checked by `ExecC1IndepB/verify-locators.sh` →
  `rec/verify-locators.txt` (`VERIFY: ALL_LOCATORS_HOLD`, exit 0, 38 `OK` lines); locators were computed
  with `grep -n`, never typed.

## 7. Files and receipts (all under `.ufo/waves/round-47/w2/ExecC1IndepB/`)

* `mado-terminal.py` — the candidate (sha256 `f7fb0c04…`, byte-identical to the scored commit
  `9017d32d…:tools/mado-terminal.py`, re-hashed after the count).
* `verify-locators.sh`, `rec/verify-locators.txt` — locator/quote verification.
* `rec/count-base.txt`, `rec/count-nonce4711.txt`, `rec/count-nonce1.txt`, `rec/count-tmpfs.txt` — counter
  runs (full stdout, clause lines included).
* `rec/docstring-literal-strip.txt`, `rec/docstring-literal-readsplit.txt`,
  `rec/docstring-literal-noalias.txt` — the three contract-literal builds and the fixtures each loses.
* Scratch (`/fast/scratch/hyaku/mado-r47/ExecC1IndepB/`, incl. the throwaway clone and the local
  non-sandboxed fixture comparator) is not cited and is deleted at seat end.
* No tool install/upgrade was made; no package transaction; no compositor or GUI action; the resolver was
  only ever run with `--print-*` and `XDG_CACHE_HOME` inside scratch.
