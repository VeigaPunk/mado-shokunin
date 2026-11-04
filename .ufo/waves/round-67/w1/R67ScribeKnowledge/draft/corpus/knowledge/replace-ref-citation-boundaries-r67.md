source: S436 — git v2.56.0 `Documentation/git-replace.adoc` (tag v2.56.0, fetched 2026-11-03, sha256 3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631) — the `refs/replace/` namespace, the replace-by-default rule, its two escape hatches, and the BUGS/CAVEATS limits
verified-at: 2026-11-03
recheck: on-release — when the host git leaves 2.56.0 or the tag's `git-replace.adoc` changes (re-fetch, re-hash, re-run the §2 fixture receipt), and when the standing instrument's child set changes (re-run the §4 census at the then-current revision)

# Replacement refs on git 2.56.0: what `refs/replace` rewrites, which lane object reads need `GIT_NO_REPLACE_OBJECTS=1`, and what the round's R control proves (MADO-R67-1)

## Scope

Lane-tooling scope only. This entry answers three questions about the
round-67 C2 replacement-ref control (`claims-declaration-r67.md:65-104`;
baseline `.ufo/waves/round-67/control-baseline-r67.txt`): what a replacement
ref does to a git child's object reads on this host's git 2.56.0, which
lane instruments read objects through git and therefore need
`GIT_NO_REPLACE_OBJECTS=1`, and what the round's R control can and cannot
prove. It is not a desktop claim, not a truth claim about PROVINCE state
cells, and not an authenticity claim about repository objects. Every host
row below was measured on this host in scratch fixtures under
`/fast/scratch/hyaku/mado-r67/R67ScribeKnowledge/` (deleted with the seat);
the receipt is `.ufo/waves/round-67/w1/R67ScribeKnowledge/receipts/host-replace-fixtures.txt`,
and each row is re-derivable from the command shown in it.

The C2 baseline already measured the defect this entry explains: at the
pre-r67 tip `usedby_guard=0`, `ledger_guard=0`, and a child env built from
scratch read `forged` where a guarded read returned `real`
(`control-baseline-r67.txt`, lines beginning `BASELINE_C2`).

## Documented rows (`[INF-docs]`, tag v2.56.0, opened 2026-11-03)

| row | teaches (tag v2.56.0) | source | locator | quoted line |
|---|---|---|---|---|
| K01 | A replacement lives in a dedicated ref namespace, one ref per replaced object; the ref name is the replaced object's oid (K02), so a repo can carry replacements without changing any of its own commit history. | S436 | git-replace.adoc:20 | "Adds a 'replace' reference in `refs/replace/` namespace." |
| K02 | The ref name carries the replaced object's SHA-1 and the ref content the replacement's SHA-1: the mapping is a name-to-name indirection, not a rewrite of the stored objects. | S436 | git-replace.adoc:22 | "The name of the 'replace' reference is the SHA-1 of the object that is replaced. The content of the 'replace' reference is the SHA-1 of the replacement object." |
| K03 | Replacement is type-checked by default (same type), and `-f` bypasses that check; the lane's controls plant same-type replacements, so the type rule is not exercised by them. | S436 | git-replace.adoc:26 | "The replaced object and the replacement object must be of the same type. This restriction can be bypassed using `-f`." |
| K04 | Beyond type there is no restriction: merge and non-merge commits are interchangeable as replacement targets, which is why a replaced commit can change the tree a reader walks. | S436 | git-replace.adoc:31 | "There is no other restriction on the replaced and replacement objects. Merge commits can be replaced by non-merge commits and vice versa." |
| K05 | Replacement applies by default to all git commands except reachability traversal (prune, pack transfer, fsck): object reads are exactly the class of commands that honour it. | S436 | git-replace.adoc:34 | "Replacement references will be used by default by all Git commands except those doing reachability traversal (prune, pack transfer and fsck)." |
| K06 | The per-command escape hatch is a git-level option placed just after `git`; on 2.56.0 both `git --no-replace-objects -C D` and `git -C D --no-replace-objects` read the real bytes (H02). | S436 | git-replace.adoc:38 | "It is possible to disable the use of replacement references for any command using the `--no-replace-objects` option just after 'git'." |
| K07 | The process-level escape hatch is the environment variable, and the document states equivalence with the option; the exact value semantics are not specified by this file (H03 measures presence semantics). | S436 | git-replace.adoc:55 | "The `GIT_NO_REPLACE_OBJECTS` environment variable can be set to achieve the same effect as the `--no-replace-objects` option." |
| K08 | A documented side effect: replace objects turn off commit-graph reading or writing, so a timing-sensitive lane measurement taken in a repo carrying replacements is not a clean timing baseline. | S436 | git-replace.adoc:151 | "The existence of replace objects or commit grafts turns off reading or writing to the commit-graph, which can cause performance issues." |

