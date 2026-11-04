# R85ScoutSources — independent read of the two round-85 sources

## 0. Scope, discipline, and what this seat did

- **Role:** UFO-FSD scout (read-only reconnaissance of the two round-85 sources, independent of the pin seat). Leaf member: no subagent dispatch.
- **Lane root:** `/home/vgpnk/Projects/shokunin/mado-shokunin`
- **Freeze revision:** `3905311c75a39c5710413105865c0a1a7dd0116a`; base `5f174ca48d4f9cf94abf1a8c58b7d6f88733aced`
- **Declaration read first:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/claims-declaration-r85.md`
- **Writes:** this report file only. No production edits, no registry edits, no counter/control/declaration edits, no git mutation, no tool install. All scratch under `/fast/scratch/hyaku/mado-r85/R85ScoutSources/`, removed on exit.
- **Tooling:** no tool installed or upgraded this round (the GNU endpoint gaps were routed around by fetching upstream release tarballs; no `pacman` transaction).

This seat answers the four questions asked of the two named sources, and proposes one candidate source for the C1 cause vocabulary.

---

## 1. What I opened, and how

### 1.1 POSIX.1-2024 XCU §2.9.3 — the declaration's locator is off by one section

The declaration (and the seat brief) cite "POSIX.1-2024 XCU §2.9.3 *Pipelines*". I opened the named URL myself and confirmed the anchor is wrong:

> `#### 2.9.2 Pipelines` … `#### 2.9.3 Lists`

- `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html` (Issue 8, IEEE Std 1003.1-2024)
- Independent byte-level fetch: `curl` → 357,953 B, sha256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`.
- **This is byte-identical to the lane's own pin** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-85/fetch/S488.bin` (same sha256, same 357,953 B). The pin is sound; only the declaration's *section number* is wrong.
- Byte offsets inside the pinned bytes: `2.9.2 Pipelines` @ 33656; `2.9.3 Lists` @ 110936; `The exit status of a pipeline shall depend` @ 131749; `shall wait for the last command specified in the pipeline to complete` @ 131538; `at the time it begins execution of the pipeline` @ 132250; `the last (rightmost) command specified in the pipeline` @ 133049; `Zero, if all commands in the pipeline returned an exit status of 0` @ 133532; `greater than 128` @ 109111; `shall identify, in an implementation-defined manner` @ 109145; `greater than 255 if a command terminates` @ 109306.

**Consequence for the registry:** the row already in `corpus/SOURCES.md:440` (S488) anchors `Issue8 section2.9.2 Pipelines, Exit Status table` — **correct**, and it already departs from the declaration's §2.9.3. The lesson file `corpus/lessons/round-85.md:28` records this as M85-8 (reference drift). Both are right; the declaration prose is the stale artifact.

### 1.2 GNU Bash Reference Manual §3.7.6 — the declaration's locator is off by one *section number* here too

The declaration (and the seat brief) cite "§3.7.6 *Exit Status*". In every Bash manual edition I checked, **Exit Status is §3.7.5 and §3.7.6 is Signals**:

| edition | Exit Status | Signals | source |
|---|---|---|---|
| bash 2.05a (2006) | 3.7.5 | 3.7.6 | `ftp.gnu.org/old-gnu/Manuals/bash-2.05a/html_chapter/bashref_3.html` TOC + body |
| bash 5.2 (2022) | 3.7.5 | 3.7.6 | `bash-5.2/doc/bashref.info` node headers; `bash-5.2/doc/bashref.texi` |
| bash 5.3 (2025-05-18) | 3.7.5 | 3.7.6 | `bash-5.3/doc/bashref.info` node headers; `bash-5.3/doc/bashref.texi` |

The GNU HTML endpoint (`www.gnu.org/software/bash/manual/html_node/Exit-Status.html`) **timed out on every attempt from this host** — 4 reader fetches plus one 60 s `curl` (rc 28). That matches the pin seat's recorded outcome (`corpus/lessons/round-85.md:28`: "the GNU URL named by the declaration was unreachable in 5 attempts (curl rc 28) and is **not** pinned"). **I did not observe a GNU-endpoint quote; I never saw that page.** What I did instead:

