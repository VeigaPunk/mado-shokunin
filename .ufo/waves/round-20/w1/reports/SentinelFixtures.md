# SentinelFixtures — landed f3da504 (already public) scans clean: 0 secrets, 0 IPs, 0 copied transcript lines; commit synthetic classes only behind the tested scan below, never real transcript lines (gitleaks cannot see them)

Scope: security of committing `.ufo/waves/round-20/w1/cases/` and `.ufo/waves/round-20/w1/corpus/`, both built from `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin`, plus a scan L1 runs before landing. Axes: (a) credentials/tokens, (b) IPs, (c) personal emails, (d) private paths, (e) copied transcript metadata (provider/account fields, private reasoning). Scratch: `/tmp/mado-r20-SentinelFixtures` (own clone; HEAD observed e629f731 at start, moved to f3da5048 for the post-landing check). Times are UTC. No values of any candidate secret appear in this report or in my tool output; prefixes (`ghp_`, `AKIA`) and lengths only.

## Publication path

- Anonymous probe, credential helpers disabled: `env GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/false git -c credential.helper= ls-remote https://github.com/VeigaPunk/mado-shokunin.git refs/heads/master` printed f3da504's full object id (f3da50488661…) for `refs/heads/master`. The lane remote is world-readable and already carries L1's round-20 landing f3da504 (20:09:29Z, "precision suite (175 scored + 12 held-out) … wave-1 evidence", 509 files: `w1/cases/` 200, `w1/corpus/pre-vs-harmed.json`, `precision/`, `precision-heldout/`, `w1/reports/` 82, `w1/drafts/` 8). The same probe found all 21 lane remotes under `/home/vgpnk/Projects/shokunin/*-shokunin` anonymously readable.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.gitignore` ignores only `.ufo/interactive-sessions/`, `.ufo/state/`, `__pycache__/`; `git check-ignore` on `w1/cases/x/a.jsonl` and `w1/corpus/pre-vs-harmed.json` returned rc 1 (committable). Fetch bodies are already digest-only through `.ufo/waves/round-20/fetch/.gitignore` (0 bodies in f3da504).
- So this review is partly after the fact: what landed is scanned below and is clean. The scan is for every later landing in this round (w2 reports, the repaired tool's corpus diff, receipts, lessons).

## Findings

### S1 — Medium — copied real transcript lines are a leak class gitleaks cannot see, and the lane has already published one twice

- Exploit path: a case author "adopts" a corpus line by copying the JSONL line (the r13 `run_record(...)` shape, RerunPrecision corpus lines), or L1 re-pins a round-20 frozen suite from the round-19 inputs, then commit, then push to the public remote.
- What a real line carries (key census of one real session file, values not read): `message.credentialId` (2-digit int), `responseId`, `usage`, `provider`, `model`, `api`, `contextSnapshot{promptTokens,…}`, `requestControls`, `providerPayload{type,provider,dt,items}`, `thinking` blocks (private reasoning) with `thinkingSignature` (provider-encrypted, 1.2 to 2.8 KB each), `toolCall.intent`.
- Already published: `.ufo/waves/round-18/frozen/inputs/*.jsonl` (added in 4c103b5) and byte-identical `.ufo/waves/round-19/frozen/inputs/*.jsonl` (01b8094): 5 files, 26 real lines, 22 thinking blocks totalling 14,015 characters of reasoning, 15 thinking signatures, plus credentialId/responseId/usage/providerPayload on every line. `gitleaks git` over the lane history (78 commits scanned) reports none of this; its single finding is a generic-api-key false positive at `.ufo/waves/round-13/w1/reports/ProtocolPhases.md:25` (a 40-hex upstream commit id after the word "access"). Canaries C4 and C11 below: gitleaks rc 0 on fixtures carrying these keys.
- Round 20 today: the 187 fixture `.jsonl` in f3da504 `precision/` + `precision-heldout/` (and the same 187 under `w1/cases/`) are all in the minimal template envelope (0 deviations, 0 copied-line markers). `W-WrapperCrossCell-r13-verbatim` copies only the code text of MadoR13.jsonl:437 and :470 under synthetic ids and timestamps, which is the compliant pattern (`.ufo/waves/round-20/precision/expected.json:1000-1002`).
- Impact: private reasoning, provider-bound encrypted payloads and account/run metadata become public and cannot be recalled; thinking text can quote any file an agent read. No credential was found in the 26 published lines (gitleaks 0; the fallback's one hit there was an `sk-` run starting mid-word inside a provider blob, a false positive).
- Smallest remediation: never commit a transcript line. Re-envelope the code/command text only (class 2 below) or keep it digest-only. A frozen pin that needs the exact r13-r15 bytes should point at the committed round-19 blobs rather than add a third copy. The scan enforces this on every `.jsonl` except `receipts.jsonl` (FINDING `fixture-real-line-markers`).

### S2 — Medium — five demonstrated ways a plain `gitleaks dir` passes these directories silently

gitleaks 8.30.1 at `/usr/bin/gitleaks` (sha256 ef931a755d99f66e…; `gitleaks version` prints "version is set by build process"; the version comes from `/var/lib/pacman/local/gitleaks-8.30.1-1/desc`, read as file bytes, no pacman run). Canary harness `/tmp/mado-r20-SentinelFixtures/run_canaries.py` (sha256 6aff9f30e5b4b93b…; fake tokens are generated at runtime and never printed; canary dirs deleted afterwards):

| canary | plain gitleaks | scan below |
|---|---|---|
| C2 inline `gitleaks:allow` on the line (one JSONL line is a whole message, so it silences everything in it) | rc 0 | `--ignore-gitleaks-allow`: gitleaks rc 3, scan exit 1 |
| C3 `.gitleaks.toml` at the target root allowlisting `.*` (config precedence 4 when no `-c`) | rc 0 | pinned `-c`: rc 3, plus suppression-file FINDING |
| C9 token inside a mode-000 subdirectory | rc 0, log `WRN skipping directory error="permission denied"`, report `[]` | exit 2 (`find failed`) |
| C13 URL userinfo password; C15 `ya29.` and `xai-` shapes (the classes of this host's own OAuth helper scripts in `~/.local/bin`) | rc 0 | fallback regex: exit 1 |
| C4/C11 copied-line keys; C5 private IP, absolute example path, extra row key in a corpus diff | rc 0 | envelope/schema/pattern checks: exit 1 |

- Exploit path: any of these reaching a landing guarded only by `gitleaks dir` gives a silent pass, then a public push.
- Remediation: the scan below (pinned config, empty ignore dir, `--ignore-gitleaks-allow`, `--redact`, leak exit code 3 distinct from errors, symlink and suppression-file check, abort on unreadable dirs, generated-canary self-test before trusting gitleaks).

### S3 — Low — corpus-diff examples carry real command text; measured clean, with known residual classes

- Shape (`.ufo/waves/round-20/corpus-diff.py`, sha256 ded258752ee46cf0…, identical in f3da504): `lost_rows` = {file (session-relative), line, class, rule, count} (:216); `added_rows[].examples` = {file, line, command = finding["command"]}, at most 20 per (class, rule, evidence) (:228-233); `"corpus": str(corpus)` absolute (:247).
- `command` is the tripwire's `redact(text)` (`tools/mado-tripwire.py` at e629f73 :201-206 and :223-227; same text at 9c54c56 :113-139): URL userinfo, `AKIA…`, and any `[A-Za-z0-9_-]{32,}` run become `<redacted>`, then the text is cut to 240 characters. The row's `argv0` is not redacted (:1596-1602), but corpus-diff does not emit it. The digest of SECRET_PATTERNS + MAX_COMMAND + redact() (command D) is `e3ce3385cb26fb99…` at 9c54c56, e629f73 and f3da504 alike.
- Upper-bound measurement (`/tmp/mado-r20-SentinelFixtures/rowscan.py`: both tool revisions over all 5,623 `.jsonl` between 19:48Z and 19:50Z, one `python3 -I tool --scan FILE` per file, all 11,246 runs exited 0 or 1): 1,638 rows at 9c54c56 and 7,405 at e629f73. gitleaks over every row: "no leaks found". IPv4: 0 rows. Email-shaped: 382 rows, 0 non-synthetic (all `.local`, example or invalid domains, plus `user@1000.service` and jj revsets). Home paths: `~/.local` or `/home/vgpnk/.local` in 708 rows, one `~/.kimi-webbridge`. Credential keywords: 1 row, a ps/date `-p` format flag (false positive). Here-string or `sudo -S` rows: 0.
- The actual `w1/corpus/pre-vs-harmed.json` (sha256 a85bc7fe8cb9f592…, 104,356 B, identical in f3da504): 5,623 files, 5,345 stable, 0 lost rows, 65 groups, 589 examples, longest command 240, 0 absolute example paths, example keys exactly {command, file, line}. gitleaks 0, fallback 0, IPv4 0, 45 email-shaped strings all synthetic or revsets, 164 `~/.local` paths, 25 examples containing `<redacted>`.
- Residual classes redact() does not cover: secrets shorter than 32 characters outside URL userinfo, base64 containing `+` or `/`, IPs, emails, paths. This matches the round-17 table at `.ufo/waves/round-17/w1/reports/SentinelTranscriptRead.md:134-137`.
- Exploit path: a classified segment (vcs_write, tool_install, host_mutation …) whose argv carries one of those residual classes, for example a short password flag or an internal host IP, becomes one of the 20 examples, then is committed and pushed. Impact: disclosure of that value. Measured instances today: 0.
- Remediation: commit after the scan. If the scan ever reports a FINDING in an example, or the landing revision changes redact()/MAX_COMMAND (command D), commit digest-only (rewrite E).

### S4 — Info — the corpus holds the risky material; none of it reached committed or round-20 bytes

- `gitleaks dir` over the corpus (default rules; a scratch config that skips only `.log` tool-output files, which the tripwire never reads; redacted report): 4.66 GB in 4m2s, 25,273 candidates. Of these, 24,869 are `sourcegraph-access-token`, which here means 40-hex object ids in files that mention "sourcegraph". The rest: 268 generic-api-key, 39 github-pat, 31 aws-access-token, 18 curl-auth-header, 13 github-app-token, 8 github-oauth, 7 jwt, 6 github-refresh-token, 6 curl-auth-user, 6 1password, 2 gitlab.
- Value-free triage (raw values only in a mode-0600 `/tmp` file, deleted after triage): 406 high-signal hits, 116 distinct values. 7 distinct values also occur in the committed lane tree, all false positives by shape: 40-hex upstream object ids (including the ProtocolPhases one), one 64-hex digest, two path fragments. 1 occurs in the round-20 dir: a tracked-path fragment, which is also the only candidate that survives into tripwire row commands (93 rows). Of 53 non-generic candidates, 3 also occur in fleet files: one `ghp_` value in the fleet root's tracked `.ufo/waves/round-9/corpus-gate.mjs` and `.ufo/waves/aggregator-r11/seats/sentinel.md` ([INFERENCE] a gate test value), and two curl `-u` placeholders. The other 50 occur only in transcripts, mostly in read/grep tool results and provider payload fields. [UNK] whether any of them is live; I did not validate them, because validating means using them. Shapes from this host's credential helpers (`ya29.`, `xai-`, `sk-ant-`, `sk-proj-`): 0 lines in the corpus.
- Outside this surface: any credential ever printed in an agent session should be treated as exposed to every reader of `~/.omp`. To get a pointer list, re-run `gitleaks dir <corpus> --redact`, which prints file:line and never values.

## Per-class recommendation

| # | class | where | decision | basis |
|---|---|---|---|---|
| 1 | synthetic fixtures in the minimal envelope (`type,id,timestamp,message{role,content[toolCall{type,id,name,arguments{language,code[,reset]} or {command}}]}`) | `w1/cases/*/*.jsonl`, `precision/`, `precision-heldout/` | COMMIT | required: `tw-precision.py` reads them through `git show PIN:` and checks their sha256, so digest-only would break the C1 counter; f3da504 scan: 0 FINDING |
| 2 | code/command text taken from a real transcript and re-enveloped (e.g. `W-WrapperCrossCell-r13-verbatim`) | same | COMMIT after the scan | only `arguments.code` or `arguments.command` survives; ids and timestamps are synthetic; the scan checks the text itself |
| 3 | real transcript lines, verbatim or trimmed (any `credentialId, responseId, usage, provider, model, api, providerPayload, contextSnapshot, requestControls, thinkingSignature, textSignature, …`; thinking/text blocks; toolResult/user records) | anywhere, including a future round-20 `frozen/inputs` | NEVER COMMIT; rewrite to class 2, or DIGEST-ONLY (sha256 + session-relative path:line, bytes stay local) | invisible to gitleaks (C4, C11); precedent 4c103b5/01b8094 is already public |
| 4 | case manifests (`cases.json`, `expected.json`: names, want rows, `why`, sha256) | `w1/cases/*/cases.json`, `precision*/expected.json` | COMMIT after the scan | free text; the only live REVIEW is `~/.local` at `w1/cases/CaseAdoptW2/cases.json:781`, which is not a secret |
| 5 | corpus-diff aggregates (refs, tool sha256, files/stable/unstable counts, totals) | `w1/corpus/*.json` | COMMIT | no transcript content |
| 6 | `lost_rows` keys (session-relative file, line, class, rule, count) | same | COMMIT | the "loses 0 findings" guard needs them; empty today; no content |
| 7 | `added_rows` example `command` (tool-redacted, ≤ 240 chars, ≤ 20 per group) | same | COMMIT after the scan; DIGEST-ONLY (command → command_sha256, rewrite E) on any FINDING or if D's digest changes | S3: 0 secrets, IPs or real emails across all 9,043 rows of both revisions |
| 8 | `corpus` root and session-relative file names (timestamps, UUIDv7 session ids, seat names) | same | COMMIT | `.omp/agent/sessions` already occurs 3,447 times in the committed tree at e629f73 |
| 9 | raw tool rows or stdout over the corpus (`tool_call_id`, `timestamp`, unredacted `argv0`, per-file sha256) | not committed so far | DIGEST-ONLY (row count + sha256 of the dump; dump stays in /tmp) | adds no evidence beyond the diff; `argv0` is not redacted |
| 10 | fetched upstream bodies | `fetch/` | DIGEST-ONLY (already, `fetch/.gitignore`) | upstream author emails, public but irrelevant |
| 11 | seat reports and drafts that quote corpus lines (adjacent surface, same risk class) | `w1/reports/`, `w1/drafts/` | COMMIT after the scan | f3da504 scan: 0 FINDING |

## Pre-landing scan (tested)

~~~
# A. extract the tested script from this report; the digest must be ea22f0c96736c47da88f029f471d0fd92efcb9ca3fb9752f76afeca4d38b5476
awk '/^```bash prelanding-scan.sh$/{f=1;next} f&&/^```$/{f=0} f' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/reports/SentinelFixtures.md > /tmp/prelanding-scan.sh && sha256sum /tmp/prelanding-scan.sh

# B. before every commit that adds round-20 files (default target: the round-20 wave dir)
#    exit 0 land | 1 fix every FINDING and rerun | 2 could not evaluate: do not land
bash /tmp/prelanding-scan.sh

# C. before every push: the round's commit range, read from a /tmp clone (also covers corpus/lessons, SOURCES, SCORECARD quotes)
#    rc 0 push | 3 triage the redacted report | anything else: do not push
rm -rf /tmp/r20-prepush /tmp/r20-prepush-noignore && git clone -q --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/r20-prepush && mkdir /tmp/r20-prepush-noignore && printf '[extend]\nuseDefault = true\n' > /tmp/r20-prepush-gl.toml && (cd /tmp/r20-prepush-noignore && gitleaks git /tmp/r20-prepush --log-opts="e629f73..refs/remotes/origin/master" -c /tmp/r20-prepush-gl.toml -i . --ignore-gitleaks-allow --redact --no-banner --no-color --exit-code 3 --report-format json --report-path /tmp/r20-prepush.json); echo "rc=$?"

# D. redaction stability before trusting example text produced by a new tool revision (both digests must be equal)
for r in 9c54c56 REV; do git -C /home/vgpnk/Projects/shokunin/mado-shokunin show $r:tools/mado-tripwire.py | python3 -I -c 'import sys,re,hashlib; s=sys.stdin.read(); a=re.search(r"^SECRET_PATTERNS = \(.*?^MAX_COMMAND = \d+$", s, re.S|re.M).group(0); b=re.search(r"^def redact\(text\):\n(?:    .*\n)+", s, re.M).group(0); print(hashlib.sha256((a+b).encode()).hexdigest())'; done

# E. digest-only rewrite of a corpus diff (plaintext stays in /tmp; the result passes the scan, canary C17)
python3 -I -c 'import hashlib,json,sys; d=json.load(open(sys.argv[1])); [e.update(command_sha256=hashlib.sha256(e.pop("command").encode()).hexdigest()) for g in d["added_rows"] for e in g["examples"]]; open(sys.argv[2],"w").write(json.dumps(d,ensure_ascii=True,sort_keys=True,separators=(",",":"))+"\n")' /tmp/PLAINTEXT.json /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/corpus/NAME.json
~~~

Triage. A FINDING is one of: a gitleaks hit; a suppression file or symlink (the link target is printed); `fixture-real-line-markers`; a token/key shape; IPv4 or a non-synthetic email in a fixture, suite manifest or corpus diff; a home path outside `Projects` inside a fixture `.jsonl` (the case contract allows only `/home/vgpnk/Projects` and `/tmp`); a corpus-diff schema violation (extra key, absolute or `..` file, command over 240, more than 20 examples, over 2 MiB). A corpus diff is recognised by location (`/w1/corpus/`) or by `"schema":"mado-corpus-diff-v1"` anywhere. Fix the file and rerun; do not waive by editing the scan. A REVIEW (home paths and emails in reports, specs and manifests; envelope deviations that carry no copied-line key; absolute paths in fixtures) is informational. Output never contains a matched value: file:line and class only, gitleaks `--redact`. That matters because L1's own transcript becomes corpus for the next round.

Evidence for the scan (script sha256 ea22f0c96736c47d…, run_canaries.py sha256 6aff9f30e5b4b93b…; last run 20:11Z):

| run | result |
|---|---|
| live round-20 wave dir, 20:11Z | exit 0; 0 FINDING; 199 REVIEW (164 home path, 35 email: upstream authors in fetch bodies, `.md.snap` filenames) |
| landed f3da504 round-20 tree (clone) | exit 0; 0 FINDING; 138 REVIEW (134 home path, 4 email) |
| commit range e629f73..f3da504 (command C) | "1 commits scanned", "no leaks found", rc 0 |
| canaries C0 to C17 (19 rows) | 19/19 expected exits: clean copies of the live cases (C0, and C12 as `precision/`) 0; C1 PAT, C2 allow-comment, C3 root config, C4 copied-line keys, C5 corpus IP/abs/extra key, C6 JSON-escaped private key, C7 PAT in a report, C10b provider email, C11 frozen copied-line keys, C13 userinfo, C15 ya29./xai-, C16 corpus diff under `evidence/` with a private IP: 1; C8 missing target and C9 unreadable dir: 2; C10a synthetic emails + escaped `@decorator`, C14 AWS doc-example key + `example.com` userinfo, C17 digest-only rewrite of the real diff: 0 |
| gitleaks absent (PATH without it) | prints `NOTE gitleaks absent: fallback token patterns only`; C1 exit 1, C0 exit 0 |
| an always-clean fake `gitleaks` first on PATH | `could_not_evaluate: gitleaks self-test rc=0: a generated canary token was not detected`, exit 2 |
| calibration on committed precedent | round-18 and round-19: exit 1, exactly 26 `fixture-real-line-markers` each (the frozen inputs) + the deliberate symlink fixtures; round-17: exit 1, 3 home paths in fixture `.jsonl`, 1 deliberately malformed line, 1 symlink (`tripwire/hardening/symlink-target.jsonl -> /etc/hostname`). These legacy suites are red by design; round 20 is green |

```bash prelanding-scan.sh
#!/usr/bin/env bash
# mado round-20 pre-landing leak scan (SentinelFixtures). Read-only on every target; writes only a fresh /tmp dir.
# usage: bash prelanding-scan.sh [TARGET ...]   default TARGET: the round-20 wave dir
# exit 0 clean | 1 findings: triage before landing | 2 could not evaluate: do not land
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
[ $# -gt 0 ] || set -- "$LANE/.ufo/waves/round-20"
OUT=$(mktemp -d /tmp/mado-r20-prelanding.XXXXXX) || { echo "could_not_evaluate: mktemp"; exit 2; }
die() { echo "could_not_evaluate: $*"; exit 2; }
command -v python3 >/dev/null || die "python3 missing"
for t in "$@"; do
  case "$t" in /*) ;; *) die "target must be absolute: $t";; esac
  [ -e "$t" ] || die "missing target: $t"
done
fail=0
# 0. suppression files and symlinks are findings (a target-root .gitleaks.toml or an inline gitleaks:allow can silence gitleaks)
sup=$(find "$@" \( -name '.gitleaks.toml' -o -name 'gitleaks.toml' -o -name '.gitleaksignore' -o -type l \) -printf '%p -> %l\n') || die "find failed"
if [ -n "$sup" ]; then echo "FINDING suppression-file-or-symlink (path -> link target):"; echo "$sup"; fail=1; fi
# 1. gitleaks: upstream default rules via an explicit config, no ignore file, inline allow comments ignored, secrets redacted
if command -v gitleaks >/dev/null; then
  printf '[extend]\nuseDefault = true\n' > "$OUT/gitleaks.toml"
  mkdir "$OUT/noignore" "$OUT/selftest" || die "mkdir"
  # self-test first: a generated canary token must be detected, else the scanner is not trusted (fail closed)
  python3 -I -c 'import secrets,string; a=string.ascii_letters+string.digits; print("{\"t\":\"%s\"}" % ("gh"+"p_"+"".join(secrets.choice(a) for _ in range(36))))' \
    > "$OUT/selftest/canary.jsonl" || die "canary generation"
  (cd "$OUT/noignore" && gitleaks dir "$OUT/selftest" -c "$OUT/gitleaks.toml" -i "$OUT/noignore" --ignore-gitleaks-allow \
     --redact --no-banner --no-color --exit-code 3 --report-format json --report-path "$OUT/selftest.json" > "$OUT/selftest.log" 2>&1)
  st=$?; rm -rf "$OUT/selftest"
  [ "$st" -eq 3 ] || die "gitleaks self-test rc=$st: a generated canary token was not detected"
  n=0
  for t in "$@"; do
    n=$((n + 1)); r="$OUT/gitleaks-$n.json"
    (cd "$OUT/noignore" && gitleaks dir "$t" -c "$OUT/gitleaks.toml" -i "$OUT/noignore" --ignore-gitleaks-allow \
       --redact --no-banner --no-color --exit-code 3 --report-format json --report-path "$r" > "$r.log" 2>&1)
    rc=$?
    case $rc in
      0) python3 -I -c 'import json,sys; sys.exit(0 if json.load(open(sys.argv[1])) == [] else 1)' "$r" \
           || die "gitleaks rc=0 but non-empty or unreadable report: $r" ;;
      3) echo "FINDING gitleaks ($t), secrets redacted, report $r:"
         python3 -I -c 'import json,sys
for f in json.load(open(sys.argv[1])): print("  %s %s:%s" % (f["RuleID"], f["File"], f["StartLine"]))' "$r" || die "unreadable gitleaks report $r"
         fail=1 ;;
      *) die "gitleaks rc=$rc on $t (log $r.log)" ;;
    esac
  done
else
  echo "NOTE gitleaks absent: fallback token patterns only (step 2)"
fi
# 2. structure + fallback patterns; prints file:line and class only, never the matched value
python3 -I - "$@" <<'PY'
import ipaddress, json, os, re, sys
TOKEN = re.compile(r"(?<![A-Za-z0-9])(?:gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{60,}|glpat-[A-Za-z0-9_-]{20}"
                   r"|xox[abpors]-[A-Za-z0-9-]{10,}|(?:AKIA|ASIA)(?![0-9A-Z]{9}EXAMPLE)[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}"
                   r"|sk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}|npm_[A-Za-z0-9]{36}|ya29\.[0-9A-Za-z_-]{20,}|xai-[A-Za-z0-9]{40,}"
                   r"|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})"
                   r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
                   r"|(?i:authorization:\s*(?:bearer|token|basic)\s+[A-Za-z0-9._~+/=-]{8,})"
                   r"|://[^/\s:@\"'<>$*]+:[^/\s@\"'<>$*]{8,}@(?!(?:[A-Za-z0-9-]+\.)*example\.(?:com|org|net)\b)")
IPV4 = re.compile(r"(?<![0-9.])(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}(?![0-9.])")
EMAIL = re.compile(r"(?<![\\\w.%+-])[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})")
NOT_MAIL = re.compile(r"(?i)(?:^|\.)(?:example\.(?:com|org|net)|invalid|test|localhost|local)$|noreply\.github\.com$"
                      r"|\.(?:service|socket|target|timer|mount|path|slice|scope|device|swap)$|\.\.")
HOME = re.compile(r"/home/[A-Za-z0-9._-]+/(?!Projects(?:/|\b))|(?<![\w/.$])~/(?!Projects(?:/|\b))|(?<![\w.])/root/|/run/user/\d")
ABS = re.compile(r"(?<![\w.~$:/-])/(?!tmp(?:/|\b)|home/vgpnk/Projects(?:/|\b))[A-Za-z0-9._-]+/[A-Za-z0-9._/-]*")
ENV_TOP, ENV_MSG, ENV_ITEM = {"type", "id", "timestamp", "message"}, {"role", "content"}, {"type", "id", "name", "arguments"}
ENV_ARGS = {"eval": {"language", "code", "reset"}, "bash": {"command", "timeout", "cwd"}}
# keys that only a copied real transcript line carries (provider/account/run metadata, encrypted reasoning)
REAL_KEYS = {"credentialId", "responseId", "usage", "provider", "model", "api", "providerPayload", "contextSnapshot",
             "requestControls", "thinkingSignature", "textSignature", "errorMessage", "errorId", "inputTransformations",
             "serviceTier", "completedAt", "ttft", "duration", "stopReason", "encrypted_content"}
CD_TOP = {"schema", "base", "new", "corpus", "files", "stable_files", "unstable_files", "base_findings", "new_findings",
          "lost_rows", "added_rows"}
fail = review = 0
def say(level, path, line, what):
    global fail, review
    print("%s %s %s:%d" % (level, what, path, line))
    if level == "FINDING": fail = 1
    else: review += 1
def ip_bad(s):
    ip = ipaddress.ip_address(s)
    doc = any(ip in ipaddress.ip_network(n) for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24"))
    return not (ip.is_loopback or ip.is_unspecified or doc or s.startswith("0."))
def keys_deep(x):
    if isinstance(x, dict):
        for k, v in x.items():
            yield k
            yield from keys_deep(v)
    elif isinstance(x, list):
        for v in x:
            yield from keys_deep(v)
def envelope(path, n, obj):
    real = sorted(set(keys_deep(obj)) & REAL_KEYS)
    if real: say("FINDING", path, n, "fixture-real-line-markers[%s]" % ",".join(real)[:120])
    bad = [] if isinstance(obj, dict) else ["not-object"]
    if not bad:
        bad += [k for k in obj if k not in ENV_TOP]
        m = obj.get("message")
        if not isinstance(m, dict) or m.get("role") != "assistant" or not isinstance(m.get("content"), list):
            bad.append("message-shape")
        else:
            bad += ["message." + k for k in m if k not in ENV_MSG]
            for it in m["content"]:
                if not isinstance(it, dict) or it.get("type") != "toolCall" or it.get("name") not in ENV_ARGS:
                    bad.append("content-item"); continue
                bad += ["toolCall." + k for k in it if k not in ENV_ITEM]
                a = it.get("arguments")
                if not isinstance(a, dict): bad.append("arguments"); continue
                bad += ["arguments." + k for k in a if k not in ENV_ARGS[it["name"]]]
    bad = sorted(set(bad) - {"message." + k for k in real} - {"toolCall." + k for k in real} - set(real))
    if bad: say("REVIEW", path, n, "fixture-envelope-deviation[%s]" % ",".join(bad)[:120])
def corpus_diff(path, doc):
    if not isinstance(doc, dict): return say("FINDING", path, 1, "corpus-json-not-object")
    extra = sorted(set(doc) - CD_TOP)
    if extra: say("FINDING", path, 1, "corpus-json-extra-keys[%s]" % ",".join(extra)[:120])
    for row in doc.get("lost_rows", []) + [e for g in doc.get("added_rows", []) for e in g.get("examples", [])]:
        if set(row) - {"file", "line", "class", "rule", "count", "command", "command_sha256"}:
            say("FINDING", path, 1, "corpus-json-row-extra-keys")
        f = str(row.get("file", ""))
        if f.startswith(("/", "~")) or ".." in f.split("/"): say("FINDING", path, 1, "corpus-json-absolute-or-dotdot-file")
        if len(str(row.get("command", ""))) > 240: say("FINDING", path, 1, "corpus-json-command-over-240")
    for g in doc.get("added_rows", []):
        if len(g.get("examples", [])) > 20: say("FINDING", path, 1, "corpus-json-over-20-examples")
def onerror(err):
    raise err  # an unreadable directory is could-not-evaluate, never a silent skip
def walk_all():
    for root_arg in sys.argv[1:]:
        walk = ([(os.path.dirname(root_arg), [], [os.path.basename(root_arg)])] if os.path.isfile(root_arg)
                else os.walk(root_arg, onerror=onerror))
        for root, dirs, names in walk:
            dirs[:] = sorted(d for d in dirs if d != ".git")
            for name in sorted(names):
                p = os.path.join(root, name)
                if os.path.islink(p): continue  # reported by step 0
                fixture = name.endswith(".jsonl") and name != "receipts.jsonl"  # transcript-shaped, wherever it sits
                suite = any(s in p for s in ("/w1/cases/", "/precision/", "/frozen/", "/tripwire/"))
                data = open(p, "rb").read()
                text = data.decode("utf-8", "replace")
                doc = None
                if name.endswith(".json"):
                    try: doc = json.loads(text)
                    except ValueError: doc = None
                # a corpus-diff output is recognised by its location OR its schema, wherever L1 writes it
                corpus = "/w1/corpus/" in p or (isinstance(doc, dict) and doc.get("schema") == "mado-corpus-diff-v1")
                strict = fixture or suite or corpus
                if corpus and len(data) > 2 * 1024 * 1024: say("FINDING", p, 1, "corpus-json-over-2MiB")
                if corpus and name.endswith(".json"):
                    if doc is None: say("FINDING", p, 1, "corpus-json-unparsable")
                    else: corpus_diff(p, doc)
                for n, line in enumerate(text.split("\n"), 1):
                    if fixture and name.endswith(".jsonl") and line.strip():
                        try: envelope(p, n, json.loads(line))
                        except ValueError: say("FINDING", p, n, "fixture-unparsable-line")
                    if any(len(set(m.group(0))) >= 8 for m in TOKEN.finditer(line)):  # AKIA000… placeholders excluded
                        say("FINDING", p, n, "token-or-key-shape")
                    if any(ip_bad(m.group(0)) for m in IPV4.finditer(line)): say("FINDING" if strict else "REVIEW", p, n, "ipv4")
                    if any(not NOT_MAIL.search(m.group(1)) for m in EMAIL.finditer(line)): say("FINDING" if strict else "REVIEW", p, n, "email")
                    if HOME.search(line): say("FINDING" if fixture else "REVIEW", p, n, "home-path-outside-Projects")
                    if (fixture or suite) and ABS.search(line): say("REVIEW", p, n, "fixture-abs-path-outside-tmp-and-Projects")
try:
    probe = "gh" + "p_" + "".join(chr(c) for c in range(65, 91)) + "abcdefghij"
    if not TOKEN.search(probe) or len(set(probe)) < 8:
        print("could_not_evaluate: fallback self-test"); sys.exit(2)
    walk_all()
except Exception as exc:
    print("could_not_evaluate: pattern step %s: %s" % (type(exc).__name__, getattr(exc, "filename", "")))
    sys.exit(2)
print("patterns: fail=%d review=%d" % (fail, review))
sys.exit(1 if fail else 0)
PY
prc=$?
case $prc in 0) ;; 1) fail=1 ;; *) die "pattern step rc=$prc" ;; esac
echo "prelanding-scan: targets=$# fail=$fail out=$OUT"
exit $fail
```

## Limits

- I did not validate whether any corpus candidate credential is live [UNK]; doing so means using it. I did not scan sibling lanes' or the fleet root's published history, other refs or tags on the remote, or whether GitHub secret scanning or push protection is enabled on it [UNK].
- The corpus measurements are snapshots: the row upper bound ran 19:48Z to 19:50Z over 5,623 files, and the gitleaks corpus pass ran 19:49Z to 19:53Z. The corpus grows with every session, this one included, so the repaired tool's corpus diff and every w2 artifact must be scanned again at landing (command B), and its example text depends on redact() staying unchanged (command D).
- The fallback patterns are heuristics. IPv4 can match version strings; email/home/IP checks run per line, so the compact one-line corpus JSON reports at most one REVIEW per class; private paths are judged against the case contract (`/home/vgpnk/Projects`, `/tmp`) and a short list of private roots. gitleaks ran with its upstream default rules only.
- I did not judge the landed cases' semantics (families, want rows), only their leak surface. My scan and canary scripts live in `/tmp` and are not lane files; the script text above is the deliverable. Unredacted triage data and canary trees were deleted (`/tmp/mado-r20-SentinelFixtures/raw`, `canary/`, `rows/`).
- Contract note: besides the listed read-only git commands (log, show, ls-tree, rev-parse, ls-remote) plus `check-ignore`, `remote -v` and `config --get-regexp`, I ran `git status --porcelain -- .ufo/waves/round-20/w1/reports/SentinelFixtures.md` once in the lane checkout at the end. It is not on the read-only list and can refresh `.git/index` stat data; it changes no content. No jj command and no other git command ran in the lane; clone, fetch and checkout happened only in `/tmp/mado-r20-SentinelFixtures/clone`.

## Installs

none. gitleaks 8.30.1 was already installed (`/usr/bin/gitleaks`, pacman package per `/var/lib/pacman/local/gitleaks-8.30.1-1/desc`). Not upgraded, because pacman is paused; no newer release was needed for these checks.
