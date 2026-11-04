# R79Sentinel — security & boundary review, round 79 (freeze `5eb8f20f`, base `e4b153df`)

Method: read the full bytes of `tools/mado-barfoot.py` (923 lines), `quality/counters/c1-r79-reserve.py` (369),
`quality/counters/c2-r79-runbook.py` (582), both control sets, all 12 fixture files, the declaration, the five
receipts, the fetch manifest and the freeze diff. Working-tree hashes verified against the pins before review:
`tools/mado-barfoot.py` = `c9aa1391…` (matches the frozen r79-v1 pin), `c1-cases-r79.json` = `5f7ebb3c…`
(matches), `HEAD` = `5eb8f20f…` (matches). No repo file was edited; no mutating git/jj command was run; host
probes were limited to `ls -ld`, `pgrep`-free file reads. No tools were installed (none needed).

## 1. `tools/mado-barfoot.py` — `--rules` handling

**Path refusals — implemented as specified.** `read_bytes` (`tools/mado-barfoot.py:124-143`): `os.lstat`, then
`stat.S_ISREG` → a symlink (lstat sees `S_IFLNK`), FIFO, socket, device and directory all die with
`refused non-regular path: %s` (:137); size cap `MAX_BYTES = 1048576` → `file exceeds %d bytes` (:139);
`--config` cannot be `-` (stdin only accepted for `--layers`/`--monitors`, :126-131).

**F1 (LOW, exploit path: local TOCTOU).** `read_bytes` lstats the path, then `open(path, "rb")` (:141) follows
whatever is at the path *at open time*. A path swapped from a regular file to a symlink between lstat and open
is read anyway. Impact is bounded: the bytes are parsed and only structured fields come back out (see echo
analysis below) — no raw content is ever printed — so this is a hardening gap, not a leak primitive.
Smallest remediation: `os.open(path, os.O_RDONLY | os.O_NOFOLLOW)` + `os.fstat` before read.

**UTF-8 — strict, fail-closed.** `read_text` decodes the rules file strictly → `rules file is not UTF-8`
(:332-337); `load_json`/`load_jsonc` decode strictly → `%s is not UTF-8` (:191, :202). No replacement-char
fallback anywhere. Every decode failure is `Setup` → rc 2 with a stage-prefixed one-liner.

**Content echo — none from `--rules`.** All output sites are `tools/mado-barfoot.py:600-601, 615, 880, 896,
919, 922`. `parse_static_reserve` failures carry the path argument and a 1-based line number only (:362-363,
:367, :381); no rule text is quoted. RESULT/STATIC rows print config-derived scalars (position, layer,
namespace, monitor name, four static integers, `source=rules|none`). The only `%r` echoes of file content are
the caller's own `output` value (`outside the modelled subset`, :259/:266/:270 region) — data the caller
supplied in the same invocation. Verdict: the tool reflects caller-supplied fields back to the caller and
never echoes rules-file bytes.

**Observations (no action):**
- `"##" in value` (:367 area) is unreachable — `strip_rule_comment` already truncates at the first `#` (:345).
  Dead defense, harmless.
- `INT_FIELD_RE = -?[0-9]{1,6}` (:113) accepts *negative* `addreserved` fields, mirroring the C++ handler's
  `std::stoi` parity the docstring claims; the empty-usable-box refusal (`evaluate`, :500 region) bounds the
  damage. No frozen case exercises a negative static reserve — a future case could pin it.

## 2. Counters — scratch discipline, child env, raw echo

### C1 `quality/counters/c1-r79-reserve.py`

- **Scratch:** `--scratch-root` required (usage → rc 2, :277); refuses `/` (:283) and a symlinked scratch root
  (:284); `tempfile.mkdtemp(dir=args.scratch_root)` (:289); removal guaranteed in `finally: rmtree` (:367).
  No `/tmp` default anywhere — the only tempfile call names the scratch dir.
- **Child env:** fixed minimal env (:99-106) — `PATH`, `LC_ALL`, `LANG`, `PYTHONDONTWRITEBYTECODE`,
  `TMPDIR=cwd`. **No inherited secrets.** PASS. `TMPDIR` is even pinned into the scratch so the tool selftest's
  `TemporaryDirectory` never touches `/tmp` (:104-105).
- **Raw echo:** case rows print parsed fields only (:327); no child stdout is echoed raw.
- **F2 (LOW):** `resolve()`/`extract()` run git with `cwd=repo` while `env["TMPDIR"]` equals that cwd (:99-106
  applied to every `run`): a git temp spill would land in the repo. `rev-parse`/`show` never spill, so this is
  theoretical; remediation is a scratch `cwd` or a dedicated `TMPDIR` for the two git helpers.
- **F3 (LOW):** the symlink refusal checks only the final path component (`os.path.islink`, :284). A scratch
  root *under* a symlinked ancestor passes. Checked this host: `/fast`, `/fast/scratch`, `/fast/scratch/hyaku`
  are real dirs today. Remediation: compare `os.path.realpath(parent)` before `mkdtemp`.

