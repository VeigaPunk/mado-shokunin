# SrcJjHelp — jj 0.45.1 parses and prints help in clap before any workspace load/snapshot; `jj git push --dry-run` is documented long-only and returns before `push_refs`

Scout for E4's jj half. Sources are file bytes at the `v0.45.1` tag, fetched with curl and
receipted under `.ufo/waves/round-20/fetch/SrcJjHelp/`.

## 1. Tag and host binding

- `git ls-remote https://github.com/jj-vcs/jj refs/tags/v0.45.1 'refs/tags/v0.45.1^{}'` →
  one line only: `7c41cdeb16b6b321c64e789a966b6adf723816a5 refs/tags/v0.45.1`. No `^{}` line
  ⇒ lightweight tag, commit **7c41cdeb16b6b321c64e789a966b6adf723816a5**.
- Host binary binds to the same commit: `/tmp$ jj --version` →
  `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` (binary `/home/vgpnk/.local/bin/jj`,
  sha256 prefix `cd5efc3eb281d606`). Run outside the lane (`/tmp`); no jj command in the lane.
- Every body below was fetched at that commit; sha256s in §5 and in
  `receipts.jsonl` (8 rows, all HTTP 200).

## 2. Where help is handled relative to workspace loading and snapshot

Observed chain (all `cli/src/…` at 7c41cdeb):

1. `main.rs:29` — `CliRunner::init().version(env!("JJ_VERSION")).run().into()`; the whole CLI
   is one `CliRunner::run` (`cli_util.rs:4726`).
2. `run_internal` (`cli_util.rs:4574`) loads **config** levels (system/user/repo/workspace),
   then expands aliases, then parses arguments:
   `cli_util.rs:4635` — `let (matches, args) = parse_args(&self.app, &string_args)`
   `.map_err(|err| map_clap_cli_error(err, ui, &config))?;`
3. `parse_args` (`cli_util.rs:4291-4299`) is pure clap:
   `.arg_required_else_help(true).subcommand_required(true).try_get_matches_from(string_args)?`
   (`:4296`). Clap itself turns `-h`/`--help` into `ErrorKind::DisplayHelp` and `--version`
   into `DisplayVersion`; both are returned as a `clap::Error` and never reach dispatch.
4. `map_clap_cli_error` → `CommandErrorKind::Cli` → `handle_clap_error`
   (`command_error.rs:1098-1121`): help/version render to **stdout** and
   `return Ok(0)` at `:1113-1115`; help kinds request the pager at `:1106-1107`.
5. Only after parsing does the runner build `CommandHelper` with a *loader object*:
   `cli_util.rs:4646` computes `maybe_workspace_loader` (for `-R` it calls
   `workspace_loader_factory.create(...)` = path resolution, not a load),
   `:4709` constructs `CommandHelper`, `:4721` calls `dispatch.call(...)`.
6. The **workspace is loaded lazily by the command body**:
   `cli_util.rs:459` — "Loads workspace and repo, then snapshots the working copy if allowed."
   → `workspace_helper` `:461` → `workspace_helper_with_stats` `:474` →
   `self.load_workspace()` `:478` → `snapshot_impl(ui, &git_import_export_lock)` `:495`.
   `CommandHelper` holds `maybe_workspace_loader`; nothing loads or snapshots before a
   `cmd_*` asks for it.

`jj help …` is a **dispatched** command but also never touches a workspace:
`commands/mod.rs:200` — `Command::Help(args) => help::cmd_help(ui, command_helper, args)`;
`commands/help.rs:50` `cmd_help` uses only `command.app().clone()` (`:70`) and
`command.render_long_help()` (`:87`) — no `workspace_helper` call in the file.

Empirical differential (outside any repo, `/tmp/srcjjhelp`, so any workspace load must fail):

```
jj git push --help       exit=0  stdout=8993 B  stderr=0 B  first="Push to a Git remote"
jj git push -h           exit=0  stdout=2320 B  stderr=0 B  first="Push to a Git remote"
jj help git push         exit=0  stdout=8993 B  stderr=0 B  first="Push to a Git remote"
jj --help                exit=0  stdout=7929 B  stderr=0 B
jj -h                    exit=0  stdout=4208 B  stderr=0 B
jj help --help           exit=0  stdout=5237 B  stderr=0 B
jj git push --dry-run    exit=1  stderr='Error: There is no jj repo in "."'
```

Help succeeds with no repo; dry-run fails with no repo. That is the ordering made visible:
help is answered by clap before workspace resolution, dry-run is not.

Current tool behaviour on the same shapes (text only, `--scan`, no fixture executed),
`/tmp/srcjjhelp/fx.jsonl` (5 lines: the help forms and the dry run):

```
python3 -I tools/mado-tripwire.py --scan fx.jsonl → exit 1, counts vcs_write 3
  line 1  jj git push --help      rule jj:git
  line 3  jj git push --dry-run   rule jj:git
  line 5  jj git push -h          rule jj:git
  (line 2 jj help git push and line 4 jj --help are clean)
```

