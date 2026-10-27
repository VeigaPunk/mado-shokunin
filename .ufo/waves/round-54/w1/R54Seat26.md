# R54Seat26 — sentinel safety review (item 26)

Axes: **operability** (the claim must be decidable from committed source bytes) and
**coverage** (what the C2 claim is allowed to book). Attacked predicate: `PRED-C2-r54`
clauses (b) and (c) — `claims-frozen.md:55-65` — evaluated against the tree as it stands at
`HEAD e25149fec8152a3aabd2b18a0ee8663b23cf65aa` plus the round-54 integration that landed
during wave 1, and the wave's own safety fence (source-only scope, no host actions, no
protected-config changes, no domain-checkout writes).

No host/domain reads, no producer execution, no compositor/service/D-Bus contact, no git or
jj mutation. Read-only commands only; the sole writes are this report and scratch
(`/fast/scratch/hyaku/mado-r54/R54Seat26`, removed before yield).

## S26-1 HIGH — clause (b) is unsatisfiable as frozen; the landed rows make `TARGET_MET` reachable only by weakening the predicate

Verbatim probe of the three frozen quotes (raw bytes, interior-newline-normalized, and
newline+markdown-emphasis-normalized), plus the landed `teaches` cells at
`corpus/SOURCES.md:325-327`. Normalizations, exactly: newline layer is
`re.sub(r'[ \t]*\n[ \t]*', ' ', text)`; emphasis layer additionally removes `re.sub(r'\*+', '', …)`.
No other folding (case, whitespace runs inside a line, punctuation) was applied.

| row | frozen quote, raw | frozen quote, newline-norm | frozen quote, `*`-stripped | landed `teaches` cell (raw / norm / `*`-stripped) | frozen anchor |
|---|---|---|---|---|---|
| S375 | **absent** | present | present | **absent / absent / absent** | `README.md:117-118` — quote's tail `implementation is used)` is on line **119** |
| S376 | **absent** | **absent** (pin line 60 reads `*uwsm-app* client sends …`) | present | **absent / absent** / present | `uwsm-app.1.scd:60` |
| S377 | present (line 3714) | present | present | **absent / absent / absent** (landed cell is the paraphrase `unit name includes desktop and command substrings and random hexadecimal text`) | `uwsm/main.py:3714` |

Exact pin bytes behind the table:

```
$ sed -n '117,119p' .ufo/waves/round-54/fetch/uwsm-0.27.1-README.md
- Difference between environment state before and after preparation is exported
  into systemd user manager (and D-Bus activation environment if reference D-Bus
  implementation is used)
$ sed -n '60p' .ufo/waves/round-54/fetch/uwsm-0.27.1-uwsm-app.1.scd
*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon
$ sed -n '3714p' .ufo/waves/round-54/fetch/uwsm-0.27.1-main.py
            unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"
```

Exploit path. Clause (b) says the row's "`teaches`/quote cell's located quote … occurs
verbatim in the round-54 pin" (`claims-frozen.md:60-63`). A counter that tests the registry
cells it is pointed at cannot reach `rows=3/3`: S375 and S377 are absent under every
normalization, and S376 needs markdown emphasis stripped. A counter that instead tests the
frozen table in `registration.md` passes S377 and (normalized) S375 — and thereby never looks
at the registry, so the landed paraphrase cells (not source text at all) are admitted. Both
branches are defective, and no frozen control distinguishes them: C2-CTL-1's forged S376
quote (`sends arguments via a socket`) is far from any match under any relaxation, so the
control suite cannot detect a counter that swapped "verbatim" for "words from the quote
appear in the pin".

Impact. There is no honest `TARGET_MET` at the landed revision. Printing the frozen line
would assert `rows=3/3` of a property two rows do not have, and the verdict would certify
registry text as source text.

Smallest remediation (pre-data, new file — never edit `registration.md` or a pin): re-register
as `claims-frozen-v2.md` with (i) the S375 quote/anchor corrected to `117-119` (or the quote
truncated to the 117-118 text), (ii) an explicit normalization rule for quotes (markdown
emphasis stripped, interior newlines and line indentation collapsed to one space — the same
rule C1 already states), and (iii) a drift clause copied from C1: every registry `teaches`
cell must equal the frozen quote byte-for-byte modulo trailing spaces, else `TARGET_MISSED`.

## S26-2 HIGH — clause (c) is a transcription test, not evidence; the landed entry already fails the literal set (0/8)

