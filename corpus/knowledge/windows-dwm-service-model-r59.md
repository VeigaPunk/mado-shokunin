source: S399, S400 (existing registry rows), S405 (new row, opened 2026-10-31, Microsoft Learn)
verified-at: 2026-10-31
recheck: on-release

# The DWM service model on the Windows host (round 59)

**Scope.** Closes the r57 entry's finding D01 — the refreshed DWM overview
(S399) carries a Vista/7-era sentence claiming DWM "runs as a Windows service"
that "can be enabled and disabled through the Administrative Tools Control
Panel item, under Services, as Desktop Window Manager Session Manager", while
S400 states composition is always enabled as of Windows 8 and the observed
host reports TRUE. D01's named flip was "a sourced row that states the Win11
DWM service model". This entry lands the sourced model row (S405, Microsoft
Learn Compatibility Cookbook, opened 2026-10-31) and joins it to host probes
on build 26200. Layers stay separate (QUALITY 15/16): every documentation
sentence is a dated `[INF-docs]` claim, every host sentence cites the command
that produced it, and neither substitutes for the other.

**Named residue (kept visible).** No page naming Windows 11 in the model
sentence surfaced in this round's bounded sweep (DWM service-model pages and
UxSms / "Desktop Window Manager Session Manager" references; search log
§ Round 59 in `corpus/SOURCES.md`). D01 closes on the documented Windows-8+
model (S405 + S400, one doc set) joined to build-26200 host observations —
not on a Win11-labeled sentence. A future Win11-labeled primary page would
strengthen the pin, not change the verdict.

## 1. Host claims (H rows, each with its re-derivation command)

| id | proposition | command (read-only) | observed 2026-10-31 |
|---|---|---|---|
| H09 | no Windows service matching name `dwm`/`uxsms` or display name "Desktop Window" is registered on build 26200 | `Get-CimInstance Win32_Service`, filtered (probe `.ufo/waves/round-59/receipts/dwm-service-probe.ps1`) | `SERVICES 0` — two runs, identical receipts `dwm-service-run1.txt`/`run2.txt` |
| H10 | the Vista/7-era "Desktop Window Manager Session Manager" service name does not resolve on this host | `sc.exe query UxSms` | rc=1060: "The specified service does not exist as an installed service." (both runs) |
| H11 | dwm.exe runs as a session process and hosts no services | `Get-Process dwm` + `tasklist /svc /fi "IMAGENAME eq dwm.exe"` | one process point-in-time: `DWMPROC name=dwm pid=1692 session=1`; `tasklist /svc` services column `N/A` (both runs; pid is not bound across runs) |
| H12 | DWM composition is enabled (the r57 H04 probe, re-run for this join) | `dwmapi!DwmIsCompositionEnabled` | `hr=0 enabled=True` (both runs) |

## 2. Documented claims (K rows — dated [INF-docs], never host facts)

| id | proposition (≤25-word quotes verbatim from the named row) | row / anchor | class |
|---|---|---|---|
| K15 | "In Windows 8, Desktop Window Manager (DWM) is always ON and cannot be disabled by end users and apps." | S405 § Description | [INF-docs] |
| K16 | "In Windows 8, DWM desktop composition is a core operating system component and cannot be disabled." | S405 § Controlling desktop composition | [INF-docs] |
| K17 | "it's started before the user logon and remains active for the duration of a session." | S405 § Controlling desktop composition | [INF-docs] |
| K18 | "All of the options for disabling desktop composition that exist in Window 7 are removed" (the page's own "Window 7" spelling, verbatim) | S405 § App compatibility and user action | [INF-docs] |
| K19 | "Apps cannot use DwmEnableComposition to disable desktop composition." — the call reports success and does not disable | S405 § App compatibility and user action | [INF-docs] |
| K20 | "As of Windows 8, DWM composition is always enabled." — the S400 note D01 set against S399's service sentence, re-opened from its page this round | S400 § Parameters (Note) | [INF-docs] |

## 3. Claim-to-host joins (the only place K and H touch)

| join | documented side | host side | verdict |
|---|---|---|---|
| J09 | K15/K16: Windows-8+ DWM cannot be disabled; it is a core OS component | H09/H10: no DWM service is registered and the named Vista/7-era service name does not resolve (rc 1060) — nothing that could be "enabled and disabled … under Services" exists | `agreement` (the S399 service sentence has no host referent on build 26200) |
| J10 | K17: composition starts before logon and remains active for the session duration | H11: one dwm.exe process observed running in session 1 (point-in-time) | `agreement*` (the session-scoped shape is observed; "before logon" is a boot-time fact not readable read-only from the lane, and per-session process counts are not enumerated by this probe — named limits) |
| J11 | K18/K19: every Windows-7-era disabling path removed; the disable API is a documented no-op | H12: composition reports enabled (`hr=0 enabled=True`); no disabling path exists to exercise | `agreement` (vacuous shape named: the removal means only the enabled side is observable) |
| J12 | K20 (S400's always-enabled note) against K15 (S405's model statement) | — | `agreement` (two pages, one doc set, one model; the D01 set contradiction resolves against the service sentence, not the always-enabled note) |

## 4. Finding D01 — closed (flip met, residue named)

The r57 entry's D01 (source-internal drift: era mixing in a refreshed page)
asked which sentence describes the build-26200 service model and named its
flip: "a sourced row that states the Win11 DWM service model." S405 states
the model — Windows-8+ DWM is an always-on core OS component whose every
Windows-7-era disabling path, including the Administrative Tools → Services
toggle the S399 sentence names, was removed — and the host probes agree on
every observable: no DWM service (H09), the named service does not resolve
(H10), dwm.exe runs outside any service (H11), composition is enabled (H12).
D01 closes as **closed (flip met)** with the residue named in § Scope: the
row states the Windows-8+ model rather than a Win11-labeled sentence. The
r57 entry carries an `## Errata (round 59)` pointer; its § 6 line "D01 is
open" is history as of this entry.

## 5. Verify (re-runnable, read-only)

```powershell
# probe (committed receipt artifact): service census, UxSms query, dwm.exe
# census + hosted services, composition flag — queries only
powershell.exe -NoProfile -ExecutionPolicy Bypass -File `
  .ufo/waves/round-59/receipts/dwm-service-probe.ps1
# expect: SERVICES 0; SC_UXSMS_RC=1060; DWMPROC name=dwm pid=<n> session=<n>;
# tasklist /svc services column N/A; DWM_COMPOSITION hr=0 enabled=True
```

Receipts: `dwm-service-run1.txt` and `dwm-service-run2.txt` (byte-identical
outputs, both rc=0, 2026-10-31).

## 6. Limits and unknowns

- "Before logon" (K17) is not observable read-only from the lane — a boot-time
  fact. `[UNK]`.
- The dwm.exe per-session process count on multi-session hosts (RDS) is
  untested on this single-session host; H11 binds one process at one moment.
- No Win11-labeled primary page stating the model surfaced; the residue is
  named in § Scope and § 4, and the Windows-8+ reading rests on S400's
  "As of Windows 8" note in the same doc set.
- S405's Platforms metadata is "Clients – Windows 8"; carried verbatim in the
  row. The page's own text speaks of Windows 8 throughout; the doc-set-internal
  continuity (K20) is what joins it to a build-26200 host.