Rows carry no `evidence` key today, so under the round-20 comparison they count `observed`.
That fixture is my /tmp scratch, not a suite case.

## 3. `jj git push --dry-run` — documented meaning and control flow

- Arg definition, `cli/src/commands/git/push.rs`: doc comment at `:231`
  (`/// Only display what will change on the remote`), `#[arg(long)]` at `:232`,
  `dry_run: bool` at `:233`. **Long-only** — no `-n` short form (contrast `git push -n`,
  and contrast jj's own gerrit push, which does document `-n`).
- Control flow in `cmd_git_push`: `workspace_helper(ui)` at `:280` (this is the snapshot),
  `start_transaction()` `:290`, sign-on-push only when `!args.dry_run` `:538`,
  then `:552-555`:
  `if args.dry_run { writeln!(ui.status(), "Dry-run requested, not pushing.")?; return Ok(()); }`
  — returning **before** `git::push_refs` `:561` and before `tx.finish(ui, description)`
  `:595`. So a dry run prints the planned ref updates and does not push or commit the
  transaction.
- Docs surface: `docs/cli-reference.md` is a 674 B stub that includes
  `../cli/tests/cli-reference@.md.snap` (the reference is generated by a Rust test, and the
  stub itself says it "does not match the `jj help` output exactly"). In that snapshot,
  inside `## jj git push` (section starts `:1886`, next section `:2057`), `:1946` reads
  `` * `--dry-run` — Only display what will change on the remote ``. The published sentence
  is therefore the Rust doc comment at `push.rs:231`.
- Only two `--dry-run` options exist in the 0.45.1 reference: `:1573` (`jj gerrit push`,
  `-n`, `--dry-run`) and `:1946` (`jj git push`). A jj dry-run exemption is therefore a
  `jj git push` fact, not a generic jj flag.

## 4. Contradictions and edge facts the E4 paragraph does not predict (report per contract)

1. **`-m --help` is not an "option value" write in jj.** `jj describe -m --help` exits **2**
   with `error: a value is required for '--message <MESSAGE>' but none was supplied`
   (stderr 112 B, stdout 0 B). Clap refuses a hyphen-leading token as the value, so the
   command never runs and never writes. The E4 parenthetical `-m --help` (option value) is a
   git-`commit` shape, not a jj shape. A "suppress when `-h`/`--help` appears" fix that also
   cleans this case is defensible on "no write occurred" grounds, but not because `--help`
   was consumed as a message.
2. **`jj git push --dry-run` still loads the workspace and snapshots the working copy**
   (`push.rs:280`, before the `:552` return). It is "no push, no transaction finish", not
   "no write at all". The tool's current rationale for flagging every jj subcommand is
   precisely that "jj snapshots the working copy on all of them" — so the dry-run exemption
   is a **scoping decision (ref/remote writes)**, not a snapshot-free fact. Help is the
   stronger case: it never resolves a workspace at all.
3. **Help as an option value the other way:** `jj git push --dry-run --help` and
   `jj git push --dry-run -h` both print help, exit 0 (help dominates). `jj log --help -r @`
   also prints help, exit 0.
4. **After `--`, `--help` is not a flag:** `jj git push -- --help` exits 2
   (`error: unexpected argument '--help' found`), same for `-- -h`. No write either way, but a
   rule should only honour `-h`/`--help` before a `--` separator.
5. **Short-option clusters:** `jj git push -hb` → help (exit 0); `jj git push -bh` →
   `-b h` = bookmark value `h`, not help (exit 1, no repo); `jj git push -nh` → exit 2
   `unexpected argument '-n' found`. A substring test for `-h` would wrongly clean `-bh`.
6. `jj git push -n` exits 2 (`unexpected argument '-n' found`) — no git-style `-n` alias.
7. `jj version` is a real subcommand that prints the version and needs no repo (exit 0);
   `JJ_NO_SNAPSHOT = {"help", "version"}` (`tools/mado-tripwire.py:133`) is consistent with
   the source.

## 5. Drafted SOURCES rows (11-column shape of `corpus/SOURCES.md`; id pending L1)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1xx-pending | jj v0.45.1 CLI dispatch source — https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/cli_util.rs (also command_error.rs, commands/mod.rs, commands/help.rs at the same tag) | code | A | where clap parses and prints help relative to workspace loading and the working-copy snapshot in jj 0.45.1 | tag v0.45.1 → commit 7c41cdeb16b6b321c64e789a966b6adf723816a5 (lightweight: `git ls-remote … refs/tags/v0.45.1 'refs/tags/v0.45.1^{}'` returns only the first line); cli_util.rs 185,869 B sha256 `ee1eb31d16c0b5a920ea80ad2f73ff4183b83450013f63dacb8402f2f77f1e2d`; command_error.rs 39,287 B sha256 `bebfbbb4360ed3579b19cad604594d8e15c6411e41a804bbebbe707a78aed4bb`; commands/help.rs 5,481 B sha256 `f83d6425ed6b877146e6778f13291a01ef3481371d64ecb699f519de01b19fdc`; commands/mod.rs 9,368 B sha256 `b1ca564932c0255888564d24f56b409ad00f018fd4239683e60a0f07d8b7d253`; cli_util.rs:4291-4299 `parse_args`, :4635 its call, :4646 loader only, :4709 `CommandHelper`, :4721 dispatch, :459-461/:474/:495 `workspace_helper` → `snapshot_impl`; command_error.rs:1106-1115; commands/mod.rs:200 | `jj <cmd> -h/--help` and `jj help …` are clap-level help: printed to stdout, exit 0, before dispatch; a workspace is loaded and snapshotted only when a command body calls `workspace_helper`, so help cannot read or write the working copy | queued | 2026-10-20 | on-release | tools/mado-tripwire.py (vcs_write jj rule); .ufo/waves/round-20/w1/cases (H family) |
| S1xx-pending | jj v0.45.1 `jj git push --dry-run` — https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/src/commands/git/push.rs and https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/cli/tests/cli-reference@.md.snap | code | A | the documented meaning and control flow of `jj git push --dry-run` in jj 0.45.1, and where its docs text comes from | tag v0.45.1 → 7c41cdeb16b6b321c64e789a966b6adf723816a5; push.rs 53,600 B sha256 `213469e3bcfbd5d991245a88efc88aaa28c7be30e9fcb81f88ab1aa37dcf3a0d`:231 doc, :232-233 `#[arg(long)] dry_run: bool` (no short), :280 `workspace_helper`, :538 sign only when `!args.dry_run`, :552-555 early `return Ok(())`, :561 `git::push_refs`, :595 `tx.finish`; cli-reference.snap.md 154,561 B sha256 `b330694348c2a6fb21b637425c711d48ac9fa41d0b3596b4ca2955f7a9333554`:1946; docs/cli-reference.md 674 B sha256 `5832fd949ae8b876fde7dc97cd5a92a3c26055de136eb76c53f7d1ade1487dbb` | a dry run prints the changes and returns before `git::push_refs` and `tx.finish`, so it does not push or commit a transaction; it still loads the workspace (:280), so the exemption is about ref/remote writes, not about touching the working copy; `--dry-run` has no `-n` short form | queued | 2026-10-20 | on-release | tools/mado-tripwire.py (vcs_write jj rule); .ufo/waves/round-20/w1/cases (H family) |

Located quotes (≤25 words each):

- `cli/src/cli_util.rs:4296` — "try_get_matches_from(string_args)?;"
- `cli/src/cli_util.rs:459` — "Loads workspace and repo, then snapshots the working copy if allowed."
- `cli/src/cli_util.rs:495` — ".snapshot_impl(ui, &git_import_export_lock)"
- `cli/src/command_error.rs:1113` — `clap::error::ErrorKind::DisplayHelp | clap::error::ErrorKind::DisplayVersion => {`
- `cli/src/command_error.rs:1114` — `write!(ui.stdout(), "{clap_str}")?;`
- `cli/src/command_error.rs:1115` — `return Ok(0);`
- `cli/src/commands/git/push.rs:231` — "Only display what will change on the remote"
- `cli/src/commands/git/push.rs:552` — `if args.dry_run {`
- `cli/src/commands/git/push.rs:553` — `writeln!(ui.status(), "Dry-run requested, not pushing.")?;`
- `cli/src/commands/git/push.rs:554` — `return Ok(());`
- `cli/tests/cli-reference@.md.snap:1946` — `` * `--dry-run` — Only display what will change on the remote ``

Fetch receipts: 8 rows in `.ufo/waves/round-20/fetch/SrcJjHelp/receipts.jsonl`, bodies
`cli_util.rs`, `git_push.rs`, `main.rs`, `commands_mod.rs`, `cli-reference.md`, `help.rs`,
`cli-reference.snap.md`, `command_error.rs` (curl 8.23.0, all `http_status` 200, URLs
commit-pinned to 7c41cdeb — never `main`/`latest`).

## Limits

- I did not run a real `jj git push --dry-run` against a repo with a remote (would require
  creating a repo/remote and is the executor's empirical lane); the no-push claim rests on
  `push.rs:552-561` and the `:231` doc, plus the no-repo differential above.
- Snapshot-on-load for dry-run is source-read (`push.rs:280` → `cli_util.rs:495`), not
  observed in a live repo.
- I did not fetch the git(1) side (`git commit -n`, `git add -n`) — sibling scouts
  SrcGitHelpSource / SrcGitAddPushDoc own it; the `-m --help` contradiction in §4.1 is
  jj-only and leaves the git shape unverified.
- I did not check the round-20 case suite or the H-family executor's implementation; no
  claim about N/N scores.
- Web facts are as served by raw.githubusercontent.com at fetch time; bodies are retained
  and digest-pinned, so a later re-fetch can be compared byte-for-byte.

## Installs

none (curl/python3/jj already present; no package manager invoked).
