# SentinelVcsFixtures — real jj/git transcript lines carry no credential, but must never be committed verbatim; one HIGH leak (operator public IPv6 in 3 ArchWiki bot-challenge bodies) was contained in-flight; crate tarballs and HTML stay digest-only

Scope: commit safety of (a) tripwire fixtures derived from real OMP transcripts (jj/git commands) and (b) the round-19 fetch tree `.ufo/waves/round-19/fetch/`. Snapshot taken 2026-10-20 ~17:05–17:14Z, while sibling seats were still writing. Lane remote tip `17661e0fa83f…` = `refs/heads/master`. The repo is **public**: a logged-out GET of `https://github.com/VeigaPunk/mado-shokunin` returned 200.

Axes: secrets/tokens · host and operator identity · licence/redistribution · provenance honesty · tree hygiene (symlinks, slugs, ignore coverage).

## Verdict table (per artifact class)

| Class | Example paths | Recommendation | Basis |
|---|---|---|---|
| T1 Real transcript lines, verbatim (assistant toolCall jj/git) | `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/**` | **Do not commit.** Use synthetic fixtures, or the round-18 `mado-transcript-projection-v1` projection with provenance digests. | F2 |
| T2 Real toolResult / custom lines | same | **Never commit.** | F3 |
| T3 Synthetic OMP-shaped fixtures (`r19-frozen-f1f2`, planned `r19-vcs`) | `.ufo/waves/round-19/tripwire/**` | **Commit.** Use synthetic ids, no real call ids, gitleaks clean. | F5, F6 |
| T4 Re-pinned round-19 frozen baseline built from the round-18 inputs | `round-18/frozen/inputs/*.jsonl` → new DIR | **Commit.** No new exposure: these bytes are already public at `9c54c56`. Add no new real lines unless they are screened. | F2 |
| R1 Tag- or commit-pinned raw GitHub text (walker `Cargo.lock`, `Cargo.toml`, `src/*.rs`, `resources/config.toml`; omarchy `colors.toml`) | `fetch/{SrcS084,DeltaWalkerCli,DeltaWalkerConfig,SrcS094}/*` | **Commit.** The licence bodies for these refs are already committed (round-18 `FetchBodyPolicy`). gitleaks is clean. Rename 3 slugs. | F7 |
| R2 crates.io `.crate` tarballs | `fetch/SrcS084/xdg-3.0.0.crate`, `fetch/FrontierRows/xdg-3.0.0.crate` | **Digest-only (D3).** The receipt plus the committed `Cargo.lock` checksum line are the anchor. | F4 |
| R3 HTML pages (GitHub tree, docs.rs, wiki.hypr.land, third-party blog) | `fetch/{HtmlAnchorSweep,CriticC1,MadoR19.UnpinnedUrlSweep}/*.html` | **Digest-only (D1/D2).** | F8 |
| R4 Bot-challenge bodies holding a client IP | `fetch/HtmlAnchorSweep/s061-archwiki-oldid-{1,2,3}.txt` (now withheld) | **Never commit, never credit.** Delete the withheld /tmp copies once digests are recorded. | F1 |
| R5 ArchWiki wikitext and API JSON (GFDL) | `s061-archwiki-raw.html`, `s061-archwiki-api.json` | **Digest-only (D2).** | F8 |
| H1 Host walker binary bytes (S096) | `/usr/bin/walker` | **Digest plus offsets only.** No ELF is present in round-19. | F9 |

## Findings

### F1 — HIGH (contained): ArchWiki "raw" fetches returned Anubis bot-challenge pages that embed the operator's public IPv6 address

**Evidence**
- `fetch/HtmlAnchorSweep/s061-archwiki-oldid-{1,2,3}.txt` came from receipt lines 13, 14 and 19. The URL was `https://wiki.archlinux.org/index.php?title=Alacritty&oldid=869789&action=raw`, with `http_status` 200 and 7,469/7,469/7,468 B.
- The bodies are not wikitext. Each begins `<!doctype html>…<title>Making sure you&#39;re not a bot!</title>`.
- Each carries `"challenge":{"issuedAt":…,"metadata":{"User-Agent":"curl/8.23.0","X-Real-Ip":"<operator IPv6>"}` — a full residential IPv6 address. I reproduce neither the value nor its prefix here.
- Three fetches gave three digests (`e7983df2…`, `2e04311c…`, `fda76acf…`). The only difference is the challenge `issuedAt`/`id`/`randomData` block (diff at line 42–45).
- The file named `s061-archwiki-raw.html` is actually the real wikitext. It begins `[[Category:Terminal emulators]]`, so its suffix is the wrong way round.
- Sweep: `grep -rlE 'X-Real-Ip|X-Forwarded-For|"remote_?addr"'` and a fixed-string grep for the address's first two hextets, run over the round-18 and round-19 fetch trees, `corpus/` and `tools/`, matched only these 3 files. `git grep` for the same strings at `17661e0` found nothing, so the address is not in any landed commit. Broader client-IP keys (`client_ip`, `cf-connecting-ip`, `true-client-ip`) gave 0 hits.