## Host rows (git 2.56.0 at /usr/bin/git, 2026-11-03)

Fixtures are scratch repos (`git init`, toplevel asserted equal to the
fixture dir before the first commit). `<orig>` is the oid a clean tree
stores; `<forged>` is a second object written with `git hash-object -w`;
the plant is `git -C "$D" replace <orig> <forged>`.

| row | measured on this host | re-derivation |
|---|---|---|
| H01 | Blob-level replacement (the C2/R shape): after replacing one blob, `git -C "$D" cat-file -p <orig>` and `git -C "$D" show HEAD:f.txt` both print the replacement's bytes (`forged bytes`), while `git -C "$D" ls-tree HEAD` still prints the stored original blob oid (`4b085e39…`) and `git -C "$D" rev-parse HEAD:f.txt` still prints that same original oid. The listed id and the bytes read for that id disagree. | fixture A in the receipt: `git replace <orig-blob> <forged-blob>`, then `cat-file -p <orig-blob>`, `show HEAD:f.txt`, `ls-tree HEAD`, `rev-parse HEAD:f.txt`; all rc 0 |
| H02 | Both escape hatches return the real bytes: `GIT_NO_REPLACE_OBJECTS=1 git -C "$D" cat-file -p <orig>` and `git --no-replace-objects -C "$D" show HEAD:f.txt` print `original bytes`; `git -C "$D" --no-replace-objects show HEAD:f.txt` also prints `original bytes` (the option works in both positions on 2.56.0, though K06 documents the just-after-git form). | fixture A in the receipt; four commands, all rc 0 |
| H03 | The variable is read for presence, not truth value: with the original blob replaced, an unset variable reads `forged bytes`, while `1`, `0`, the empty string, `true` and `false` all read `original bytes`. The config plane agrees in direction — `-c core.useReplaceRefs=false` reads real and `-c core.useReplaceRefs=true` reads forged — and a repo config cannot re-enable replacement against the process guard (`env=0 + core.useReplaceRefs=true` reads real). | fixture A in the receipt; six env forms and four config forms, each `cat-file -p <orig>` |
| H04 | Tree-level replacement changes what listings and path resolution return: after replacing a tree with a same-named tree built by `git mktree` over a forged blob, `git -C "$D" ls-tree -r HEAD` prints the replacement tree's blob oid (`114ecba9…` instead of `17e3475…`) and `git -C "$D" rev-parse HEAD:a.txt` returns the forged oid; `GIT_NO_REPLACE_OBJECTS=1` restores both (`17e3475…`). | fixture B in the receipt: `mktree`, `git replace <tree> <forged-tree>`, `ls-tree -r HEAD`, `rev-parse HEAD:a.txt`, guarded repeat |
| H05 | Commit-level replacement does the same one level up: after replacing a commit with a `commit-tree` commit over a different tree, `git -C "$D" ls-tree -r HEAD` lists the replacement commit's tree entries and `git -C "$D" rev-parse HEAD^{tree}` returns the replacement tree oid (`9540a65…` instead of `91ebfad…`); the guard restores `91ebfad…`. | fixture C in the receipt: `write-tree`, `commit-tree`, `git replace <commit> <forged-commit>`, `ls-tree -r HEAD`, `rev-parse HEAD^{tree}`, guarded repeats |
| H06 | The guard ignores replacements; it does not hide or delete them: under `GIT_NO_REPLACE_OBJECTS=1`, `git -C "$D" for-each-ref refs/replace --format='%(refname) %(objectname)'` still prints `refs/replace/<orig> <forged>` and `git -C "$D" replace -l` still lists `<orig>`. Detection is therefore a separate channel a lane must install itself. | fixture A in the receipt; both enumeration commands rc 0 |
| H07 | Name resolution is not rewritten: `git -C "$D" rev-parse HEAD` prints the same commit oid with and without the guard (the ref still points at the original commit). The replacement is applied when an object's content is dereferenced, which is why a printed revision can be correct while the bytes read under it are not. | fixture A in the receipt; two `rev-parse HEAD` calls, equal output |

