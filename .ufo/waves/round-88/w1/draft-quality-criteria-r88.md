# QUALITY criteria draft — round 88 (L1 integrates into corpus/QUALITY.md)

Numbering: the last registered criterion is **145** (`grep -nE '^[0-9]+\. ' corpus/QUALITY.md | tail -3` → 97, 98, 99;
the bold-form block runs to 145 at `corpus/QUALITY.md:1052`). These two are therefore 146 and 147, in the file's
existing style (number, statement, "Shown able to fail", "Limits").

---

**146. A resolver claim replays the host's own configuration once, and the replay's refusals are part of the claim.**
A tool that resolves effective configuration for a named host (mako, waybar, any config chain it reads) is credited
only when its claim carries one run over the host's own config chain, at a named revision, with the tool's sha256,
the command, and the refusal lines it printed; a resolver that refuses the host's own lines is reported as refusing
them, never as resolving the surface. The replay is read-only and stays inside the credential-material rule: only
the config files the chain names.
Shown able to fail: round 87's resolver, replayed at 24ba2a9ddac21c1211579231e6ee1d98963f9988 on this host,
prints `invisible='true': expects 0 or 1` for `~/.local/share/omarchy/default/mako/core.ini:15` and the same for
`:18`, and resolves `invisible` to `"0"` — the host's do-not-disturb state is not resolved
(`.ufo/waves/round-88/w1/receipt-base-host-config-r88.txt`, base tool sha256 `67a955a5…`), while the round-87 case
set carries no `invisible` token at all (22 cases; `invisible=true` 0, `invisible=false` 0).
Limits: the replay proves the tool's behaviour on the bytes present at that run, not mako's runtime behaviour; a
host config that changes after the replay is outside the claim; and a tool that refuses every line of the chain
satisfies the letter of "carries the refusals" — the claim must also state what it did resolve.
(lesson: lessons/round-88.md#mistakes M88-1)

**147. A declared counting command carries its sha pins from the freeze, and a case file is frozen before any attack
seat reads it.**
Every counting command a declaration registers names the digest of each case, mutant and figure file it reads
(`--expect-cases-sha256`, `--expect-mutants-sha256`, `--expect-figures-sha256`) at the freeze revision, so no erratum
is needed to add the pin later; and every case file is committed and pinned before the first attack seat opens it, so
a finding is about frozen bytes. A wave whose case file changes after a seat read it voids that seat's finding for
the final file and says so.
Shown able to fail: round 87's frozen C2 command omitted `--expect-figures-sha256` (erratum 6,
`corpus/lessons/round-87-verifier-spotcheck.md:25`) and its C1 case file was rewritten once during the wave, voiding
early-seat findings (erratum 4, `:26`; the voiding is recorded as M87-5 in `corpus/lessons/round-87.md`). Round 88's
declaration carries `--expect-cases-sha256` and `--expect-mutants-sha256` in both counting commands, with the mutant
digests already fixed (`40645a28…` for C1, `49373eee…` for C2).
Limits: a pin proves the bytes read are the bytes named, not that the case set is adequate (that is the mutant
population's job); a pin added by erratum after scoring is not this criterion's green; and the freeze ordering is
proved by the commit graph, not by a timestamp in the file.
(lesson: lessons/round-88.md#mistakes M88-1; outside lessons/round-87-verifier-spotcheck.md §6 R4, `:117-118`)
