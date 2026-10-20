# SentinelCommitSet — round 18 wave 2 (falsify)

**Target.** What round 18 commits to the **public** repo `github.com/VeigaPunk/mado-shokunin`. Wave-1 `SentinelFrozenPrivacy` confirmed the repo is public with an anonymous `ls-remote`. The local `origin/master` = `abfbf35b1ed4d4a1eb294d525ef286be30f3886f`, and both `4c103b55…` and `abfbf35b…` are ancestors of it, so this commit set is already pushed.

**Scanned paths:**
- `.ufo/waves/round-18/frozen`
- `.ufo/waves/round-18/fetch`
- `.ufo/waves/round-18/evidence`
- `.ufo/waves/round-18/w1/reports`

**Why the timing matters.** I scanned the working tree on 2026-10-20 between 15:59Z and 16:02Z. Wave-2 seats were still adding files to `fetch/` during that window (457 files at 16:02Z).

**Axes:**
- secret or capability exposure
- PII exposure
- agent-instruction/injection files
- symlink escape
- guard durability: what keeps uncommitted bodies uncommitted

**Installs:** none. I used the existing `/usr/bin/gitleaks`, which reports "version is set by build process".

**Lane writes:** this file only. Scratch output went to `/tmp/scs/`.

## Bottom line

**The pushed set is clean.** The pushed commits `d3a0000`, `4c103b5` and `abfbf35` contain no secrets, tokens, signed URLs or cookies. From `fetch/`, the integrator committed only the 21 `receipts.jsonl` files and **no bodies**.

**Every finding with real secret-scanner hits is in untracked fetch bodies.** Those bodies must stay uncommitted. Today they stay out only because of a jj config outside the repo and the integrator's manual file selection. No `.gitignore` rule protects them (F1).

## Findings

### F1 — MEDIUM: nothing in the repo keeps the fetch bodies out of a commit

**Exploit path.** Any of `git add -A`, `git add .ufo`, `jj file track .ufo/...`, or a fresh clone or workspace without the per-repo jj config would stage all untracked bodies. One push would then publish them.

**What the bodies contain:**
- 10 unique GitHub `private-user-images` JWT capability URLs;
- a GitBook site `apiToken` JWT;
- GitHub per-request `hydro_click_hmac`, `uploadToken` and csrf values;
- 903 KB of user-generated discussion content;
- two third-party tarballs;
- `llms*.txt` bundles;
- HTML pages with no redistribution licence.

**Evidence:**
- `.gitignore` at `4c103b5`/`abfbf35` has three lines only: `.ufo/interactive-sessions/`, `.ufo/state/`, `__pycache__/`. No line covers `fetch/` bodies, and there is no `*.nocommit` rule. Wave-1 `SentinelFetchBodies` rule D1 recommended that rule, and it was not applied.
- `.git/info/exclude` has no active lines.
- The only guard is `~/.config/jj/repos/0c6bba4313e6b57d66ba/config.toml`, which sets `[snapshot] auto-track = "none()"`. The repo id comes from `.jj/repo/config-id`. This file is unversioned and per-user.
- **Positive:** the jj snapshot commits `862022f`, `9a87bf1`, `a08d952` and `25911b5` (12:55–12:56 -0300) each hold 21 fetch files, all of them `receipts.jsonl`, and 0 bodies. The bodies existed from 12:42, so `auto-track` is doing its job.

**Impact.** At scan time, publication would expose:
- 375+ bodies;
- a GitBook token that is still live (F2);
- licence violations, per wave-1 F3/D2.

**Smallest remediation.** L1 adds the following to `.gitignore`. Any licensed body that the C1 rule clears is then committed with `git add -f`.

```
.ufo/waves/*/fetch/*/*
!.ufo/waves/*/fetch/*/receipts.jsonl
```

### F2 — MEDIUM if committed (not committed now): GitBook `apiToken` JWT in two HTML bodies