**Route around (upstream release tarballs over FTP, which answered).** `ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` and `bash-5.2.tar.gz` both downloaded cleanly and carry the manual's own source, `doc/bashref.texi` / `doc/bashref.info` — the upstream origin of the HTML the GNU endpoint renders:

| artifact | sha256 | bytes |
|---|---|---|
| `bash-5.3.tar.gz` | `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba` | 11,355,854 |
| `bash-5.3/doc/bashref.texi` | `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` | 415,804 |
| `bash-5.3/doc/bashref.info` | `4edb431cb97126281be3f8e5038a5e3377177f97ab1ca3f6ad9809bd555e8654` | — |
| `bash-5.2.tar.gz` | `a139c166df7ff4471c5e0733051642ee5556c1cc8a4a78f145583c5c81ab32fb` | 10,950,833 |
| `bash-5.2/doc/bashref.texi` | `32ced60bb645d47be7bfa4e5767edb2ea1b0c840d8968c17f3eb9df960b44863` | — |
| `bash-5.2/doc/bashref.info` | `eb92b3a76d0ebe72cea246fb4cad7a25e05f33a0f4162fe5936530f1cabc2166` | — |

`bash-5.3/doc/version.texi` reads `@set VERSION 5.3` / `@set UPDATED 18 May 2025` — the same "Edition 5.3, 2025-05-18" the pin seat's maintainer-copy row records. The upstream tarball text and the maintainer copy agree word-for-word on every quote used below.

The registry row `corpus/SOURCES.md:441` (S489) anchors "Edition5.3 section3.7.5 Exit Status" — **correct**, and the lesson M85-8 already records the §3.7.6→§3.7.5 drift. The declaration prose is again the stale artifact.

### 1.3 The lane's own pin set (read only)

- `.ufo/waves/round-85/fetch/S488.bin` — sha256 `0889867a…1acd`, 357,953 B (POSIX Issue 8 ch. 2)
- `.ufo/waves/round-85/fetch/S489-alt-tiswww.bin` — sha256 `b91026ac…77a4`, 1,040,870 B (Chet maintainer copy of the Bash manual)
- `.ufo/waves/round-85/fetch/source-pins-r85.json` — the pin manifest

I did not modify any of these. My own POSIX fetch reproduced `S488.bin` byte-for-byte, which independently confirms the pin.

---

## 2. Question 1 — is a pipeline's exit status the last command's?

**Answer: yes by default, but the sources qualify it, and the qualification is exactly what C2 turns on.**

Located quotes (each ≤ 25 words):

- POSIX Issue 8 §2.9.2, Exit Status table, `pipefail` disabled / no `!`: "The exit status of the last (rightmost) command specified in the pipeline." (13 words) — pinned `S488.bin` @ 133049.
- POSIX Issue 8 §2.9.2, `pipefail` enabled / no `!`: "Zero, if all commands in the pipeline returned an exit status of 0; otherwise, the exit status of the last (rightmost) command specified in the pipeline that returned a non-zero exit status." (32 words → trimmed to) "the exit status of the last (rightmost) command specified in the pipeline that returned a non-zero exit status" (19 words) — pinned `S488.bin` @ 133532.
- Bash §3.2.3 Pipelines: "The exit status of a pipeline is the exit status of the last command in the pipeline, unless the `pipefail` option is enabled" (23 words) — `bash-5.3/doc/bashref.texi` @node Pipelines.

So: **unqualified, the pipeline's status is the last command's**; **with `pipefail`, it is the last *failing* command's**, which is the whole point of the guard. Both sources agree. Neither source makes the *producer's* status the pipeline's status — they make the *rightmost nonzero* the pipeline's status.

