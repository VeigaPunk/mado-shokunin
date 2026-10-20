# MadoR19.AtkGateHeader — partial

Item: the gate's walker re-pin text — `tools/mado-verify.sh` header lines 50-110,
`walker_live_rows`, and the WL0-WL3 scenarios, at tip `01b80946d92b26370d3012a7da655d00dd135154`.
**All line numbers below are the committed tip bytes** (`git show 01b8094…:tools/mado-verify.sh`,
blob `45357874…`, 4097 L), re-read with `nl -ba` on that stream. The worktree later acquired an
uncommitted wave-2 changeset (24 files; `tools/mado-verify.sh` is now blob `693dce3f…` / 4156 L).
I did not use the drifted file for any citation and did not touch it; see Limits for what that
changeset already rewrites.

## Direct answers

1. **Does the PASS certify only "installed version matches pin"? — Yes.**
   The live PASS text (tip `tools/mado-verify.sh:3296`) is exactly:
   `"$WALKER_VERSION_PIN (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)"`.
   The header states the same narrowing twice (`:56-61`, `:65-69`), the function comment at
   `:3284-3288` says it again, the call-site comment at `:3553-3555` says "never the 2.17.0-era
   claims", and the FAIL arm at `:3298` forces re-verification on a moved pin. No PASS string
   claims a refresh; WL1 asserts both the disclaimer substring and the absence of the exact
   phrase `claims re-verified` (`:1265-1269`).

2. **Does any line still imply the 2.17.0-era claims (MADO-R3-1 §6, 298 L) are re-verified? — No.**
   `grep -n "298"` on the tip finds only `:60` and `:1922`, both of which say the table **stays
   dated**. §6 citations at `:3281` and `:3286` are immediately narrowed by `:3284-3288`; `:3553-3555`
   says "never the 2.17.0-era claims". The 298 L figure is in fact stale (S091 records 305 L /
   13,743 B), and the gate dates rather than restates it.

3. **Is WL0 honestly labelled? — Yes as written, with one coupling caveat.**
   `:1258-1259` asserts `"2.17.2" = "$WALKER_VERSION_PIN"`. The label says
   "pin constant is 2.17.2 (S096 file-byte evidence; not a host read)". The value's provenance is
   real at tip: `corpus/SOURCES.md:108` (S096) records the sole literal `2.17.2\n` at file offset
   856,302 in `.rodata`, and the same row says no running-process fact is claimed. The check does
   not read S096 or the host; it would pass unchanged if S096 were retracted or its literal moved.
   That is a weak coupling, not a false label.

## Findings

### F1 (main) — the pins bullet still names a pin authority that says 2.17.0
Tip `tools/mado-verify.sh:65-69`:

```
#   pins    — Hyprland 0.56.2 commit efb5099…, waybar v0.15.0, walker 2.17.2
#             (S096 host rodata + S090 pacman.log:2929, round 19; SKILL.md
#             "Version pins"): ...
```

