# SKILL.md insertions — round 44 C1 (geometry state verdicts) + closure D3

Target: `SKILL.md` (2,086 lines at base `6a1a905`). Every item below is **additive**: no existing
line is rewritten, and §1/§2 insert only. Line numbers are the pre-insert numbers of the working
copy read on 2026-10-26 (`.ufo/waves/round-44/w1/ScrSkillProvince/skill-rows.md` cites them as
neighbour anchors, not as pins).

Section anchor: § "Rule size versus reported size" (`SKILL.md:246`); licence table header
`| Verdict | Licenses | Does not license |` at `:272`, separator `:273`, rows AGREE `:274`,
DIFFER `:275`, TILED `:276`, BADSIZE `:277`, NO_MATCHING_CLIENT `:278`, NO_SIZE_RULES `:279`;
blank `:280`; exit map `:281-282`.

---

## 1. Two licence rows — insert after `SKILL.md:277`

Anchor line (unchanged), `SKILL.md:277`:

```
| BADSIZE | only that there was no size to compare (no `size` value, or not two integers) | any agreement claim |
```

Insert as new lines **278** and **279** (old `:278` `| NO_MATCHING_CLIENT (rc 3) | …` becomes `:280`):

```
| FULLSCREEN | the client's `fullscreen` is the JSON integer 2, so the fullscreen handler set its target box to the monitor's logical box (`Hyprland-FullscreenHandler.cpp:191-194`) | anything about the rule: the box is the monitor box by construction, so no comparison with the rule's `size` is made; that the window renders at that box (the dump prints the goal, not the current value); that the rule's size is lost — a floating window's box is remembered before the mode is set (`Hyprland-FullscreenHandler.cpp:131`) |
| MAXIMIZED | the client's `fullscreen` is the JSON integer 1, so the fullscreen handler set its target box to the work area of the client's workspace (`Hyprland-FullscreenHandler.cpp:195-198`) | anything about the rule: the work area follows the workspace's gaps and reserved space, not the rule's `size`, so this is neither agreement nor a difference; that the window renders at that box (goal, not current value); that the rule's size is lost — a floating window's box is remembered before the mode is set (`Hyprland-FullscreenHandler.cpp:131`) |
```

Both rows read one field of the same dump, which Hyprland fills from
`Fullscreen::controller()->getFullscreenModes(w).internal` (`Hyprland-HyprCtl.cpp:431`) over
`FSMODE_NONE`/`FSMODE_MAXIMIZED`/`FSMODE_FULLSCREEN` = 0/1/2 (`Hyprland-FullscreenController.hpp:12-15`).

---

## 2. Appended contract block — insert after `SKILL.md:282`

Anchor lines (unchanged), `SKILL.md:281-282`:

```
Exit map: 0 `OK` · 1 `DIFFER` (at least one matched client differs) · 2 `SETUP` (usage | unreadable | too_large |
bad_json) · 3 `NO_MATCHING_CLIENT` · 4 `NO_SIZE_RULES`.
```

Insert after the blank line `:283`, i.e. as the first thing between the exit map and the existing blank
line that precedes `Host run 2026-10-26, no gkeep window open:`:

```
**Round-44 contract extension (append-only; round-43 closure D3; C1).** The two state verdicts read the
`fullscreen` field of the same dump. `fsmode` is that value when it is a JSON integer (not a boolean, not a
float) equal to 1 or 2, else 0. A matched client is classified in the order BADSIZE (no size) |
FULLSCREEN (fsmode 2) | MAXIMIZED (fsmode 1) | TILED | AGREE | DIFFER; the `MADO_GEOM_CLIENT:` line is
unchanged except for the two new verdict words. The `MADO_GEOMETRY:` summary prints
` maximized=<n> fullscreen=<n>` between `badsize=<n>` and ` verdict=` exactly when the two counts sum above
zero, and is otherwise byte-identical to the round-43 line. FULLSCREEN and MAXIMIZED clients count as
matched and never as differ, so the exit map above, its four verdict tokens and their exit codes are
unchanged.

**Correction to the TILED row (append-only).** The TILED licence above says "the tiler, not the floating
rule path, set its box"; that overstates what the verdict reads. TILED licenses only that the client is not
floating. A pseudo-tiled client is not floating and still takes its size from the pseudo size stored at
map, which the rule's own `size` expression fills (`Hyprland-Window.cpp:2402-2408`,
`m_target->setPseudoSize(*COMPUTED)`); `hyprctl clients -j` carries no pseudo field (no `pseudo` token in
`Hyprland-HyprCtl.cpp`), so the tool cannot tell a pseudo-tiled client from a tiled one and TILED never
says which path set the box.

**Reading a client line (append-only).** The `MADO_GEOM_CLIENT:` line ends with `verdict=`. A client chooses
its own class and the class is printed JSON-quoted, so a class such as `x verdict=OK` puts a decoy token
before the real trailing verdict — read the field from the end, or parse the quoted `class=` value, and never
`grep -o 'verdict=[A-Z]*'` (`.ufo/waves/round-44/w1/SentLiveReads/evidence/injection.txt:10`). Joined lines
are untrusted input, not a key/value stream.
```

