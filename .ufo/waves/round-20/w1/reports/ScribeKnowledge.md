# ScribeKnowledge — draft written; source rows still pending, tripwire E1-E4 unobserved at any revision

Scope: draft `corpus/knowledge/tripwire-precision-r20.md` as a file at
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/drafts/ScribeKnowledge.md`
(192 lines, sha256 prefix `5b869a5c…`). Nothing was written to `corpus/`, the lane's tracked files, SOURCES.md, or any fleet path.

## Behaviour (what the draft says, with evidence)

Observed at 1f7f995 (red baseline) and 9c54c56 (pre-harm), by `python3 -I <tool> --scan` on one-line synthetic envelopes in `/tmp/mr20-scribe`:

- `BLOCK=frozenset(['pacman','-Q','hyprland'])` (eval py): 1f7f995 → `package_query`, `pacman:-Q`, line 1, no `evidence` key, exit 1; 9c54c56 → clean, exit 0. Reproduces the round-19 closure's counterexample.
- Literal argv `['pacman','-Q','hyprland']` handed to an unbound `run_record(...)`: 1f7f995 → unmarked `package_query` (should be `lead` under E1); 9c54c56 → clean.
- Same-text `def show(argv): return str(argv)` called with that argv: clean at 1f7f995 (E2-consistent).
- Same-text `def frozenset(argv)` with a spawn body, called with literal argv: 1f7f995 → unmarked `package_query` (E3-consistent); 9c54c56 → clean, `unparsed_spawns=1`.
- Eval `subprocess.run(["git","commit","-m","x"])`: 1f7f995 → `vcs_write`, `git:commit`; 9c54c56 has no `vcs_write` key at all (class absent).
- Bash `git commit -n -m t` → 1f7f995 `vcs_write` (correct: `-n` is `--no-verify`; scratch repo gained a commit).
- Bash `git commit --dry-run -m t`, `git add -n file`, `git push --dry-run origin main`, `git commit -h`, `jj git push --help` → all `vcs_write` at 1f7f995 (the H-family harm the target E4 exempts). `jj help git push` → clean.
- `git commit --dry-run -m t; git commit -m real` and `git commit -m a && git commit -m b` → one `vcs_write` row each, naming only the first command. A row can name a dry run and hide the write.

Scratch-observed git/jj/bash facts: `git commit --dry-run` leaves history unchanged; `git add -n file` leaves the file untracked; `git commit -h` rc=0; `jj help git push` and `jj git push --help` print help rc=0 and create no `.jj` directory in a plain directory; `false && echo x; payload` still runs the payload under `set -e` (canary written); `if ! setup; then exit 1; fi` and `setup || { exit 1; }` abort before the payload (canary absent).

Round-19 incident shape (`unshare ... inns.sh bash -c '... /usr/bin/hyprctl probe ...'`) is quoted from `corpus/lessons/round-19-verifier-spotcheck.md` § Incidents. It was not re-run.

## Sources

- Reserved S099-S110 are unassigned. The draft carries `S1xx-pending` by topic: git-commit, git-add/git-push, git.c help, jj help, Python builtins, shlex, bash errexit. No row content was verified from a source; every upstream statement is marked `[INFERENCE]`.
- No fetch was made, so no fetch receipt exists for this seat.

## Findings

1. The draft is written to the scoped drafts path only. The header carries `source:`, `verified-at:`, `recheck:`, `surface:` in house style (`idle-lock-route-r17.md`, `terminal-route-r17.md`).
2. **Process error, corrected:** one `edit` call replaced draft line 1 (the `source:` header) with a placeholder. I caught it on the next read and rewrote the full draft with the header restored (verified by `head`). The file on disk is the corrected version; no other file was affected.
3. Defect for the round-20 tool (routed, not fixed here): one bash call yields one `vcs_write` row naming the first match, so a dry run before a real write hides the write. Target E4 keeps the write; the row must name it.
4. Defect for the round-20 tool (routed): at 1f7f995 every row lacks `evidence`, so the L-family lead cases are indistinguishable from observed runs under the counter's rule.
5. The 9c54c56 tool has no `vcs_write` class; a `clean` there for git write forms is class absence, not a precision result. Do not cite it as a no-harm comparison for `vcs_write`.

## Limits

- No S1xx row was opened or assigned; every upstream claim is `[INFERENCE]`. The draft must not be published into `corpus/knowledge/` until the source rows land and the `S1xx-pending` placeholders are replaced.
- Target E1-E4 behaviour is not observed at any revision; the draft says so in its text and table.
- Synthetic fixtures are one-line envelopes; they do not measure precision across the lane and do not replace the round's precision suite.
- `git push --dry-run` was not run against a remote; `git --help <sub>` was run only with `MANPAGER=cat` in scratch.
- `unshare` was not executed; fail-closed rules were tested only with canary writes in `/tmp`. Its exit status for an unavailable namespace or mount is `[UNK]`.
- Did not check QUALITY.md criteria 29 and 30 wording or the round-17 measure output; the draft does not claim a score.
- Did not read the round-20 precision suite (`.ufo/waves/round-20/precision/`) or other seats' case drafts.

## Installs

none. Scratch checks used the already-present git 2.56.0, jj 0.45.1, bash 5.3.20, Python 3.14.8 and util-linux `unshare` (present, not run). No pacman, sudo, systemctl, hyprctl, or other host command was run. No git or jj write was made in the lane; scratch repositories live only under `/tmp/mr20-scribe`.