**Historical note (relevant to how the declaration's own gloss reads):** POSIX Issue 7 (IEEE Std 1003.1-2017) had **no `pipefail` at all** — I grepped the full Issue 7 chapter-2 HTML (`9699919799/utilities/V3_chap02.html`, 259,910 B) and `pipefail` occurs **0** times; its §2.9.2 reads only "the exit status shall be the exit status of the last command specified in the pipeline". The `pipefail` row in the Issue 8 Exit Status table is new in the 2024 edition. So the S488 row's scope note ("Issue8 also specifies pipefail") is materially informative, not pedantic.

---

## 3. Question 2 — does a fatal signal N give 128+N?

**Answer: Bash says yes and gives the arithmetic; POSIX does not say 128+N at all.**

Located quotes:

- **Bash §3.7.5 Exit Status:** "When a command terminates on a fatal signal whose number is N, Bash uses the value 128+N as the exit status." (21 words) — `bash-5.3/doc/bashref.texi` line 3912, byte-identical in `bash-5.2/doc/bashref.texi`; `bashref.info` node header reads "3.7.5 Exit Status".
- **Bash §3.2.1 Simple Commands** carries the same arithmetic a second time: "or 128+n if the command was terminated by signal n" — `bash-5.3/doc/bashref.texi` line 766.
- **POSIX Issue 8 §2.8.2 Exit Status for Commands** says only: "Otherwise, if the command terminated due to the receipt of a signal, the shell shall assign it an exit status greater than 128." (24 words) — pinned `S488.bin` @ 109111.
- **POSIX Issue 8 §2.8.2** adds that the signal is identified only "in an implementation-defined manner" — pinned `S488.bin` @ 109145 — and permits "greater than 255 if a command terminates" — @ 109306.

So the arithmetic is **Bash's**, not POSIX's. POSIX mandates only *greater than 128* and leaves the mapping *implementation-defined*, explicitly allowing values above 255. The registry row S489 says exactly this ("not a POSIX-wide encoding guarantee") and is right to.

**This is the load-bearing limit for C2's `signal` class.** C2 binds `signal` to `rc == 128 + N`. That is sound *as a Bash-encoding check*, and the counter's own docstring already says so — `quality/counters/c2-r85-status-classes.py:17`: "statuses0,7,141. The last is an expected Bash encoding, not independent proof of signal cause", and `:346-347`: "`signal` expects the Bash encoding128+N. This status cannot distinguish a signalled child from explicit exit128+N."

**Host fact, measured here** (read-only, in-lane): this host's `/bin/sh` is a symlink to `bash` (GNU bash 5.3.20(1)-release, x86_64-pc-linux-gnu), `set -o pipefail` is accepted, and the round-85 fixtures reproduce the declared classes:

| fixture | guarded (`set -o pipefail`) | unguarded |
|---|---|---|
| `.ufo/waves/round-85/fixtures/status-ok.sh` | rc 0 | rc 0 |
| `.ufo/waves/round-85/fixtures/status-exit7.sh` | rc 7 | rc 0 |
| `.ufo/waves/round-85/fixtures/status-sigpipe.sh` \| `head -n 1` | rc 141 (= 128+13), stdout `MADO_STATUS: sigpipe line 0` | rc 0 |

This confirms the C2 no-work control's premise on this host: without the guard the exit7 and sigpipe producers both report 0. It also confirms the `signal` encoding is *this host's shell's* encoding, not a portable one.

---

## 4. Question 3 — does either source promise `pipefail` semantics?

**Answer: yes, both — and the POSIX promise is stronger and newer than the declaration's gloss implies.**

- **POSIX Issue 8 §2.9.2** has a four-row Exit Status table keyed on `pipefail` enabled/disabled × begins-with-`!`/not, and the table's own lead-in says: "The exit status of a pipeline shall depend on whether or not the `pipefail` option is enabled and whether or not the pipeline begins with the `!` reserved word" (27 words → trimmed to) "The exit status of a pipeline shall depend on whether or not the `pipefail` option" (14 words) — pinned `S488.bin` @ 131749.
- **POSIX Issue 8 `set` builtin** carries the option itself, with no `[OB]`/`[UP]` marker on it (I enumerated the option-marker sequence around it: `_nolog_ [OB] Option Start Option End _notify_ _nounset_ _pipefail_ _verbose_ _vi_` — `pipefail` sits bare between `_nounset_` and `_verbose_`): "Derive the exit status of a pipeline from the exit statuses of all of the commands in the pipeline, not just the last (rightmost) command" (25 words). So POSIX.1-2024 makes `pipefail` a **required** `set` option, not an optional one.
- **Bash §3.2.3 Pipelines** states the same rule: "If `pipefail` is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status" (23 words) — `bash-5.3/doc/bashref.texi` @node Pipelines.

**Two things the sources promise that the declaration's phrasing does not carry:**

1. **The `!` reserved word changes the meaning.** POSIX Issue 8 §2.9.2's table has two `!` rows, and the lead-in says the `!` reserved word "causes the exit status to be the logical NOT of the exit status of that command". So "a pipeline's status is the last command's" is true only for the *un-negated* pipeline. A runbook row that pipes through `!` would invert the class.
2. **The `pipefail` setting is read at pipeline *start*.** POSIX Issue 8 §2.9.2: "The shell shall use the `pipefail` setting at the time it begins execution of the pipeline, not the setting at the time it sets the exit status of the pipeline" — pinned `S488.bin` @ 132250. So `cmd | set -o pipefail` does not retroactively arm the guard; only a `set -o pipefail;` *before* the pipeline does. The lane's runbook rows use exactly that prefix form, so they are on the right side of this rule; but the rule is the reason the prefix form is the only correct one.

**Nothing about producer payload truth.** Both sources are silent on whether the bytes a producer wrote were truthful. S488's registry text already says so ("This does not certify producer payload truth"), and the round-84 knowledge note `corpus/knowledge/runbook-producer-status-r84.md` says the same. Measured above: `status-sigpipe.sh` writes plausible `MADO_STATUS: sigpipe line 0` on stdout *and* dies by SIGPIPE — plausible text, nonzero status, no contradiction between them.

---

## 5. Question 4 — what does either source NOT license?

This is the part I would press hardest, because several plausible readings of C2's frozen predicate outrun the sources. Each item below is a *non-license* I verified from the source text, with the consequence for the lane's claim.

### 5.1 A shell that merely *starts* a pipeline has not observed its producer

POSIX Issue 8 §2.9.2 says the shell "shall wait for the last command specified in the pipeline to complete, and **may also** wait for all commands to complete" — pinned `S488.bin` @ 131538. The permissive "may also" is decisive: **POSIX does not require the shell to wait for the producer at all**, and the Exit Status table describes the status of *the pipeline*, not of any named stage. Only with `pipefail` enabled does the standard make the status depend on the *nonzero* stages — and even then it reports "the last (rightmost) command … that returned a non-zero exit status", i.e. a status of *some* stage, with no per-stage attribution.

Bash is stronger than POSIX here but still stops short: Bash §3.2.3 says "If a pipeline is not executed asynchronously, the shell waits for all commands in the pipeline to terminate before returning a value" — Bash waits for all stages, and so Bash *can* report the rightmost nonzero. But Bash's wording is about *the pipeline's* return status, and the manual never promises a caller can learn *which* stage failed, nor *why*.

**Consequence:** the C2 class `signal` binds "the pipeline's status is 128+N". It does not bind "the producer was killed by SIGPIPE". On this host the fixture's producer *is* the stage that died (verified rc 141 with the reader `head -n 1` closing the pipe), but that attribution comes from the *fixture's construction*, not from the status value. This is exactly the distinction S490 records as rejected, and my measurement reproduces the same ambiguity in the other direction: `sh -c 'exit 141'` yields 141 with no signal involved. The counter's docstring already states it; the sources confirm there is no way around it from the status alone.

### 5.2 POSIX does **not** license `128+N` — only Bash does

Covered in §3 above, but the consequence is worth restating: a `signal` class bound to `128+N` is a **Bash-encoding** assertion. POSIX only requires *greater than 128*, with implementation-defined signal identification and permission to exceed 255. Any statement of the form "a POSIX shell reports a fatal signal as 128+N" would be false as written.

### 5.3 Neither source licenses "the producer's status" as a distinct observable

There is no POSIX or Bash construct that reports *a named stage's* status separately from the pipeline's. The most C2 can honestly claim is: *the guarded pipeline's status equals the rightmost nonzero stage's status*, and the fixture is arranged so the producer is the only nonzero stage. That is a property of the fixture, not of the shell.

### 5.4 Neither source licenses "the producer exited nonzero" from the status alone

`128+N` distinguishes "died by signal N" from "exited with code 128+N" only *given* the extra fact that the process died. The number alone does not carry that fact. POSIX's implementation-defined wording and Bash's `exit n` builtin ("Exit the shell, returning a status of n to the shell's parent", `bash-5.3/doc/bashref.html` §4.1) both block the converse. S490 is the registry's correct record of this.

### 5.5 Neither source licenses "the negation case behaves like the plain case"

POSIX Issue 8 §2.9.2's `!` rows invert the status (logical NOT). A row that negates a pipeline has a *different* class meaning, and the C2 vocabulary (`ok`/`exact`/`signal`) has no place for an inverted expectation.

### 5.6 Neither source licenses arming `pipefail` from inside the pipeline

POSIX Issue 8 §2.9.2 reads the setting at pipeline start (`S488.bin` @ 132250). `cmd | set -o pipefail` leaves the pipeline unarmed. Only the prefix form is.

### 5.7 Neither source licenses "a backgrounded pipeline reports the producer's failure"

POSIX Issue 8 §2.9.3.1: "The exit status of an asynchronous AND-OR list shall be zero." (13 words) — pinned `S488.bin`; Bash §3.2.3 agrees ("The return status of an asynchronous pipeline is 0"). A `&`-backgrounded probe therefore reports 0 whatever the producer did, and no status class can distinguish the two.

### 5.8 Neither source licenses host support for `pipefail`

POSIX.1-2024 requires `set` to support it; that is a *specification* fact, not a *host* fact. A host whose `/bin/sh` is not POSIX-conforming need not support it. The round-84 knowledge note already insists on this ("host support is separately measured"), and the round-85 fixtures plus my measurement above are the host measurement. This host's `/bin/sh` → bash 5.3.20 accepts `set -o pipefail` (rc 0).

### 5.9 Neither source licenses anything about *payload* truth

Already noted in §4; restated here as a non-license because it is the easiest thing to over-claim from a passing runbook row.

---

## 6. Candidate source for the C1 cause vocabulary — proposal and verdict

The C1 claim rests on held **S486** (RFC 8259 §4) plus "the lane's own declaration grammar" (`claims-declaration-r85.md`, C1 "Sources"). The question asked of me: **one candidate source for the C1 cause vocabulary (duplicate declaration identities refused rather than collapsed), with an admit/reject verdict and the reason.**

### 6.1 The candidate: RFC 7493 (I-JSON) §2.3 "Object Constraints"

`https://www.rfc-editor.org/rfc/rfc7493.txt` — Standards Track, March 2015, T. Bray (Ed.). Independent fetch: 12,849 B, sha256 `a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062`.

Located quotes (each ≤ 25 words):

- §2.3: "Objects in I-JSON messages MUST NOT have members with duplicate names." (12 words)
- §2.3: "In this context, "duplicate" means that the names, after processing any escaped characters, are identical sequences of Unicode characters." (20 words)
- §3 Software Behavior: "This allows receivers to reject or otherwise disregard messages that do not conform to the requirements in this document for I-JSON messages." (24 words)

### 6.2 Verdict: **REJECT for the cause vocabulary as such; ADMIT as a bounded corroborating row for the *refusal* half only.**

Reasoning, in the lane's own terms:

1. **It upgrades the norm from SHOULD to MUST, in-format.** RFC 8259 §4 says "The names within an object SHOULD be unique." (8 words, `rfc8259.txt` @266; the lane's own pin digest `61a5378f…cd2d7` reproduced by my independent fetch) and then concedes that when names are not unique "the behavior of software that receives such an object is unpredictable" — with the explicit note that "Many implementations report the last name/value pair only." I-JSON §2.3 says the same JSON-family object **MUST NOT** have duplicate names. That is the difference between *unpredictable* and *forbidden*, and it is a **Standards Track** strengthening of the very RFC the lane already holds. This is a real, citable upgrade — but see (2).

2. **It does not supply a cause vocabulary, and cannot.** I-JSON states one rule about one class of defect. The C1 vocabulary is **ten** tokens over three distinct defect families — allocation-map shape (`alloc-not-object`, `alloc-empty-namespace`, `alloc-non-integer`, `alloc-negative`), allocation-name resolution (`alloc-unknown-namespace`, `alloc-duplicate-key`), and surface-identity/level collisions (`namespace-duplicate-bar`, `namespace-duplicate-surface`, `namespace-duplicate-cross-level`, `live-duplicate-surface`). Eight of the ten are about *layer-shell namespace identity and level*, a domain I-JSON says nothing about. A source cannot underwrite a ten-token vocabulary it does not mention; the C1 vocabulary's authority is the lane's own declaration grammar, exactly as the declaration already states. Quoting I-JSON as the cause vocabulary's ground would be a category error of the kind criterion 104 (source-grounded sentences must stay within their pinned evidence) exists to catch.

3. **§3 is the part that actually earns a row.** "This allows receivers to reject or otherwise disregard messages that do not conform" is the *permission to refuse* that C1's `alloc-duplicate-key` relies on — a normative, in-format sentence that a receiver may reject a duplicate-bearing message, not merely that it might. S486 licenses refusal *by argument* ("refusing duplicates avoids silently selecting a last value", `corpus/SOURCES.md:438`); I-JSON §3 licenses it *by permission*. That is a genuine strengthening of the same half.

4. **But the scope must be marked, or the row overclaims.** I-JSON is a *restricted profile for Internet protocols*. The lane's `--allocation` declaration is not an I-JSON message, and nothing in the lane establishes that it is. So the row's `teaches` must be scoped to "a Standards Track JSON profile that forbids duplicate member names and explicitly permits receivers to reject non-conforming messages" — **not** "the lane's declaration is I-JSON", and **not** anything about namespace identity, levels, or layer-shell semantics.

5. **It cannot touch the case question.** I-JSON's identity test is "identical sequences of Unicode characters" after escape processing. That is *exact-code-point* identity — so `Waybar` and `waybar` are **two distinct names** under I-JSON, which is the same answer the lane's `ns-case-distinct-accepted` witness already reaches by measurement (`corpus/knowledge/bar-footprint-identity-causes-r85.md`: "a case variant is a different name, never a resolution of another"). So I-JSON is *consistent with* the lane's case handling and gives it a citable ground — but it grounds a **two-names** answer, not the lane's *refusal* of an unknown case-variant key (`alloc-unknown-namespace`), which is a resolution failure, not a duplicate.

### 6.3 The alternatives I considered and why each loses

- **RFC 8785 (JCS) §3.1** — "JSON objects MUST NOT exhibit duplicate property names." (9 words; `rfc8785.txt`, fetched; §3.1 "Creation of Input Data"). Tempting, but it is an **Informational** RFC about *canonicalization for cryptography*, whose whole purpose is to define one canonical serialization — it forbids duplicates so that sorting is well-defined, not to license a consumer's diagnostic vocabulary. It is also built on I-JSON by reference, so it adds nothing I-JSON does not already say, at a weaker tier. **Reject as primary; it is a derivative of the candidate above.**
- **YAML 1.2.2 §3.2.1.1 / §3.2.1.3 / §3.3** — genuinely the richest *vocabulary-shaped* source I found: "with the restriction that each of the keys is unique" and, in §3.3 Loading Failure Points, an enumeration of distinct failure classes (ill-formed stream, unidentified alias, unresolvable tag, unrecognized tag, invalid content, non-unique mapping keys, unavailable native type). Structurally that is much closer to a cause-token taxonomy than anything in the JSON family. **But it is a different data format with different failure semantics, and the lane's declaration is JSON.** Admitting YAML would put a non-JSON grammar behind a JSON declaration's refusals. **Reject.**
- **ECMA-404 (2nd ed., 2017) §6 Objects** — "The JSON syntax does not impose any restrictions on the strings used as names, does not require that name strings be unique" (21 words). This is the *negative* anchor: the normative JSON syntax standard explicitly declines to require uniqueness, and RFC 8259 §1.2 says the ECMA-404 reference is "normative" for the *grammar* only. So ECMA-404 is the right source for the statement "JSON-the-language does not require unique names; therefore the refusal is a *profile* choice, not a syntax requirement" — which is a limit on C1, not a support for it. **Useful as a bounding row, not as the cause vocabulary.**
- **RFC 8259 §8.3 "String Comparison"** — "Implementations that transform the textual representation into sequences of Unicode code units and then perform the comparison numerically, code unit by code unit, are interoperable in the sense that implementations will agree in all cases on equality or inequality of two strings." (43 words → trimmed) "perform the comparison numerically, code unit by code unit, are interoperable" (12 words). This is the strongest available ground for the lane's **exact-string** namespace comparison (the `ns-case-folded` / `alloc-case-folded` mutants' target) — same document as S486, so it would be a *scope extension of an existing row* rather than a new source id. It says nothing about *refusing* duplicates, so it supports the exactness half of C1, not the refusal half.

### 6.4 Net recommendation for the C1 source row

Keep S486 as the load-bearing row. If the lane wants one addition, add **RFC 7493 (I-JSON) §2.3 + §3** scoped to the *refusal-permission* half only (Standards Track, tier A, in-format, digest `a44ccf14…062`), and consider a **scope extension of S486 to RFC 8259 §8.3** for the exact-string-comparison half. Neither may be cited for the ten-token vocabulary, which stays with the lane's own declaration grammar. Record ECMA-404 §6 as the bounding counter-source: uniqueness is a *profile* rule, not a JSON-syntax rule, so no external standard compels this tool's refusal — the lane's own join grammar does.

---

## 7. Cross-checks that matter to the two claims, and what I could not run

**Confirmed (read-only, in-lane):**
- POSIX Issue 8 §2.9.2 is *Pipelines*; §2.9.3 is *Lists*. The declaration's locator is off by one; registry row S488 and lesson M85-8 already carry the correction.
- Bash Exit Status is §3.7.5 in bash 2.05a, 5.2 and 5.3; §3.7.6 is Signals. The declaration's locator is off by one; registry row S489 and lesson M85-8 already carry the correction.
- The GNU HTML endpoint was unreachable from this host (4 reader fetches + 1 curl rc 28). I did not observe that page and make no claim about its bytes. The upstream FTP release tarballs answered, and their `doc/bashref.texi` agrees word-for-word with the lane's maintainer-copy pin.
- My independent POSIX fetch is byte-identical to `.ufo/waves/round-85/fetch/S488.bin` (sha256 `0889867a…1acd`).
- My independent RFC 8259 fetch reproduces the digest the lane's S486 knowledge file pins (`61a5378f…cd2d7`).
- POSIX Issue 7 (2017) has **zero** occurrences of `pipefail` in chapter 2 — the `pipefail` table and the required `set` option are new in Issue 8 (2024).
- Host measurement of the three round-85 fixtures: guarded 0/7/141, unguarded 0/0/0 — the C2 no-work control's premise holds on this host, and the `signal` encoding is this host's Bash's.

**Not run / not claimed:**
- No counter was executed (not my seat: `quality/counters/c1-r85-identity-causes.py` and `c2-r85-status-classes.py` are other seats' files; the freeze and scoring are the main agent's).
- No mutating git/jj command was run; no file outside this report and my scratch was written.
- I did not verify the round-84 closure, the harm-watch receipt, or the mutation battery — out of scope for a source-reading seat.

---

## 8. One-line summary for the ledger

Both sources are read and quoted above; the two declaration locators are off by one section each (POSIX Pipelines is §2.9.2 not §2.9.3; Bash Exit Status is §3.7.5 not §3.7.6) and the lane's registry/lesson already carry both corrections; POSIX.1-2024 mandates `pipefail` as a required `set` option while POSIX says only ">128, implementation-defined" for signals, so `128+N` is Bash's encoding and not a POSIX-wide guarantee; and the strongest candidate for the C1 cause vocabulary is RFC 7493 §2.3/§3, which I would **reject** as the vocabulary's ground (it states one rule, not ten, and eight tokens are layer-shell namespace/level defects it does not mention) and **admit only** as a scoped row licensing the *refusal* half.
