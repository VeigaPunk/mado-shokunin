# ScribeProvince draft — round 20 (PROVINCE.md and corpus/README.md)

Base: `e629f73` (sha256 prefixes: PROVINCE.md `1b25bb1e980925b3`, corpus/README.md `c38227ff7339f974`).
Lane: /home/vgpnk/Projects/shokunin/mado-shokunin. Nothing below is applied; L1 integrates.

## 1. PROVINCE.md — no line must change

Reason: the tripwire (`tools/mado-tripwire.py`), its precision suite, the isolation check and
QUALITY criteria 29–30 are lane tooling and corpus text. None is a province surface.
PROVINCE.md `Owns` lists config trees (`~/.config/hypr|waybar|walker|alacritty|…`, themes, idle);
`Refuses` lists secrets, endpoints, quality; neither names tooling. `git show e629f73:PROVINCE.md`
has 0 `tripwire` matches (checked).

## 2. corpus/README.md — no existing line must change

- `## Quality bar` (lines 47–50) points to `QUALITY.md` without a criterion count. Criteria 29–30
  change the count only inside QUALITY.md, so this line stays true.
- Lines 69–76 (`tools/mado-verify.sh --no-live`, standing-use pointers): the gate does not reference
  the tripwire (`git show e629f73:tools/mado-verify.sh | grep -ci tripwire` = 0). Round 20 does not
  touch the gate, so the invocation text stays correct.
- `## Coverage map` rows and `## Frontier` bullets for rounds 1–19: unchanged.

## 3. corpus/README.md — additions for the new note `knowledge/tripwire-precision-r20.md`

The note is drafted by ScribeKnowledge (spec: `corpus/knowledge/tripwire-precision-r20.md`). Its
title and source ids are `S1xx-pending` until L1 assigns SOURCES rows; the two lines below must be
re-checked against the note's final header.

### 3a. Coverage map — insert as a new last row, after line 45 (`knowledge/theme-route-r18.md` row)

Gate for this row: the existing index admits gate and lane-tooling notes (`gate-standing-use.md`,
`gate-mutation-proof.md`, `snapshot-diff-receipt-r9.md`), so a tooling note has precedent here.

```
| `knowledge/tripwire-precision-r20.md` (round 20; lane tooling, no province surface) | Documentary boundary of the transcript tripwire: `observed` versus `lead` evidence markers; git/jj help and dry-run non-writes, with write negatives (`git commit -n` is `--no-verify`); Python builtin and shadowing rules for pure callables. Scan labels are not host behaviour; no command is run to test them. | `source:` S1xx-pending (git help and dry-run, jj help, Python builtins, shlex) in [SOURCES](SOURCES.md); precision suite and counter are lane-local under `.ufo/waves/round-20/`. |
```

### 3b. Frontier — append after line 150 (end of the round-19 bullet), as a new bullet

```
- Round 20 (2026-10-20, repair round; pre-registered at `e629f73`; landed state pending L1
  verification) moves **no province surface**. Its changes are lane tooling: the transcript tripwire
  (`tools/mado-tripwire.py`) and its precision suite, which label each row `observed` (execution
  path stated in the scanned text) or `lead` (literal argv handed to a callee whose body is not
  visible), and which are pre-registered to stop flagging help/dry-run non-writes and provably pure
  containers. [Tripwire boundary](knowledge/tripwire-precision-r20.md) records what a text scan can
  and cannot tell, from `S1xx-pending` sources. A clean scan is not evidence that no command ran; a
  `lead` row is not evidence that one did. The isolation check (routed R19-V4: setup failure must
  abort before any payload) is a QUALITY criterion 29 check in `corpus/QUALITY.md`, not a host probe.
  Still open, unchanged: rendered UI, Waybar module text, Walker socket protocol, dispatcher
  behaviour, per-window rule effects, idle/lock transitions and daemon stop-cause, runtime theme
  application and wallpaper reload.
```

Placement: the bullet sits at the same indentation as the round-19 bullet (`- ` with two-space
continuation). Last existing line 150 ends `re-pin is a pin, not a measurement.`; keep a blank line
before the next section if one is added later.

## 4. Open items for L1

- The 3a row and 3b bullet name `knowledge/tripwire-precision-r20.md`; if ScribeKnowledge retitles the
  note, both must follow. No `S1xx` ids are assigned here.
- The 3b bullet says "pre-registered to stop flagging"; it must be rewritten to "stops flagging" only
  after the C1 counter reports the landed tool clean on the P and H families.
