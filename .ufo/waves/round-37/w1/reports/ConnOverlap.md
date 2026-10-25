# ConnOverlap — connector seat, mado round 37 wave 1

Seat: `L1Mado37-2.ConnOverlap` (connector). Lane HEAD at read: `80b83c856b8c` (= `master`; one commit after the
v2 freeze `893a8aa`, the wave-1 spec/prompts). Read-only throughout; scratch `/dev/shm/mado37-ConnOverlap/`
(the full `ss -xpa` capture was deleted after counting; only counts appear below). No tool installed or updated.

## TL;DR

- **No sibling lane claims the Hyprland event socket, compositor logging or Waybar internals.** The
  ground is uncontested. Two lanes route desktop or compositor work *to* mado: tsukuroi
  `PROVINCE.md:48` (ADJ-03) and game-dev-3d `PROVINCE.md:75`.
- **The C2 tool's read set does cross five sibling grounds.** Each crossing is shared evidence, not
  shared ownership:
  - the compositor *unit journal* is tsukuroi's;
  - journal reading as kill evidence is mori's;
  - `ss -p` walks every readable `/proc/<pid>/fd`, which is souji's own-uid fd listing and is excluded by mori's privacy rule;
  - the agent and keyring socket paths in a raw `ss -xpa` table are kagi's exposure ground;
  - the `ss -p` owner-attribution caveat is kama's method.
- **PROVINCE has no line for this theme.** `git log -S socket2 -- PROVINCE.md` → 0 commits. The
  round-23 inventory claim "covers every tracked file under `tools/`" is **already false**:
  `tools/mado-wsrules.py`, tracked since round 27, has no row. `mado-eventq.py` would be the second
  file missing from the inventory.
- **Proposed move:** commit the live `ss` snapshot scoped to the socket2 rows, as byte-identical raw
  lines, and record the full capture's sha256 and row count in the live receipt. The frozen C2 `live`
  clause still passes. I tested this on ExecEventqA's draft: the replay gives identical client lines.
  It keeps 1,092 unrelated rows, including 18 agent/keyring path rows, out of lane git.

## 1. Sibling scan — commands and hits

```
cd /home/vgpnk/Projects/shokunin
grep -il -E 'hyprland|event socket|socket2|\.socket2|hyprctl|waybar|unix socket|unix-socket|\bss\b -x|ss -x|compositor log|hyprland\.log|debug:disable_logs|rollinglog|ipc' */PROVINCE.md */SKILL.md */corpus/README.md
```
Hits outside mado: `tsukuroi-shokunin/PROVINCE.md`, `kaidoku-shokunin/SKILL.md`, `kumitate-shokunin/SKILL.md`,
`kaidoku-shokunin/corpus/README.md`, `kotodama-shokunin/corpus/README.md`, `kumitate-shokunin/corpus/README.md`.
I then widened the sweep over every `*/PROVINCE.md` (`socket|journal|\bss\b|/proc|session log|user unit|waybar|hypr|compositor|desktop|wayland|event`)
and over every `*/SKILL.md` and `*/corpus/README.md` (`socket|hyprland|waybar|compositor|session log|hyprctl|journalctl --user|user unit|/proc/*/fd|ss -x|unix`).

