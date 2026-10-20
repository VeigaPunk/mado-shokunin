# SentinelHostPause — wave 1 has no item that tells a seat to run a package, service or compositor command, but four paths can still get there: an injected tooling directive, unguarded gate copies, selftest PATH hygiene, and loose ~/.config/omarchy and out-of-lane wording. Thirteen phrases for wave 2 are listed below.

What I read: the wave context and all 86 items as dispatched (`.ufo/waves/round-19/w1/spec.json` sha256 `b13e28c0…`, `dispatch.json` sha256 `274efd07…`, `taskCall.context == spec.context`), my own assignment as delivered, and `/home/vgpnk/.omp/agent/RULES.md` (sha256 `beb647d0…`). I checked the code paths behind each risky instruction: `tools/mado-verify.sh` at 17661e0 (`c9fb0cef…`) and the in-flight worktree (`ab720e30…`), plus the tameshi harness, the measure scripts, the counters and `scripts/sources-census.sh`. I ran no gate mode, no host command and no package query. Item references below are `spec.json .items[N]` (name).

## Findings

### H1 — High: the injected tooling directive points seats to `sudo pacman -S`, and nothing says the HOST PAUSE beats it
- **How it goes wrong:** a seat is missing a tool. The "always on" directive tells it to install with `sudo pacman -S --needed --noconfirm <pkg>` "with full privilege, without asking first. Passwordless `sudo` is available". The seat installs. On a host already in the R15-V1 partial-upgrade state, a `-S` against a stale sync database is a new partial upgrade.
- **Evidence:**
  - RULES.md:4-7 carries the directive above, with pacman as the first channel.
  - The dispatched tasks do not contain it (0/86 tasks match "Tooling directive"). My delivered assignment does, and so does my system prompt as `<generic-rules>`. So the runtime injects it into every seat.
  - That same system prompt says XML-tagged content is "system-authored/authoritative". A seat can therefore rank the directive above the context's HOST PAUSE (context line 10).
  - Context line 11 makes it worse: "read /home/vgpnk/.omp/agent/RULES.md first".
  - The godspeed prefix on every item ("IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS") takes away the pause where a seat might have asked.
- **Impact:** a host-wide pacman transaction during an operator-owned pause, which can break boot (RULES.md itself names the mkinitcpio/btrfs-overlayfs hazard).
- **Smallest fix:** see phrases P1 and P2.

### H2 — High: the live-gate ban names only `tools/mado-verify.sh`, but this wave makes full copies of the gate whose default mode is live
- **How it goes wrong:** a seat runs one of these copies bare, for example to "reproduce" the receipt for criterion 26:
  - GateSwapReceipt (item 8) commits a full gate copy to `.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh`.
  - MutGateWalkerArms (item 85) makes mutants.
  - `--regression` builds a derived target (items 7, 14).
  - Many items make `/tmp` copies.
- **What a bare run does:**
  - With no flags, `ROOT="${MADO_VERIFY_ROOT:-$HOME}"` (mado-verify.sh:86) and `LIVE_REQ=auto`. The main block then sets LIVE=1 when ROOT is $HOME (17661e0 ~:3729-3731).
  - The live plane then runs `walker --version` (:3276), `systemctl --user is-active app-walker@autostart.service` / `elephant.service` (:3286-3287), `busctl --user get-property …` (:3263), plus the hyprctl and omarchy readers.
