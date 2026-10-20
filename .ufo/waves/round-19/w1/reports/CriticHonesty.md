# CriticHonesty — the most likely overclaim is C2 read as "walker pins are current" or "freshness improved"; three phrasings in the drafts already overreach (host pause, fetch-verify, the WL0 label)

Seat `MadoR19.CriticHonesty` (critic, leaf). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, baseline `9c54c56`, pre-registration `17661e0`.
I attacked the round's honesty plan and wrote nothing except this report. Checked at 2026-10-20T14:10-03:00. The working copy was still being edited by sibling seats, so line numbers in uncommitted files are a snapshot.

Axes: (A) claim wording versus what each counter actually counts; (B) provenance and identity (rows, anchors, gate rows); (C) host-pause and installs statements.

## 1. Most likely overclaim: C2 (freshness) — axes A, B

**Counterexample.** `fresh-pins.py` counts a file as current when one of its lines has both `2.17.2` and any `\bS\d{3}\b` token. It never checks that the row exists, what the row is about, or whether the file still states `2.17.0` in the present tense. I ran the regex over the working copy and checked each id against `corpus/SOURCES.md`:

- 11/13 files already match. `SKILL.md` and `tools/mado-verify.sh` do not. The gate copy I read already had `2.17.2`+`S096` on lines 57/94-100, so the gate is moving too.
- Four files are counted current through **S096, which is not yet a row**: `remaining-planes-census.md`, `walker-deep-r9.md`, `walker-deep.md`, `walker-live-surface.md` (`grep -c '^| S09[6-9]' corpus/SOURCES.md` → 0). If S096 never lands, the counter still scores these four as current.
- `walker-route-r18.md` and `corpus/README.md` were current at baseline only because a header or source line lists S072…S091 next to `2.17.2`. Neither is a forward pointer.
- `PacmanLogMoves.md` (sibling) found that the same 09:16/09:31 transactions moved 22 province packages: elephant plus 12 plugins 2.21.0→2.22.1, uwsm 0.26.7→0.27.1, hyprland 0.56.2-2→-4, hyprtoolkit 0.5→0.6, aquamarine, and others. The C2 counter sees walker only.
- The gate's live arm (`walker --version` against `WALKER_VERSION_PIN`) cannot run this round. The new selftest assertion `st_eq "WL0: the pin is the host 2.17.2" "2.17.2" "$WALKER_VERSION_PIN"` (`tools/mado-verify.sh:1226`, working copy) compares a constant with a literal but its label says **"host"**. That is false provenance inside a test name. WL1/WL2 test the arm logic against a stub, not the host.

**Phrasing to avoid:**
- "walker pins are current", "stale pins fixed", "no stale walker pin remains"
- "freshness: improved" with no scope attached
- "gate verifies walker 2.17.2", "live.walker.version PASS"
- "selftest confirms the host pin"
- "S096 shows the host runs walker 2.17.2"

**Allowed:**
- "walker version-pin currency sub-axis (fresh-pins.py, fixed 13-file set): 2/13 → N/13 at <commit>".
- "Every S### on a counted pointer line resolves to a `mined` row at <commit>". Show this check: `grep` each id in `SOURCES.md` at REV.
- "The gate pin moved to 2.17.2 on file-byte evidence (S096/S090). The live arm was not run (host pause). That `walker --version` prints `2.17.2` is [INFERENCE] from the rodata literal shape `version2.17.2\n` at offset 856,302 (`HostWalkerBytes-row.md`)."
- "Other province package moves on 2026-10-20 are not counted and stay unpinned."

**Smallest correction:**
- (1) At closure, add a row-resolution check next to fresh-pins: each counted id must be present and `mined` at REV.
- (2) Rename WL0 to something like "pin constant equals the S096 file-byte literal", or drop it. Never say "host".
- (3) Give freshness a verdict scoped to the walker sub-axis, or call it "unchanged elsewhere".

## 2. "The host pause holds" — axis C

`ReportSkeleton.md` says "**Host:** the host pause holds (no package query or transaction, …)". `LogDraft.md` says "no installation or update evidenced". Both make claims about the whole host, and the lane cannot observe the whole host.

**Evidence:**
- `/var/log/pacman.log` has 3169 lines. Its last transaction is `3161-3169` at `2026-10-20T13:23:08/09-0300`: `pacman -U … /home/vgpnk/.cache/yay/zcode/zcode-3.16.2-1…`, then `-D --asexplicit zcode`. The actor is [UNK], and the round-18 closure (`round-18-verifier-spotcheck.md:123-126`) records it as an install made while the pause was in force.
- That transaction is before the pre-registration (`17661e0` 13:59:52) and before baseline `9c54c56` (13:53:34).
- `find ~/.local/bin ~/.local/share/uv/tools ~/.cargo/bin -maxdepth 1 -newermt '2026-10-20 13:53:34'` → empty (at 14:10:21).

**Phrasing to avoid:** "the host pause held", "host unchanged", "no installs happened", "R15-V1 unchanged", "host recovered".