```
$ python3 probe: frozen host strings literally present in the entry
~/.local/share/omarchy/default/hypr/autostart.conf:1..6   -> false x6
~/.config/hypr/bindings.conf:2                            -> false
~/.local/share/omarchy/bin/omarchy-toggle-idle:9          -> false
entry line 17 short forms: "autostart.conf" true, "bindings.conf:2" true,
                           "omarchy-toggle-idle:9" true, "lines 1–6" true
app names hypridle/mako/waybar/fcitx5/swaybg/omarchy-hyprland-monitor-watch
  in entry: true x6      in .ufo/waves/round-54/fetch/README.txt: true x6
```

`corpus/knowledge/uwsm-app-environment-r54.md:17` states the six `exec-once = uwsm-app -- …`
launches, the `bindings.conf:2` terminal route and the `omarchy-toggle-idle:9` idle re-arm;
line 2 carries `verified-at: 2026-10-27`. Every one of those host facts is verbatim in the
committed L1 prose `.ufo/waves/round-54/fetch/README.txt` (join paragraph and the same six
app names), which no wave seat may obtain by reading the host — seats are barred from host
reads, so the entry is necessarily a transcription of that prose and the `verified-at` line
re-asserts L1's read.

Exploit path. Copy the manifest paragraph into the entry: a basename/alias-relaxed counter
scores ≥2 joins with no host byte behind them, indistinguishable from an invented join.
A literal-set counter rejects the landed entry (0/8) → `TARGET_MISSED` even though the entry
is the intended deliverable. C2-CTL-6 (`entry text carries none of the frozen host set`,
`registration.md:87`) only tests absence, so it cannot see the difference.

Impact. The provenance trio certifies a host claim whose only in-repo support is the same
actor's prose manifest; the coverage claim books host declarations it cannot evidence.

Smallest remediation. In v2 either drop clause (c) or bind it to committed evidence: L1
commits a pre-freeze capture (`round-54/hostjoins/` with the joined line text and per-file
sha256) and clause (c) requires the entry to cite the capture path, not the host path;
require distinct locations (Seat22/23) and forbid basename matching. Keep the entry's
wording at "declared launch route" (it already does at line 17) with the provenance labelled
as L1's pre-freeze record, not the authoring seat's verification.

## S26-3 HIGH (province) — two of the three frozen propositions are systemd user-manager ground

S375's fact is *export into the systemd user manager (and D-Bus activation environment)*; S377's
fact is transient app **unit** naming (scope/service). `PROVINCE.md:34` rules that mado's
"unit-state rows sit next to tsukuroi's unit-health ground, **which stays tsukuroi's**", and
`PROVINCE.md:96` records the same routing for runtime-IPC ground (tsukuroi OUT-004 holds the
runtime half). The province owns the config plane and display behavior; the C2 surface is
declared as the owned chain's *launcher half* (`claims-frozen.md:46-53`).

The landed entry repeats both facts as core sourced content (line 9: environment export to
the systemd user manager; line 13: generated unit name from `main.py:3714`), while conceding
at line 17 that "No process, unit, environment, D-Bus state or compositor behavior was
probed".

Impact. Two thirds of the coverage gain is booked on session-manager/unit state that this lane
neither owns nor measures; a later reader can mistake the systemd environment export for
mado-sourced ground.

Smallest remediation. Keep S375/S377 as boundary citations marked "systemd user-manager/unit
ground — not absorbed", and ground the entry's own facts on S376 plus the declared host launch
lines; or add one append-only PROVINCE refinement naming the systemd environment/unit-name
contract as read-only shared documentation ground before the round scores it as coverage.

## S26-4 MEDIUM — scored content landed mid-wave with no attribution receipt

```
$ git rev-parse HEAD
e25149fec8152a3aabd2b18a0ee8663b23cf65aa
$ git status --porcelain --untracked-files=all -- corpus/ tools/ quality/ LOG.md SCORECARD.md
 M corpus/README.md
 M corpus/SOURCES.md
?? corpus/knowledge/uwsm-app-environment-r54.md
?? corpus/lessons/round-54.md
$ stat -c '%n %y' corpus/knowledge/uwsm-app-environment-r54.md corpus/SOURCES.md
corpus/knowledge/uwsm-app-environment-r54.md 2026-10-27 14:07:00 -0300
corpus/SOURCES.md                            2026-10-27 14:08:20 -0300
```

`receipts/before.txt` (13:57:27) records entry 0, index 69, last row S374 — the landed files
appeared ten minutes later, during wave 1, with no receipt in the wave or receipts directory
naming the actor, the command or the revision that landed them. Seat bounds are "wave-dir
reports only"; the frozen target is "the round's final content revision"
(`claims-frozen.md:68`). Seats now score a tree that moved after dispatch, and w2 attackers
inherit content nobody receipted.

Smallest remediation. One integration receipt per landing (actor, command, paths, content
revision, timestamp) under `.ufo/waves/round-54/receipts/`, and C2's `--rev` must name the
revision that contains the entry/rows. Do not amend the frozen files.

