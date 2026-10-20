# AtkInstallsRecord — partial

Attacked: the round's install record — every report's `## Installs` section (59 w1 + 29 w2
present at 15:11) says none, i.e. the claim that this round produced no install or package
transaction, and the host-side measurement the w1 audit used to support it.

Result in one line: **no `## Installs` line is false.** The claim holds for durable tool
installs (PATH, uv tools, cargo, system npm/pnpm) and for anything a seat executed. It is
*partial* because two package-manager cache materializations did occur inside the round
window with no line in any report (one actor proven non-mado, one `[UNK]`), and the only
quoted host-side check (`CriticHonesty.md:43`) is narrower than a "no installs" reading.

## 1. ALPM log — no package transaction in the window

```
$ date '+%Y-%m-%dT%H:%M:%S%z'; stat -c 'mtime=%y size=%s' /var/log/pacman.log; sha256sum …; wc -l …
2026-10-20T15:03:04-0300   (T0)
mtime=2026-10-20 13:23:09.074537491 -0300 size=244858
27bbd0b558cfbc6ee27f5644863d6a62e1b468d462f4ea0de577ced86b256ffc  /var/log/pacman.log
3169
```
- Re-measured at T1 `15:08:41` and T2 `15:09:47`: identical mtime, size, digest, line count.
  Digest is the same value round 18 recorded (`…/round-18/w3/reports/MadoR18.W3NumbersAudit.md:220`),
  so the file was not rewritten between rounds.
- `grep -n '^\[2026-10-20T1[2-5]'` returns only `3161-3169`: `pacman -U … zcode-3.16.2-1`
  at `13:23:08` → `installed zcode (3.16.2-1)` → `pacman -D --asexplicit zcode` at `13:23:09`.
  No line carries a time ≥ 13:24.
- Window start: baseline `9c54c56` = `2026-10-20T13:53:34-03:00` (`git log`), pre-registration
  `17661e0` = `13:59:52`. The zcode transaction is **30 m 20 s before baseline**, already
  recorded with actor `[UNK]` at `corpus/lessons/round-18-verifier-spotcheck.md:124-125`
  and `SCORECARD.md:1009`. It is not a round-19 install and no mado seat names it.

## 2. Durable install channels — clean since baseline

```
for d in ~/.local/bin ~/.local/share/uv/tools ~/.cargo/bin /usr/local/bin \
         ~/.local/lib ~/.local/share/npm ~/.local/share/pnpm; do
  find "$d" -newermt '2026-10-20 13:53:34' | wc -l; done
→ 0, 0, 0, 0, 0, 0, 0
```
- `uv tool list`: `check-jsonschema v0.38.2`, `ruff v0.17.1`, `trafilatura v2.3.1`,
  `unblob v26.6.4`, `vulture v2.16`; `uv --version` = `uv 0.13.0`, `/home/vgpnk/.local/bin/uv`
  mtime `2026-10-09`.
- `uv-receipt.toml` mtimes: check-jsonschema `10-19 18:31`, trafilatura `10-19 18:01`,
  unblob `10-13 13:53`, ruff `10-20 13:14:22`, vulture `10-20 13:14:53` — the two newest are
  ~39 min **before** the window.
- `~/.local/bin` entries touched today: `09:10 swarm`, `10:17 llama-server` (symlink),
  `13:14 ruff`, `13:14 vulture`; newest mtime `13:14`. Nothing after.
