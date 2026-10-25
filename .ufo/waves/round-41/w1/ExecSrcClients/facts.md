# C2 client-side and tracker facts — seat `ExecSrcClients`, round 41 w1

Every row below was re-opened this seat from the frozen fetch receipts under
`.ufo/waves/round-41/fetch/`. The `sha256` column is the digest of the whole receipt file (recomputed
this seat, not copied). `locator` is `fetch/<file>:<line>` or `fetch/<file>:<first>-<last>` relative to
the lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Verification: `python3 -I .ufo/waves/round-41/w1/ExecSrcClients/verify-facts.py` asserts, per row, (1) the
file's sha256 equals the row's, (2) the quote is 3–25 whitespace-separated words (the C2 gate bound), and
(3) the quote occurs in the receipt's text normalized exactly as `PRED-C2-r41-v1` clause d normalizes it
(`<script>`/`<style>` removed, tags removed, entities decoded, whitespace collapsed), both over the whole
file and over the named line range.

| fact | quote | locator | sha256 |
|---|---|---|---|
| A client wraps an already-created `hyprland_focus_grab_v1` proxy and initializes it on construction | `FocusGrab::FocusGrab(::hyprland_focus_grab_v1* grab) { this->init(grab); }` | fetch/quickshell-grab.cpp:11 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| Adding a window means: add_surface, queue it as pending, require a commit | `this->add_surface(window->surface()); this->pendingAdditions.append(window); this->commitRequired = true;` | fetch/quickshell-grab.cpp:66-68 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| Removing a window calls remove_surface and only re-arms the commit; the client does not deactivate locally | `this->remove_surface(waylandWindow->surface()); this->commitRequired = true;` | fetch/quickshell-grab.cpp:60-61 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| `sync()` is a no-op while a transaction is open — commits are deferred | `if (this->transactionActive) return;` | fetch/quickshell-grab.cpp:72 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| After committing, the client clears the pending list and flips to active on the first addition | `this->pendingAdditions.clear(); if (!this->active) { this->active = true; emit this->activated();` | fetch/quickshell-grab.cpp:81-86 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| Client's stated reason for not tracking destruction: `cleared` always arrives on deactivation (next comment line adds "even if it was due to window destruction") | `the protocol will always send cleared() when the grab is deactivated` | fetch/quickshell-grab.cpp:78 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| Transaction open: later `sync()` calls are swallowed | `void FocusGrab::startTransaction() { this->transactionActive = true; }` | fetch/quickshell-grab.cpp:91 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| Transaction close: flag down, then one `sync()` | `this->transactionActive = false; this->sync();` | fetch/quickshell-grab.cpp:93-95 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| The `cleared` event is the client's only deactivation signal: it clears `active` and re-emits to the app | `void FocusGrab::hyprland_focus_grab_v1_cleared() { this->active = false; emit this->cleared(); }` | fetch/quickshell-grab.cpp:98-101 | 6f7cecf15a4dbfd0dc39341c8794639595a83dd2a4ab13b6b377ac970a301a40 |
| The portal logs every advertised global before any branch | `Got interface: {} (ver {})` | fetch/xdph-PortalManager.cpp:88 | 15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55 |
| The portal has exactly one registry callback and it routes every global into `onGlobal` | `registry->setGlobal([this](CCWlRegistry* r, uint32_t name, const char* iface, uint32_t ver) { onGlobal(name, iface, ver); })` | fetch/xdph-PortalManager.cpp:300 | 15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55 |
| Sibling Hyprland managers do get a bind branch — the bind pattern the focus-grab manager is denied | `if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)` | fetch/xdph-PortalManager.cpp:99 | 15c3e39cea5af1a92924ebc1ffe0f7825c86ac3c0b49e894aede86b2e091ea55 |
| The running portal logged the focus-grab advert exactly once, at LOG level | `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` | fetch/xdph-journal.txt:117 | bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7 |
| Issue title | `New windows in inactive workspaces stealing focus` | fetch/issue-565.html:144 | 148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc |
| Expected behavior (rule-level focus control: `silent` should withhold focus) | `If a workspace windowrule contains silent then matching windows should not get focus, unless that window's workspace is already the active one.` | fetch/issue-565.html:659 | 148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc |
| Actual behavior (transient focus steal, then focus returns) | `it seems to steal it momentarily and then give it right back to the previously focused window` | fetch/issue-565.html:661 | 148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc |
| Reported rule, second repro (pavucontrol pinned silent to workspace 4) | `windowrule = workspace 4 silent,^(pavucontrol)$` | fetch/issue-565.html:656-657 | 148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc |
| Reported rules, first repro (browser pinned silent to workspace 1) | `windowrule = workspace 1 silent,^(librewolf)$ windowrule = workspace 1 silent,^(firefox)$` | fetch/issue-565.html:647-649 | 148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc |
| Reporter's environment claim (built from source, current at posting) | `I'm running both Hyprland and wlroots built from source, cloned less than an hour before posting this issue` | fetch/issue-565.html:662 | 148a9053e813a7d912c3c2e9fdb234ef42d20004438d33b41f1110d37679d1dc |

## What the portal does NOT do with `hyprland_focus_grab_manager_v1`

Evidence, in the order it was gathered:

1. `grep -n 'focus_grab\|FocusGrab\|focus-grab' fetch/xdph-PortalManager.cpp` → exit 1, no output. The
   string `hyprland_focus_grab_manager_v1` does not occur in the portal's registry handler file at all.
2. `onGlobal` (fetch/xdph-PortalManager.cpp:85-261) is the whole handler. Its first statement after the
   log line is the branch chain. `grep -n wl_registry_bind fetch/xdph-PortalManager.cpp` yields nine
   calls naming nine distinct interfaces: `zwlr_screencopy_manager_v1` (:90),
   `hyprland_global_shortcuts_manager_v1` (:95), `hyprland_input_capture_manager_v1` (:99),
   `zxdg_output_manager_v1` (:102), `hyprland_toplevel_export_manager_v1` (:110), `wl_output` (:118),
   `zwp_linux_dmabuf_v1` (:126), `wl_shm` (:232), `hyprland_toplevel_mapping_manager_v1` (:242). One
   further global is handed to a helper that binds it itself (`zwlr_foreign_toplevel_manager_v1` →
   `CToplevelManager(name, version)`, :234). `hyprland_focus_grab_manager_v1` is in neither set — it is
   not bound and not even handed to a helper.
3. The only registry callback is the one at :300, and it forwards unconditionally to `onGlobal` (:301
   forwards `global_remove` to `onGlobalRemoved`, which only prunes outputs, :263-265). So a global that
   `onGlobal` does not name can only reach the log statement at :88 — there is no second dispatch path.
4. The host journal shows that is exactly what happened: one line, at LOG level, and nothing else
   (`fetch/xdph-journal.txt:117`, sha256 `bf8fa91a…`). `grep -n focus_grab fetch/xdph-journal.txt`
   returns that single line; `grep -c 'Got interface'` returns 78, so the focus-grab advert is one of 78
   adverts in the captured run and the only one mentioning the interface.

Therefore: the portal **logs the advert and does nothing else with it** — no `wl_registry_bind`, no
portal object, no proxy, no capability gate. Consequence for the C2 entry: the focus-grab manager is
advertised to *every* client of the compositor, not brokered through the portal, so the portal is not a
policy point for it (contrast the input-capture manager at :99, which the portal does wrap). Scope limit:
only `src/core/PortalManager.cpp` was opened this seat; the claim is bounded to the file that owns the
registry handler, and the handler is provably the only registry callback in that file.

## Client lifecycle (quickshell @ 9b0f339b19057f4731bf3b48293307d7ef241671, `src/wayland/hyprland/focus_grab/grab.cpp`)

- The file is compiled against the generated client header for this protocol:
  `grep -n 'client-protocol.h' fetch/quickshell-grab.cpp` → `7:#include <wayland-hyprland-focus-grab-v1-client-protocol.h>`
  (that include line cannot be a gate quote: clause d strips `<…>` as a tag, so it vanishes from normalized text).
