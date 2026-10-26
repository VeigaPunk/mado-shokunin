# Seat ExecHyprlangOracle — report (mado round 46, wave w1)

**Move.** Differential test of the C1 contract (`l1-draft/mado-devices.py`, `parse_config`/`expected_names`) against
the host's real hyprlang 0.6.8, using a C++ oracle that registers what Hyprland 0.56.2 registers and reproduces the
accessors the contract models. Random configs only; nothing in the lane written except this seat dir and this file.

**Files (new, all under `.ufo/waves/round-46/w1/ExecHyprlangOracle/`).**
`oracle.cpp` (the oracle, `g++ -std=c++23 -O2 -lhyprlang`, linked to `/usr/lib/libhyprlang.so.0.6.8`), `gen.py`
(generator), `differ.py` (corpus runner + comparison), `repro.py` (A/B/C receipts), `attribute.py` (B1/B2/unexplained
attribution), `hostcheck.py` (live-receipt cross-check), `fixturescan.py` (read-only scan of the frozen 90),
`verify_quotes.py` (quote verifier), `report.md` (full report, oracle and generator inline), `evidence/*`.

**Behaviour measured.** 16,800 generated configs, 251,959 config lines, 15,215 comparable (the other 1,585 the
reference itself declines); every comparable config compared per device name on the five XKB names, `kb_file`, the
two-decimal scroll factor, block presence and category creation order.

- **Agreement: 15,181 / 15,215 (99.78 %).** Zero divergence on comments/`##`, continuations (incl. trailing spaces
  and the CRLF interaction), CRLF, `[[EMPTY]]`, empty RHS, all four device-line forms, merges and duplicate names,
  creation order, the `us`/empty default chain, `std::stof` prefix semantics, the 0..100 clamp and `-0.00`.
- **Two contract bugs, 34 configs, 8 minimal repros (A1–A9):**
  1. **B1 (26 configs): a key Hyprland does not register, inside a `device` block after a `device[X]:…` line (or
     after `device:name = X`, or after an empty-named block), re-targets the rest of the block to another device**
     — hyprlang keeps `currentSpecialKey` and `currentSpecialCategory` separately (`fetch/hyprlang-config.cpp:297`,
     `:376`, `:438`, `:896`), the reference keeps one `cur`. Both devices then get a wrong expectation and the tool
     prints a false `DIFFER` (exit 1). A real typo (`tap_to_click` instead of `tap-to-click`) is enough (A9).
     Surfaces: five names 21 configs, `kb_file` 4, `scroll_factor` 4.
  2. **B2 (8 configs): a `scroll_factor` literal below `2**-150` (e.g. `1e-50`, `1e-999`) is modelled as `0.0`**,
     while `std::stof` throws `out_of_range` (`fetch/hyprlang-config.cpp:467`) so the key is never set and
     `hyprctl` prints `-1.00`. The reference's guard misses exactly `0 < |literal| < 2**-150`. Result: a false
     `scroll_factor=0.00 reported=-1.00 verdict=DIFFER` on such a pointer.
- **Declined classes (1,585 configs) are all decidable by the parser.** Per class, with the host's actual answer, in
  `evidence/repro.txt` §B: directives, `$var`, `{{ }}`, interior `\`, selector-less `device:k` (creates a block named
  `0`), block-first-not-name (renames the block instead of failing), rename (renames in place), `inf`/`nan`/hex
  (100/`nan`/16/8), flat `device:k` after a bracket line or across a file boundary (applies to the carried-over
  device), `device:name = A` then `device { name = B }` (renames A), continuation before CRLF (literal backslash).
  Coverage loss, not wrong output; two of them contradict the contract's own justification prose.
- **Unsupported share:** 2,255 increments over 251,959 generated lines = **0.89 %**; within the clean grammar
  (224,565 lines) **0.000 %**.
- **Live cross-check:** the oracle and the reference agree on all 14 devices of the lane's own host receipt
  (`evidence/hostcheck.txt`), so the corpus findings are not an artefact of the oracle.

**Effect on the frozen claims.** None on the counters' verdicts: `fixturescan.py` finds no fixture with either
precondition (`evidence/fixturescan.txt`: 0 of 90), and I did not touch counters, fixtures, controls, registration,
reference or pins. The counter's declared residual ("clause g's oracle is the reference") now has a number: 0.22 %
of comparable configs, in two mechanisms. Whether to note that in the registration residual or in the tool docstring
is the L1's call.

**C2 note (routed, not scored).** The entry's sentence "the device block whose name equals the keyboard's name when
that block SETS the key" is falsified by B1's mechanism for files with an unregistered key after a bracket/selector
line; the two selection states (`fetch/hyprlang-config.cpp:297/:376/:438/:896`) are the sourced detail that makes it
true.

**Host safety.** No installs, no `pacman`, no compositor mutation, no Wayland client, no input injection. Compositor
reads: `hyprctl version` only. File reads: pinned `fetch/`, `~/.config/hypr/input.conf`, the lane's own live receipt.
All scratch under `/fast/scratch/hyaku/mado-r46/ExecHyprlangOracle/` (removed at the end); receipts copied into the
seat dir. `g++ 16.2.1`, libhyprlang 0.6.8-5 (`evidence/build.txt`).

**Peer input received here (not acted on).** `SentTool` and `ConnCrossClaim-3` both flagged C1 clause r (absolute-path
and selftest-PATH bypass; `AF_UNIX` to the live socket not blocked) with receipts in
`.ufo/waves/round-46/w1/SentTool/`. Outside this seat's scope; belongs to the L1 / counter author.

**Risks / limits.** The oracle models the config → stored-rules/scroll-factor step, not XKB compilation, the FALLBACK
reset, the virtual-keyboard takeover, `deviceNameToInternalString`, `source =` following or runtime `hyprctl keyword`
drift. The divergence *rate* is a property of my grammar (adversarial, 45 % of cases carry an unregistered key), not
a claim about real-world configs. No blocker.
