# SentinelCommitSet — holds

I attacked commit range `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d..01b80946d92b26370d3012a7da655d00dd135154` and found no secret, IP address, private email or out-of-suite symlink. The 7 added symlinks are exactly the `f2-*` fixtures, and every target resolves inside the suite. No body in a digest-only class is committed.

The range is already public. `origin/master` is `01b8094…`, and the GitHub API reports the repo as `"private":false` with master at `01b80946d92b26370d3012a7da655d00dd135154` (receipts below). So a leak in the range would have been unrecoverable. None was found.

I found one LOW forward-risk gap in the `fetch/.gitignore` design (F1) and three INFO notes.

## Scope / commit set
- `git diff --name-status --no-renames 9c54c56 01b8094` lists **293 paths: 272 added, 21 modified, 0 deleted**.
- `git diff --raw` modes:
  - 273 × `100644`
  - 13 × `100755`, all scripts: `round-19/*.py|*.sh`, `round-18/measure-mutants.py`, `tools/mado-tripwire.py`, `tools/mado-verify.sh`
  - 7 × `120000`
- Commits:
  - `17661e0` pre-registration
  - `df84807` wave-1 integration
  - `01b8094` tripwire merge
- All three are authored and committed as `mado-shokunin <mado@shokunin.local>`, unsigned (`%G?`=N).

## Attack 1 — gitleaks on a /tmp clone
`git clone --no-local <lane> /tmp/scs-clone && git checkout 01b8094`, then:

| scan | result |
|---|---|
| `gitleaks git --log-opts="9c54c56..01b8094"` | 3 commits, ~2.72 MB, **no leaks**, rc 0 |
| `gitleaks dir /tmp/scs-clone/.ufo/waves/round-19` (committed tree) | ~2.60 MB, **no leaks**, rc 0 |
| `gitleaks git` (all 68 commits) | 1 finding: `generic-api-key` in `.ufo/waves/round-13/w1/reports/ProtocolPhases.md:25`, commit `95cbc41`. `git merge-base --is-ancestor 95cbc41 9c54c56` → it predates the baseline, so it is **out of range** |
| `gitleaks dir <lane worktree>/.ufo/waves/round-19` | 8 `generic-api-key`: `auth_hydro_click_hmac` (line 349) and `uploadToken` (line 508) in `fetch/HtmlAnchorSweep/s094-tree-{a,b}-{1,2}.html`. All 4 files are untracked **and** `git check-ignore` matches them, so the ignore list works for these |

## Attack 2 — grep added lines (35,841 `+` lines from `git diff -U0`)
- **IPv4 / IPv6 regex** (full and `::`-compressed forms): **0 hits**.
- **The operator IPv6 itself.** I read it in-process, without printing it, from the 3 withheld bodies in `/tmp/html-anchor-sweep-withheld/` (mode 0600). I then searched for the full address and for its 2-, 3- and 4-hextet prefixes, case-insensitive. **0 hits** in:
  - every blob of tree `01b8094` (1,943 files)
  - `git log -p --all`
  - the whole lane worktree, including untracked files
- **`X-Real-Ip|X-Forwarded-For|cf-connecting-ip|true-client-ip`:** 13 hits. All are field names in prose, with no value:
  - `fetch/HtmlAnchorSweep/WITHHELD.md:5`
  - `gen_w2.py:131`
  - `w1/reports/SentinelVcsFixtures.md:29,32,43,157`
  - `corpus/lessons/round-19.md:21` (M6 row)
- **Emails:** 14 hits. All are public or fixture identities:
  - `app-walker@autostart.service` ×11, a systemd unit name
  - `pkgs@omarchy.org`, the Omarchy package `%PACKAGER%` at `w1/reports/HostWalkerBytes.md:56`
  - `mado@shokunin.local` at `w1/reports/JjIncidentScan.md:160`

  The real-name email `jpveigao10@…` exists only on 3 pre-baseline commits. It is in no added line and no range commit.
- **Token patterns** (`ghp_`, `github_pat_`, `sk-`, `AKIA`, JWT, `Bearer`, PEM, `hmac`, `uploadToken`, `nonce`, `csrf`): 15 hits.
  - **14** are prose in `w1/reports/SentinelVcsFixtures.md` and `HtmlAnchorSweep.md` describing classes without values. For example, `:75` `BEGIN PRIVATE KEY` describes a grep pattern.
  - **1** is `frozen/inputs/r13-root.jsonl:2` `sk-nniw…`, a substring inside a base64 provider-ciphertext blob (the `sk-` comes from `…QpMe8sk-nniwPx…`). The same line is in `.ufo/waves/round-18/frozen/inputs/r13-root.jsonl:2` at `9c54c56` (`git grep`).
