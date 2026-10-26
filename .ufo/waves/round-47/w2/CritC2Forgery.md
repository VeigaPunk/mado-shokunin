# CritC2Forgery — C2 counter forgery findings (round 47, w2, FALSIFY)

Seat: `CritC2Forgery` (leaf, no subagents). Target: **PRED-C2-r47** — admit an entry that teaches
nothing or lies. All ten forgeries below were built as scratch clones at BASE
`60edb66e2f1cb90acc6e9442fc93ded0ca42d750`, committed, and scored with the frozen counter
`quality/counters/c2-r47-terminal-entry.py`. **Every forgery was admitted (admitted=1/1,
exit 0).** The official positive control (POS) was rebuilt first and admitted, validating the harness
(identical clause profile to `receipts/ctl-c2/ctl-pos.txt`: quotes=8, steps=7, script=1500 lines).

Controls/results receipts: `score-<name>.txt` per forgery and `results.txt` in this seat dir.
Verification script `verify-report.py` passes: every pin locator, quoted span and forgery shape below
is checked by it (run `python3 -I verify-report.py`).

## Setup

- Pins `pins/xdg-terminal-exec-0.14.3/` extracted from the tag tarball
  `https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3`
  (sha256 `82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe`, verified).
  Script bytes sha256 `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` =
  `PIN_SHA["xdg-terminal-exec"]`.
- Real host baseline (print modes only, `XDG_CACHE_HOME` in scratch; no launch, no host write):
  `/usr/bin/xdg-terminal-exec --print-id --print-path --print-cmd` →
  `Alacritty.desktop` / `/home/vgpnk/.local/share/applications/Alacritty.desktop` / `alacritty`
  (copy: `real-host-print-capture.txt`). So on this host the *print* selection is the user override.
- No tools installed (existing python3/git/curl; no pacman/uv/npx channels used).

## Results (all admitted, exit 0)

| forgery | what changed vs POS | admitted | declared residual at registration.md:76-78? |
|---|---|---|---|
| POS (control) | none | yes | — |
| F1 false-mechanism chain | steps 1/5 state reversed preference and first-wins mechanics; same real locators/quotes | yes | yes (clause e counts steps/locators, not truth) |
| F2 comment-quotes chain | behavioral claims anchored only to `#`-comment/doc spans of the script | yes | yes (true quote beside unsupported claim) |
| F3 typed capture | receipt+observed hand-written; observed contradicts the receipt's own echo and the real host capture | yes | yes (capture can be typed; form + digest line checked) |
| F4 README row pointing elsewhere | README index row claims the entry answers the launch half | yes | **no** |
| F5 false row scope | S326-S330 scope cells claim live host measurement; rows are mined docs only | yes | no in registration (docstring residual: "clause c binds URL+digest+name, not the truth of the row's scope sentence") |
| F6 re-claimed held ground | S326-S330 restate held rows S056/S057/S060 scopes under the new census terms | yes | yes (clause i is a term census, not novelty proof) |
| F7a r17 deleted | `terminal-route-r17.md` deleted; entry still cites `terminal-route-r17.md:144-145` | yes | **no** |
| F7b r17 anchor shifted | 6 blank lines inserted before line 144; the [UNK] now sits at :150-151; entry still cites :144-145 | yes | **no** |
| F8 launch-half claim | entry asserts "at launch the user override wins", answering the launch half with a print-mode capture | yes | **no** (closest residual: clause f binds the sentence to a committed capture, not a re-run) |
| F9 provenance lie | head line labels S326 as the man page; the S326 row is the script | yes | **no** |

Scored revisions (scratch clones): POS `d67e8a5a66e084e05af3e4765693431708beb74c`; F1
`343cf612a822ef710af6e3e6950a5ec00838eaff`; F2 `c91848f36e1d5462a13f119c47a745327db0fa11`; F3
`56ce4fe9e9eeb09ee93162fce0d59429ed34d839`; F4 `bddfcd70d0f364f407b386bcdef38e99bbe35f70`; F5
`4f35fd1077f80d24d0d2ba58f3b9fa3364f1129b`; F6 `9f3de76ad7b30196bfc8ba6207757be71eabf0f3`; F7a
`8652ded45d90376b14d353c2b7994cb4fdb420c1`; F7b `338c1fcb0db8ece58bf5541680d31394f016b38a`; F8
`c405af9396257f11b952766d87e7b7a60e250a5b`; F9 `c01ff076e82747853175a0be770fda8db235a556`.

## The six named forgeries