**Exploit path.** L1 runs `git add .ufo/waves/round-19` and pushes. Nothing ignores this tree: `git check-ignore` rc 1, with 51 untracked paths. The operator's home IP, with geolocation to the ISP and region, and a timestamp then become permanently public in git history. Separately, the receipts say 200, so `fetch-verify.py` criterion (a) treats a challenge page as a creditable body. Its CONFLICT rule would also report "oldid instability" that is really a per-request nonce, which would falsely support the R18-V1 durable-anchor criterion.

**Impact.** Operator PII leak (irreversible once pushed), plus a misleading anchor-durability datum.

**Status / remediation**
- I messaged `MadoR19.HtmlAnchorSweep`. It moved the 3 bodies out of the lane to `/tmp/html-anchor-sweep-withheld/` (dir 0700, files 0600). It left `fetch/HtmlAnchorSweep/WITHHELD.md` and states in its report that the variance is the Anubis nonce. I re-checked afterwards: the prefix grep over `.ufo/waves/round-19` gives no hits.
- Still required from L1:
  1. Classify the receipts digest-only and never-credit. Either add a round-19 `fetch/RETENTION.json` entry (class `bot-challenge`), or give the receipt a `"retain":"digest-only"` field. Lines 13, 14 and 19 currently have no `retain`, so `fetch-verify` prints MISSING for them and exits 1.
  2. Delete the `/tmp` copies after L1 is done with them.
  3. Add a pre-commit grep for `X-Real-Ip|X-Forwarded-For|challenge":{` over `fetch/`. gitleaks does not flag IP addresses: rc 0 on these bodies before the move, because its 8 findings were elsewhere.

### F2 — MEDIUM (if committed verbatim): real jj/git toolCall lines are clean of credentials but are ~90% unrelated account and provider payload

**Evidence.** I scanned every `*.jsonl` modified since 2026-10-19 under the session root: 4,310 files, 3.56 GB, read-only. The selection was assistant `toolCall` items (bash `command`, eval `code`) that name a jj subcommand or a git write verb and mention `mado-shokunin` in the command or cwd.
- **223 lines in 100 files** (213 bash, 10 eval). Top verbs: `git:add` 76, `git:commit` 73, `git:clone` 47, `git:checkout` 44, `git:config` 30, `git:push` 18, `jj:log` 12, `jj:config` 9. Nine of the lines are `jj-lane.sh` helper calls.
- **Secrets:** 0 hits in the commands for credential URLs (`scheme://u:p@`), `x-access-token`/`oauth2:`, `ghp_`/`github_pat_`, `Authorization`/`extraheader`/Bearer, token env vars (`GH_TOKEN`, `GITHUB_TOKEN`, `GIT_ASKPASS`, `CARGO_REGISTRY_TOKEN`), credential helpers, `.ssh`/`ssh://`/`git@host:`, private keys, `sk-`/`AKIA`/`AIza`, or JWTs. `gitleaks dir --redact` gave **no leaks** both over the 223 extracted command texts and over the 223 whole lines (2,500,811 B).
- **Identity:** every email in the commands is a lane or fixture identity: `ma***@shokunin.local` ×18, `pr***@shokunin.local` ×5, `*@example.invalid` ×4. Push targets are `git -C …/mado-shokunin push` or `git push -q origin master`. The only URLs are `file://` lane paths, public github/raw URLs and `example.invalid`.
- **Non-command payload in those same lines:**
  - `credentialId`, `responseId` and cost/usage: 223/223 lines.
  - Thinking plaintext: 200.
  - `providerPayload`: 125.
  - `thinkingSignature`/`thoughtSignature`: 70.
  - `encrypted_content`: 24.
  - `premiumRequests`: 27.
  - `/tmp` paths: 92.
  - Sibling-lane paths (`tameshi-shokunin` 45, `kumitate-shokunin` 2).
  - Command text is ~10% of line bytes (252,545 / 2,500,811).
