# R54W2Seat32 — w2 falsification: C2 semantic overclaim control

Seat: R54W2Seat32 (connector, w2 item 32). Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Scratch: `/fast/scratch/hyaku/mado-r54/R54W2Seat32` (removed before yield; see §7).
Leaf seat: no subagent, no background job, no git/jj mutation, no lane/source/predicate/registration edit, no host read, no install.

## 1. Attacked claim and frozen lines

Item 32 attacks **PRED-C2-r54**: a structurally valid C2 entry whose prose paraphrases or overstates its pinned source.

Frozen text used:

- `claims-frozen.md` L55–65 (predicate): clause (a) provenance trio + index + registry leg; clause (b) each row `mined`, `opened` 2026-10-27, commit-pinned, and "its `teaches`/quote cell's located quote (≤25 words) occurs verbatim in the round-54 pin"; clause (c) ≥2 frozen host-set citations; clause (d) six controls rejected.
- `claims-frozen.md` L73–75 (do-nothing control) and L70–71 (kill rule): both are about forged controls, a recycled entry, a stub, or a missing row. No do-nothing or control route concerns prose.
- `claims-frozen.md` L82–84 (causal separability): C2 reads the entry, `corpus/README.md`, rows S375–S377 and the pins. It does not say which entry text is evidence.
- `registration.md` C2 table L61–65 (S375–S377 quote and quote-location), host set L73–76, C2 controls L80–87. Of the six controls, only CTL-1 mutates a quote, and it mutates the **row** quote (`S376 row quote → sends arguments via a socket`), not entry prose. No control mutates entry prose, and no frozen leg maps a prose sentence to a cited span.
- `w1/R54Seat32.md` (my w1 report): item 3 (S376 frozen quote absent from pin because of `*uwsm-app*` emphasis at pin L60; S375 location 117–118 vs quote 117–119; CTL-1 not discriminating under the literal judge); S4 (host-join strings); S5 (`S375–S377` en-dash source line); S6 (entry was untracked at freeze time). All of these are re-verified or still relevant below.

## 2. What the three pinned spans actually say (pinned bytes, hashes verified)

`sha256sum -c SHA256SUMS.txt` in the fixture copy: `uwsm-0.27.1-README.md: OK`, `uwsm-0.27.1-main.py: OK`, `uwsm-0.27.1-uwsm-app.1.scd: OK` (lane pins `.ufo/waves/round-54/fetch/`).

| row | frozen quote | pinned span | what the span is about |
|---|---|---|---|
| S375 | "Difference between environment state before and after preparation is exported into systemd user manager (and D-Bus activation environment if reference D-Bus implementation is used)" | `uwsm-0.27.1-README.md` L117–119 (quote spans 3 lines) | Inside the README bullet list under L109 "On startup a specialized unit **prepares environment**". It is the uwsm preparation unit exporting into the systemd user manager. It is not an application-launch statement. |
| S376 | "uwsm-app client sends arguments to uwsm's app daemon via a pipe." | `uwsm-0.27.1-uwsm-app.1.scd` L60 (`*uwsm-app* client sends …`) | Client-to-daemon **transport**. It says nothing about which environment the launched process receives. |
| S377 | `unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"` | `uwsm-0.27.1-main.py` L3714 | Unit-name construction. Not environment. |

Pinned text the frozen rows do **not** cite, but which is what "uwsm-app's environment" would have to rest on:

- `uwsm-0.27.1-README.md` L235–237: `uwsm-app` is "a drop-in replacement of `uwsm app`".
- `uwsm-0.27.1-README.md` L585–592: for `uwsm app`, scopes are "executed in-place … inheriting environment and pty of origin"; services are "given an environment based on the current state of the activation environment of systemd".
- `uwsm-0.27.1-uwsm-app.1.scd` L15–17: "Analogous to *uwsm app* command and uses the same arguments … same parser."
- `uwsm-0.27.1-main.py` L146–152: `Varnames.session_specific` = {XDG_SEAT, XDG_SEAT_PATH, XDG_SESSION_ID, XDG_SESSION_PATH, XDG_VTNR}. `WAYLAND_DISPLAY` is **not** in this set.
- `uwsm-0.27.1-main.py` L3732–3741 (inside `app()`): scope branch appends `--scope` (L3733) with no `--setenv`. Service branch adds `--setenv={var}=…` only for `sorted(Varnames.session_specific)` that are set (L3738–3740).

