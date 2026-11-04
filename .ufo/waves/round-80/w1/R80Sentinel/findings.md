# R80Sentinel — boundary and security review, round-80 instruments (read-only)

Seat: R80Sentinel (sentinel). Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope: `tools/mado-barfoot.py` (1400 ln), `quality/counters/c1-r80-multisurface.py` (459 ln),
`quality/counters/c2-r80-runbook.py` (689 ln), control sets
`.ufo/waves/round-80/controls/c1-cases-r80.json` (33 cases) and
`c2-runbook-cases-r80.json` (24 cases), and the round-80 wave tree for credential material.
Evidence basis: full read of all three instruments and both control sets; the frozen receipts
(`measurement-c1-r80.txt`, `measurement-c2-r80.txt`, TARGET_MET at
`6c302a53eb8f577e83fbcadc01e05a286778df8e`) were read as declared, not re-run — this seat is
read-only and re-running C2 would probe the live host. No scratch directory was created;
nothing to remove.

## Findings

### F1 — LOW: C2 `run()` inherits the full caller environment into every probed child
- Evidence: `c2-r80-runbook.py:130` `env = dict(os.environ)`; only `LC_ALL`/`LANG`/`PYTHONDONTWRITEBYTECODE`
  are overridden (130-133), `XDG_RUNTIME_DIR`/`HYPRLAND_INSTANCE_SIGNATURE`/`OMARCHY_PATH` are
  added (134-152), and five directories are *appended* to `PATH` (153-160). All 24 child
  invocations (`run(case["argv"], repo)`, line 626) receive whatever secrets happen to sit in
  the seat environment.
- Exploit path: none within the frozen control set — every probed child is a local read verb
  (verified below) and the argv itself is frozen and sha-pinned at freeze. The exposure is
  ambient: any credential exported in the runner's environment is handed to `hyprctl`, `jq`,
  `makoctl`, `omarchy`, and `systemctl`. C1 does this better: it builds a minimal env
  (`c1-r80-multisurface.py:118-125`, only `PATH`, `LC_ALL`, `LANG`,
  `PYTHONDONTWRITEBYTECODE`, `TMPDIR`).
- Impact: information disclosure limited to a hostile/compromised local read tool; not
  round-80-introduced (carried from r79).
- Smallest remediation: in `run()`, replace `dict(os.environ)` with the same minimal allowlist
  C1 uses, plus the four probe-specific keys.

### F2 — LOW: C2 does not pin `TMPDIR`; the no-`/tmp`-write property is implicit, not enforced
- Evidence: C1 sets `"TMPDIR": cwd` for every child (`c1-r80-multisurface.py:124`); C2's env
  (130-160) never sets `TMPDIR`. The counter itself uses only
  `tempfile.mkdtemp(prefix="c2-r79-", dir=args.scratch_root)` (line 560) and removes the tree
  in `finally` (683-685).
- Verification that §7 nonetheless holds: traced every write the counter and its children can
  perform. Counter writes: mutant files under `workroot` (648-650), nothing else. Children
  (all 24 frozen commands, listed under Verification V5): `hyprctl` (socket reads), `jq`,
  `head`, `pgrep`, `makoctl mode`, `omarchy theme current|version|menu keybindings --print`,
  `cut`, `systemctl --user is-active`, and `python3 -I tools/mado-barfoot.py` on committed
  fixtures — none creates a temp file. No counter or child write under `/tmp` was found by
  reading; none by execution (not executed — read-only seat).
- Impact: a future row added with a temp-writing verb would silently land in `/tmp`, breaking
  the QUALITY/§7 rule (cf. `corpus/QUALITY.md:445`, no host `/tmp` use).
- Smallest remediation: add `env["TMPDIR"] = <scratch-per-case dir>` in C2's `run()`, mirroring C1.

### F3 — INFO: `parse_surfaces` silently accepts negative surface margins and negative `exclusive` ints below −1
- Evidence: margins are validated only as ints (`tools/mado-barfoot.py:601-606`); `exclusive`
  is validated only as int-or-`"auto"` (587-589). The bar *config* refuses negative margins
  (`declared_bar`, 341-343 → Unmodelled), so the surfaces path is the asymmetric one.
- Bounds that keep this harmless: `apply_exclusive` only shrinks when `zone + margins[edge] > 0`
  (guard at line 634; shrink 635-642) — a negative margin can only *reduce* the amount, never
  grow the usable box or invert the shrink direction. A negative-but-not-−1 `exclusive`
  (e.g. −5) is silently treated as inert for shrinking yet, unlike the protocol's −1, is
  arranged against the running usable box rather than the full box (`zone == -1` special case
  at 720-722) — a model-faithfulness nit affecting only that declaration's own verdict, never
  the counter's files or another case.
- Impact: hostile surfaces content can skew its own case verdict at worst; no cross-case or
  host effect. Out of sentinel remediation scope (correctness, not a trust boundary); named
  for the record.

## Verified non-issues (checks that came back clean)

- **V1 Read path (`read_bytes`, barfoot:145-170).** All five inputs (`--config`, `--layers`,
  `--monitors`, `--rules`, `--surfaces`; main:1369-1381) funnel through it. `O_RDONLY|O_NOFOLLOW`
  (153) refuses symlinks; `fstat` + `S_ISREG` (157-158) refuses directories/fifos/devices;
  size cap `MAX_BYTES = 1048576` (87) enforced on both the file size and the actual read
  (159-161); stdin capped at `MAX_BYTES + 1` (148-150). No TOCTOU window of consequence
  (content is read once, used read-only; the tool "writes nothing" and nothing in the code
  contradicts that).
