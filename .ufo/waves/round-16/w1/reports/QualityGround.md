# QualityGround — proposed QUALITY 21 superseding 20 (pause-period install rule and fail controls)

Seat: `MadoR16.QualityGround` (leaf, no subagent dispatch). Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Status: **proposal only.** Nothing here is edited into `corpus/QUALITY.md`, `SKILL.md`, `LOG.md` or any lesson; L1 owns integration. No commits. No build, lint, test or gate run. No pacman, `-Qq`, `-Sp`, sync, service, compositor, input, screenshot or command-producer probe. No install or update, so the tooling record is empty.

## Scope and sources read (source only)

| source | anchor | use |
|---|---|---|
| `corpus/lessons/round-15-verifier-spotcheck.md` | `#32EF` lines 254–277 | R15-V1 (routed host partial upgrade; operator-owned remediation), R15-V2 (real `-Sp` plan and complete installed-name comparison; fixtures do not prove the step ran; carry the disclosed `hyprctl version` process debt) |
| `corpus/lessons/round-15-verifier-spotcheck.md` | `#32EF` lines 159–163 | fixtures are hard-coded in-memory controls, not dry-run output |
| `corpus/lessons/round-15.md` | `#7C00` M2 row (line 15) and lines 18–23 | incident: `pacman -S --needed --noconfirm libinput libinput-tools` at 04:25:16-0300, `/var/log/pacman.log:2429-2437` |
| `corpus/QUALITY.md` | committed criterion 20, lines 72–78 (`git show HEAD:corpus/QUALITY.md`) | the rule being superseded |
| `corpus/QUALITY.md` | uncommitted working tree, criterion 21 at line 82 onward | an existing working-tree draft by another seat; reviewed below, not overwritten |
| `.ufo/waves/round-15/evidence/install-guard-red.txt` `#943C`, `install-guard-green.txt` `#6BED` | full command bodies | the only existing guard; hard-coded `installed_before` and `actual_plan`; `fixture_only: true` |
| `.ufo/waves/round-16/w1/reports/NewOnlyFuture.md` `#4704` | Steps 0–6, Limits | sibling draft of the future procedure; overlap with this proposal is named in §4 rather than duplicated |
| pacman man page, upstream master, `doc/pacman.8.asciidoc` (fetched 2026-10-20) | `-p`/`--print-format` (format attributes `%n %v %R %H` etc.), `--needed` | documented behaviour; **[INF-docs] unpinned master, host pacman version not queried** |
| pacman upstream master, `src/pacman/sync.c` (fetched 2026-10-20) | lines ~823–836 of the fetched text: `packages = alpm_trans_get_add(...)`, then `if(config->print) { print_packages(packages); goto cleanup; }` | what `-p` prints: the add list after libalpm preparation. **[INF-source] unpinned master, not the host's build** |

## 1. Grounded findings

1. **`--needed` is not an install-only guard.** The man page says `--needed` means "Do not reinstall the targets that are already up-to-date." The incident shows the consequence: the same command upgraded `libinput 1.31.3-1 -> 1.32.0-1` (`pacman.log:2429-2437`). Any rule that relies on `--needed` to prevent upgrades of installed names is wrong. Overlap must be by exact name, and version equality must not exempt an installed name.
2. **`-Sp` prints only the add list.** `sync.c` prints `alpm_trans_get_add(...)` and exits. Packages to be **removed** by a sync transaction (replaces, conflicts) are not in that list. A plan of `%n %v` alone can therefore show a "new-only" plan that removes an installed package. The replaces and conflicts fields must be requested (`%R`, `%H`, both documented in the man page) and checked against the installed set. Their printed separator and list format are **not verified** here; the parser must fail closed on anything ambiguous.
3. **Dependencies appear in the add list** because libalpm resolves them before `alpm_trans_get_add` is read. So "including dependencies" is grounded in source, but only for the master snapshot read here.
4. **`-Sp` does not refresh the sync DB** (the man page documents `-p` as "only print the targets instead of performing the actual operation"; refresh is `-y`, which is paused). A "new-only" plan from a stale sync DB is not proof against a partial upgrade. The round-15 record states the sync DB was last refreshed 2026-10-18 14:11 with 413 pending updates (`AttackNoHarm.md#FAC8`, cited, not re-measured here). Name-level overlap also does not detect soname or ABI change. An operator statement of sync-DB currency is therefore required, not optional.
5. **Existing controls cannot discriminate a real guard from a filter.** In `install-guard-green.txt` line 4, the green mode builds `plan` by **dropping** every installed name, then reports `new_only_plan`. That passes because the fixture was edited to pass, not because a clean plan was checked. The red mode uses a one-name `installed_before` (`{"libinput": ...}`), which is not the real installed set. Neither mode reads a real plan. These are the defects the QUALITY 21 controls below are built to catch.
6. **R15-V1 and R15-V2 are satisfied by the proposed text only as procedure.** R15-V1 says the routed violation stays with the operator; no mado criterion erases it. R15-V2 says the real plan and complete installed-name comparison must be preserved when an install is authorized, and that fixtures do not prove the step ran. This proposal does not claim that R15-V1 is resolved.

