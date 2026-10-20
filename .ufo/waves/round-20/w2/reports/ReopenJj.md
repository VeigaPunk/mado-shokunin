# ReopenJj — partly falsified: S103/S104 bytes, quotes, and tag pin re-fetch exact, but S103's "`jj help …` … before dispatch" is false and the note repeats its mechanism

Item: reopen SOURCES rows S103/S104 (`corpus/SOURCES.md:115-116`) and their Gate lines
(`corpus/lessons/round-20.md:40-41`) against the pinned URLs, the w1 receipts
(`.ufo/waves/round-20/fetch/*/receipts.jsonl`), and the claims they carry in
`corpus/knowledge/tripwire-precision-r20.md:1,53,55` and `SKILL.md:555-561`.
Lane tip checked read-only: `a4046a8216080d4004de3f268c62cf142095ac07`; the tool the note
pins hashes `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`
(`tools/mado-tripwire.py`), equal to the note's `verified-at`. Fetch bodies and receipts:
`.ufo/waves/round-20/w2/ReopenJj/fetch/` (8 receipts, 8 bodies); line-check log:
`.ufo/waves/round-20/w2/ReopenJj/evidence/citations.txt`.

## F1 — Tag pin holds (command that could have falsified it)

```
$ git ls-remote https://github.com/jj-vcs/jj refs/tags/v0.45.1 'refs/tags/v0.45.1^{}'
7c41cdeb16b6b321c64e789a966b6adf723816a5	refs/tags/v0.45.1
$ ... | wc -l
1
```

One line: no peeled `^{}` line, so lightweight, and the commit equals both rows' pin
(`corpus/SOURCES.md:115-116` → `7c41cdeb16b6b321c64e789a966b6adf723816a5`). A different SHA
or a second peeled line would have falsified.

## F2 — S103 bytes hold at the tag URL (and at the commit URL in the receipts)

Fetched at `https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/<path>`; all HTTP 200,
`final_url` unchanged.

| file | B | sha256 | row | w1 receipt (commit URL) |
|---|---|---|---|---|
| cli/src/cli_util.rs | 185,869 | `ee1eb31d16c0b5a920ea80ad2f73ff4183b83450013f63dacb8402f2f77f1e2d` | same | same (`fetch/SrcJjHelp`) |
| cli/src/command_error.rs | 39,287 | `bebfbbb4360ed3579b19cad604594d8e15c6411e41a804bbebbe707a78aed4bb` | same | same |
| cli/src/commands/help.rs | 5,481 | `f83d6425ed6b877146e6778f13291a01ef3481371d64ecb699f519de01b19fdc` | same | same |
| cli/src/commands/mod.rs | 9,368 | `b1ca564932c0255888564d24f56b409ad00f018fd4239683e60a0f07d8b7d253` | same | same |

A one-byte drift at the tag vs the commit receipts would have falsified; none.

## F3 — S103 line citations hold (25/25 PASS)

`evidence/citations.txt` is the PASS/FAIL table; all 25 checks pass, including:
`cli_util.rs:4291` `fn parse_args`, `:4635` its call, `:4646` `let maybe_workspace_loader`,
`:4709` `CommandHelper`, `:4721` `dispatch.call`, `:459-461` `workspace_helper`,
`:474` `workspace_helper_with_stats`, `:495` `snapshot_impl`;
`command_error.rs:1106/1113/1114/1115`; `commands/mod.rs:200`; `push.rs:231/232/233/280/538/552/554/561/595`;
`cli-reference@.md.snap:1946`; `cli_util.rs:782-783`.

