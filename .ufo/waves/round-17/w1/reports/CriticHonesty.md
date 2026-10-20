author: MadoR17.CriticHonesty (critic seat, round 17 w1; advisory only — I do not judge or admit)

# Critic: round-17 honesty plan — R15-V1, operability wording, admission language

Read first: `corpus/lessons/round-16-verifier-spotcheck.md` (all 185 lines).
Also read: SCORECARD.md l.640–700, 790–865; QUALITY.md l.72, 82, 107;
the drafts `ScoreTableDraft.md`, `ReportSkeleton.md`, `LessonDraft.md`,
`QualityDraft.md`, `SkillRegistryDraft.md`, `FrontierDraft.md` (via grep); the
watchdog launch line; and `/var/log/pacman.log`. I read that log as a file with
`grep`/`cut` only, which the contract allows. I ran no package, service,
compositor, probe or jj command. I read no OMP transcript; my item names none.
`tools/mado-tripwire.py` had not landed at 2026-10-20T11:01-03:00, so the
points about tool output below are about the contract, not about observed runs.
I installed or updated no tools.

## Finding 1 (high): the host's pacman "pause" premise does not hold, so R15-V1 is now `[UNK]`. It is not "unresolved and unchanged"

**Counterexample from the log** (`/var/log/pacman.log`; I read it as a file only). Between the end of round 16 (06:06:30) and the round-17 launch (10:51:22), these transactions ran on the host:

| Line | Time (-03:00) | Command (as `[PACMAN] Running`) |
|---|---|---|
| 2440 | 07:45:36 | `pacman -S --needed --noconfirm compsize pacman-contrib` |
| 2448 | 07:50:25 | `pacman -S --needed --noconfirm fclones` |
| 2454 | 08:14:12 | `pacman -Rns --noconfirm electron39 mbedtls` |
| 2461 | 08:20:52 | `pacman -Sw … limine-mkinitcpio-hook plymouth mkinitcpio` |
| 2462 | 09:15:30 | `pacman -Syu --needed --noconfirm nvme-cli … linux-lts …`: a **full system upgrade**, including `mkinitcpio (41.1-1 -> 42.2-1)`, `linux (7.2.3.arch1-3 -> 7.2.11.arch1-1)`, `libevdev`, `libwacom`, `hyprland`, `walker`, `plymouth`, `limine` |
| 3064–3152 | 09:27–09:39 | `fwupd` install, `go` install and removal, `pacman -U` of yay-built `elephant` packages, two `-Rns` |

There are 0 `[PACMAN]` or `[ALPM]` transaction lines after 09:39:21. The 10:51:22 launch time comes from `.ufo/watchdog.log` l.480.

`/proc/uptime` read 3878 s at 11:01:19, so the host booted at about 09:56. `uname -r` printed `7.2.11-arch1-1`, which means the host rebooted into the upgraded kernel. The R15 harm itself is at `pacman.log:2429-2436`: `pacman -S --needed --noconfirm libinput libinput-tools` at 04:25:16, `libinput 1.31.3-1 -> 1.32.0-1`.

**Why it matters.** R15-V1 is a **partial upgrade**: libinput moved ahead of an unsynced system. A later full `-Syu` plus a reboot plausibly changes that condition `[INFERENCE]`. Nobody has adjudicated that, and the lane must not try. Two opposite overreaches are now both live:

- (a) "The host-wide pause held since R15", or "no package transaction since round 15". This is false on the log. The pre-registration says "Host pause carried" (SCORECARD l.825). That phrase is acceptable only as a statement about what the *lane* was allowed to do. It must not be stated, or read, as a fact about the host.
- (b) "R15-V1 resolved (operator full upgrade)". This is not established. The actor of the 07:45–09:39 transactions is `[UNK]`. Whether those transactions repair or compound the R15 state is `[UNK]`. Disposition stays operator-owned. `ScoreTableDraft.md` l.57 offers the slot `<carried / resolved by operator>`. That slot invites (b) and must lose the "resolved" option. The lane may only quote an operator disposition if one exists in writing.

