# SentEvidenceLeak — round 40 w1 leakage scan (mado-shokunin)

Seat: `SentEvidenceLeak` (leaf; no dispatch, no background jobs, no installs, no compositor verbs).
Scope: `.ufo/waves/round-40/**` — 312 files at the closing sweep — and the candidate sources under
`/home/vgpnk/Projects/shokuknow/merge/mado/` (72 files, read-only).
Axes: (A) secret-shaped tokens/keys, (B) absolute private paths beyond `/home/vgpnk`, (C) session /
host identifiers, (D) ai-usage cache content, (E) emails and credential material.

**No secret value is reproduced in this report — paths, line numbers and shapes only.**

## Verdict

**No credential exists anywhere in either surface**: zero API keys, bearer tokens, passwords,
private-key blocks, cookies, Authorization headers, credential files, UUIDs or session tokens. The
single email that is *not* fabricated is a third-party paper author's (F9).

What the round does carry is **host-identifier and private-data leakage**, and one place where a seat
broke its own redaction rule (F7). Ten findings; the two that must be fixed before these bytes are
committed are **F1** (literal Hyprland session signature, already in the tracked corpus) and **F7**
(live private cache timestamp printed in two wave files). None of them changes a claim's truth
value: every redaction below is a rewrite of an identifier, not of an assertion.

## Findings, in fix order

### F7 — HIGH: the live ai-usage cache `updated_at` value is printed, against the seat's own rule

- `w1/ExecFetchK2Sources/quotes.md:100` — "`~/.cache/ai-usage/status.json:3` now reads
  `"updated_at": <fresh ISO-8601 ts>,"`" — the **live** value.
- `w1/ExecFetchK2Sources/quotes.md:110` — the same fresh value again, contrasted with the
  candidate's value.
- `w1/ExecFetchK2Sources.md:66` — same fresh value in the summary table.
- **Self-contradiction, and the proof of it:** the same round's quotable receipt states the rule and
  honours it — `fetch/host-k2-reads.txt:78` "the raw timestamp is NOT quotable",
  `:80` "[NOT-QUOTABLE] every mtime/ctime/date, the cache `updated_at` string …", and
  `w1/ExecK2HostReads/host-reads.txt:121` gives only `type str, ISO-8601 "Z"`. Two files obey; two
  print the value.
- **Impact:** a private activity timestamp (when the operator last ran an AI CLI) plus a live
  "the cache is fresh" assertion; it is also a *volatile pin*, which is exactly the round-39
  closure failure this entry is supposed to fix (`w1/ExecK2HostReads.md:46`).
- **Redaction:** replace both literals with `"updated_at": <ts>` and keep
  `updated_at_within_24h=true` (`fetch/host-k2-reads.txt:78`) plus the `STALE_AFTER_SEC = 20*60`
  threshold. Nothing in the S241 verdict depends on the digits — the verdict is "DIFFERENT
  (rotated)", which survives as "value rotated; property holds".

### F1 — HIGH: literal Hyprland instance signature (session id + UID) in wave evidence

- `w1/ConnEvidenceResolve/freeze_SOURCES.md:222` — row S258 carries the instance directory
  literally: `/run/user/1000/hypr/efb5099…_<epoch>_<counter>` (UID `1000` + the full per-session
  HIS). Byte-identical to `corpus/SOURCES.md:222` (both files are 464 lines — the seat copied the
  tracked bytes).
- **This is a break of the lane's own convention, not a new policy:** `corpus/knowledge/hyprctl-verification-layer.md:29`
  writes `` `/run/user/1000/hypr/<sig>/` `` and says "shape only"; `corpus/lessons/round-38.md:63`
  writes `<HIS>_<epoch>_<rand>`. Row S258 is the one exception, and round 40 now holds a copy of it.
- **Redaction:** `/run/user/$UID/hypr/<HIS>`. The claim (directory mode 0700, sockets 0755) does
  not depend on the name. Fix `corpus/SOURCES.md:222` in the same pass; the wave copy is downstream.

