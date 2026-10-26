# SentLiveReads — safety review: the round's host reads and the C1 reference

Round 44 (hyaku run 9, 2026-10-26), wave `w1`, seat `SentLiveReads`. Leaf; no dispatch.
Base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, freeze `e2289516a9a857f55cda7be635933e89b931c3da`.
Everything below is measured on this host or read out of a pinned source; evidence files live in
`evidence/` beside this file and every quote is checked by `verify-quotes.py` (run it: it prints
`QUOTES: 12/12 verified`).

Scope asked of me: (1) the host commands the wave context allows and the ones the live-host and
oracle-free seats run — read-only? any socket write beyond request-socket reads? (2) the C1 reference
against attacker-chosen class/title strings — output injection, ReDoS, and whether the `timeout 5`
guard is still documented; (3) whether the C2 entry's planned claims could lead a reader to mutate
the desktop. Ranked by severity with repro.

I ran no mutating verb, opened no compositor socket of my own, made no Wayland connection, ran no
package transaction, and did not execute the one probe that would have been the hazard (a newline
inside a `getoption` name — see S3). Tool state: no installs; `python3` 3.14.8 and `/usr/bin/strace`
were already present.

---

## S1 — HIGH — verbatim session material (window titles, PIDs) is being written into the lane repo

**What attacks.** `SKILL.md:332` — the lane's own fence: "`clients` for length/tags, never window
titles". The live-host seat broke it, and the files are inside the repo the L1 commits at the data
commit, so the leak becomes git history.

**Evidence.**
- `.ufo/waves/round-44/w1/ExecLiveHost/live-clients.json` — the verbatim `hyprctl clients -j` dump,
  3 clients, each carrying `title`, `initialTitle`, `pid`, `address`; e.g. the Alacritty client's
  `"title"` whose value is 48 characters of the operator's in-flight work title (value withheld here —
  this file must not repeat the leak it reports; length and sha256 are in `evidence/leak.txt` §A).
- `.ufo/waves/round-44/w1/ExecLiveHost/live-states.txt` — 336 lines, embeds that dump whole; 3
  `"title"` occurrences.
- `.ufo/waves/round-44/w1/ExecLiveHost/fs2.json`, `max1.json` — 31-key objects (the hand-made state
  dumps are copies of the Alacritty client), so they carry the same `title`/`initialTitle`/`pid`.
- The round-43 *pinned* receipt shows the intended shape: `.ufo/waves/round-43/fetch/host-clients-r43.json`
  has exactly `address, at, class, floating, mapped, monitor, size` and no title, no pid.
- The leak is already in the base: `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json` is
  git-tracked and holds 4 titles (`evidence/leak.txt` §B). Round 44 repeats it in three more files.
- `hyprctl clients -j` prints those fields by design — pinned `Hyprland-HyprCtl.cpp:403` (`"title": "{}"`)
  and `:430` (`escapeJSONStrings(w->m_title)`, `w->getPID()`).

**Repro.**
```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -c "import json;print([sorted(c) for c in json.load(open('.ufo/waves/round-44/w1/ExecLiveHost/live-clients.json'))])"
grep -c '"title"' .ufo/waves/round-44/w1/ExecLiveHost/live-states.txt
git ls-files .ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json
```

**Impact.** No attacker is needed: the operator's in-flight work titles, host PIDs and window
addresses enter a published repo, and a later scrub cannot remove them from history. It also
propagates — `build-live-states.py` regenerates the receipt from those files, so every rerun re-leaks.

**Smallest remediation.** Project the dump to the round-43 7-key schema before writing (the tool never
reads `title`, `pid`, `initialTitle` or any of the other 24 keys, so nothing is lost), keep only the
full dump's sha256, regenerate `live-states.txt` from the projection, and have the L1 scrub the
round-43 tracked seat file (or record it as an accepted closure item). This is a w1 fix: nothing is
committed yet.

