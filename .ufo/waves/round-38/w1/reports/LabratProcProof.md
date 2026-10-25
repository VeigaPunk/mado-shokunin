# LabratProcProof — the /proc binding is committed text, re-derived by nobody

Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (LANE). Leaf member, no subagents dispatched.
Scope: `quality/counters/c2-r38-eventq.py` (`PRED-C2-r38-v3`) live clause, third artifact
`.ufo/waves/round-38/receipts/eventq-live-proc.txt`, and the manifest control `c2-proc-mismatch`.

**Verdict: the hypothesis is CONFIRMED, and worse than stated.** The counter does **not** re-derive
`/proc` at counter-run time; it trusts the committed text. A forged proc artifact — including one
whose "holders" line names a *non-compositor* process, one whose inode numbers appear only in prose,
and one that never mentions `/proc` at all — reaches `TARGET_MET`. The minimum sufficient forgery is
**112 bytes** (or **2 lines**) and is derivable **entirely from the committed repo**, with no
`/proc` access of any kind.

Bounds compliance: read-only on LANE production files; the only LANE write is this report. All
mutations ran in a `git clone -q --no-local` sandbox at `/tmp/mado38-LabratProcProof/sb`
(`git rev-parse --show-toplevel` verified == the sandbox path before every mutation). No
`git add/commit/stash/checkout/reset/push` in LANE; no `hyprctl`, no socket connection, no
`/proc` write. Tool installs: **none needed** (record: none).

---

## 1. The probe (`/tmp/mado38-LabratProcProof/probe.py`)

Minimal script; reads only the committed artifact's bytes; opens no `/proc`, spawns no subprocess.

```
$ python3 -I /tmp/mado38-LabratProcProof/probe.py \
    /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-38/receipts/eventq-live-proc.txt
verdict_field=AGREE
agree_line=OVERALL: AGREE
```

The verdict field is a **string in a file**. It is produced identically with or without a kernel.

## 2. Does the live clause re-derive `/proc`? No — it trusts the committed text

`quality/counters/c2-r38-eventq.py`, `live_check()`:

| Line | Code | What it does |
|---|---|---|
| **194** | `proc = git(repo, "show", f"{rev}:{LIVE_PROC}")` | The proc artifact is read **out of git**, from the committed blob. Never from the running kernel. |
| **232** | `ptext = proc.decode("utf-8", "replace")` | The artifact becomes a string to be grepped. |
| **233** | `snap_sha = hashlib.sha256(snap).hexdigest()` | Digest of the **committed snapshot** — again a committed byte. |
| **235–240** | `srv` derivation over `snap_text` | The socket2 server inodes are taken from the **committed `ss` snapshot**. |
| **241** | `named = sum(1 for i in srv if re.search(rf"\b{i}\b", ptext))` | "Named" == the integer **appears somewhere in the proc text**. No row, no path, no holder, no pid is required. |
| **242–244** | `proc_ok = (f"ss_sha256={snap_sha}" in ptext and srv and named == len(srv) and re.search(r"OVERALL:\s*AGREE", ptext) is not None)` | The whole proc clause: a digest substring, N integer substrings, and an `AGREE` substring. |
| **248** | `live = int(sha_ok and replay_ok and full_table and proc_ok)` | `live=1` iff those four booleans hold. |

**Three facts are required of the proc artifact: the snapshot's digest, the snapshot's server inode
numbers, and the literal `OVERALL: AGREE`.** The counter never parses `holders:`, never parses a
pid, never checks that an inode is *held*, never checks that a `/proc/net/unix` row exists, and
never compares a `/proc` path to the socket path. `grep -n 'holders\|pid' quality/counters/c2-r38-eventq.py`
returns only fixture-table constants and the client-triple regex — no proc-artifact parsing at all.

### Empirical proof: no `/proc` access at counter-run time

```
$ strace -f -qq -e trace=openat,open,execve -o strace.out \
    python3 -I quality/counters/c2-r38-eventq.py --repo . --rev HEAD
counter rc=0
openat/open lines mentioning /proc/: 32
   16 "/proc/sys/vm/overcommit_memory"     <- CPython runtime
   16 "/proc/self/maps"                    <- CPython runtime
execve of ss/hyprctl/journalctl/cat/ls: 0
references to net/unix: 0
```