**Smallest correction.** In SCORECARD, the report and the lesson, state the window-scoped fact plus the disclosure, for example:

> R15-V1 carried, operator-owned, not resolved by this lane. Host-log fact: non-lane pacman transactions, including a full `-Syu` (09:15:30), ran between rounds 16 and 17 (`pacman.log:2440–3152`; actor `[UNK]`); the R15 partial-upgrade condition's current state is `[UNK]` and not adjudicated here. In the round-17 window `[10:51:22, <close>]`: `<n>` transactions.

Re-measure `<n>` at close with the same grep. `ReportSkeleton.md` l.105 has the slot `Host-wide pause in force: {{PAUSE_STATE}}`. Fill it as "lane pause binding on seats; host log shows non-lane transactions before launch". Do not fill it with "yes".

**Impacted axes:** operability (host-safety row), calibration (claim/receipt match), adjacency (host recovery stays routed, not absorbed).

## Finding 2 (high): the tripwire must never be the evidence for "no host harm" or "the pause held"

**Counterexample.** Suppose L1 scans the round-17 seat transcripts, gets `MADO_TRIPWIRE: clean`, and writes "no host mutation in round 17". The 09:15 `-Syu` shows why that sentence is wrong: it is a real host mutation that a lane-transcript scan cannot see, because its session is not in the scan set. Within the scanned files, the tripwire is still blind to several routes, all by contract:

- eval Python that does not start with `!` (`subprocess.run(['sudo','pacman',…])`);
- `python3 -c "os.system('sudo …')"`, because `python3` is not a recursion target;
- `bash /tmp/x.sh`, whose script body is not read;
- tools other than bash/eval;
- sessions that were never indexed.

The host-side record is `pacman.log`, plus systemd/journal records that the round may not probe. A transcript tripwire is lane-side self-report about issued commands.

**Required phrasing.** Every use of a `clean` result gets this bound:

> `clean` = no unpermitted listed pattern among parsed bash/`!`-eval toolCalls in the files named by sha256 in the verdict; not a statement about host state, not proof of absence.

Host-window statements cite `pacman.log` counts, never the tripwire. `QualityDraft.md` and `SkillRegistryDraft.md` l.21 already carry most of this bound. The report and SCORECARD must repeat it inline, not just link to it.

## Finding 3 (high): a `--permit` run can print `clean` over the R15 harm

**Counterexample.** By the shared contract, `--scan <R15 transcripts> --permit host_mutation` exits 0 ("no unpermitted finding"). The first-line label set is `clean|findings|could_not_evaluate`, and nothing distinguishes "clean" from "clean only because permitted". So this command would print `MADO_TRIPWIRE: clean` over call_38165 `sudo pacman -S … libinput`. This is the R16-V1 defect class again: a receipt labeled with a verdict token the evidence does not support.

**Smallest correction** (pick one; L1 owns the contract):

- (a) TripwireCore emits `clean` only when `findings` is empty, and uses `findings` with exit 0 when every finding is permitted.
- (b) Keep the contract, but require every cited verdict to quote `permitted` and `counts`, and forbid citing a permitted run's first line as "clean".

`SkillRegistryDraft.md` l.16 maps exit 0 to the label "clean"; it should read "0 no unpermitted finding (see `permitted`)". No `--permit` run belongs in the C3 evidence.

## Finding 4 (medium): C3 is a demonstrated capability, not an operability or safety improvement

Recalling the one already-known positive (line 54, call_38165) proves the tool reproduces an answer chosen in advance. That is near-zero evidence about recall on unseen breaches. The oracle is "independent" in code, but it shares the same declared class table, so the two share failure modes: a wrapper missing from the table is missed by both.

**Permissible verdict line:**