- One candidate line, `…/MadoR18/MadoR18.SentinelFrozenPrivacy.jsonl:68` (14,043 B), carries the operator directive phrases "Passwordless" and `btrfs-overlayfs`.

**Exploit path.** Byte-exact copies are needed only because "frozen" inputs are pinned byte-exact. Committing these lines would publish account-slot profiling (`credentialId`, provider, `premiumRequests`) and provider reasoning ciphertext. The one line above would also republish the host's root-escalation and boot-fragility facts. The scanner reads only `content[].toolCall` (round-18 SentinelFrozenPrivacy F1/F3), so none of this extra payload adds coverage.

**Remediation (smallest).**
- Build `r19-vcs` from synthetic fixtures, as the TwVcsClass brief already says.
- If a real jj/git incident line must anchor recall, commit only its `mado-transcript-projection-v1` projection: `type`, `timestamp`, and the `toolCall` id/name/`command|code|language`. Pin `source_path`, `source_sha256`, `source_line` and `source_line_sha256` in `provenance.json`, as specified in round-18 `w1/reports/SentinelFrozenPrivacy.md` §Remediation.
- JjIncidentScan's report should hold ≤200-char redacted commands only, which is its brief. Its report was not yet written when I checked, so I did not scan it.

### F3 — MEDIUM (if committed): toolResult lines in the same 100 files contain test-vector secrets and many git identities

**Evidence.** A regex sweep over the toolResult lines of the 100 candidate files found:
- **Test vectors:** `MadoR17.SentinelTranscriptRead.jsonl:68` holds a fake `ghp_` token, the AWS documentation example access-key id and `https://bob:***@example.com`.
- **Identities:** 327 `user.email=…@shokunin.local`, plus `x`, `example.invalid`, `selftest` and `fixture.invalid` values. No personal domain appeared.
- **One false positive:** `BEGIN PRIVATE KEY` in the root session `2026-10-19T20-36-43-523Z_….jsonl:405` is a grep result quoting a sentinel regex, not a key.

**Exploit path.** None of these values is real. But committing any toolResult line holding the `ghp_`/AKIA vectors would make the fleet's own gitleaks gate fail [INFERENCE: GitHub push protection may block it too]. A `git config -l` or `jj config list` result line would expose whatever identity or remote is configured at that moment.

**Remediation.** Commit assistant toolCall lines only. This is the round-18 rule, and it still holds.

### F4 — LOW: the xdg crate tarball is safe and redistributable but redundant; keep it digest-only

**Evidence**
- `sha256sum`: the copies in `SrcS084`, in `FrontierRows` and in round-18 `SrcWalkerConfigPaths` are identical: `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`, 15,821 B.
- That digest equals `fetch/SrcS084/walker-v2.17.2-Cargo.lock:2708` `checksum = "2fb43323…585b5"` (`name = "xdg"`, `version = "3.0.0"` at `:2705-2706`).
- `tarfile` listing: 39 members, all regular files or dirs. No symlinks or hardlinks, no absolute paths, no `..`, no setuid/setgid bits, all mode 0644. Extraction in /tmp is therefore safe.
- Licence `Apache-2.0 OR MIT`, with `LICENSE-APACHE` and `LICENSE-MIT` inside the crate.
- `.cargo_vcs_info.json` gives `sha1 c0f6bc329b0fd92b015a55bcbbee72b2864fae4b`, repository `https://github.com/whitequark/rust-xdg`.
- `Cargo.toml` `authors` holds 2 personal maintainer emails.

**Why digest-only.**
- crates.io crates are immutable and content-addressed by the `Cargo.lock` checksum, which sits in a tag-pinned raw `Cargo.lock` that is itself committable. Anyone can re-fetch and verify, so a committed copy adds no verifiability.
- The archive carries 3 copies of bundled author PII, and text review and diff tools cannot see inside it (round-18 D3).