The only `/proc` paths touched are CPython's own two runtime probes (one per `python3 -I`
subprocess the counter spawns). `net/unix` is referenced **zero** times; `ss`, `hyprctl` and
`journalctl` are never exec'd by the counter (the tool is replayed with `--ss-file`, so its own
live verbs are never reached either).

### No committed generator, no independent validator

`grep -rln 'net/unix' tools/ quality/` → only `quality/counters/c2-r38-eventq.py` (which mentions
`/proc/net/unix` in a docstring at line 31 and a comment at line 231, and in neither reads it).
`grep -rln 'eventq-live-proc'` over `*.py|*.sh|*.json|*.md` → the counter, the manifest, the
wave-1 spec/dispatch, the scorecard, and the round-37 lessons. **Nothing else in the repo
independently validates the proc artifact.** The `c2-proc-mismatch` control is the only check
that ever looks at it, and §4 shows what it actually discriminates.

## 3. Quantification — forged triplets pass

Sandbox: `git clone -q --no-local <LANE> /tmp/mado38-LabratProcProof/sb`; each row = write files,
commit with `sandbox` identity, run `python3 -I quality/counters/c2-r38-eventq.py --repo . --rev HEAD`.

```
EXPERIMENT                        RESULT
----------------------------------------------------------------------------------------------------------------------------------
0. baseline (committed triplet untouched)                  rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
1. 112-byte forged proc: digest + 3 numbers + AGREE        rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
2. 2-line forged proc (all tokens on one line)             rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
3. forged proc asserts AGREE then DISAGREE                 rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
4. forged proc ends with DISAGREE (docstring says 'ends AGREE') rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
5. 'OVERALL: AGREE' only as a substring of a longer token  rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
6. inodes appear only in prose, no /proc rows at all       rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
7. forged proc claims inodes held by bash, NOT the compositor rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
8. INVENTED inodes + rewritten snapshot (receipt untouched) rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
9. manifest c2-proc-mismatch artifact (wrong digest+inode) rc=1 TARGET_MISSED  replay=1 sha=1 full_table=1 proc=0/3 sha_in=0 agree=1
10. correct digest + real inodes + EXTRA fabricated inode 99999999 rc=0 TARGET_MET     replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
----------------------------------------------------------------------------------------------------------------------------------
control: proc artifact absent ->
11. proc artifact absent (artifacts-missing)               rc=1 TARGET_MISSED  artifacts-missing
```

Row 7 is the hypothesis verbatim: the artifact asserts the socket2 inodes are held by `bash/4242`,
not by Hyprland, and the counter accepts it (`proc=3/3`). Row 8 is the strongest form: **invented
inodes** `900000001/2/3` in both the snapshot and the proc artifact, with the *receipt untouched* —
`TARGET_MET`.

### The forgery kit needs only the committed repo

`/tmp/mado38-LabratProcProof/forge_kit.py` reads `eventq-live-ss.txt` (public in the same repo) and
derives every token the clause demands:

```
$ python3 -I /tmp/mado38-LabratProcProof/forge_kit.py
derived from committed repo only: digest=653311be6bb86efbe… inodes=['10029', '181151236', '38117']
forged proc artifact (112 bytes):
---
ss_sha256=653311be6bb86efbe1d4448a102c4fb64666c1c6c9b63346d7a3e930ed147d3b
10029
181151236
38117
OVERALL: AGREE
---
counter verdict=TARGET_MET rc=0 detail=replay=1 sha=1 full_table=1 proc=3/3 sha_in=1 agree=1
```

**Cost: 112 bytes, 5 lines, zero host access, zero knowledge beyond the public snapshot.**
Committed artifact: 1079 bytes / 17 lines. The forgery is **~10 % of the size** of the honest one.

### Line-level ablation of the committed proc artifact

Deleting each of the 17 committed lines and re-scoring: **15 of 17 lines are deletable and the
counter still returns `TARGET_MET`.** Only two lines are load-bearing:

