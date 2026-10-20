# FleetToolScan — prior-art scan for transcript scanners / command tripwires

Seat: `MadoR17.FleetToolScan` (scout, leaf). Round 17, wave 1. Read-only.
Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; lane tip at scan time
`0175f13d83dceb9344fd0ecc5f94aa4aac5dfb53`.

Axes (the only ones this seat moves):

1. **True-negative safety** — is "no existing tripwire" a claim that survives a
   widened net, not just the two assigned directories?
2. **Overlap precision** — separate genuine overlap from keyword collisions, so
   L1 does not absorb a tool with a different input contract.
3. **Handoff cost** — each row must be actionable without re-deriving it.
4. **Anchor durability** — every claim carries path + sha256 + revision.

Move kept only where it improves one axis and harms none: report, never absorb.

## 0. Compliance

- Host pause honoured: **no** `pacman`/`yay`/`paru` (not even `-Q`/`-Si`), no
  `sudo`, no `systemctl`/`hyprctl`/`libinput`/terminal/waybar/walker/hypridle
  invocation, no screenshots, no input probes. All evidence is file bytes plus
  read-only git plumbing (`git log`, `git rev-parse`); no `jj`.
- No writes outside this report. No sibling `.ufo/waves` read.
- No tool installed or upgraded; no network fetch.

## 1. Method

Scope as assigned: every `*-shokunin/tools/` tree and `scripts/`.

- 8 lanes carry `tools/` — chousa(1 file), kama(4), kotodama(366, of which the
  bulk are `gates/frozen`/`gates/expected` snapshots), mado(2), mori(8),
  souji(121), tameshi(7), tsukuroi(6) = **515 files** (`__pycache__` excluded).
- `scripts/` = **25 files** (`fixtures/`, `hyaku/`, two top-level gates).
- Greps run, in scope: `toolCall|tool_call_id`, `jsonl`, `sessions`,
  `pacman|sudo|host_mutation|live_probe|package_query|tripwire`, `shlex`,
  literal `"bash"|"eval"|"sh"|"zsh"` name tables, `assistant`/`content[{`
  JSON-shape fragments, and a filename net (`*tripwire*`, `*transcript*`,
  `*scan*.{sh,py}`, `*guard*.sh`). Then one hop outside the fleet for the
  adjacent OMP runtime, because a fleet-local scanner would have to match its
  envelope.

## 2. Verdict

**No transcript command tripwire exists in the assigned directories, and none
exists anywhere in the fleet that reads OMP session JSONL commands.**

- `toolCall` / `tool_call_id`: **zero hits** across all `*/tools` and `scripts`.
- No file in scope opens `/home/vgpnk/.omp/agent/sessions` or parses a
  transcript's `message.content[]`. The `.omp/agent` references in scope are
  all *boundary* facts, never reads: protected-root/prefix tables in three
  souji tools (`souji-census.sh:60-90,205-265`;
  `souji-evidence-cache.py:124,307`; `souji-preservation-evidence.py:160,394`),
  one fixture path string (`chousa-shokunin/tools/research-gate.sh:3483`), and
  advisory prose (`scripts/hyaku/lane-addendum.md:78`).
- The only in-scope tool that classifies dangerous commands is
  `mado-shokunin/tools/mado-action-plan.py`, and it classifies a **declared
  JSON plan before execution** — it never reads a transcript.

So C3's tripwire has no predecessor to reuse and no duplicate to displace. The
rows below are the artifacts a reviewer *will* find when they grep the same
way, with the exact reason each is not the tripwire.

## 3. Genuine overlap (reported, not absorbed)