**Remediation.**
- Keep one receipt per seat and gitignore both `.crate` bodies.
- If S098 needs a line quote, fetch `https://raw.githubusercontent.com/whitequark/rust-xdg/c0f6bc329b0fd92b015a55bcbbee72b2864fae4b/src/base_directories.rs` and the LICENSE at that commit with receipts. Commit those text bodies (rule C1/C2) rather than extracting files from the tarball.

### F5 — LOW: the round-19 F2 fixture suite commits 7 symlinks, including a self-loop

**Evidence.** `find .ufo/waves/round-19/tripwire -type l`:
- `f2-symlink-dir-{dot,dot-slash,inputs-dotdot,plain} -> f2-target`
- `f2-dotdot/link -> ../f2-outside/deep`
- `f2-outside/evil -> ../f2-target`
- `f2-ancestor-symlink -> .`

`readlink -m` shows every target resolves inside `r19-frozen-f1f2/`, and none is absolute. `find -L . -maxdepth 6` reports 1 filesystem loop. `gitleaks dir --follow-symlinks` gave rc 0 and terminated. gitleaks without following gave no leaks.

**Exploit path.** Nothing escapes the repo. But any recursive consumer that follows links will re-walk the suite until its depth cap: `os.walk(followlinks=True)`, `cp -rL`, `rsync -L`, `tar -h` or a future fleet scanner. On `core.symlinks=false` checkouts the links become text files, which silently changes what the cases test.

**Remediation.**
- Keep the links: they are the point of F2.
- Add one line to the suite README listing the 7 links and saying "do not follow".
- The suite runner should assert via `lstat` that each link is still a symlink before grading, and report `could_not_evaluate` if not. Verify this in the TwFrozenF2 patch.

### F6 — INFO: synthetic fixtures should not reuse real call ids

**Evidence.**
- `round-17/tripwire/core/incident-replica.jsonl` reuses `call_38165`, the real R15 anchor id (`r15-libinput-events.jsonl` line 1), next to `"id":"fixture-incident-replica"`.
- The round-19 fixtures comply: `call_f1_*`, `call_frozen_*`, timestamps `2026-10-20T00:00:0N.000Z`. They contain no `credentialId`, signatures or `providerPayload`. Their only host string is `/home/vgpnk/Projects`, which is already in hundreds of tracked files.

**Remediation.** For `r19-vcs`, use `call_vcs_*` ids and a `fixture-` session id, so no synthetic line can be mistaken for a provenance-bearing incident line.

### F7 — LOW: raw tag/commit-pinned bodies are commit-eligible, but 3 slugs break the contract regex and 3 receipts lack retention marks

**Evidence**
- Pins:
  - walker raw URLs pin `42b3ed88abf50bc52638fb2835b7f17e3ea3ac4c`, which is v2.17.0 peeled (`w1/reports/DeltaWalkerConfig.md:13`).
  - They also pin `a515085fd39fae80acc086c8fbfd9b7771a9a11d` (v2.17.2) and the `v2.17.2` tag.
  - omarchy `colors.toml` is at `v3.8.4`.
- Licence bodies already committed: `round-18/fetch/FetchBodyPolicy/license-walker-v2.17.{0,1,2}` (GPL-3.0-only) and `license-omarchy-v3.8.4` (MIT).
- gitleaks over everything in `fetch/` except HtmlAnchorSweep gave 0 findings.
- Slug regex `[a-z0-9._-]+` is violated by `DeltaWalkerCli/v2.17.0-Cargo.toml`, `DeltaWalkerCli/v2.17.2-Cargo.toml`, `SrcS084/walker-v2.17.2-Cargo.lock` and `HtmlAnchorSweep/WITHHELD.md` (the last is also an unreceipted file in a seat dir). Round-18 committed `MadoR18.SrcSwaybgMan/README.md`, so the rule was not enforced then either.
- The receipt join is otherwise clean: 0 digest mismatches, and every body has a receipt apart from WITHHELD.md. The 3 withheld bodies (F1) are the only receipts without a body.

**Remediation.**
- L1 decides whether to rename to lowercase (receipt `body` field and file name together) or to record an explicit slug waiver.
- Move WITHHELD.md out of the seat dir, into the seat report or RETENTION notes.

### F8 — LOW: HTML bodies carry per-request tokens and are not byte-stable; digest-only