**Status 14:12 — both w1 copies verified fixed.** ExecLiveHost applied the fix and I re-checked it:
`live-clients.json`/`live-monitors.json`/`live-workspaces.json` now carry 10 / 13 / 8 keys and no
`title`, `initialTitle`, `pid`, `serial`, `make`, `model`, `description`, `modes` or `lastwindowtitle`;
`live-states.txt` has 0 `"title"` occurrences; `raw-dumps.sha256` keeps the raw hashes only
(clients `931ed70a…`, 2619 raw bytes); `projection-invariance.txt` shows raw and projected give
byte-identical stdout under both tools. The `lastwindowtitle` drop matters beyond clients — a
workspace record carries a window title too, so the leak class was wider than `clients`.

A **second live dump appeared after my first sweep**:
`.ufo/waves/round-44/w1/ExecIndepB/receipt-live-clients.json` — 3 clients, 32 keys, every client with
`title`/`initialTitle`/`pid`, 2619 bytes, cited at `w1/ExecIndepB.md:20`, a *different* capture from
ExecLiveHost's. Reported to its owner, and **also fixed and verified**: now 10 keys
(`address, at, class, floating, fullscreen, fullscreenClient, fullscreenHandler, mapped, monitor, size`),
1108 bytes, raw sha256 `5ead9176…` kept in `receipt-live-raw.sha256`, and
`receipt-live-projection-invariance.txt` shows `SENSITIVE_KEYS_PRESENT: 0` with its two live receipts
(`nomatch_rc=3`, `synth_rc=0`) reproducing identically under the projection.

The two captures corroborate each other: their raw dumps differ (`931ed70a…` vs `5ead9176…` — only in
dropped fields, the title nonce), yet both project to the **same bytes**
(`sha256 983c3a1736c2a09ff84f11c79a911582d1ad87405560ec7983d16a14311cd8ed`), so the kept fields are
exactly the fields the claim reads and the two seats observed the same three clients.

What remains is the **round-43 tracked file** `.ufo/waves/round-43/w1/ExecLiveHost/host-clients-live.json`
(4 titles) — the L1's call, since no seat may edit a frozen earlier round. A sweep of every `*.json`
under `round-44/w1` for `pid` + a string `title` now returns nothing.

---

## S2 — MEDIUM — the ReDoS is real, the `timeout 5` guard is still documented, but the documented trigger class is incomplete