- **Auth/trace headers** (`authorization:`, `x-request-id`, `cf-ray`, `x-amz`, …): 0.
- **`w1/task-result.json`** (477 KB, the largest added blob): 0 hits for `agent.db`, `auth.json`, `.ssh/`, `credentials`, `oauth`, `X-Real-Ip`, PEM, `ghp_`, `AKIA` or non-fixture emails.

## Attack 3 — transcript bytes in the commit set
- **Re-pinned frozen inputs.** `round-19/frozen/inputs/*.jsonl` has 26 lines. Every one carries `credentialId`, plus `providerPayload`/`thinkingSignature`/`encrypted_content`, real `call_<hex>|fc_<hex>` ids and long ciphertext.
  - **All 26 are byte-identical to lines already committed at `9c54c56`**, the round-18 frozen inputs. I checked this with a set-membership test against `git grep -h` of round-13/17/18 at baseline.
  - All have role `assistant`. There are no `user` or `toolResult` lines, so the round adds no new transcript bytes.
- **Tripwire suites.** The 340 other added `.jsonl` lines (`round-19/tripwire/**`) are new but synthetic:
  - 0 real `call_<24+ hex>`, `fc_`, `rs_` or `thinkingSignature`
  - 254 carry a `2026-…` timestamp
  - 10 carry a `/home/vgpnk` path, which is pre-existing public in the lane
  - The one `toolResult` line (`tripwire/r19-vcs/mention-and-data-clean.jsonl:6`) is a hand-built fixture: `toolCallId":"call_m3"`, text `git commit -m x\njj commit`.
- **Host hooks/extensions bodies.** One hit only: `evidence/gate-swap-d9a5a18.sh` names the path `…/omarchy/hooks/battery-low.d`. It is a path string in the gate copy, not a body.

## Attack 4 — symlinks
`git diff --raw … | awk '$2=="120000"'` gives exactly 7, all under `.ufo/waves/round-19/tripwire/r19-frozen-f1f2/`:

| link | target (`git cat-file -p`) | `readlink -m` (lane-relative) |
|---|---|---|
| `f2-ancestor-symlink` | `.` | `…/r19-frozen-f1f2` |
| `f2-dotdot/link` | `../f2-outside/deep` | `…/r19-frozen-f1f2/f2-outside/deep` |
| `f2-outside/evil` | `../f2-target` | `…/r19-frozen-f1f2/f2-target` |
| `f2-symlink-dir-dot` | `f2-target` | `…/r19-frozen-f1f2/f2-target` |
| `f2-symlink-dir-dot-slash` | `f2-target` | same |
| `f2-symlink-dir-inputs-dotdot` | `f2-target` | same |
| `f2-symlink-dir-plain` | `f2-target` | same |

- No target is absolute and none leaves the suite.
- The other 4 symlinks in the tree (round-17 hardening, round-18 frozen) predate the range.
- `find .ufo/waves/round-19 -type l` on the worktree lists the same 7.

## Attack 5 — committed fetch bodies vs the `.gitignore` digest-only list
`round-19/fetch/.gitignore` (tip blob `da0a606`) has 29 exact-path entries and 1 comment line.

- **Committed bodies under `round-19/fetch/`.** Only upstream source text is committed:
  - `DeltaWalkerCli/v2.17.{0,2}-{Cargo.toml,src_data.rs,src_main.rs}`
  - `DeltaWalkerConfig/resources-config-*.toml`
  - `SrcS084/walker-v2.17.2-{Cargo.lock,src-config.rs}`
  - `SrcS094/colors.toml`

  Everything else committed is receipts or `WITHHELD.md`. **No `.html`, `.crate` or API `.json` body is tracked** (`git ls-tree -r 01b8094 .ufo/waves/round-19/fetch/`).
- **Every on-disk HTML, crate or API-JSON body** from the committed sweeps is untracked and `check-ignore`-matched. That is all 28 such bodies across CriticC1, DeltaWalkerCli, FrontierRows, HtmlAnchorSweep, MadoR19.UnpinnedUrlSweep and SrcS084.
- **Receipt → body mapping** over all 8 committed `receipts.jsonl`: every body is TRACKED or IGNORED except the 3 withheld bodies in F1.

## Findings