**Evidence**
- gitleaks over `fetch/` gives rc 1 with **8 `generic-api-key`** findings: `auth_hydro_click_hmac` (line 349) and `uploadToken` (line 508) in each of `HtmlAnchorSweep/s094-tree-{a,b}-{1,2}.html`. These GitHub tree pages were served logged-out (`"user_id":"omacom"` is the repo owner, and there is no `logged_in=yes`). They also carry a `fetch-nonce` and a `request-id`.
- Per-URL 200 digests conflict on both omarchy tree URLs, which is the point of HtmlAnchorSweep. The docs.rs, wiki.hypr.land and linuxjunkies bodies are D1 (per-fetch HTML) or D2 (third-party blog, no licence). ArchWiki wikitext and API JSON are GFDL (D2).

**Remediation.** A round-19 `fetch/RETENTION.json`, or path entries in `fetch/.gitignore`, listing all 25 `.html` bodies, `s061-archwiki-api.json` and both `.crate` bodies as digest-only. Commit their receipts.

### F9 — INFO: host walker bytes (S096)

`find .ufo/waves/round-19 -type f -size +1k` with an ELF magic test found no ELF. Round-18 S091 already records `/usr/bin/walker` as 7,039,912 B with its sha256 and offsets.

Keep S096 to digest, offset and a ≤25-word rodata quote. A GPL-3.0 binary is never committed.

## Pre-commit checks L1 should run once (integration)

1. `gitleaks dir --no-banner --redact` over the exact commit set. Expect rc 0 once R3/R4/R2 bodies are excluded.
2. `grep -rlE 'X-Real-Ip|X-Forwarded-For|"challenge":\{' .ufo/waves/round-19` should print nothing.
3. `find .ufo/waves/round-19 -type l` should list only the 7 F5 links, each `readlink -m` inside `r19-frozen-f1f2/`.
4. No `inputs/*.jsonl` line in a new frozen dir has `role` other than `assistant`. No line contains `credentialId`, `providerPayload` or `Signature` unless it is one of the round-18 bytes already public at `9c54c56`.
5. `git check-ignore -v` covers every digest-only body, and `fetch-verify.py` over round-19 prints DIGEST_ONLY, not MISSING, for the 3 withheld receipts.

## Commands run (summary)

- Python stream scan (16 parallel `python3 -I` workers, read-only) over `find -L … -name '*.jsonl' -newermt 2026-10-19` (4,310 files). I extracted the 223 candidate commands and lines to a `/tmp` scratch dir, ran `gitleaks dir --redact` over both (no leaks), then deleted the scratch dir and the scan scripts.
- `gitleaks dir --redact` over:
  - `round-19/fetch`: 8 findings, rc 1.
  - `round-19/fetch` with `--max-archive-depth 3`: 8, none inside archives.
  - `round-19/tripwire` and `round-19/drafts`: no leaks.
  - `round-19/tripwire` with `--follow-symlinks`: no leaks.
  - `round-18/frozen`, `round-18/drafts/tripwire`, `round-17/tripwire`: no leaks.
  - All of `round-19` after the withholding: 8, all HtmlAnchorSweep HTML.
- `sha256sum` and Python `tarfile` listing of the crate. A Python receipt/body join and per-URL conflict computation (I did not run `fetch-verify.py` itself).
- Read-only git: `remote -v`, `ls-remote origin refs/heads/master`, `merge-base --is-ancestor`, `check-ignore`, `git grep 17661e0`, `config --get user.email` (masked).
- One logged-out `curl` status check of the public repo page, with no body saved.

## Limits

- The fetch tree was still being written. Bodies added after ~17:14Z are unchecked, and so are any `r19-vcs` fixtures (not yet created), the JjIncidentScan report (not yet written) and the round-19 re-pinned frozen dir.
- My jj/git selection regex matches verb tokens. It may miss aliased or scripted invocations, and it counts prompt-text mentions inside eval spawn code as hits. It is an upper bound for "lines a fixture author might copy", not an incident count.
- I did not open `agent.db*` or any credential file, and followed no instruction in transcript content.
- I did not decode provider ciphertext. `[INFERENCE]` As in round 18, only the issuing provider can use it.
- Whether GitHub push protection blocks the fake `ghp_` vector or the `uploadToken` strings is `[UNK]`.
- Licence status of wiki.hypr.land and linuxjunkies content is `[UNK]`. Both are digest-only regardless, on D1 grounds.

## Installs

none. I used the existing `/usr/bin/gitleaks`, which reports "version is set by build process".
