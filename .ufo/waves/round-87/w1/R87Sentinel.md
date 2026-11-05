# R87Sentinel — security & privacy review (round mado 87, wave w1)

Date 2026-11-05. Read-only seat. Reviewed the six round-87 artifacts once they existed (watcher
window 1: 15 checks × 60 s, 0→5/6 present; window 2: 14 checks, `mako-cases-r87.json` PRESENT at
check 14, file mtime 06:21:26 -0300) plus the wave evidence in `w1/` as of close (9 reports +
`swarm-registry.json`; `R87Scout.md` and `R87MutTester.md` were still absent at close — not
reviewed). No lane counter was executed (L1 runs them). Dynamic probes of `tools/mado-mako.py`
ran once each in `$HYAKU_SCRATCH/mado-r87/R87Sentinel/` (deleted on exit; verified absent).
No installs (no pacman, no uv, no binaries). All pattern scans used the file-selector `grep`
tool, never shell grep.

## Checks, commands, counts

**C1 — secret-shaped material.** `grep pattern='op://|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{16,}|github_pat_|xox[abps]-|sk-[A-Za-z0-9]{16,}|-----BEGIN [A-Z ]*PRIVATE|api[_-]?key|apikey|passw(or)?d|secret|Bearer |set-cookie|set_cookie'` over `tools/mado-mako.py`, `quality/counters/c1-r87-mako-criteria.py`, `quality/counters/c2-r87-control-fidelity.py`, `controls/mako-cases-r87.json`, `controls/mako-mutants-r87.json`, `controls/r86-figures-r87.json` → **0 hits**. Same pattern + `cookie` over all 9 w1 reports → **0 hits**. Count: 0.

**C2 — device/window/network identifiers.** `grep pattern='serial|monitor|edid|dbus|DBUS_SESSION|unix:path|wayland|xdotool|wmctrl|window.?title|WM_CLASS|([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}|([0-9]{1,3}\.){3}[0-9]{1,3}'` over the six artifacts → **0 hits** (the tool never even names wayland/dbus despite being a mako resolver); over all 9 w1 reports → **0 hits**. No monitor serials, no MAC/IP, no session-bus addresses, no window titles in fixtures or reports. Count: 0.

**C3 — operator home path.** `vgpnk` in the three code files and three control JSONs → **0 hits**. In w1 reports, occurrences (all host-anchor citations required by the content — lane roots, census/git commands, and the config plane under study):
- `R87Connector.md` 8, 12, 15 (lane-tree grep commands, omarchy skill path).
- `R87ExecFidelity.md` 3; `R87ExecMako.md` 3 (lane-root headers).
- `R87ScribeEntry.md` 3, 37, 185, 186, 231 — 37/185/186 cite the real mako plane (`~/.config/mako/config` → omarchy theme `mako.ini` → `default/mako/core.ini`, with sha256s); 231 records `XDG_CONFIG_HOME=/home/vgpnk/.config` — justified: it is the observed anchor for open question U2 (XDG resolution), standard default value.
- `R87ScribeLesson.md` 3, 106, 143 (lane root, census command, git ls-files command).
- `R87ReviewMako.md` 4 (target path header). `R87Critic.md`, `R87ExecCounter.md`, `R87ReviewFidelity.md`, `swarm-registry.json`: 0.
Compliant with "only where a manual or host-anchor citation requires it". Count: 16 lines, 0 defects.

**C4 — literal `/tmp`.** `grep pattern='/tmp'` over the three .py files → **0 hits**; over the 9 w1 reports → **0 hits**. Purpose of each hit: n/a — there are none. Nuance, not a literal: `c1-r87-mako-criteria.py:573` `tempfile.mkdtemp(prefix="mado-mako-selftest-")` omits `dir=`, so `--selftest` alone puts its fixture in the default temp root when TMPDIR is unset (removed in `finally` at :658; the counting path always requires and pins `--scratch-root`, :369). Info finding F6.

