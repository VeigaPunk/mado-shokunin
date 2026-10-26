# LabDupNames — round 46 w1 critic: exactness of `device` block names, and which duplicate gets the suffix

Seat: `.ufo/waves/round-46/w1/LabDupNames`. Claims frozen at `registration.md` (freeze `8c5434c6`, base `b22ea56b`).
Hypothesis under test: *a device block named `foo` never applies to a device named `foo-1`, and names are matched
byte-exactly.* Method: the pinned C++ (`fetch/`), plus an oracle built against the **host's own**
`/usr/lib/libhyprlang.so.0.6.8` (`-lhyprlang`, header sha256 `3d95d168…63b61`, lib sha256 `51f1d29b…1aa927`;
`evidence/build.txt`), plus the frozen C1 counter run on two deliberately wrong tools.

**Verdict: HOLDS**, with two corrections that matter for the entry and for anyone reading a block name as a device
identity. It attacks nothing in C1/C2 as frozen; both adjacent wrong readings I could build (suffix-stripping,
block-prefix) are caught by the frozen counter, the second only by clause g (§4).

## 1. Matching is byte-exact, case-sensitive, with no prefix and no suffix bleed

`device` is a hyprlang *keyed* special category whose key is the `name` value
(`fetch/Hyprland-ConfigManager.cpp:518`, `addSpecialCategory("device", {"name"});`). Both lookups compare the stored
key with `!=` on `std::string` — `fetch/hyprlang-config.cpp:1089` (`sc->name != CAT`, `!= KEY`) and
`…:1117` (`sc->name != category`, `!= key`) — and Hyprland passes the keyboard's `m_hlName` straight in
(`fetch/Hyprland-ConfigManager.cpp:1117`, `getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());`).

Oracle A (`evidence/oracle.cpp`, output `evidence/oracle-out.txt`), one `device { name = foo … }` block, 12 probe keys:

| probe key | stored-key hit | why |
|---|---|---|
| `foo` | yes (`kb_layout=de`, `scroll_factor=0.5`) | the key |
| `foo-1`, `foo-1-1`, `fo`, `foobar` | no | no prefix/suffix matching |
| `Foo`, `FOO` | no | case is bytes |
| `foo␠`, `␠foo`, `foo␉` | no | no trimming at match time |
| `"foo "` (with quotes) | no | see §2 |

`specialCategoryExistsForKey` agrees on every probe (same file, `:1112-1126`). Unicode is bytes too: an NFC key
matches, the NFD spelling and `FÖÖ` do not (`evidence/oracle4-out.txt`).

## 2. The matching is exact; the *inputs* are not normalised symmetrically (correction 1)

The device side is normalised once, at creation: `deviceNameToInternalString` lower-cases and maps space, newline and
comma to `-` (`fetch/Hyprland-MiscFunctions.cpp:777`). The **config key is not normalised at all** — the parser stores
the `name` value verbatim (`evidence/oracle2-out.txt`, cases O/S: stored keys `Logitech MX Keys`, `Foo,Bar`).
Consequences, all measured:

* `device { name = Razer DeathAdder V2 }` can never match: its key keeps the capitals and the spaces. This is already
  modelled: fixture `stale-block` and `bracket-name-with-space` both expect `NO_SUCH_DEVICE`
  (`quality/counters/c1-r46-fixtures.json`), and entry row 7 says the same.
* `deviceConfigExists` replaces `' '` with `'-'` only (`fetch/Hyprland-ConfigManager.cpp:1198`,
  `std::ranges::replace(copy, ' ', '-');`) and does **not** lower-case — and its argument is already the internal
  name, so the replacement is dead; it cannot rescue a `Foo Bar` block.
* Trailing space: an unquoted value is trimmed by the parser, so `name = foo ` and `name = foo` are the same key
  (`foo`). A *distinct* trailing-space key is only reachable by quoting, and then the quotes are part of the key:
  `name = "foo "` stores the six bytes `"foo "` (`evidence/oracle2-out.txt`, case F). Hyprlang does not unquote
  `STRING` values (`kb_layout = "de"` stores `"de"`), so the reference tool's literal-RHS model is right here
  (`evidence/oracle3-out.txt`).
* `#` cuts the value even inside quotes (`name = "foo#bar"` → key `"foo`), matching the contract's comment rule.

## 3. `foo-1` is a real name and a real block target; it names a *slot*, not a unit (correction 2)

`-1` is not a nonce: the compositor mints it. `getNameForNewDevice` (`fetch/Hyprland-InputManager.cpp:2119`) proposes
the internal name, then appends `-N` while the candidate is taken by a **live** HID (`…:2126`,
`while (std::ranges::find_if(m_hids`; `…:2124`, `"-" + std::to_string(dupeno)`). Simulator transcribing that function
and `deviceNameToInternalString` (`evidence/dedup.cpp`, `evidence/dedup-out.txt`):