### F9 — MEDIUM: third-party personal data in a fetched dump

- `w1/ExecQuarantineSlice/src/arxiv-html.html:214` — an arXiv paper author's institutional email
  (`<initials><digits>@<university>.edu`), inside a 243 KB full-HTML copy. The abstract copy
  (`arxiv-abs.html`) carries no `mailto:` — only this one does.
- **Impact:** retaining a real person's contact address in lane bytes for no claim; the quarantine
  slice needs the paper's *claim*, not its author block.
- **Redaction:** drop `arxiv-html.html` from the committed slice (cite the arXiv id / DOI and keep
  `arxiv-abs.html`), or strip the `ltx_contact` author block. Nothing in the slice's verdict reads it.

### F2 — MEDIUM: the ai-usage cache's *values* are quoted in the candidate sources (K2 input)

The round's own standard — "cache file … metadata ONLY (key names, no values …)"
(`make-w1-spec.py:183`) — is newer than these rows:

- `…/shokuknow/merge/mado/SOURCES.append.md:45` (S241) — quotes the cache's `"updated_at": <ISO-8601 ts>`
  **and** `"label": <window>, "used_pct": <int>` from `providers.codex.windows[0]`: a real activity
  timestamp, the operator's quota consumption, and which AI CLI they run.
- `…/knowledge/corpus/knowledge/host-producer-outputs-r29.md:35` — repeats `"updated_at": <ISO-8601 ts>,`
  verbatim as an OBS quote. **This is the note round 40 is assimilating as K2.**
- `…/knowledge/corpus/knowledge/host-producer-current-outputs-r30.md:86` — `"version": 1,` (schema
  field, benign; listed for completeness).
- **Redaction before any admission:** keep key names and file metadata, drop values —
  `"updated_at": <ts>`, no `used_pct`, provider key only if the claim needs it. The claim ("the
  chip's text is a pure function of a cache that names its own freshness") is unaffected.

### F8 — MEDIUM: the operator's AI-provider inventory is enumerated

- `fetch/host-k2-reads.txt:77` — `provider_keys=12 (<twelve vendor names>)`.
- `w1/ExecK2HostReads/host-reads.txt:119-120` — the same twelve names, expanded.
- This is inside the seat's instruction ("key names"), so it is not a violation — it is a **privacy
  judgement to make before commit**: the entry needs the *count* (12) and the fact that the schema
  is per-provider; the vendor list is the operator's private tool inventory and identifies their AI
  subscriptions.
- **Redaction:** keep `provider_keys=12`; drop the parenthesised names from both files.

### F4 — MEDIUM: absolute private home paths (tilde-normalizable), now a large surface

- `w1/ExecHostSourceGraph/graph.json` — **252** occurrences of `/home/vgpnk/…` (the same file also
  carries the correct `~/…` duplicates at e.g. `:1149`).
- `w1/ExecK2HostReads/host-reads.txt` — 11 (`:34, 35, 37, 39, 41, 44, 45, 115, 116, …`);
  `fetch/host-k2-reads.txt:9` (`path=/home/vgpnk/.config/waybar/config.jsonc`);
  `w1/ExecK2HostReads.md:22-23`; `w1/ExecAssimIdGuard/guard.md:4, 5, 12-14, 94, 159-161`;
  `w1/ExecFetchK2Sources/quotes.md` (one, in the symlink note);
  `w1/ConnEvidenceResolve/freeze_SOURCES.md:32, 205, 208, 209, 210`.
- Candidate sources: `SOURCES.append.md:44, 45`, `host-producer-outputs-r29.md:9-12`,
  `host-producer-current-outputs-r30.md:12`.
- **Redaction:** `~/…`. The wave already contains the standard to apply —
  `w1/ExecLiveCensus/census-receipt.txt` notes "owner paths are relative to `$HOME`".

### F10 — MEDIUM: sibling private repositories disclosed through symlink resolution

- `fetch/host-k2-reads.txt` `[PIN-2]` — `~/.local/bin/gkeep -> /home/vgpnk/Projects/gkeep/bin/gkeep`,
  `~/.local/bin/ai-usage -> /home/vgpnk/Projects/omarchy-usage-tray/bin/ai-usage`.
- Same targets at `w1/ExecK2HostReads/host-reads.txt:34-45`, `w1/ExecK2HostReads.md:22-23`,
  `w1/ExecFetchK2Sources/quotes.md:99, 101` (there as `Projects/…`, still a private repo name).
- **Impact:** reveals two private host repos outside the lane (one of them a private AI-usage
  tracker) plus their commit history was read (`w1/ExecK2HostReads.md:48-49` cites `git -C … log`).
  The claim only needs "the entry point is a 252 B shim" and "a single-file Python program".
- **Redaction:** `~/Projects/<repo>/…` or "symlink target (private checkout), sha256 …"; drop the
  repository names and the commit ids of foreign repos.

### F3 — MEDIUM: hostname inside verbatim journal quotes (candidate sources only)

- `…/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md:24, 32` —
  `2026-10-23T22:14:10-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: …`
- `…/knowledge/corpus/knowledge/idle-lock-chain-armed-r14.md:21` — `… plazir27 systemd[1493]: Started hypridle.`
- The machine name is already in the lane's tracked corpus (`corpus/knowledge/waybar-walker-semantics.md:4`,
  `walker-deep.md:4`, `walker-live-surface.md:6`, `walker-deep-r9.md:8`), so this is a pre-existing
  convention rather than a new break — but these three are *journal quotations*, which also pin a
  session start time, the local UTC offset and two journal PIDs.
