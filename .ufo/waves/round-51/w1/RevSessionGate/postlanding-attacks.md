# Post-landing attacks: round-50 instruments

## `quality/check-session-material.py` (session gate v3)

**Strongest remaining cheat:** the privacy checks are pattern recognizers over committed blobs, not a confidentiality proof. A receipt can encode sensitive material in an unrecognized form (for example base64/hex, split across lines, or transformed into a non-matching representation) and pass; the gate also has explicit limits on object scanning and bounded text/object work, so an adversarial oversized or deeply embedded payload can seek a blind spot. The round-50 counter's canned transcript/all-rule spray demonstrates an additional instrumentation weakness: selftest output and tags alone do not establish which behavior actually ran.

**Fix candidate:** add independent black-box behavioral fixtures run against the exact committed gate bytes, with per-case expected rule and finding identity asserted (not merely a total pass count or rule-tag presence); include encoded/split sensitive canaries and truncation/limit-boundary cases. A verifier should derive its expected outputs independently rather than invoke the gate's own selftest as its oracle.

**Scope:** later round. Round 51 claims freeze different instruments and C2 content; expanding the session-material contract would exceed this round's scope.

## `quality/check-wave-done.py`

**Strongest remaining cheat:** settlement is inferred from receipt-shaped committed JSON plus dispatch/ready metadata. A forged or stale result document can name every dispatched seat and provide plausible nonempty output/note without proving that an agent actually ran or that its output corresponds to the assigned task. Thus the checker establishes internal consistency of artifacts, not execution provenance or semantic completion.

**Fix candidate:** add a separately authenticated dispatch/result linkage: bind each result to an immutable task payload digest and an execution receipt emitted by the orchestrator, and require matching round/wave/seat identity and digest. Keep this explicitly as provenance evidence, not as proof of answer quality. Also make the final integration-tip check receipt part of closure acceptance, addressing routed D1.

**Scope:** D1 is in this round's scope (commit the final WAVE-DONE receipt at integration tip or correct claims); provenance/authenticity changes belong in a later round because they alter the checker protocol.

## `quality/check-round-outcome-first.py`

**Strongest remaining cheat:** the checker identifies a round section and scores surface/first-paragraph properties using regular expressions. A report can satisfy the syntactic outcome-first shape while making a misleading, hedged, or unsupported claim in that paragraph; surface matches likewise do not establish that a substantive capability change occurred or that cited paths support it.

**Fix candidate:** add a gate arm requiring the first paragraph's outcome statement to cite concrete evidence pointers and a separate deterministic check that each referenced path exists at the assessed revision; for stronger semantic assurance, retain human review rather than treating lexical checks as truth validation. Expand fixtures with adversarial reordered/ambiguous headings, quoted process language, and unsupported outcome statements.

**Scope:** later round. No round-51 claim targets outcome-first semantics, and changing its rubric now would broaden the frozen claims.
