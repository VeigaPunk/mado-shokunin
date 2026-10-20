# SimplifyGateStub — git-stub rc knobs for the omarchy drift rows (R18 W1)

Seat: simplifier (leaf; no subagents). Item: read the selftest `git` stub and the
OM scenarios in `tools/mado-verify.sh` (~:620-720) and propose the smallest change
that lets each git verb fail (rc knobs) without duplicating scenario setup. **No
lane edit.** Every measurement below ran on `/tmp` copies (`/tmp/mado-r18-lab/`);
the lane working tree was verified byte-identical before and after
(`tools/mado-verify.sh` sha256 `2bdf5e8afbb6…` at close, unchanged by this seat).
No lane gate was executed; `--selftest`/`--regression` were run only against those
`/tmp` copies. Only this report was written.

Axes named for the item:

- **A1 expressiveness** — each of the three git verbs can exit nonzero on demand,
  with its canned stdout still available.
- **A2 minimality** — the knobs are added to the existing stub and driven through
  the existing OM fixture; no second fixture tree, no per-verb scenario setup.
- **A3 bite** — the new assertions fail when the property under test is removed
  (an assertion that cannot fail is documentation, not a check).
- **A4 fidelity** — the rc is attributed to the verb that produced it, and the
  bytes hashed are exactly the bytes that verb wrote.
- **A5 regression budget** — the 372 assertions at HEAD stay green, and the
  recorded mutation table still reproduces.

## 1. The fixture as it stands at HEAD

`tools/mado-verify.sh` at HEAD (`fba82a662795…`, 372/372 selftest assertions) builds
the OM fixture once at `:622`-`:801`: stub dir `$OMB`, fixture root `$OMR`, leaf
`$OM_LEAF`, command JSON `$OM_CMDS`. The stub is `:664`-`:670`:

```
describe) printf '%s\n' "${STUB_GIT_TAG:-v3.8.4}"; exit 0 ;;
rev-parse) printf '%s\n' "${STUB_GIT_HEAD:-8fcc9d60…}"; exit 0 ;;
show) cat "${STUB_GIT_BLOB:-/dev/null}"; exit 0 ;;
```

