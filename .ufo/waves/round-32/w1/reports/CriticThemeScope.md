# CriticThemeScope — theme fit, refusal, already-held, province boundary

Seat: critic, round-32 w1. Scope: item-10 contract (one theme, 1–3 entries,
≥1 admit AND ≥1 reject with reason + flip in the lesson's `## Gate`). Sources
read: `MERGE-REPORT.md` (61 staged entries), `PROVINCE.md`,
`corpus/QUALITY.md`, `corpus/README.md` coverage map + frontier, the three
candidate entries, and the boundary candidates named below.

## Verdicts per candidate

| candidate | verdict | ground |
|---|---|---|
| `ipc-contract-r25.md` | **ADMIT** | New ground; closest held material is inventory-only |
| `dispatcher-semantics-r25.md` | **ADMIT** | New layer (Lua `hl.dsp.*` object model); held inventory is the hyprlang bind layer |
| `dispatcher-surface-and-request-grammar-r26.md` | **ADMIT** | New claims on an already-held *file* (S018/S158 HyprCtl.cpp); the cited lines were never anchored |
| `compositor-focus-manipulation-literature-r26.md` | **REJECT** | Out of province on three independent grounds; the refusal to record (below) |

The contract's ≥1 admit + ≥1 reject is satisfied inside C1 without touching
the counter: the reject is a *considered* package entry, not one of the three,
so `entries=3 rows=5 cited_entries=3` is still reachable.

## 1. One theme or two

**ONE theme: the Hyprland IPC request/dispatch contract on the host's 0.56.x
line.** The attack worth making is the two-theme split — "socket transport"
(ipc-contract) vs "dispatcher surface" (the other two) — and it fails:

- All three entries bind the same registered frontier item
  (`corpus/README.md:91-93`: "dispatcher behavior … arc gap ledger §6"; the
  entries' `ground:` lines all name F1/U1). The registration declares them as
  a single claim C1 (`registration.md:16-36`) with one frozen counter
  (`entries=3 rows=5 cited_entries=3`). Splitting would either kill C1 or
  require a second unregistered claim — not open to the wave.
- The third entry (`dispatcher-surface-and-request-grammar-r26`) is itself the
  fusion: §1 the dispatcher *set* at the host's release, §2 how the *request
  socket* resolves a dispatcher name (`m_dispatchers.find`, "Invalid
  dispatcher", flag-strip at `:2096`, batch split at `:1309`). A two-theme
  reading forces this entry to be cut in half — evidence the pair is one
  mechanism, not two adjacent ones.
- The chain is causal: `[flags]/command args` grammar (ipc-contract §1) →
  server-side flag strip + registry resolution (r26 §2) → dispatcher objects
  described by `hl.dsp.*`/`hl.dispatch()` (semantics §1) → `event()` writes
  back to socket2's `EVENT>>DATA` framing (semantics §2 ↔ ipc-contract §2).
  Same code path (HyprCtl.cpp ↔ EventManager.cpp, same pinned commit
  `efb50993`).

Contrast test: a genuinely two-theme pick in this package would be
`chinese-translation-drift-r31` + `gkeep-size-to-real-size-r11` — no shared
mechanism. Ours share one.

Risk, stated: "one theme" is broad enough to also absorb the socket-measure
entries (`request-socket-live-bound-r8`, `socket-client-contract-*-r29`…) —
but the contract caps at 1–3 entries, so breadth is a non-issue; fit, not
exhaustion, is the test.

## 2. The refusal to record

**Refuse `compositor-focus-manipulation-literature-r26.md`** (arXiv:2604.18860
preprint, "window focus hijacking" on X11). Strongest refusal in the package
because it misses the province on three independent grounds, and its own text
supplies the evidence:

- *No owned-surface claim.* Its OBS/INF concern a threat model (observation-
  to-action gap, X11 focus redirect), not `~/.config/**`, an owned tool, or
  this host's display behavior. PROVINCE owns "the Hyprland/waybar/walker
  configuration plane and display behavior **on this host**"; a preprint's
  X11 experiment is neither. Its `ground:` line claims F1 "per-window rule
  effects" — but U1 is about *this host's* rules; the entry carries zero
  host-anchored claim.
- *Self-declared off-target* (its §3): "experiments target X11/its test
  environment, not Hyprland 0.56.2; there is no Hyprland-specific
  measurement." The host runs Hyprland on Wayland — the source is
  off-protocol and off-version at once.
- *Unclosable under the lane's own rules* (its UNK): testing "would require
  running an untrusted client against a live session — outside this lane's
  authority." An entry whose own unknown is outside the lane's authority can
  never be rechecked here — permanent tier-B ballast, which fails the spirit
  of QUALITY 2/16 (claims the lane can re-derive).

Drop-in for the lesson's `## Gate` (registry reject form matches
S012/S045/S062 style):

> **REJECTED: `corpus/knowledge/compositor-focus-manipulation-literature-r26.md`
> (row S201, arXiv:2604.18860).** Reason: out of province — the entry's claims
> are an X11 threat-model preprint, not the host's configuration plane or
> display behavior on this host; its own §3 states no Hyprland-0.56.2
> measurement exists, and its own UNK states verification requires running an
> untrusted client, which the lane may never do. The `ground: F1` line borrows
> U1 ("per-window rule effects") for a source that cannot bind to it.
> **Flip:** admit only if (a) `PROVINCE.md` gains a dated refinement owning
> compositor-security literature as a mado surface, or (b) the same source is
> re-scoped to a *corroborating row* under an entry whose claims live on an
> owned surface (e.g. a host-measured focus-grab note citing S201 as
> background) — S201 then rides as a mined `used-by` source, never as a
> standalone entry.

Same-class alternates if the L1 wants a different reject or a second:
`wayland-input-security-literature-r8.md` (S261/S262 — pure academic
literature, its INF is "academic grounding … has been missing", no owned-
surface claim) and `privileged-client-surface-r29.md` (S227 — a community blog
analysis; same class the lane rejected at S012: third-party restatement). Both
flips identical in shape. Do not refuse all three if the L1 wants the
focus-grab chain to keep its explanatory frame — refuse the weakest one and
record the boundary for the rest (§4).

## 3. Already-held check — none of the three is held

Swept `corpus/knowledge/` + `corpus/README.md` coverage map for
dispatcher/socket/request-grammar content:

- **`ipc-contract-r25` — not held.** Held: the socket *files' existence*
  (`hyprctl-verification-layer.md:29-31` — `.socket.sock`, `.socket2.sock`
  srwx under `/run/user/1000/hypr/<sig>/`; `config-health-report-r3.md:165-168`)
  and one socket2 *consumer* (`remaining-planes-census.md:236` — the socat
  monitor-watch); client-side path derivation `getRuntimeDir()+"/"+sig+
  "/.socket.sock"` (S169, cited `bind-table-r25.md:66`). Not held anywhere:
  the `[flags]/command args` grammar, synchronous-eval freeze hazard,
  `EVENT>>DATA\n` framing, 1024-char truncation + newline flattening, backlog
  10, the 44-name catalogue diff.
- **`dispatcher-semantics-r25` — not held.** Held: the *hyprlang* dispatcher
  vocabulary — `keybind-rule-semantics.md` §3, a 24-dispatcher inventory,
  `[INF-docs]` semantics, live counts. Not held: the Lua `hl.dsp.*`
  description-objects, `hl.dispatch()` wrapper, the upstream instability
  caveat (S188:9), `event()`/`force_idle`/`dpms` semantics. Different layer —
  config-era object model vs bind-table grammar. The r24 rule-attribution
  note's Lua surface is `set_enabled`/`get_windows`, not `hl.dsp`.
- **`dispatcher-surface-and-request-grammar-r26` — not held as a claim; its
  source *file* is held.** S018/S158 already pin `src/debug/HyprCtl.cpp` at
  `efb50993`, but their recorded anchors cover `:346-484, :613-630,
  :647-723, :1463-1645, :2003-2044` — getprop, clients, layers, rule lists.
  The entry's claims sit at `:1132` (Lua wrap), `:1149`/`:1151`
  (`m_dispatchers.find` / "Invalid dispatcher"), `:1309` (batch split),
  `:2096` (flag strip) — none inside a held anchor. Admit with a `used-by`
  extension on S018, not a new row; the package's S196 is genuinely new.

One consistency flag for the reviewers, not a refusal:
`rule-attribution-r24.md` (round-25 erratum) records **45** socket2 event
names from 76 `postEvent` call sites in source; `ipc-contract-r25` §4 records
**44** names in the published *catalogues*. Different populations (source call
sites vs documented table) — both can be true, but ReviewEntryIPC should
confirm the diff was over the catalogue and not the code.

## 4. Package boundary — clearly out of mado's province

61 staged entries; the clear outs, for the L1's boundary record:

**Translation/localization coverage (claims about foreign-language wikis, not
the host) — 11 entries:**
`two-literature-coverage-r25`, `two-literature-drift-r26`,
`chinese-wiki-canonical-url-r28`, `zh-wiki-snapshot-semantics-r29`,
`chinese-article-revision-r30`, `chinese-translation-drift-r31`,
`chinese-wiki-revision-list-r7`, `chinese-wiki-ipc-section-r7`,
`cn-framing-coverage-r8`, `chinese-ipc-framing-absence-r13`,
`japanese-input-observation-methods-r14`. Each entry's claim is about a wiki
corpus (its revision, URL, framing presence/absence), never about an owned
config tree or this host's display. A *sourced doc surface* is in province
only when it documents an owned surface; these own nothing here.

**Security literature / third-party analysis — 3 entries:**
`compositor-focus-manipulation-literature-r26` (the recommended reject,
above), `wayland-input-security-literature-r8`, `privileged-client-surface-r29`
(blog analysis). Domain background, tier B/C; no host- or config-anchored
claim, and r8/r29 supply no measurement the lane can recheck.

**Unrelated tools / session-manager internals — 1 clear, 1 arguable:**
`uwsm-app-daemon-unit-r7` — the app-daemon's unit synthesis is the
systemd-user session plane; PROVINCE's own table keeps unit-state ground with
tsukuroi ("unit-health ground … stays tsukuroi's"). Clear out → report to
tsukuroi. `update-check-and-app-lifecycle-r31` is split: §1 (the
omarchy-update producer) sits in the bar-producer chain — in; §2 (app lifetime
= uwsm/pkill) is the same session-manager out. Arguable, not clear.

**In-province, for completeness:** everything else — the socket/request
measurements (`request-socket-live-bound-r8`, `socket-client-contract-*`,
`host-request-socket-cap-r7`, `request-limits-upstream-r31`, `hyprctl-flags-r28`,
`socket-modes-and-request-read-r30`, `event-*`), waybar producer/module
entries, host idle-lock chain entries, gkeep geometry/rule entries,
`weather-glyph-render-r7`, `focus-grab-*` (Wayland protocol surface =
display behavior; they stand on their own protocol sources even if the
literature entries are refused), `focus-control-surfaces-r28`,
`host-bar-and-idle-binding-r26`, `host-*-producers-*`, `idle-*`.

## Risks handed to L1

- If the L1 instead refuses a *candidate*, C1's `entries=3` counter dies —
  honest stop, per registration kill rule. The clean path is the one above:
  three admits + the literature reject.
- `dispatcher-semantics-r25` is single-source (S188, pinned wiki commit) —
  thin but within bar; its own UNK already flags the version gap that r26
  then closes. Admit pair-order matters only narratively.
- S018 `used-by` extension must list the r26 entry or ReviewUsedByClosure
  will flag it.
