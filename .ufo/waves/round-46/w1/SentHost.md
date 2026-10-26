# SentHost — host-mutation audit of the round-46 w1 instructions

Report: `.ufo/waves/round-46/w1/SentHost.md`
Seat: `SentHost` (sentinel). Date 2026-10-26. Lane `mado-shokunin`.
Inputs: `.ufo/waves/round-46/w1-spec.json` (66 items, context 9670 B), `.ufo/waves/round-46/registration.md`
(frozen, `8c5434c6`), plus the lane rules the items themselves point at (`SKILL.md`, `PROVINCE.md`) and the
lane scripts the items run (`tools/mado-verify.sh`, `quality/*.py`, `scripts/sources-census.sh`).
Evidence transcript: `.ufo/waves/round-46/w1/SentHost/checks.txt` (all locators below are `checks.txt:<line>`).

**Bottom line.** No item asks a seat to run a mutating compositor verb: across all 66 prompts, `hyprctl`
followed by `dispatch`, `keyword`, `reload`, `setprop`, `setcursor`, `switchxkblayout`, `output`, `notify`,
`plugin` or `--batch` occurs in command position **0 times** (`checks.txt:46`), and no item names `pacman`,
`systemctl`, `journalctl` or `udevadm` as a command (`checks.txt:173-179`). The mutating-command risk in this
wave is not the happy path; it is instruction wording that can put a host secret into process argv (H2), retain
hardware identity in committed evidence (H1), or leave a gate's default mode outside the wave's own read
whitelist (H3). Ten findings: five medium (H1-H3, H9, H10), one low-medium (H4), four low (H5-H8); none
critical. H10 is a provenance state, not an exploit: a v2 re-registration is being built untracked and its freeze
document is absent while eleven items still name the v1 counters.
H9 is a harness defect reported by the sibling sentinel and verified here at code level: the counter's read-only
clause is unsound and its sandbox is read-permeable to the live compositor socket.

---

## 1. Command inventory — every host command a seat is told to run

"Host command" = anything the item text executes against the host (compositor, host config tree, host
library/compiler, host home directory) rather than against the lane or a scratch clone. Fragments are as
written in the item (computed inventory: `checks.txt:3-46`).

