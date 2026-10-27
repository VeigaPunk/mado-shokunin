# R54Seat31 — round-54 wave-1 attack: the frozen C1 contract has two admissible readings that disagree on two of its own six controls

Seat: `R54Seat31` (executor, wave 1). Axis focus: coverage + operability.
Base/freeze under test: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; freeze commit `350d30e4ec5531f65ce99a57efeb8216f38e678a`.
Scratch (all fixtures, clone, scripts): `/fast/scratch/hyaku/mado-r54/R54Seat31` — removed at yield.
No lane tracked file was edited; no `git`/`jj` mutation in the lane; the only `git` mutations were inside the scratch clone.

## Attacked predicate

`MADO_ERRATA_TRUTH: rev=<rev> propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET`
— frozen at `.ufo/waves/round-54/claims-frozen.md:19-30` (PRED-C1-r54, clause (d): "each of the six frozen C1 controls of `registration.md` is rejected by the counter"), with the six controls at `.ufo/waves/round-54/registration.md:40-47`.

## Axes named (godspeed)

| axis | what moves it | status here |
|---|---|---|
| **operability** (C1, record-instrument) | a counter that rejects its six frozen controls is *reproducible by an auditor* | **attacked** — the frozen sentence does not determine which counter is admissible |
| **coverage** (C2, sourced entry) | the C2 legs that read pins/registry | **attacked** — two of the three frozen C2 quotes are not present in the frozen pin at all (corroborates sibling M54-3) |
| honesty | a frozen claim that cannot be falsified is not a claim | **attacked** — `controls=6/6` is self-reported |

---

## Finding 1 (primary, distinct): the frozen C1 sentence admits two counter contracts that disagree on CTL-2 and CTL-4 — so "controls=6/6" is auditor-reproducible only if the auditor guesses the right one

`claims-frozen.md:22-30` states C1 as four clauses (a)–(d). Clause (b) fixes the anchor side-claims as **absolute facts about the pin**: "P19 at exactly ConfigActions.cpp:1554-1558; P20 at exactly :1576; …". It never says the *entry's* `Pin:anchor` cell must equal those anchors.

`registration.md:21-23` adds a clause the frozen sentence does not contain: "the counter extracts the committed entry's P19–P22 rows and **checks them against THIS table byte-for-byte modulo trailing spaces**; any drift is a TARGET_MISSED".

Both documents are frozen and both govern. Two counter implementations satisfy every clause of `claims-frozen.md`; they disagree on whether CTL-2 and CTL-4 are rejected.

**Measurement.** Six control trees built as real git commits in a scratch clone of the lane (`git clone --no-hardlinks <lane> clone`), each mutating exactly what `registration.md:40-47` names, then run under two contracts that differ *only* in the anchor-cell binding (same judge, same hash source):

```
$ python3 ref6.py --repo <clone> --rev <rev> --contract {claims-frozen|registration} --hash-source tree-sums
### contract=claims-frozen (predicate sentence only)
BASE     ... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=0/6 verdict=TARGET_MET
CTL-2    ... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=0/6 verdict=TARGET_MET   <-- ADMITTED
CTL-4    ... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=0/6 verdict=TARGET_MET   <-- ADMITTED
### contract=registration (adds byte-for-byte table comparison)
BASE     ... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=0/6 verdict=TARGET_MET
CTL-2    ... propositions=4/4 quotes=3/4 anchors=3/4 pins=4/4 controls=0/6 verdict=TARGET_MISSED
CTL-4    ... propositions=4/4 quotes=3/4 anchors=3/4 pins=4/4 controls=0/6 verdict=TARGET_MISSED
```

Under the frozen sentence alone, **CTL-2 (shifted anchor `:1576`→`:1575`) and CTL-4 (P21 anchor moved to `:573`) are admitted** — the quote is still found in the pin at the frozen side-claim location, so every clause (a)–(c) still holds. The counter prints `controls=6/6 verdict=TARGET_MET` on two of the six trees the registration says it must reject. Under `registration.md`'s extra byte-for-byte clause both are correctly rejected.

