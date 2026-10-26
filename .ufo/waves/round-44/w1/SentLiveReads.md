# SentLiveReads — w1 safety review: host reads, the C1 reference, the C2 entry's advice

Status: **complete**. Full ranked findings with repro: `.ufo/waves/round-44/w1/SentLiveReads/findings.md`
(276 lines); evidence in `.ufo/waves/round-44/w1/SentLiveReads/evidence/`; every quote checked by
`.ufo/waves/round-44/w1/SentLiveReads/verify-quotes.py` → `QUOTES: 25/25 verified`.

Base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, freeze `e2289516a9a857f55cda7be635933e89b931c3da`.
No mutation, no package transaction, no compositor socket of my own, no Wayland connection. One probe
was deliberately **not** run because it was the hazard (a newline inside a `getoption` name); the
pinned source settles it. Tool state: nothing installed (`python3` 3.14.8 and `/usr/bin/strace`
already present); scratch removed.

## Verdict per question asked

**(1) The host reads.** Read-only in the only sense available: every allowed verb is exactly one
connection and **one request-string write** to the compositor's request socket, then a read — there is
no verb-less read path (`evidence/strace.txt` §B, instance signature redacted to `<SIG>` per
`SKILL.md:332`):

```
hyprctl version -> "/version" 8   clients -j -> "j/clients" 9   monitors -j -> "j/monitors" 10
workspaces -j -> "j/workspaces" 12   getoption general:gaps_out -j -> "j/getoption general:gaps_out" 28
```

`-j` is not a flag on the wire, it is the `j/` prefix of the same request. `getoption` is read-only
(`Hyprland-HyprCtl.cpp:1647-1667` only calls `getConfigValue`) and the name is appended *after* the
verb, so a crafted name cannot become a command. The only multi-command path is the `[[BATCH]]` prefix
(`:2069`, `dispatchBatch` splits on `;` at `:1312`). What the seats actually ran: **one** literal
host-binary spawn in the whole wave — `ExecLiveHost/build-live-states.py:58` `run(["hyprctl",
"version"])` — plus the live-host seat's shell reads of `clients/monitors/workspaces -j` (captured to
JSON) and reads of `~/.config/hypr/gkeep.conf` and `/proc/sys/kernel/osrelease`. Every other seat
spawns python3/git/bash inside its own dir; the mutating-verb sweep over the whole wave directory
returns zero invocations (`evidence/host-reads.txt` §C/§D). `ExecHarmBase`'s `CASE xargs-pkill` lines
are `mado-tripwire.py --selftest` string classifications, not commands.

**(2) The C1 reference.** Injection: **blocked**, and verified with ten attacker-chosen classes
(`evidence/injection.txt`): quotes escaped, `=`/spaces stay inside the JSON-quoted field, LF/CR/NUL/ESC
are rejected before any line is printed (the `matches()` control-char gate drops the client entirely),
U+009B/DEL/`ü` are escaped by `json.dumps`, and a rule regex cannot inject because SAFE excludes
whitespace, `=` and newlines. Titles are never printed by the tool, so that vector does not exist in
C1. Host-free at syscall level: 0 socket/connect/bind/sendto, 1 execve (the interpreter), 0 opens with
`O_WRONLY|O_RDWR|O_CREAT` (`evidence/strace.txt` §A). ReDoS: **real and worse than documented** —
`(a|aa)+$` at 39 chars 6.9 s, `(a+)+$` at 31 chars **43.9 s**, 1 KB under `timeout 5` → rc 124 with
**0 bytes** of stdout (`evidence/redos.txt`). The `timeout 5` guard is still documented at
`SKILL.md:300` and is sound (output is written once at the end, so there is no partial verdict to
misread); what is stale is the *trigger* sentence at `SKILL.md:297`, which names only "an alternation
under a repeat" while SAFE also accepts nested quantifiers. The scorer is not exposed: it runs the
tool under bubblewrap with 30 s per fixture and stops after 3 timeouts.

**(3) The C2 entry.** The staged predecessor is clean — its recheck is `hyprctl clients -j` and it
keeps the observation `UNK` (`gkeep-client-size-request-r12.md:13,66`). The **predicate** is the gap:
`PRED-C2-r44` constrains only the shape of the `recheck:` line (counter `:75-76`), and no clause
forbids a mutation verb, so an entry that rechecks with `hyprctl dispatch resizewindowpixel …` is
admitted. The corpus convention already guards this in prose (`corpus/knowledge/theme-route-r18.md:3`,
`corpus/knowledge/idle-lock-route-r17.md:3` name every excluded tool), so the fix is a clause or a w2
checklist item, not a new idea.

## Ranked

| id | severity | one line | owner |
|---|---|---|---|
| S1 | HIGH | verbatim live dump with window titles/PIDs/addresses written into the repo. ExecLiveHost's copy (`live-clients.json`, `live-states.txt`, `fs2.json`, `max1.json`) is **fixed and re-verified** (10-key projection, raw sha256 only, 0 title lines, `timeout=30` harness); `w1/ExecIndepB/receipt-live-clients.json` was also **fixed and verified** (10-key projection, raw sha256 `5ead9176…`, `SENSITIVE_KEYS_PRESENT: 0`, both live receipts reproduce); the round-43 seat file is still tracked with 4 titles | L1 for the round-43 file |
| S2 | MEDIUM | ReDoS accepted by SAFE; `timeout 5` documented and sound but the documented trigger class is incomplete; the seat harness has no timeout | ScrSkillProvince, ExecLiveHost |
| S3 | MEDIUM | the wave fence is a denylist that omits `eval`/`repl` (Lua in the compositor) and `--instance`; `tools/mado-tripwire.py:255-259` already owns the better list | L1, ScrSkillProvince |
| S4 | MEDIUM | no C2 clause stops the entry from advising `hyprctl dispatch` in its recheck | L1 / w2 checklist |
| S5 | LOW | a client class can spoof a naive `verdict=` grep; the scorer is not foolable | ScrSkillProvince |
| S6 | INFO | positives: C1 reference is injection-free, socket-free, process-free, write-free; scoring an arbitrary tool file is sandboxed | — |

Two peer messages sent with the in-flight fixes: ScrSkillProvince (S2 wording, S5 sentence),
ExecLiveHost (S1 projection, S2 harness timeout).

## Checks the integrator should run

- `python3 -I .ufo/waves/round-44/w1/SentLiveReads/verify-quotes.py` → `QUOTES: 25/25 verified`.
- `git status --porcelain .ufo/waves/round-44/w1/ExecLiveHost/` before the data commit: S1 is only
  fixable while those files are untracked.
- `grep -c '"title"' .ufo/waves/round-44/w1/ExecLiveHost/live-states.txt` → 0 (was 3; ExecLiveHost's
  fix verified).
- `python3 -c "import json;d=json.load(open('.ufo/waves/round-44/w1/ExecIndepB/receipt-live-clients.json'));print(sum(1 for c in d if isinstance(c.get('title'),str)))"`
  → 0 (ExecIndepB's fix verified); the same sweep over every `*.json` in `round-44/w1` for `pid` + a
  string `title` returns nothing.
- `grep -n 'timeout=TIMEOUT' .ufo/waves/round-44/w1/ExecLiveHost/build-live-states.py` → line 37
  (S2 harness fix, verified).