| # | Item (role) | Command as instructed | Surface | Verdict |
|---|---|---|---|---|
| 1 | ExecLiveHost (executor) | `hyprctl devices -j \| python3 -I <ref> --devices - --config ~/.config/hypr/input.conf` | compositor read + file read | **allowed** — `devices -j` is on the context whitelist (`context:51`); the reference imports no `subprocess`/`socket` and uses neither (`checks.txt:158`) |
| 2 | ExecLiveHost | read every `.conf` reached by `source =` in `~/.config/hypr/hyprland.conf` (18 source lines, `checks.txt:169`), grep for `kb_`/`device`/`scroll_factor` | host tree read | **allowed** (config trees READ-ONLY, `context:53`) |
| 3 | ExecLiveHost | read `~/.local/share/omarchy/default/hypr/input.conf` "read-only" | host tree read | **allowed**; file exists (`checks.txt:125`) |
| 4 | ExecLiveHost | "the same dump against a **scratch copy** of input.conf with `kb_layout = zz`" | **file write, target not named** | **H5** |
| 5 | ExecW2Monitors (executor) | `hyprctl monitors all -j \| <tool from git show 4d22eeb…> --monitors - --config ~/.config/hypr/monitors.conf` | compositor read + file read | **allowed**; tool has no process/socket path (`checks.txt:159`) |
| 6 | ExecW2Monitors | materialize `tools/mado-monitors.py` out of `git show` (no output dir named) | **write, target not named** | **H4** |
| 7 | ExecSerialRule (executor) | `hyprctl monitors all -j` → shell var; `git -C <lane> grep -l -F "$SERIAL" <rev>` | compositor read + **secret in argv** | **H2** |
| 8 | ExecSerialRule | `$SERIAL` must never be echoed; only paths/lines/counts printed | process discipline | conforms, but defeated by #7 (argv) |
| 9 | ExecXkbCompile (executor) | ctypes on host `libxkbcommon` (`xkb_context_new`, `xkb_keymap_new_from_names`); compare `active_keymap` from `hyprctl devices -j` | host library load + allowed read | **allowed** — in-process library, no Wayland client, no write surface; residual `XKB_CONFIG_ROOT` risk is the item's own question |
| 10 | ExecHarmBase (executor) | `bash tools/mado-verify.sh --selftest`; `quality/check-axis-scores.py …`; `quality/check-index.py …`; round-45 counters; `tools/mado-monitors.py --selftest`; `tools/mado-geometry.py --selftest`; `…/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | host script runs | `--selftest` **verified hermetic** (rc 0, `460/460`, zero files in redirected `HOME` and cwd, `checks.txt:54-57`); but the relative paths and the script's default live mode make **H3** |
| 11 | ExecSupersede (executor) | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/SOURCES.md` | fleet script | **allowed** — header: "writes only stdout or `--out`" (`scripts/sources-census.sh:7`) |
| 12 | ExecHarmBase / ExecDataRehearsal | `tools/*.py --selftest` for every tool with a selftest | lane tools | allowed; three tools need an argument (§5, O2) |
| 13 | CritPremise (critic) | `hyprctl getoption input:kb_layout`, `hyprctl devices -j`; `grep ~/.local/share/omarchy/bin` (read-only) | compositor read + host tree read | **allowed** (`context:51`) |
| 14 | CritW2Gate (critic) | craft a fixture that is "`hyprctl clients` plain text" | compositor verb named, not marked synthetic | **H6** |
| 15 | RevPrivacyRound (reviewer) | rule on `hyprctl devices -j` product names as session material | allowed read | **allowed**; the ruling is pre-empted by #1 of H1 |
| 16 | CritRegistration (critic) | "check … against the repo **and the host**": base hash, versions, keyboard and pointer counts, "one input block and no device block" | compositor reads + host tree reads | **allowed** (the item names no verb; every read it needs is whitelisted or file-only) |
| 17 | ConnSiblings (connector) | read sibling-lane `PROVINCE.md` and grep corpora for `hyprctl devices` | file reads | allowed |
| 18 | ScoutOmarchyInput (scout) | read `~/.local/share/omarchy/default/hypr/input.conf`; grep `bin` and `migrations` "read-only; never run them" | host tree read | **allowed**, explicitly fenced |
| 19 | ScrSerialCorrection (scribe) | `hyprctl monitors all -j` → `git grep -c -F "$SERIAL"` | compositor read + **secret in argv** | **H2** (same defect, second seat) |
| 20 | ExecHyprlangOracle, ExecHyprlangOracleB, ExecStofOracle, LabFloatFormat, LabDupNames, RevengerHyprlang | `g++ -std=c++23 -lhyprlang` against `/usr/include/hyprlang.hpp` + `/usr/lib/libhyprlang.so` | host compiler + host library | **allowed** (present: `checks.txt:103-109`); **H4** for the unnamed output dir |
| 21 | LabVirtualRules, ScoutRecheck, ScoutFrontier | fetch upstream raw/API (`efb50993`, Hyprland/hyprlang main) | network read | allowed (no install, no package action) |
| 22 | ExecSeedSweep, CritC1Cheat, CritC1Narrow, ExecDoNothingC1, Mut*, ExecIndep*, ExecC1Separability, ExecDataRehearsal, RevC1Counter, RevC2Counter, CritC2Forgery | `python3 -I quality/counters/c1-r46-devices.py|c2-… --repo <clone> --rev HEAD --work /fast/scratch/…` | counter runs (bubblewrap per tool run) | **allowed for writes, not for reads** — sandbox is `--ro-bind / /` + tmpfs over repo/lane/lane-parent + writable bind of its own marker dir only, `--unshare-pid --unshare-net` (`checks.txt:111-119`); read-permeable and clause r unsound → **H9** |
| 23 | SentTool (sentinel) | review the counters' scratch handling and fake PATH binaries | review only | n/a |

Counts for the compositor verbs actually named in command position: `devices` 5 items, `monitors` 3,
`clients` 1, `getoption` 1, and 0 for every mutating verb (`checks.txt:29-46`).

---

## 2. Findings