| Lane | Line (quoted) | Contested? | What mado routes rather than absorbs |
|---|---|---|---|
| tsukuroi | `PROVINCE.md:10-11` "systemd user units & timers (`systemctl --user`, unit files, failed states), journal/boot triage (`journalctl -b`, dmesg error classes)"; `:41-42` "Shared evidence is not shared ownership"; `:48` ADJ-03 "Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis … mado"; `:124` OUT-004 names mado's plane | **Adjacent; shared evidence.** The C2 live default `journalctl --user -u wayland-wm@hyprland.desktop.service` (registration §C2; draft `mado-eventq.py:66-67`) reads a unit journal inside tsukuroi's journal and unit plane | Any reading of that unit as **health**: failed or restarted states, journal error classes, boot triage → tsukuroi. Mado counts two marker strings only. Mado's own `PROVINCE.md:32` already concedes "its unit-state rows sit next to tsukuroi's unit-health ground, which stays tsukuroi's". The unit exists and runs: `systemctl --user show …` → `ActiveState=active` `SubState=running` |
| mori | `PROVINCE.md:8-9` journal kill/OOM records; `:13-14` "mori reads journal and cgroup events as fleet evidence"; `SKILL.md:414-416` "Also excluded: … `cat /proc/<pid>/fd/*` (`omp` holds 51 readable fds onto session JSONL), and any journal output mode that keeps `MESSAGE`" | **Adjacent; method divergence, not scope.** The draft reads the journal with `-o cat` (MESSAGE text, held in memory; `mado-eventq.py:79` "No journal or log line is printed; only counts and fds"), and `ss -p` walks `/proc/<pid>/fd` (§3) | If a subscriber vanishes (waybar or socat gone) and the question becomes "was it killed or OOM'd?" → mori. Mado must not attribute a missing client to a kill |
| souji | `PROVINCE.md:136-143` "the own-uid cwd/argv/fd listing produced by `tools/souji-proc-census.sh` … is Core … Reaping stays outside the lane"; `:153-155` other uids → mori, credentials → kagi | **Adjacent; same observation primitive.** `ss -xpa` attributes owners by scanning own-uid fd tables (§3) | A lingering or orphaned subscriber process (for example, a stale `socat` listener) is **process residue** → souji (list-only; reaping is operator-only). Mado reports the subscriber, not its disposal |
| kagi | `SKILL.md:81-83` "`SSH_AUTH_SOCK` (live agent, 3 keys), `XDG_RUNTIME_DIR` (GPG agent sockets), `DISPLAY`/DBus … Blast radius = caller's whole user session" | **Adjacent; exposure surface.** A raw `ss -xpa` table on this host carries 18 local-path rows of agent and keyring classes (§3) | Exposure assessment of any committed socket table → kagi. Mado commits only socket2 rows (§4) |
| kama | `PROVINCE.md:10` "`tools/kama-probe.sh listeners` (`ss -ltn` loopback enumeration + per-listener classification)"; `corpus/README.md:261` "procfs socket-inode/child-fd ownership join"; `SKILL.md:79-82` "unprivileged `ss -ltnp` prints **no owner** … A missing owner is not 'no process'" | **Not contested.** kama covers TCP serving ports (AF_INET/INET6); mado's ground is the compositor's AF_UNIX socket. The shared method is `ss -p` owner attribution | Cite kama's caveat; don't re-derive it. A socket2 peer row without a `users:(…)` field (another uid, or a race) is "owner unknown", not "no subscriber". The fixtures don't cover that case (`c2-r37-eventq.py:51-59`: every row carries `users:`) |
| tameshi | `PROVINCE.md:7-18` owns the reusable mutation and fixture method; `:32-33` names mado `tools/mado-verify.sh` as a measured surface | **Not contested.** | MutC2Clauses and MutC1Clauses consume the method. Any general claim about the method → tameshi |
| kaidoku | `corpus/README.md:23,112,124,130,131,139,158`: Electron `ipcMain`/IPC channels in shipped ASARs | **No.** Its "IPC" means Electron app internals, not compositor IPC | — |
| kumitate | `SKILL.md:386` "`ufo-ground-handler.mjs` serves a one-line-JSON unix socket"; `:616` "(requested **mount** binds — not the Hyprland `mado-binds.py` keybind file)" | **No.** That socket is kumitate's own tooling, and it already disambiguates itself from mado | — |
| game-dev-3d | `PROVINCE.md:75` "Desktop/compositor display behavior belongs to `mado-shokunin`" | **No** (routes to mado) | — |
| kotoba | `PROVINCE.md:63` mado row "none" | **No** | — |

Verdict: **PASS.** No sibling contests the event-socket ground. Five adjacencies need route lines (§5).

## 2. Mado PROVINCE — where this theme sits