`SKILL.md:22-23` still reads `Version pins for all claims below: … walker 2.17.0`.
The superseding text is an append-only errata at `SKILL.md:1853-1856` ("This supersedes the pins
above … the pin line names what was measured, not what is installed"), which the gate does not cite.
The baseline had the same citation with 2.17.0 (`git show 9c54c56:tools/mado-verify.sh:60-62`), so
the re-pin changed the value without re-anchoring the authority. This is exactly the risk wave 1
pre-registered at `.ufo/waves/round-19/w1/reports/CriticC2.md:121`: the gate now uses the
*installed* pin meaning while the section it names uses the *measured* pin meaning; only the
uncited errata distinguishes them. A reader checking the gate's pin against the named block sees
2.17.0. [INFERENCE] on how tightly the parenthetical binds to walker; the bytes are certain.
Smallest fix: cite `SKILL.md` errata (round 19) or scope the `SKILL.md "Version pins"` pointer to
Hyprland/waybar and leave walker on S096/S090.

### F2 — the WL negative guards are weaker than their labels
(a) `:1269` `st_not_has … "claims re-verified"` is literal-phrase blind. Scratch mutants of the
tip PASS row (`/tmp` copies, `--selftest` only):
- insert `; all claims are re-verified` → rc 2, **442/443**, only `R10` (byte identity) failed;
  the WL1 negative did **not** fire.
- insert `; claims re-verified` → rc 2, **441/443**, `R10` + `WL1: the PASS claims no claim refresh`
  (`unexpected: claims re-verified`).
So a paraphrased refresh claim passes the honesty guard; only the exact phrase is caught. The
positive check at `:1267` is a substring requirement, so the two can coexist.
(b) `:1291` `st_not_has "WL: no row still names the old 2.17.0 pin" "$wl_out" "2.17.0"` runs on the
`$wl_out` set at `:1285-1286` from the **WL3 absent-binary arm only**. That arm's rows cannot
contain `2.17.0` by construction, while the WL1 PASS row deliberately contains `2.17.0` as the era
marker (asserted at `:1267`). The label says "no row", the check covers one row set and is
vacuous for the PASS arm.

### F3 — an unreadable version is reported as a pin change, not UNKNOWN
`walker_live_rows` `:3294-3298` reads `kv=$(tmo walker --version 2>/dev/null | head -1)`; if the
binary is present but times out, errors, or prints to stderr, `kv` is empty and the row emits
`FAIL "pin changed: ''"`. The header's own rule (`:25-26`) says "a plane that cannot be verified
reads UNKNOWN". FAIL also blocks CLEAN, so no fake CLEAN, but the diagnosis is false. No WL
scenario covers present-but-unreadable: WL1 match, WL2 drift, WL3 absent (`:1258-1291`). Same
class at `:3305-3310`: `systemctl` present but no user bus → both values empty →
`FAIL "… (want active/active)"` instead of UNKNOWN. The live-plane preflight requires a
reachable Hyprland session, which reduces but does not eliminate the bus case. [INFERENCE] on
reachability; the mapping is source-observed and unexecuted under the host pause.

### F4 (minor) — "installed binary" is a PATH command, not a bound artifact
`:3289-3294` checks `have walker` and the first line of `walker --version`; nothing binds the
command to `/usr/bin/walker` or to S096's digest `25240650…`. A PATH shim printing `2.17.2`
satisfies the row while the text at `:3296` says "installed version". Low risk on this host,
but the wording is stronger than the check. [INFERENCE].

### F5 (minor) — a run history that did not happen
`:102-103` says "the old pin failed every live run from that transaction onward". The last
recorded live gate receipt is `.ufo/evidence/round-12/gate-live-after.txt:30`
(`hypr-live live.walker.version PASS 2.17.0 (pin matches)`); `find .ufo -name '*gate-live*'`
returns only round-12. No live run exists after the 2026-10-20 transaction, so the sentence is
true only vacuously or as a counterfactual ("would fail").

### F6 (minor) — the dated example misnames the artifact
`:59-60` calls the 298 L item "the 298 L packaged help table". The claim it is dating is the
packaged default file, not a help table: `corpus/knowledge/waybar-walker-semantics.md:234`
(`git show 01b8094…:…`) reads `packaged default | /etc/xdg/walker/config.toml | 298 lines |
full default table`; §6.1 is the config-line count, and S091 re-measures the same file at
305 L / 13,743 B. No 298-line `walker --help` table exists in the committed knowledge.
The value is correctly dated, but the noun is wrong, so the disclaimer does not faithfully
quote the claim it dates.

## Commands and outputs

```
$ git -C … rev-parse HEAD
01b80946d92b26370d3012a7da655d00dd135154
$ git hash-object tools/mado-verify.sh          # at first check
45357874ae17941e5127bad9de399a7880b3bc78
$ git rev-parse 01b8094…:tools/mado-verify.sh
45357874ae17941e5127bad9de399a7880b3bc78

$ bash tools/mado-verify.sh --selftest          # on the tip worktree, 4097 L
MADO_SELFTEST: 443/443 assertions passed        # rc=0, 13.0 s, twice

$ git show 01b8094…:tools/mado-verify.sh | nl -ba | sed -n '53,69p;99,105p;3289,3312p'
   56  version pin 2.17.2 (S096 host rodata + S090 pacman.log:2929;
   57  round-19 re-pin). The version row's PASS certifies one thing
   58  only: the installed binary prints the pin. It does not refresh
   59  the claims — the 2.17.0-era measurements (MADO-R3-1 §1/§6, e.g.
   60  the 298 L packaged help table, probe window 2026-10-14) stay
   61  dated and are routed by walker-route-r18.md.
   65  pins    — … walker 2.17.2
   66  (S096 host rodata + S090 pacman.log:2929, round 19; SKILL.md
   67  "Version pins"): …
  105  WALKER_VERSION_PIN="2.17.2"
 3289  walker_live_rows() {
 3294    kv=$(tmo walker --version 2>/dev/null | head -1)
 3295    if [ "$kv" = "$WALKER_VERSION_PIN" ]; then
 3296      row … PASS "$WALKER_VERSION_PIN (installed version matches pin; claims measured on 2.17.0 2026-10-14 stay dated — walker-route-r18.md, S096)"
 3298      row … FAIL "pin changed: '$kv'; re-verify claim anchors (pin $WALKER_VERSION_PIN, S096)"

$ git show 01b8094…:SKILL.md | nl -ba | sed -n '22,23p;1853,1856p'
   22  Version pins for all claims below: Hyprland 0.56.2 …, waybar v0.15.0,
   23  walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified `hyprctl version`). …
 1853  ## Errata (round 19, append-only — walker 2.17.2 pins; S090/S091/S096)
 1855  > Erratum … This supersedes the pins above: …

$ git show 01b8094…:corpus/SOURCES.md | sed -n '108p'   # S096 tail
… **no running-process fact is claimed** — `walker --version` was not executed (host pause) | mined | 2026-10-20 | on-change | …
$ git show 01b8094…:corpus/knowledge/walker-route-r18.md | nl -ba | sed -n '328p'
 328  - Host walker binary on 2026-10-20 (file bytes, S096): 2.17.2 literal at offset 856,302; `--version` output and runtime behaviour of 2.17.2 are not observed (host pause) and stay [UNK].

$ find .ufo -name '*gate-live*' -o -name '*live-after*'
.ufo/evidence/round-12/gate-live-after.txt
.ufo/evidence/round-12/gate-no-live-after.txt
$ sed -n '30p' .ufo/evidence/round-12/gate-live-after.txt
hypr-live live.walker.version             PASS    2.17.0 (pin matches)
```

Scratch mutation receipts (tip bytes copied to `/tmp/atkgh/*.sh`, each run with `--selftest`; R10 is the
byte-identity check and fails on any mutation by design, so only non-R10 failures are behavioral):

```
a  :3295  "=" -> "!="                          rc=2  WL1(a 2.17.2 binary…), WL1 PASS-detail,
                                                     WL1 two-rows, WL2 all three  -> comparator killed
b  :3296  + "; all claims are re-verified"     rc=2  442/443  only R10        -> WL1 guard blind
c  :3296  + "; claims re-verified"             rc=2  441/443  R10 + WL1 negative -> exact phrase caught
```

## Limits

- Host pause: I did not execute `walker`, `pacman`, `systemctl`, `hyprctl`, or the gate's live
  mode. The 2.17.2 `--version` print is unobserved; its being exactly `2.17.2` is [INFERENCE] from
  the S096 rodata run `version2.17.2\n` and the round-12 plain `2.17.0` observation. A prefixed
  print (e.g. `walker 2.17.2`) would make every live run a false FAIL; S096 explicitly leaves the
  print [UNK].
- F1's severity depends on how a reader binds the `SKILL.md "Version pins"` parenthetical; the
  stale bytes are certain, the reading is [INFERENCE]. The errata does resolve the semantic split
  for a reader who reads to `SKILL.md:1853`.
- F3's reachability under a live Hyprland session is [INFERENCE]; FAIL and UNKNOWN both block
  CLEAN, so no fake-CLEAN path.
- The worktree drifted mid-run: a 24-file uncommitted wave-2 changeset now exists. All citations
  are from `git show 01b8094…`; the two 443/443 receipts were taken while the worktree still
  hashed to the tip blob (`wc -l` = 4097). I made no lane edits and no git/jj writes.
  For triage, the uncommitted gate diff already rewrites F1 (`SKILL.md "Version pins"` scoped to
  Hyprland/waybar, with `SKILL.md:23` named as the measured 2.17.0), F5 ("would FAIL ... no live
  gate receipt exists after round 12") and F6 ("packaged default config (/etc/xdg/walker/config.toml)"),
  and replaces the WL "no row still names 2.17.0" check with exact PASS-value assertions
  (`live.walker.version PASS 2.17.2 (` / no `2.17.0 (pin matches)`), closing F2(b). It does not
  change the `claims re-verified` literal guard (F2(a)) or add a present-but-unreadable arm (F3);
  F4 is unchanged. The tip under attack still carries all six findings.
- Scratch mutants lived only under `/tmp/atkgh`; no lane file was copied into the lane or
  modified. R10 failures on mutants are expected and were not counted as behavioral.

## Installs

none.