### H1 — Medium — ExecLiveHost instructs a seat to commit input-device product names
- **Attacks:** `.ufo/waves/round-46/w1-spec.json` item `ExecLiveHost`; `.ufo/waves/round-46/registration.md` shape-only posture.
- **Instruction:** "device names are product names: keep them; drop nothing else is needed" (item `ExecLiveHost`).
- **Exploit path:** a seat follows the sentence literally and writes the 10 keyboard and 4 pointer names from
  `hyprctl devices -j` into `.ufo/waves/round-46/w1/ExecLiveHost/runs.txt`, which the L1 integrates. The
  committed receipt already carries two such names: `.ufo/waves/round-46/receipts/live-devices-host-l1.txt:5`
  (a FIDO CCID security-key keyboard) and `:11` (a launcher/audio device); locators computed, values not
  reproduced (`checks.txt:167-168`). That set is a hardware fingerprint of the operator's desk.
- **Contradiction:** the context says session material "stays shape-only: never commit window titles, monitor
  serials/descriptions, process tables or home-directory listings" (`context:53-54`), and the wave charters
  `RevPrivacyRound` to "rule explicitly on whether input device product names … are session material"
  (item `RevPrivacyRound`). Item `ExecLiveHost` pre-empts that ruling in the affirmative.
- **Impact:** irreversible-by-policy disclosure of input hardware into pushed history — the same class the
  round's own D2 treats as unrecoverable without an operator decision (`corpus/lessons/round-45.md`, closure D2).
- **Smallest remediation:** change the sentence to "project the dump to counts and per-class verdicts; if you
  need exact names while debugging, keep them only in an uncommitted scratch file", or make it conditional on
  `RevPrivacyRound`'s ruling. One sentence, no counter change.

### H2 — Medium — the serial is put into process argv by ExecSerialRule and ScrSerialCorrection
- **Attacks:** items `ExecSerialRule` and `ScrSerialCorrection`; the context's absolute rule.
- **Instruction:** `ExecSerialRule` runs `git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -l -F "$SERIAL"
  4d22eeb…` with the rider "NEVER echo the value"; `ScrSerialCorrection` says to "verify the counts with
  `git grep -c -F` using a shell variable read from `hyprctl monitors all -j`".
- **Exploit path (two, both real):**
  1. **Argv disclosure.** `$SERIAL` becomes an element of `git`'s command line. `/proc/<pid>/cmdline` is
     world-readable `0444` (`checks.txt:100-101`; dummy token, no host value used). Any process, an audit
     daemon or a crash reporter can read the serial, and any `set -x`/trace or pasted command carries it.
     "NEVER echo the value" is satisfied while the value is still written, which is exactly what the context
     forbids: "Never write the host monitor's serial number anywhere" (`context:54-55`).
  2. **Empty-pattern false evidence.** If the extraction yields empty (field renamed, `jq` absent, typo in the
     key), `git grep -l -F ""` matches **every tracked file** with rc 0 (`checks.txt:92-94`). The D2 counts
     (3 held entries + 21 wave files) then become an unverifiable receipt that still "passes".
- **Impact:** the secret lands in a readable process table; the closure count can silently become false.
  Serial shape here is 12 characters, mixed class (`checks.txt:132`) — selective enough that a prose pattern
  is plausible, short enough that quoting it anywhere is still a disclosure.
- **Smallest remediation:** feed the pattern on stdin, which keeps argv clean and fails closed:
  `[ -n "$SERIAL" ] && printf '%s\n' "$SERIAL" | git -C <lane> grep -l -F -f - <rev>`. Verified in a scratch
  repo: `-f -` works and an empty stdin gives `fatal: no pattern given` rc 128 (`checks.txt:95-97`). Apply the
  same form to the optional `--serial-from-host` gate mode; otherwise that gate permanently embeds a live
  read plus the argv leak in a committed file.

### H3 — Medium — the only gate instruction is safe only as written; the same script's default mode is outside the whitelist
- **Attacks:** item `ExecHarmBase` and, by adoption, `ExecDataRehearsal` ("`tools/*.py --selftest`").
- **Instruction:** `bash tools/mado-verify.sh --selftest`, given with **lane-relative** paths from a seat cwd
  that is the fleet root (`quality/check-axis-scores.py`, `quality/check-index.py`, `tools/mado-monitors.py`).
  The fleet root has no `quality/` directory (`checks.txt:170`), so the first commands fail.