1. **Chain with real lines but false mechanisms (F1).** Step 1 claims config dirs precede the config
   home and the list is read in ascending preference; the pin reads `for xte__dir in
   ${XDG_CONFIG_HOME...` (xdg-terminal-exec:148, before the DIRS loop) and the code comment says
   "descending order of preference" (xdg-terminal-exec:147). Step 5 claims first-found wins; the pin
   says "Entries are checked in ascending order of preference, so use last found if duplicate"
   (xdg-terminal-exec:780). All locators and quotes are genuine; the mechanisms are inverted. Admitted.
2. **Quotes from comments only (F2).** Every behavioral quote cited is a `#` comment or usage-text
   span, not executable code: xdg-terminal-exec:112,147,353,364,565,805. The counter only checks
   verbatim existence at the stated range (clause d). Admitted.
3. **Capture typed by hand (F3).** `live-observed.txt` was typed (no resolver run):
   `WezTerm.desktop` / `/home/vgpnk/.local/share/applications/WezTerm.desktop` / `wezterm`.
   The receipt `live-host.txt` echoes `Alacritty.desktop` (mismatch the counter never compares) and
   the real host print capture shows Alacritty, not WezTerm. The entry states the typed values.
   Admitted.
4. **README row pointing elsewhere (F4).** `corpus/README.md:75` index row describes the entry as
   "The launch decision ... at launch the user override wins", which the entry does not teach (and
   which the lane declares `[UNK]`). Clause g checks three cells, no redirect word, no other
   `knowledge/` file, id coverage — not the row's content. Admitted.
5. **False row scope (F5).** `corpus/SOURCES.md:275-279` scope cells claim "measured live on this
   host"; the rows are mined pins (no host measurement). Clause c binds URL+digest+name, not the
   scope sentence. Admitted.
6. **Re-claimed held ground with renamed terms (F6).** S326-S330 restate held rows S057 (script
   option/lookup code), S056 (README selection contract), S060 (system list) verbatim in scope
   ("restated from held row S057" etc.) while clause i's census terms are present, so the ground is
   "new" only by term census. Admitted.

## Holes outside the declared residuals (v2 candidates)

- **F4** — no declared residual covers the README index row's content; the row can route a reader to
  a claim the entry never makes.
- **F7a/F7b** — clause f requires only that the entry *text* contains `terminal-route-r17.md:144`
  and a receipt path; the counter never opens `corpus/knowledge/terminal-route-r17.md`, never checks
  line 144 exists, and never checks the `[UNK]` is there. An entry can answer a question that has
  moved or vanished, and the counter admits it. Smallest safe correction: clause f should also verify
  at REV that `terminal-route-r17.md` exists and that its line 144-145 still contains the `[UNK]`
  question (byte/pin-bound), else fail.
- **F8** — the entry substitutes the launch half for the selection half: registration.md:16-19 keeps
  the launch half `[UNK]` and scopes C2 to the selection half, but clause f accepts a sentence that
  says "at launch the user override wins" bound to a print-mode capture. Smallest safe correction:
  clause f should require the entry's answer sentence to use the selection/print modality (and
  either not mention launch or keep the launch half `[UNK]`).
- **F9** — no check ties each head `source: S### - <description>` description to its row's actual
  source/kind; a head can label the script as the man page and be admitted. Smallest safe
  correction: clause b should verify each head description names the row's kind/repo (e.g. the
  row's kind cell appears in the description, or the description's URL repo matches the row's URL).

## Reproducible commands

Pins:

    mkdir -p /fast/scratch/hyaku/mado-r47/CritC2Forgery/pins
    curl -fsSL https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3 -o t.tgz
    printf '82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe  t.tgz\n' | sha256sum -c -
    tar -xzf t.tgz -C pins --strip-components=1 --wildcards 'xdg-terminal-exec-0.14.3/*'

Full battery (builds POS + F1-F9, scores each, writes `score-*.txt` + `results.txt`):

    cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/CritC2Forgery
    python3 -I forge.py
    python3 -I verify-report.py

Single forgery (e.g. F7b) from scratch:

    python3 -I -c "import sys;sys.path.insert(0,'.');import forge;print(forge.build_forgery('F7b-r17-anchor-shifted',{'f7b':True})[0])"

Any scored commit can be re-checked directly:

    python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r47-terminal-entry.py \
      --repo /fast/scratch/hyaku/mado-r47/CritC2Forgery/f/F7b-r17-anchor-shifted --rev HEAD

Scratch was deleted after copying receipts into this seat dir (per operator directive).