## 3. Candidates (isolated fixture, scratch only)

Fixture: `D=/fast/scratch/hyaku/mado-r54/R54W2Seat32/fx.Ityh`, created with `mktemp -d -p`, `git -C "$D" init -q`, and `test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"` → `TOPLEVEL_OK`. Copies: lane pins + `SHA256SUMS.txt`, lane `corpus/SOURCES.md` (byte-equal, `cmp` exit 0), lane `corpus/README.md` plus one appended index line. No commit was made.

- **A — literal**: states only what S375/S376/S377 say, and says it "makes no claim about which environment a launched application receives".
- **B — overstated**: "uwsm-app hands the session environment to every application it launches … Therefore every process started through uwsm-app inherits WAYLAND_DISPLAY and the compositor's session variables, and the owned chain is covered end to end." Quotes are verbatim. Three full-path host strings are cited.
- **C — forged prose**: same structure as B, but the S376 quote in the **prose** is `uwsm-app client sends arguments via a socket.` (not in the pin). Host strings: 2.

Probe: `/fast/scratch/hyaku/mado-r54/R54W2Seat32/ref_c2_clauses.py`. It implements clauses (a)–(c) literally from the frozen text (not the lane counter, which does not exist). It has two **non-frozen** flags, printed in every output line and used only to isolate the prose question: `--judge strip-emphasis` (drops `*` from the pin before whitespace-collapse) and `--ignore-status` (skips the `mined` leg). Clause (d) is not run.

## 4. Measured results (verbatim outputs; the fixture has no commit, so commands are relative to `$D`)

Frozen judge, frozen status leg:

```
== A literal, frozen
clause_a: trio={'source:': True, 'verified-at:': True, 'recheck:': True} cites=['S375', 'S376', 'S377'] indexed=True registry_leg=PASS -> PASS
clause_b: S375 status='rejected' opened=2026-10-27 commit_pinned=True quote_words=24 quote_in_pin=True -> FAIL
clause_b: S376 status='queued' opened=2026-10-27 commit_pinned=True quote_words=11 quote_in_pin=False -> FAIL
clause_b: S377 status='rejected' opened=2026-10-27 commit_pinned=True quote_words=3 quote_in_pin=True -> FAIL
clause_c: host_joins=3/8 -> PASS
PROBE_C2_CLAUSES: entry=entry-A-literal.md judge=frozen ignore_status=False rows=0/3 hosts=3 clause_a=PASS verdict=TARGET_MISSED (clause d not run)
rc=1
== B overstated, frozen
… identical clause_a/clause_b/clause_c lines as A …
PROBE_C2_CLAUSES: entry=entry-B-overstated.md judge=frozen ignore_status=False rows=0/3 hosts=3 clause_a=PASS verdict=TARGET_MISSED (clause d not run)
rc=1
== C forged-prose, frozen
PROBE_C2_CLAUSES: entry=entry-C-forged-S376.md judge=frozen ignore_status=False rows=0/3 hosts=2 clause_a=PASS verdict=TARGET_MISSED (clause d not run)
rc=1
```

Probe-only relaxations (non-frozen; isolate prose):

```
== A, probe-only relax (strip-emphasis + ignore-status)
clause_b: S375 … quote_in_pin=True -> PASS ; S376 … quote_in_pin=True -> PASS ; S377 … quote_in_pin=True -> PASS
clause_c: host_joins=3/8 -> PASS
PROBE_C2_CLAUSES: entry=entry-A-literal.md judge=strip-emphasis ignore_status=True rows=3/3 hosts=3 clause_a=PASS verdict=TARGET_MET (clause d not run)
rc=0
== B, probe-only relax
PROBE_C2_CLAUSES: entry=entry-B-overstated.md judge=strip-emphasis ignore_status=True rows=3/3 hosts=3 clause_a=PASS verdict=TARGET_MET (clause d not run)
rc=0
== C, probe-only relax
clause_c: host_joins=2/8 -> PASS
PROBE_C2_CLAUSES: entry=entry-C-forged-S376.md judge=strip-emphasis ignore_status=True rows=3/3 hosts=2 clause_a=PASS verdict=TARGET_MET (clause d not run)
rc=0
== B with forged S376 ROW quote (C2-CTL-1 analogue), probe-only relax
clause_b: S376 status='queued' … quote_words=5 quote_in_pin=False -> FAIL
PROBE_C2_CLAUSES: … rows=2/3 hosts=3 clause_a=PASS verdict=TARGET_MISSED (clause d not run)
rc=1
== B, strip-emphasis only (status frozen)
PROBE_C2_CLAUSES: … rows=0/3 hosts=3 … verdict=TARGET_MISSED
rc=1
```

