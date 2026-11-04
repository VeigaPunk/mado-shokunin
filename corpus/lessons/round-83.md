# Round 83 — surface allocation and tray state

Base: 67dd2b667b72f7f72309340d488b355d543841a5. Instrument freeze: dbc09269fe547ab13541e722dd7d2ba33015f348.
Claims: C1 coverage (allocation map resolves a second declared layer surface); C2 operability (31 executable runbook rows, including tray count and boolean state).

## Mistakes

| class | evidence | captured-by | fix shown able to fail |
|---|---|---|---|
| scope | freeze 4e48d8e7 regressed carried auto-left-dock, 54/55 | carried-case counter | preserve the compositor assign branch: dbc09269 receipt correct=58/58 |
| vacuous | duplicate bar resolution masked alloc-composition-ignored; intermediate freeze 4208c24a killed=36/38 | mutation kill count | one resolution site; bar-band-no-refusal killed by exclusive-false composition case |
| number-drift | dbc09269 measurement prints mutants=38 killed=39 and TARGET_MISSED | literal frozen predicate | successor constant corrected to actual list length; original claim is still reported missed, not retroactively admitted |
| reference-drift | bool matcher comment separated anchor from return; second short anchor occurred three times | full matcher mutation run | anchored two-line block; dbc09269 C2 receipt kills=27/27 |

## Gate

Opened 2026-11-04:

- S484, https://raw.githubusercontent.com/systemd/systemd/v262/man/busctl.xml, fetched into .ufo/waves/round-83/fetch/busctl-man.txt. Located quote at 495–496: “For arrays, a numeric argument for the number of entries followed by the entries shall be specified.” Admit scoped to terse property formatting, not pipeline failure propagation. C2 rests on this row.
- S485, https://raw.githubusercontent.com/Alexays/Waybar/90b209add8937514d0a987aa842e701bd8f1232e/src/modules/sni/host.cpp, fetched into .ufo/waves/round-83/fetch/waybar-sni-host.cpp. Located quote at 78: “sn_watcher_call_register_host(host->watcher_, host->object_path_.c_str(), host->cancellable_,”. Admit host registration call and registered-list read at 101; not proof that every host state is healthy.
- Reopened the held S481 zero-size clause and S482 KDE XML property block from round-82 pins. Reject using a live box as the allocation's source: independent inputs must be allowed to disagree (alloc-live-band-differs and composed twin).
- Reject assuming absent allocation always forbids a compositor-assigned spanning box: carried auto-left-dock contradicts that blanket rule.
- No existing registry status, recheck or used-by cell changed. New rows only. Independent outside-lane admit/reject spot-check remains pending; dispatched seats are still the lane.

## Carry-in corrections and limits

Round-82 spotcheck D1: its knowledge note's receipt revision became stale; readers must resolve the receipt at its cited commit, not assume the live path retains those bytes. D2: seat statuses were 7 ok and 7 defect, not 11/3. D3: census output includes W01 S277 as well as W04 duplicate-URL warnings; unfiltered round83 end receipt retained. D4/D5: set_size request ends at 137, its quoted assignment sentence is 128–129; 347–348 is configure, not set_size. Existing append-only registry anchor correction remains routed rather than silently editing S481. D6: round83 retains actual results handoff; D7/D8: record revision and hash type explicitly. D9: round82 eight new cases contained three refusals, not six. D10: Gate must quote the admitted row's own sentence.

G1 bool allocation and V1 vertical branch are exercised; G2 object-as-array and G3 stage prefix have successor selftest assertions. V7 readers now have both single and composition mismatch cases. V8 tautological control clause removed, but the held-section refusal alone does not prove substantive semantic improvement; V9 successor --no-mutants is diagnostic and names skipped kills.

Assimilation: none. considerthese/2026-11-04.md read; proposal 7 (label relayed versus re-measured) applied here: measurements are re-executed; prior-round errata are evidence-verified from round-82-verifier-spotcheck.md, not newly rerun. No tools installed. Pacman paused.

## Settled wave integration

WAVE-DONE received from Main; w1-results.json contains ten seats, seven nonempty outputs and three empty outputs (scout, connector, entry scribe). No empty seat is replaced. L1 wrote the bounded entry instead.

ReviewerC1 found three 58/58 survivors: using a non-bar live box instead of declared allocation, overriding an extra's positive band, and overriding an explicit exclusive zone. MutationTester independently confirms positive-band precedence survives and finds boolean-padding and later-array-element gaps. These are counter limitations, not implemented product defects; no stronger certification is admitted.

ExecC2Live demonstrates a failing producer emitting plausible array text can yield rc0 through the count pipeline. C2's finite predicate is green, but successful bus-property execution is not established by that pipeline. Critic also notes diagnostic --no-mutants can print TARGET_MET without kills. These strong operability interpretations are rejected, with these exact failure conditions as flips for a later frozen claim. No frozen case set is enlarged after the wave.

Sentinel found local account/path exposure, not credentials. Machine-protocol handoff absolute paths are required by the operator; they remain. Two actual session identifiers in the new negative fixture were replaced with synthetic identifiers; the frozen and amended hashes differ and the report discloses that repair. Historical commits are not rewritten.

Round admission: honest stop. C1's frozen predicate misses its own population count; repaired successor is green but the causal survivors remain. C2 is measured green on its finite set, not admitted as proof of producer-status propagation. Outside-lane closure is the authority.