### F1 — LOW (forward risk; nothing leaked at the tip): `fetch/.gitignore` lists exact paths, not the digest-only classes its header names
- **Evidence**
  - `fetch/.gitignore:1` says the digest-only classes are "HTML with per-fetch tokens, crate archives, API JSON". Lines 2–30 are fixed file paths only, with no `*.html`, `*.crate` or `*.json` pattern.
  - In the current worktree, `.ufo/waves/round-19/fetch/RevRubricVRisk/xdg-3.0.0.crate` (15,821 B, a wave-2 seat's file) is **untracked and not ignored**: `git check-ignore -q` → rc 1. So are its siblings `receipts.jsonl`, `walker-v2.17.2-Cargo.lock` and `omarchy-v3.8.4-matte-black-colors.toml`.
  - The 3 withheld bot-challenge bodies `HtmlAnchorSweep/s061-archwiki-oldid-{1,2,3}.txt` are named by `fetch/HtmlAnchorSweep/receipts.jsonl` lines 13, 14 and 19 (`http_status` 200, no `retain` key). Their paths are **not** in `.gitignore`, and no round-19 `RETENTION.json` exists (`find .ufo/waves/round-19 -iname '*retention*'` → empty). The lane is protected today only because the files sit in `/tmp`.
- **Exploit path.**
  - A wave-2 integration runs `git add .ufo/waves/round-19` and pushes to the **public** `VeigaPunk/mado-shokunin`. That commits a crate archive, against the digest-only rule.
  - Separately, re-running the HtmlAnchorSweep `oldid=` fetch into the lane would write three new Anubis challenge pages with the operator's IPv6 under paths nothing ignores. The same "nothing ignored" condition that w1 `SentinelVcsFixtures` rated HIGH would then recur.
  - gitleaks does not catch IPs (w1 report; consistent with Attack 1 rc 0 on bodies with no IP).
- **Overclaim.** `corpus/lessons/round-19.md:21` (M6) says `fetch/.gitignore` "keeps all HTML/crate/API bodies digest-only". That is true only for the set of files present at commit time. It is not a class rule.
- **Smallest remediation.** Append class globs to `.ufo/waves/round-19/fetch/.gitignore`:

  ```
  *.html
  *.crate
  *-api.json
  /HtmlAnchorSweep/s061-archwiki-oldid-*
  ```

  Optionally, add `"retain":"digest-only"` to receipts 13, 14 and 19.

### F2 — INFO: directory loop from `f2-ancestor-symlink -> .`
- **Evidence:** `grep -R -l zzzz_nomatch .ufo/waves/round-19/tripwire/r19-frozen-f1f2` prints `grep: …/f2-ancestor-symlink: filesystem loop detected` and exits 2. `find -L` gives the same message.
- **Status:** the loop is intended (F2 fixture) and was already reported in w1 `SentinelVcsFixtures.md:107-109`. A grep of `tools/` and `.ufo/waves/round-1{7,8,9}` scripts found no lane tool using `followlinks=True`, `grep -R`, `find -L` or `rsync/cp -L`. The `find -L` hits are in fetched upstream omarchy bodies and in report prose.
- **Impact:** only a future symlink-following scanner. No escape.

### F3 — INFO: re-pinned frozen inputs re-commit provider ciphertext and `credentialId` fields
The 26 lines are byte-identical to `9c54c56` (Attack 3), so nothing new is exposed. Each re-pin round does add another copy of the same ciphertext to history. [INFERENCE] Only the issuing provider can use it (w1 report, same position).

### F4 — INFO: `/tmp` copies of the IPv6-bearing bodies still exist
`/tmp/html-anchor-sweep-withheld/s061-archwiki-oldid-{1,2,3}.txt` are mode 0600, outside the lane. w1 remediation item 2 says to delete them after L1. That is outside the lane, so I did not delete them.

## Fetch receipts (curl, no auth; bodies in /tmp only)
| url | http status | bytes | sha256 | fetched_at |
|---|---|---|---|---|
| `https://api.github.com/repos/VeigaPunk/mado-shokunin` | 200 | 5702 | `0e4a1d5e3804f4513d997d2d670382e4d579dedbf4615f179ca5b0787f796be5` | 2026-10-20T18:05:22Z |
| `https://api.github.com/repos/VeigaPunk/mado-shokunin/commits/master` | 200 | 628090 | `df1390b8252ee17052657b8180d5a16cd8611520e5f2ddcc8f4b01b89b736869` | 2026-10-20T18:05:26Z |

Results: `private:false`, `visibility:public`, `pushed_at 2026-10-20T18:01:56Z`, and master `sha` = `01b80946d92b26370d3012a7da655d00dd135154`. These are API JSON digests, used only as a visibility observation and not as anchors.

## Limits
- gitleaks used its default ruleset. It does not detect IP addresses or PII, so IPs and emails were covered by my regex sweeps, and the IPv6 by an exact search for the one known address. [UNK] Another operator-identifying value that is not an IP, email or token shape (for example a geolocation string) would be missed by both. I sampled no geolocation keys.
- The email regex sweep counts only `+` lines in the range diff. It does not cover pre-baseline history, apart from what gitleaks `git` covered.
- I did not attempt licence review of the committed upstream source bodies.
- The RevRubricVRisk files are wave-2 worktree state, outside the attacked range. F1 is a forward risk, not a defect in the committed bytes.
- Scratch: `/tmp/scs-clone`, `/tmp/scs-gl-*.json`, `/tmp/scs-repo.json`, `/tmp/scs-master.json`. No lane writes besides this report, and no git or jj writes in the lane.

## Installs
none. `/usr/bin/gitleaks` was already present; its `version` subcommand prints "version is set by build process", so the version is [UNK].