The ordering claim is verified end to end, not just quoted:
`parse_args` at `cli_util.rs:4635-4636` → `map_clap_cli_error` → error propagates out of
`run_internal`; a `WorkspaceLoader` is constructed at `:4602` (cwd) and `:4646-4662` (`-R`), but
construction does not load the workspace (comment at `:4600`: "WorkspaceLoader::init() won't do
any heavy lifting other than the path resolution"), and dispatch is `:4721`. `workspace_helper` (`:461`) reaches `snapshot_impl` only through
`workspace_helper_with_stats` (`:474`, `:478`, `:485`, `:495`), gated on
`is_working_copy_writable` (`:782-783`). Exit path: `handle_command_result:1004` →
`try_handle_command_result:1008` → `CommandErrorKind::Cli:1027-1029` → `handle_clap_error:1098`
→ `:1113-1115` (`write!(ui.stdout(), …); return Ok(0);`) → `CliRunner::run:4726-4737` returns
that `u8`. So "printed to stdout, exit 0, before any workspace load" is true for
`jj <cmd> -h/--help`.

Gate quote: it is an elided composite over `command_error.rs:1113-1115`; every retained token
is verbatim (`DisplayHelp`, `DisplayVersion`, `write!(ui.stdout(),`, `return Ok(0);`), the
ellipsis is marked the same way S099/S109 mark theirs, and it is 9 whitespace tokens
(≤ 25).

## F4 — FALSIFIED: S103's "`jj help …` … before dispatch" is wrong (the outcome is not)

S103's teach cell (`corpus/SOURCES.md:115`) says: "`jj <cmd> -h/--help` and `jj help …` are
clap-level help: printed to stdout, exit 0, **before dispatch**".

Observed: `jj help` is a dispatched subcommand, not clap's `DisplayHelp` error path.

```
commands/mod.rs:200  Command::Help(args) => help::cmd_help(ui, command_helper, args).await,
help.rs:50           pub(crate) async fn cmd_help(...)
help.rs:70           let mut app = command.app().clone();
help.rs:87           let help_text = command.render_long_help();
help.rs:89/91        write!(ui.stdout(), ...)
help.rs:93           Ok(())
```

The row's own cited line `commands/mod.rs:200` contradicts its "before dispatch". The
*outcome* survives: `grep -n 'workspace\|snapshot\|load_workspace' help.rs` returns nothing;
`cmd_help` touches only `command.string_args()` (`help.rs:63-66`) and `command.app()`
(`:70`), so `jj help` cannot read or write the working copy. What fails is the mechanism
sentence, and the knowledge note repeats it: `tripwire-precision-r20.md:53` says
"no — clap answers before any workspace load or snapshot | S103 `command_error.rs:1113-1115`".
For `jj help` clap does not "answer"; `cmd_help` renders it, and the cited line does not cover
that path. `SKILL.md:556-558`'s operative claim ("VCS help … are not writes: … `jj help`
(S103)") is still supported by the row's help.rs/mod.rs evidence.

Separately, the row's general clause "a workspace is loaded and snapshotted only when a
command body calls `workspace_helper`" is over-broad: `workspace_helper_no_snapshot` loads
without snapshotting (`cli_util.rs:523-527`), and `maybe_snapshot` (`:1364-1375`) and
`WorkspaceCommandHelper::update_stale` (`:1570`) reach `snapshot_impl` from command bodies
without another `workspace_helper` call. It does not affect the help verdict — `cmd_help`
calls none of these entries — but the clause should be narrowed.

Suggested amendment (row, not tool): split the sentence — `-h/--help` → clap
`DisplayHelp` before dispatch (`command_error.rs:1113-1115`, ordering at `cli_util.rs:4635-4646`);
`jj help` → dispatched `cmd_help` that never calls `workspace_helper`/`load_workspace`
(`commands/mod.rs:200`, `help.rs:50-94`). The note's `jj help` clause should cite
`help.rs:50-94`, and its "clap answers" should be scoped to `-h/--help`.

## F5 — Gate S103 pairs its quote with another file's sha (presentation defect, evidence recoverable)

Gate line `corpus/lessons/round-20.md:40`: URL `…/cli_util.rs`, sha `ee1eb31d…` (cli_util.rs,
185,869 B), quote `command_error.rs:1113-1115` (39,287 B, `bebfbbb4…`). A checker who fetches
the gate URL and matches its sha cannot find the quoted text; the quoted bytes are pinned only
in the row's evidence cell (`corpus/SOURCES.md:115`) and in `fetch/SrcJjHelp/receipts.jsonl`.
The round's own convention for multi-file rows is "per-file sha256 in the receipts"
(S102 `:39`, S109 `:46`); S103 is the one gate of the two that mixes files without saying so.
Not a false claim, but a gate that should name the companion file (or use "per-file sha256").

## F6 — S104 bytes hold

| file | B | sha256 | row | receipt |
|---|---|---|---|---|
| cli/src/commands/git/push.rs | 53,600 | `213469e3bcfbd5d991245a88efc88aaa28c7be30e9fcb81f88ab1aa37dcf3a0d` | same | same (`SrcJjHelp`) |
| cli/tests/cli-reference@.md.snap | 154,561 | `b330694348c2a6fb21b637425c711d48ac9fa41d0b3596b4ca2955f7a9333554` | same | same |
| docs/cli-reference.md | 674 | `5832fd949ae8b876fde7dc97cd5a92a3c26055de136eb76c53f7d1ade1487dbb` | same | same |

## F7 — S104 control flow holds; gate quote verbatim at `:231`

```
$ grep -n 'Only display what will change on the remote' push.rs
231:    /// Only display what will change on the remote      (8 words, == snap:1946)
$ grep -n dry_run push.rs
233:    dry_run: bool,                                       (#[arg(long)] at 232: no short)
538:    if !args.dry_run && tx.settings().get_bool("git.sign-on-push")? {
552:    if args.dry_run {
```

Only three `dry_run` occurrences: the field, the sign guard, and the early return — there is
no later test that could re-enable the push. `:280` `workspace_helper` runs first (snapshot via
`cli_util.rs:474-495`); `:290` starts the transaction; `:538` skips signing; `:552-555` prints
"Dry-run requested, not pushing." and returns `Ok(())`; `:561` `git::push_refs` and `:595`
`tx.finish` are only reachable after that return (and `tx.finish` is the file's only
`tx.finish`). So "prints the changes and returns before `git::push_refs` and `tx.finish`" and
"still loads the workspace (`:280`)" both hold.

Docs provenance holds: snap `:1946` reads

```
* `--dry-run` — Only display what will change on the remote
```

and `docs/cli-reference.md` is a 674 B generator stub that include-markdowns the snap
(`start="<!-- BEGIN MARKDOWN-->"`). (The other `-n, --dry-run` at snap `:1573` is Gerrit push,
a different subcommand.)

Caveat on the gate gloss, not the quote: "the working copy is snapshotted first" is supported
by `push.rs:280`, not by the quoted `:231` (a doc comment). The row's evidence cell carries
`:280`; the gate quote alone does not.

## F8 — S104's note citation lands on the doc comment

`tripwire-precision-r20.md:55` cites `S104`'s `push.rs:231` for "the working copy is snapshotted
before the dry-run return". `:231` is the docstring; the snapshot is `:280`. The row has the
right line; the note's pointer should be `:280` (the `+1 op` measurement is separate and was
not re-run here).