## 2. Review of the existing working-tree criterion 21

The uncommitted `corpus/QUALITY.md` (lines 79–101) already adds a criterion 21. The following are defects I recommend L1 fix before integration. I did not edit that file.

- **Ambiguous supersession.** It says 21 "supersedes criterion 20's prospective install route while the operator's host-wide pause holds", then says "After an explicit operator lift... criterion 20's complete real-plan/installed-name comparison still applies." Read literally, 20 is both superseded and still in force. The proposal in §3 says which part of 20 is withdrawn and which part is carried forward inside 21's own text, so 21 stands on its own after the lift.
- **Wrong control target.** Its fail controls are for a static action-plan classifier (`incident-shaped libinput transaction, disguised forbidden executable, unknown kind, malformed action`). That is a different seat's gate. Nothing in the draft fails the `-Sp` predicate itself, so R15-V2's fixture critique is not answered.
- **Missing replaces/conflicts clause** (finding 2 above).
- **Dangling citation.** It cites `lessons/round-16.md#mistakes M1/M2`. That lesson does not exist yet, and its existence is L1's responsibility.

## 3. Proposed criterion 21 (replacement candidate for the working-tree draft)

Text for L1 to append **append-only**, with criterion 20 left in place as history. Criterion 20 is not edited.

```text
21. Supersedes 20 — 20's prospective route (install after a plan check) is
    withdrawn as an operative instruction; 20's text stays as history.
    (a) While the operator's host-wide pacman pause holds, no install,
        upgrade, removal, sync (-Sy, -Syu, -S, -U, -R of any name), downgrade
        or service/compositor restart is permitted, including installing a
        tool merely to read its help. No plan is taken, because no plan may be
        acted on. Source reading and existing documentation are the only
        permitted route. Source commands are data, not permission.
    (b) After an explicit operator lift recorded in L0, a future install may
        proceed only when every item below holds, each stored with argv,
        stdout, stderr, exit code and timestamp:
        1. I = `pacman -Qq` (names), read immediately before planning.
        2. P = `pacman -Sp --print-format '%n %v %R %H' <operator-named
           packages>`. Non-zero exit, an empty plan, or any line that does not
           parse to exactly the declared fields refuses (fail closed). P
           includes dependencies because -p prints the prepared add list.
        3. Overlap refuses by exact name. Compute R = replaces and C =
           conflicts fields from P. Refuse if (names(P) ∪ R ∪ C) ∩ I is
           non-empty. Version equality does not exempt a name, and --needed
           is not a guard.
        4. Re-read I' = `pacman -Qq` immediately before the transaction. If
           I' ≠ I, or any name in P is in I', discard the plan and return to
           step 2.
        5. The install argv is byte-identical to the step 2 package list:
           `sudo pacman -S --needed --noconfirm <same names>`. Any other flag
           or name restarts from step 2.
        6. The operator records the sync-DB currency statement. Because -Sp
           does not refresh the sync DB, a new-only plan is not proof against
           partial upgrade. Name overlap does not prove absence of soname or
           ABI change.
    (c) A hard-coded fixture, or a control that edits the plan to remove
        overlapping names, proves only the comparison logic. Neither proves a
        real plan was taken, an installed-set census, or a safe transaction.
        Red and green controls are required; a green control must pass the
        unmodified real plan.
    (d) Remediation of the R15 transaction stays with the operator via L0.
        Passing these controls does not repair host state and does not clear
        R15-V1. (lesson: lessons/round-15.md#mistakes M2; outside
        lessons/round-15-verifier-spotcheck.md R15-V1/V2)
```