```
del line  3 -> TARGET_MISSED  'ss_sha256=653311be6bb86efbe1d4448a102c4fb64666c1c6c9b63346d7a3e930ed147d3b'
del line 17 -> TARGET_MISSED  'OVERALL: AGREE'
```

Every other line — the `/proc/net/unix` rows, the `holders:` lines, the `server … inode=` lines,
the `compositor pids holding socket2 inodes: ['1619']` line, the "every socket2 server inode
present in /proc/net/unix and held only by the compositor" line — is **decoration**. Deleting the
`holders:` lines does not change the verdict; the counter never read them.

## 4. What `c2-proc-mismatch` actually discriminates (the manifest's reject control)

The manifest control (`manifest.json`, id `c2-proc-mismatch`, note *"the triplet lies about the
proc binding: fabricated inodes named as held"*) writes:

```
# forged proc binding
ss_sha256=0000000000000000000000000000000000000000000000000000000000000000
server ESTAB inode=99999999 held by Hyprland/1619
OVERALL: AGREE
```

It rejects — but only because **both** its tokens are wrong relative to the *committed snapshot*:
`sha_in=0` (digest ≠ snapshot digest) and `proc=0/3` (inode 99999999 is not a snapshot server
inode). Isolating the two:

```
[manifest c2-proc-mismatch verbatim]
     verdict=TARGET_MISSED detail=... proc=0/3 sha_in=0 agree=1
[same artifact, CORRECT digest (fabricated inode 99999999 only)]
     verdict=TARGET_MISSED detail=... proc=0/3 sha_in=1 agree=1
[correct digest + 3 real inodes + extra fabricated inode 99999999, all claimed Hyprland-held]
     verdict=TARGET_MET  detail=... proc=3/3 sha_in=1 agree=1
```

So `c2-proc-mismatch` rejects **a mismatch between the proc artifact and the snapshot**, not a
forgery of the *binding*. The moment the forger supplies the snapshot's real digest and its real
inode numbers — both derivable from the public committed snapshot — the same class of artifact
(including the fabricated inode `99999999` still labelled "held by Hyprland") is **accepted**
(row 10). The control proves the two artifacts are *mutually consistent*, which is exactly the
property a consistent forgery also satisfies.

## 5. Honesty of the committed artifact (the residue that *is* real)

Cross-checking the committed claims against the live host, read-only (no socket, no write):

```
live /proc/net/unix: committed inodes present = ['10029', '181151236', '38117']
live holder sets (pid/fd counts):
  inode 10029: holder_count=2 distinct_pids=1
  inode 181151236: holder_count=2 distinct_pids=1
  inode 38117: holder_count=2 distinct_pids=1
```

The committed artifact is **truthful today**: its three inodes exist in `/proc/net/unix`, and each
is held by exactly one distinct pid. The finding is not that the artifact lies — it is that
**nothing in the instrument can tell a truthful artifact from a lying one**.

## 6. Gap between the counter's own docstring and its code

The docstring (`c2-r38-eventq.py:30-35`) promises the proc artifact:

> "names every socket2 LISTEN/ESTAB server inode from the snapshot as `/proc` rows **held only by
> the compositor pid(s) the receipt names**, and **ends** `OVERALL: AGREE`."

Neither clause is enforced.

- *"as `/proc` rows"* — row 6: the inodes need only appear in prose, with no `/proc` row at all.
- *"held only by the compositor pid(s)"* — row 7: an artifact naming `bash/4242` is accepted; the
  `holders:` line is never parsed.
- *"ends `OVERALL: AGREE`"* — rows 4 and 5: `re.search` (not `re.search` anchored to the end, and
  not `\b`-delimited) means `OVERALL: DISAGREE` as the last line still passes, and so does
  `NOT_OVERALL: AGREED_THIS_IS_A_LIE`.

The docstring's own Residual paragraph (lines 37-42) declares:

> "a fully fabricated consistent triplet — invented inodes repeated identically across ss and proc
> artifacts — still reaches the live clause … it does not make live truth provable from committed bytes."

**My result confirms and sharpens that residual.** The declared residual is *consistent*
fabrication (invented inodes repeated identically). The measured reality is weaker than the
declaration: the three artifacts need not be mutually consistent with each other beyond the
snapshot↔proc digest+inode pair, and — decisively — **the honest `ss` snapshot and the honest
`eventq-live.txt` receipt can both be left untouched**. Only the 112-byte proc artifact is
rewritten. The crib is "forge one artifact against a public snapshot", not "forge three mutually
consistent artifacts" as line 40-41 claims.

## 7. Findings

| # | Finding | Severity | Evidence |
|---|---|---|---|
| **F1** | The live clause **trusts committed text**; it re-derives `/proc` at **no** point. `live_check` reads the proc artifact with `git show` (line 194) and greps it. | **HIGH** (claim-invalidating for C2) | `c2-r38-eventq.py:194,232-244`; strace: `net/unix` referenced 0 times, `ss`/`hyprctl`/`journalctl` never exec'd. |
| **F2** | The proc clause checks only **digest ⊂ text**, **inode integers ⊂ text**, **literal `AGREE` ⊂ text**. It never checks a `/proc` row, a socket path, a holder, or a pid. | HIGH | Line 241: `re.search(rf"\b{i}\b", ptext)`. Rows 6, 7. |
| **F3** | **112 bytes / 5 lines** suffice; derivable entirely from the committed repo; the honest snapshot and receipt need not be touched. | HIGH | `forge_kit.py` output above; rows 1, 8. |
| **F4** | The docstring's three promised properties (*as `/proc` rows*, *held only by the compositor*, *ends `OVERALL: AGREE`*) are **all unenforced**. | MEDIUM | Lines 30-35 vs 241-244; rows 4, 5, 6, 7. |
| **F5** | The manifest reject control `c2-proc-mismatch` discriminates **snapshot↔proc consistency**, not **forgery**. With the correct digest + the snapshot's real inodes, the same artifact class (fabricated inode "held by Hyprland") is accepted. | MEDIUM | §4 isolation runs; row 10. |
| **F6** | The committed proc artifact is **truthful today** (3/3 inodes live, each held by 1 pid). The defect is instrument reachability, not a false claim in the landed data. | INFO | §5 live cross-check. |

## 8. What would close it (for the L1; not implemented — READ-ONLY seat)

Any one of these converts the proc clause from a self-receipt into a binding:

1. **Re-derive at count time**: have the counter (or the tool) read `/proc/net/unix` + `/proc/<pid>/fd`
   live and compare against the committed snapshot's inodes and holders. This is what
   `corpus/lessons/round-37.md:95` says the round *intended* ("cross-checks a live snapshot against
   `/proc/net/unix` server inodes") but the implementation only checks that a committed file
   *mentions* those inodes.
2. **Anchor the digest to a host-truthful root**: bind the proc artifact to a re-fetched
   `fetch/` receipt digest (the mechanism C1 already uses) so it cannot be hand-written alongside
   the snapshot.
3. **Raise the grammar floor** on the proc artifact: require an `/proc/net/unix:` row per inode,
   the socket path to equal the snapshot's socket2 path, a `holders:` line naming exactly the
   compositor pid, `OVERALL: AGREE` as the **last** line, and `\b`-anchored `OVERALL:` — turning
   rows 4-7 into rejects. This alone raises the crib from 112 bytes to a multi-artifact forgery,
   but still does not make live truth provable from committed bytes.

Note the honest limit of (3): a *fully consistent* forgery (invented inodes repeated across
snapshot and proc, with a matching receipt) still passes. Only (1) or (2) closes that.

## 9. Exact commands run (all mutations in the sandbox)

```
git clone -q --no-local /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado38-LabratProcProof/sb
git -C /tmp/mado38-LabratProcProof/sb rev-parse --show-toplevel     # == the sandbox path
python3 -I quality/counters/c2-r38-eventq.py --repo . --rev HEAD     # in the sandbox
strace -f -qq -e trace=openat,open,execve -o strace.out \
    python3 -I quality/counters/c2-r38-eventq.py --repo . --rev HEAD
python3 -I /tmp/mado38-LabratProcProof/probe.py <committed proc artifact>
python3 -I /tmp/mado38-LabratProcProof/forge.py
python3 -I /tmp/mado38-LabratProcProof/strace_probe.py
python3 -I /tmp/mado38-LabratProcProof/forge_kit.py
python3 -I /tmp/mado38-LabratProcProof/summary.py
```

Artefacts: `/tmp/mado38-LabratProcProof/{probe.py,forge.py,strace_probe.py,forge_kit.py,summary.py,strace.out}`.

## 10. Cross-reference — overlap with the sibling `CritV3Residual` seat

`CritV3Residual.md` (landed in `master` as `166c795`, 11:32, after my runs) reaches the **same core
conclusion**: *"Nothing binds any of it to the live host: the forger invents the inodes in the
snapshot they themselves wrote, so consistency is free"*, and quotes the same deciding lines
(`:241-243` proc check, `:248` conjunction). **Not a duplicate.** The deltas from my seat, which
that report does not contain:

1. **The honest two artifacts need not be forged at all.** CritV3Residual's cheapest C2 shapes
   forge the tool + receipt + snapshot + proc together (1,505–14,190 B). My rows 1/3 and the
   `forge_kit.py` output keep the **committed `eventq-live.txt` receipt and the committed
   `eventq-live-ss.txt` snapshot byte-identical** and rewrite **only** the proc artifact —
   **112 B / 5 lines**, vs their 220 B floor (and their 220 B still needed a forged snapshot).
2. **The `holders:` claim is not merely unchecked — it can be affirmatively false.** Row 7: an
   artifact asserting `holders: bash/4242/fd7` for the three real socket2 inodes passes
   (`proc=3/3`). CritV3Residual proposes "proc-holder consistency" as a *narrowing clause*; I
   measure that the clause is **absent**, so the current counter accepts a false holder claim.
3. **The docstring's three promised properties are all unenforced** (F4): `as /proc rows` (row 6,
   prose-only passes), `held only by the compositor` (row 7), `ends OVERALL: AGREE` (rows 4-5 —
   `re.search` is neither end-anchored nor `\b`-delimited, so a trailing `OVERALL: DISAGREE` and a
   `NOT_OVERALL: AGREED_THIS_IS_A_LIE` both pass).
4. **The manifest's reject control `c2-proc-mismatch` does not discriminate forgery** (§4, row 10):
   it rejects a snapshot↔proc *mismatch*; supply the snapshot's real digest + real inode numbers
   and the same artifact class — including a fabricated inode still labelled "held by Hyprland" —
   is accepted. CritV3Residual classifies the C2 residual as "accepted tradeoff (declared, not a
   defect)"; my measurement shows the **declared residual is wider than the docstring's own
   declaration** (docstring lines 40-41 say "forge three mutually consistent artifacts"; the
   measured crib is "forge one artifact against a public snapshot").