## F9 — Row → note/SKILL support verdict

- **S103 supports** `SKILL.md:556-558`'s operative claim that `jj -h|--help` and `jj help` are
  not writes: clap returns at `cli_util.rs:4635-4636` before the loader (`:4646`) and dispatch
  (`:4721`); `cmd_help` never calls `workspace_helper`/`load_workspace`. The note's sentence at
  `:53` is right about the verdict, wrong about the mechanism for the `jj help` half.
- **S104 supports** `SKILL.md:558-559`'s "plain `jj git push --dry-run` (it snapshots first;
  S104)" and the note's `:55` row: `:280` snapshots (unless `--ignore-working-copy`/
  `--at-op`), `:552-555` returns before `:561`/`:595`.
- **Not sourced by either row:** the note's `--ignore-working-copy git push --dry-run` row
  says "measured: +0 ops" and SKILL does not attribute it to S103/S104. Source-level support
  exists outside these two rows' pinned scope (`cli_util.rs:485` + `:782-783`), so it is not a
  misattribution — but S104 alone does not prove the `--ignore-working-copy` variant.

## Falsifiers tried (all negative except F4)

Different tag target or a peeled `^{}` line (F1); tag-vs-commit byte drift (F2); line drift on
all 25 citations (F3, table); quote not present or over 25 words (F3/F7); a `-n` short form on
`dry_run` (`#[arg(long)]` only, `:232-233`); a second `dry_run` check after `push_refs` (only
three occurrences); `cmd_help` reaching `workspace_helper`/`load_workspace` (grep empty);
`tx.finish` on the dry-run path (only `:595`, after the return); docs text not derived from the
snap (`docs/cli-reference.md` includes it). The one positive is F4's mechanism sentence.

## Limits

- Source-only. I did not execute `jj`; the note's "0 ops" / "+1 op, `refs/jj/keep`" are w1
  measurements and were not re-run by this seat. [UNK] whether any host config path (e.g.
  config migration) writes during `jj help` — the source shows no disk write on that path, but
  it was not executed.
- Pin evidence is `git ls-remote` plus raw fetches at both the tag and the commit URL — not a
  clone of jj and not an object-level tag verification.
- Bodies are stored under my fetch dir (largest 185,869 B); no host VCS or host-probe commands
  were run. [INFERENCE] that raw.githubusercontent's tag redirect and commit URL serve the same
  bytes is confirmed only by equal sha256 (they do).
- `jj help`'s stdout/exit-0 outcome is verified by the code path, not by execution; the row's
  "measured: 0 ops" remains the only empirical check for that clause.

## Installs

none.
