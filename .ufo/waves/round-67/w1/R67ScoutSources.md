# R67ScoutSources — independent source binding (mado round 67, seat scout)

Read-only seat. Base `0b28ffb4baac9586566d246c3f0986b2bb650a33`, freeze
`061dc329b598b2723a224b6c7b305b436946ec91`. All fetches and fixtures ran under
`/fast/scratch/hyaku/mado-r67/R67ScoutSources/` (removed before yield).

## 1. Source binding (C2 replacement-ref semantics)

| item | value |
|---|---|
| canonical URL | `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc` |
| secondary URL | `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc` |
| access date | 2026-11-03 |
| sha256 (git-replace.adoc, 5398 B) | `3f61be3f0ea0426cf1e075929819b9a6bce240c6955cfd25d99fb2c974640631` |
| sha256 (git.adoc, 47005 B) | `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79` |
| version pin | tag `v2.56.0` → tag object `2478544319491bbd2a42cc57a83e3d2f4730a280`, peeled commit `a018953688f1b10bddf91bff8747068f5f4746a4` (independently confirmed by read-only `git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'`, rc 0) |

Located quotes (the sentence IS in git-replace.adoc; no fallback needed for the
equivalence claim, and git.adoc carries the ignore claim):

1. `Documentation/git-replace.adoc`, section `DESCRIPTION` (heading line 18),
   **lines 55-56**, 16 words:
   > The `GIT_NO_REPLACE_OBJECTS` environment variable can be set to achieve the same effect as the `--no-replace-objects` option.
2. `Documentation/git.adoc`, section "Environment Variables" (heading line 478),
   entry `GIT_NO_REPLACE_OBJECTS` at **line 927**, quote **lines 928-929**, 18 words:
   > Setting and exporting this environment variable tells Git to ignore replacement refs and do not replace Git objects.

Supporting but out of quote budget: `git-replace.adoc:34-36` — replacement refs
are used by default by all Git commands except reachability traversal
(prune, pack transfer, fsck).

## 2. Local git and installed documentation agreement

What I actually opened / ran:

- `git --version` → `git version 2.56.0` (rc 0).
- `pacman -Q git` → `git 2.56.0-1`; `pacman -Qo /usr/share/man/man1/git-replace.1.gz`
  → `is owned by git 2.56.0-1` (read-only query, no transaction).
