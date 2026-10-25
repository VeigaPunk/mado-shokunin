# RevEntryLimits — sentence-level audit of `corpus/knowledge/request-limits-upstream-r31.md` vs S253.bin

Round 38 wave 1, reviewer leaf. No tool installs (none needed). Lane production files untouched;
all commands were read-only network fetches plus local diffs under /tmp.

## Items and verdicts

### I1 — The two constants, verbatim incl. whitespace — PASS

Command:
```
diff <(awk 'NR==43||NR==44' .ufo/waves/round-38/fetch/S253.bin) \
     <(grep -o '`static constexpr[^`]*`' corpus/knowledge/request-limits-upstream-r31.md | tr -d '`')
```
Output: `IDENTICAL` (exit 0). Preceding `cat -A` on the fetched lines showed no trailing
whitespace and fixed the exact spacing:

```
static constexpr size_t REQUEST_LIMIT      = 1024 * 1024;$
static constexpr size_t FOLLOW_QUEUE_LIMIT = 64 * 1024;$
```

S253.bin:43-44 = entry's quoted lines exactly — 6 spaces between `REQUEST_LIMIT` and `=`,
1 space between `FOLLOW_QUEUE_LIMIT` and `=`. 1 MiB = `1024 * 1024`, 64 KiB = `64 * 1024` as stated.

### I2 — `:118` check inside `readRequest` — PASS

grep on S253.bin: `readRequest` declared at S253.bin:111 (`bool CUnixPeer::readRequest(...)`),
check at S253.bin:118: `if (m_input.size() > REQUEST_LIMIT)` → `return false` at :119. Line and
function membership match the entry. Semantics: trips only when accumulated size exceeds the
limit, so "bounded at 1 MiB" is accurate.

### I3 — `:166` check inside `addFollowData` — PASS

`addFollowData` declared at S253.bin:165, check at S253.bin:166:
`if (queuedBytes() + data.size() > FOLLOW_QUEUE_LIMIT)`; `queuedBytes()` at :210-211 is
`m_output.size() - m_writeOffset` — genuinely the followed stream's queue, as the entry says.

### I4 — "file does not exist at host tag" 404 claim — PASS

Command: `curl -fsSIL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/ipc/s1/Unix.cpp`
Output (2026-10-25):
```
exit=22
curl: (22) The requested URL returned error: 404
HTTP/2 404
```
Tag identity additionally verified (the entry claims this hash is "the host's tag v0.56.2"):
`git ls-remote https://github.com/hyprwm/Hyprland 'refs/tags/v0.56.2' 'refs/tags/v0.56.2^{}'` →
```
efb50993780079460b0cbed1363e2166a2de1d9f	refs/tags/v0.56.2
```
Single ref line = lightweight tag pointing directly at `efb5099…`, so v0.56.2 **is** that commit.
The entry's UNK clause is fully grounded.

### I5 — Refused-draft characterization (r29 64 KiB claim) — PASS with 2 LOW notes

Draft read at `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/socket-client-contract-measurements-r29.md` (exists; the entry's `merge/mado/…/socket-client-contract-measurements-r29.md` elision resolves to it). Draft §1 quotes S243:

> "There is no `/tmp` fallback. Requests are capped at 64 KiB"

and the draft's own UNK admits it measures a third-party re-implementation, not Hyprland. The
r31 re-point is supported: 64 KiB is exactly `FOLLOW_QUEUE_LIMIT` (S253.bin:44, follow-queue
ceiling), while the request ceiling upstream now declares is 1 MiB (S253.bin:43) — so "not a
request ceiling" is true of the code that matters for the lane's host contract.

- **LOW (quote case)**: r31 quotes the draft as "requests are capped at 64 KiB" (lowercase r);
  the draft reads "**R**equests are capped at 64 KiB". Trivial, but it is a verbatim-quote
  context — suggest matching case or dropping quotation marks.
- **LOW (parse)**: "is the *follow-queue* ceiling of a different implementation" is ambiguous:
  S253 proves 64 KiB is *Hyprland upstream's* follow-queue ceiling; it does not prove anything
  about chonkstep's (the draft's source, S243) own queue internals. The supported reading —
  "the figure matches the follow-queue ceiling upstream now declares (S253 :44), not a request
  ceiling" — holds; the other reading (attributing the 64 KiB queue ceiling to chonkstep) is
  unestablished. Wording, not a fact defect; claim is marked INF.

## Bonus checks (entry scaffolding)

- **S253 ↔ claimed commit identity — PASS**: fetched raw bytes at
  `a1c2428f79b3b05c3fd36c27378e3538c8c6a014/src/ipc/s1/Unix.cpp`; sha256 of both =
  `3ba8e461bd466a8a716a7a29a2a917d94a4d9af6fb87904a2c76978f4833d6cf`; `cmp` → BYTE-IDENTICAL,
  408 lines each. The entry's "source: S253 @ commit a1c2428…" is honest.
- **S158 `:2270-2280` citation — PASS**: S158.bin:2270-2279 shows the v0.56.2 handler
  `read(ACCEPTEDCONNECTION, readBuffer.data(), 1023)` accumulating into `request` with
  `if (messageSize < 1023) break` and no total bound — exactly the entry's "accumulates
  1023-byte chunks with no total bound".

## Findings summary

| Item | Verdict |
|---|---|
| I1 constants verbatim | PASS |
| I2 :118 in readRequest | PASS |
| I3 :166 in addFollowData | PASS |
| I4 404 at host tag (= v0.56.2 = efb5099) | PASS |
| I5 refused-draft characterization | PASS, 2 LOW notes (quote case; "of a different implementation" parse) |
| Info | Entry says "current upstream"; upstream `main` is now `c4e7596a…` (a1c2428 no longer tip). Constants are commit-pinned and `recheck: on-release` covers drift — informational only. |

No FAIL findings. No blocked items. Residual risk: none material; the two LOW notes are wording
polish, both inside clearly-marked INF/quote contexts.