* **Order of plug decides.** The first live unit with a given internal name keeps the bare name; each later unit takes
  the lowest free suffix *at its own plug* — `foo`, `foo-1`, `foo-2`.
* The search is over live `m_hids` only, and `m_hids` is shared by keyboards, mice and touch devices
  (`…:1138`, `…:1322`, `…:1946`; erased on destroy `…:1532`). A mouse can therefore consume the `foo-1` slot a
  keyboard's name implies.
* Nothing is renamed on unplug: with `foo`+`foo-1` live, unplug `foo` and plug a new identical unit → the **new**
  unit takes `foo` and the old survivor keeps `foo-1`. The block-to-physical-unit binding moves across a replug.
* The suffix is appended to the *proposed* name, so a kernel name that already ends in `-N` collides instead of
  counting: `foo`+`foo-1` live, then a unit named `Foo 1` → `foo-1-1` (not `foo-2`); plug `Foo 1` first and the
  duplicate pair ends up `foo`, `foo-2`, because `foo-1` was taken.
* Case, comma and space fold into one namespace: `FOO` then `foo` → `foo`, `foo-1`; `Foo,Bar`, `Foo Bar` and
  `foo-bar` are three claims on one name. Empty names become `unknown-device`, `unknown-device-1`.
* Virtual keyboards go through the same dedup (`setupKeyboard` → `getNameForNewDevice`, `…:1141`), so a second one
  from the same client is `hl-virtual-keyboard-1`.

The live host already carries four duplicate-suffixed device names — `receipts/live-devices-host-l1.txt:7,13,16,18`
(two keyboards, two mice; names redacted here). Therefore:

* block `foo` → device `foo-1`: **never matches** (oracle A; §1). The hypothesis is true in this direction.
* block `foo-1` → device `foo-1`: **matches exactly** (oracle G/H). So a `-N` block is meaningful config, and it
  binds to whichever unit currently holds the slot — after a replug it can be a unit that used to be `foo`.

## 4. Counterexample attempt: three tools scored on a scratch clone at the freeze commit

I first read the raw fixture JSON as carrying no `-N` device names (the dumps use `{A}`-style placeholders) and
suspected a control hole. The counter resolves the placeholders from `VENDORS × MODELS × SUFFIX` with
`SUFFIX = ["", "", "-keyboard", "-mouse", "-consumer-control", "-keypad", "-1", "-2"]`
(`quality/counters/c1-r46-devices.py:116`), and it keeps the four names of one case free of prefix relations
(`if all(n not in p and p not in n for p in picked)`, `…:124`). Three tools, each the reference with one lookup
patch, same clone base `8c5434c6`, same counter, work dirs under scratch:

| variant | patch | result |
|---|---|---|
| reference (positive control) @ `415a9d6` | none | `fixtures=90/90 generated=150/150 … TARGET_MET` (`evidence/ref-positive-control.txt`) |
| suffix-strip @ `2e066d5` | drop `-\d+$` from dump names before lookups | `fixtures=80/90 generated=121/150 … TARGET_MISSED` (`evidence/variant-suffix-strip.txt`) |
| block-prefix @ `710caf0` | a device resolves to the longest block whose name is its `-`-separated prefix | `fixtures=90/90 generated=129/150 … TARGET_MISSED` (`evidence/variant-prefix.txt`) |

So the claim is achievable at the freeze commit (90/90, 150/150) and both adjacent wrong readings are caught — but by
different clauses. Suffix stripping is caught by f **and** g; the block-is-a-prefix-of-device reading, the direct
violation of this seat's hypothesis, passes **all 90 fixtures** and is caught only by g (21 of 150 cases). Clause g's
oracle is the reference, so a reference-and-tool shared error would be invisible there; this seat's non-author oracle
(§1) is the evidence that the reference's exactness is right, and it agrees. The reference also answers the suffix
case correctly on a hand-built dump (`evidence/ref-suffix-run.txt`: block `foo` vs device `foo-1` → `block=no`,
`NO_SUCH_DEVICE`, `stale=1`; block `foo-1` → `block=yes`, `MATCHED`).

## Impacted axes

* **C1 f/g** — satisfied; additionally strengthened in this session by a positive control at the freeze commit
  (90/90, 150/150) and two near-miss variants (80/90 + 121/150; 90/90 + 129/150). One measured asymmetry: clause f
  alone does **not** separate a block-prefix reading of names; clause g does (21 of 150 cases). No defect.