- **Exploit path:** the natural recovery from a relative-path failure is `cd <lane> && bash tools/mado-verify.sh`,
  dropping `--selftest`. The script's default is a live run with `ROOT="${MADO_VERIFY_ROOT:-$HOME}"`
  (`tools/mado-verify.sh:109`) that executes `hyprctl -j instances` (`:3421`), `configerrors` (`:3443`),
  `-j binds` (`:3499`), `monitors` (`:3515`) and `-j layers` (`:3595`) — four verbs the round-46 whitelist
  does not contain (`context:51-53`). `--selftest` itself is safe: verified rc 0, `460/460`, no file created
  in a redirected `HOME` or cwd (`checks.txt:54-57`).
- **Impact:** out-of-whitelist compositor reads (bind table, layer names, config errors) during a round whose
  context fences exactly that; the read fence then rests only on the seat's care.
- **Smallest remediation:** write the item as an absolute path plus an explicit stop: "run
  `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh --selftest`; the live mode is out of scope
  this round". Two changes, both in item text.

### H4 — Low-Medium — six compile/materialize items name no output directory, and the seat cwd is the fleet root
- **Attacks:** items `ExecHyprlangOracle`, `ExecHyprlangOracleB`, `ExecStofOracle`, `LabFloatFormat`,
  `LabDupNames`, `RevengerHyprlang` (all "a small C++ program … `g++ -std=c++23 -lhyprlang`") and
  `ExecW2Monitors` ("`<the tool from git show …>`").
- **Exploit path:** `g++ probe.cpp -lhyprlang` with no `-o` writes `a.out` into the current directory, which is
  `/home/vgpnk/Projects/shokunin` (host guard). Likewise `git show …:tools/mado-monitors.py > tool.py` with a
  relative path. 6 of 66 items name `/fast/scratch` at all (`checks.txt:48-51`), and none of the eight above
  does.
- **Impact:** untracked binaries/scripts in the fleet root — a write outside the seat's scope, and a plausible
  trigger for a seat to "tidy" with `rm` in a directory it does not own.
- **Smallest remediation:** append the seat's scratch path to those eight item texts (the context already
  mandates `/fast/scratch/hyaku/mado-r46/<Seat>/`; the items just have to say it once).

### H5 — Low — ExecLiveHost's `kb_layout = zz` copy has no named target
- **Attacks:** item `ExecLiveHost`, step (4).
- **Exploit path:** "a scratch copy of input.conf" is one keystroke from
  `cp ~/.config/hypr/input.conf ~/.config/hypr/input.conf.zz`, i.e. a write into a config tree the lane's own
  fence calls mutating: "any file write under `~/.config/`…" (`SKILL.md:322`, under "Mutating commands —
  operator only, mado never runs", `SKILL.md:314`), and `context:53` ("Host config trees … are READ-ONLY").
- **Impact:** a stray file in the operator's Hyprland tree; not compositor state until reloaded, but outside
  every declared surface and invisible to the round's gates.
- **Smallest remediation:** "write the modified copy under `/fast/scratch/hyaku/mado-r46/<Seat>/`; never under
  `~/.config/hypr`" in the same item.

### H6 — Low — CritW2Gate names the `clients` dump without marking it synthetic
- **Attacks:** item `CritW2Gate`; the context whitelist.
- **Instruction:** "Craft committed-file shapes it misses (… `hyprctl clients` plain text, …)". One item in
  command position (`checks.txt:37`).
- **Exploit path:** a seat runs `hyprctl clients -j` to obtain the shape. That verb is **not** on the round-46
  whitelist (`context:51-53`) and its output is window titles, the first class the shape-only rule names
  (`context:53`). The lane's `SKILL.md:326` *does* list `clients` among permitted read verbs, so a seat that
  reconciles the two documents by the looser rule has a written license for the run.
- **Impact:** window titles in a seat file — the most damaging class in this lane's own risk table.
- **Smallest remediation:** add ", synthesized by hand — never by running `hyprctl clients`" to that clause.

### H7 — Low — three-way disagreement between the lane's fence and the wave's whitelist
- **Attacks:** the round-46 context vs `SKILL.md` vs `PROVINCE.md`.
- **State:** (a) the lane still declares a source-only scope: "This source-only round additionally forbids
  package queries, live reads (including process and compositor probes)" (`SKILL.md:40-42`), "source-only scope
  supersedes the historical conditional license" (`SKILL.md:339`), "round is source-only; no screenshot,
  refresh signal or service launch" (`SKILL.md:613`) — while this wave's context authorizes five live read
  verbs and nine prompts name a live read (`checks.txt:171`), and the registration's own live receipt depends
  on them. (b) `SKILL.md:326` and
  `PROVINCE.md:28` declare a **wider** read set (`clients`, `binds`, `instances`, `layers`, `configerrors`,
  `workspaces`, `animations`) than the context's five. (c) `SKILL.md:350` and `:365` put probe artifacts under
  `/tmp/<lane>-*`, while the operator SCRATCH directive in the context mandates
  `/fast/scratch/hyaku/mado-r46/<Seat>/` and says a `/tmp` path is never citable evidence.
- **Exploit path:** any seat that resolves (a) conservatively refuses work; any seat that resolves (b) by the
  looser document runs `clients`/`binds`/`layers` — the H6 path; any seat that resolves (c) by the lane rule
  produces non-citable evidence.
- **Impact:** the wave has no single authoritative read fence; compliance depends on which document a seat
  read first. No mutation results.
- **Smallest remediation:** one line in the wave context (L1, not a seat): "for this round the whitelist above
  supersedes `SKILL.md:326` and `PROVINCE.md:28`; `SKILL.md:39-44` is historical scope; the operator SCRATCH
  directive governs over `SKILL.md:350`". Reconciling the tracked documents is a later, separate change.

### H8 — Low — the C1 counter accepts a `--work` anywhere outside repo/lane/lane-parent
- **Attacks:** `quality/counters/c1-r46-devices.py` (frozen) as invoked by every counter item.
- **State:** the guard is `hidden_paths(repo) = {repo, lane, parent(lane)}` and the Setup error "work dir inside
  a hidden path" (`quality/counters/c1-r46-devices.py:241-243`, `:424`); the work dir is created with
  `tempfile.mkdtemp(dir=a.work)` and removed with `shutil.rmtree(work)` (`:425-429`). A `--work /home/vgpnk`
  (or `/tmp`) is accepted.
- **Exploit path:** a mistyped `--work` puts transient `c1r46-*` directories under the operator's home (or
  `/tmp`), then removes them. No instruction in the wave passes anything but a `/fast/scratch` path
  (`checks.txt:49`, six items), so this is a guard-strength observation, not an instruction defect.