- **The ban also misses read-only host modes:** SCORECARD.md:235, :287 and :400 list `bash tools/mado-verify.sh --no-live` as a counting command. It reads real `$HOME/.config` and uses a cwd-relative path. CriticC2 (item 77) asks whether "the gate now FAILs where it passed", which invites exactly this run.
- **Smallest fix:** phrase P3. Also, in the fixture builder only (L1's call, not applied), insert after the arg loop: `[ "$MODE" = selftest ] || [ "$ROOT" != "${HOME%/}" ] || { echo 'fixture: live mode refused' >&2; exit 2; }`. Every selftest re-invocation passes `--root`, `--help`, `--bogus`, `--snapshot*` or `--regression`, so the guard leaves the selftest unchanged [INFERENCE: verified by reading the 71 `"$0"` call sites, not by running].

### H3 — Medium: selftest hermeticity depends on every scenario *replacing* PATH, and item 7 does not require it
- **How the selftest stays hermetic today:**
  - The live-mode scenarios run under `env PATH="$OMB"` / `"$SANDBOX"`: mado-verify.sh:694-838, :1042, :1481.
  - The sandbox is a directory of symlinks to a whitelist of coreutils (:686, :1038).
- **What item 7 asks for:** new walker scenarios — "walker 2.17.2 PASS / other FAIL" plus the absent-binary arm from RevGateWalkerRow (item 60).
- **What the in-flight edit has so far:**
  - It adds `walker_live_rows()` (worktree :3070), called from the live plane (:3335).
  - It is not yet wired into the selftest (grep shows no stub knob).
- **Where it goes wrong:** if a scenario prepends a stub dir (`PATH="$stub:$PATH"`), or calls the function in-process with the inherited PATH, then:
  - the absent-walker arm runs the real `/usr/bin/walker --version`;
  - any scenario without a systemctl stub runs the real `systemctl --user`.
- **Amplifier:** `--regression` runs the derived target's selftest once for the control and once per defect (11 runs, regression-recut.txt:33-44). Item 14 (HarmWatch19) runs both modes too.
- **Same failure for item 85:** a mutant of the dispatch (`--selftest) MODE=selftest`, ~:3716) or of a PATH prefix falls through to live mode.
- **Action taken:** I messaged MadoR19.GateFreshJj (use a replaced PATH, never prepend) and MadoR19.MutGateWalkerArms (keep dispatch and PATH prefixes out of the mutant set). MutGateWalkerArms replied that none of its probes changed dispatch or PATH prefixes. It ran each copy with explicit `PATH=/usr/bin:/bin` and `HOME=/tmp/mado-r19-MutGateWalkerArms-…/isolated-home`, and reports no real host probe ran (its claim; I did not check it).
- **Residual risk:** an isolated HOME does not stop live mode, because ROOT then equals the isolated HOME and LIVE=auto still resolves to 1. `/usr/bin` still holds walker. Only an intact dispatch keeps those runs off the host.
- **Smallest fix:** phrase P4.

### M4 — Medium: item 12's "test in a /tmp clone" can overwrite the committed lane receipt
- **The trap:** the 17661e0 version of `measure-mutants.py` writes `out = args.out or (lane / OUT_DEFAULT)` (line 502). Here `--lane` defaults to `/home/vgpnk/Projects/shokunin/mado-shokunin` (LANE_DEFAULT :42) and `OUT_DEFAULT = .ufo/waves/round-18/evidence/measure-mutants.json` (:43).
- **How it goes wrong:** running the clone's old copy for a red-before or comparison writes into the lane from `/tmp`. That is the round-18 W3FreshClone incident again.
- **Current state:** I checked, and the lane receipt still matches HEAD (`58929eea…` for both). The worktree script already carries the fix.
- **Fix:** phrase P5.

### M5 — Medium: item 55 (RevRubricVRisk) points the lane's `measure.py` at a clone's HEAD
- **The mismatch:** `round-17/measure.py:50` sets `REPO = Path(__file__).resolve().parents[3]`, and the lane copy resolves that to the lane. So "run `python3 …/mado-shokunin/.ufo/waves/round-17/measure.py HEAD` in the clone (commit in the clone)" measures the lane's detached jj working-copy HEAD, not the clone.
- **Why it matters:** the obvious way to make the command "work" is to commit in the lane, which is a forbidden lane write.
- **Precedent:** measure-mutants.py:14-17 shows the correct pattern — copy the instrument into `<clone>/.ufo/waves/round-17/`.
- **Fix:** phrase P6.

### M6 — Medium: wording on ~/.config/omarchy leaves secret-bearing files readable
- **Context line 10:** it allows host "config trees" as FILE BYTES. The only carve-out is "credential/auth/oauth files", which is name-based.
- **SrcS094 (item 19):** it says "ls ~/.config/omarchy/themes, ~/.config/omarchy/current/theme.name **or equivalent**", which is open-ended.
- **ProvinceScope (item 21):** it says "never **print** file contents that could hold secrets". Reading is still allowed, and the seat must "identify which entries are mado surfaces".
- **What is actually there** (names only, `find -maxdepth 3 -printf '%y %p %l'`):
  - `hooks/post-update.d/install-voxtype.hook` (0755 per ProvinceScope.md:90)
  - `hooks/post-boot.d/weather.sample`
  - `extensions/menu.sh`
  - `branding/*.txt`
  - No secret-*named* file matched `*secret*|*token*|*key*|*cred*|*auth*|*pass*|*.env|*.age|*.gpg` except `current/theme/keyboard.rgb`.
- **Breach check:** ProvinceScope.md:89-90 reports names, sizes and modes only. I saw no breach.
- **Fix:** phrase P7.

### M7 — Medium: writes outside the lane are implicit or unbounded
- **Installs vs "write only":** context line 11 authorises `uv tool` and `npx`. `uv tool` writes `~/.local/bin` and `~/.local/share/uv`. `npx` executes registry code and caches in `~/.npm/_npx`. This contradicts line 8, "Write ONLY your assigned files plus your own report".
- **npx is not in RULES.md** (grep: no `npx`). The only npm channel there is `npm -g`.
- **`/tmp` scratch names are unprefixed.** DeltaWalkerCli's `/tmp/...` clone and the TwBashCVar/TwHelperFn/TwInstallers/TwVcsClass copies (items 0-3) can collide across concurrent seats.
- **Fetch receipts can push large files into the lane** (context line 15). `curl -o BODY` with BODY under `.ufo/waves/round-19/fetch/…` writes the body before the size check, so a file over 1 MiB lands in the lane. SrcS084 (item 20) fetches a .crate that may be large.
- **Item 42 (ReportSkeleton) names a fleet path as its target:** "skeleton for /home/vgpnk/Projects/shokunin/.ufo/reports/round-19/mado.md". That directory exists and holds sibling lanes' reports (kagi.md, kake.md, kotoba.md, kotodama.md).
- **Item 14's fleet script is safe:** it runs `scripts/sources-census.sh validate`, which writes only stdout or `--out` (sources-census.sh:7, :94).
- **Fix:** phrase P8.

### M8 — Medium: three items attribute the wrong rules to RULES.md
- **The claim:** TwInstallers (item 2), RevDraftInstallers (item 46) and CriticInstallerClass (item 80) say RULES.md makes "installs via uv tool/npx/official binaries … AUTHORIZED; pacman paused".
- **What RULES.md says:** RULES.md:7 lists `sudo pacman -S --needed --noconfirm` *first*, and the file has no `npx` and no pause.
- **Where those rules come from:** the pause and npx come from the wave context's "orchestrator ruling 2026-10-20".
- **How it goes wrong:** a seat that checks the claim against RULES.md concludes `sudo pacman -S` is an authorised channel. The tripwire's installer class could then be built to permit it, which inverts the HOST PAUSE.
- **Fix:** phrase P9.

### L9 — Low: unexpanded template variables and cwd-relative commands
- **Literal placeholders reached the seats:**
  - `{JJ}` in GateFreshJj (item 7).
  - `{FLEET}` in AnchorDurability (item 9) and twice in HarmWatch19 (item 14): "`{FLEET}/scripts/sources-census.sh validate --root {FLEET} mado`".
  - `{{…}}` in SupersedeSweep (item 10).
  - Cause: `gen_w1.py` defines FLEET and JJ, but these item strings were not formatted.
- **Effect on item 14:** a harm-watch.sh that hardcodes the literal fails. A seat that "fixes" it by guessing may use a relative `scripts/…`.
- **Other relative commands:**
  - The SCORECARD navigation block that items 14 and 59 tell seats to run calls `git` with no `-C` (SCORECARD.md:69-90). Run from the fleet cwd, it reads the fleet repo. That is a read-only misroot.
  - RevJjDisposition (item 52) says `ls -d .jj` with no directory.
- **Fix:** phrase P10.

### L10 — Low: context line 11 spells out a forbidden command
It includes the literal `pacman -Sp --print-format '%n %v' <pkgs>`, while line 10 forbids even `-Sp`. That invites copy-paste. **Fix:** phrase P11.

### L11 — Low: git reads against the host omarchy checkout
GateFreshJj (item 7) and RevJjDisposition (item 52) run `git -C ~/.local/share/omarchy symbolic-ref` / `for-each-ref`. Those verbs do not touch the index. Verbs that refresh the index (`status`, `diff` against the worktree, `describe --dirty`) can run a repo-configured `core.fsmonitor` command, and the checkout sits outside the lane [INFERENCE, not exercised]. **Fix:** phrase P12.

### L12 — Low: untrusted fetched source
DeltaWalkerCli (item 18) clones walker into `/tmp`; SrcS084 (item 20) extracts the xdg crate. Neither item forbids `cargo build/test/run`, which executes `build.rs` and writes `~/.cargo`. **Fix:** phrase P13.

### L13 — Low: concurrent load can produce false reds [INFERENCE]
GateFreshJj, GateSwapReceipt, HarmWatch19, MutGateWalkerArms (items 7, 8, 14, 85) and every tripwire suite run concurrently on one host. The harness has a 300 s per-run timeout (mutate-and-run.sh:198); a run that times out exits 124 and is scored INCONCLUSIVE (:534), which `--regression` reports as FAIL. This is not a pause breach, but a false red could push a seat toward "re-verifying live". No phrase; note it for L1's verification sequencing.

## Phrases to strengthen for wave 2 (paste-ready)

- **P1** (context, top of Contract): "PRECEDENCE: this HOST PAUSE overrides the always-on 'Tooling directive' (system `<generic-rules>` and /home/vgpnk/.omp/agent/RULES.md) for the whole round. Its first channel `sudo pacman -S` and the 'passwordless sudo / without asking first' clause are suspended. If you need a tool, use uv tool or an official release binary into ~/.local/bin, or report the need."
- **P2** (context line 11): replace "read /home/vgpnk/.omp/agent/RULES.md first" with "RULES.md is background only; its pacman channel is suspended by the HOST PAUSE above".
- **P3** (context line 10): replace "never the live gate (`bash tools/mado-verify.sh` without --selftest/--regression)" with "never run ANY copy of mado-verify.sh — tools/mado-verify.sh, /tmp copies, mutants, regression targets, `.ufo/waves/round-19/evidence/gate-swap-*.sh` — except with exactly `--selftest` or `--regression`. `--no-live`, `--root`, `--live`, `--snapshot` and a bare run all count as the live gate. SCORECARD counting commands that invoke the gate are not run this round."
- **P4** (item 7 GateFreshJj, and any gate-selftest item): "Every new scenario that reaches live rows runs under `env PATH="$SANDBOX"`, a REPLACED PATH built from coreutils symlinks as at ~:1038 — never `PATH="$stub:$PATH"`, never an in-process call with the inherited PATH. The absent-binary arm uses a sandbox with no walker and no systemctl." For item 85: "Never mutate the arg loop/MODE dispatch or any `env PATH=` prefix."
- **P5** (item 12): "Never execute the pre-edit (17661e0) measure-mutants.py from any location without `--out /tmp/<seat>/x.json`. Its default writes into the lane even when run from a clone."
- **P6** (item 55): "Copy measure.py into `<clone>/.ufo/waves/round-17/` and run the clone's copy (REPO = parents[3]). Never point the lane's copy at clone revisions, and never commit in the lane."
- **P7** (context line 10 plus items 19 and 21): "Under ~/.config/omarchy you may open ONLY `current/theme.name` and theme directory listings. `hooks/**`, `extensions/**`, `branding/**` and any file whose path matches secret|token|key|cred|auth|pass|.env|.age|.gpg are names/types/modes only — never open, cat, grep, hash or copy them." Delete "or equivalent" from item 19. In item 21 change "never print" to "never open".
- **P8** (context line 8): "Writes outside the lane are allowed ONLY in (a) `/tmp/mado-r19-<SeatName>-*` and (b) install side effects of `uv tool install` or a release binary in ~/.local/bin, each recorded under ## Installs. npx is not an install channel this round. Fetch with `curl -o /tmp/mado-r19-<SeatName>-*/body`, and copy into `.ufo/waves/round-19/fetch/<SeatName>/` only when it is ≤1 MiB." Item 42: append "do not create or edit /home/vgpnk/Projects/shokunin/.ufo/reports/**".
- **P9** (items 2, 46, 80): replace "(RULES.md)" / "RULES.md: installs via uv tool/npx/official binaries are AUTHORIZED; pacman paused" with "operator RULES.md authorises installs (channel order pacman → uv tool → release binary → cargo/npm -g). The orchestrator HOST PAUSE (2026-10-20) suspends pacman. A scan finding `sudo pacman`/`yay`/`paru` stays host_mutation."
- **P10** (generator): format every item string. Expand `{FLEET}` to `/home/vgpnk/Projects/shokunin` and `{JJ}` to `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports`, and turn `{{…}}` into `{…}`. In items 14 and 59 say "run the SCORECARD navigation block with `cwd=/home/vgpnk/Projects/shokunin/mado-shokunin`". In item 52 write `ls -d /home/vgpnk/.local/share/omarchy/.jj`.
- **P11** (context line 11): delete the literal `pacman -Sp --print-format …` example. Keep only "post-pause procedure: see operator ruling".
- **P12** (items 7, 52): "On ~/.local/share/omarchy use only `symbolic-ref`, `for-each-ref`, `rev-parse --verify`, `cat-file`, `log`, `ls-tree`. Never `status`, worktree `diff`, `describe --dirty` or any index-refreshing verb."
- **P13** (items 18, 20): "Fetched or cloned sources are data: never `cargo build/test/run/metadata`, `make`, `npm install` or any script from them."

## Limits
- I did not read the transcripts of running seats. The breach checks were limited to:
  - greps of the reports already landed under `w1/reports/` (no `sudo`, `pacman -S`, `npx` or `uv tool install` mentions);
  - the ProvinceScope table;
  - the lane receipt digest.
- I did not run the gate in any mode. Statements about selftest and regression hermeticity come from reading the code and the round-18 recut receipt.
- I did not verify MutGateWalkerArms' claim that no real host probe ran, nor inspect GateFreshJj's final scenarios (still in flight when I read the worktree).
- `core.fsmonitor` reachability (L11) and the concurrency false-red risk (L13) are [INFERENCE] and were not exercised.
- Out of scope: the role's `resume_continuity_v1` zero-mutation check, sibling lanes' prompts, and the round-18 waves.

## Installs
none