Current lines (`PROVINCE.md`):
```
3: **Domain:** desktop & compositor craft — the Hyprland/waybar/walker
4: configuration plane and display behavior on this host.
6: **Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,
7: animations), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator
8: configs (`~/.config/alacritty|foot|kitty|ghostty/`), themes/wallpapers as
9: declared files, screen/idle behavior (hypridle/hyprlock where present).
14: **Refuses:** secrets in configs (shape-only, → kagi), model endpoints
15: (→ kama), model quality (→ kengaku). Never mutates a running compositor
16: state; every claim is file-byte- or screenshot-verified.
```
`:32` (round-23 wave-2 correction): "the inventory above covers every tracked file under `tools/`".

Finding: **the theme sits only under the Domain phrase "compositor craft" (`:3`).** No owned surface (`:6-9`)
names compositor runtime IPC. Every owned surface is a config tree, and Waybar is owned as `~/.config/waybar/`,
not as an event-socket client. The lane has already worked this ground for three rounds without a PROVINCE line:
`corpus/README.md:55` (`ipc-contract-r25.md`, round 32: "the event socket `.socket2.sock` with the `EVENT>>DATA`
framing …") and `:58` (`waybar-module-text-route-r25.md`, round 34, "Waybar event-socket client"). This is the
same shape as the round-36 D9 case at `PROVINCE.md:66-69`: practised, but stated nowhere.
```
git log --oneline -S <t> -- PROVINCE.md | wc -l
socket2: 0   event socket: 0   journalctl: 0   ss -x: 0   wsrules: 0   socket: 3 (the "no socket" tool-row phrases)
```
Line `:16` ("every claim is file-byte- or screenshot-verified") was already qualified at `:32` for live
read-only probes. The C2 tool adds two live read verbs that are new to PROVINCE: `ss -xpa` and `journalctl --user -u …`.

Inventory claim `:32` is false today:
```
git ls-files tools/   → … tools/mado-verify.sh  tools/mado-wsrules.py   (8 files)
grep -c wsrules PROVINCE.md SKILL.md → 0, 0
git log -- tools/mado-wsrules.py → 48b9434 / 20022a6 (2026-10-23, round-27 C1 data)
```
Table rows `:24-30` list 7 tools; `mado-wsrules.py` is missing. Landing `tools/mado-eventq.py` without a row would
make two missing files, and `tools/mado-assessment.py:24` gates "No cross-domain bleed (PROVINCE.md still accurate)".

Verdict: **finding — PROVINCE needs an append-only line naming the delivery half of the event socket** as an
observed, never-connected runtime surface, plus an inventory row for `mado-eventq.py` (and, separately, the missing
round-27 row for `mado-wsrules.py`). Proposed text is in §5. Writing it is the scribe's or integrator's call.

## 3. Host measurements (counts only; no paths or titles pasted)

```
$ ss -V                       → ss utility, iproute2-7.2.0
$ ss -xpa > ss-full.txt; rc=0; sha256 d39aefb5b5d0960f…
rows=1097  with_users=806  path_rows=301  abstract_rows=135  distinct_comms=61
sensitive_local_path_rows=18   (classes: gnupg 12, ssh 2, 1password 2, keyring 2)
socket2_listen=1  socket2_estab=2   peers: 1 "socat", 1 "waybar"
```
Subscriber lineage (`ps -o pid=,ppid=,etimes=,comm=`):
```
935660 1493 25749 waybar     ← 1493 systemd ← 1 systemd
2293 1689 126078 socat       ← 1689 omarchy-hyprlan ← 1619 Hyprland
```
Finding: the `socat` subscriber is omarchy's own event listener. It is a child of an `omarchy-hyprlan…` process
spawned by Hyprland, up about 35 h. It is not a wave seat. The C2 fixture pids (`c2-r37-eventq.py:52-55`:
waybar 935660 fd 21, socat 2293 fd 5) are this host's live values.

`ss -p` procfs footprint:
```
$ strace -f -e trace=socket ss -xpa        → 1 socket(AF_NETLINK, SOCK_RAW|SOCK_CLOEXEC, NETLINK_SOCK_DIAG
$ strace -f -e trace=openat,open,getdents64 ss -xpa  → 1760 "/proc/N/fd/", 167 "/proc/N/stat", 1 "/proc/"
$ strace -f -c -e trace=readlinkat,readlink ss -xpa → 4785 readlink calls (123 errors)
```
Findings:
- **(a)** C2's `readonly` clause (`c2-r37-eventq.py:181-183`) checks only that the tool's own source has no
  `import socket` or `connect(`. The `ss` child does open a socket: an `AF_NETLINK` sock_diag socket to the kernel,
  never a Hyprland socket. The draft's docstring "never opens any socket" (`mado-eventq.py:76`) is true of the
  Python process only. A PROVINCE row should say "connects to no Hyprland socket; `ss` queries the kernel over
  NETLINK_SOCK_DIAG".
- **(b)** Every live run walks every readable `/proc/<pid>/fd` on the host. That is souji's fd-listing primitive
  and the read mori's `SKILL.md:415` excludes. The tool's output is still socket2-scoped (§4).

## 4. Proposed move (one, bounded)

**Evidence.**
- The registration (Amendment 1) and the counter docstring (`c2-r37-eventq.py:17`) say "the committed **raw**
  snapshot `.ufo/waves/round-37/receipts/eventq-live-ss.txt`".
- The `live` clause (`:153-177`) checks only that replaying the snapshot yields the same (comm, pid, fd) multiset
  as the receipt. It never checks completeness.
- ExecEventqA's draft (`w1/scratch/ExecEventqA/mado-eventq.py`, sha256 `29b730668fc5ca43…`, copied to my scratch,
  run on my capture with `--log empty --journal-file empty --disable-logs 1`) already scopes the snapshot.
  Its `:71-73` reads: "`--snapshot-out` writes the ss header plus exactly the rows used (socket2 LISTEN row, its
  ESTAB rows, their peer rows)". Results:
  ```
  full table  → rc=0  MADO_EVENTQ_CLIENT: comm=waybar pid=935660 fd=21 … / comm=socat pid=2293 fd=5 … subscribers=2 verdict=CLEAN
  draft --snapshot-out → draft_snapshot_rows=5 not_in_full=0 listen_rows=1
  replay of that 5-row file → REPLAY_OF_DRAFT_SNAPSHOT_IDENTICAL
  my own inode-join subset (header + socket2 rows + peer rows) → scoped_rows=5, 0 lines not in full,
       scoped_sensitive=0, client lines identical (CLIENT_LINES_IDENTICAL)
  ```