- Lifecycle: `addWindow` → (surface exists? `addWaylandWindow` → `add_surface` + pending + `commitRequired`)
  → `sync()` → `commit()` → pending list cleared → `active = true` + `activated()` emitted. If the surface
  does not exist yet, the add is deferred to `QWaylandWindow::surfaceCreated` (:22-36).
- `sync()` is transactional: it returns early while `transactionActive` (:72), and
  `completeTransaction()` clears the flag and calls `sync()` once (:93-95), so a batch of window adds
  produces one commit.
- Deactivation is entirely event-driven: `hyprland_focus_grab_v1_cleared()` sets `active = false` and emits
  `cleared()` (:98-101). The client does not deactivate on `removeWindow` (:57-62) and says why in the
  comment at :78-79 — the compositor always sends `cleared`, even when the grab ended because a window was
  destroyed. So a client that removes its last surface waits for the compositor's event rather than
  inferring deactivation.
- Consequence for the entry: the `cleared` event is not advisory; for this real client it is the sole
  authority on grab termination, and the client's own `active` flag is a mirror of compositor state.

## Issue #565 metadata (tracker)

Extracted deterministically by `.ufo/waves/round-41/w1/ExecSrcClients/extract-issue.py` from the single
`react-app.embeddedData` JSON payload in the saved page (full output:
`.ufo/waves/round-41/w1/ExecSrcClients/issue-565-extract.txt`).

