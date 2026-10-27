# mado round 48 — registration v2 (frozen BEFORE any round-48 data commit; L1 attempt 3)

Supersedes both predicates of `registration.md` (freeze `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`), through the path that
file declares before any scoring: "W2 may find a pre-data hole; only before data may L1 re-register as a new version and
re-run the complete control set. After data, the predicate and kill rule are immutable." No data commit exists: above
the base `579f694b` the lane carries only the setup `5ff16742` (claims, w1 spec) and the v1 freeze `3e6c848a`;
`corpus/knowledge/xkb-keymap-compile-r48.md`, rows S340-S350 and the extended `tools/mado-terminal.py` are absent from
every committed revision. Claims, axes, surfaces, the lowest-axis argument, separability and the routed non-claim items
are `claims.md`/`registration.md`'s, unchanged.

Disclosure, so the judge can weigh it: the w2 falsify wave (48 seats) scored the **v1** instruments against the data
candidates committed with the v1 freeze (`l1-draft/`), and v2 was written by the L1 after reading those results. v2 is
therefore not blind to w2. What makes it more than a re-aim is the control set below: every candidate a w2 seat built
to break v1 (and every w1 control) is re-scored against v2 and must miss, and the v1 counters are also run at the data
commit and reported beside v2 (`PRED-C1-r48`, `PRED-C2-r48`), so the closure can rule on either.

## Why (w2 findings that break v1's own control rule or its registered contract text)

| finding | seat | v1 behaviour | registration text it breaks |
|---|---|---|---|
| B1: a tool that performs the resolver's cache save and swallows EROFS meets | `w2/RevC1Counter`, `w2/MutC1ReadOnly` M-WRITE | `TARGET_MET` | §C1 Contract "no subprocess, socket or file write"; `writes-cache` is a registered control that "must miss" |
| M-FORK: a tool that forks (no exec) meets | `w2/MutC1ReadOnly` | `TARGET_MET` | "no subprocess" |
| B2: `--print-content` on a hit whose cached path is live and differs from cold is unscored | `w2/RevC1Counter` (`content-cold2`) | `TARGET_MET` | the C1 claim itself ("a stale-but-valid cache can make SUPER+RETURN start a different command") |
| G1: `command -v` executability (exists without +x) unscored | `w2/MutC1Tool` (`m4-break-cmdv`) | `TARGET_MET` | §C1 Contract (the resolver gates on `command -v`) |
| F1: the LF reconstruction of a multi-line cached command unscored | `w2/RevC1Cache` (`joinless`) | `TARGET_MET` | §C1 clause w "cache parser" |
| F2: an unreadable cache (`invalid`, not `absent`) unscored | `w2/RevC1Cache` (`unreadable_absent`) | `TARGET_MET` | §C1 "cache states" |
| `-L`: no fixture can make a symlink, so a no-dereference `ls` meets | `w2/RevC1Ls` (`m3-no-deref`) | `TARGET_MET` | §C1 "`gen_hash` must be byte-equal to `LC_ALL=C LANG=C ls -LRl`" |
| pin mode not enforced | `w2/RevC2Counter` (`c-pin-mode-S340`) | `admitted=1` | the C2 counter's own clause c text ("mode 100644") |
| a quote span over 600 characters is dropped, not refused | `w2/RevC2Counter` (`x-quote-600-invisible`) | `admitted=1` | §C2 clause d (quotes ≤25 words at their pin ranges) |
| clause x's three `--observed` captures are all rooted in the tool's own tree, so a basename comparator agrees | `w2/RevC1Explain` F1 (`observed-basename`) | `TARGET_MET` | §C1 clause x (AGREE/DIFFER both ways) |
| an empty cached command word, and a newline inside the first one, are unscored | `w2/RevC1Explain` F2/F3 (`cmd-empty-word-dropped`, `cmd-argv0-newline`) | `TARGET_MET` | §C1 clause w/x (the cached command) |
| a default-location (`$HOME/.cache`) warm cache, `XTE_CACHE_ENABLED=''` and a directory at the cache path are unscored | `w2/CritDataCompleteness` C1-A/B/C | (omission) | §C1 "cache states" |
| clause r's replay judge is whatever `xkbcli` the caller's PATH finds | `w2/MutC2Replay` (PATH shim, A2) | `admitted=1` | §C2 Residuals ("replay independently proves the live compiler output") |
| step 8's NULL rests on internal helpers that return false; the public call is unpinned | `w2/CritDataCompleteness` C2-A | (evidence gap) | §C2 contract (the compositor-visible NULL) |