## Finding

**F01 — the "ls-tree object ids are not rewritten" phrasing is true only at
the blob level.** The seat brief for this entry stated that a replacement
rewrites what `git show`/`cat-file` consumers read but not `ls-tree` object
ids. Measured on 2.56.0, that holds for a replaced *blob* only while the
tree and commit being traversed are not themselves replaced (H01: listing
prints the stored original blob oid, reads return the replacement's bytes).
A replaced *tree* rewrites the listing and path resolution (H04), and a
replaced *commit* rewrites both the listing and `rev-parse <rev>^{tree}`
(H05). The rule that survives both shapes is two-level: the 40-hex names
that refs and tree entries store survive name resolution (H07), while every
dereference of a replaced object returns the replacement — so a listing
prints the ids stored in whatever tree object it read, following a replaced
tree or commit but not a replaced blob. For lane tooling this means `ls-tree` output is
not an integrity check against a tree- or commit-level replacement, and the
process guard (or `core.useReplaceRefs=false`) is the only layer measured
here that restores the real objects.

## Lane instruments that read objects through git

Census at the freeze revision `061dc329` (lexical, read-only: a file that
mentions `git` as a token, or `show`/`cat-file`, may still use it only to
build its own fixtures). Commands and outputs, run in the lane root:

```
# 82 files under quality/ and tools/ mention a git command token
git grep -l -E '(^|[^A-Za-z0-9_-])git([^A-Za-z0-9_-]|$)' 061dc329 -- quality tools | wc -l
# 79 of them contain show or cat-file (an upper bound on object-content
# readers, not a per-call proof)
git grep -l -E '(^|[^A-Za-z0-9_-])(show|cat-file)([^A-Za-z0-9_-]|$)' 061dc329 -- quality tools | wc -l
# 3 set the guard
git grep -l GIT_NO_REPLACE_OBJECTS 061dc329 -- quality tools
# -> quality/counters/c1-r56-autoreload-entry.py
# -> quality/counters/c1-r66-register.py
# -> quality/landing-counters.sh
```

The standing instrument's legs at `061dc329` read objects as follows:

| leg | what it reads | guard state at `061dc329` |
|---|---|---|
| `quality/landing-counters.sh` nav leg (inline python, `landing-counters.sh:24-28`) | `git ls-tree --name-only <rev>:corpus/knowledge` names and `git show <rev>:corpus/README.md` bytes | the script exports `GIT_NO_REPLACE_OBJECTS=1` at line 8, and the inline child inherits the process environment |
| `quality/counters/c3-r56-used-by.py` (`git_env` at `:59-69`, reads at `:100` and `:121`) | `git ls-tree -z <sha> -- <path>` ids, then `git cat-file blob <oid>` bytes | no guard: the env dict is built from scratch, so the parent export does not reach it |
| `quality/check-tool-ledger.py` (`git_env` at `:101-110`, reads at `:145` and `:162`) | `git ls-tree -r -z <sha>` ids and `git show <sha>:<path>` bytes | no guard: `GIT_ENV_KEYS` is `PATH`/`SYSTEMROOT` (`:79`), and the env is built from scratch |
| `tools/mado-receipt-citecheck.py` (`:100-101`) | `git ls-tree -r --name-only <rev>` names only | no explicit env (the child inherits `os.environ`); names can still be rewritten by a tree/commit replacement (H04/H05) |
| `quality/counters/c1-r66-register.py` (`:42-45`) | `git show` bytes at `--rev` | guarded: `env.update(... GIT_NO_REPLACE_OBJECTS="1")` |
| `quality/counters/c1-r65-register.py` (`:84-90`) | `git show` and `ls-tree` at `--rev` | no guard at the freeze revision (`env = dict(os.environ)` plus lock/locale keys only) |

Therefore: any leg that reads object bytes under a `--rev` it also prints
needs the key in its own env constructor (the parent's `export` covers only
children that inherit the environment). The r67 C2 dispatch names the three
children of the standing instrument — `c3-r56-used-by.py`,
`check-tool-ledger.py`, `mado-receipt-citecheck.py` — as the ones that gain
`GIT_NO_REPLACE_OBJECTS=1` this round (`.ufo/waves/round-67/w1-dispatch.json`,
R67ExecChildren task text); the r67 C1 counter is specified with the same
key. The 76 unguarded files in that lexical content-reader set remain a
declared residual, not a claim of this round.

## What the round's R control proves, and what it does not

The frozen R control is: a fixture repo in which the used-by child legitimately
scores `TARGET_MISSED` (a SOURCES row whose used-by names a missing knowledge
file), plus a planted `refs/replace` ref that would make the child read the
forged bytes and score `TARGET_MET`; the candidate control passes only when
the child still reports the real verdict, and the M-R mutant deletes exactly
the added guard key line from the child's env constructor
(`claims-declaration-r67.md:86-92`; `w1-dispatch.json`, R67ExecHarness task
text).

What it proves, on that fixture and that child:

- with the key present, the child's verdict does not move under the planted
  replacement, i.e. the child read the real object bytes (H01's guarded
  branch, reproduced as the child's own env shape in
  `control-baseline-r67.txt`: `child_env_read=forged guarded_read=real`);
- deleting exactly that one key line is load-bearing: the mutant reads the
  forged view, the control exits nonzero on it, and the unmutated candidate
  control exits 0. That is a two-mutant, two-control statement, which is the
  claim's own declared limit.

What it does not prove:

- **No protection against a repo already rewritten.** If the measured
  commit's objects were rewritten in place (no `refs/replace` at all), the
  guard has nothing to ignore and the child reads the rewritten objects as
  the repo's truth. The control plants a ref; it does not detect a repo whose
  history was genuinely replaced.
- **No authenticity.** "Real objects" means the objects this repository
  stores, not objects that are authorized, signed, or expected. Nothing in
  the control signs, pins by digest, or allowlists.
- **No truth of state cells.** A valid receipt read honestly still does not
  make a PROVINCE row's prose true; the claim is a read-path property, not a
  register-truth property.
- **No universal fault coverage.** The claim is exactly M-Z and M-R on the
  frozen controls; the census above shows 79 lexical content readers and 3
  guarded files at the freeze revision, and the 76 unguarded files in that
  set are not covered.
- **No detection or reporting.** The guard silently ignores replacements
  (H06: `refs/replace` still enumerates); a lane that wants to notice a
  plant must add its own check.
- **No statement about arrival of a replacement ref.** How a `refs/replace`
  ref could be introduced by clone/fetch is not in this file and was not
  measured here; the control plants it locally with `git replace`.

## Limits and unknowns

- The S436 anchor names no `pin` path (the tag's adoc is not in the lane
  tree), so a criterion-107 run reads `eof=unchecked` for these rows; the
  line numbers were checked by hand against the fetched bytes (5398 bytes,
  168 lines) and recorded in the receipt.
- The instrument census is lexical (82/79/3 at `061dc329`); it bounds
  exposure, it does not prove any single file's call sites.
- Clone/fetch transfer of replacement refs: unmeasured, and not asserted by
  the document.
- Detection is not installed by r67; only ignoring is.
- The type rule (K03) is bypassable with `-f`, so type sameness is not a
  trust property.
- No desktop, compositor, session or service surface was read or written.

## Recheck and provenance

- Fetch: `curl -fsSL -o git-replace.adoc https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc`;
  `sha256sum` → `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631`,
  5398 bytes; tag `v2.56.0`; host `git --version` → `git version 2.56.0`.
- Host rows: re-run the fixture shapes in §2 against any git on the host;
  the oid values quoted are fixture-local and will differ per run, the
  relations (which side prints the replacement, which side restores) are the
  measured claim.
- Cadence: on-release. When the host git leaves 2.56.0, re-fetch the tag's
  file, re-hash it, and re-run H01-H07; when the standing instrument's child
  set changes, re-run the §4 census and re-check which legs build an env
  from scratch.
