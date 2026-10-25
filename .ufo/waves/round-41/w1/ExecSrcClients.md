# ExecSrcClients — client-side and tracker facts for the C2 entry (round 41, w1)

Status: DONE. Facts table at `.ufo/waves/round-41/w1/ExecSrcClients/facts.md` (19 rows, all verified).
No tracked file touched, no git/jj mutation, no journal command run (the saved journal receipt was read),
no compositor/Wayland contact, no package transaction, no subagent dispatched.

## Deliverables

| path | role |
|---|---|
| `.ufo/waves/round-41/w1/ExecSrcClients/facts.md` | the `fact \| quote \| locator \| sha256` table (19 rows) + the portal negative finding + issue metadata |
| `.ufo/waves/round-41/w1/ExecSrcClients/verify-facts.py` | asserts every row: sha256 of the receipt, quote 3–25 words, quote ∈ `norm(receipt)` **and** ∈ `norm(named line range)`, with `norm` copied from `PRED-C2-r41-v1` clause d |
| `.ufo/waves/round-41/w1/ExecSrcClients/verify-facts.txt` | the run: `VERIFY rows=19 failed=0`, exit 0 |
| `.ufo/waves/round-41/w1/ExecSrcClients/extract-issue.py` | deterministic extraction of issue #565 from the page's single `react-app.embeddedData` JSON |
| `.ufo/waves/round-41/w1/ExecSrcClients/issue-565-extract.txt` | that extraction: metadata, verbatim body, ordered text nodes |

Reproduce: `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-41/w1/ExecSrcClients/verify-facts.py`

## Receipts re-opened (sha256 recomputed this seat)

```
6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40  fetch/quickshell-grab.cpp        (2568 B)
15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55  fetch/xdph-PortalManager.cpp     (24182 B)
bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7  fetch/xdph-journal.txt           (19130 B)
148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc  fetch/issue-565.html             (475170 B)
```

Each is ≥ 512 bytes and distinct, so each can back one cited registry id under clause d.

## 1. What the portal does NOT do with `hyprland_focus_grab_manager_v1`

**It logs the advert and nothing else.** No bind, no portal object, no proxy, no capability gate.

- `grep -n 'focus_grab\|FocusGrab\|focus-grab' fetch/xdph-PortalManager.cpp` → **exit 1, no output**.
- `onGlobal` (`xdph-PortalManager.cpp:85-261`) is the entire handler and the first statement after the log
  line is its branch chain. `grep -c wl_registry_bind` → **9**, naming nine interfaces: screencopy (:90),
  global-shortcuts (:95), input-capture (:99), xdg-output (:102), toplevel-export (:110), wl_output (:118),
  dmabuf (:126), wl_shm (:232), toplevel-mapping (:242); one more (`zwlr_foreign_toplevel_manager_v1`,
  :234) is handed to a helper that binds it. Focus-grab is in neither set — not bound, not delegated.
- There is exactly one registry callback, `xdph-PortalManager.cpp:300`, forwarding unconditionally to
  `onGlobal`; `global_remove` (:301) only prunes outputs (:263-265). A global that `onGlobal` does not name
  can therefore only reach the log at :88 — no second dispatch path exists in the file.
- The host journal shows exactly that outcome: one line, LOG level —
  `fetch/xdph-journal.txt:117` → `[LOG]  | Got interface: hyprland_focus_grab_manager_v1 (ver 1)`
  (2026-10-25T13:36:24-03:00, pid 1952). `grep -n focus_grab fetch/xdph-journal.txt` returns that single
  line out of `grep -c 'Got interface'` = **78** adverts.

Entry consequence: the focus-grab manager is advertised straight to every compositor client, so the portal
is **not** a policy point for it — contrast `hyprland_input_capture_manager_v1` (:99), which the portal
does wrap. Scope limit: only `src/core/PortalManager.cpp` was opened; the claim is bounded to the file that
owns the registry handler, and that handler is provably the file's only registry callback.

Located quotes (all ≤ 25 words):

- `xdph-PortalManager.cpp:88` — `Got interface: {} (ver {})` (5 words) — the unconditional log.
- `xdph-PortalManager.cpp:300` — `registry->setGlobal([this](CCWlRegistry* r, uint32_t name, const char* iface, uint32_t ver) { onGlobal(name, iface, ver); })` (14 words) — the only dispatch.
- `xdph-PortalManager.cpp:99` — `if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)` (4 words) — the bind pattern focus-grab is denied.
- `xdph-journal.txt:117` — `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` (5 words) — the observed advert.

## 2. A real client's grab lifecycle (quickshell @ 9b0f339, `src/wayland/hyprland/focus_grab/grab.cpp`)