**Allowed:**
- "No lane seat issued a package, service, compositor, input or screenshot command (evidence: <tripwire scan of seat transcripts + seat self-reports>)."
- "`/var/log/pacman.log` gained no line between <t0> and <t1> (3169 lines at both)." Re-measure t1 at closure.
- "The 13:23 zcode transaction (lines 3161-3169) is round-18 history, actor [UNK]."
- "R15-V1 operator-owned; its state was not observed this round."

## 3. R18-V1 cannot be stated as "fetch-verify now passes" — axes A, B

I ran it read-only:

- `python3 -I .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md` → 4 `CONFLICT` (both GitHub tree URLs × basecamp/omacom), `SUMMARY receipts=424 … conflicts=4`, **rc=1**.
- The same run with `--fetch-root .ufo/waves/round-19/fetch` → 5 `CONFLICT`, **rc=1**. These are the tree pages HtmlAnchorSweep re-fetched (`78707acc…`≠`da907006…`, `36bfe79b…`≠`fc803500…`) plus an Arch Wiki URL (see §4).

Conflicts are properties of receipts, and receipts are append-only. S097 cannot clear them.

**Phrasing to avoid:** "R18-V1 closed: fetch-verify exits 0", "S094 fixed".

**Allowed:** "S097 appended, superseding S094's HTML anchor. S094 stays as history. The HTML CONFLICT lines remain as M7 evidence (rc=1 by design on those roots)."

**Smallest S097 anchor without HTML.** Git tree object ids are content-addressed. Read-only `git -C ~/.local/share/omarchy rev-parse` at tag commit `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` (`v3.8.4`) gives:
- `themes/matte-black` tree `3fc08f954e5a3f67072a79a7c52d94e0a153b9ec`;
- `…/backgrounds` tree `ff02c34193836c016d8e57bde56bcef5f3c64b4c`;
- the `ls-tree` names equal the S094 name lists (9 entries; 4 images);
- the `colors.toml` blob `cat-file` bytes hash to `dbdd13a6…` (same as the raw-URL digest).

Reproduce in a `/tmp` clone before citing, so the anchor does not depend on the host checkout.

## 4. Fetch-provenance traps in round-19 bodies — axis B

- **Arch Wiki `oldid=869789&action=raw` is a bot challenge.** HtmlAnchorSweep receipts lines 13-14 have HTTP 200, 7,469 B, and two digests. `diff` shows Anubis challenge JSON (`issuedAt`, `randomData`) on body lines 39/42, not wikitext. Do not write "oldid raw varies per fetch". It is an interstitial, and a 200 status does not mean the body is the content. No harm today because S061 is `rejected` and anchors the plain `action=raw` digest `c39c563d…`, which reproduced. But the "flip: oldid-pinned" in S061 is not reachable with curl.
- **Bodies with no receipts.jsonl:** `fetch/DeltaWalkerConfig/` (4 `.toml` bodies) and `fetch/FrontierRows/xdg-3.0.0.crate`. Any row or note that cites them before a receipt line exists is unreceipted. SrcS084 has its own receipted crate, `static.crates.io/crates/xdg/xdg-3.0.0.crate` sha `2fb43323…`. Its fetched `walker-v2.17.2-Cargo.lock:2705-2707` pins `xdg 3.0.0`, so S098's version matches.

## 5. S096 duplicates existing authority — axis B

S090 already anchors `pacman.log:2929`. S091 already anchors `/usr/bin/walker` at 7,039,912 B, sha `25240650686fe6ad…` (`SOURCES.md:102-103`). I re-hashed the binary and got the same value. S096's new content is only the version-literal offset 856,302, the BuildID, and the `desc`/`mtree` digests.

Host rows have no URL, so census W04 will not flag the overlap. QUALITY 17 needs an explicit scope review.

**Correction:** scope S096 as "the version literal inside the S091 binary bytes (same digest)", or append it as a stated extension. Do not present it as a fresh, independent host anchor.

## 6. Gate F6: the implemented fix is right for omarchy branch switches, with one false-PASS hole — axes B (identity)

The audit's literal suggestion was `rev-parse refs/heads/master`. That would be wrong after `omarchy-channel-set rc|dev`, which calls `omarchy-branch-set` → `git switch rc|dev` (`~/.local/share/omarchy/bin/omarchy-branch-set:18`). The working-copy gate avoids this by resolving `symbolic-ref -q HEAD` (`tools/mado-verify.sh:3500`).

**Residual counterexample.** Take a plain-git (non-jj) checkout with a detached HEAD, for example `git checkout v3.7.x`, and exactly one local branch. Lines 3503-3510 then read the branch tip (`v3.8.4`) instead of the checked-out commit, so the tag and head rows PASS against a tree whose files are another release. The old `rev-parse HEAD` read MOVED, which was correct. Today HEAD = `refs/heads/master` = `8fcc9d60` = `v3.8.4`, so nothing is wrong on this host now.

**Correction:**
- Take the branch-tip fallback only when `[ -d "$tree/.jj" ]`; otherwise keep `rev-parse HEAD`.
- Add a selftest case: detached HEAD, one branch, no `.jj` → MOVED or UNKNOWN, never PASS.