- **Impact:** transient writes outside the scratch contract if a seat deviates; nothing persistent.
- **Smallest remediation:** none in the data path (the counter is frozen); if it is ever re-cut, refuse a
  `--work` under `$HOME` or under `/tmp` when `/fast/scratch` exists. Until then the wave context's explicit
  path is the control.

### H9 — Medium — the C1 harness's read-only clause is unsound, and its sandbox is read-permeable to the live compositor
- **Attacks:** `quality/counters/c1-r46-devices.py` (frozen) as run by 14 items plus 5 by description; the wave's
  claim that the counter never runs `hyprctl` and that tool runs are isolated.
- **Code shape (verified by reading, `checks.txt:181-191`):**
  1. The fake `hyprctl`/`libinput`/`journalctl`/`udevadm` bin only lands on `PATH` for fixture and generated runs
     (`env_a`/`env_b`, `:260-270`); the **selftest run gets `PATH=/usr/bin:/bin`** (`:375`), so a bare-name
     `hyprctl` inside a tool's own `--selftest` reaches `/usr/bin/hyprctl` and writes no marker. Clause r reads
     only that marker (`:400`).
  2. Any run can exec `/usr/bin/hyprctl` **by absolute path** — the sandbox binds the real filesystem
     `--ro-bind / /` (`:252`) and does not shadow the real binaries.
  3. `hidden_paths()` hides only the repository, the lane and the lane's parent (`:241-243`); `$HOME` and
     `/run/user/<uid>` stay readable, and `--unshare-net` does not isolate AF_UNIX — so a scored tool can reach
     `$XDG_RUNTIME_DIR/hypr/<sig>/.hyprland.sock`. Environment B **supplies that path**: `XDG_RUNTIME_DIR` is set
     to `/run/user/<getuid()>` (`:269`).
- **Exploit path:** a tool that is scored by this counter runs `/usr/bin/hyprctl devices -j` (or connects to the
  request socket directly) and reads the live session — real device names, real config — while printing the
  expected fixture verdicts. The counter still reports `readonly=ok`, because no marker exists. That is both a
  fixture-solving short-cut and a live compositor connection the wave's context forbids a seat to open
  (`context:51-52`); here the seat does not open it, but the harness it is told to run permits the scored
  artefact to.