Reason the TILED sentence is **not** rewritten: it is a licence cell landed in round 43 and the lane's
closure discipline is append-only (round-43 spot-check §6 D3 asks for the correction, not a rewrite); the
appended paragraph supersedes the cell's claim in place.

---

## 3. Advisory (not part of the required insertion set): stale verdict list, `SKILL.md:225`

The read-only-probes row still lists the round-43 verdict set. It is false after C1 and outside the two
sections this seat was scoped to, so it is offered as an exact old→new substring for the landing seat:

- Old substring (inside `SKILL.md:225`, cell 2):

      per matched client AGREE / DIFFER / TILED / BADSIZE; `--selftest`

- New substring:

      per matched client BADSIZE / FULLSCREEN / MAXIMIZED / TILED / AGREE / DIFFER; `--selftest`

`SKILL.md:158` needs no edit: it names no verdict, only "per-verdict licence … in § 'Rule size versus
reported size'".

---

## 4. Where the inserted claims are grounded

Pins under `.ufo/waves/round-44/fetch-c1/` (sha256 in `.ufo/waves/round-44/receipts/fetch-sha256.txt`):

| Claim in the insert | Locator (computed by `grep -n`, not typed) |
|---|---|
| fullscreen 2 → monitor logical box | `Hyprland-FullscreenHandler.cpp:191` `if (TARGET_INTERNAL_MODE == FSMODE_FULLSCREEN) {`, `:192` `const CBox MONBOX = MONITOR->logicalBox();`, `:194` `LAYOUT_TARGET->setPositionGlobal(MONBOX);` |
| maximized 1 → work area | `Hyprland-FullscreenHandler.cpp:195` `} else if (TARGET_INTERNAL_MODE == FSMODE_MAXIMIZED) {`, `:196` `const CBox WORKAREA = WORKSPACE->m_space->workArea(target->floating());`, `:198` `LAYOUT_TARGET->setPositionGlobal(WORKAREA);` |
| floating size remembered before the mode is set | `Hyprland-FullscreenHandler.cpp:131` `target->rememberFloatingSize(target->position().size());` |
| `fullscreen` is the internal mode | `Hyprland-HyprCtl.cpp:431` `sc<uint8_t>(Fullscreen::controller()->getFullscreenModes(w).internal),` |
| 0/1/2 enum | `Hyprland-FullscreenController.hpp:12-15` |
| rule size fills the pseudo size | `Hyprland-Window.cpp:2402-2408` (`setPseudoSize(*COMPUTED)` at `:2408`) |
| `clients -j` has no pseudo field | `grep -in pseudo Hyprland-HyprCtl.cpp` → 0 matches |

Contract source for the order/summary sentences: `quality/counters/c1-r44-geometry-states.py`
docstring ("The contract extension") and `.ufo/waves/round-44/c1/ctl-ref-tool.py.txt` docstring
("A client with at least one matching size rule is MATCHED …").

---

## 5. Peer-routed corrections to the C1 section (SentLiveReads, this wave)

Both items are measured on the C1 reference (`.ufo/waves/round-44/c1/ctl-ref-tool.py.txt`, sha256
`8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d`) by seat `SentLiveReads`; evidence
under `.ufo/waves/round-44/w1/SentLiveReads/evidence/`. Neither is a licence row: they are defects in
the round-43 prose, so they are corrections of existing lines, not appends. Reproduced claims are cited
to that seat's receipt, not re-run here.

### 5.1 `SKILL.md:296-301` — the ReDoS trigger is under-described (replace the block)