- **Redaction for any new admission:** `<host>`, `<pid>`; keep the decisive fragment (`Started hypridle`).
  Round 40 contains no such quote (verified: zero `plazir27` hits in the wave).

### F5 — LOW: host process identifiers

- `w1/ExecK2HostReads/host-reads.txt` `[QUERY-3]/[QUERY-4]` (hypridle/waybar pids),
  `w1/ExecK2HostReads.md:30` (supporting reads), `w1/ExecQuarantineSlice/registry-rows.txt:8`
  (`pid 1667`), `w1/ConnEvidenceResolve/freeze_SOURCES.md:207`, `w1/ConnEvidenceResolve/freeze_README.md:60`.
- `w1/ExecWatchdogTable/table.md` §D — 20 verbatim fleet watchdog lines with `pgid=<7-digit>` per
  launch and local `-03:00` timestamps: a process-liveness fingerprint of the fleet driver.
- Candidate sources: `SOURCES.append.md:72` (`PID 1667`), `idle-lock-runtime-state-r28.md:42` (`PID 1718`).
- **Redaction:** `<pid>` / `pgid=<pgid>`. Every count and duration the seats measured is unaffected.

### F6 / F11 — LOW: volatile private timestamps and scratch paths

- `w1/ExecK2HostReads/host-reads.txt:24, 115` — `stat -c 'size=%s mtime=%y'` output with full
  nanosecond mtimes and the local `-0300` offset, including the **cache file's** mtime (`:115`) —
  the same class the seat itself lists as `[NOT-QUOTABLE]` (`fetch/host-k2-reads.txt:80`). The
  quotable receipt (`host-k2-reads.txt`) correctly omits it; only the full capture carries it.
- `/tmp/mado-options-ref.py` (`w1/ExecLiveCensus.md:5`), `/tmp/elephant.sock`, `/tmp/hypr`
  (`w1/ConnEvidenceResolve/freeze_SOURCES.md:92, 203`), `-03:00` (`:215`).
- **Redaction:** none required for commit; do not treat mtimes as evidence pins (round-39 D2 class).

## Clean — searched and absent (positive evidence)