- **Bounded by:** `--unshare-net` blocks TCP/UDP, and the response the tool returns must still satisfy the 90
  fixtures and 150 generated cases; the live dump helps only where it matches the fixture's synthetic names.
  `SentTool-3` reports executed bypasses reaching `TARGET_MET` at nonce 46 (`.ufo/waves/round-46/w1/SentTool/findings.md`
  F1/F2, receipts `clause-r-bypass-*.txt`); I verified the code shape above and did not re-run their bypasses.
- **Impact:** `readonly=ok` and "no hyprctl run" are not guarantees; the counter can be met by a tool that
  reads the live compositor, which is exactly the property clause r exists to certify.
- **Smallest remediation (the named counter is frozen — for a v2 cut):** `--ro-bind` the four fake binaries
  over their `/usr/bin` names in `sandbox()`; give the selftest `env_a`'s `PATH`; add
  `os.path.expanduser("~")` and `/run/user/<uid>` to `hidden_paths()` so the socket path is tmpfs'ed, and keep
  `XDG_RUNTIME_DIR` out of environment B.
- **State at audit time — an untracked v2 candidate already implements most of this** (`checks.txt:194-223`):
  `quality/counters/c1-r46-devices-v2.py` (sha256 `19d00e66…`, `:202`) replaces the root bind with an allowlist
  (`--ro-bind /usr`, `--ro-bind /etc`, `--tmpfs /tmp`, no `/run`), puts the fake bin on the **selftest** `PATH`
  (`:403` in-file) and replaces the deletable marker with an inherited pipe (`pass_fds`, write-end held by the
  tool, read-end outside the sandbox). That closes the live-socket path by construction and makes marker deletion
  impossible. Residual after the candidate: an absolute `/usr/bin/hyprctl` exec is still invisible to clause r,
  though it can no longer reach a compositor because `/run/user/<uid>` does not exist inside the sandbox — so
  clause r's wording ("no hyprctl run") stays slightly stronger than what it certifies.

### H10 — Medium — the v2 re-registration is in flight, untracked, and its freeze document does not exist
- **Attacks:** the round's counting line; every counter item in the wave.
- **State at audit time** (`checks.txt:194-223`): six untracked artefacts — `quality/counters/c1-r46-devices-v2.py`
  (`19d00e66…`), `quality/counters/c1-r46-fixtures-v2.json` (`d31849db…`), `quality/counters/c2-r46-input-device-entry-v2.py`
  (`eb6db5c9…`), `.ufo/waves/round-46/ctl/run-c1-controls-v2.py`, `…/run-c2-controls-v2.py`, and the
  `.ufo/waves/round-46/v2/` tree (`mado-devices.py`, `entry.md`, `build-pos.py`, `gen-fixtures.py`, `__pycache__`).
  The v2 counter's docstring already asserts "Re-registered BEFORE any round-46 data commit
  (`.ufo/waves/round-46/registration-v2.md`)" (v2 file line 4), and **that file does not exist** (`checks.txt:195`).
  Eleven items still name the v1 counter paths; **no** item names a v2 artefact (`checks.txt:222-223`).
- **Exploit path (provenance, not mutation):** a seat runs the item text as written and scores the superseded v1
  predicate; or a seat picks up the v2 counter because it is newer, produces a receipt with it, and the receipt's
  counting line has no freeze, no controls and no registration behind it — the exact "vacuous, survivor,
  stale-premise" class the lane's own lessons record for rounds 40/41/45. The v2 files are also a write into
  `quality/counters/` and `.ufo/waves/round-46/`, i.e. outside every seat directory; if the author is the L1 (the
  only integrator) the write is legitimate, and if it is a seat the seat has left its scope. My evidence cannot
  distinguish the author.
- **Impact:** if a v2 number is cited before `registration-v2.md` + the v2 control receipts exist, the round has two
  incompatible predicates live at once and the w1 receipts stop being comparable.
- **Smallest remediation:** before any v2 number is quoted, the L1 writes `registration-v2.md` (freeze commit,
  before/after lines, kill rule) and the v2 control receipt, and issues one wave-level notice naming the v2 files
  and their sha256 pins; otherwise the v1 counters stay the only citable ones and the v2 tree should leave
  `quality/counters/` until it is frozen.

---

## 3. What the instructions get right (checked, not assumed)