**Why this is the claim's own kill rule.** `claims-frozen.md:37-39`: "if any frozen C1 control is admitted by the counter … the counter prints `verdict=TARGET_MISSED` and a non-zero exit — the claim is dead for the round". So an auditor cannot tell, from the frozen text alone, whether a submitted counter that reports `controls=6/6` is honest or is running the `claims-frozen` reading and has admitted CTL-2/CTL-4. The verdict label is not a sufficient check.

**Exact commands.** Fixture construction (scratch clone, `git rev-parse --show-toplevel` asserted as the clone before each commit):

```
$ cd /fast/scratch/hyaku/mado-r54/R54Seat31/clone
$ git rev-parse --show-toplevel      # -> /fast/scratch/hyaku/mado-r54/R54Seat31/clone
$ git config user.email seat@example.invalid && git config user.name R54Seat31
# CTL-2: P20 anchor :1576 -> :1575 in the entry
$ python3 -c 'p="corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"; s=open(p).read(); assert "Hyprland-ConfigActions.cpp:1576" in s; open(p,"w").write(s.replace("Hyprland-ConfigActions.cpp:1576","Hyprland-ConfigActions.cpp:1575",1))'
$ git commit -qam "CTL-2 shifted-anchor" && git rev-parse HEAD   # -> 431518e2422c797430e8b8ceaf3beb93026caae2
# CTL-4: P21 anchor moved to :573
$ python3 -c 'p="corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"; s=open(p).read(); assert "Hyprland-legacy-DispatcherTranslator.cpp:619-622" in s; open(p,"w").write(s.replace("Hyprland-legacy-DispatcherTranslator.cpp:619-622","Hyprland-legacy-DispatcherTranslator.cpp:573",1))'
$ git commit -qam "CTL-4 wrong-range" && git rev-parse HEAD      # -> 3a2392d3c374d4a544851b2921869d68aab64409
```

**Smallest safe correction** (no frozen file is edited by this seat): the next versioned freeze must put the entry↔table comparison *inside the predicate sentence* — e.g. clause (b) becomes "each anchor side-claim holds **and the entry's Pin:anchor cell equals it**" — so that one contract is determined. This is a pre-data re-registration under `claims-frozen-v2.md`, exactly the mechanism `claims-frozen.md:5-7` reserves. Editing `claims-frozen.md` in place after seats have scored is forbidden.

---

## Finding 2 (secondary, distinct): the frozen hash anchor has two admissible sources with opposite verdicts — one admits a self-consistent pin forgery, the other admits CTL-3

Clause (c) — `claims-frozen.md:28-29` — "each of the four pins' bytes hash to **the round-52 recorded sha256**". Two sources are admissible and they give opposite verdicts on the frozen control CTL-3 and on a coordinated forgery:

* **Source A — the frozen table.** `registration.md:14-19` lists the four round-52 sha256 values; `registration.md:12` calls them "its committed `SHA256SUMS.txt`". Note: **that file does not exist** — the round-52 fetch dir has `SHA256SUMS` (no `.txt`): `ls .ufo/waves/round-52/fetch/` → `Hyprland-ConfigActions.cpp … README.txt  SHA256SUMS`. The four table values do match the committed `SHA256SUMS` lines.
* **Source B — the tree's own `SHA256SUMS`.** `claims-frozen.md:81` puts `.ufo/waves/round-52/fetch/` (+SHA256SUMS) in C1's read set, and `registration.md:44` makes CTL-3 mutate "the tree's SHA256SUMS".

**Measurement** (identical counter, only the expected-hash source varies; control trees are the same scratch commits):

```
$ python3 ref4.py --repo <clone> --rev <rev> --hash-source {tree-sums|table}
### hash-source=tree-sums   (expected hash read from the tree's SHA256SUMS)
CTL-3    ... pins=3/4 verdict=TARGET_MISSED     <-- CTL-3 correctly rejected
FORGE-A  ... pins=4/4 verdict=TARGET_MET       <-- coordinated forgery ADMITTED
### hash-source=table      (expected hash from registration.md's frozen table)
CTL-3    ... pins=4/4 verdict=TARGET_MET       <-- CTL-3 ADMITTED
FORGE-A  ... pins=3/4 verdict=TARGET_MISSED
```