All three verbs hard-code `exit 0`, so **no OM case can reach a git-failure arm**:
`omarchy.git.tag` `:3432`, `omarchy.git.head` `:3441`, and (after any rc fix)
`omarchy.skill.vs_head`. `STUB_GIT_{TAG,HEAD,BLOB}` select stdout only. The audits
ask for the knobs (`JjAuditMado.md:358`: "Add `STUB_GIT_RC` (and per-verb rc) plus
an OM scenario asserting UNKNOWN"). Per-verb, not one knob: a single `STUB_GIT_RC`
cannot fail `describe` while `rev-parse` still answers, so it cannot separate the
tag row from the head row.

## 2. Proposed mechanism — 3 changed lines, no new setup

```
-    describe) printf '%s\n' "${STUB_GIT_TAG:-v3.8.4}"; exit 0 ;;
-    rev-parse) printf '%s\n' "${STUB_GIT_HEAD:-8fcc9d60…}"; exit 0 ;;
-    show) cat "${STUB_GIT_BLOB:-/dev/null}"; exit 0 ;;
+    describe) printf '%s\n' "${STUB_GIT_TAG:-v3.8.4}"; exit "${STUB_GIT_DESCRIBE_RC:-0}" ;;
+    rev-parse) printf '%s\n' "${STUB_GIT_HEAD:-8fcc9d60…}"; exit "${STUB_GIT_REV_PARSE_RC:-0}" ;;
+    show) cat "${STUB_GIT_BLOB:-/dev/null}"; exit "${STUB_GIT_SHOW_RC:-0}" ;;
```

(plus two comment lines naming the knobs; the header comment at `:664-666` currently
says the answers are canned, which stays true).

Why **emit then fail**, rather than exit before printing: the property that must be
proven is *the row trusts the verb's status, not its stdout*. Fail-before-print can
only prove "empty output is not mistaken for a digest"; it cannot express a failure
whose stdout happens to match the worktree, which is the false-PASS half of the
same defect class (measured in §4 row 3). One knob covers both directions: leave
`STUB_GIT_BLOB` at the leaf for the matching-bytes failure, point it at `/dev/null`
for the empty failure.

Knob spelling: `STUB_GIT_DESCRIBE_RC`, `STUB_GIT_REV_PARSE_RC`, `STUB_GIT_SHOW_RC`
— one rule (verb, underscore, `RC`), `:-0` so unset *and* empty keep `exit 0`, which
is what keeps OM1-OM8 behavior identical (measured, §4 row 1 vs 2).

## 3. Proposed scenarios — 33 lines, inserted at the OM8 tail (`:800-:801`)

Both cases reuse `$OMB`, `$OMR`, `$OM_LEAF`, `$OM_CMDS`; nothing is built twice.

```
  # --- OM9: a failing git read verb is UNKNOWN, never its stdout -----------
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB="$OM_LEAF" \
    STUB_GIT_DESCRIBE_RC=7 STUB_GIT_REV_PARSE_RC=8 MADO_VERIFY_LIVE=yes \
    "$BASH_BIN" "$0" --root "$OMR" 2>&1); om_rc=$?
  st_eq  "OM9: exit 1 — the unreproducible sha row stays the only red" 1 "$om_rc"
  st_row_detail "$om_out" omarchy.git.tag UNKNOWN "rc=7" \
    "OM9: describe's rc reaches the tag row, not its v3.8.4 stdout"
  st_row_detail "$om_out" omarchy.git.head UNKNOWN "rc=8" \
    "OM9: rev-parse's rc reaches the HEAD row"
  st_not_has "OM9: a failed describe is never read as a moved tag" "$om_out" "MOVED: describe"
  st_not_has "OM9: a failed rev-parse is never read as a held HEAD" "$om_out" "HELD: 8fcc9d60"
  st_counts_agree "$om_out" "OM9: counts agree with rows"

  # --- OM10: a failed `git show` is UNKNOWN, never a digest of nothing ----
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB="$OM_LEAF" \
    STUB_GIT_SHOW_RC=128 MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR" 2>&1)
  st_row_detail "$om_out" omarchy.skill.vs_head UNKNOWN "rc=128" \
    "OM10a: a failed show is UNKNOWN even when its bytes match the worktree"
  st_not_has "OM10a: ... never a false 'worktree == HEAD blob'" "$om_out" "worktree == HEAD blob"
  om_out=$(env PATH="$OMB" STUB_OM_CMDS="$OM_CMDS" STUB_GIT_BLOB=/dev/null \
    STUB_GIT_SHOW_RC=128 MADO_VERIFY_LIVE=yes "$BASH_BIN" "$0" --root "$OMR" 2>&1)
  st_row_detail "$om_out" omarchy.skill.vs_head UNKNOWN "rc=128" \
    "OM10b: a failed show with no bytes is UNKNOWN"
  st_not_has "OM10b: ... no false 'local edit'" "$om_out" "local edit"
  st_not_has "OM10b: ... and the empty-input digest is never named" "$om_out" "e3b0c442"
  st_counts_agree "$om_out" "OM10: counts agree with rows"
```

Distinct rc values 7 and 8 in OM9 mean one run proves per-verb wiring, because each
row echoes its own rc. OM10 needs two runs only because the two halves of F10 are
mutually exclusive in one invocation (matching bytes vs no bytes); it is two `env`
lines, not two fixtures.

## 4. Evidence that the checks are alive (all `/tmp` lab)

| # | variant | result |
|---|---|---|
| 1 | HEAD copy (`base.sh`, sha `fba82a66…`) | `MADO_SELFTEST: 372/372 assertions passed` (9.8 s) |
| 2 | §2+§3 plus the `:3406` rc fix and a `PIN_MADO` re-cut | `384/384 assertions passed`; `MADO_REGRESSION: PASS`, table 10/10 KILLED, flips 0, target `8bdded4bfa9f…`, harness `0673d2e5…` (recorded `b56c6e57…`, provenance only) |
| 3 | same as 2 with only the `:3406` fix reverted | 378 passed / **6 failed**: `R10` (expected pin drift) + all five OM10 assertions — the old pipeline printed `worktree == HEAD blob` for a failed read (false PASS) and `… != HEAD blob e3b0c442… (local edit)` for an empty failed read (false FAIL, exactly `JjAuditMado.md:235-247`) |
| 4 | same as 2 with the tag `grc` check neutered (`if false; then`) | OM9 fails: `want row omarchy.git.tag UNKNOWN containing 'rc=7'` — OM9 bites even though it passes against HEAD code |
| 5 | pipeline semantics | after `blob=$(… \| sha256sum \| cut …)`, `PIPESTATUS[0]` is **0**, so the audit's suggested `grc=${PIPESTATUS[0]}` (`JjAuditMado.md:350`) does not capture git's rc; `set -o pipefail` *inside* the substitution yields rc 3 and does not leak (`pipefail off` outside) |

Row 4 is the honest qualification on OM9: against HEAD code it is coverage, not a
bite (the tag/head rc arms are already correct at `:3432`/`:3441`); its value is
that it fails if those arms are ever simplified away.

## 5. Reconciliation with the change already in the working tree

While this seat was measuring, the working tree gained a comparable change
(`tools/mado-verify.sh` sha `2bdf5e8afbb6…`, +17 assertions, stub knobs at
`:672`/`:675`/`:678`, OM9 at `:811`, OM10 at `:832`, show fix at `:3453`-`:3467`).
Measured on a copy of exactly that file:

- `--selftest`: **388/389**, the only failure is `R10` — `PIN_MADO` is still
  `cd1d73d75fcc…` while the R7-excised target is now
  `20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744`.
- With that pin re-cut in the copy: **389/389**, and `--regression` PASSES:
  `REGRESSION_TABLE … match=10/10 recorded-killed=10 measured-killed=10 survived=0
  inconclusive=0 flips=0`, `MADO_REGRESSION: PASS (case=mado-verify-hardened;
  target=20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744)`
  (111 s wall).

So the pin re-cut is mandatory, not cosmetic: the R7 excision removes only the two
`MADO-R7-*` blocks, so every line added inside `MADO-R8-OMARCHY-BLOCK` moves
`PIN_MADO`. Order matters: final edit → take the `R10` "got" value → re-cut →
`--regression` green. (The regression table did reproduce unchanged for both this
variant and the §2/§3 variant, so the added assertions cost no re-measurement
beyond the pin.)

Deltas worth taking in that landed change (each ≤ 3 lines):

1. **Stub shape** — the landed stub exits *before* printing (`if [ "${…_RC:-0}" != 0 ]; then exit …; fi`
   then `printf`), 9 lines where 3 suffice, and a failing verb can never emit the
   worktree's bytes, so the false-PASS direction of F10 stays untestable (row 3
   above is what that costs). Replace with the emit-then-fail three-liner in §2.