- `man -P cat git-replace` → rendered page carries the same sentence at
  rendered lines 45-46 ("The GIT_NO_REPLACE_OBJECTS environment variable can be
  set to achieve the same effect as the --no-replace-objects option."), footer
  `Git 2.56.0   2026-09-27   GIT-REPLACE(1)`.
- `git --html-path` prints `/usr/share/doc/git-doc`, but that directory does
  **not** exist on this host — no HTML docs installed, so the man page is the
  only local rendering.
- `git --man-path` → `/usr/share/man`.

Verdict: local git and installed docs are 2.56.0 and agree with the fetched
tagged bytes on the two sentences used. The local man page is generated
(pod2man) so its bytes are not comparable; only the sentence-level agreement is
claimed.

## 3. SOURCES id, row-check and duplicate verdict

- Registry census: `corpus/SOURCES.md` = 372 rows matching `^| S\d{3}`, no
  duplicate ids, **max id `S435` → next unused id `S436`**. Ids are not
  contiguous (gaps below S435), so "next unused" was computed from the maximum
  present id, not from the row count. Census start file
  `.ufo/waves/round-67/census-start-r67.txt` (exit 0) records the same path.
- **Duplicate-URL verdict: NO collision (census W04 clean).** The canonical
  `.../v2.56.0/Documentation/git-replace.adoc` URL has **0 occurrences** in
  `corpus/SOURCES.md`. `raw.githubusercontent.com/git/git/` appears 5 times, all
  for *different files at the same tag*: S099 `git-commit.adoc`, S100
  `git-add.adoc`, S101 `git-push.adoc`, S102 `git.c` + `parse-options.c` +
  `builtin/help.c` + `gitcli.adoc`, S118 `builtin/commit.c`. Source-family
  precedent, not a URL duplicate; no `git-scm.com` row exists.
- Row shape the scribes must append (11 columns verified against the registry
  header `| id | source | kind | tier | scope | anchor | teaches | status |
  opened | recheck | used-by |`), no literal `|`, no `\|`, kind `docs`, tier `A`
  scoped to lane-instrument object reads, anchor tag-pinned (no `latest`/`main`),
  opened `2026-11-03`, status `mined`, `recheck` `on-release`, used-by names the
  lesson and the knowledge entry — reference text written to
  `.ufo/waves/round-67/w1/R67ScoutSources/row-candidate.txt`, sha256
  `8318e4e85277404f71919450e562a90bfc2082fd399a11041e2c830eaa178221`.
  The block below is that single line with the two file sha256 values abbreviated
  to `…` for width; the file holds the unabbreviated text.

```
| S436 | git v2.56.0 Documentation — git-replace.adoc + git.adoc Environment Variables — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-replace.adoc | docs | A | lane-instrument object reads: what a refs/replace entry rewrites and how to make a git child read real objects | Documentation/git-replace.adoc:55-56 (DESCRIPTION) + Documentation/git.adoc:478,927-929 (Environment Variables) @ tag v2.56.0 (git-replace.adoc sha256 3f61be3f…, git.adoc sha256 050c5330…) | Two sentences: the env variable is equivalent to --no-replace-objects, and setting and exporting it tells Git to ignore replacement refs. Scoped to lane instruments that read objects through git, never to repo authenticity or state-cell truth. | mined | 2026-11-03 | on-release | corpus/lessons/round-67.md, corpus/knowledge/replace-ref-citation-boundaries-r67.md |
```

Check performed programmatically: 11 cells after splitting on `|`, `'\|' in row`
False, every required cell present, id absent from the registry, both URLs
absent from the registry. The scribes' `draft/corpus/SOURCES-row.txt` did not
exist at scout time (only `R67Exec*` and `R67RevRegister` drafts were on disk),
so this is the validating reference rather than a review of their text; the
lesson Gate should diff their row against it.

## 4. Rejected candidate + flip (for the lesson Gate)

**Rejected: `https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/config/core.adoc:761-764` (`core.useReplaceRefs`)**, sha256
`aa6015220b25a284408fa5e03bba40b70fcc69fe1a03a60859e019a84a2c9f5d`. The key
really exists and says "If set to `false`, behave as if the `--no-replace-objects`
option was given on the command line". Reason for rejection: it grounds the
*config-file* plane, which a fixture repository controls through its own
`.git/config`; C2's M-R mutant deletes a **process-level** env key line, and a
child that reads objects must be protected against a repository that could set
`core.useReplaceRefs=true`. Measured confirmation that the env var is not
overridden by config: `replace-object.h:26-31` states replacement is active iff
`disable_replace_refs()` not called **and** `GIT_NO_REPLACE_OBJECTS` unset/zero
**and** the repo does not have `core.useReplaceRefs=false` — a conjunction, so
config cannot re-enable what the env var switched off. Flip: if a future entry
claims config-plane defense (setting both planes), or a tag sentence states
env-over-config precedence that makes the config row independently usable,
admit it as a second row.

**Second rejection (cheaper, if the Gate wants a same-file alternative):**
`Documentation/git-config.adoc` at the same tag, sha256
`655541c20fe58e30c2e45803df422a5a1ed3658bf025ceaed6c1764089edcd27` — it holds
**0** occurrences of `GIT_NO_REPLACE_OBJECTS`; its 22 case-insensitive "replace"
hits are all `--replace-all` / "Replaced by" text, and the config keys live in
the file it includes at line 635 (`include::config.adoc[]`), not in itself.
Flip: the tag's git-config.adoc itself gaining a documented replacement-ref key.

## 5. R65 live-receipt binding for C1 (the literal the predicate pins)

`git show 061dc329b598b2723a224b6c7b305b436946ec91:.ufo/waves/round-65/receipts/gate-live-r65.txt`

- sha256 `676ba88b484e194d4962ee27d07a54b5b7441a8461256b0f3ea0c83d1910e8ed`, 6516 B, 66 lines, trailing newline present.
- Git blob is `88cd0232780239dc4a75b48a2b3df6f36dd998f1` at **both** base `0b28ffb4` and freeze `061dc329` — the C1 literal is byte-stable across the round boundary.
- CLEAN literal is **line 65**, exactly one occurrence in the file, byte-identical to
  `.ufo/waves/round-67/controls/c1-controls.json` → `live_line`:
  `MADO_VERIFY: CLEAN (52 pass, 8 notes; file + live planes verified read-only)`
- line 66 is `rc=0`; `cases[0].objects[".ufo/waves/round-65/receipts/gate-live-r65.txt"]`
  equals that literal plus `\n`. So a register row citing the live path with
  this identical line is the only shape the `genuine` control accepts.

## 6. Measured replacement-ref behaviour (fixture, git 2.56.0-1)

Fixture `D=$(mktemp -d "$S/fixture.XXXX")`, `git -C "$D" init -q`, toplevel
verified equal to `$D` before the first commit; commits `A=68f1d484…` ("commit-one")
and `B=17d3af95…` ("commit-two", child of A); `git -C "$D" replace A B`.

| invocation | `git log --oneline -n 2` second line | verdict |
|---|---|---|
| unset | `68f1d48 commit-two` | replacement ACTIVE |
| `GIT_NO_REPLACE_OBJECTS=1` | `68f1d48 commit-one` | ignored |
| `GIT_NO_REPLACE_OBJECTS=0` | `68f1d48 commit-one` | **ignored (presence, not truthiness)** |
| `GIT_NO_REPLACE_OBJECTS=` (empty) | `68f1d48 commit-one` | ignored |
| `-c core.useReplaceRefs=false` | `68f1d48 commit-one` | ignored |
| `-c core.useReplaceRefs=true` | `68f1d48 commit-two` | active |

Two findings for the lesson/knowledge entry, both from execution:

1. **Presence, not value.** `common-init.c:42` (`if (getenv(NO_REPLACE_OBJECTS_ENVIRONMENT)) disable_replace_refs();`)
   tests presence only, and the fixture confirms `=0` and `=` both disable.
   This contradicts the in-tree header comment `replace-object.h:29`
   ("`GIT_NO_REPLACE_OBJECTS` is unset or zero"), which is stale as a statement
   of the code. Consequence for C2: a child that sets the variable to any value
   is guarded; a child that *unsets* it is not — the guard must be the presence
   of the key in the env constructor, exactly the line M-R deletes.
2. **`ls-tree` object ids ARE rewritten.** Planner's planned sentence in the
   knowledge-entry spec ("rewrites what `git show`/cat-file consumers read but
   not `ls-tree` object ids") is false as measured: under replacement
   `git -C "$D" ls-tree A` prints blob `814f4a42…` (B's `one\ntwo\n`), guarded it
   prints `5626abf0…` (A's `one\n`); `rev-parse A^{tree}` gives `d3a57765…`
   versus `7385b9ca…`. What replacement does **not** rewrite is the 40-hex
   *name*: `git rev-parse A` returns `68f1d484…` in both modes. The entry should
   say "every content dereference — `show`, `cat-file`, `ls-tree`, `rev-parse
   <rev>^{tree}` — returns the replacement's bytes; only the oid *spelling*
   survives".

## 7. Commands, exit codes

| command | rc |
|---|---|
| `curl -fsSL -o … raw.githubusercontent.com/git/git/v2.56.0/Documentation/{git-replace,git,git-config}.adoc` | 0 (5398 / 47005 / 21576 B) |
| `curl … Documentation/config/core.adoc`, `repo-settings.c`, `replace-object.{c,h}`, `repository.c`, `setup.c`, `object-file.c`, `config.c`, `environment.c`, `git.c` | 0 |
| `curl … codeload.github.com/git/git/tar.gz/refs/tags/v2.56.0` | 0 (12789076 B, sha256 `d761232b81394f7d4c3ef1a99fa804ffbe10d278ae1ad302833a0892050ca9fc`) |
| `git ls-remote https://github.com/git/git refs/tags/v2.56.0 'refs/tags/v2.56.0^{}'` | 0 |
| `git show 061dc329:…/gate-live-r65.txt` | 0 |
| fixture `init`/`commit`/`replace`/`log`/`ls-tree`/`rev-parse`/`cat-file` | 0 |
| `grep -c GIT_NO_REPLACE_OBJECTS git-config.adoc` | 1 (0 matches — the rejection evidence) |

No git mutation in the lane, the fleet repo or any sibling lane: the only
mutating git calls were `init`/`config`/`add`/`commit`/`replace` inside the
mktemp fixture under scratch, each addressed with `git -C "$D"`, toplevel
asserted equal to `$D` first. No commit, push, stage, stash, checkout, switch or
reset anywhere. No packages installed or upgraded (nothing was needed; pacman
not invoked in mutating mode — `pacman -Q`/`-Qo` read-only queries only).
Scratch `/fast/scratch/hyaku/mado-r67/R67ScoutSources/` removed before yield.

## Remaining unknowns

- The `genuine` C1 case's accept path beyond the receipt literal (counter
  implementation is L1/executor-owned; not inspected by this seat).
- Whether the scribes' `used-by` cell will name the lesson and the knowledge
  entry exactly as above — their drafts did not exist when this seat closed.
- Whether `core.useReplaceRefs` ever needs a second row (depends on the Gate's
  flip test, §4).