* **C2 row 7** — supported as written (lower-casing/dash normalisation, exact key compare, product name never
  matches). Optional, not needed for admission: one clause that the `-N` suffix is assigned at plug time and never
  re-assigned on unplug, so a suffixed block names a slot. Sources: `fetch/Hyprland-InputManager.cpp:2119-2131`,
  `:1532`.
* **No axis harmed**; nothing in the claims or counters needs to change for this hypothesis.

## Smallest safe correction

None required: the hypothesis holds, the reference implements it, and the counter separates both adjacent wrong
readings. If a v2 freeze happens for other reasons, two cheap additions would move the exactness plane from clause g
into clause f: (i) one fixture `device { name = foo }` against a dump device `foo-1` (expect `block=no`,
`NO_SUCH_DEVICE`, `stale=1`), the direct case of this hypothesis, which f currently does not contain — measured by the
block-prefix variant passing 90/90; and (ii) that variant itself as a named control. Do not touch the frozen fixtures
or counters now.

## Adjacent harness caveat (not this seat's finding, verified at code level)

Another w1 seat (`SentTool`) reports that C1 clause `r` is a PATH-marker test: the `--selftest` run executes with
`PATH=/usr/bin:/bin` and no fake bin (`quality/counters/c1-r46-devices.py:375`), and any run can exec
`/usr/bin/hyprctl` by absolute path past the fake bin (`env_a`, `…:260-262`), and `hidden_paths()` hides only the repo,
the lane root and its parent (`…:241-243`, `:251-257`) — not `$HOME` or `/run/user/<uid>`, so `--ro-bind / /` leaves the live
compositor socket reachable (a read-only bind does not stop `connect()`). I confirmed those three code facts; the
scored bypasses are their receipts (`.ufo/waves/round-46/w1/SentTool/evidence/clause-r-bypass-*.txt`). It does not
change anything in §1-§4: a clause-`r` hole can only inflate a `TARGET_MET`, and both variants I scored were
`TARGET_MISSED`. It does weaken the registration's evidence that a *scored* tool runs no hyprctl, which a v2 freeze
should fix by masking `/usr/bin/{hyprctl,libinput,journalctl,udevadm}` with the marker fakes and by adding `$HOME`
and `/run/user/<uid>` to `hidden_paths()`.

## 5. What this seat did not do

No `hyprctl`/`libinput`/`journalctl`/`udevadm` run, no host config read or written, no compositor call, no package
transaction, no install. Only `/usr/include/hyprlang.hpp` + `/usr/lib/libhyprlang.so.0.6.8` were linked, and the
reference script was executed read-only. All clones and builds lived under
`/fast/scratch/hyaku/mado-r46/LabDupNames` and were deleted.

## 6. Receipts and reproduction

`evidence/` holds: `oracle.cpp`, `oracle2.cpp`, `oracle3.cpp`, `oracle4.cpp`, `dedup.cpp` and their outputs,
`fixture-scan.txt`, `build.txt` (compiler, header/lib sha256), `make_quotes.py` + `quotes.txt` (locators computed by
grep on `fetch/`, 19 entries, all verified), `ref-suffix-run.txt`, `variant-suffix-strip.txt`,
`ref-positive-control.txt`, plus the synthetic inputs `d1.json`, `t1.conf`, `t2.conf`.

```
# oracle (cwd = scratch)
g++ -std=c++23 -O1 -o oracle  oracle.cpp  -lhyprlang && ./oracle
g++ -std=c++23 -O1 -o oracle2 oracle2.cpp -lhyprlang && ./oracle2
g++ -std=c++23 -O1 -o oracle3 oracle3.cpp -lhyprlang && ./oracle3
g++ -std=c++23 -O1 -o oracle4 oracle4.cpp -lhyprlang && ./oracle4
g++ -std=c++23 -O1 -o dedup   dedup.cpp   && ./dedup

# variant score (scratch clone at the freeze commit, tool patched with _stem())
python3 -I quality/counters/c1-r46-devices.py --repo "$D" --rev HEAD --work "$S/work"
```

Variant patch 1, exactly (three call sites plus the presence set):

```python
def _stem(n):
    return re.sub(r"-\d+$", "", n)
exp, kbfile = expected_names(st, _stem(name))
"yes" if _stem(name) in st.devices else "no"        # x2 (keyboard, mouse)
blk = st.devices.get(_stem(name), {})
present = dump_names(doc) | {_stem(n) for n in dump_names(doc)}
```

Variant patch 2 (block-prefix): add a resolver and use it at the same four places, plus
`ok = name in present or any(n.startswith(name) and n[len(name):].startswith("-") for n in present)`:

```python
def _resolve(st, name):
    if name in st.devices:
        return name
    cand = [k for k in st.devices if k and name.startswith(k) and name[len(k):].startswith("-")]
    return max(cand, key=len) if cand else name
```