- Repository/URL: `https://github.com/hyprwm/Hyprland/issues/565`; number `565`.
- Title: `New windows in inactive workspaces stealing focus` (also rendered at `fetch/issue-565.html:144`).
- Author: `rrredface`. Created: `2022-08-23T14:03:55Z`.
- State: `CLOSED`, `stateReason: COMPLETED`. Closure: one `ClosedEvent`, `createdAt 2022-08-25T23:08:33Z`,
  actor `vaxerski` (event id `CE_lADOHA7HmM5QWRQZzwAAAAGw7b4-`). No `ReopenedEvent` in the page
  (`grep -c ReopenedEvent` → 0); the two `ClosedEvent` matches are the same event serialized twice.
  These fields live only in the stripped `<script>` payload, so they cannot be gate quotes — they are
  reported here from the extract, with `fetch/issue-565.html:644` as the byte locator.
- The issue body is present twice in the page: once as JSON in the script at `:644`, once rendered as
  HTML at `:646-662`. Only the rendered copy survives clause-d normalization, so quotes must be taken
  from `:646-662` (all table rows above are).
- Text-node order of the body (index from the extract, blank lines skipped):
  `000 To reproduce:` → `001 One way is…` → `002-003` browser rules → `004` web-notifications repro →
  `006-007` `sleep 5; pavucontrol` → `008-009` framing → `010` pavucontrol rule → `012 Expected behavior:`
  → `013` the `silent` sentence → `015 Actual behavior:` → `016` the steal-and-return sentence →
  `018` environment line. The order matters for the entry: the expected/actual pair is stated *after* both
  repros and the rules, i.e. the reporter frames focus withholding as a rule-level contract
  (`silent` ⇒ no focus) before describing the observed focus transfer.

## Notes for the entry author (not facts)

- Gate quotes are unique per source id in `PRED-C2-r41-v1`, and each cited id needs a *distinct* receipt
  path and sha256. The four receipts here are distinct (`quickshell-grab.cpp`, `xdph-PortalManager.cpp`,
  `xdph-journal.txt`, `issue-565.html`), each ≥ 512 bytes, so one quote per id is available from this set.
- Hazard 1: clause d strips `<[^>]+>`, so any quote containing a C++ template/`#include` angle bracket is
  destroyed by normalization. Avoid them (the include line above is cited by command, not by quote).
- Hazard 2: a literal `|` inside a quote is fine for the counter but breaks a pipe table; none of the
  quotes above contains one.
- Hazard 3: backticks do not survive either — `<code>` tags are stripped and the backticks in the issue
  body's markdown are not in the rendered HTML. The expected-behavior quote therefore reads
  `contains silent then`, not ``contains `silent` then``.

## Seat state

- Wrote only `.ufo/waves/round-41/w1/ExecSrcClients/` and this report. No tracked file, no git/jj
  mutation, no journal command, no compositor/Wayland contact, no package transaction.
- No subagent dispatched (the single labrat allowance was not needed: every field was extracted by a
  deterministic script over committed bytes).
- Tooling: none installed; `python3` stdlib only.