2. **Knob spelling** — landed `STUB_GIT_REVPARSE_RC` (`:675`) versus
   `STUB_GIT_DESCRIBE_RC` / `STUB_GIT_SHOW_RC`; use `STUB_GIT_REV_PARSE_RC` so the
   three names follow one rule.
3. **Dead arm** — `elif [ -z "$blob" ]` at `:3465` now follows the rc test, so it
   can no longer fire for the failure it names ("cannot read HEAD:…"); the only
   reachable path is `sha256sum` itself dying, which `have sha256sum` at `:3451`
   already treats as a precondition. Delete those 2 lines (or, if kept as a belt,
   reword: it no longer describes git). This is the arm `JjAuditMado.md:243-246`
   called unreachable; the rc fix makes the rc arm govern and leaves this one
   vestigial.
4. The landed OM10's `omarchy.skill.vs_head PASS` assertion while tag/head are
   UNKNOWN is a good independence pin — keep it.

## 6. Preserved contract

- OM1-OM8 assertions are untouched: with knobs unset the stub is behaviorally
  identical (`exit 0`, same bytes), and rows 1-2 of §4 differ only by the 12 new
  assertions.
- No scenario setup is duplicated: no new directories, stub files, or roots; all
  new cases are `env … "$BASH_BIN" "$0" --root "$OMR"` against the existing
  fixture.
- No other plane's rows, no theme scenarios, no tripwire file and no harness were
  touched; harness sha drift is reported by the gate as provenance, not gated.
- Lane tree untouched by this seat (sha verified at start `fba82a66…`, at close
  `2bdf5e8a…`, the latter from the sibling's in-flight edit, not this seat).

## 7. Named limitations / tradeoffs

- **`sw`'s producer is unchecked too** — `sw=$(sha256sum "$leaf" 2>/dev/null | cut …)`
  (`:3463`) has the same class of defect (a failed local read becomes an empty
  `sw`, hence a false "local edit" FAIL). Same one-line rc capture would fix it,
  but a deterministic fixture needs `chmod 000`, which is root-dependent and would
  make the suite non-hermetic; recorded here, deliberately not tested.
- **`timeout 5` → rc 124** maps to UNKNOWN with a message that says "git show
  failed (rc=124)". Correct direction; no scenario (would cost 5 s per assertion).
- **Emit-then-fail is less git-like** — real git usually prints nothing on failure.
  The fixture's job is to bound the code's decision space; the realistic empty
  case stays covered by `STUB_GIT_BLOB=/dev/null`, so nothing is lost.
- **Cost** — OM9 is one extra live-mode gate run, OM10 two: measured 10.8 s patched
  selftest versus 9.8 s base, +1.0 s total.

Install/update record: none (no tool installed, upgraded, or queried).