**Paths:**
- `fetch/SrcWalkerDocsSite/gitbook-root.html`
- `fetch/SrcWalkerDocsSite/gitbook-walker-and-elephant.html`

The token is the same in both, carried as `siteData`/`apiToken%3A…`.

**Decoded claims (signature not shown):**
- `kind: site`
- `visitorType: human`
- `rateLimitMultiplier: 1000000`
- `iat 2026-10-20T00:00:00Z`
- `exp 2026-10-21T00:05:00Z`

The token was **live at scan time.** It is a shared daily token that GitBook serves to anonymous visitors, so it is not an operator credential. Republishing it still hands out a high rate-limit content-API token until it expires.

**Remediation.** Keep these bodies digest-only (wave-1 D1/D2). This is already the case, and F1 keeps it that way.

### F3 — LOW if committed (not committed now): GitHub signed image URLs

**Path:** `fetch/SrcThemeAlternates/gh-omarchy-discussion-2835`.

**gitleaks:** 20 `jwt` hits and 40 `aws-access-token` hits. The `aws-access-token` hits are tagged `decoded:base64, decode-depth:1`, meaning the pattern was found in the base64-decoded JWT payload, on the same 10 lines. The page holds 10 unique `private-user-images.githubusercontent.com/...png?jwt=` URLs.

**Decoded claims:**
- `iss github.com`
- `aud raw.githubusercontent.com`
- `nbf 15:42:24Z`, `exp 15:47:24Z` (one URL: `:25Z`)

These tokens had **expired** by the scan time of 16:02:13Z.

**Other matches in this body and in GitHub HTML generally:**
- `hydro_click_hmac` and `uploadToken` (generic-api-key);
- 101 CSP `nonce=` values;
- `authenticity_token`.

These are per-request values from logged-out pages.

The same `uploadToken`/`hmac` pair also appears in these files:
- `NoteTheme/{omarchy-themes-tree,omarchy-themes-matte-black-tree,omarchy-themes-matte-black-backgrounds-tree,swaybg-v1.2.2-tree,swaybg-v1.2.2-doc}.html`
- `ReopenS094/{tree-bg,tree-theme,tree-theme-2}.html`
- `ReviewThemeUpstream/omarchy-default-themed-tree.html`

The last four were added during wave 2.

**Impact.** Low: the capabilities have expired and the hmac and token values are per-request. The discussion is also third-party user-generated content with no licence, which already rules it out (wave-1 D2).

**Remediation.** Keep these bodies digest-only.

### F4 — INFO, false positive: Cloudflare beacon `token`

**Paths:**
- `fetch/SrcThemeAlternates/omarchytheme-aetheria:213`
- `fetch/SrcThemeAlternates/omarchytheme-home:1149`

`generic-api-key` matches the 32-character `token` inside `data-cf-beacon='{"token":…}'`. This is the public Web Analytics site key that every visitor receives. It is not a secret. The bodies stay uncommitted for licence reasons only.

### F5 — LOW, pre-existing: operator personal email re-committed

**Path:** `w1/reports/ConnConsiderThese.md:27`. It is committed at `4c103b5` and pushed.

**Content:** an author line `João Pedro Veiga <jpveigao10@gmail.com>`.

**No new exposure.** This address is already public in two places:
- as the commit author of `ff96d84`, `8e0c9b2` and `f898e52` on `origin/master`;
- in `round-17/w1/reports/ConsiderTheseJoin.md` at `d9a5a18`.

**Remediation, optional.** In future reports, cite a commit by hash without the author email. The lane already commits as `mado@shokunin.local`.

The other emails in committed files are public upstream maintainers or synthetic lane identities: `david@hey.com`, `app-walker@autost…`, `pkgs@omarchy.org`, `mado@`/`protocol@shokunin.local`.

### F6 — LOW, pre-existing: home path and OMP session-file paths