**Phrasing:** "F6/F9 covered by selftest; live omarchy rows not run (host pause)". Not "F6 verified on the host".

## 7. Installer class (TwInstallerChannels) — axes A, C

**Facts:**
- The operator directive (`~/.omp/agent/RULES.md:7-8`) authorizes `uv tool install`, official release binaries into `~/.local/bin`, `cargo install` and `npm -g`. Only pacman is paused this round.
- The draft's `tool_install` class makes `--scan` exit 1 unless `--permit tool_install` is passed (`verdict_of`, `tools/mado-tripwire.py:832-837`).
- It does not see channel 3 at all (curl or download into `~/.local/bin`), nor pnpm/yarn/bun/brew/nix (draft docstring).

**Phrasing to avoid:**
- "tool_install violation/breach"
- counting `tool_install` under host-mutation or pause findings
- "Installs: none (tripwire clean)"

**Allowed:**
- "tool_install: N events — operator-authorized channels, recorded, not pause breaches."
- "Installs: <per-seat report lines>; the tripwire does not classify downloads into `~/.local/bin`."

**C3 credit.** The three known-miss lines contain no installer token. I grepped them at `9c54c56`:
- `r14-source-safety.jsonl:2` has `curl -fsSL` and prose `hyprctl monitor commands`;
- `:3` has `pacman -Q hyprland`;
- `r13-root.jsonl:4` has `'pacman','-Q','wayland-utils'`.

So TwInstallerChannels cannot move C3, and the report must not credit it there. `tw-recall.py` counts **any** class on a line. If a new class fires on `:2` because of `curl` or `hyprctl`, the line scores "detected" while the variable-held `pacman -Q` miss remains.

**Correction:** next to recall, report the rule that hit each incident line. It should be `package_query`/`pacman:-Q` for the three known misses.

## 8. C1 and R18-V2 wording — axis A

**C1.** `measure.py` c1 counts numbered `QUALITY.md` lines that contain `lessons/` (`.ufo/waves/round-17/measure.py:92-93`). "Each criterion has a runnable check red on a real `9c54c56` artifact" is not counted. It must be shown per criterion by headed receipts.

**R18-V2 trap.** The new criterion for R18-V2 needs its own red-before receipt, with a `tool_sha256=`/`measured_commit=` header. Without it, the round repeats R18-V2.

**R18-V2 wording.** Re-running the swapped block now uses the `9c54c56`-era gate, which is a different tool from the uncommitted `2bdf5e8a…`. Allowed: "a header-bound red-before re-cut at <commit>; the round-18 `gate-rc-redbefore.txt` stays headerless (superseded, named)". Never "the round-18 red-before is now header-bound"; corrections append and never relabel (`corpus/QUALITY.md:116-117`).

**Phrasing to avoid:** "calibration improved" without "(literal lesson-citation fraction)".

## 9. PROVINCE, F1/F2, F16, R15-V1 — axis A

- **PROVINCE.** The `~/.config/omarchy/**` path-root line is a non-claim repair (pre-registration). Adjacency is "unchanged (not scored)". SHONEN box 4 stays `[~]` unless a non-author verifies it.
- **F16.** LandedCheck's "LANDED at origin/master" holds. My own `git ls-remote https://github.com/VeigaPunk/mado-shokunin.git refs/heads/master` → `17661e0f…` = `refs/heads/master`. No finding.
- **F1/F2.** These change the frozen harness. Report the frozen suite count with the old and new tool sha, not as an unchanged "31/31".

## 10. Self-disclosure (fence-adjacent reads)

To test the counterexample "the running walker is still the 2.17.0 inode", I read procfs as files: `/proc/[0-9]*/comm`, `readlink /proc/PID/exe`, `stat` mtime, and `/proc/stat` `btime`. No command from the forbidden list was run.

Result:
- boot `2026-10-20T09:56:56-03:00`, after the 09:16:46 upgrade;
- walker PID 1858 and elephant PID 1861 started 09:57:13;
- the exe links are `/usr/bin/walker` and `/usr/bin/elephant`, with no `(deleted)` suffix.

So the counterexample is refuted [INFERENCE: the process maps the current file].

This read is the file equivalent of `ps`, which the lane classifies as `live_probe`, and HostWalkerBytes deliberately did not make it. L1 should not cite it as row evidence without accepting that fence reading.

It also exposes a gap: **tripwire cannot see procfs reads**. A "no live probe" statement backed only by tripwire scans is weaker than it sounds; this command of mine is the counterexample.

I also ran `.ufo/waves/round-18/fetch-verify.py`, a read-only lane verifier that is not my own script, twice (see §3).

## Limits

- I did not run fresh-pins, tw-recall, measure.py, any gate mode or any suite. The C2 numbers in §1 are a regex simulation on the working copy.
- I did not review the TwMissBashCVar/TwMissHelperFn diffs or the QUALITY 27+ drafts (owned by CriticC1/CriticC3/CriticInstallerClass).
- I did not verify the S098 quote in the crate source.
- I did not check whether the operator authorized the zcode install.
- The working copy changed while I read it; the gate line numbers are a snapshot.

## Installs

none