Reading of the matrix:

| candidate | frozen judge, frozen status | strip-emphasis + ignore-status |
|---|---|---|
| A literal | rows 0/3 → MISSED | rows 3/3, hosts 3 → **MET** |
| B overstated | rows 0/3 → MISSED | rows 3/3, hosts 3 → **MET** |
| C forged prose | rows 0/3 → MISSED | rows 3/3, hosts 2 → **MET** |
| B + forged **row** S376 (CTL-1 analogue) | — | rows 2/3 → **MISSED** (control discriminates under this judge) |

A and B get the same verdict in every configuration. C, which quotes a sentence that is not in the pin, also passes. The only thing that rejects a forged quote is a forged **row**.

## 5. Findings (item 32)

**F1 — prose quotes and prose claims are outside the predicate.** Clause (b) reads the located quote from the frozen table (L61–65), not from the entry text. Candidate C's forged prose quote (`sends arguments via a socket`) is never checked, so it passes the relaxed probe. No frozen control mutates entry prose, so the matrix of controls cannot catch it either.

**F2 — overclaim B is structurally indistinguishable from literal A.** B asserts (i) "every process started through uwsm-app inherits WAYLAND_DISPLAY and the compositor's session variables", (ii) "the owned chain is covered end to end", and (iii) that the host lines "exercise this". None of (i)–(iii) is checked by any clause. Clause (c) counts citation strings only. The host files were not read (live host reads are forbidden in this wave), so the host-join truth is not established by this seat either. The predicate has no leg that asks whether a sentence's claim is supported by the span it cites.

**F3 — the three frozen rows do not cover the topic in the claim title.** The claim is "`uwsm-app`'s environment". The rows cover a preparation-unit export (S375), a transport contract (S376) and a unit-name format (S377). Clauses (a)–(c) can be met with these three rows while the claim's subject is untouched. The pinned bytes that actually speak to app environment (§2 "not cited" list) sit in the same pins but are not in any frozen row, and the predicate does not require them. A coverage-claim predicate with no coverage leg is a gap.

**F4 — B's universal claim is not supported by the pins.** Two readings:

- Service units (`-t service`): `app()` forwards only `Varnames.session_specific` via `--setenv` (main.py L3738–3740, set at L146–152). `WAYLAND_DISPLAY` is not in that set. So the pinned forwarding does not carry `WAYLAND_DISPLAY`. Whether the service unit's activation environment has it depends on README L338–376 (compositor/finalize behavior), which no frozen row cites.
- Scope units (default): README L586–587 describes `uwsm app` scopes as inheriting environment of origin. This is a statement about `uwsm app`; `uwsm-app` is said to be a drop-in replacement (README L236) with the same parser (scd L15–17). So for scope units the outcome depends on the **caller's** environment, which none of S375–S377 establish. [INFERENCE] that `uwsm-app` scope behaviour matches `uwsm app`; not tested on host.

So B's "every process … inherits WAYLAND_DISPLAY" is an unqualified universal that the pins contradict on the service path and do not establish on the scope path. A counter that accepts B has accepted a claim the source does not carry.

**F5 — registry drift: the lane's current rows fail the frozen status leg, independent of prose.** On my read (14:49–14:50; `corpus/SOURCES.md` unchanged from the fixture copy, `cmp` exit 0):