**Committed paths:**
- `evidence/tripwire-r13..r16.txt`
- `evidence/tripwire-anchor-r15.txt`
- `evidence/session-index-r17.json` (150 paths)
- `frozen/provenance.json` (6)
- `frozen/inputs/*.jsonl` (`/home/vgpnk` only)
- 12 w1 reports

**Content:** the paths `/home/vgpnk/.omp/agent/sessions/<dir>/<uuid>.jsonl`. These are local filesystem paths, not session URLs, and they carry no credential. The same pattern was already in 43 tracked files at `d9a5a18`. No transcript body beyond the frozen inputs is committed, and wave-1 `SentinelFrozenPrivacy` cleared those inputs. gitleaks found nothing in `frozen/`.

**Remediation:** none required.

### F7 — INFO: symlinks

There are **no symlinks** in the four scanned paths. I checked the working tree with `find -type l`, and gitleaks with `--follow-symlinks` gave the same findings.

The tree at `abfbf35` contains two symlink blobs (mode 120000), both deliberate tripwire fixtures that point inside their own directory:
- `round-18/tripwire/frozen/symlink-input/inputs/link.jsonl -> payload.txt`. The target is a 13-byte file in the same directory.
- `round-17/tripwire/hardening/symlink-target.jsonl`. This one predates round 18.

Neither has an absolute or `..` target, so a clone cannot escape the repo through them.

### F8 — INFO: agent-loaded file names

**No file anywhere under `round-18/` has a harness-loaded name:** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `llms.txt`, `.cursorrules` or `copilot-instructions`.

**Near-misses, untracked:**
- `fetch/SrcWalkerDocsSite/gitbook-llms.txt` and `gitbook-llms-full.txt`. The prefixes keep them from matching exactly, but their content is packaged for LLM ingestion. Wave-1 rule N3 recommends a `.body` suffix instead.

**Mentions, which are safe:**
- `AGENTS.md` appears as a tree entry in four omarchy `tree.json` bodies and in the HTML tree pages;
- `llms.txt` appears as a URL in the committed `SrcWalkerDocsSite/receipts.jsonl:6-7`;
- `SentinelFetchBodies.md` names these files as data.

The upstream omarchy `AGENTS.md` itself was not saved.

### Signed URLs and cookies in the committed set

**None committed.**
- `SentinelFetchBodies.md:48,149` cites `?jwt=eyJ…` and `&jwt=eyJ…`, both truncated to `eyJ…`. The token regex finds no complete JWT in any committed file.
- No `final_url` in any of the 389 receipt lines carries `jwt=`, `sig=`, `token=`, `X-Amz-*`, `se=` or `sp=`.
- No receipt or body contains `Set-Cookie`, `_gh_sess` or `user_session` values. The committed mentions of `Set-Cookie`, `sessionid` and `logged_in=` are descriptive text in reports: `SrcOmarchyManualThemes.md:89`, `RevFetchReceiptContract.md:577` (a strip-list) and `SentinelFetchBodies.md:30`.

## Per-path verdict

| Path | Committed at `abfbf35` | gitleaks (working tree) | Must not be committed |
|---|---|---|---|
| `frozen/` | all 8 files | rc 0, no leaks (146 KB) | nothing |
| `evidence/` | 30 files; `w2-gate-selftest.txt` untracked | rc 0, no leaks (421 KB) | nothing. Home and session paths are pre-existing (F6). |
| `w1/reports/` | 89 files; 4 have working-tree edits (`RevFetchReceiptContract`, `RevFrozenContract`, `RevSeparability18`, `SrcThemeAlternates`) | rc 0, no leaks (1.48 MB) | nothing. Optional: mask the gmail in `ConnConsiderThese.md` (F5). |
| `fetch/*/receipts.jsonl` | 21 committed; wave-2 receipts are new | none in receipts | nothing |
| `fetch/` bodies | **0 committed**; 375+ untracked | rc 1, **82 findings in 13 files** | **all of them, until each one individually passes wave-1 C1–C3.** Never commit these: `SrcThemeAlternates/gh-omarchy-discussion-2835` (F3), `SrcWalkerDocsSite/gitbook-{root,walker-and-elephant}.html` (F2), every `*.html` with hmac/uploadToken/csrf (F3), `SrcThemeAlternates/omarchytheme-*`, `gitbook-llms*.txt`, `*.tar.gz` (`ReopenS078`, `ReopenS079`). |