Patterns over both surfaces:
`api[_-]?key|secret|passw|token|bearer|authorization|credential|BEGIN [A-Z ]*PRIVATE KEY|ghp_|gho_|sk-[A-Za-z0-9]{16,}|xox[baprs]-|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}\.`
→ only prose hits: the option key `misc:initial_workspace_token_timeout`
(`w1/ExecAllOptionsForms/raw-census.jsonl:218`), the tool's own "tokens" wording, "credential
prompt" narrative, and this report's pattern list. No PEM block, no base64 blob ≥60 chars outside
sha256/md5 digests.

- **Emails (all four hits):** `ctl@ctl.invalid` (`ctl/run-c2-controls.py:183`) and
  `crit@crit.invalid` (`w1/CritC2Cheat/build-cheats.py:25`) — fabricated git fixtures under the
  reserved `.invalid` TLD, correct; `cli-reference@.md.snap` (`w1/ConnEvidenceResolve/freeze_SOURCES.md:116`)
  — a filename, false positive; and F9's real one.
- **UUIDs:** zero, both surfaces.
- **HTTP receipts:** `fetch/*.http.txt` carry only `DATE_UTC, HTTP_STATUS, SIZE, SHA256,
  EFFECTIVE_URL, CURL_EXIT` — no Cookie / Authorization / Set-Cookie.
- **Fetched bytes:** upstream public files (Hyprland `ConfigManager.cpp`, `ComplexDataTypes.hpp`,
  hyprlang `config.cpp`, omarchy v3.8.4 indicators). The two host indicator copies
  (`fetch/host-indicator-*.bin`) are 7-line public scripts byte-identical to upstream
  (`w1/ExecFetchK2Sources/quotes.md` cmp) with no path, host name or secret.
- **Private dotfiles:** no `.ssh`, `.gnupg`, `.aws`, `.netrc`, `git-credentials`, `password-store`,
  `mozilla`/`thunderbird` profile path, and no `.env` content quoted, anywhere.
- **Host config bytes:** the verbatim waybar blocks (`fetch/host-k2-reads.txt` QUOTE-A/B) are host
  config content, which the round is allowed to copy into evidence; they contain `~/.local/bin/…`
  exec lines and no secret.
- **Hostname in round-40:** zero occurrences (F3 is candidate-side only).

## Redaction checklist for the integrator

1. `quotes.md:100, 110` + `ExecFetchK2Sources.md:66` → `"updated_at": <ts>` (F7).
2. `corpus/SOURCES.md:222` + `w1/ConnEvidenceResolve/freeze_SOURCES.md:222` → `<HIS>` (F1).
3. Drop or strip `w1/ExecQuarantineSlice/src/arxiv-html.html` (F9).
4. Any K2 admission: shape-only cache row, `<host>`/`<pid>` in journal quotes (F2, F3).
5. `~/…` rewrite across `graph.json`, the K2 receipts and `guard.md` (F4); `<repo>` for the symlink
   targets (F10); `provider_keys=12` only (F8).
6. `<pid>` / `pgid=<pgid>` if the watchdog table is committed (F5).

## Re-scan (closing sweep, after the last wave files landed)

Wave grew 59 → 312 files during this seat. All patterns re-run on the final state (312 files); the
counts below are from that last pass, and the four emails / one HIS / zero UUIDs / zero secrets were
identical at 59, 261 and 312 files:

| axis | result at close |
|---|---|
| secrets / keys / PEM / bearer | none (only prose and this report's pattern string) |
| emails | 2 fabricated `.invalid`, 1 filename false positive, 1 real (F9) |
| UUID / session token | none |
| Hyprland instance signature | 1 literal (F1), unchanged |
| hostname | 0 in the wave |
| ai-usage cache values | 2 files print the live timestamp (F7); 12 provider names (F8); no cache body elsewhere |
| absolute home paths | 252 in `graph.json`, 11 in `host-reads.txt`, remainder single digits |
| host pid/pgid | 4 wave files + 20 watchdog lines |

`git status --porcelain` (read-only) shows the wave as the only untracked surface — nothing leaked
into tracked files this round except through F1's source line, which predates round 40.