> operability: capability acquired (post-hoc transcript detection; selftest k/n exit 0 at <rev>, sha256 <…>; R15 anchor classified host_mutation/sudo + pacman:-S, matching a separately implemented oracle over the same class table). Host-safety: R15-V1 harm carried, operator-owned, not remediated, not prevented from recurring; the tripwire runs after the fact and could not have stopped call_38165.

The round-16 closure used "improved (capability only) … not host recovery and not install prevention" (spot-check l.84–85). Keep exactly that shape. Never write a bare "operability: improved".

## Finding 5 (medium): admission-language blacklist and allowed replacements

| Overreaching wording (do not use) | Why | Use instead |
|---|---|---|
| "admitted", "round admitted", "C3 admitted" (author text) | Admission belongs to the non-author closure (SCORECARD l.816–817 precedent) | "Admission not asserted; independent closure and operator disposition required" |
| "R15-V1 mitigated / addressed / guarded / closed / resolved" | The tripwire changes no host state, and the host was changed by others (Finding 1) | "R15-V1 carried, operator-owned, current host condition `[UNK]`" |
| "prevents recurrence", "safety net", "guardrail", "enforces the pause" | Post-hoc reading only; no interception | "detects after the fact, in scanned transcripts only" |
| "no host harm this round", "pause held", "host clean" | Not tripwire-provable; host log shows non-lane transactions | "`pacman.log`: `<n>` transactions in `[10:51:22, close]`" plus the Finding-1 disclosure |
| "verified" for C3 by the author | Author self-run; round 16 closure called it "evidence-verified, not executed" | "author-run, receipts at <rev>; non-author verification pending" |
| "readmits round 15" or "unblocks progression" | Round 15 stays rejected-harmed; only the operator authorizes remediation (SCORECARD l.684) | "This round does not readmit round 15." (repeat verbatim) |
| "the seat issued no host command" based on a tripwire run | Self-attestation by an author tool, with blind spots | "tripwire `clean` over files <sha256…> (bound as Finding 2)" |
| "P4/P6 covered" meaning observed | Documentary routes; `xdg-terminals.list` naming Alacritty is a declared rule, not a launch | "documentary route covered under rubric V; behaviour `[UNK]`" (FrontierDraft l.8–9 already does this) |

## Finding 6 (low–medium): calibration integrity of C1

- **QualityDraft adds criterion 24**, which is lesson-cited, on top of the C1 criterion (23). The pre-registration declares one criterion (≥15/23). With both, the count reads 16/24. Adding a second lesson-cited row lifts the literal fraction and edges toward farming the rubric. The report must name which row is C1's and state the count both with and without row 24.
- Criterion 24 also makes a tripwire run the precondition for "admission claims about a seat's conduct". That turns an author tool into admission evidence. Reword it as "before *asserting* a seat's command conduct…" and keep admission with closure.
- The R16-V1 correction must be appended in round-17 M1. Do not edit round-16 lesson l.131 or the closure file in place. The label check has to be shown **red** on that baseline line, `frozen_error` ≠ `snapshot_tampered`, with that receipt retained.
- The pre-registration (SCORECARD l.855) says "`bash` tool calls". The contract and drafts also parse `!`-eval. State the actual scope in the results so the claim matches the tool.
- `N/N` in C3 is unbound in the pre-registration. Record N from the committed `expected.json` at integration, together with its sha256, so N is not chosen after seeing results.

## Impacted axes

- operability: host-safety row (Findings 1–4).
- calibration: label integrity (Findings 3 and 6).
- adjacency: host recovery and other lanes' transactions are routed, not adjudicated or absorbed.
- coverage: wording only (Finding 5, P4/P6 row).

## Fixable versus tradeoff

Findings 1, 3, 5 and 6 are fixable wording or contract defects. The judge should reject only if they ship uncorrected:

- a "pause held" or "R15-V1 resolved" claim;
- a permitted run reported as clean;
- a bare "operability improved".

Finding 4's blindness to unseen breaches is an inherent tradeoff of a post-hoc, single-anchor capability. Disclose it; it does not need fixing.