5. **Line-level ablation**: 15 of the 17 committed proc-artifact lines are deletable with the
   verdict unchanged — including all three `holders:` lines and all three `/proc/net/unix` rows.

Together: F1/F3 (no live re-derivation; 112 B single-artifact crib) and F4/F5 (unenforced docstring
properties; the reject control tests consistency, not forgery) sharpen the C2 residual from
"declared, accepted tradeoff" to "the declared residual is materially understated".

## 11. Unresolved / not covered

- I did **not** test whether C1's `c1-r38-event-ground.py` has an analogous committed-text hole;
  it has no `/proc` clause (`grep 'proc\|OVERALL\|ss_sha256'` → only `import re/subprocess` hits),
  and my brief was C2's proc binding.
- The manifest's `c2-proc-mismatch` control currently rejects, so the **frozen 19/19 discrimination
  result is not disturbed by this finding** — the control is doing exactly what it was written to
  do (detect a snapshot↔proc mismatch). This is a *residual-strength* finding, not a
  discrimination failure. (Separately, `master` HEAD `3f14bd2` carries an errata commit reporting
  the frozen claim at 18/19 — that is RevCommitChain's finding, not mine.)
- I did not attempt to re-derive the *snapshot*'s honesty against a fresh `ss -xpa`; the sibling
  seat `RevLiveTriplet` did that (PASS on all three receipts) and I did not duplicate it.
- The 14-fixture and 14-case counts, the readonly clause, and the tool-presence clause were out of
  scope and untouched by my mutations (every run printed `fixtures=14/14 readonly=1 tool=present`).