- `CriticHonesty.md:43`'s command (`find ~/.local/bin ~/.local/share/uv/tools ~/.cargo/bin
  -maxdepth 1 -newermt '2026-10-20 13:53:34'`) re-run at 15:03 → still empty. True, but its
  `-maxdepth 1` × three directories cannot see §4.

## 3. Seat behaviour — no seat executed an installer

Transcript scan over `…/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_…/MadoR19/*.jsonl`
(`toolCall` blocks only; heredoc bodies and quoted regions stripped; command-position matching
for `uv tool install|run`, `uvx`, `uv run --with`, `uv pip install`, `pip install`,
`npm i|install|exec`, `npx`, `cargo install`, `pacman -S`, `yay/paru -S`, `curl -o ~/.local/bin`):

```
files=154 toolCalls=4956 candidate_executed_installer_commands= 1
MadoR19.AtkInstallsRecord.jsonl @ 18:02:40Z:  uv tool list 2>&1      ← this seat, read-only
```
- Main orchestrator `…/MadoR19.jsonl`: `toolCalls=128 installer_candidates=0`.
- Second-order check (a script written earlier, then run): 40 distinct `/tmp/*.sh|*.py`
  invocations from seat bash calls, each opened and re-scanned. Only
  `/tmp/revinstallers/head/tools/mado-tripwire.py` contains installer tokens (`|uvx` inside
  its classifier regex); none of the 40 executes an installer.
- `eval` calls: 161 scanned for `%pip` / `%bun add` / `!…installer`; 31 lexical hits, all
  fixture strings inside attack seats (e.g. `MadoR19.AdvBashCVar` writing `! pacman -S …`
  into a docstring/`/tmp/atk-note.sh` fixture), none executed.
- Coverage: 59/59 w1 reports have `## Installs`; all say none. 29/29 w2 reports present at
  15:11 have it; all none (`AdvVcs`, `MutAnchorSweep`, `MutFrozenRepin`, `MutGateR19`,
  `ReopenS097`, `RerunLanded`, `RerunSuites`, `ScribeLogCheck`, `SentinelCommitSet`, … quote
  read-only tools already present).

## 4. What the record does not cover — in-window cache-level installs

**(a) uv, 13:54:48 — actor proven, not mado.**
```
~/.cache/uv/archive-v0/pPGtjoTdVZCmphdc created 13:54:48:
  markdown_it_py-4.0.0.dist-info/REQUESTED, mdurl-0.1.2
~/.cache/uv/environments-v2/4125d872e233ee51/6184fad417806aba -> that archive (13:54)
  (sibling a4f97acb16a24776 -> archive kuXMbE9vgWVjSzxs at 13:23, site-packages: blender_mcp)
```
Attribution, from `KaidokuR18.GateREGISTRY.jsonl` (16:54:48Z = 13:54:48-0300):
```
uv run --no-project --with 'markdown-it-py==4.0.0' python3 -I -B -c "import markdown_it…"
→ "Installed 2 packages in 7ms / markdown-it-py 4.0.0 3.13.16"
```
This is a **kaidoku lane round-18 seat**, 74 s after the mado baseline. It writes only
`~/.cache/uv`; it is not a mado install and needs no mado `## Installs` line — but it is the
counterexample to any closure sentence that says "no packages were installed during this
window" rather than "no tool was installed".

**(b) npm, 14:22:01 — actor `[UNK]`.**
`~/.npm/_cacache` index entries written `14:22:01` (`time` 1792516921036/…1074):
```
https://registry.npmjs.org/acorn            385,243 B  (etag W/"f4d10430…")
https://registry.npmjs.org/acorn/-/acorn-8.19.0.tgz  134,282 B
```
No seat transcript in a ±30 s window mentions `acorn`; no `node_modules/acorn` appears under
`/home/vgpnk/Projects` (depth 9, `14:15-14:30`) or `/tmp`, `/var/tmp` (depth 7); the npm
debug log for 14:22 no longer exists (`logs-max:10`; later runs pruned it). Nothing ties it to
a mado seat; actor `[UNK]`.

**(c) 14:57:56-14:58:31 — ephemeral registry runs, non-mado `[INFERENCE]`.**
Live at 15:05: `npm exec --yes rea-agents@6.7.0 mcp`, `npm exec --yes godot-mcp`,
`/home/vgpnk/.local/bin/uv tool uvx mcp-for-blender`, and
`node /home/vgpnk/.zcode/cli/plugins/cache/zcode-plugins-official/blender/0.2.3/dist/server.mjs`.
npm debug logs give cwds `/home/vgpnk/Projects`, `/home/vgpnk/Projects/BTVREV`,
`/home/vgpnk/.zcode/workspace/…` — none is the lane. Side effects: `_npx/a1722018f28f9df2`
created `14:58:31`, uv index fetches for the blender-mcp dependency set `14:57:56`, uv
interpreter-v4 writes `15:02:40`. No PATH change; no report line is owed.

## 5. Record-wording checks

- Committed `LOG.md` at `01b8094` ends with **round 18** — no round-19 install sentence exists
  yet, so no committed artifact overclaims "no installs this round".
- `SentinelHostPause.md:130` says its greps of landed reports found "no `sudo`, `pacman -S`,
  `npx` or `uv tool install` mentions". That is **false about the w1 set as it now stands**:
  `CriticInstallerClass.md:51-52`, `TwInstallers.md:46-49`, `TwMerge.md:191`,
  `CriticC3.md:100`, `CriticHonesty.md:104/113` all contain those strings. Its own grep ran at
  14:11:24; those reports carry mtimes 14:12+, so whether it was true then is `[UNK]`.

## Falsifiers (what would move this verdict)

1. A w2 report landing with a non-none `## Installs` line.
2. Any ALPM line after `13:23:09` (none through T2 15:09:47).
3. A mado transcript command that starts an installer (none in the 154 files scanned; in-flight
   w2 sessions can still add one).
4. Attribution of the acorn 8.19.0 cache fetch to a mado actor (`[UNK]` now).

## Limits

- w2 is in flight: 29 reports and 154 transcripts with tool calls at 15:10; later writes are
  unaudited. My scanner is lexical (command-position + heredoc/quote stripping); an indirect
  install — a fetched script that itself downloads — is not detected, though the 40 written
  `/tmp` scripts were re-read and none carries an installer.
- The 14:22 npm event is provably *a* registry fetch but not a *durable* install: no
  `node_modules/acorn` appeared anywhere I could scope.
- `ps` was used for process attribution; it is not in the pause's forbidden list, but note it.
- Pause respected throughout: no `pacman`/`yay`/`paru` in any form (not even `-Q`), no `sudo`,
  no `systemctl`/`journalctl`/`loginctl`, no compositor/input/service command, no gate run
  (no copy in any mode), no `jj`, no lane edit. `pacman.log`, pacman `desc`, caches and
  transcripts read as file bytes / `stat` / `grep` / `sha256sum` / `python3` only.

## Installs

none — nothing installed or upgraded; `uv --version`, `uv tool list`, `ps`, `find`, `stat`,
`sha256sum`, `python3` were used read-only from tools already present. No fetch.