**C5 — tool write confinement.** Code: the only write sites are `_write` (`tools/mado-mako.py:388-391`, `makedirs` + `open(path,"w")`) called only from `selftest`, whose tree is `tempfile.mkdtemp(prefix="mako-selftest-", dir=scratch_root)` (:397) removed by `shutil.rmtree(work)` (:486); the only other `open` is the read at :222; `main()` prints only. Dynamic: probes A–C ran the resolver on symlink/absolute/device includes — probe D (`find -newer marker`) showed **zero files written** during the runs; probe E: `--selftest --scratch-root <dir>` → `MADO_MAKO_SELFTEST: checks=29 failed=0`, exit 0, zero residue. **PASS — no write outside `--scratch-root`** (and none at all outside selftest mode).

**C6 — tool network.** `grep pattern='socket|urllib|urlopen|http\.client|requests\.|http://|https://|ftplib|smtplib|telnetlib|getaddrinfo'` → 0 hits; imports are argparse/json/os/re/shutil/stat/sys/tempfile (:51-58); no `subprocess` anywhere. Corroborated by `R87ReviewMako.md` import-spy under `python3 -I`. **PASS — opens no socket.**

**C7 — symlinked include target that escapes HOME.** `include()` at `tools/mado-mako.py:339-363`: tilde form joins `self.home` (:340-341), absolute accepted verbatim (:342-343), `os.stat` follows symlinks (:348), refuses non-regular targets (:353-354), `os.path.realpath` used **only** for cycle detection (:356-359) — there is **no HOME containment check**. What it actually does (measured, exit codes from the runs):
- Probe A — `~/escape.ini` symlink → `$S/outside/escape.ini` (outside HOME): **exit 0, `refusals=0`, external file parsed and applied** (`width=1234` entered `effective`; `applied` lists the configured path).
- Probe B — `include=/dev/null`: refused "not a regular file" (`refusals=1`), resolution exit 0.
- Probe C — `include=/etc/hosts` (absolute, outside HOME, regular): **applied, exit 0**.
**Finding S4 (LOW): it does NOT refuse an escaping symlinked include; it follows it.** Impact bounded: read-only local oracle — refusal strings echo the absolute target path + line number (:350-351, :354), recognized `key=value` lines surface in `effective`; no content reflection beyond mako keys; no network. Note the tool's own header contract (:13-16) claims only regular-file/missing/cycle refusals, so this is under-documented, not misimplemented; the counter's `globals-include` control *is* home-contained (`include_target`, c1:246-262), i.e. stricter than the tool under test — harmless for scoring (controls need only score below N).

**C8 — counters scrub GIT_DIR and friends.** C1: `SCRUB` (:40-46) = GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES; applied in `git_env()` (:59-62) to every `git` subprocess; plus `GIT_NO_REPLACE_OBJECTS=1`; selftest proves it with a decoy GIT_DIR (:604-615). C2: `GIT_SCRUB` (:39-40), same five, applied in `git_env()` (:57-59) to every subprocess incl. the flood re-run (:189). **PASS.** Residual (Info F7): neither scrubs `GIT_COMMON_DIR` or the `GIT_CONFIG_*` family; the executed git surface is read-only (`rev-parse --verify`, `show`) with `-C repo`, so practical impact is negligible in the L1's trusted shell.

**C9 — counters never write the repo, never hardcode /tmp.** C1 writes: homes/tool/mutants under `gen` (:192-202, :372-373, :390-391), selftest fixtures under its scratch (:592-595); `rmtree` :415, :658; reads cases/mutants from caller paths (:430, :442); git ops read-only except selftest fixture commits (`git init/add/commit` inside a `mktemp` fixture with throwaway identity `-c user.name=mado-selftest` :596-599, toplevel asserted :577-580). C2 writes: r85 module + flood files under `work` (:148, :176-185), fixtures under its root (:275-283), `mkdtemp(dir=scratch)` :220, :304, `rmtree` :234, :369; real-run git ops read-only; fixture commits with throwaway identity and `commit.gpgsign=false` (:284-287), toplevel asserted (:277-279). **PASS — zero repo writes in the counting path.**

## Findings (severity-rated)