`FORGE-A` is a coordinated forgery built with git plumbing in the scratch clone: **the pin's bytes are changed and the recorded sha256 in the tree's `SHA256SUMS` is updated to match**, so the tree stays internally self-consistent. Under source B it is admitted (`pins=4/4`, `verdict=TARGET_MET`); under source A it is rejected. No frozen control covers FORGE-A — the six controls (`registration.md:40-47`) never mutate a pin together with its recorded hash.

**Exact commands.**

```
$ cd /fast/scratch/hyaku/mado-r54/R54Seat31/clone
$ python3 - <<'PY'
import hashlib
hpp=".ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp"
b=bytearray(open(hpp,'rb').read()); b+=b"\n// forged tail (not read by any proposition)\n"
open(hpp,'wb').write(bytes(b))
new=hashlib.sha256(bytes(b)).hexdigest()
s=".ufo/waves/round-52/fetch/SHA256SUMS"; t=open(s).read()
old="746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073"; assert old in t
open(s,"w").write(t.replace(old,new,1)); print("new hpp sha:",new)
PY
# -> new hpp sha: 1e9c6ff0a90bee5a77aedc56f6f1f0d73215d883e926c860b1a8fc4db5f93476
$ git commit -qam "FORGE-A self-consistent pin+sha forgery" && git rev-parse HEAD  # -> 49c52162c37d920c2ff6ad27a418ef10d6fca944
```

**Why this matters beyond a documentation nit.** The pinned bytes are the round-52 *fetched* artifacts; the pin set includes `Hyprland-ConfigActions.hpp`, which **no proposition quotes** (P19/P20 quote the `.cpp`; P21/P22 quote the legacy dispatcher). So a counter whose expected hashes come only from the tree's own manifest can be satisfied by editing an unquoted pin and its recorded hash, and the proposition/quote/anchor legs stay green. The frozen control set has no case for this.

**Smallest safe correction.** Freeze the expected-hash source explicitly (e.g. "the four sha256 values in the registration table, verbatim; the tree's `SHA256SUMS` is additionally required to agree with them") and add a seventh control that changes a pin's bytes *and* its recorded hash together, requiring `pins≤3/4`.

---

## Finding 3 (distinct): `controls=6/6` is a self-reported number — the counter is its own control author, and no frozen control fixture trees exist for round 54

`claims-frozen.md:41-44` states the do-nothing control: "a counter that prints the frozen line without reading git objects fails the six control runs (each control is a mutated tree the counter must reject; an always-print counter accepts them → `controls<6/6`)". Receipt: "the counter's own control run is committed per control".

That defence assumes the six control *trees* are fixed and known to the auditor. They are not:

* There is **no** `.ufo/waves/round-54/controls/` directory (contrast round 52, which shipped `.ufo/waves/round-52/controls/c1-do-nothing.md`, `c1-row-context-control.md`, `c2-do-nothing.md`; round 53 shipped none; round 54 ships none).
* `registration.md:36-38` says only "run against mutated trees — the counter reads all inputs from `--repo`/`--rev` git objects, so a control = a mutated copy of the scored tree". It never freezes the mutation *content* as bytes; it names them in prose.

**Measurement — level 1, always-print.** A counter that reads no git object and prints the frozen line verbatim:

```
$ python3 donothing.py --repo <clone> --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a --work <scratch>
MADO_ERRATA_TRUTH: rev=350d30e4ec5531f65ce99a57efeb8216f38e678a propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
```
It prints the byte-identical frozen line (compare `claims-frozen.md:21`) and exits 0 at **every** rev, including all six mutated control trees. `claims-frozen.md:41-44` calls this out and says it "fails the six control runs" — but that is only true if the control trees are externally fixed.