## C1 — `PRED-C1-r48-v2` (replaces `PRED-C1-r48`)

- **Counter** `quality/counters/c1-r48-terminal-cache-v2.py` (= `l1-draft/v2/`), v1 byte for byte except: clause r traces
  `fork vfork clone clone3` with the process set, and in every tool run except the clause-s selftest a write
  **attempt** (open/openat/openat2 with O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND, creat, mkdir(at), rmdir,
  unlink(at), rename(at/at2), link(at), symlink(at), truncate, ftruncate, mknod(at)) is a trip; the python3 execve is
  recognised when strace splits it (`<... execve resumed>`; v1 skipped resumed lines first, which read as
  `python-execve-not-seen` once more syscalls were traced: `receipts/v2/ref.txt` first run, trips=43 of that kind only);
  schema v2 gains `links` {path: target} (top level and in `after`) and applies a `.rw/` mode only to a tree with a
  cache, after the cache edits; clause x adds a fourth `--observed` capture - the oracle's capture with its root replaced
  by `/r48-foreign-root` - that must read DIFFER/1, and compares `cmd=` with each newline in the word written as the two
  characters `\n` (the form the tool's one-line explain now prints). `PRED`, final line and clause labels read
  `PRED-C1-r48-v2`.
- **Fixtures** `quality/counters/c1-r48-fixtures-v2.json` (sha256 `3ab1f5d0e7e382ea1949195689177aa135af83d07eddaccf449ece24aa8e51ef`, pinned
  in the counter) = the 204 v1 fixtures unchanged + 24 measured from the pin by `l1-draft/v2/add-fixtures-v2.py` (three
  identical runs each, receipt `receipts/l1-v2-add-fixtures.txt`): L1-11..16 live cached path with `--print-content`
  (B2, `WARM-DIFFERS`), L1-17/18 non-executable `Exec[0]` warm and cold (G1), L1-19/20 multi-line cached command (F1),
  L1-21 mode-000 cache (F2, `invalid`), L1-22..28 symlinks: operand dir, entry file, dangling entry, dangling revived,
  chain, sibling twins, data home (`-L`), L1-29/30 default-location cache hit and same-size edit (C1-A), L1-31
  `XTE_CACHE_ENABLED=''` (C1-B, `disabled`), L1-32 a directory at the cache path (C1-C, `absent`), L1-33 an empty cached
  command word, L1-34 a newline inside the first cached command word (RevC1Explain F2/F3). Cold fixtures
  (`c1-r47-fixtures.json`), pin, clauses a/s/f/g/i, selftest minimum 60, nonce rule and `--work` rules are v1's.
- **Command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r48-terminal-cache-v2.py --repo . --rev <rev> --work <scratch outside the lane> [--nonce N]`.
- **Target:** `cold=190/190 warm=228/228 explained=418/418 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0, at the data commit and the final tip. Any other result is a miss. Before: the base tool (`579f694b:tools/mado-terminal.py`) under v2 (`receipts/v2/ctl/BASE.txt`).
- **Contract amendments (the tool, not the counter):** the ls-environment out-of-contract guard runs on every path, not
  only where the hash is computed (`w2/CritC1LsEnv`: with `POSIXLY_CORRECT=1` the resolver exits 1 on a cold run while the
  v1 tool answered `foot`); selftest case `ls-env-out-of-contract-without-hash` (70/70); explain's `cmd=` writes a newline inside the first command word as `\n`
  (RevC1Explain F3: the v1 line broke in two and could not be parsed). Out-of-contract classes are
  declared in the counter's residual paragraph (six-month boundary second, ACL/xattr, newline names, the six ls
  variables, FIFO candidates, symlink loops); none is reached by a fixture and none is scored.
- **Control table corrections (`w2/RevC1Counter` §5):** clause f is the round-47 cold harm watch and catches no warm
  rule; `trust-any` misses on s+w+x, `no-line-limit` on s+x only (it passes w).
