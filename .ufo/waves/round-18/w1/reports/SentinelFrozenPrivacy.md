# SentinelFrozenPrivacy — round 18 wave 1

**Surface:** committing real OMP transcript lines into the pushed lane repo as `.ufo/waves/round-18/frozen-tripwire/inputs/*.jsonl`.

**Source session:** `…/sessions/-Projects-shokunin/2026-10-20T01-48-55-258Z_01a156ff-…`.

**Candidates reviewed:**
- `MadoR15.LibinputEvents.jsonl` lines 50–62
- `MadoR13.GlobalCapture.jsonl:19`
- `MadoR14.ReviewSourceBar.jsonl:41`, plus `:34` as a coverage substitute
- `MadoR14.OutputSpec.jsonl:65`
- `MadoR14.SourceSafety.jsonl:152,155`
- `MadoR13.jsonl:470`
- After it landed, `frozen-tripwire/inputs/r15-libinput-events.jsonl` (sha256 `7118b883…`; source lines 54, 83, 86, 123, 158).

**What I did not do:**
- I copied no secrets in this report. Identity values were matched in memory and masked.
- No installs. I used the existing `/usr/bin/gitleaks`, which prints its version as "version is set by build process".
- No host probes, no git or jj writes.
- I wrote only this file and a `/tmp/sfp-r18.*` scratch directory, which I deleted after the run.

## Verdict

**No secret, credential or token** is in any candidate line, or in any assistant toolCall line of the six source files.

**Operator-identifying data** is limited to two things, both already public:
- the home path `/home/vgpnk`, present in 418 tracked files;
- the lane's own git identity, a lane name at a `.local` domain. It is not a personal name.

**The repo is public.** An anonymous `git -c credential.helper= ls-remote https://github.com/VeigaPunk/mado-shokunin` returned `refs/heads/master` = `d3a00003…`. Everything committed is world-readable.

**Residual risk is LOW for verbatim assistant lines.** It is **MEDIUM if `OutputSpec:65` or any toolResult line is committed.**

The smallest remediation that keeps the digests meaningful is a whitelist projection that changes no verdict (§Remediation). I verified that the projection gives the identical verdict.

## Negative results

**Pattern scan.** I scanned every string field, including nested JSON strings. No hits in any candidate line for:
- `gh[pousr]_` / `github_pat_`, `sk-…`, `AKIA…`, `xox?-`, `AIza…`
- JWT `eyJ…`, `Bearer …`, `BEGIN … PRIVATE KEY`
- `authorization` / `api_key` / `token` / `secret` / `password` key=value pairs
- IPv4, MAC addresses, localhost endpoints

**Host and operator identity.** I checked for the `/etc/hostname` value, the git `user.name` and `user.email`, and the GitHub owner handle.
- 0 hits for the hostname and the handle.
- The `user.name` / `user.email` local-part hits are the lane name inside lane paths and in `/tmp/<lane>-…` scratch names.

**Monitor identifiers.** `HDMI-A-1` appears 3× in `OutputSpec:65`, but only in the wlr protocol's documentation example. No host monitor make, model or serial appears anywhere. The `serial` hits are protocol text.

**Device paths.** The `/dev/input/eventN` hits in `LibinputEvents:50,53,63,64` are libinput documentation and man-page examples. No host device enumeration appears.

**gitleaks, `dir --redact`:**
- All 9 candidate lines (899,891 B) and the landed snapshot: **no leaks**.
- Over all six full source files: 10 `sourcegraph-access-token` hits at `ReviewSourceBar:20`, `SourceSafety:29` and `MadoR13:351-352`. **All are false positives.** Each is a 40-hex upstream commit SHA. All 6 distinct values are already in tracked lane files at `refs/heads/master`, and none carries an `sgp_` prefix. None of these lines is a snapshot candidate.

**Control-line screen.** I screened every assistant toolCall line in the six files (LE 46, GC 33, RSB 20, OS 4, SS 41, R13 137) for credential, auth or oauth paths, `.ssh`, gnupg, shell history, hostname or machine-id, `env` / `printenv`, `/etc/shadow`, and `journalctl` / `loginctl`. Two lines were flagged, and both are benign:
- `LE:147`: thinking text that says "credential access" is forbidden.
- `GC:12`: an `id -u` used inside a path. That line is a finding line.

## Findings

### F1 — MEDIUM (if committed): `MadoR14.OutputSpec.jsonl:65` is a 792,860-byte bulk carrier of non-scanner content