| # | Artifact | sha256 | What it actually is | Overlap | Gap vs `tools/mado-tripwire.py` |
|---|---|---|---|---|---|
| 1 | `mado-shokunin/tools/mado-action-plan.py` (906 L) | `226220ae41436506c048258aff15fff83577acf0ae71ffa955d585a18ba5aea3` | Round-16 pre-execution declared-plan gate | Same *semantic target* (host mutation), same deny vocabulary, same fail-closed `0/1/2` | Input is `{kind, argv}` JSON; `argv[0]` **basename only**, no `shlex`, no `;`/`&&`/pipe segmentation, no `bash -c` recursion, no `eval` at all. Its own docstring: "not arbitrary shell analysis". Cannot see the red anchor. |
| 2 | `kagi-shokunin/corpus/transcript-scan.sh` (282 L, kagi HEAD `c2cab35b`) | `2d60981b198cef41b9263a1427b41f92d98b65eb26ff71c28057bea0ad823a23` | **Post-hoc transcript tripwire**, registered gate at `kagi-shokunin/SKILL.md:44` | Two-tier HIT/WARN, `0/1/2` exits, `--selftest` with seeded hit + clean + WAL-resident fixtures, source never opened (snapshot copy to `mktemp`) | Different substrate (`sqlite3` CLI over `opencode.db`), different observable (secret-shape `LIKE` patterns), **not OMP JSONL**, **no command classification**. Lives in `corpus/` because kagi has no `tools/`. Do not absorb: the mado tool must stay `python3 -I` stdlib and must not gain a sqlite dependency. |
| 3 | `scripts/hyaku/await-capacity.sh` (16 L) | `cc5747b17e2d2b5ac033f91b6114c31e40a73fea3f8329e44d8aac97888ed0d9` | Capacity poll for the orchestrator | **Same input substrate**: `find <session-dir> -name '*.jsonl' -newermt` — proves the fleet already enumerates OMP session dirs by glob | Content is never read. `-name '*.jsonl'` + mtime count only. Zero parsing. Convention worth matching: sorted `*.jsonl` discovery. |
| 4 | `souji-shokunin/tools/souji-census.sh` | `9c9521a5069c4a13feaada6b34ba79502c68eb95c8afc6caf3dfda3e471ac688` | Census with a protected boundary (`:60-90`, `:205-265`); the same `.omp/agent` protected-prefix convention is duplicated in `souji-evidence-cache.py` and `souji-preservation-evidence.py` | **Policy precedent** for touching the agent store: `~/.omp/agent` (HOME ∪ passwd home ∪ `/root` ∪ `PI_CONFIG_DIR`/`PI_CODING_AGENT_DIR`) is a protected root; a root/compare that reaches, equals or is an ancestor is refused `path-protected`, exit 2 | Guards a *walker's root*, not an explicit file read. Not a scanner. Advisory only: mado's `--scan` should take caller-supplied paths and never default-walk `~/.omp/agent`. |
| 5a | `ufo-fsd-alpha/scripts/collect-omp-native-handoff-lib/events.mjs` (outside fleet, HEAD `31c465f`) | `93685bf3a7086c1a3e2258f32516c96ea9a7c6f14e9600eaf0ea3911c0e6cf3d` | The fleet's closest **OMP transcript envelope reader** | Iterates `message.role === "assistant"` → `content[]` items `type === "toolCall"`; same predicate C3 must implement | It **deliberately discards** non-task toolCall arguments: `item.name !== "task"` ⇒ `arguments` replaced by `TRUNCATION_MARKER` ("bulk payload", `:20-21`, `:71`). A `bash` command is redacted there by design. C3 would be the first consumer of non-task `arguments`. |
| 5b | `ufo-fsd-alpha/crates/ufo-core-runtime/src/native_transcript.rs` (939 L per kumitate ledger; HEAD `31c465f`) | `ab6c5d599a02601c6819ff665f6ebba09a19a29b14c15af0bb374b76f1c20090` | Rust validator for one agent's OMP JSONL | Only prior OMP-JSONL parser: canonical read, digest pin, UTF-8 gate, `MAX_TRANSCRIPT_LINE_BYTES` = 128 KiB per line, duplicate call-id rejection, `toolCall` filtered to `task`/`yield` | Structural/dispatch validation only; **no shell parsing, no command classes**. Also the source of a hazard note (below). |

### 5b hazard note for C3's output schema