### C2 `quality/counters/c2-r79-runbook.py`

- **Scratch:** same discipline — required (:454), refuses `/` (:460) and a symlinked final component (:461),
  `mkdtemp` (:466), `finally: rmtree` (:581). PASS.
- **F4 (INFO/by design, recorded):** child env is `dict(os.environ)` (:108) — the full parent environment,
  secrets included, reaches every row child (`/bin/sh -c` for live rows). This is necessary for the session
  probes (Wayland/DBus), but it is the opposite of C1's minimal env. The counter also *probes the host*: it
  sets `HYPRLAND_INSTANCE_SIGNATURE` by listing `$XDG_RUNTIME_DIR/hypr` and picking the lexicographically
  first entry with `.socket.sock` (:115-121) — with two live sessions it can attach to the wrong one; sets
  `OMARCHY_PATH` by probing `~/.local/share/omarchy/bin` (:124-131); appends five directories to `PATH`
  (:133-140). None of these probed values is ever printed. Smallest remediation for the env: a passlist
  (`PATH`, `LC_ALL`, `LANG`, `XDG_RUNTIME_DIR`, `WAYLAND_DISPLAY`, `DBUS_SESSION_BUS_ADDRESS`,
  `HYPRLAND_INSTANCE_SIGNATURE`) instead of wholesale inheritance.
- **F5 (LOW):** the four refusal rows invoke `python3` (resolved from that extended `PATH`) rather than
  `sys.executable` as C1 does — a `python3` earlier in the parent PATH shadows the interpreter (the pinned
  `.py` bytes are hash-bound by `tree=bound`; the interpreter is not). Remediation: `sys.executable` in the
  frozen argv next generation.
- **Raw echo — good design, verified in the receipt:** `observed()` (:331-341) prints `rc=%d json-bytes=%d`
  for all JSON kinds (:334) — the receipts indeed show `json-bytes=1339` for the monitors dump, whose reply
  carries serials/descriptions, never quoted; every other kind is truncated at 100 chars. Error paths echo
  `argv` only (:148), never env.
- **F6 (MEDIUM-LOW, contract integrity):** rows are bound by `cell == case["skill_anchor"]` (:509) but the
  bytes executed are `case["argv"]` (:524) — the counter never asserts the argv *is* the anchor command.
  Measured today across all 22 cases: the 18 `/bin/sh -c` rows satisfy `argv[2] == skill_anchor` and the 4
  refusal rows satisfy `join(argv) == skill_anchor` (jq check, byte-equal) — **no live divergence** — but a
  future frozen set could execute different bytes than the published row while still printing `rows=22/22`.
  Smallest remediation (one assertion in the counter): require
  `argv == ["/bin/sh", "-c", skill_anchor]` for shell rows and `" ".join(argv) == skill_anchor` for the rest.
- **F7 (LOW-MED, receipt integrity):** C1 prints the control set's sha256 (`MADO_R79_CONTROL … sha256=`,
  :318/:353); **C2 never prints any control-set hash** — the `MADO_R79_RUNBOOK` verdict line (:568) carries
  only `rev` and `tree=bound`, so a C2 receipt cannot prove which control-set bytes produced it. Remediation:
  add `controls_sha256=<sha>` to the verdict line.

## 3. Session material / secret shapes in the new artifacts

Scope = the freeze diff `e4b153df..5eb8f20f` (declaration; both control sets + both makers; 10 fetch files +
`sha256-r79.txt`; 12 fixture files; 5 receipts; both counters; SKILL.md round-79 section + 2 ledger rows;
`quality/tool-ledger.md` row updates).

- **Fixtures — clean, synthetic:** monitors `M1`, layer pid `4242`, output pattern `"DP-1 DP-2"`, scale `2.0`
  (`fixtures/refuse-*/`). No description/serial/make/model fields anywhere (jq scan over both case sets).
- **Fetch pins:** upstream Hyprland bytes. `S459.bin` and `S466.bin` share sha `0a52e145…` because both pins
  are `src/desktop/reserved/ReservedArea.cpp` at the same upstream commit — verified identical heads, expected,
  not duplication. S462's 404-and-r78-pin-reuse is disclosed in the declaration.
- **No instance signature, token, hostname, window title or session path in any new artifact.** The carried
  exact outcomes are host *config* values by design (`str: br`, `custom type: 0 0 0 0`, `Matte Black`, binds
  `192`, namespaces `wallpaper,waybar`).
- **F8 (LOW, the one pid):** case `waybar-process` carries `"frozen": "1720"` — a real waybar PID captured at
  round 78 — in `.ufo/waves/round-79/controls/c2-runbook-cases-r79.json`, and it recurs verbatim in
  `receipts/measurement-c2-r79.txt` (`name=waybar-process … out='1720'`). It is currently unreferenced by the
  live rule (that row is `int_range [1,4194304]`); only the held-r78 fixed-value control and the receipts show
  it. The carried-field assertion (`c2-r79-runbook.py:472-481`) forbids removing it this round. Future
  remediation: re-bind this row shape-only (as was done for the keybindings row) and drop the pid from
  `frozen` at the next allowed control-set generation.