**Measurement — level 2, self-authored controls.** The counter builds its own six control trees as *arbitrary* corruptions it happens to detect (here: each pin file's bytes tampered), never the six named mutations, and self-reports `controls=6/6`:

```
$ python3 selfctrl.py --repo <clone> --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a --hash-source tree-sums
MADO_ERRATA_TRUTH: rev=350d30e4ec5531f65ce99a57efeb8216f38e678a propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
```
Its six self-authored trees are the same pin-tamper corruption six times over; the two *named* controls CTL-2 and CTL-4 are **admitted** by the same counter (Finding 1). So `controls=6/6` on the frozen line is satisfied by a counter whose six "controls" are not the six frozen controls.

**Exact commands.** Control trees are created with git plumbing in the scratch clone (no working-tree copy):

```
$ python3 - <<'PY'
import os,subprocess,tempfile
repo=os.path.abspath("clone"); rev="350d30e4ec5531f65ce99a57efeb8216f38e678a"
env=dict(os.environ); env["GIT_INDEX_FILE"]=tempfile.mktemp()
subprocess.run(["git","-C",repo,"read-tree",f"{rev}^{{tree}}"],env=env,check=True)
p=".ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp"
blob=subprocess.run(["git","-C",repo,"rev-parse",f"{rev}:{p}"],capture_output=True,text=True).stdout.strip()
data=subprocess.run(["git","-C",repo,"cat-file","blob",blob],capture_output=True).stdout
nb=subprocess.run(["git","-C",repo,"hash-object","-w","--stdin"],input=data+b"//x\n",capture_output=True).stdout.decode().strip()
subprocess.run(["git","-C",repo,"update-index","--cacheinfo",f"100644,{nb},{p}"],env=env,check=True)
t=subprocess.run(["git","-C",repo,"write-tree"],env=env,capture_output=True,text=True).stdout.strip()
print(subprocess.run(["git","-C",repo,"commit-tree",t,"-p",rev,"-m","x"],capture_output=True,text=True).stdout.strip())
PY
# -> 167dc347f8608dba0913c60ed7900b3b69a6752d
```

**Smallest safe correction.** Commit the six control trees (or the six mutated-tree recipes with expected verdicts) under `.ufo/waves/round-54/controls/`, and require the counter to accept their revs as input so `controls=6/6` is a claim an auditor re-derives rather than a self-report.

---

## Finding 4 (corroborating, C2 side): two of the three frozen C2 located quotes are absent from the frozen pin — and one of the three landed `SOURCES.md` rows' quotes is a paraphrase

Corroborates sibling lesson M54-3 for the byte-verbatim leg; my distinct measurement is the **collapse** leg and the **row-shape** leg.

```
$ python3 c2verify.py
=== S375  pin=uwsm-0.27.1-README.md  declared location :117-118
    quote (24 words): 'Difference between environment state before and after preparation is exported into systemd user manager (and D-Bus activation environment if reference D-Bus implementation is used)'
    verbatim byte-contiguous in pin : False
    whitespace-collapsed span       : (117, 119)   (declared (117, 118))   <-- span != declared range
=== S376  pin=uwsm-0.27.1-uwsm-app.1.scd  declared location :60
    quote (11 words): "uwsm-app client sends arguments to uwsm's app daemon via a pipe."
    verbatim byte-contiguous in pin : False
    whitespace-collapsed span       : None   (declared (60, 60))            <-- quote absent entirely
    declared lines text: ["*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon"]
=== S377  pin=uwsm-0.27.1-main.py  declared location :3714
    verbatim byte-contiguous in pin : True
    whitespace-collapsed span       : (3714, 3714)   (declared (3714, 3714))
```

Two independent defects beyond byte-verbatimness:

1. **S376's quote is not in the pin at all**, under *any* normalisation: the scdoc source renders the program name as `*uwsm-app*` (emphasis markers). `grep -c "uwsm-app client sends arguments to uwsm's app daemon via a pipe\." uwsm-0.27.1-uwsm-app.1.scd` → `0`; with the markers → `1`. So no collapse/trim rule reaches it. Clause (b) of `claims-frozen.md:60-62` ("its `teaches`/quote cell's located quote (≤25 words) occurs verbatim in the round-54 pin named by its source file") is unsatisfiable for S376 as frozen — a de-marking rule would have to be frozen too, and none is.
2. **S375's quote spans lines 117–119 but the registration declares `:117-118`.** The quote's third line ("implementation is used)") is on line 119. A counter that checks "quote lies within the declared range" fails the frozen fixture itself.

**Row-shape defect.** The predicate reads the quote from the row's `teaches`/quote cell. The three landed rows in `corpus/SOURCES.md` do **not** carry the located quote in that cell — they carry paraphrases, and the located quote lives in the *lesson* Gate (`corpus/lessons/round-54.md:9-11`), which is **outside C2's read set** (`claims-frozen.md:82-85`: "C2 reads only … `corpus/SOURCES.md` and `.ufo/waves/round-54/fetch/` … Shared record files (README registry table, SOURCES.md, **lesson**, LOG, SCORECARD) are integration surfaces, **not claim evidence**"). Measured:

```
$ python3 c2rows.py
=== S375  teaches-cell = 'Difference before and after preparation is exported into systemd user manager'
    landed teaches verbatim-in-pin=False  collapsed-in-pin=False
    landed teaches == frozen quote? False
=== S376  teaches-cell = "uwsm-app client sends arguments to uwsm's app daemon via a pipe"
    landed teaches verbatim-in-pin=False  collapsed-in-pin=False
=== S377  teaches-cell = 'unit name includes desktop and command substrings and random hexadecimal text'
    landed teaches verbatim-in-pin=False  collapsed-in-pin=False
```

So the quote C2 is told to verify is in neither the row's `teaches` cell nor the entry. Checked directly: none of the three frozen quotes occurs in `corpus/knowledge/uwsm-app-environment-r54.md` either (`S375 verbatim=False collapsed=False`, same for S376, same for S377). Clause (b) names a location that holds none of the three quotes.

**Smallest safe correction.** Freeze, per row, *which cell* carries the located quote and freeze the quote strings that are actually present in the pinned bytes (de-marking `*uwsm-app*` for S376, widening S375's declared range to `:117-119`), or freeze the quote→cell binding to the lesson Gate and add the lesson to C2's read set. Both are pre-data re-registration items; no frozen file was edited by this seat.

---

## Finding 5 (corroborating, C1 side): the frozen P19/P21/P22 quotes are space-joined, so the registration's own "verbatim" judge sentence is unsatisfiable as written

`registration.md:51-53` fixes the judge: "Judge of 'verbatim': **exact byte contiguity** after single-space normalization of interior newlines **ONLY where the frozen quote itself carries a newline** (P19/P21/P22 are single logical lines)".

The frozen quotes for P19, P21 and P22 are single-line (no newline) — so per that sentence no newline normalisation is permitted for them, and they must be byte-exact contiguous. They are not: each is a whitespace-joined rendering of a multi-line region that **elides a blank source line**.

```
$ python3 noelide.py
P19: collapsed span 1554-1558; frozen anchor 1554-1558
    span text == full collapsed text of frozen range? False     # the blank line 1555 is elided
    byte-exact contiguous in pin: False
P21: collapsed span 619-622; frozen anchor 619-622
    span text == full collapsed text of frozen range? False     # the blank line 620 is elided
    byte-exact contiguous in pin: False
P22: collapsed span 573-574; frozen anchor 573-574
    span text == full collapsed text of frozen range? True
    byte-exact contiguous in pin: False
```

Note the *shape*: P19's frozen quote is `…sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(…` — the source has a **blank line at 1555** between `sendKeyboardMods` and `if (S.m_passPressed`, so the frozen quote is not a contiguous excerpt of the pin even after whitespace-collapsing (it is only found because collapsing also erases the blank line). The frozen anchor side-claim "P19 at exactly ConfigActions.cpp:1554-1558" is satisfied by the collapsed span, but the quote is a **reconstruction**, not an excerpt.

This is the same defect class the round-52 verifier recorded for P16 ("the space-joined quote `sendKeyboardMods(modMask, 0, 0, 0); sendKeyboardKey(…)` occurs nowhere contiguously in `Hyprland-ConfigActions.cpp`") — `corpus/lessons/round-52-verifier-spotcheck.md`, §2 C2 bullet. The r53 errata fixed P16's *proposition* but kept the space-joined *quote* form, and round 54's freeze froze that form again as the target's own table. Under the registration's literal judge the honest tree scores `quotes=1/4`:

```
$ python3 ref2.py --repo <lane> --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a --judge literal --hash-source table
MADO_ERRATA_TRUTH: rev=350d30e4ec5531f65ce99a57efeb8216f38e678a propositions=4/4 quotes=1/4 anchors=1/4 pins=4/4 controls=0/6 verdict=TARGET_MISSED
   detail: P19:quote-not-found[literal]
   detail: P21:quote-not-found[literal]
   detail: P22:quote-not-found[literal]
$ python3 ref2.py --repo <lane> --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a --judge collapse --hash-source table
MADO_ERRATA_TRUTH: rev=350d30e4ec5531f65ce99a57efeb8216f38e678a propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=0/6 verdict=TARGET_MET
```

So the C1 target's attainability depends on which of the two readings of the judge sentence is taken — the registration's literal one (`quotes=1/4`, TARGET_MISSED on the honest tree) or the lane's house standard (whitespace-collapsed, word-bounded; `quality/counters/c2-r47-terminal-entry.py:55`, `quality/counters/c2-r49-bind-entry.py:57`, both of which say "verbatim (whitespace-collapsed, word-bounded)"). The lane's own convention and the round-54 registration's sentence disagree, and the registration's sentence is the one that governs the target.

**Smallest safe correction.** In the v2 freeze, either (a) state the judge as whitespace-collapsed-with-blank-line-elision-bounded and require the *whole* range (not a reconstruction) to be quoted, or (b) re-quote P19/P21/P22 as exact contiguous excerpts of single physical lines. Do not edit `registration.md` after seats have scored.

---

## Files changed

* `.ufo/waves/round-54/w1/R54Seat31.md` — this report (the only file written in the lane; wave-dir report path assigned to this seat).
* Scratch (created and **removed** at yield): `/fast/scratch/hyaku/mado-r54/R54Seat31/` — `clone/` (scratch git clone with the six control commits + FORGE-A/FORGE-B), `ref2.py ref3.py ref4.py ref5.py ref6.py`, `donothing.py`, `selfctrl.py`, `qcheck.py`, `span.py`, `c2q.py`, `c2rows.py`, `c2verify.py`, `noelide.py`, `revs/`. Lane `git status` shows no new tracked modifications from this seat.

## Behaviour of the lane (unchanged by this seat)

No lane edit, no commit, no push, no host/compositor/service/config write, no campaign tool, no domain/host read, no screenshot, no package query, no producer execution. Only static committed pins were read (`.ufo/waves/round-52/fetch/`, `.ufo/waves/round-54/fetch/`), plus the frozen `claims-frozen.md` / `registration.md` and the committed `corpus/` files. The lane's own working tree (`corpus/SOURCES.md` modified, `corpus/knowledge/uwsm-app-environment-r54.md` untracked, `corpus/lessons/round-54.md` untracked) is the pre-existing state of other seats' work and was not modified here.

## Tool / version / channel updates

**None.** No package was installed or updated this run (no `pacman`, no `uv tool install`, no release binary, no `cargo`/`npm -g`). Tools used, all pre-existing: `git` (system), `python3` 3.14 (system interpreter, `python3 -I` not required for the scratch probes), `grep`/`sed`/`sha256sum` (coreutils), `shutil`/`hashlib`/`subprocess`/`tempfile` (stdlib). Reason for no update: the attack needed only byte-level text/git plumbing already present; nothing in the task required a newer tool.

## Risks / blockers

* Findings 1, 2 and 5 are **pre-data defects in the freeze**, not counter bugs. Per `claims-frozen.md:5-7` ("a falsified predicate is an honest stop or a pre-data re-registration under a NEW versioned file, never an edit of this one"), they are routed as re-registration items under `claims-frozen-v2.md` / a v2 registration; this seat edited neither file.
* Finding 4's S376 leg is the same defect family as sibling lesson M54-3 (already in `corpus/lessons/round-54.md`). It is reported here because the seat was asked to test a distinct input; the *new* part is the collapse leg (S376 is absent under every normalisation, not merely non-byte-verbatim), the S375 range mismatch (`:117-118` vs actual `:117-119`), and the row-shape/read-set defect (the quote is in neither the row's `teaches` cell nor the entry).
* Whether a wave-2 auditor can reproduce any `controls=6/6` at all depends on the counter landing its own control trees; if the counter does not commit them, Finding 3 stands unmitigated.
* Not verified here (out of this seat's read scope): whether the lane's `tools/mado-verify.sh --selftest` still reports 460/460 and whether the sources census still exits 0 — no lane writes were made, so neither should be affected, but this seat did not re-run them.
