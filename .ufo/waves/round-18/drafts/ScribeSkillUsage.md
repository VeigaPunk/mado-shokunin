Insertion points (integrator applies; this draft does not edit SKILL.md):
- (a) `### Frozen tripwire replay (round 18)` goes after the round-17 tripwire section, before `## Gate registry` (SKILL.md:541).
- (b) Rule 7 goes after rule 6 and before the closing line `Persist nothing into config trees` (SKILL.md:252-254).

---

### Frozen tripwire replay (round 18)

Run `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` from the lane root. It reads the five committed, SHA-256-pinned incident inputs under `frozen/inputs/` (each with clean controls), reruns the classifier on those bytes, and compares the result with `frozen/expected.json`. It never reads a live transcript. Exit map: 0 `MADO_TRIPWIRE_FROZEN: frozen_match` (scan exit, label and the (file, line, class, rule) multiset equal the pin; no `known_misses` line fires); 1 `frozen_verdict_mismatch` (a pinned finding is missing, an unpinned finding appears, the exit or label differs, or a known miss now fires); 2 could-not-evaluate: `snapshot_tampered` (digest mismatch, or a missing, symlinked or unlisted `.jsonl` input), `unpinned_legacy` (input entry without `sha256`), `frozen_error` (malformed `expected.json` or scan failure). The verdict JSON carries `tool_sha256`; the pin does not, so cite that digest beside any frozen result.

It proves change detection only: the classifier's output on these pinned incident lines is the same as when the pin was written. It does not prove classifier correctness on any other input, that a seat's commands were never run, that the snapshot was copied faithfully from its transcript (provenance is the author's claim; the tool does not check it), or that unpinned lines are clean. It is not prevention, interception or host repair. A `known_misses` line that starts firing is a fixed miss to re-pin, not a regression pass.

Re-pin rule: copy input lines byte-exactly from source; update the `sha256` values in `expected.json` and `provenance.json` together; re-derive `expected_findings` and `known_misses` from a receipt the current tool produced on the new bytes, and cite its `tool_sha256`. Never hand-edit an input without both digests, and never re-pin to clear a mismatch without naming the classifier change that caused it.

---

7. **Fetch receipts — one line per fetch, credit on 200 only.** Every `curl` fetch appends exactly one `mado-fetch-receipt-v1` line to `.ufo/waves/round-18/fetch/<seat>/receipts.jsonl`, including non-200 fetches. Fields: `url`, `final_url`, `http_status`, `fetched_at` (UTC, `Z`), `bytes`, `sha256`, `body`, `tool`. Only a receipt with `http_status` 200 whose body re-hashes may back a SOURCES row or a quote; a 404 or error body is recorded and never credited. HTML bodies are digest-only: the receipt keeps `sha256` and `bytes`, and the body is not committed, because such pages carry per-request `nonce`, `request-id` and `csrf_tokens` values that make the digest non-reproducible. Tokens never enter the lane: no cookies, auth or session headers (`-H`, `-b`, `-c`), no session URLs, and no token value in any receipt, body, report or transcript excerpt. Fetch with the fenced form only: `curl -sSL --max-time 60 -o BODY -w '%{http_code} %{url_effective}' URL`. The `fetch-verify` probe does not yet enforce the 200 gate; this rule binds the seat until it does.