- **Truncation containment:** the keybindings receipt line stops at 100 chars (`SUPER + RETURN → Terminal\n
  SUPER ALT + RETURN → Tmux\nSUPER S…`) — application names, not window titles; the full live bind list is not
  committed.
- **Pre-existing, out of round scope (flagged for a future pass):** SKILL.md's older rows commit
  `~/.config/hypr/gkeep.conf` plus a host-specific rule capture (`size arg=420x500 class=^(org.omarchy.gkeep)$`)
  from round 43, and the ledger's updated r77 row commits the generic host path `~/.config/hypr/monitors.conf`.
  Both predate this round's diff (the gkeep row) or name a standard config location (monitors.conf).
- Control/base receipts are single-line setup errors or parsed fields only — clean
  (`control-c2-r79-at-base.txt`, `control-c2-heled-instrument-at-base.txt`, `control-c1-r79-at-base.txt`).

## 4. Runbook rows — write scope

All 22 executed commands (frozen `argv` in `c2-runbook-cases-r79.json`, byte-equal to the SKILL.md:231ff rows —
verified case by case):

- hyprctl read verbs only: `version`, `configerrors`, `monitors -j`, `getoption general:gaps_out`,
  `getoption input:kb_layout`, `binds -j`, `layers -j`, `activeworkspace -j`, `workspaces -j`,
  `clients -j` — all pipes (`head -n 1`, `jq`, `sort | join`) **no redirection anywhere, no `keyword`,
  `dispatch`, `reload`, `setprop`, `output`, `plugin`**.
- `pgrep -x waybar | head -n 1` — read-only.
- `makoctl mode` — the read form; no `dismiss`/`mode -s`/`restore`.
- `omarchy theme current`, `omarchy version`, `omarchy menu keybindings --print` — the printing variants; no
  `theme set`, no menu *opening* subcommand.
- The four `python3 -I tools/mado-barfoot.py --config … --layers … --monitors …` rows run the lane's read-only
  join over committed fixtures (the tool opens three repo-relative files, writes nothing, starts nothing —
  verified above).

**Could a row be made to write?** Only by editing the frozen, sha-pinned control set (and matching SKILL.md
row) to smuggle `>` or a mutating verb through the `/bin/sh -c` wrapper — the freeze, the carried-field
assertion and (visually) the C1-style control hash stand in the way today; the counter itself enforces neither
the anchor↔argv equivalence (F6) nor a control-set hash in the receipt (F7). The table's text does not invite
writes: the section intro states "the command cell is the exact command the case executes … all read-only",
binds refusal *stage* rather than message, and no outcome cell suggests a mutating variant.

## Severity summary

| # | Finding | Sev | Evidence | Smallest remediation |
|---|---|---|---|---|
| F1 | lstat/open TOCTOU in `read_bytes` (no `O_NOFOLLOW`) | LOW | `tools/mado-barfoot.py:124-143` | `os.open` + `O_NOFOLLOW` + `fstat` |
| F2 | git helpers run with `TMPDIR=repo` | LOW | `c1-r79-reserve.py:99-106` vs `cwd=repo` call sites | scratch `cwd`/`TMPDIR` for `resolve`/`extract` |
| F3 | symlink refusal checks final component only | LOW | `c1:284`, `c2:461` | realpath the parent before `mkdtemp` |
| F4 | C2 children inherit full parent env (incl. secrets); host probing of session dir | INFO/by design | `c2-r79-runbook.py:108-140` | env passlist for row children |
| F5 | refusal rows use PATH-resolved `python3`, not `sys.executable` | LOW | case `argv` vs `c1:170`-style `sys.executable` | `sys.executable` in next frozen argv |
| F6 | executed `argv` never asserted equal to the bound row text | MED-LOW | `c2:509` vs `c2:524` (measured equal today, all 22) | one assertion in the counter |
| F7 | C2 receipt carries no control-set sha256 | LOW-MED | `c2:568` verdict line vs `c1:353` | add `controls_sha256=` to the verdict line |
| F8 | stale waybar PID `1720` committed in `frozen` + receipts | LOW | `c2-runbook-cases-r79.json` case `waybar-process`; `measurement-c2-r79.txt:9` | shape-bind the row at the next control-set generation |

Nothing found rises to a blocker for the frozen round: the two claims' instruments behave as declared, both
counters are scratch-clean and refuse `/` + symlinked scratch, C1's child env is minimal, no rules-file content
or JSON dump is ever echoed, no session signature/title/token is committed by this round, and every runbook row
is a read verb.

Receipts cited (copies in `w1/R79Sentinel/receipts/`): `receipts/measurement-c1-r79.txt`,
`receipts/measurement-c2-r79.txt`, `receipts/control-c1-r79-at-base.txt`,
`receipts/control-c2-r79-at-base.txt`, `receipts/control-c2-heled-instrument-at-base.txt`.

Report: .ufo/waves/round-79/w1/R79Sentinel.md