Compiled against the generated client header (`:7` `#include <wayland-hyprland-focus-grab-v1-client-protocol.h>` —
cited by command, not by quote: clause d strips `<…>` as a tag, so that line cannot be a gate quote).

Lifecycle, with locators:

1. Construction wraps an existing `hyprland_focus_grab_v1` proxy: `:11`
   `FocusGrab::FocusGrab(::hyprland_focus_grab_v1* grab) { this->init(grab); }`.
2. Add a window → `add_surface` + append to pending + require a commit: `:66-68`
   `this->add_surface(window->surface()); this->pendingAdditions.append(window); this->commitRequired = true;`
   (if the surface does not exist yet, the add is deferred to `QWaylandWindow::surfaceCreated`, `:22-36`).
3. Remove a window → `remove_surface` + re-arm the commit only: `:60-61`
   `this->remove_surface(waylandWindow->surface()); this->commitRequired = true;` — **no local deactivate**.
4. `sync()` is transactional and commits once: `:72` `if (this->transactionActive) return;`; `:91`
   `void FocusGrab::startTransaction() { this->transactionActive = true; }`; `:93-95`
   `this->transactionActive = false; this->sync();`.
5. On commit the client clears pending and flips active on the first addition: `:81-86`
   `this->pendingAdditions.clear(); if (!this->active) { this->active = true; emit this->activated();`.
6. The `cleared` event is the **only** deactivation authority: `:98-101`
   `void FocusGrab::hyprland_focus_grab_v1_cleared() { this->active = false; emit this->cleared(); }`.
   The client says why it keeps no local destruction tracking — `:78`
   `the protocol will always send cleared() when the grab is deactivated` (11 words), continued at `:79` by
   "even if it was due to window destruction, so we don't need to track it."

Entry consequence: for a real client, `cleared` is not advisory — it is the sole signal that the grab
ended, and the client's `active` flag is a mirror of compositor state, not an independent record.

## 3. Issue #565 (tracker, rule-level counterpart)

Extracted from the page's single `react-app.embeddedData` JSON (full output in
`issue-565-extract.txt`; JSON locator `fetch/issue-565.html:644`).

- `https://github.com/hyprwm/Hyprland/issues/565` — number **565**, author **rrredface**, created
  **2022-08-23T14:03:55Z**.
- State **CLOSED**, `stateReason: COMPLETED`. Closure: one `ClosedEvent`, **2022-08-25T23:08:33Z**, actor
  **vaxerski** (event `CE_lADOHA7HmM5QWRQZzwAAAAGw7b4-`, databaseId 7263338046). `grep -c ReopenedEvent` → 0;
  the two `ClosedEvent` hits are the same event serialized twice (identical id and databaseId).
- These metadata fields exist only inside the `<script>` payload, which clause d strips, so they are
  reported here and must not be used as gate quotes.

Located quotes (all from the rendered body `:646-662`, the only copy that survives normalization):

- `:144` title — `New windows in inactive workspaces stealing focus` (7 words).
- `:658-659` — `Expected behavior:` then `If a workspace windowrule contains silent then matching windows should not get focus, unless that window's workspace is already the active one.` (22 words; note the
  rendered HTML drops the markdown backticks around `silent`).
- `:660-661` — `Actual behavior:` then `it seems to steal it momentarily and then give it right back to the previously focused window` (17 words).
- `:656-657` — `windowrule = workspace 4 silent,^(pavucontrol)$` (5 words) — the second repro's rule.
- `:647-649` — `windowrule = workspace 1 silent,^(librewolf)$ windowrule = workspace 1 silent,^(firefox)$`
  (10 words) — the first repro's rules, contiguous after the two code lines are collapsed.
- `:662` — `I'm running both Hyprland and wlroots built from source, cloned less than an hour before posting this issue` (18 words).

**Text-node order of the body** (index from the extract, blank lines skipped):
`000 To reproduce:` → `001` browser-rule framing → `002-003` librewolf/firefox rules → `004` web-notification
repro → `006-007` `sleep 5; pavucontrol` → `008-009` framing → `010` pavucontrol rule →
`012 Expected behavior:` → `013` the `silent` sentence → `015 Actual behavior:` → `016` the steal-and-return
sentence → `018` environment line. The expected/actual pair comes **after** both repros and all three rules:
the reporter states focus withholding as a rule-level contract (`silent` ⇒ no focus) first, then the
observed transient focus transfer. That is the rule-level counterpart the entry needs — the protocol-level
grab and the `silent` windowrule are two different mechanisms for the same user-visible effect.

## Facts table (headline rows)