- **V2 No path traversal via `--surfaces` content.** `namespace` is the only
  attacker-controlled string (validated non-empty, 558-560) and is used exclusively as a
  dict key for attribution (757), an equality match against the layers-JSON content
  (`find_layer`, 836-848), and stdout. It is never joined to a path, never opened. Case
  files write only fixed filenames under the per-case outdir
  (`c1-r80-multisurface.py:177-203, 231`); case *content* is never interpreted as a path.
- **V3 No unbounded loop or allocation from a hostile declaration.** Every input is ≤ 1 MiB
  (V1), so the surfaces list is bounded by the input itself; parsing is one O(n) pass
  (550-619) plus an O(n log n) sort (714-715). `order`/margins are Python ints — no overflow,
  and a worst-case ~1 MB digit string yields only a ~3 Mbit bigint. Margins of ±10^9 flow into
  guarded box arithmetic (634, 763) that collapses to zero on any inconsistency. Static
  `addreserved` fields are regex-capped at 6 digits with optional minus (`INT_FIELD_RE`, 103;
  enforced 398-399) and clamped `max(0, …)` (400-401). A 1e6-surface or huge-`order` payload
  is therefore a slow-ish bounded parse, not a DoS.
- **V4 `apply_exclusive` cannot shrink the usable box the wrong way.** Guard at 634 makes the
  shrink amount strictly positive; each shrink only ever moves the near edge inward
  (635-642); the running box's validity is re-checked against the original before any layer
  area is credited (`contains_box`, 645-648, used at 763), and an invalid area zeroes the
  dynamic band. Negative zone never reaches the shrink (`zone <= 0` returns None, 632-633;
  sequence partitions on `zone > 0`, 714-716).
- **V5 Scratch containment and the 24 C2 commands.** Both counters refuse `/` as scratch root
  (c1:369-370, c2:553-554), refuse a symlinked scratch root (c1:371-372, c2:555-556),
  `makedirs` + `isdir` check (c1:373-375, c2:557-559), create one generation dir via
  `tempfile.mkdtemp(dir=args.scratch_root)` (c1:376, c2:560), and `shutil.rmtree(workroot,
  ignore_errors=True)` in `finally` (c1:453-455, c2:683-685). No counter write path escapes the
  scratch root; no counter or child write under `/tmp` exists (F2). All 24 frozen argv read
  from `c2-runbook-cases-r80.json`: rows 0-16 `hyprctl …` (version, configerrors, monitors,
  getoption, binds, layers, activeworkspace, clients, workspaces) with `jq`/`head`;
  `pgrep -x waybar`; `makoctl mode`; `omarchy theme current|version|menu keybindings --print`
  (plain and `| cut -c1-35`); rows 17-20 `python3 -I tools/mado-barfoot.py` on committed
  fixtures (read-only join); row 23 `systemctl --user is-active hypridle`. Every one is a read
  verb or the lane's read-only join. A case's argv cannot reach a write verb: the counter
  cross-checks each case's executed command against its documented row anchor
  (c2:614-618), binds every row to exactly one case (592-613), and binds SKILL.md, the tool,
  and all fixtures to the measured revision by sha256 (578-595).
- **V6 C2 `run()` environment probe is read-only.** `XDG_RUNTIME_DIR` discovery (134-136) and
  the `HYPRLAND_INSTANCE_SIGNATURE` walk (137-144) only `isdir`/`listdir`/`exists` under
  `/run/user/<uid>/hypr`; `OMARCHY_PATH` discovery (146-152) only `isfile`/`access`-checks
  candidate directories. `git rev-parse`/`git show` (96-103, 341-346 in C1) are read-only
  verbs with `cwd=repo`. PATH directories are appended, not prepended (153-160), so the
  discovery does not shadow the seat's ambient resolution order.
- **V7 No credential material.** `grep -rn 'op://'` over `.ufo/waves/round-80/`,
  `tools/mado-barfoot.py`, and both counters: 7 matches, all in the round's own spec prose
  (`make-spec-r80.py:189,341-342`, `w1-dispatch.json:151,186`, `w1-spec.json:34,69`) quoting
  this check's instruction text itself — zero in the instruments, control sets, receipts, or
  fixtures. An extended sweep (`bearer`, `authorization:`, `session[_-]token`, `cookie:`,
  `api[_-]key`, `secret`, `password`, `BEGIN .* PRIVATE`) over the same surface, excluding
  those three spec files, returned empty. `observed()` in C2 also truncates probed output to
  100 chars and refuses to quote JSON dumps (387-394), so monitor serials/descriptions do not
  leak into receipts.

## Receipts

Both frozen receipts report `TARGET_MET` at `6c302a53eb8f577e83fbcadc01e05a286778df8e`
(`.ufo/waves/round-80/receipts/measurement-c1-r80.txt`, `measurement-c2-r80.txt`), consistent
with the claims declaration; taken as declared, not re-executed (read-only seat).

STATUS: ok — no high/medium boundary defects; two low hardening deltas (F1 full-env
inheritance in C2's `run()`, F2 unpinned `TMPDIR`) and one informational model nit (F3),
each with the smallest remediation named. Nothing missing.
