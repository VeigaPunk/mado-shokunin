# ExecSkillSection — w2 falsify (round 47, wave 2)

Scope: run **every** command of `.ufo/waves/round-47/w1/ScrSkill/section.md` exactly as written, with
`tools/mado-terminal.py` substituted by the L1 reference `.ufo/waves/round-47/l1-draft/mado-terminal.py`,
`XDG_CACHE_HOME` inside scratch, and no terminal ever launched. Then report every place an operator gets stuck or
misled. I did not touch C1/C2 counters (their seats own them); everything below is the SKILL text against the tool
it documents.

Environment of every run: host `XDG_CURRENT_DESKTOP=Hyprland`, `HOME=/home/vgpnk`,
`PATH=/usr/local/bin:/usr/bin:/bin`, `/usr/bin/xdg-terminal-exec` sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` (equal to
`.ufo/waves/round-47/fetch/xdg-terminal-exec`, the pin). Scratch `/fast/scratch/hyaku/mado-r47/ExecSkillSection`,
deleted at the end; every receipt is copied under
`.ufo/waves/round-47/w2/ExecSkillSection/receipts/`. No tools installed.

## Verdict

The tool side holds: all five section commands ran, and every printed item the section shows is what the tool
prints — **except the verdict line in the third block, which the tool cannot print** (H1). Beyond that, three
statements in the text are false about the frozen reference and one points at documentation that does not exist
(H2–H4); four more are traps or imprecisions (H5–H9). No hole found in the C1 capability itself by these
commands: five extra print pairs are byte-equal, the resolver and the tool agree on the host, and the resolver's
own cache is the only thing either run writes.

Severity for the freeze: **H1–H4 should be fixed before the data commit** (they are operator-facing lies inside
the shipped SKILL; H4 is also a gap in the C1 contract, so fixing it changes the docstring the C1 counter judges
against — cheaper now than after data). H5–H9 are wording/robustness; H5 cannot be fixed by the skill alone
because the divergence is in the tool's stderr, which the contract deliberately leaves out.

## Every command, as written

Receipts: `receipts/section-as-written.txt` (the script `run-section.sh` reproduces all of it in 4 s),
`receipts/divergences.txt`, `receipts/section-probes.txt`, `receipts/strace-print.txt`,
`receipts/script-locators.txt`, `receipts/quotes.tsv` + `receipts/quotes-verified.txt` (each quote below is greped
against its stated `file:line`; 14/14 found, all ≤ 25 words).

| # | command (as written, reference substituted) | observed | verdict |
|---|---|---|---|
| 1 | `python3 tools/mado-terminal.py print --print-id --print-path --print-cmd` | `Alacritty.desktop` / `/home/vgpnk/.local/share/applications/Alacritty.desktop` / `alacritty`, rc 0 | matches the block exactly |
| 2 | `print --print-id --print-path --print-cmd --dir=/tmp -- htop` | three lines above, then `--working-directory=/tmp`, `-e`, `htop`, rc 0 | matches exactly |
| 3 | `explain` | 5 trace lines, then `MADO_TERM: … cmd=alacritty cache=absent verdict=OK`, rc 0 | **the quoted line is not the line printed (H1)** |
| 4 | cold `xdg-terminal-exec … > term.observed` then `explain --observed term.observed` | capture 3 lines + trailing `\n`, 1 cache file written (backgrounded); tool `verdict=AGREE`, rc 0 | matches |
| 5 | `--selftest` | `MADO_TERMINAL_SELFTEST: 43/43 passed`, rc 0 | matches (`N >= 30`) |
| 6 | `print --dir=/tmp --print-cmd` (symptom table) | `alacritty`, `--working-directory=/tmp`, rc 0 | matches |
| 7 | `XTE_DEBUG=1 XDG_CACHE_HOME=… xdg-terminal-exec --print-id` (Notes) | stdout `Alacritty.desktop`, 628 debug lines on stderr | matches ("debug goes to stderr") |

Exit-status paragraph also checked: `print` with no print flag → `MADO_TERM_OUT_OF_CONTRACT: no print option and
no --test: the resolver would launch a terminal`, rc 2; unknown mode → one usage line, rc 2; unreadable
`--observed` → one line, rc 2; `DIFFER` → rc 1 (H6 receipts); `NO_TERMINAL` → rc 3; `--observed` on a no-terminal
tree → rc 0.

## Holes

### H1 — the `explain` sample verdict line is one the tool never prints (must fix)

`section.md:35` quotes `MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop verdict=OK`
— it omits `cmd=` and `cache=`, which the reference docstring fixes at `l1-draft/mado-terminal.py:19`
(`MADO_TERM: selected=<id|-> path=<path|-> cmd=<exec[0]|-> cache=<absent|present|disabled> verdict=<V>`) and which
the tool always prints (`l1-draft/mado-terminal.py:854`). An operator diffing their output against the SKILL sees a
mismatch on the one line the SKILL told them to read, in both the OK and AGREE rows
(`section.md:52`, `section.md:53`).

Reproduce:
```
python3 tools/mado-terminal.py explain | grep '^MADO_TERM:'
# MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop cmd=alacritty cache=absent verdict=OK
sed -n '35p' .ufo/waves/round-47/w1/ScrSkill/section.md
```
Fix: quote the full line (both places: the sample block and any row text that repeats it).

### H2 — "print with no `--print-*` flag is a usage error" is false for `--test` (must fix)

`section.md:47` says `print` with no `--print-*` flag is a usage error. `--test` is not a `--print-*` flag, is
accepted by the reference (`l1-draft/mado-terminal.py:15` — "… `--print-cmd[=SEQ]` or `--test` is required"), and
prints the composed argv at rc 0, byte-identical to the resolver; the tool's own refusal message already says
`no print option and no --test` (`l1-draft/mado-terminal.py:763`). The SKILL therefore hides the one mode that
shows *all* composed arguments (id, path, exec args, command) in one go — the thing an operator debugging
`--dir`/`--title` wants.

Reproduce:
```
python3 tools/mado-terminal.py print --test -- htop; echo rc=$?     # rc=0
XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --test -- htop; echo rc=$?   # rc=0, same three lines
```
Receipt `receipts/divergences.txt` §H2.

### H3 — the `--print-content` note is false twice (must fix)

`section.md:76` says "`--print-content` is a script mode the draft contract does not cover". Falsified both ways:
the reference docstring lists it as a sufficient print flag (`l1-draft/mado-terminal.py:15`) and states what it
prints (`:76`), and the tool implements it (`:748`) with stdout+rc byte-equal to the pinned script on this host:
sha256 `713703ba90ff8cd8d66eeb2804202e05e0c80c48e651ad00b9b7276f3d057683` from both. The note tells an operator to
avoid a mode that is in contract and verified; `--print-content --print-cmd` is also byte-equal
(sha256 `c1ca5ef1058eb2e73f1e9f8f7007d1bd22385abea2af53ff1ad8d0d5cc5c0adf` from both), i.e. the two modes the
script's own `--help` calls conflicting (`/usr/bin/xdg-terminal-exec:120`) compose in both implementations.

Reproduce:
```
python3 tools/mado-terminal.py print --print-content | sha256sum
XDG_CACHE_HOME=$(mktemp -d) xdg-terminal-exec --print-content | sha256sum   # same digest
```

### H4 — "the tool's docstring fixes their prefixes" points at nothing; the `-` sentinel is undefined (must fix, or fix the docstring before data)

`section.md:34` elides the trace as "… trace lines (the tool's docstring fixes their prefixes) …". The docstring
(lines 1–79 of the reference) never names `MADO_TERM_TRACE` or `MADO_TERM_DESKTOPS`; both appear only in code
(`l1-draft/mado-terminal.py:835` and `:837`, verified by `receipts/quotes-verified.txt`). The desktop line's
sentinel for an empty desktop list (`MADO_TERM_DESKTOPS: -`) is also undocumented. An operator who follows the
pointer finds nothing, and the trace — the SKILL's main diagnostic surface — has no contract at all.

Reproduce:
```
env -u XDG_CURRENT_DESKTOP python3 tools/mado-terminal.py explain | head -2
# MADO_TERM_DESKTOPS: -
grep -n 'MADO_TERM_TRACE\|MADO_TERM_DESKTOPS' .ufo/waves/round-47/l1-draft/mado-terminal.py
# 835 / 837 only; no docstring line
```
Note the selection is still correct with the desktop var unset (resolver and tool byte-equal, receipt
`receipts/divergences.txt` §H4b), so this is a documentation gap, not a behavior bug. Fixing it touches the C1
contract, which is why it belongs in the pre-data window.

### H5 — the rc-1 row describes the resolver's stderr, but the operator sees the tool's (doc-only; the tool diverges)

`section.md:57`: "stdout empty; the resolver's stderr carries `No valid terminal entry was found in:` and the
applications dirs". Running the *tool* in that state prints the heading, then one directory per line; the resolver
prints them `:`-joined on one line (`/usr/bin/xdg-terminal-exec:1109`, `IFS=':' error …`). stdout and rc are equal,
so the C1 contract is not broken (it is stdout+rc); the row just reads as if the stderr text matches.

Reproduce (empty hermetic tree, receipts/divergences.txt §H5):
```
XDG_CACHE_HOME=… xdg-terminal-exec --print-id 2>&1 | od -c | tail -3
XDG_CACHE_HOME=… python3 tools/mado-terminal.py print --print-id 2>&1 | od -c | tail -3
```
Fix in the SKILL: say "the tool prints the heading and the dirs, one per line; the resolver joins them with `:`".
(Or, if stderr should match, that is a tool change and a C1 contract change — decide before data.)

### H6 — the DIFFER row's cause list misses the most common cause: a capture made with other print flags

`section.md:54` names three causes ("a missing `--dir`/command argument, a different `XDG_*` value, or a warm
cache"). A capture made with `--print-delimiter='|'`, or with `--print-id` alone, yields `DIFFER` rc 1 while the
selection is identical — the tool compares the three expected lines, so any other capture shape differs. The
remedy ("re-capture with the exact command above") is right, but the diagnosis sends the operator to
`--dir`/`XDG_*`/cache first. Receipt `receipts/divergences.txt` §H6, §H6b (capture bytes shown).

### H7 — `AGREE` with `selected=-` is a clean bill of health for a machine with no terminal

An empty capture file is exactly what a no-terminal resolver run leaves (rc 1, 0 bytes). Feeding it back gives
`MADO_TERM: selected=- path=- cmd=- cache=absent verdict=AGREE`, rc 0; the AGREE row's next step is "none for the
selection", which reads as "fine". AGREE is correct in the docstring's sense (both printed nothing), so this is a
SKILL gap: state that `AGREE` with `selected=-` means *both* found nothing, and point at the NO_TERMINAL row.
Receipt `receipts/divergences.txt` §H7.

### H8 — `--selftest` under a TMPDIR that does not exist dies with a traceback

`section.md:42` says the cases are "built under $TMPDIR". With `TMPDIR` set to a missing directory the tool exits 1
with `FileNotFoundError` from `tempfile.mkdtemp` (reference `l1-draft/mado-terminal.py:991`) and never prints the
`MADO_TERMINAL_SELFTEST` line, so an operator's wrapper reports a failure with no verdict. Either the docstring
should create the directory (`os.makedirs(..., exist_ok=True)`, a C1 contract change) or the SKILL should say the
directory must exist. Receipt `receipts/divergences.txt` §H8.

### H9 — "a run that includes `--print-cmd` rewrites the cache" reads as the tool's run

`section.md:9` (parenthetical) — measured: the tool writes **0** files into a fresh `XDG_CACHE_HOME`;
the resolver with `--print-id` alone writes **0**; the resolver with `--print-cmd` writes **1** (it backgrounds
`save_cache`, `/usr/bin/xdg-terminal-exec:1457`). Say "a *resolver* run that includes `--print-cmd`…". Receipt
`receipts/section-as-written.txt`, last block.

## Verified sound (do not re-litigate without new evidence)

- All five commands' stdout/rc match the section (H1 excepted), including the seq `id → path → cmd` order under
  reversed flag order.
- Five extra print pairs byte-equal to the resolver: `--print-cmd='\t'`, `--print-delimiter='\n\n'`,
  `--print-cmd=, -- htop`, `--dir=/nonexistent --print-cmd`, and the hotkey shape
  `--dir=/tmp --app-id=C --title=T --hold -- htop`.
- Prose claim "starts no process, opens no socket": `strace -f -e trace=execve,clone,clone3,fork,vfork,socket,connect`
  around one print run shows 1 `execve` (python3 itself), 0 clone/fork, 0 socket/connect
  (`receipts/strace-print.txt`); `grep -nE 'subprocess|os\.system|popen|fork|socket'` on the reference finds only
  the docstring line.
- Cache claims: only the resolver writes, only with `--print-cmd`, and `explain` reports `cache=present` without
  changing the selection (`receipts/section-probes.txt` P8).
- Symptom-table rules, hermetic probes (`receipts/section-probes.txt`, each case byte-compared tool vs resolver):
  P1 `Type=Link` selected; P2b `NoDisplay=true` selected; P3 listed `Hidden=true` skipped, trace names
  `rejected: Hidden=true`; P4 `OnlyShowIn=GNOME` rejected as fallback, accepted when listed; P5 bad action
  rejected (`rejected: Actions lacks 'BadAction'`), good action selects `good.desktop:New` on both id and path;
  P6 empty `--title=` composes nothing, `--title=T` composes `--title=T`; P7 duplicate id resolves to the user
  copy and its `X-TerminalArgDir` composes `--working-directory=/tmp`; P2a fallback order is reverse `find` order.
- `Type=` / `NoDisplay=` are never read: `grep -nE 'Type=|NoDisplay' /usr/bin/xdg-terminal-exec` → no match
  (`receipts/script-locators.txt`).
- Host facts the SKILL asserts: `~/.config/hypr/bindings.conf:2` is the SUPER+RETURN line
  `bindd = SUPER, RETURN, Terminal, exec, uwsm-app -- xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"`;
  `uwsm-app` is present in `/usr/bin`; `omarchy-cmd-terminal-cwd` is present at
  `~/.local/share/omarchy/bin/omarchy-cmd-terminal-cwd`; `~/.config/xdg-terminals.list` line 3 is
  `Alacritty.desktop`; the user entry carries `X-TerminalArgExec=-e`, `X-TerminalArgDir=--working-directory=` while
  the system copy `/usr/share/applications/Alacritty.desktop` has no `X-Terminal*` key at all — so the SKILL's
  duplicate-ID sentence is materially load-bearing and correct (the second example's `--working-directory` only
  appears because the *user* copy wins).
