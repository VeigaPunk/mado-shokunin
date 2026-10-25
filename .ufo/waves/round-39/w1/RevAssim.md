# RevAssim — round-39 w1 assimilation adoption spot-check

Role: UFO-FSD reviewer (leaf). Scope: spot-check the dispatcher amendment adoption per
registration.md §Assimilation. Read-only; no files written outside this seat. No tools
installed (read-only inspection; nothing needed).

Environment: lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`; git HEAD =
`457d1b125932c1e0d797061a2156b917bcd7edaa` (round-39 freeze commit); base =
`08be4eb7fd13358ed29b096e8924005d46ac409c`. No round-39 data commit has landed yet — all
w1 artifacts above are uncommitted (git status: untracked only).

## 1. S220 quote vs fetch receipt (verbatim, ≤25 words, located) — PASS

- Source re-opened: `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/`
  (0.56.0 Dispatchers page), fetch receipt `.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin`,
  297,863 B, sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`
  (byte-identical to the scout's `SctDispatchersPage/S220.bin`).
- Entry quote (amendment §1 + lesson GATE S220 + rows draft): "Their purpose is to be fed
  into hl.bind() or hl.dispatch()." — **10 words** (≤25). Located: raw HTML lines
  2937–2938, opening `<p>` of the `#dispatchers` section (h2 anchor `id="dispatchers"` at
  line 2937), page revision "Last updated on July 15, 2026".
- Verbatim check: `sed -n '2935,2940p' S220.bin` shows the paragraph:
  `<p>Dispatchers return tables that describe an action you want to make. They do not invoke
  any action immediately, and their contents are not guaranteed to be stable at all. Their
  purpose is to be fed into <code>hl.bind()</code> or <code>hl.dispatch()</code>.</p>`
  The sentence is byte-present with `<code>` inline tags; rendered text is exactly the quote.
  A strict bytes-verbatim alternative "Dispatchers return tables that describe an action you
  want to make." (11 words) is also present at raw offset 262669 — noted in the lesson's
  spot-check table. Verdict: quote accurate, rendered-verbatim, ≤25 words, located.

## 2. S018 (HyprCtl.cpp@efb5099) quotes vs held receipt — PASS

- Held receipt `.ufo/waves/round-24/fetch/S158.bin` sha256
  `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — matches the
  amendment header's S018 hash and the S018 row hash.
- All five cited quotes found at exactly the cited upstream line numbers (grep/sed on
  S158.bin):
  - `:1149` → `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(DISPATCHSTR);`
    (5 words)
  - `:1151` → `return "Invalid dispatcher";` (3 words)
  - `:1131` → `// For lua, this is just a wrapper for `eval("hl.dispatch(in)`
    (10 words); `:1132` → `std::string evalStr = std::format("return hl.dispatch({})", in);`
    (6 words)
  - `:1310` → `// split by ; ignores ; inside [] and adds ; on last command` (14 words;
    amendment cites 1309–1310, line 1310 holds the comment)
  - `:2096` → `request = request.substr(sepIndex + 1); // remove flags and separator so we
    can compare the rest of the string` (19 words)
- All ≤25 words and located. The amendment's §2 INF follows the quoted evidence.

## 3. Held knowledge file append vs replace — NOT YET APPENDED (data tip pending)

- `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` in the current worktree is
  byte-identical to the freeze commit: `git diff HEAD -- <file>` → 0 lines; `git diff
  08be4eb..HEAD --stat -- <file>` → 0 (no change at freeze). Holds the full round-32 text
  ending at §4 ("What this entry does not claim"); grep for "Amendment"/"2026-10-25" returns
  nothing — the file has NOT been replaced.
- The adoption block exists only as a draft:
  `.ufo/waves/round-39/w1/ScrDispatcherAmendment/dispatcher-amendment-section.md` (dated
  "## Amendment — re-grounded … (2026-10-25)", structured as an appended section, held text
  untouched). It has not yet been spliced into the held file; no data commit carries the
  append.
- Since HEAD is still the freeze commit, a base→tip diff of the held file cannot be produced
  yet. **Verification gap**: re-run after the data commit lands — `git diff
  08be4eb..<data-tip> -- corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`
  must show only end-of-file additions. If the wave closes without the append, the
  assimilation is unadopted (the draft would then be a dangling artifact).

## 4. Refused package entries remain refused with reasons (lesson Gate) — PASS

- `ScrLesson/round-39.md` Gate lists exactly four refused package entries with reasons:
  event-queue-host-measurement-r28.md (null channel `debug:disable_logs=1`; corrected by
  event-queue-observability-r37.md), event-queue-journal-measurement-r29.md (same null
  channel), socket-client-contract-measurements-r29.md (64 KiB cap is chonkstep's own cap,
  S277 `:61`), socket-modes-and-request-read-r30.md (frozen registration declines successor
  chain; covered by S158/S187/S253). All four match the round-38 lesson `:40-43` refusal
  reasons verbatim. Staged register stays unassimilated — consistent with registration.

## 5. Additional finding (adjacent to scope, same assimilation chain): stale S219 Gate receipt hash

- Lesson GATE S219 binds `sha256=9787b53b298216aee93ec1193814e2972d9fef9125656ce9ed0bd03ed7fbcf59`
  but the current worktree `tools/mado-options.py` (37,358 B) hashes
  `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e`. Docstring line 2
  ("mado-options.py - static resolver of the config-tree option table.") matches the quote,
  but the bound bytes differ. The draft's own trim notes (SimplDraftTrim) flag this and
  instruct re-hashing at data tip (`git show <data-tip>:tools/mado-options.py | sha256sum`).
  The GATE line must be updated to the committed bytes before closure.

## Summary

- S220 quote vs receipt: PASS (verbatim rendered, 10 words, located).
- S018 quotes vs held receipt: PASS (5/5 at cited lines, ≤25 words).
- Appended-never-replaced: precondition intact; append not yet landed → verify after data tip.
- Refused entries remain refused with reasons: PASS.
- Residual risk: S219 receipt hash stale; instruction append and S219 tool bytes must be bound
  in the data commit, and the held knowledge file diff re-checked at tip.