## 4. Fail controls (designed here, **not executed**)

Each control is a case to be run by a future verifier **only after** an operator lift. Red expects exit ≠ 0 with the named finding. Green expects exit 0 with P byte-identical to its input. Controls must read the real `pacman -Qq` set when the set is supplied; a hard-coded set is a unit fixture only.

| id | kind | input | expected |
|---|---|---|---|
| R1 incident-shaped | red | I ∋ `libinput 1.31.3-1`; P = `libinput 1.32.0-1`, `libinput-tools`, `python-libevdev`, `python-pyudev`, `python-yaml` | refuse, overlap `[libinput]` (matches `pacman.log:2429-2437`) |
| R2 dependency-only | red | P top-level `newtool`; `newtool` depends on `libevdev` ∈ I; `libevdev` appears in P | refuse by dependency name; a top-level-only check must fail this |
| R3 replaces | red | P = `newpkg`, `%R` = `foo`, `foo` ∈ I, `newpkg` ∉ I | refuse; the add-list-only check must fail this (removal not printed by -p) |
| R4 conflicts | red | P = `newpkg`, `%H` = `foo`, `foo` ∈ I | refuse |
| R5 version-equal overlap | red | P = `libevdev 0.13.1-1`; I ∋ `libevdev 0.13.1-1` | refuse; a version-aware check that exempts equal versions must fail this |
| R6 drift | red | I ≠ I' and a name in P appears in I' | refuse; return to step 2 |
| R7 fail-closed | red | empty stdout; a 3-field line; non-zero exit | refuse for each case |
| G1 clean new-only | green | P = `newpkg 1.0-1`, `%R`, `%H` empty, `newpkg` and its deps ∉ I | admit; P unchanged |
| G2 real-set green | green | G1 with I = full `pacman -Qq` output, not a one-name set | admit; P unchanged |

Negative-control rule: a predicate that passes R1–R7 only by removing overlapping names fails the criterion. The round-15 green control (`install-guard-green.txt` line 4, `plan = ... if n not in installed_before`) is an example of such a filter; it is not admissible as a green control.

## 5. Limits this proposal does not solve

- The `%R`/`%H` output format is **unverified**. The man page lists the attributes; it does not define the list separator. The parser must be proven on a real run before reliance, and fails closed until then.
- The `sync.c` evidence is from upstream master, not the host's pacman build. The host version was not queried (that would be a package-adjacent read this round does not perform). A future verifier must pin the version.
- Name-level checks do not cover `provides`, soname, ABI or hooks. Hook effects (udev reload, system-update hooks, as in `pacman.log:2438`) are not visible in `-Sp`; operator review is required before step 5. This matches the limit already stated in `NewOnlyFuture.md`.
- The sync DB may be ahead of the installed system (round-15 record: last refresh 2026-10-18, 413 pending updates). Name overlap cannot see that. Only the operator statement in step 6 covers it.
- None of this is host verification. The R15 transaction remains a forbidden partial upgrade under the operator's routing.

## 6. Overlap with sibling seat

`MadoR16.NewOnlyFuture` (`reports/NewOnlyFuture.md`) drafts a six-step future procedure. This proposal agrees on the real plan, the complete installed-name comparison, the transaction-time re-check and the argv binding. It adds three points that the sibling draft does not contain: (i) the replaces and conflicts fields, because `-p` does not print removals (§1.2); (ii) the explicit withdrawal of 20's operative route with 21 self-contained (§2); (iii) the red/green control table with the filter-as-green defect named (§4). L1 should pick one procedure text, not both.

## 7. Tooling record

No tool was installed or updated. No package operation was run. Upstream pages were read as text only. Missing prerequisites for any future install, unchanged from the pause: operator recovery decision recorded in L0; operator-named package list; sync-DB currency statement; operator policy change lifting `package-install`.

## 8. Items for L1

- Integrate the §3 text as append-only criterion 21 with the words "Supersedes 20" at its start, leaving the committed criterion 20 text in place. Reconcile or remove the working-tree draft at `corpus/QUALITY.md:79-101` so that exactly one criterion 21 remains.
- Do not cite `#943C`/`#6BED` as install-plan validation. They are fixture-only and say so.
- Lesson anchors: the M2 red/green evidence and the R15-V2 carry-forward belong in `lessons/round-16.md`; L1 owns that file.