Full table: `facts.md`. Verified: `VERIFY rows=19 failed=0` (`verify-facts.txt`).

| fact | quote | locator | sha256 (short) |
|---|---|---|---|
| client ctor wraps the proxy | `FocusGrab::FocusGrab(::hyprland_focus_grab_v1* grab) { this->init(grab); }` | quickshell-grab.cpp:11 | 6f7cecf1 |
| add = surface+pending+commit | `this->add_surface(window->surface()); this->pendingAdditions.append(window); this->commitRequired = true;` | quickshell-grab.cpp:66-68 | 6f7cecf1 |
| remove ≠ deactivate | `this->remove_surface(waylandWindow->surface()); this->commitRequired = true;` | quickshell-grab.cpp:60-61 | 6f7cecf1 |
| sync deferred by transaction | `if (this->transactionActive) return;` | quickshell-grab.cpp:72 | 6f7cecf1 |
| active flip on first addition | `this->pendingAdditions.clear(); if (!this->active) { this->active = true; emit this->activated();` | quickshell-grab.cpp:81-86 | 6f7cecf1 |
| cleared always arrives | `the protocol will always send cleared() when the grab is deactivated` | quickshell-grab.cpp:78 | 6f7cecf1 |
| cleared handler | `void FocusGrab::hyprland_focus_grab_v1_cleared() { this->active = false; emit this->cleared(); }` | quickshell-grab.cpp:98-101 | 6f7cecf1 |
| portal logs every global | `Got interface: {} (ver {})` | xdph-PortalManager.cpp:88 | 15c3e39c |
| single registry dispatch | `registry->setGlobal([this](CCWlRegistry* r, uint32_t name, const char* iface, uint32_t ver) { onGlobal(name, iface, ver); })` | xdph-PortalManager.cpp:300 | 15c3e39c |
| sibling manager is bound | `if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)` | xdph-PortalManager.cpp:99 | 15c3e39c |
| observed advert | `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` | xdph-journal.txt:117 | bf8fa91a |
| issue title | `New windows in inactive workspaces stealing focus` | issue-565.html:144 | 148a9053 |
| expected | `If a workspace windowrule contains silent then matching windows should not get focus, unless that window's workspace is already the active one.` | issue-565.html:659 | 148a9053 |
| actual | `it seems to steal it momentarily and then give it right back to the previously focused window` | issue-565.html:661 | 148a9053 |
| rule (2nd repro) | `windowrule = workspace 4 silent,^(pavucontrol)$` | issue-565.html:656-657 | 148a9053 |
| rules (1st repro) | `windowrule = workspace 1 silent,^(librewolf)$ windowrule = workspace 1 silent,^(firefox)$` | issue-565.html:647-649 | 148a9053 |

## Hazards for the entry author

1. **Angle brackets die.** Clause d applies `re.sub(r"<[^>]+>", "", …)` to *every* receipt, so any quote
   containing a C++ template or `#include <…>` is destroyed. The client's include line is cited by command
   in `facts.md`, never as a quote.
2. **Backticks die.** `<code>` tags are stripped from the rendered issue HTML, so the expected-behavior
   quote reads `contains silent then`, not `` contains `silent` then ``.
3. **Pipes.** A literal `|` inside a quote is fine for the counter but breaks a markdown pipe table; no
   verified quote above contains one.
4. **Script payload is invisible to the counter.** Issue state/author/dates live in the `<script>` JSON that
   clause d strips; they are report facts, not quotable evidence.
5. **Quote uniqueness.** Clause d requires distinct quotes, paths and shas per cited id. The four receipts
   here are distinct, and the 19 verified quotes are all distinct — one per id is available.

## Risks / blockers

- The portal finding is file-bounded: only `src/core/PortalManager.cpp` was opened (the receipt the L1
  fetched). If xdph bound the manager in another translation unit the claim would need widening; the
  registry callback argument above is what makes the file-bounded claim sufficient (one dispatch path).
- The journal advert is the only occurrence in the 153-line capture; the receipt is a saved journal, not a
  live run — this seat ran no `journalctl`.
- The issue page is a 2026-10-25 snapshot; state is as of that fetch, and the page carries no reopened event.
- No blockers; nothing left unreachable.

## Seat hygiene

- Wrote only `.ufo/waves/round-41/w1/ExecSrcClients/` and this report.
- Read-only git not needed; no mutating git/jj anywhere; no `/tmp` scratch created (the extractor reads the
  frozen receipts in place).
- No subagent dispatched — the single labrat allowance was unnecessary because every field came from a
  deterministic script over committed bytes.
- Tooling: nothing installed; Python 3 stdlib only (`json`, `re`, `hashlib`, `html`).