**What attacks.** `tools/mado-geometry.py` and the C1 reference match a client-chosen class against a
config regex with Python `re.fullmatch` (`SKILL.md:296`: "the match is Python `re.fullmatch`, which
backtracks"). `SKILL.md:297` describes the trigger as "an alternation under a repeat, such as `(a|aa)+$`".
That is one trigger, not the class: the SAFE alphabet and `regex_ok` also accept nested quantifiers,
which backtrack far worse.

**Evidence** (`evidence/redos.txt`, reference sha256 `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d`):

| regex | accepted by `regex_ok` | class | wall time |
|---|---|---|---|
| `(a\|aa)+$` | yes | `"a"*38+"b"` | 6.88 s |
| `(a+)+$` | yes | `"a"*30+"b"` | **43.92 s** |
| `^(a\|aa)+$` | yes | `"a"*30+"b"` | 0.18 s |
| `(a\|aa)+$` | yes | `"a"*1024+"b"` under `timeout 5` | rc 124, 5.00 s, **0 bytes stdout** |

So a rule regex with no alternation at all (`(a+)+$`) hangs worse than the documented example, and the
sentence "an alternation under a repeat" would let a reader conclude that a non-alternation regex is
safe.

**The mitigation is still documented and is sound.** `SKILL.md:300` still says to run the join as
`hyprctl clients -j | timeout 5 python3 tools/mado-geometry.py …` and "treat exit 124 as" no verdict.
I verified the second half matters: the tool writes its output once at the end, so a timeout yields
**0 bytes of stdout** — there is no partial `MADO_GEOM_CLIENT:`/`MADO_GEOMETRY:` line to mistake for a
verdict. Keying on the exit code (and not on line counts) is the correct reading.

**Exposure today.** No incident: the live `~/.config/hypr/gkeep.conf` regex is `^(org.omarchy.gkeep)$`
and the live classes are short. The realistic path is a seat or a future contributor writing a
nested-quantifier `match:class` into a rule file and then joining a client whose class is long — the
class is chosen by the client, so any Wayland app can supply it. Availability only; nothing mutates.

**Also exposed (fixed 14:07):** the live-host harness shelled the tool with no timeout at all
(`build-live-states.py` `def run(argv):` … `subprocess.run(argv, …)`, previously line 28). It now runs
`timeout=TIMEOUT` with `TIMEOUT = 30` (`build-live-states.py:22,35-39`) and records a timeout as rc 124
with a TIMEOUT marker, never as a verdict — so the harness pattern a future seat copies is bounded.

**Smallest remediation.** In the same SKILL edit that adds the state verdicts, replace "an alternation
under a repeat" with "ambiguous repetition — an alternation under a repeat, or a quantified group under
a repeat, e.g. `(a+)+$`" and keep the `timeout 5` rule unconditional (it is the only bound). Add
`timeout=` to the seat harness. Note the scorer is already bounded: the inherited counter runs the
tool under bubblewrap with 30 s per fixture and stops after 3 timeouts
(`quality/counters/c1-r42-geometry.py:440-451`), so scoring a hostile tool cannot stall the counter.

---

## S3 — MEDIUM — the wave's mutation fence is a denylist, and the pinned compositor exposes non-read verbs it does not name

**What attacks.** `.ufo/waves/round-44/w1-spec.json:78` fences by enumeration: "NEVER `dispatch`,
`keyword`, `reload`, `setprop`, `--batch`, `output`, `plugin`, `kill`". The compositor's IPC table is
larger, and two of the unnamed verbs execute code inside the compositor.

**Evidence** (pinned `Hyprland-HyprCtl.cpp`, round-43 fetch):
- `:2042` `registerCommand(SHyprCtlCommand{"eval", …})` — `evalRequest` (`:1110-1119`) runs Lua via
  `luaMgr->eval(code, …)`; `:2043` `repl`; `:2028` `reload`; `:2036` `dispatch`; `:2037` `keyword`;
  `:2029` `plugin`; `:2008` `kill`; `:2035` `output`; `:2041` `[[BATCH]]`. Also `seterror`,
  `switchxkblayout`, `reloadshaders`, `notify`, `dismissnotify` (`:2026-2034`).
- The verb is chosen by the **first word**: exact names first, then prefix match at `:2117`
  `if (request.starts_with(cmd->name))`. So whatever occupies the first token decides the verb.
- The only multi-command path is the 9-character prefix: `dispatchBatch` is reached only when the
  request starts with `[[BATCH]]` (`:2069`), and it splits on `;` (`:1312` `request.substr(9)`).

**Why this is not an incident.** No seat ran any mutating verb: a grep over the whole wave directory
for `hyprctl (dispatch|keyword|reload|setprop|output|plugin|kill|--batch|--instance)`, `pkill`,
`kill -`, `systemctl start|stop|restart`, `gdbus`, `dbus-send`, `wl-copy`, `grim`, `.socket.sock`,
`WAYLAND_DISPLAY` and `wl_display_connect` returns only policy text, zero invocations
(`evidence/host-reads.txt` §C). The live-host seat ran `hyprctl version`, `clients -j`, `monitors -j`,
`workspaces -j` (and read `~/.config/hypr/gkeep.conf`, `/proc/sys/kernel/osrelease`) — all allowed.

**Answer to "any socket write beyond request-socket reads?"** Every allowed verb is exactly one
connection and one request-string write; there is no verb-less read. Measured
(`evidence/strace.txt` §B; instance signature redacted to `<SIG>` per `SKILL.md:332`'s shape-only rule):

```
hyprctl version                write(3, "/version", 8)
hyprctl clients -j             write(3, "j/clients", 9)
hyprctl monitors -j            write(3, "j/monitors", 10)
hyprctl workspaces -j          write(3, "j/workspaces", 12)
hyprctl getoption general:gaps_out -j   write(3, "j/getoption general:gaps_out", 28)
```

`-j` is not a flag on the wire; it is the `j/` prefix of the same request. `getoption` is read-only —
`dispatchGetOption` (`:1647-1667`) only calls `Config::mgr()->getConfigValue(curitem)` and formats —
and the option name is appended *after* the verb, so a crafted `<name>` cannot become a command (it
would have to occupy the first token). **I did not run the crafted-name probe** (a newline or a verb
prefix inside `<name>`): that probe is the hazard itself, and the pinned grammar settles it without a
run.

**Smallest remediation.** State the fence as `SKILL.md:315`'s allowlist (the 12 read verbs) instead of
a denylist, and add `--instance` to the forbidden set. A future seat that adds a verb then has to
justify it against the allowlist rather than slip past an enumeration that omits `eval`.

The lane already owns the better list: `tools/mado-tripwire.py:255-258` `HYPRCTL_MUTATE` names
`dispatch, keyword, reload, kill, setcursor, switchxkblayout, seterror, notify, dismissnotify, plugin,
output, setprop, hyprpaper, hyprsunset, eval`, and `:259` `HYPRCTL_ARG_OPTS = {"-i", "--instance"}`;
`--batch` is handled at `:1246`. So the fence can cite that set instead of re-enumerating — and it
needs only two additions to be complete against the pinned table: `reloadshaders` (`:2026`) and `repl`
(`:2043`), plus a rule that a request beginning `[[BATCH]]` is mutating by construction.

---

## S4 — MEDIUM — PRED-C2-r44 does not police mutation advice in the entry

**What attacks.** The C2 entry is a reader-facing document, and its `recheck:` line is the place a
reader is told what to run. The predicate constrains the shape of that line, not its content.

**Evidence.** `quality/counters/c2-r44-gkeep-size-request.py:75-76` requires "exactly one `recheck:`"
and that it be an ISO date, `NNd` or `on-*` — nothing about the text after it. A grep of the counter
for `dispatch|keyword|setprop|reload|mutat` finds no clause that forbids them. So this entry would be
admitted:

```
recheck: 30d — run `hyprctl dispatch resizewindowpixel exact 420 500,class:^(org.omarchy.gkeep)$`
and read the client's `size` in `hyprctl clients -j`
```

and a reader following it resizes the operator's live window. That is the exact failure the corpus
convention already guards against in prose: `corpus/knowledge/theme-route-r18.md:3` ends its recheck
with "no omarchy-*, omarchy theme, swaybg, pkill, pgrep, hyprctl, pacman, systemctl or live probe";
`corpus/knowledge/idle-lock-route-r17.md:3` likewise names every excluded tool.

**The predecessor text is clean**, so the risk is what the w1 scribes add, not what they inherit: the
staged `gkeep-client-size-request-r12.md` rechecks with `hyprctl clients -j` only (line 13) and keeps
the observation `UNK` (line 66: "observation remains a single `hyprctl clients -j` reading").

**Smallest remediation.** Add to the counter (or, if the counter is treated as frozen, to the w2 review
checklist) a clause that no unfenced entry line carries a mutating verb — `hyprctl
dispatch|keyword|reload|setprop|output|plugin|eval|repl|--batch`, `omarchy
restart|refresh|toggle|theme`, `pkill|kill`, `systemctl start|stop|restart` — and require the recheck
line to name the reads it uses. The predecessor's own wording already satisfies that.

---

## S5 — LOW — a client-chosen class can spoof a *naive* `verdict=` grep, though not the scorer

**What attacks.** `MADO_GEOM_CLIENT:` carries the class as a JSON string, so a class of
`x verdict=OK` prints `class="x verdict=OK" … verdict=AGREE`. A consumer that greps the line for the
first `verdict=[A-Z]+` reads `OK`; the true verdict is the trailing field.

**Evidence** (`evidence/injection.txt`): `quote`, `equals`, `space`, `utf8` all match and print; the
line is `MADO_GEOM_CLIENT: addr="0x1" class="x verdict=OK" floating=true size=420x500 want=420x500
float_rule=- verdict=AGREE`. The scorer is **not** foolable: `judge()` compares stdout
byte-for-byte (`quality/counters/c1-r42-geometry.py:453`, `if got != want_out:`).

**Impact.** A human or an ad-hoc script reading a pasted line can be misled about one client's verdict.
Nothing else consumes the client line.

**Smallest remediation.** One sentence in the SKILL section that documents the client line: the verdict
is the last field; parse the JSON-quoted `class=` field or anchor on ` verdict=` at end of line.

---

## S6 — INFO (positive, verified) — the C1 reference is injection-free and host-free

**Output injection: blocked.** `evidence/injection.txt`, reference sha256 `8e871a00…`, rule
`match:class .*`, ten attacker-chosen classes: a quote is escaped (`class="x\" verdict=OK"`), `=` and
spaces stay inside the quoted field, and every control character is either rejected before printing
(LF, CR, NUL, ESC — the `matches()` gate `any(ord(ch) < 0x20 …)` drops the client entirely, so no
`MADO_GEOM_CLIENT` line is emitted at all) or escaped by `json.dumps` (`\u009b`, `\u007f`, `\u00fc`).
The `MADO_GEOM_RULE: … class=<REGEX>` field cannot be injected either: SAFE excludes whitespace, `=`
and newlines, so a rule regex cannot introduce a field or a line. Titles are never printed by the tool
at all, so the title vector does not exist in C1.

**Host-free: verified at syscall level.** `evidence/strace.txt` §A, `strace -f -qq -e
trace=socket,connect,bind,sendto,write,execve,openat,…`: 0 socket/connect/bind/sendto calls, 1 execve
(the interpreter itself), 0 opens with `O_WRONLY|O_RDWR|O_CREAT`, 71 read-only `openat`s, 0 bytes
stderr. The docstring's "it starts no process and opens no socket" holds for the reference.

**Scoring an arbitrary tool file is contained.** The inherited counter runs the tool under
`bwrap --unshare-all --cap-drop ALL --clearenv --tmpfs /tmp` with `RLIMIT_NPROC = 1`
(`quality/counters/c1-r42-geometry.py:153-169`), 30 s per fixture, 3-timeout stop. `--tool <file>` is
therefore not a host hole; the trust boundary is the seat, not the counter.

---

## Ranked summary

| id | severity | one line | fix owner |
|---|---|---|---|
| S1 | HIGH | window titles/PIDs from the live dump land in repo files; already true at base — both w1 copies (`ExecLiveHost`, `ExecIndepB`) **fixed and verified**; the round-43 tracked file remains | L1 scrub of the round-43 seat file |
| S2 | MEDIUM | ReDoS accepted by SAFE; `timeout 5` documented and sound, but SKILL names only the alternation trigger; seat harness has no timeout | ScrSkillProvince (SKILL text), ExecLiveHost (harness) |
| S3 | MEDIUM | fence is a denylist; `eval`/`repl` (Lua in the compositor) unnamed; `--instance` unnamed | L1 (wave context), ScrSkillProvince |
| S4 | MEDIUM | no clause stops the C2 entry from advising `hyprctl dispatch` in its recheck | L1 / w2 review checklist |
| S5 | LOW | naive `verdict=` grep can be spoofed by a client class | ScrSkillProvince (one sentence) |
| S6 | INFO | C1 reference: no injection, no socket, no process, no write; scorer sandboxed | — |

Nothing in this review required a mutation, and none was run.