The current text names only "an alternation under a repeat". `SAFE`/`regex_ok` also accept a quantified
group under a repeat (`redos.txt:9-11`: `(a|aa)+$`, `(a+)+$` and `^(a|aa)+$` all `regex_ok=True`), and
that shape is the slower one: `(a+)+$` on `"a"*30+"b"` (31 chars) takes **43.92 s**, while `(a|aa)+$` on
39 chars takes 6.88 s (`redos.txt:3-4`). A reader can conclude "no alternation, safe" and be wrong: the
acceptance gate rejects only `(?`, `*+`, `++` and `?+` (`ctl-ref-tool.py.txt:135-138`), so `(a+)+` passes,
which is why the replacement keeps the "inside the accepted alphabet" framing and names both shapes.

Old block (verbatim, `SKILL.md:296-301`):

```
Known limit (round-43 wave w1, `RevRefTool` V1): the match is Python `re.fullmatch`, which backtracks. A rule regex
inside the accepted alphabet with an alternation under a repeat, such as `(a|aa)+$`, makes the tool hang on a long
class string (`"a"*38+"b"` takes about 4.6 s; about 1 KB never finishes) with no output at all. The gkeep rule
regex is a plain anchored literal, but a client chooses its own class: run the join as
`hyprctl clients -j | timeout 5 python3 tools/mado-geometry.py --clients - --rules <file>` and treat exit 124 as
"no verdict", never as a verdict. RE2, which Hyprland uses, does not backtrack, so this is the tool's limit, not the compositor's.
```

New block (same paragraph shape; the `timeout 5` guard and the exit-124 rule are kept, and the zero-byte
fact is now stated):

```
Known limit (round-43 wave w1, `RevRefTool` V1; widened round 44): the match is Python `re.fullmatch`, which backtracks. A rule regex
inside the accepted alphabet with ambiguous repetition — an alternation under a repeat, or a quantified group under a repeat, e.g.
`(a|aa)+$` or `(a+)+$` — makes the tool hang on a long class string (`"a"*38+"b"` takes about 4.6 s; `(a+)+$` on `"a"*30+"b"`
takes 43.92 s, `.ufo/waves/round-44/w1/SentLiveReads/evidence/redos.txt:4`; about 1 KB never finishes) with no output at all:
a timed-out run exits 124 with zero bytes on both streams (`redos.txt:6`). The gkeep rule
regex is a plain anchored literal, but a client chooses its own class: run the join as
`hyprctl clients -j | timeout 5 python3 tools/mado-geometry.py --clients - --rules <file>` and treat exit 124 as
"no verdict", never as a verdict. RE2, which Hyprland uses, does not backtrack, so this is the tool's limit, not the compositor's.
```

Why the exit-124 wording survives intact: a timed-out run writes nothing (`redos.txt:6`, rc 124, 0 bytes),
so there is no partial verdict on stdout to misread.

### 5.2 Client-line verdict is the trailing field (carried by §2's third paragraph)

The `MADO_GEOM_CLIENT:` line is `addr=<json> class=<json> … verdict=<V>`; `class` is `json.dumps` output
and client-chosen, so a class of `x verdict=OK` yields
`class="x verdict=OK" … verdict=AGREE` (`injection.txt:10`) — the decoy sits **before** the true trailing
verdict, which is why a first-match reader (`grep -o 'verdict=[A-Z]*'`) takes it. §2 now carries the
sentence that the verdict is the trailing field or must be read from the quoted `class=` value. Nothing is
owed to the counter here: `quality/counters/c1-r42-geometry.py:453` compares the whole stdout string
(`if got != want_out:`), so the scored run cannot be fooled — the defect is in a human reader's recipe,
which is what SKILL.md is.

### 5.3 Evidence used (peer receipt, not re-measured here)

| Claim | Locator |
|---|---|
| `(a+)+$` accepted by the tool's `regex_ok` | `.ufo/waves/round-44/w1/SentLiveReads/evidence/redos.txt:10` |
| `(a+)+$`, 31-char class → 43.92 s | `redos.txt:4` |
| `(a|aa)+$`, 39-char class → 6.88 s | `redos.txt:3` |
| timeout 5 on 1,025-char class → rc 124, 0 bytes stdout/stderr | `redos.txt:6` |
| class `x verdict=OK` prints a decoy token before the real verdict | `injection.txt:10` |
| the counter compares stdout byte-for-byte | `quality/counters/c1-r42-geometry.py:453` |