**Evidence.** `message.providerPayload` is of type `cursorHistory`, 738,203 B, with 84 records (34 assistant, 50 tool). It replays a whole seat history, including:
- **The operator's tooling directive, read verbatim from `~/.omp/agent/RULES.md` (first 50 lines).** It states that agents get passwordless sudo, and it names the fragile boot-chain hooks (mkinitcpio 42 `/sysroot`, `btrfs-overlayfs`, `plymouth`).
- **pacman transaction output** naming the pre-transaction hook `limine-snapper-sync`, and a host wayland package inventory (`egl-wayland`, `lib32-wayland`, `qt5-wayland`, `xorg-xwayland`, …).
- **116 occurrences of 6 third-party upstream maintainer email addresses**, taken from wlr-protocols commit metadata.
- Full `/usr/share` protocol XML and lane-file contents.
- A cursor reasoning `signature` (328 B).

The message's own toolCalls account for only 6,615 B of the line.

**Exploit path.** Published together in one public, machine-readable blob, this tells anyone:
- that a prompt-injected agent on this host can get root without a password;
- which boot hooks break on a partial upgrade;
- a slice of the installed package set.

The maintainer emails become a harvestable bulk copy.

**Mitigating facts:**
- The `Passwordless` / `btrfs-overlayfs` wording is already in 3 tracked reports.
- The emails are public in upstream git.
- `TwFrozenSnapshot`'s brief already says to skip source lines over 256 KiB, so this line is excluded by default.

**Impact.** Republishes host attack-surface data and third-party personal data for **zero** scanner value. The tripwire reads only `message.content[].toolCall` items (`tools/mado-tripwire.py:755-797`), never `providerPayload`.

**Remediation.**
- Keep it excluded.
- If its 7 findings are wanted, include only the projected line (6,615 B, §Remediation). The projection preserves every finding byte-for-byte.
- Its rules (`sudo`, `pacman:-S`, `-Q`, `-Ss`, `-Ql`, `-Qi`) are otherwise all covered by `GC:19`, `LE:54`, `LE:57` and `RSB:34`.

### F2 — MEDIUM (if committed): toolResult and doc-fetch lines in the "LibinputEvents:54 region" carry host output with no scanner value

**Evidence.** In lines 50–62:
- **toolResult lines:**
  - `:50` (12,829 B) and `:53` (9,761 B): fetched libinput documentation.
  - `:56`: pacman transaction output showing the upgrade 1.31.3→1.32.0 and dependency versions.
  - `:59`: a `pacman -Ql` listing.
- **Tool-start echoes:** `:52,55,58,61,62` are `custom` records.

