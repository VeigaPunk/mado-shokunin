# CritC2Cheat - forgeries against PRED-C2-r44 (admitted entries whose claims are not grounded)

Seat: `w1/CritC2Cheat`. Frozen predicate: `quality/counters/c2-r44-gkeep-size-request.py` at
`e2289516a9a857f55cda7be635933e89b931c3da` (base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`). The
counter and every frozen input were read only; the only files this seat wrote are in
`.ufo/waves/round-44/w1/CritC2Cheat/`. No lane file is edited, and the counter is not touched.

## Method

Each fixture is a throwaway shared clone of the lane at the freeze, detached at
`e2289516…`, with one commit adding the C2 entry, four registry rows (S298-S301; S164's used-by
cell extended, cells 1-9 untouched), a `corpus/lessons/round-44.md` with five `GATE` lines and one
`ADMIT`/one `REFUSE`, and a `corpus/README.md` index row. Clone identity was asserted with
`rev-parse --show-toplevel` in every clone; every git call names `-C <clone>`; identity comes from
`-c user.name=fixture -c user.email=fixture@scratch.invalid`. Builders:
`w1/CritC2Cheat/harness.py` (fixtures), `collect.py` (seat-local copies of the committed bytes),
`verify-quotes.py` (locator recomputation, 25 checks, `verify-quotes.txt`: PASS), `tighten.py`
(patched copy `c2-r44-tightened.py` plus patch `tighten.diff`, 64 added lines over 4 hunks).

Score (both counters) - fixture commits are in `w1/CritC2Cheat/fixtures-manifest.md`:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <clone> --rev HEAD --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f
python3 -I .ufo/waves/round-44/w1/CritC2Cheat/c2-r44-tightened.py --repo <clone> --rev HEAD --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f
```

| variant | what the fixture forges | frozen | tightened | class |
|---|---|---|---|---|
| F0-BASE | the L1 draft entry registered on S164+S298-S301 (grounded baseline, not a forgery) | **MET** | **MET** | baseline |
| F1-CLAIM-INVERSION | true GTK quote, inverted claim ("always adopts") | **MET** | **MET** | declared residual (non-author reading) |
| F2-FORGED-PIN | the pinned `Hyprland-Window.cpp` receipt replaced; held S164 carries the forged bytes | **MET** | MISSED | defect, closed by T1 |
| F3-LOCATION-DRIFT | pinned bytes, registry locations moved (1.49→1.48, gkeep commit → all-zero) | **MET** | MISSED | defect, closed by T2 |
| F4-SIZE-REQUEST-PROSE | true census, prose asserts `set_size_request(420, 500)` | **MET** | MISSED | defect, closed by T3 |
| F5-DEFAULT-SIZE-PROSE | true census, prose asserts `set_default_size(800, 600)` | **MET** | MISSED | defect, closed by T3 |
| F6-OVERCLAIM-TABLE | a decision table that answers a protocol question, naming no id | **MET** | **MET** | declared residual (non-author reading) |
| F7-CONTENT-FREE-SHELL | 17-line entry: five bound quotes + the two census lines, no chain | **MET** | **MET** | declared residual (coverage is not measured) |
| F8-REGISTRY-ANCHOR-LIE | registry `scope`/`teaches` cells assert a falsehood; anchor truthful | **MET** | **MET** | residual (cells 4-6 unread); see T4 note |
| F9-REGISTRY-ANCHOR-OUT-OF-RANGE | registry anchor `gdktoplevel-wayland.c:9999-10005` | **MET** | MISSED | defect, closed by T4 |

Frozen receipts: `frozen-<variant>.txt` / `frozen-all.txt`; tightened receipts:
`tight-<variant>.txt` / `tight-all.txt`.

**Read before the rest:** the frozen counter admits 9 of 9 forgery sets and also admits the
grounded baseline. The target is reachable, and it is reachable without the claim's content.

## F0 - the grounded baseline (support, and a positive control the freeze lacks)

The L1 draft `.ufo/waves/round-44/l1-draft/entry.md` (69 lines) registers on S164 (held,
`Hyprland-Window.cpp`) plus S298-S301 (the four remaining pins) and scores `clauses=a:1 b:1 c:1
d:1 e:1 f:1 g:1 h:1 i:1 admitted=1` at commit `b996e119571af6e45bb74c61aae12fc6d0436c47`.
The five Gate quotes recompute to the locators the draft states: `Hyprland-Window.cpp:1687`,
`Hyprland-XDGShell.cpp:455`, `xdg-shell.xml:1150`, `gdktoplevel-wayland.c:681`,
`gkeep-ui.py:475` (quote start; `window.set_default_size(420, 500)` itself sits at
`gkeep-ui.py:476`), and the census recomputes to
`xdg_setSize=1 x11_configure=1` from `sendWindowSize` at `Hyprland-Window.cpp:1732`
(`verify-quotes.txt`). Spot-checked neighbours also land: `Hyprland-Window.cpp:1514`
(`void CWindow::onAck(uint32_t serial) {`), `Hyprland-Window.cpp:1753`
(`m_pendingSizeAcks.emplace_back(...setSize(REPORTSIZE)...)`), `Hyprland-XDGShell.cpp:354`
(`setSize` signature), `gkeep-ui.py:449` (`application_id="org.omarchy.gkeep",`).

Consequence for the freeze text: registration §"Controls (committed receipts at this freeze)"
says "No positive control exists at the freeze". It does: the draft, registered as above, is
MET. That is a positive control for the builder seat, not a counter defect (it is the L1's own
draft, so a second author should still write one).

## F1 - a true quote under a claim it does not support (declared residual)

Lines: `fixtures/F1-CLAIM-INVERSION-entry.md:52` -
`**INF** So GTK 4.24.1 always adopts the configured size exactly: the minimum cannot override it
and the client has no other choice.` The quoted bytes are unchanged and true
(`wayland_surface->next_layout.configured_width = width;` at `gdktoplevel-wayland.c:681`); the
entry's own docstring sentence, which said the opposite, is replaced.

The clause that should have caught it: none. Clause g binds a quote to a *line*; nothing binds a
line's claim to the quote's meaning. This is the residual the counter docstring names ("a real
quote at a true locator can be cited for a claim it does not support"). The tightening I tried
that keeps F0 admitted is none: any lexical contradiction detector I could write for "always"
would also permit "always" in an honestly hedged sentence. **Declared residual (non-author
reading).** Smallest honest correction is procedural: the closure reviewer reads the claim line,
not the counter.

## F2 - the pinned receipt is forgeable for a held id (defect; closes with T1)

Lines: `fixtures/F2-FORGED-PIN-entry.md:30` -
`**OBS** The compositor never notifies an xdg client of a size change: the body of sendWindowSize
holds no setSize and no configure call (Hyprland-Window.cpp:1732), so the census line above is
the whole path.` and `:32` - `hyprland sendWindowSize xdg_setSize=0 x11_configure=0`. The fixture
commit also replaces `.ufo/waves/round-44/fetch/Hyprland-Window.cpp` with a copy whose
`sendWindowSize` body is `;`; the `GATE S164` line carries the forged digest
(`eae97520b3ce2718…`, not the pin `d735d454cc4b7983…`), and the entry cites the held id S164.

The clause that should have caught it: **d**, whose pin check is computed only for new ids -
`quality/counters/c2-r44-gkeep-size-request.py:496-499`:
`pin_ok = True` then `if i in new_ids:` then the digest comparison. S164 is in the base registry,
so `pin_ok` stays `True` and the fabricated bytes are accepted; clause h then recomputes the
census from those same fabricated bytes, so the round-44 census line - the clause the freeze
calls a rebuild - reports the inverse of the pinned fact. The docstring at line 31-32 says the
held receipt "must be byte-equal to be counted by i+", but clause i compares file names only
(`:603`: `used = set(os.path.basename(gates[i][0][0]) for i in receipts)`), so name coverage is
satisfied by the forged file. Implementation and contract text disagree; the implementation is
the weaker one.

Inheritance: the same three-line branch exists at `quality/counters/c2-r43-gkeep-entry-v2.py:490-492`,
`c2-r42-gkeep-entry.py:410-412` and `c2-r41-focus-entry-v2.py:367-369`. Every C2 counter since
round 41 pins new ids only; the exposure is not new in round 44. (The closed rounds are not
re-scored here.)

Smallest safe correction (T1, 4 lines): apply the existing pin test to every cited id.

```python
-            pin_ok = True
-            if i in new_ids:
-                pin_ok = PINS.get(os.path.basename(path)) == digest \
-                    and path == FETCH + os.path.basename(path)
+            pin_ok = PINS.get(os.path.basename(path)) in (None, digest) \
+                and (os.path.basename(path) not in PINS
+                     or path == FETCH + os.path.basename(path))
```

Keeps a genuine entry admitted: F0 stays `TARGET_MET` under the patched counter (tight-F0-BASE,
commit `b996e119…`), because it cites the pin bytes. Closes F2 (`d:0 g:0 h:0 i:0`). A held id may
still cite a *non-pin* receipt; the honest fix for that is "a round-44 entry may cite only the
pinned receipts", which is T1 plus the name test T4 or a PINS-membership rule; I state the
stronger variant rather than smuggling it in: **for a held id in a round-44 entry, the receipt
basename must be in PINS** (no genuine F0 id is excluded).

## F3 - pinned bytes, drifted provenance (defect; closes with T2)

Lines: `fixtures/F3-LOCATION-DRIFT-rows.md:3` - S299's source cell ends
`https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.48/stable/xdg-shell/xdg-shell.xml`
while the receipt is the 1.49 file, and `:5` - S301's cell ends
`https://raw.githubusercontent.com/VeigaPunk/gkeep/0000000000000000000000000000000000000000/gkeep/ui.py`.
Quote, locator, digest and census are all true; only the claim of *which document version* is
false. Clause e compares the last path component of the location with the receipt basename
(`xdg-shell.xml` vs `xdg-shell.xml`; `ui.py` inside `gkeep-ui.py`) and e+ pins only Hyprland
URLs to the commit. So a version- or host-level provenance change is invisible: 1.48, 1.49 and
any future re-cut of the same path are indistinguishable, and so is any other host serving the
same file name.

Smallest safe correction (T2): keep a URL with each pin and require it for pin-named receipts.

```python
PINS_URL = {...five basenames -> the frozen raw URLs from receipts/fetch-sha256.txt...}
    for i in ids:                      # in clause e, before cl["e"]
        ...
        pin_url = PINS_URL.get(os.path.basename(gl_[0][0]))
        if pin_url is not None and pin_url.split("#")[0] != loc_:
            e_ok = False
```

Keeps a genuine entry admitted: F0's four new rows carry exactly the fetched URLs (tight-F0-BASE
MET); closes F3 (`e:0`, both ids printed).

## F4 / F5 - true census lines, prose that contradicts them (defect; closes with T3)

Lines: `fixtures/F4-SIZE-REQUEST-PROSE-entry.md:60` -
`**OBS** gkeep declares 420x500 as a minimum through set_size_request(420, 500), so the configure
of §2 cannot shrink it.` and `fixtures/F5-DEFAULT-SIZE-PROSE-entry.md:60` -
`**OBS** gkeep calls set_default_size(800, 600) before the window is realized.` Both entries keep
the recomputed census lines verbatim at :58 and :32 in both F4 and F5:
`gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and
`hyprland sendWindowSize xdg_setSize=1 x11_configure=1`.

The clause that should have caught it: **h**, which requires the census line to exist exactly once
and recomputes it from the pins, but never checks that any other line agrees with it. The census
is a *quote of a computed fact*; the surrounding entry can deny it in the same breath.

Smallest safe correction (T3, inside clause h, after `entry_lines` is built): a censused number
may not be contradicted by another unfenced line.

```python
if N0 == 0 and re.search(r"set_size_request\s*\(", l):            h_ok = False
for w, h in re.findall(r"set_default_size\(\s*(\d+)\s*,\s*(\d+)\s*\)", l):
    if (w, h) != (W0, H0):                                        h_ok = False
for v in re.findall(r"xdg_setSize=(\d+)", l):
    if int(v) != X0:                                              h_ok = False
for v in re.findall(r"x11_configure=(\d+)", l):
    if int(v) != Y0:                                              h_ok = False
```

(plus the same parse of `census_lines` into W0/H0/N0/X0/Y0). Keeps a genuine entry admitted: F0's
S301 bound line quotes `window.set_default_size(420, 500)` (matching digits) and says "no
`set_size_request` call" without parentheses, so F0 stays MET; closes F4 (`h:0`) and F5 (`h:0`).

## F6 - a decision table that overclaims without naming an id (declared residual)

Lines: `fixtures/F6-OVERCLAIM-TABLE-entry.md:46` -
`| Does a client have to adopt the configured size? | yes, always | OBS |` and `:48` -
`**OBS** No client may differ from the configure; the protocol and GTK agree, so the box
Hyprland sends is the box the client commits.` Neither line carries an id, so clause g's
`all_body_lines_bound` (which forces every id-naming line to carry the quote and locator) does not
apply; the entry's S299 line keeps the hint language verbatim
(`The width and height arguments specify a hint to the window` at `xdg-shell.xml:1150`).

The clause that should have caught it: none - the same gap as F1, with the overclaim moved into a
table so the bound prose stays innocent. **Declared residual (non-author reading).** A regex for
"always"/"must" is a detector of hedging style, not of grounding, and I will not propose one.

## F7 - a 17-line entry reaches the target (declared residual, but the largest hole)

`fixtures/F7-CONTENT-FREE-SHELL-entry.md` is 17 lines: a title, five `source:` lines,
`verified-at`, `recheck`, one line per id carrying its quote and locator, and the two census
lines. It scores `admitted=1` both frozen and tightened. It grounds seven facts (five quoted
lines plus the two censuses) of the roughly twenty the C2 claim names: no ack list, no `onAck`,
no pending-size-ack semantics, no X11 branch prose, no protocol-state reading, no GTK layout
pass, no gkeep widget tree. Everything it says is true; the entry is simply not the coverage the
axis measures.

The clause that should have caught it: none. Clause i+'s pin coverage (all five receipts cited)
is a *breadth* proxy, and a one-line-per-document shell satisfies it. Clause b has no floor on
body length; nothing counts claim lines. Declared as **residual (coverage is not measured)**.
The corrections I considered and reject as unsafe:

- a line-count or word-count floor: defeated by padding (I would have to demonstrate the padded
  variant too, and it would pass);
- another computed census line (for example an `onAck`/`pendingSizeAcks` line from the same
  pinned `Window.cpp`): it is one line of bookkeeping the shell can also carry; it raises the
  floor without measuring content, and it would add a required line the genuine entry does not
  have, so it is not a tightening that keeps a genuine entry admitted — it is a format change;
- requiring each quote to be *load-bearing* (the line's other words must name the quoted
  construct): a lexical approximation that a forger writes to, and one that rejects honest
  summary lines.

If the judge wants a content floor it has to be a different instrument (a per-section required
fact list, or the closure reviewer), not this counter.

## F8 / F9 - registry cell provenance (F8 residual, F9 closes with T4)

F8: `fixtures/F8-REGISTRY-ANCHOR-LIE-rows.md:4` - S300's `scope` cell says
`GTK forbids a client from deviating from the configured size and proves the protocol's size is
mandatory` and `teaches` says `the configured size is mandatory for every client`; the anchor
stays truthful. Admitted: clause c reads cells 1, 7, 8, 9, 10 of a new row (cells 1-9 are only compared
byte-for-byte, and only for an id already in the base registry) and clause e reads cell 1; cells 3
(`tier`), 4 (`scope`), 5 (`anchor`) and 6 (`teaches`) of a new row are never read by PRED-C2-r44. The registry
is the lane's evidence index, so a false `scope`/`teaches` is a provenance defect with no
detector. **Residual (unread cells)**; closing it needs a reading of prose, not a comparison.

F9: `fixtures/F9-REGISTRY-ANCHOR-OUT-OF-RANGE-rows.md:4` - the anchor
`gdktoplevel-wayland.c:9999-10005 @ 4.24.1` while the receipt has 2964 lines. A locator that
cannot exist is machine-detectable. T4 (12 lines, clause e, new ids): the anchor must name the
gated receipt's basename and every range end must stay inside the receipt's line count. F0's
anchors (`Hyprland-XDGShell.cpp:354-455`, `xdg-shell.xml:1144-1161`,
`gdktoplevel-wayland.c:518-544, 633-637, 681`, `gkeep-ui.py:446-488`) are inside their receipts,
so F0 stays MET; F9 goes `e:0` with the printed anchor. This is a new format requirement on the
registry row (an anchor range), so it is an extra-window tightening, not a one-line fix.

## Impacted axes and what I would put in front of the judge

- **coverage (C2)**: 9 of 9 forgery sets are admitted at the freeze. Three are closable now
  without touching the genuine entry (T1 held-id pin digest, T2 pin URL, T3 census/prose
  numbers); one is closable with a new anchor rule (T4). Four are residuals the counter cannot
  close (F1, F6 claim-to-quote; F7 content; F8 unread registry prose).
- **the trust root is shared**: the `if i in new_ids` pin branch is the same at
  `c2-r41-focus-entry-v2.py:367-369`, `c2-r42-gkeep-entry.py:410-412`,
  `c2-r43-gkeep-entry-v2.py:490-492` and this counter's `:496-499`. T1 fixes round 44 only; the
  closed rounds keep the exposure they were scored with.
- **F2 is the one that changes a published fact**: with the pinned `Window.cpp` replaced by a
  held-id receipt, the counter prints and blesses `xdg_setSize=0 x11_configure=0` - the inverse
  of the round-44 claim's central sentence - while every other clause stays green. If the wave
  lands an entry citing S164 without the digest test, a later re-freeze cannot tell the forged
  census from the true one.
- **operability (C1)**: not touched; PRED-C2-r44 reads no tool, and no fixture touched
  `tools/mado-geometry.py`. Registered here only so the separability claim is not overstated.

## Files (all inside this seat's directory)

- `harness.py`, `collect.py`, `tighten.py`, `verify-quotes.py` - builders and checks.
- `fixtures-manifest.md` - the ten fixture commits and entry line counts.
- `fixtures/<VARIANT>-entry.md`, `-rows.md`, `-gates.md` - the committed forged bytes.
- `frozen-<VARIANT>.txt`, `frozen-all.txt` - the frozen counter's per-variant output.
- `c2-r44-tightened.py`, `tighten.diff`, `tight-<VARIANT>.txt`, `tight-all.txt` - T1-T4 and the
  patched scores (F0 MET; F2/F3/F4/F5/F9 MISSED; F1/F6/F7/F8 MET).
- `evidence-lines.txt`, `verify-quotes.txt` - every locator quoted above, recomputed by grep.
