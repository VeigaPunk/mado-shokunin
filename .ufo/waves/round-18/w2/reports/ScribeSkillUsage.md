# ScribeSkillUsage — round 18 wave 2 report

Scope: draft (a) the `Frozen tripwire replay (round 18)` usage paragraph and (b) safety rule 7 on fetch receipts, both for `SKILL.md`. Only the draft file was written; no SKILL.md, tool, corpus, fetch or lane byte was changed. No git or jj command was run. No tool was installed or upgraded. No host, package, service, compositor or config-tree command was run.

Draft: `.ufo/waves/round-18/drafts/ScribeSkillUsage.md` (3,332 B). Insertion points are stated in its header: (a) before `## Gate registry` (SKILL.md:541); (b) after rule 6, SKILL.md:252.

## Behavior

**(a) Frozen replay paragraph.** Entry: `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen`. Exit map taken from the tool's own docstring (`tools/mado-tripwire.py:23-34`) and `run_frozen` / `frozen_snapshot` / `emit_frozen` (`:858-1052`):
- 0 `frozen_match`: scan exit, label and the (file, line, class, rule) multiset equal the pin, and no `known_misses` line fires.
- 1 `frozen_verdict_mismatch`: missing or extra finding, exit or label differs, or a known-miss line fires (`:1040-1049`).
- 2 `snapshot_tampered` (digest mismatch, or missing, symlinked or unlisted `.jsonl`), `unpinned_legacy` (no `sha256`), `frozen_error` (malformed expected.json, scan failure).
- The verdict carries `tool_sha256` (`:865`), which is not pinned in `expected.json`; the draft tells the reader to cite it.

Proves: change detection of the classifier on the five pinned inputs (`frozen/inputs/`: r13-global-capture, r13-root, r14-review-source-bar, r14-source-safety, r15-libinput-events). Does not prove: correctness, prevention, snapshot provenance (the docstring at `:35-37` says so), or cleanliness of unpinned lines. Re-pin rule follows `frozen/README.md:18-20`.

**(b) Rule 7.** Style matches rules 1–6 (bold title, direct sentences, parenthetical references). Content: one receipt line per fetch including non-200; credit only `http_status` 200 with a re-hashing body; HTML digest-only; no tokens in any lane byte; the fenced curl form (`gen_w1.py:32` and the lane fetch fence). The draft states that `fetch-verify` does not yet enforce the 200 gate, so the rule is not presented as a tool gate.

## Commands run (all read-only)

- `read` of SKILL.md:225-256, :525-610; SCORECARD.md (round-18 declared claims `:931-984`, round-17 tail); `corpus/lessons/round-18.md`; `frozen/README.md`; `tools/mado-tripwire.py:1-40, :844-1055`.
- `ls` / `grep -n` over SKILL.md, SCORECARD.md, `drafts/`, `frozen/`, `fetch/`.
- `cat`/`python3 -c` over `fetch/*/receipts.jsonl` (read-only parse): 305 receipt lines, 0 bad JSON; `http_status` counts `200: 300`, `404: 5`; keys match the schema on every line.
- `find fetch -name '*.html'` (13 committed HTML bodies, 2 of them in `ReopenS094/`).
- `grep -l -i -E 'nonce|request-id|csrf|authenticity_token|x-request|_gh_sess|octo-'` over those 13 bodies: 10 matched. Key names only; **my grep printed truncated fragments (about 12 characters) of `nonce` and `request-id` values into this session's output. They are not reproduced here.**
- `grep -n http_status .ufo/waves/round-18/fetch-verify.py` → no matches (exit 1): the verifier never reads the status.
- `grep -rn` of the 404 digests (`4e0dcc9e…`, `d5558cd4…`, `e3b0c442…`) and of the 404 URLs in `corpus/SOURCES.md`, `corpus/knowledge`, `corpus/README.md`: no SOURCES row cites any of them. The only URL hit is `corpus/knowledge/theme-route-r18.md:130`, which lists the 404 probes as **non-credited**.
- `sed` of `w1/reports/RevFetchReceiptContract.md:20-34, 70-100` (the wave-1 finding F1 on the 404 credit gap, with a fixture reproduction).

Not run: `tools/mado-tripwire.py --frozen`, `--selftest`, `fetch-verify.py` and any gate. The item asked for drafted text, and the exit map was taken from code. The integrator should run the frozen replay once before applying (a) to confirm the cited exit map against the frozen expected file.

## Findings (for the integrator; not fixed here)

1. **The 200-only credit rule is not enforced.** `fetch-verify.py` ignores `http_status` (grep above). Five 404 receipts exist: `NoteTheme:6, :7, :15`, `SrcElephantProviders:19`, `SrcThemeAlternates:5`. Wave-1 `RevFetchReceiptContract.md` F1 reproduced a 404 fixture credited as `ROW … receipted` / `QUOTE … ok`, exit 0. Today no SOURCES row cites those digests or URLs, so no current row is credited by a 404. Rule 7 states the target; the verifier needs a status gate before the claim can be called enforced.
2. **Committed HTML bodies carry per-request tokens, against the rule's intent.** 10 of 13 committed `.html` bodies contain `nonce`, `request-id` and/or `csrf_tokens` keys (`NoteTheme/` ×5, `ReopenS094/` ×2, `SrcWalkerDocsSite/` ×2, `MadoR18.SrcWalkerThemes/xdg-base-directories-rs.html`). Largest: `SrcWalkerDocsSite/gitbook-walker-and-elephant.html` 348,136 B. Removing committed bodies is a cutover decision for the integrator (it is outside this draft's write scope).
3. **S094 says "digest-only HTML" but its HTML bodies are committed.** `corpus/SOURCES.md:106` describes "digest-only HTML" for the matte-black tree listings. `fetch/NoteTheme/omarchy-themes-matte-black-tree.html` (229,027 B) and `fetch/ReopenS094/tree-theme.html`, `tree-theme-2.html` (229,036 B each) are committed. This conflicts with the row's own text; the integrator should decide whether to amend the row (append-only) or retire the bodies.
4. **Lesson/policy consistency.** `corpus/lessons/round-18.md` Gate section already rejects HTML pages as sole support because per-fetch tokens make the digest irreproducible. Rule 7's digest-only clause matches that line; no contradiction there.
5. **Receipts wording.** `frozen/README.md` says the expected findings came from tool `962919ce…` receipts. The verdict-level pin does not bind the tool, so a later classifier change that keeps the same verdict still reads `frozen_match`. The draft's "cite `tool_sha256`" sentence covers this; no code change is proposed.

## Out of scope (not touched)

- SKILL.md, SCORECARD.md, `corpus/SOURCES.md`, fetch bodies, receipts, `frozen/`, `tools/`, and the three `drafts/TwMiss*.patch` / `TwInstallerChannels.patch` drafts (round-19 by contract).
- No `pacman`, `sudo`, `systemctl`, `omarchy`, `hyprctl` or socket command; no REA/browser tool.

## Artifacts

- `.ufo/waves/round-18/drafts/ScribeSkillUsage.md` (the draft; the only file written besides this report).
- `.ufo/waves/round-18/w2/reports/ScribeSkillUsage.md` (this report).

## Tool installs

None.