Other files show what toolResult lines carry in general. For example, `GC:18` contains host env **values** (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR=/run/user/<uid>`).

The scanner skips every non-`message`/assistant line (`mado-tripwire.py:755-759`).

**Impact.** Host facts and third-party document bodies become public without adding coverage.

**Remediation.**
- Snapshot only assistant toolCall lines. The landed `r15-libinput-events.jsonl` already does this.
- Exception: a `custom` tool-start line such as `LE:55` (389 B, clean) is a legitimate negative control, because it echoes `sudo pacman -S …` in `data.args.command` and must not fire. If it is used, keep it verbatim, or keep `data.args` in the projection.

### F3 — LOW: verbatim assistant lines carry opaque provider blobs and account metadata unrelated to the verdict

**Evidence** (bytes per line; *blob* = `thoughtSignature`, `thinkingSignature` or `encrypted_content`):

| Line | Bytes | Projected bytes | Blob bytes | Thinking chars | Provider | `credentialId` | `responseId` | `/home/vgpnk` |
|---|---:|---:|---:|---:|---|---|---|---:|
| `LE:54` | 3,890 | 239 | 2,500 | 297 | google-antigravity | yes | – | 1 |
| `LE:57` | 2,387 | 225 | 1,036 | 246 | google-antigravity | yes | – | 1 |
| `LE:60` | 2,204 | 333 | 924 | 0 | google-antigravity | yes | – | 2 |
| `GC:19` | 3,593 | 997 | 17 | 468 | opencode-go | yes | yes | 4 |
| `RSB:41` | 11,688 | 937 | 7,316 | 1,611 | anthropic | yes | yes | 0 |
| `SS:152` | 11,977 | 3,253 | 5,488 | 2,119 | anthropic | yes | yes | 0 |
| `SS:155` | 5,058 | 1,307 | 2,080 | 530 | anthropic | yes | yes | 0 |
| `R13:470` | 27,215 | 2,431 | 20,052 | 0 | openai-codex | yes | yes | 4 |

**R13:470** also has a `providerPayload` of 23,784 B. It holds 3 `encrypted_content` reasoning items, `rs_…` item ids, `turn_id` UUIDs, `serviceTier` and `premiumRequests`.

**Thinking plaintext.** I read it all. It is benign task reasoning, with no host values and no identity data. The `SS:152` thinking mentions the monitor-name fingerprinting risk only in the abstract.

**Exploit path.**
- None to a credential.
- `credentialId` (integers 18, 25, 28, 30) indexes the operator's credential slots in `agent.db`.
- Provider names, costs and `premiumRequests` profile which paid accounts the operator holds.
- `encrypted_content` / `thoughtSignature` are provider-bound reasoning ciphertext and signatures. `[INFERENCE]` They can be decrypted or validated only by the issuing provider.
- Provider families were already inferable from tool-call id prefixes (round-17 SentinelReceiptsPrivacy F4).

**Impact.** Account profiling, plus about 39 KB of noise in a "digest-pinned" fixture.

**Remediation.** The projection below drops all of these. Acceptable as-is if L1 keeps verbatim lines.

### F4 — INFO: the tool's output `redact()` does not protect committed inputs

`SECRET_PATTERNS` and `redact()` (`mado-tripwire.py:92-119`) sanitise only the `command` field of findings that are printed. A frozen snapshot commits the input lines raw. Any secret in a selected line would be published in full, regardless of what the receipt shows.

The pre-commit gate for inputs must therefore be a separate scan, either gitleaks or the projection. It must not rely on the tool's own redaction.

### F5 — INFO: byte-exact copies add no public verifiability over a pinned projection

The public can hash a snapshot line, but has nothing public to compare it with:
- `session-index.json` commits whole-file digests only;
- the source files are private.

Only a holder of the private transcript can confirm that "snapshot line == source line N", and that holder can equally confirm "projection(source line N) == snapshot line" if the projection rule is pinned. Byte-exactness therefore buys nothing for public verification, and it costs F1–F3 exposure.

## Remediation (smallest, digest-preserving)

**Projection `mado-transcript-projection-v1`, per selected source line.**

Assistant `message` lines are reduced to:

```json
{"type":"message","timestamp":T,"message":{"role":"assistant","content":[{"type":"toolCall","id":ID,"name":NAME,"arguments":{"command"|"code"|"language" only}}...]}}
```

The `toolCall` items keep their source order.

Serialisation:

```python
json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
```

Non-assistant negative controls are kept verbatim, or with `data.args` kept, as in F2.

**Pins:**
- **`expected.json`:** keeps the `sha256` of each snapshot file. The contract is unchanged.
- **`provenance.json`, per snapshot line:**
  - `source_path`, `source_sha256` (must equal `session-index.json`), `source_line`;
  - `source_line_sha256` = sha256 of the raw source line bytes including `\n`;
  - `projection: "mado-transcript-projection-v1"`, `snapshot_line_sha256`.
- **`provenance.json`, top level:** the projection rule text and its sha256.

Publishing `source_line_sha256` is safe. Every line has high entropy (timestamps, call ids, signatures), so a brute-force preimage is infeasible.

**Checker change (`frozen-provenance-check.py`).** For projected lines, replace "snapshot bytes == source bytes" with two checks:
- `sha256(source line) == source_line_sha256`;
- `project(source line) == snapshot line`, byte for byte.

Exit codes 0/1/2 are unchanged.

**Equivalence receipt (run once, on /tmp only).** Tripwire sha256 was `593b3aafed37…` before and after the run. I ran `python3 -I tools/mado-tripwire.py --scan` over two `/tmp` sets of the same selected lines:
- the **verbatim** set (`LE:50-62`, `GC:19`, `RSB:34,41`, `OS:65`, `SS:152,155`, `R13:470`; 899,891 B);
- the **projected** set (17,899 B; 98% smaller).

Both runs gave:
- exit 1, label `findings`;
- **identical findings multisets, 21 = 21** on (file, line, class, rule, tool_call_id, timestamp, argv0, command);
- identical per-file `bash_calls`, `eval_calls`, `eval_unparsed`, `unparsed_spawns` and `lines`.

The `SS:152,155` and `R13:470` known misses stay misses, with `unparsed_spawns` 2/0 in both runs. gitleaks found no leaks in either set.

**If L1 keeps byte-exact copies (no contract change)**, the minimum is:
- assistant toolCall lines only;
- `OutputSpec:65` excluded;
- no toolResult or `custom_message` lines.

Residual risk is then F3 (LOW). The landed `r15-libinput-events.jsonl` meets this bar: 5 assistant lines, gitleaks clean.

## Checks for L1 after integration

- `gitleaks dir --no-banner --redact .ufo/waves/round-18/frozen-tripwire`, which should report no leaks.
- Confirm that no `inputs/*.jsonl` line has a `role` other than `assistant`, unless it is a declared negative control.
- If the projection is adopted: that `frozen-provenance-check.py` re-derives every projected line.
- That `--frozen` returns `frozen_match`.