## S26-5 MEDIUM — pin identity rests on a mirror and prose

`fetch/README.txt:3-5` records that the pins come from the GitHub mirror of
`Vladimir-csp/uwsm` at tag commit `0727985c…`, that the freedesktop primary carried only
tags ≤ v0.27.0 at open time, and that the host's `uwsm --version` → `uwsm 0.27.1` with
`/usr/bin/uwsm-app` present. Bytes are immutable and verified:

```
$ cd .ufo/waves/round-54/fetch && sha256sum -c SHA256SUMS.txt ; echo "exit=$?"
uwsm-0.27.1-README.md: OK
uwsm-0.27.1-main.py: OK
uwsm-0.27.1-uwsm-app.1.scd: OK
exit=0
```

But "these bytes are upstream v0.27.1" is a single-actor tag→commit mapping over a mirror,
and the host-install observation exists only as prose.

Smallest remediation. Record the tag object id (and signature, if present) plus a second-source
digest for at least one file from the primary GitLab in `fetch/README.txt`, and label the
host-install line as L1 pre-freeze prose rather than seat-verified fact.

## S26-6 LOW — counter safety invariants the C2 build must hold

1. Read only git objects of `--repo`/`--rev`; no `expanduser`, no `HOME`, no `~` resolution,
   no host path, no network, no subprocess outside the selftest's own child.
2. `--work <dir>` only; no `/tmp` hardcode; `--selftest` ≥30 assertions with one red run per
   control.
3. Never rewrite the pins or `SHA256SUMS.txt` (hashes match today, so any rewrite is
   detectable); compare against the frozen digests as well as the revision's manifest
   (Seat18's coordinated-mutation point generalizes to C2).
4. Clause (c) matching must be literal against the frozen set (or the proposed capture path);
   basename/alias matching is the forgeable form demonstrated in S26-2.

## Safety fence attestation

- No host or domain checkout read, no config tree touched, no compositor/service/D-Bus call,
  no package query, no screenshot/input capture, no producer execution.
- Writes: this report only, plus scratch `/fast/scratch/hyaku/mado-r54/R54Seat26` (removed
  before yield). No tracked lane edit, no git/jj mutation, no PATH-directory write.
- Pins unmodified (hash receipt above). No tool installed or updated (`/home/vgpnk/.omp/agent/RULES.md`
  read; nothing needed).

## Distinctness from sibling seats

Seat22 (duplicate-join threshold) and Seat23 (alias spelling) attack clause (c)'s counting;
Seat36 attacks the semantic overclaim of a *valid* join; Seat37 attacks prose admission;
Seat18 attacks C1's manifest authority; Seats 10-13 are frontier recon. This seat's distinct
input is byte-level falsification of all three frozen quotes across three normalization layers
(raw / newline / emphasis) plus an audit of the registry and entry as they were *actually
landed* at 14:07-14:08 — none of the sibling reports read the landed artifacts, because they
did not exist when those reports were written.

## Commands run (exact, read-only)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
git rev-parse --show-toplevel ; git rev-parse HEAD ; git status --porcelain --untracked-files=all
git show HEAD:corpus/SOURCES.md | grep -c 'S375\|S376\|S377'      # 0  (base has no rows)
git ls-tree HEAD corpus/knowledge/ | grep r54                     # empty (base has no entry)
cd .ufo/waves/round-54/fetch && sha256sum *.md *.py *.scd          # == SHA256SUMS.txt, 3/3
grep -cF "*uwsm-app* client sends arguments to uwsm's app daemon via a pipe." uwsm-0.27.1-uwsm-app.1.scd   # 1
grep -cF "uwsm-app client sends arguments to uwsm's app daemon via a pipe."  uwsm-0.27.1-uwsm-app.1.scd   # 0
python3 -I verbatim2.py    # per-row raw/norm/emphasis-strip presence + landed teaches cells
python3 -I entryprobe.py   # 0/8 frozen host strings in entry; app names and joins in fetch/README.txt
stat -c '%n %y' corpus/knowledge/uwsm-app-environment-r54.md corpus/SOURCES.md
cat .ufo/waves/round-54/receipts/before.txt
```

Verdict on the attacked predicate: **PRED-C2-r54 is not satisfiable honestly at the landed
revision** — clause (b) fails for S375/S376/S377 as landed (and its S375 anchor is off by one
line even in the frozen table), clause (c) fails literally (0/8) and is only met by
transcription under a relaxed matcher, and two of the three frozen facts are outside the
province's owned ground. Honest stop or pre-data re-registration under a new versioned claims
file.

Report: `.ufo/waves/round-54/w1/R54Seat26.md`