- **Controls:** `l1-draft/v2/run-ctl-c1v2.sh` scores 64 candidates (the 19 w1 controls, the 6 w1 refA mutants, 7
  `RevC1Counter`, 7 `MutC1ReadOnly`, 8 `MutC1Tool`, 4 `RevC1Cache`, 2 `RevC1Ls`, 11 `RevC1Explain`) plus the base tool
  and an absent tool, the landed tool, and (reported only) the frozen v1 reference; receipt `receipts/v2/ctl-c1v2.txt`
  (per-candidate receipts `receipts/v2/ctl/`). Required: every candidate `TARGET_MISSED` (an absent tool is a setup
  error, exit 2, as in v1, and counts as a miss) and the landed tool `TARGET_MET`. The frozen reference is not required
  to meet: v2 scores explain's escaped newline (L1-34), which the v1 reference prints raw.

## C2 — `PRED-C2-r48-v2` (replaces `PRED-C2-r48`)

- **Counter** `quality/counters/c2-r48-xkb-entry-v2.py`: v1 byte for byte except clause c checks every row-bound
  round-48 pin is mode 100644 at REV, and `QUOTE_RE` has no 600-character cap, so an over-long span meets the 25-word
  refusal; clause r's replay runs `/usr/bin/xkbcli` (no PATH lookup) with a clean environment (`PATH=/usr/bin`,
  `LANG=C.UTF-8`, scratch `HOME`/`XDG_*`): a PATH shim moves v1 (`receipts/v2/c2-shim-c2-r48-xkb-entry.txt`, `r:0`) and
  not v2 (`-v2.txt`, admitted). Label `PRED-C2-r48-v2`.
- **Command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && TMPDIR=<scratch> python3 -I quality/counters/c2-r48-xkb-entry-v2.py --repo . --rev <rev>`.
- **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0, at the data commit and the final tip; base `admitted=0/1`.
- **Controls:** `w2/RevC2Counter`'s 98-variant harness re-run with the v2 counter (`l1-draft/v2/c2v2-harness-revc2counter.py`,
  receipts `receipts/v2/c2v2-revc2counter-matrix.txt`, `-summary.json`): exactly two verdicts flip against v1
  (`c-pin-mode-S340`, `x-quote-600-invisible`: admitted → missed); the 11 variants still admitted are the seat's own
  declared residuals or cosmetic notes (self-consistent tamper, self-pin, untrusted receipt prose, 40-hex ref, README
  closing pipe, future recheck, corpus-wide ground terms, extra/relabelled digests, e-boundary, same-basename pin).
- **Entry repairs before data (prose; no clause reads them):** step 9 severity split (`w2/RevC2Entry` M1,
  `CritQualityTrend` §4.1), the `--model nope` cell (`CritC2FalseClaim` F1), the second WARNING (F2), three ruleset files
  plus the `xorg` symlink (F3), include-path precedence attribution (F4, `RevC2Entry` L1), the models gloss (N1),
  `kb_file` wording and the compositor's shared libxkbcommon (`RevXkbIntent` LOW-2/LOW-3), the README locator after the
  data lands (`ScoutEntryLocators`), the recheck line's pin count and release/host triggers (`CritC2Pin` F2/F6); rows
  S340/S349 gain the locators the entry uses (`CritC2Pin` F4). New row **S351** (libxkbcommon 1.13.2 `src/keymap.c`,
  pin `fetch/xkbcommon-keymap.c`, opened 2026-10-26) grounds step 8's NULL at the public `xkb_keymap_new_from_names`
  (`xkbcommon-keymap.c:173-176`, `:183-189`; `w2/CritDataCompleteness` C2-A); the README row covers S340-S351.

## Kill rule and immutability

Each predicate is judged once at the data commit and once at the final tip with the commands above. A miss is reported
as a miss; after the data commit nothing in this file, either v2 counter or the v2 fixture file changes.

## Residuals carried (declared, not repaired)

The receipt header names its generator under `receipts/` while the generator is committed under `tools/` (frozen bytes;
`w2/ConnSourceLinks` 2, `RevXkbIntent` LOW-1, `SentHost` F1); `fetch/xkbcommon-meson.build` is a pin no row cites
(`CritC2Pin` F5); S346's generator chain is not self-verifying (`CritC2Pin` F1); C2's trust root is the mutual binding of
copy and row digest; owner-column justification is unscored (no chown in a fixture); C1's judge is this host's
coreutils/bash.
