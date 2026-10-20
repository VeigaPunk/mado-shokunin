# FrontierRecord — mado round 15 w1 (seat MadoR15.FrontierRecord)

Claim scope: C1 coverage — U6 input-debugging ladder frontier. Scope of this seat: draft exact search/census reporting needs and ≤25-word quote checks. No registry, corpus, SCORECARD, LOG or SKILL write (L1 owns them). No tests, gates, measure.py, builds, input-event reads, live probes, or compositor actions. No delegation. Tool installs by this seat: none.

## 1. Opens performed in this pass (read-only)

| Id | Surface | How opened | Used for |
|---|---|---|---|
| S007 | libinput helper tools, https://wayland.freedesktop.org/libinput/doc/latest/tools.html | web read (rolling "latest" page, self-labelled libinput 1.32.0 documentation) | rung R0–R2 facts, quote checks Q1–Q5 |
| S042 | Wayland debugging extras, https://wayland.freedesktop.org/extras.html | web read | rung R4/R5 tool surface, quote checks Q8–Q9 |
| S009 | Wayland architecture, https://wayland.freedesktop.org/architecture.html | web read | rung R3 path, quote checks Q6–Q7 |
| XML-1 | `/usr/share/wayland/wayland.xml` (wayland 1.26.0-1), sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` | local static read: `wl_seat` :2004, `wl_pointer` :2138, `wl_keyboard` :2573-2576 | rung R4, quote Q10 |
| XML-2 | `/usr/share/wayland-protocols/unstable/text-input/text-input-unstable-v3.xml` (wayland-protocols 1.49-1), sha256 `160815cda13c285a30df1971d8f0a5b3aac07071537df59916d2f748b18e4f59` | local static read: `zwp_text_input_v3` :50-53, :67-70; `zwp_text_input_manager_v3` :585-587 | rung R5 (IME), quotes Q11–Q12 |
| PKG | `pacman -Q / -Qs / -Qi` on libinput, libinput-tools, wayland, wayland-protocols, wayland-utils; `command -v libinput`; `libinput --version` (prints only the version) | read-only package DB and PATH checks | version pin, tool presence |
| OWN | `corpus/SOURCES.md`, `corpus/README.md`, `corpus/lessons/round-14.md`, `corpus/lessons/round-14-verifier-spotcheck.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md` (partial), `corpus/knowledge/*.md` (`covers:` and `source:` lines) | read | registry census, prior routes, R14-V1 text |
| EVID | `.ufo/waves/round-14/evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt` lines 1–5 | read | R14-V1 header census |

Not opened (leads only, not evidence): S008 Wayland book high-level design; the libinput reporting-bugs page and its evemu section; the libinput-tools man pages in `/usr/share/man/man1/libinput*.gz` (present, not read); wayland-protocols GOVERNANCE.md; S010 index; S006 as a document (its row was not re-opened). No source was admitted from search results.

## 2. Measured counts (working-tree bytes, this pass)

| Measure | Command | Result |
|---|---|---|
| SOURCES rows | python: rows matching `^\| S\d{3,} \|` in `corpus/SOURCES.md` | 50 |
| status mined / queued / rejected | same, column 8 | 38 / 8 / 4 |
| kind A / B / C | same, column 4 | 46 / 1 / 3 |
| queued ids | same | S006, S007, S008, S009, S010, S036, S038, S039 |
| knowledge notes | `ls corpus/knowledge/*.md \| wc -l` | 28 |
| notes with `^covers:` | regex `^covers:\s*(U[1-7])\s*$` | 5 notes: U1 window-rule-effects-getprop, U2 hyprland-config-era-r12, U3 xdg-portal-routing-r12, U4 wayland-protocol-boundaries-r13, U5 output-colour-boundaries-r14 |
| U6 covering notes | same | 0 |
| U7 covering notes | same | 0 |

The round-14 joined recipe (`covers:` × mined row naming the note) was not re-run here. Its recorded baseline is U1–U5 = 5/7, which the `covers:` census above agrees with on the names only. The joined count is L1's to run.

Registry change in this pass: none. Nothing was admitted, rejected or re-statused.

## 3. U6 frontier — draft ladder and what each rung may claim

Only static or documented facts are listed. Nothing here is a host behaviour observation.

| Rung | Layer | Sourced support (opened this pass) | Host-side fact observed | Not licensed |
|---|---|---|---|---|
| R0 | kernel `/dev/input/event*` nodes | S007: tools "must be run as root" for these nodes (Q1) | none (no node read) | any event content |
| R1 | libinput device description | S007 `list-devices`: built-in defaults, not desktop config (Q2); `list-kernel-devices` output is human-consumption only (Q5) | `libinput-tools 1.32.0-1` installed; `/usr/bin/libinput` present; `libinput --version` → 1.32.0 | a device's effective desktop configuration |
| R2 | libinput event stream (`debug-events`, `record`, `replay`) | S007 describes the route; `record` obscures key codes by default (Q3) | none — event reading is out of scope this round | any delivery, latency, or key-mapping claim |
| R3 | compositor receives kernel event, picks target surface | S009 steps 1–2 (Q6, Q7): compositor is the display server and transforms coordinates | none | Hyprland's dispatch behaviour (no compositor-side input source admitted yet) |
| R4 | advertised seat objects and keyboard/pointer interfaces | XML-1 `wl_keyboard` description (Q10); S043 registry rows already mined; S042 `wayland-info` lists advertised globals (Q8) | not re-probed this pass | that an advertised object implies tested behaviour |
| R5 | IME / text input | XML-2 `zwp_text_input_v3` (Q11) and focus enable/disable rule (Q12) | none | IME behaviour, commit/preedit delivery, any input-method installation. **No registry row exists for XML-2 — frontier open.** |
| R6 | protocol dumpers / debug surface | S042: `WAYLAND_DEBUG` "is not enough"; third-party dumpers are listed (Q9) | not run | any dump content; the dumpers are not admitted tools |

Retained unexercised limits (carry into any U6 note verbatim in meaning): no event read, replay, or injection; no delivery test; no IME test; no kernel or DRM diagnosis.

## 4. Source-row needs for L1 (draft, not written)

1. **S007 — owed revision anchor.** The cited page is a rolling "latest" doc. A superseding row needs the libinput source revision that matches `libinput-tools 1.32.0-1`. That commit was **not measured here**; no commit is inferred.
2. **S009 — owed revision anchor.** The page carries no revision. Its website-source commit was **not measured**; owed per the round-12 owed-anchor rule.
3. **S008, S010.** Still queued with access-date-only anchors. Not opened this pass.
4. **S006 vs S042.** S042 states it supersedes S006, but S006 is still `queued`. L1 should decide the status edit; this seat does not change it.
5. **New candidate row — XML-2.** `text-input-unstable-v3.xml`, wayland-protocols 1.49-1, sha256 `160815cd…4f59`, phase path `unstable/`. Teaches: text-input enable/disable and enter/leave semantics only. Not admitted.
6. **Libinput version pin drift.** `pacman -Q libinput` read `1.31.3-1` once in this pass. Later reads (`pacman -Q`, `pacman -Qi`, `command -v libinput`) showed `1.32.0-1`, build 2026-09-17, install 04:25:17 -03 on the run date. The cause is not established. Another actor's upgrade is plausible under the tooling directive but **unverified**. Any census must re-read the installed version at measure time and record it.

## 5. Reporting needs for the census (exact)

- **N1 registry counts.** Python over `corpus/SOURCES.md` rows: total, status, kind, and queued ids (§2). Expected to change only by L1's edits.
- **N2 coverage joined recipe.** Reuse the round-14 recipe verbatim (`covers:` regex, `source:` id join, `mined` status, path in `used-by`). Baseline U1–U5 = 5/7. U6 may count only if one note carries exactly one `covers: U6` and at least one of its `source:` ids is a `mined` row whose `used-by` lists that note path.
- **N3 owed-anchor count.** For every `mined` row, count anchors that are revision-bound (commit, tag, or sha). Today S007 and S009 would fail this test as written; S043 and S047/S048 pass by their recorded sha/commit text.
- **N4 status transitions.** Old→new per row, with reason. Only the row-level changes L1 makes.
- **N5 quote-length check.** Each quote ≤25 words, counted by `len(q.split())`, and each quote re-located verbatim in its opened source. Results in §6.
- **N6 R14-V1 receipt header census.** For each file in `.ufo/waves/round-14/evidence/` matching the three mutation receipts: check for `measured_commit` and `gate_sha256` headers and for `input_binding: provisional worktree snapshot`. Observed here, lines 1–5: all three carry `input_binding: provisional worktree snapshot`; `gate_sha256` is `ef50e262…` in `regression-recut.txt` and `d6d5eb27…` in the other two; no `measured_commit` line appears in lines 1–5. These must not be read as standalone final-gate receipts. The R14-V1 correction (an appended explanatory block mapping each header to derived target `cd1d73d7…`, with history kept) is the owning lane's edit, not this seat's.
- **N7 no-fabrication guard.** Every U6 claim cites an S-row whose opened revision is recorded. Search results alone admit nothing. The counts in this report are from the commands above, not estimates.
- **N8 frontier open marks.** A U6 note must mark R2 (event route), R5 (IME), and the libinput version pin as unexercised or unpinned, unless a later round measures them.

## 6. Quote checks (verbatim; all ≤25 words; locator = section or line)

| Id | Source | Locator | Quote | Words |
|---|---|---|---|---|
| Q1 | S007 | §Helper tools | Most of the tools must be run as root to have access to the kernel’s `/dev/input/event*` device files. | 18 |
| Q2 | S007 | §libinput list-devices (Note) | This tool does **not** show your desktop’s configuration, just the libinput built-in defaults. | 13 |
| Q3 | S007 | §libinput record and replay | For data protection, `libinput record` obscures key codes by default, any alphanumeric key shows up as letter “a”. | 18 |
| Q4 | S007 | §libinput debug-events (Note) | When submitting a bug report, always use the `--verbose` flag to get additional information: | 14 |
| Q5 | S007 | §libinput list-kernel-devices (Note) | This tool is intended for human-consumption and may change its output at any time. | 14 |
| Q6 | S009 | §Wayland Architecture | In wayland the compositor *is* the display server. | 8 |
| Q7 | S009 | §Wayland Architecture, step 2 | The compositor looks through its scenegraph to determine which window should receive the event. | 14 |
| Q8 | S042 | §Compositor features | Running `wayland-info` will list all global interfaces advertized by the compositor. (sic: "advertized") | 11 |
| Q9 | S042 | §Protocol dumpers | When using `export WAYLAND_DEBUG=1` (or `WAYLAND_DEBUG=client` or `WAYLAND_DEBUG=server`) is not enough (link markup on "is not enough" omitted) | 11 |
| Q10 | XML-1 | `wl_keyboard` description, lines 2575–2576 | The wl_keyboard interface represents one or more keyboards associated with a seat. | 12 |
| Q11 | XML-2 | `zwp_text_input_v3` description, lines 52–53 | The zwp_text_input_v3 interface represents text input and input methods associated with a seat. | 13 |
| Q12 | XML-2 | lines 67–70 | The focused surface must commit zwp_text_input_v3.enable and zwp_text_input_v3.disable requests as the keyboard focus moves across editable and non-editable elements of the UI. | 22 |

Counts are whitespace-split words of the quote as written here. Backticks and emphasis markers are counted as they appear in the source line. Q4, Q5, Q11 and Q12 were measured on the quote text as shown; line-wrap joins are the only transformation.

## 7. Findings and caveats

- **Frontier open.** U6 has no admitted knowledge note and no `covers: U6` line. R2 (event route) and R5 (IME) have no mined registry row. The R5 row is a candidate only.
- **Version drift.** Host libinput changed between two reads in this pass (§4.6). The S007 docs are a rolling latest page; they describe 1.32.0 at the time of reading. The pin must be measured at the time of use.
- **Owed anchors.** S007 and S009 lack revision-bound anchors (§4.1–4.2). A U6 admission cannot cite them as revision-bound until those rows are superseded.
- **Receipt precision.** Three round-14 mutation receipts lack the header the lane's own provenance rule asks for (§5 N6). This is recorded as R14-V1 and is not fixed here.
- **Not verified.** Hyprland's input dispatch, Hyprland input.conf effects on libinput, and any keyboard/pointer delivery on this host are not observed. They stay UNKNOWN.

## 8. Tooling record

- Installs or updates by this seat: none.
- Observed package change (not by this seat): libinput / libinput-tools at 1.31.3-1 in one read, 1.32.0-1 in later reads; install time recorded in §4.6. Cause unverified.

## 9. Out of scope, not done

- No edits to `corpus/`, `SOURCES.md`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `MANIFEST`, or configuration.
- No `measure.py`, gate, selftest, mutation run, or build.
- No input-event read, record, replay or injection; no `libinput list-devices` or `debug-events` run.
- No compositor, Hyprland, or config action.
- No subagent dispatch.