- What the draft does **not** do: it records nothing about the rows it dropped. So "raw" (frozen wording) versus
  "a 5-row subset" can't be audited from the commit. No ExecEventqB draft was present in scratch, so whether the
  B build scopes the snapshot at all is unobserved.

**Move: a synthesis of the frozen "raw" wording and ExecEventqA's scoping.**
1. The committed `eventq-live-ss.txt` holds the `ss` header plus the socket2 LISTEN row, its ESTAB rows and their
   peer rows. Each row stays **byte-identical** to the captured line.
2. The live receipt `eventq-live.txt` gets one extra line from the same single capture, for example
   `ss_capture: sha256=<full> rows=<N> kept=<k>`. "Raw" then means "unaltered rows, k of N kept" and stays auditable.
3. The receipt and the snapshot both come from **one** `ss -xpa` read. The draft does this already: `used` rows
   feed both. This rules out a race where a transient subscriber appears in one and not the other.

**Affected axes.**
- Operability (C2): no harm. The frozen `live` clause is satisfied unchanged, as shown above, and `fixtures` and
  `readonly` are untouched. The gain is auditability of the frozen word "raw".
- Coverage (C1): untouched, because C1 reads no C2 file (registration § Separability).

**Second-order effects.**
- The scoping keeps 1,092 unrelated rows out of lane git: 61 process names, 301 filesystem socket paths, and 18
  agent/keyring paths (kagi's `SKILL.md:81-83` ground).
- Lane history is append-only, so a full table committed once cannot be withdrawn.

**Risks.**
- A reviewer reading "raw" literally may call a subset non-conforming. The digest line answers that by stating the
  reduction instead of hiding it.
- The full-capture digest is an attestation, not re-verifiable, because the capture is not committed. Label it as
  such.
- If B's build writes the whole table, integration must pick A's scoping or apply the same filter before commit.

**Verification.**
```
python3 -I quality/counters/c2-r37-eventq.py --repo . --rev <tip>      # expect live=1
git show <tip>:.ufo/waves/round-37/receipts/eventq-live-ss.txt | awk 'NR>1' | wc -l   # expect small k (5 today)
git show <tip>:.ufo/waves/round-37/receipts/eventq-live-ss.txt | grep -c -i -E 'gnupg|ssh|1password|keyring|S\.gpg'   # expect 0
grep -c '^ss_capture: sha256=' <(git show <tip>:.ufo/waves/round-37/receipts/eventq-live.txt)   # expect 1
```

## 5. Proposed PROVINCE append (text for the scribe; not written by this seat)

> **Round-37 refinement (append-only; event-socket delivery; no new write surface):** the compositor's event
> socket `$XDG_RUNTIME_DIR/hypr/<instance>/.socket2.sock` is an **observed runtime surface** under the Domain
> line's "compositor craft" (`:3`). Mado observes its delivery half: who is subscribed, each subscriber's unread
> backlog, and the overflow and write-failure markers, plus whether those markers can be logged at all
> (`debug:disable_logs`). It never connects to the socket. `tools/mado-eventq.py` reads the kernel unix-socket
> table through `ss -xpa`. That `ss` child opens a NETLINK_SOCK_DIAG socket, not a Hyprland socket, and walks the
> readable `/proc/<pid>/fd` tables to attribute owners. The tool also reads the session log, the
> `wayland-wm@hyprland.desktop.service` user journal and `hyprctl getoption debug:disable_logs -j`. It prints
> counts and fds only, and its `--snapshot-out` writes only the socket2 rows. OUT (report, never absorb):
> - unit health and journal triage of that unit → tsukuroi (`../tsukuroi-shokunin/PROVINCE.md:10-11`);
> - kill or OOM attribution of a vanished subscriber → mori (`../mori-shokunin/PROVINCE.md:8-9`);
> - a lingering subscriber process as residue → souji (`../souji-shokunin/PROVINCE.md:136-143`);
> - exposure of socket paths in any captured table → kagi;
> - `ss -p` owner attribution follows kama's caveat that a missing owner is not "no process"
>   (`../kama-shokunin/SKILL.md:79-82`).
>
> Inventory row `tools/mado-eventq.py` to be added to the round-23 table. The round-27 `tools/mado-wsrules.py`
> also has no row; `:32`'s "every tracked file" claim is restored only when both land.

## 6. Verdicts

| Item | Verdict | Pointer |
|---|---|---|
| Sibling claims on Hyprland IPC/event sockets, compositor logging, Waybar internals | PASS: none contested | §1 table |
| `ss` / unix-socket diagnostics overlap | finding: kama's method (TCP), souji's fd-walk primitive, kagi's exposure surface; route, don't absorb | §1, §3 |
| Journal channel overlap | finding: tsukuroi owns the unit journal plane; mori owns kill evidence; mado counts two markers | §1 |
| Which PROVINCE surface hosts the theme | finding: Domain `:3` only; no owned-surface line | §2 |
| Does PROVINCE need an event-socket delivery line | yes; text proposed | §5 |
| PROVINCE `:32` inventory completeness | FAIL today (`mado-wsrules.py` unlisted since round 27) | §2 |
| Socat subscriber provenance | finding: omarchy listener (Hyprland → omarchy-hyprlan… → socat), not a seat | §3 |
| C2 `readonly` clause vs the `ss` child | finding: the source check holds; the child opens AF_NETLINK sock_diag; no Hyprland socket is touched | §3 |
| Proposed move (scoped raw snapshot + capture digest) | tested on the A draft: replay identical, 0 sensitive rows | §4 |

Tools installed or updated: none. No socket was connected; `ss`, `strace` on `ss`, `ps`, `systemctl --user show`
and read-only `git ls-files` / `git log` / `git rev-parse` were the only live reads.