- S375 (L325): status `rejected`; scope "environment preparation export … (adjacent system-session ground)"; teaches "REJECTED: systemd user-manager environment state is outside mado's province; flip: …".
- S376 (L326): status `queued`; scope "client-to-app-daemon transport contract; does not establish application environment"; teaches "client transmits arguments through the app-daemon pipe; runtime environment is not established".
- S377 (L327): status `rejected`; "REJECTED: systemd application-unit naming is outside mado's province …".

Consequences:

- Clause (b) requires `mined`. Under the frozen predicate, rows = 0/3 at current lane state, so PRED-C2-r54 is TARGET_MISSED by status, regardless of entry text.
- The lane's own rows now say "does not establish application environment" in the scope column. That is an explicit anti-overclaim statement that the frozen predicate does not read. The predicate reads status, opened, commit and quote, not scope.
- The teaches cells are no longer quotes. Even under strip-emphasis, a `teaches`-cell reading of clause (b) would fail on prose.
- `corpus/knowledge/` has no `uwsm*`/`r54` entry and `quality/counters/` has no `c1-r54`/`c2-r54` file at 14:50 (`ls … | grep` exit 1 each). My w1 S6 note that the entry was untracked at freeze time is therefore stale. I did not run git to trace this; the drift is recorded, not explained.
- `claims-frozen.md` (mtime 13:59) and `registration.md` (mtime 14:00) are unchanged since freeze. The conflict is between frozen clause (b) and the rewritten rows, not an edit to the frozen files.

**F6 — the frozen S376 quote is unsatisfiable under the literal judge, and CTL-1 is only discriminating under a non-frozen judge (confirms w1 item 3).** Under the frozen judge, the honest S376 leg already fails (`quote_in_pin=False`, pin L60 has `*uwsm-app*`). So CTL-1 adds no evidence there. Under strip-emphasis, CTL-1 discriminates (rows 3/3 → 2/3). The frozen C2 section has no judge sentence; the judge sentence at `registration.md` L51–53 is C1-side. This is the same finding as w1 item 3, now measured on the candidate.

**F7 — w1 items still hold (not re-attacked here).** S375 quote location 117–118 vs quote 117–119 (location is not a predicate leg, so it does not affect clause (b) as written). Host-join strings (w1 S4): bare basenames would not match the frozen full-path strings.

## 6. Remaining gap and what would close it (recommendation only; nothing edited)

Under the honesty rules, the freeze cannot be edited after scoring. A fix is a pre-data re-registration in a new versioned file (`claims-frozen-v2.md`), or an honest stop. The gap as frozen:

1. **Prose-to-pin binding.** A frozen leg that requires every quoted span in entry prose to occur in the cited pin, and every environment-claim sentence to cite a span that contains the mechanism it names. Without it, C passes.
2. **Coverage leg.** A frozen list of pinned spans that count as evidence for "uwsm-app's environment" (at minimum README L235–237, L585–592; scd L15–17; main.py L146–152, L3732–3741). Without it, F3 stands.
3. **Universal-claim control.** A control that mutates the entry prose into an overclaim (B-style) and must be rejected. None of the six C2 controls does this.
4. **Status leg vs. scope text.** Clause (b)'s `mined` requirement must be reconciled with the current `rejected`/`queued` rows, and the scope column's "does not establish" language must be either read by the predicate or explicitly ruled out.
5. **Judge for the quote.** A frozen judge sentence for C2 (the C1 one at L51–53 does not cover C2) naming how `*uwsm-app*` emphasis is handled, and which cell (teaches or the frozen quote table) is "the located quote".

Until one of these is frozen, PRED-C2-r54 cannot distinguish the literal entry A from the overclaimed entry B, and a counter built to the freeze would accept B whenever the rows are `mined`.

## 7. Scratch, installs, disk

- Installs or updates: none. No tool was needed beyond the shell and Python already on the host.
- Scratch: `/fast/scratch/hyaku/mado-r54/R54W2Seat32` (fixture `fx.Ityh`, probe script, three candidate entries). Removed before yield (`rm -rf` on the scratch root; verification output in the yield step). No `/tmp` files were created.
- No ENOSPC or other disk error observed (the fixture is ~688 KB).
- No file in the lane, `corpus/`, `quality/`, `.ufo/waves/round-54/` (except this report under `w2/`), host config, or git state was written.