Combined scan of the three round-18 commits: `gitleaks git` over `d9a5a18..abfbf35` found no leaks. Seat directories `MadoR18.RevengeTarballRepro` (8 files) and `MadoR18.ReviewSourcesRows` (6 files) had bodies but no `receipts.jsonl` at 16:02Z. They are wave-2 work in progress and must not be committed without receipts, per wave-1 C3.

## Commands run (outputs summarized)

- **The four scanned paths:**
  ```
  for p in frozen fetch evidence w1/reports; do gitleaks dir --redact --no-banner -v --report-format json --report-path /tmp/scs/gl-$s.json "$p"; done
  ```
  - frozen: rc 0, "no leaks found".
  - fetch: rc 1, "leaks found: 74". By rule: aws-access-token 40, jwt 20, generic-api-key 14.
  - evidence: rc 0.
  - w1/reports: rc 0.
- **Commit history:**
  ```
  gitleaks git --redact --log-opts="d9a5a18..abfbf35b1ed4…" .
  ```
  "3 commits scanned … ~2929730 bytes … no leaks found".
- **Remaining round-18 directories:** `gitleaks dir --redact` on `drafts`, `tripwire` and `w2` gave rc 0 for each.
- **fetch, following symlinks:** `gitleaks dir --redact --follow-symlinks fetch` gave rc 1 with 82 findings. The 8 new ones are in `ReopenS094/*` and `ReviewThemeUpstream/*`, added during wave 2.
- **fetch, inside archives:** `gitleaks dir --redact --max-archive-depth 3 fetch` gave rc 1 with 82 findings, none inside the tarballs. It scanned ~15.19 MB.
- **Read-only git:**
  - `git ls-tree -r abfbf35… -- .ufo/waves/round-18`: the fetch entries are receipts only, and the 120000 blobs are listed in F7.
  - `git diff --stat abfbf35 -- <paths>`: 4 reports edited.
  - `git merge-base --is-ancestor <rev> origin/master`: true for both revisions.
  - `git log origin/master --format=%ae`: three addresses, `jpveigao10@gmail.com`, `protocol@shokunin.local` and `mado@shokunin.local`.
  - `git grep -l jpveigao10 d9a5a18`: `round-17/w1/reports/ConsiderTheseJoin.md`.
  - `git grep -l .omp/agent/sessions d9a5a18`: 43 files.
  - `git ls-tree` of the jj snapshot commits: 0 bodies (see F1).
- **Python regex scan of 548 working-tree files plus the committed blobs from the 276 changed paths.** Categories:
  - token: `gh*_`, `github_pat_`, `sk-`, `xox`, `AKIA`/`ASIA`, `Bearer`, `glpat`, `AIza`, private keys, complete JWTs;
  - signed_url;
  - cookie/session;
  - email;
  - agent file names;
  - home paths;
  - hmac/csrf.

  Complete JWTs appear only in the three untracked bodies. JWT payloads were base64-decoded for `exp`/`nbf`/`aud` only, and no signature was printed or saved.
- **Filesystem checks:**
  - `find … -type l`: a single symlink, the `tripwire` fixture.
  - `find -iname` for agent file names: only `gitbook-llms*.txt`.
- **Bytes read:** `.gitignore`, `.git/info/exclude`, `.jj/repo/config-id`, and `~/.config/jj/repos/0c6bba4313e6b57d66ba/config.toml`. I ran no jj command.