- Cited script locators all land: `754-800` (find/fallback: 782 alias, 790 prepend, 795/797 find+awk),
  `816-968` (816 `'Categories'*=*` … 947 `'Exec'*=*`, 964 `command -v "$XTE__EXEC0"`), `829-845`
  (829 `'Actions'*=*`, 846 `'OnlyShowIn'*=*`), `1087-1101` (1092 `XTE__EXECARG_DEFINED` strict branch),
  `1415-1427` (title), `1494-1496` (1496 `cd "$XTE__DIRVAL"`), `179-215` (180/200/201 md5 + `ls -LRl`),
  `1457` (`save_cache "$1" &`). Receipt `receipts/script-locators.txt`.

## Not checkable here / residuals

- `corpus/knowledge/xdg-terminal-selection-r47.md` does not exist yet (no data commit), so the Ground line
  "(rows S326..)" dangles until the data commit lands. Expected state, not a hole — but the SKILL and the entry
  must land in the same commit or the shipped page has a dead pointer.
- Warm-cache equivalence, the launch path, `-h/--help` and empty-argv are out of contract by the registration; I
  did not run the resolver without a `--print-*` flag.
- H5's divergence is in stderr, which the C1 contract does not judge; I report it because the SKILL's row talks
  about what the operator will see, not about the contract.
- No C1/C2 score attached: I did not run the counters (not this seat's assignment), and nothing here contests
  clauses a/s/f/x/g/i/r beyond the tool behaviors exercised above.

## Receipts (all under `.ufo/waves/round-47/w2/ExecSkillSection/`)

`run-section.sh` + `receipts/section-as-written.txt` · `run-probes.sh` + `receipts/section-probes.txt` ·
`run-divergences.sh` + `receipts/divergences.txt` · `verify-quotes.sh` + `receipts/quotes.tsv` +
`receipts/quotes-verified.txt` · `receipts/script-locators.txt` · `receipts/strace-print.txt`.
Every script takes the work dir as `$1` (no `/tmp` hardcoded), sets `XDG_CACHE_HOME` inside it, and never invokes
the resolver without a print flag.