`events.mjs:82-100` (`uniquifyReusedTaskIds`; the pinned claim is the comment
at `:83`) documents that **OMP reuses sequential `task:N` tool call ids** after
a call settles, and uniquifies them only for the evidence copy.
`native_transcript.rs` correspondingly rejects *repeated* `yield` call ids per
transcript. Consequence: `tool_call_id` is **not guaranteed unique** inside one
transcript. The tripwire's addressable key must stay `(file, line)` — id and
timestamp are data. This is consistent with the declared output shape (it
already carries `line`), and it is the one place where reading the prior art
prevents a plausible-looking design error.

## 4. Keyword collisions (no overlap; listed so the same grep is not re-run)

| Hit | Why it is not a tripwire |
|---|---|
| `mori-shokunin/tools/mori-journal-window.py:726` `payload.jsonl` | Its own scratch **output** format for a journalctl probe; journal records, not agent transcripts. |
| `mori-shokunin/tools/mori-round16-regressions.py` `_parse_jsonl` | Parses the tool's **own stdout** record stream. |
| `souji-*/tools/impl-07…08,37,41,47.sh` `.jsonl` | File-**extension** classification inside inventory/vault logic. |
| `chousa-shokunin/tools/research-gate.sh` `claims.jsonl`/`manifest.jsonl` | Gate **fixtures** written under `mktemp`; also one fixture example path `:3483`. |
| `tsukuroi-shokunin/tools/tsukuroi-census.sh`, `measure-update-recheck.py` | **Live read-only** `pacman -Q*`/`-Qu` probes (the opposite of post-hoc file analysis; unusable under the host pause by construction). `measure-update-recheck.py` reads a *captured snapshot* and executes no host command. |
| `tameshi-shokunin/tools/bash-witness-study.py` | Mutation sweep over a `bash-surface-census` suite; "bash" is the target language, not an observed command. |
| `kama-*/tools/kama-probe.sh`, `test-snapshot.sh`, `kotodama` gates | Domain data and runner invocations (`["bash", ...]`); the `"sh"` hits in `phonology-sanity-gate.py` are consonant tables. |

## 5. What L1 should record (advisory; the tool stays mado's)

1. Do **not** cite `kagi-shokunin/corpus/transcript-scan.sh` as prior art for a
   command tripwire in the round-17 lesson or QUALITY. It is prior art for the
   *shape* (post-hoc, counts-only, two-tier, `0/1/2`, selftest) and for the
   *posture* (never open the live source; copy first). Its observable is a
   secret string in an SQLite DB, not an argv in a transcript.
2. Do **not** fold `mado-action-plan.py` into the tripwire or vice versa. One
   is pre-execution over a declared plan; the other is post-hoc over observed
   shell text. Sharing a class vocabulary in prose is fine; sharing code would
   require the tripwire to import a 906-line gate with a frozen-plan mode it
   does not need.
3. `--scan DIR` discovery may follow `await-capacity.sh` (recursive, `*.jsonl`,
   sorted) but should require explicit paths in docs and never default into
   `~/.omp/agent` (souji protected-root convention).
4. If L1 wants the one cheap hardening cross-check from `native_transcript.rs`,
   a per-line byte cap before `json.loads` is the only transferable idea. The
   C3 spec does not require it; treat as optional, not a claim.

## 6. Confidence and unknowns

Observed (bytes read this run): directory inventory and file counts; all grep
tallies above; the quoted selection predicate and the id-reuse comment at the
cited `events.mjs` lines; the kagi gate registration line; every sha256 and
revision id in §3.

- [INFERENCE] None load-bearing. "No in-scope scanner" rests on full
  enumeration of the 8 `tools/` trees and all 25 `scripts/` files, not on a
  sample.
- Unresolved (out of assigned scope, not blockers):
  - Other lanes' in-flight `.ufo/waves` were **not** read by contract, so a
    scanner drafted this same round by a sibling seat is invisible here.
  - Untracked/non-repo helper dirs (lane `bin/`, `~/.local/bin`) were not
    scanned; the assignment named the two directory classes only.
  - `ufo-fsd-alpha` is a moving tree: the two digests pin HEAD `31c465f` only.
  - Host package versions are `[UNK]`; no package query is permissible under
    the pause, and none was attempted.