- **Zero mutating compositor verbs in command position** across 66 items, for all ten verbs the context bans
  (`checks.txt:4-13`, `:46`); `keyword`/`reload` appear only as prose about semantics (items
  `ExecC2Census`, `RevC2Counter`, `ScrEntryDraft`, `CritToolSemantics`, `LabVirtualRules`) — those items ask
  a seat to *read* what a reload would do, and none tells it to reload.
- **Zero package actions named**: `pacman` 0, `systemctl` 0, `journalctl` 0, `udevadm` 1 (only this seat's own
  prompt text), `libinput` 3 (a grep term in `ExecIdGuard`, a "stays open" noun in `ScrReadme`, this seat)
  (`checks.txt:173-179`). The toolchain the items need is already installed (`checks.txt:103-109`), so no seat
  has a pretext to break the pacman pause.
- **The gate instruction is genuinely hermetic**: `--selftest` rc 0, `460/460`, no file created under a
  redirected `HOME` or cwd (`checks.txt:54-57`).
- **Counter sandbox cannot write the host**: `--ro-bind / /`, tmpfs over repo/lane/parent, writable bind only
  of the counter's own marker dir, `--unshare-pid --unshare-net` (`checks.txt:111-119`). It is *read*-permeable and
  its marker check is unsound — that is H9, and it qualifies every "no hyprctl run" argument made from clause r.
- **The live inputs exist**, so no seat needs to create a host config to follow items 1-3: `input.conf`,
  `monitors.conf`, `hyprland.conf`, the omarchy default all present; `input.conf` holds 0 `device` blocks,
  matching the registration (`checks.txt:124-129`).
- **The read verbs the items do name are read-only at the pinned version**: `devicesRequest` opens by building
  its result string (`fetch/Hyprland-HyprCtl.cpp:748`), and the tools the wave runs on live input contain no
  `subprocess`/`socket` use at all (`checks.txt:158-160`).

---

## 4. Residuals (declared)

- I audited the **item texts and the registration**, plus the lane scripts those texts name. I did not audit
  the round prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-46.md` (outside the lane, read-only,
  and not named to this seat) — an instruction that contradicts the context could originate there.
- I did not run any `hyprctl` other than the single whitelisted `monitors all -j` used to measure the serial's
  shape (`checks.txt:132`); no compositor mutation, no package action, no Wayland client of my own, no writes
  outside `.ufo/waves/round-46/w1/SentHost{,.md}` and `/fast/scratch/hyaku/mado-r46/SentHost/`.
- H1 is a policy judgement that belongs to `RevPrivacyRound`; I state the conflict and do not rule on whether
  device product names are session material.
- I verified that the argv path is world-readable on this host and that `git grep -f -` fails closed; I did not
  test whether an audit daemon actually records argv here (no such daemon inspected).
- The untracked v2 counters and the `.ufo/waves/round-46/v2/` tree were read (hashes, guard lines) but not run;
  I therefore report the v2 sandbox as designed, not as measured (H9/H10).
- The three `tools/*.py --selftest` forms that need an argument (`mado-tripwire.py`, `mado-assessment.py`,
  `mado-evidence-audit.py`) were read, not run; they would exit 2 on a bare flag, which is a usage error and
  not a host effect.

## 5. Adjacent observations (outside the host-mutation surface, recorded because I read the items)

- **O1 (number drift):** `registration.md` routes "triage the 48 pre-existing findings"; item
  `ExecSessionTriage` says "the 49 synthetic findings disappear". One of the two counts is stale before data.
- **O2 (unexecutable spelling):** item `ExecDataRehearsal` says "`tools/*.py --selftest` for every tool with a
  selftest"; only `mado-action-plan.py`, `mado-globals.py`, `mado-options.py`, `mado-monitors.py` and
  `mado-geometry.py` accept a bare flag; `mado-tripwire.py`, `mado-assessment.py` and `mado-evidence-audit.py`
  take a directory argument (`--selftest DIR|ROOT|FIXTURES`), and `mado-anims.py`, `mado-binds.py`,
  `mado-wsrules.py`, `mado-eventq.py` have none. The item's phrasing will produce three usage errors.
- **O3 (relative paths):** `ExecHarmBase` gives `quality/…` and `tools/…` relative to the lane, while the seat
  cwd is the fleet root; this is the trigger half of H3.
