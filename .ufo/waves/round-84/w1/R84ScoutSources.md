# R84ScoutSources — source verification (round mado 84, wave 1)

Seat: R84ScoutSources (scout leaf, no dispatch). Date: 2026-11-04.
Assignment: reopen S486 RFC 8259 §4 and S487 Bash Reference Manual §3.2.3; verify exact quotes (≤25 words), uniqueness SHOULD vs MUST, pipefail status vs SIGPIPE; review the C1 naming-restriction framing. No production edits made; none authorized.

## Sources and method

- S486: RFC 8259 (Bray, Ed., December 2017, obsoletes 7159), fetched 2026-11-04 from https://www.rfc-editor.org/rfc/rfc8259.txt. Full text read (707 lines). Scratch copy sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`.
- S487: Bash Reference Manual, node "3.2.3 Pipelines", fetched 2026-11-04 from https://www.gnu.org/software/bash/manual/html_node/Pipelines.html. Cross-checked against the official manual shipped on this host by the bash package (bash 5.3.20-1): `/usr/share/doc/bash/bashref.html` and `/usr/share/info/bash.info.gz`; §3.2.3 wording is identical in both editions (verified by reading the local §3.2.3 body against the fetched node).
- Network limitation: www.gnu.org direct connections (curl and reader) time out from this host; Pipelines.html succeeded on the first reader fetch, remaining nodes were taken from the host's official bash-package manual instead. No other source consulted.

## S486 — RFC 8259 §4 (Objects): located quotes and uniqueness level

All quotes verbatim; §4 spans pages 6–7 of the RFC.

1. "The names within an object SHOULD be unique." — 8 words. §4, p.6.
2. "An object whose names are all unique is interoperable in the sense that all software implementations receiving that object will agree on the name-value mappings." — exactly 25 words. §4, p.6.
3. "When the names within an object are not unique, the behavior of software that receives such an object is unpredictable." — 20 words. §4, p.6.
4. "Many implementations report the last name/value pair only." — 8 words. §4, p.6.

SHOULD vs MUST: §1.1 invokes RFC 2119/8174 all-caps semantics. Uniqueness appears at SHOULD level only (quote 1). Document-wide check over the full text: the word "unique" occurs only in §4 (quotes 1–3); no MUST/REQUIRED/SHALL statement anywhere in RFC 8259 requires unique member names. The MUSTs that do exist concern other obligations (§3 value forms and lowercase literals, §7 characters that must be escaped, §8.1 UTF-8 for interchange and no added BOM, §9 parser acceptance, §10 generator conformance). The §2 grammar (`member = string name-separator value`, repeated via `*( value-separator member )`) admits duplicate names; quote 2–4 describe the consequence as interoperability guidance, not a rule.

## S487 — Bash manual §3.2.3 (Pipelines): located quotes

All quotes verbatim (the manual hard-wraps lines; each quote is contiguous in the source text). HTML emphasis/quote marks around `|` and `|&` are the manual's rendering of literal operators.

1. "A pipeline is a sequence of one or more commands separated by one of the control operators '|' or '|'&'." — 20 words. §3.2.3.
2. "The exit status of a pipeline is the exit status of the last command in the pipeline, unless the pipefail option is enabled" — 23 words; sentence continues "(see The Set Builtin)." §3.2.3.
3. "If pipefail is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status" — 22 words; sentence continues ", or zero if all commands exit successfully." §3.2.3.
4. Corroborating, The Set Builtin (`set -o pipefail`): "If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands in the pipeline exit successfully." (quoted from local bashref.html for completeness; over 25 words as a whole, provided for grounding, not as a ≤25-word quote).

## Pipefail status versus SIGPIPE

- §3.2.3 itself never mentions SIGPIPE. It defines pipeline status purely in exit-status terms (quotes 2–3 above).
- Manual-wide check on the bash 5.3 official manual: zero occurrences of "SIGPIPE" in `/usr/share/doc/bash/bashref.html` (17,852 lines) and zero in `/usr/share/info/bash.info.gz`. The Signals node (§3.7.6) covers trapping/ignored-signal behavior (SIGINT, SIGQUIT, SIGTERM, SIGHUP, job-control signals) and does not discuss SIGPIPE. [INFERENCE from the zero-count plus node inspection: SIGPIPE handling is left to default disposition; the manual makes no pipefail–SIGPIPE statement.]
- What the manual does ground (Exit Status, §3.7.5): "When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status." — 21 words, verbatim (local bashref.html; wording matches §3.7.1's waitpid/128+n sentence). §3.2.3's pipefail rule keys on non-zero status, so a producer terminated by SIGPIPE (signal 13 → status 141) is surfaced by pipefail, while a zero-status tail masks it under the default last-command rule — exactly the C2 before/after shape (unguarded rc0 vs guarded rc7-style propagation).
- Scope note: pipefail's non-zero selection is manual text; the 141 mapping for SIGPIPE is the 128+N rule applied to signal 13 and was not probed on this host (no probes assigned).

## C1 naming restriction — review

Claim under review: C1 is "a restriction of the join's input grammar, NOT a claim that layer-shell globally requires unique namespaces", sourced to S486 "JSON uniqueness guidance".

- Consistent with S486: RFC 8259 gives uniqueness only SHOULD-level standing; duplicate names are grammatically legal and receiver behavior is explicitly "unpredictable", with "Many implementations report the last name/value pair only" — which matches the declared before-state (held tool silently keeps the last repeated allocation key). Refusing duplicates in the tool's own input grammar is therefore a stricter-than-protocol local restriction, not an assertion of a protocol guarantee. The framing "protocol does not promise namespace uniqueness" is correct for S486.
- Caveats for the report reader: RFC 8259 speaks of object member *names*; it never uses the word "namespace". S486 directly grounds only the duplicate-allocation-keys class (analogous duplicate keys). The duplicate-bar-namespace and duplicate-extra-namespaces classes rest on the tool's own identity grammar and the layer-shell domain, which are outside my two assigned sources and were not verified here. [INFERENCE: the analogy is fair for duplicate keys; it does not by itself constrain layer-shell namespace semantics.]

## Verdict summary

- S486 quotes located and exact; uniqueness is SHOULD, never MUST, in RFC 8259 — "protocol does not promise namespace uniqueness" holds as stated.
- S487 §3.2.3 quotes located and exact; online node wording identical to the host's bash 5.3 manual.
- pipefail vs SIGPIPE: §3.2.3 and the whole manual are silent on SIGPIPE; pipefail's rule is exit-status-based; fatal-signal exit mapping (128+N, §3.7.5) is the manual's own ground for a SIGPIPE death producing a non-zero status.
- Sources census: two assigned sources opened and quoted; no credential-era artifacts, session dumps, or authentication files touched. Exit condition for this seat: report written; no counter/probe execution assigned to this seat was run.

## Tooling record

Per /home/vgpnk/.omp/agent/RULES.md: no tools installed or upgraded (curl, coreutils, and the host bash package's bundled manual sufficed). No pacman transactions. No git/jj operations. No service, compositor, or config mutation. Scratch `/fast/scratch/hyaku/mado-r84/R84ScoutSources` created for the RFC receipt copy and removed after this report was written.