**F1 — HIGH (blocks C1 scoring): frozen cases file is rejected by the frozen counter at load.**
`controls/mako-cases-r87.json` uses `"app_name"` / `"modes"` in every one of the 23 `args` objects (lines 11/13, 31/33, 50/52, 69/71, 88/90, 107/109, 126/128, 147/149, 168/170, 190/192, 209/211, 228/230, 247/249, 267/269, 288/290, 307/309, 326/328, 345/347, 364/366, 385/387, 402/404, 419/421, 436/438). The counter validates against `ARG_NAMES = ("app-name", "urgency", "mode")` (`c1-r87-mako-criteria.py:49`) with `not set(args) <= set(ARG_NAMES)` → `SetupError` (`:131-133`), before any case runs (`run()` → `load_cases` :427). The declared counting command therefore exits 2 (`MADO_MAKO_CRITERIA: SETUP_ERROR C01-...args: unknown or non-object args`) for these bytes; C1 is unscoreable as frozen. Ground truth is from bytes only (counter not run). Smallest remediation: rename the two keys to `app-name`/`mode` in the 23 args objects (or widen `ARG_NAMES` to accept both spellings) — frozen-artifact procedure is the L1's call.

**F2 — HIGH (independently verified; corroborates `R87ReviewMako.md` G1): case C13 is unsatisfiable.**
`mako-cases-r87.json:245` `"config": ".config_mako/config"` (underscore typo) while its `home_files` (:242-244) materialize only `.config/mako/config`; the runner joins home+config raw (`c1-r87-mako-criteria.py:207`), so the tool gets a nonexistent `--config` → exit 2 → case fails. Even with F1 fixed, correct caps at 22/23 → score 9.57 → `TARGET_MISSED` for a perfect tool. ReviewMako's replay reproduced exactly this and showed the corrected path passes.

**F3 — MEDIUM (privacy/contract; corroborates `R87ReviewMako.md` D1): environment-dependent file reads.**
`tools/mado-mako.py:522` `home = args.home or os.path.expanduser("~")` — without `--home`, `~/` includes resolve against the process HOME, reading files the caller never named, against the declaration's "reads only the regular files its caller names". The C1 runner always passes `--home`, so scoring is unaffected; the exposure is the bare-CLI path.

**F4 — LOW: no HOME containment on includes (see C7).** Smallest remediation: for tilde-form includes, require `os.path.realpath(target).startswith(os.path.realpath(self.home) + os.sep)` before reading (absolute-form is the documented alternate form — decide whether it stays open); add the escaping-symlink case to the selftest.

**F5 — MEDIUM (report provenance, not substance): `R87ReviewMako.md` timeline conflicts with the filesystem.** Snapshot 1 (mtime 06:12) narrates a poll window ending 06:38; snapshot 2 (mtime 06:23:53, current) narrates "landed ~06:39 in poll window 2" and a replay "06:44" — events that post-date the file's own last write. Filesystem ground truth: cases mtime 06:21:26; my watcher found it present at window-2 check 14 (~06:21-06:22). The G1/C13 defect itself is byte-verified by this seat, so the wave's substance does not rest on the report's clock; the seat should re-issue timestamps that match the filesystem. (No other w1 report showed this pattern.)

**F6 — Info:** C1 selftest fixture in the default temp root when TMPDIR is unset (:573, cleaned :658) — see C4.
**F7 — Info:** scrub lists omit `GIT_COMMON_DIR` / `GIT_CONFIG_*` (C1 :40-46, C2 :39-40) — see C8.
**F8 — Info:** C2 executes the r85 counter bytes from REV via `importlib` (`exec_module`, :150-152) — the declaration's stated mechanism; `sys.dont_write_bytecode = True` (:29) prevents `__pycache__`; fixture-only writes stay under `--scratch-root`.

## Cross-seat corroboration

`R87ReviewFidelity.md`, `R87Critic.md`, `R87ExecCounter.md`, `R87ExecFidelity.md`, `R87Connector.md`, `R87ScribeEntry.md`, `R87ScribeLesson.md`, `swarm-registry.json`: no secret/device/home-path findings beyond C3's list; fixtures and receipts described there are scratch-scoped with cleanup receipts.

## Dead steps

- Watcher window 2 checks 1-13: cases absent (expected; artifact landed at check 14).
- Probe E first attempt: exit 2 `--scratch-root is not a directory` — my invocation error (dir not pre-created), not a tool defect; rerun with `mkdir -p` passed 29/29.
- One grep call used a mistyped lane path (`mado-shokununin`) for `R87ScribeLesson.md` — rerun clean; no result affected.

## Installs

None.
