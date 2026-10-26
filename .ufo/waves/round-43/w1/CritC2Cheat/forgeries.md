# Forgeries against PRED-C2-r43 — what the frozen counter admits although the claim is not grounded

Seat `CritC2Cheat`, round 43, w1. Deliverable of the ticket "Forgeries against C2".
Counter under test: `quality/counters/c2-r43-gkeep-entry.py`, sha256
`4b5751fe7010400a5a7e4132dafc3f297132d443f2389a61f0b89032c669016c` (printed by
`run-probes.log:1`); `git status --porcelain` over `quality/counters`, `.ufo/waves/round-43/ctl`,
`.ufo/waves/round-43/fetch`, `registration.md` is empty after all runs — the counter, the controls,
the pins and the freeze were not edited. Registration
`.ufo/waves/round-43/registration.md` (freeze `b2e2efd`), base `a35cfdf`.

**Result: 16 forged entry+registry+lesson sets score `admitted=1/1 verdict=TARGET_MET` (exit 0)
under the frozen counter** (`run-forgeries.log`, `run-more.log`). One deliberately negative
control is rejected (`B2`, clause g), which shows the counter is not merely blind. Seven of the
sixteen are closable inside the counter with a check that control P still passes; I verified each
such tightening on a scratch copy (`probes/`, `probes.py`, `run-probes.log`). The rest need a
non-author reading of the claim (the declared residual) or a decision about the genuine fixture.

## 0. Method

* Every fixture is built from the frozen controls' own helpers (`base_files`, `admitted`, `row`,
  `gate_line`, `commit_all` in `.ufo/waves/round-43/ctl/run-c2-controls.py`), so a forgery differs
  from control P exactly where its section says. Each fixture is `git -C "$D" init -q` in
  `/fast/scratch/hyaku/mado-r43/CritC2Cheat`, with `git -C "$D" rev-parse --show-toplevel == $D`
  asserted before the first commit (`forge.py:run`). Receipts used are the real pre-wave pins in
  `.ufo/waves/round-43/fetch/`, so clause d's PINS binding is satisfied *honestly*: every quote in
  every forgery below is a real quote at its real, counter-computed line in a real pinned receipt.
* Control P is re-built and re-scored first in every batch: `admitted=1/1`
  (`run-forgeries.log`, `run-more.log`, `run-probes.log`).
* The forged fixture files are kept under `fixtures/<tag>/` (entry, `corpus/SOURCES.md`,
  `corpus/lessons/round-43.md`, `corpus/README.md`); the verdicts are in `run-forgeries.log`
  (A–H), `run-more.log` (X1–X3) and `run-probes.log`/`run-more.log` (tightenings).
* The counter was never edited. Probes are string-patched **copies** written under scratch and
  copied to `probes/` (`receipts-probes-sha256.txt`).

## 1. Results

| tag | forgery | frozen counter | clause that should have caught it | class |
|---|---|---|---|---|
| A1 | real quote, unsupported claim on the citing line | admitted | g | residual |
| A2 | claim contradicted by the census the counter itself computes | admitted | g, h | residual |
| B1 | quote true for 4 occurrences, claim about another occurrence | admitted | d, g | mechanical |
| B2 | locator names the *second* occurrence (negative control) | rejected (g:0) | g | already covered |
| C1 | quote from a `// TODO` comment, cited as code behaviour | admitted | d | mechanical |
| C2 | quote from a duplicated comment | admitted | d | mechanical |
| D1 | census lines true, the claim they are made to support is false | admitted | h | residual |
| E1 | id cited on one line, contradicted on a second line that names it | admitted | g | mechanical |
| E2 | same contradiction, phrased without the id | admitted | g | residual |
| F1 | ADMIT/REFUSE name the right basename in a directory that does not exist | admitted | i | mechanical |
| F2 | REFUSE carries no flip condition (four distinct words) | admitted | i | mechanical (marker) |
| G1 | registry location is a non-existent URL path | admitted | e | tradeoff |
| G2 | registry location is a relative path that does not exist | admitted | e | tradeoff |
| H1 | entry asserts the opposite of the theme, claims nothing | admitted | b, g | residual (widened) |
| X1 | README index row says the entry was REMOVED | admitted | f | mechanical-lite |
| X2 | localized-channel marker in the entry prose (PROVINCE) | admitted | i (scope) | mechanical |
| X3 | entry cites only the three own-work receipts, no Hyprland source | admitted | b, c, d | mechanical |

"Mechanical" = closable by a check inside the counter that control P still passes.
"Residual" = needs a non-author reading of the claim, i.e. the counter's declared residual at
`quality/counters/c2-r43-gkeep-entry.py:81-84` ("a real receipt can be cited for a claim it does
not support"). "Tradeoff" = closable in principle, but the check rejects control P, so the fixture,
not the counter, must change first.

## 2. Per forgery

### A1 — a real quote cited for a claim it does not support (residual)

Fixture `fixtures/A1-unsupported-claim/`, the S291 line becomes

```
**OBS** S291 the compositor applies every rule size to the live client at once, and the client
never resizes itself again (static_.size = expr;, Hyprland-WindowRuleApplicator.cpp:426).
```

Gate quote and locator are unchanged and true (`static_.size = expr;` *is* at line 426). The added
sentence is unsupported by that assignment, and by the cited file's floating branch: S294's
`m_window->setBox(m_box.logicalBox)` is where the target applies a box. Verdict:
`### A1-unsupported-claim rc=0 admitted=1/1` (`run-forgeries.log`).

Clause g is the one that reads as if it covers this (`:54` "per cited id, one entry line …
carries its Gate quote"), but its implementation at `:490` is
`hit = any(re.search(r"\b%s\b" % i, l) and q in l and …)` — presence of the quote and the locator
on a line that names the id. The claim's words are never read. This is exactly the declared
residual; nothing to fix in the counter, everything to check in the non-author closure.

### A2 — the counter computes facts that contradict the claim and does not use them (residual, sharpest)

Fixture `fixtures/A2-census-contradiction/`:

```
**OBS** S298 the only gkeep client is mapped, floating and reports the rule size
("mapped": true, "class": "chromium", "floating": false,, host-clients-r43.json:49).
```

The quote is a real chromium object (`.ufo/waves/round-43/fetch/host-clients-r43.json:49`), and the
census clause h computes, on the same revision, `host clients total=4 floating=0 gkeep=0`
(`quality/counters/c2-r43-gkeep-entry.py:283` `host_census`). The entry's claim that a *gkeep*
client is floating is therefore false against the counter's own arithmetic, and the counter still
prints `admitted=1/1`. The quote's own text names `"class": "chromium"`.

Classification: residual, not mechanical. A phrase-conditioned guard ("if the line citing the
clients receipt contains the token `gkeep`, the quoted class must fullmatch RX") would pass P (P's
S298 line carries no such token) and kill this fixture, but it is a word list over claim prose, in
the same family as BAD_LOC — I do not recommend it as a fix; it re-invites the round-41 "quote
length" arms race. The real fix is a fixed-form conclusion line computed by clause h (e.g.
`host census gkeep=<G>` as a required entry line, rejected iff `<G>` ≠ the parser's G), which P
does not carry, so it is a v2 fixture change, not a counter-only tightening.

### B1 — a quote true for four sites, cited for a claim about another site (mechanical)

The size-rule branch is `WINDOW_RULE_EFFECT_SIZE` at `Hyprland-WindowRuleApplicator.cpp:422`
(`static_.size = expr;` is at 426). The expression line
`const auto& expr = std::get<Math::SExpressionVec2>(value);` occurs at 174 (MAX_SIZE), 203
(MIN_SIZE), 414 (MOVE) and 422 (SIZE). Fixture `fixtures/B1-second-occurrence/` uses that line as
the S291 gate quote and writes

```
**OBS** S291 const auto& expr = … - the size rule stores this expression as static_.size
(Hyprland-WindowRuleApplicator.cpp:174).
```

Verdict `admitted=1/1`, and the counter prints `clause=g id=S291 obs=1 locator_line=174`. The
locator is true for *an* occurrence and the claim is about line 422. `quote_at` returns the first
word-bounded occurrence, so the counter forces `:174` — a forger just takes the forced line and
makes the claim about the real site.

B2 is the same fixture with the honest-looking `:414` locator; the counter rejects it
(`### B2-second-locator-negative rc=1 … clauses=… g:0`) — i.e. the "second occurrence locator" is
covered but the ambiguity it creates is not.

Tightening (probe `probes/c2-probe-unique-occurrence.py`, patch at `:427`): require exactly one
word-bounded occurrence of the Gate quote in its receipt. All ten control-P quotes occur exactly
once in their receipts (verified independently of the counter, `line_of` + a raw occurrence scan),
so P stays `admitted=1/1`; B1 becomes `d:0 … g:0` (`run-probes.log`).

### C1, C2 — a quote from a comment, cited as behaviour (mechanical)

C1 (`fixtures/C1-comment-quote/`) uses
`// TODO: not very OOP, is it? — Hyprland-DefaultFloatingAlgorithm.cpp:105` as the S292 quote and
claims "the floating algorithm leaves the size to the client; no size path exists". The line is a
comment in the file whose real size path is `windowGeometry.w = COMPUTED->x;` (S292's genuine
quote, line 60). C2 (`fixtures/C2-comment-quote-dup/`) uses
`// Reserved area must be updated before this is called`
(`Hyprland-WindowTarget.cpp:102` and `:126`) as the S294 quote, claiming the target "defers every
box until the reserved area is refreshed" — the opposite reading of the same sentence. Both:
`admitted=1/1` (`run-forgeries.log`).

Clause d at `:427` accepts any word-bounded occurrence in the receipt's raw text; comments are text.

Tightening (probe `probes/c2-probe-quote-not-in-comment.py`): strip comments by extension
(`/* */` and `//` for `.cpp/.hpp/.h/.cc`, `#` for `.py/.conf`) before the occurrence test. P stays
`1/1` — every control-P quote survives its own file's comment stripping, including the two-line
S299 quote `window.set_default_size(420, 500) self.board = Board(window)` and the C++ string
literal `"size": [{}, {}],` at `Hyprland-HyprCtl.cpp:395`. C1 becomes `d:0 … g:0`.

Caveat, stated as a cost: comment stripping is a per-extension heuristic (the counter's `kind`
cell is `code`/`docs`/`own-work`, not a language), and a quote inside a C++ string literal that
contains `//` would be truncated by the naive strip. That is why the probe strips per line and
accepts the quote if it survives *anywhere* in the stripped text; a v2 may prefer an explicit
language cell per row.

### D1 — census lines that are true but irrelevant (residual)

Fixture `fixtures/D1-census-irrelevant/` leaves the three census lines byte-exact (they must match
the parsers' output) and adds above them:

```
The census below proves the applied geometry: the single gkeep client is floating and reports
420x500, so the rule size is the rendered size.
```

Observed `admitted=1/1`. Clause h checks the three lines against its own parsers and nothing about
what the entry concludes from them; the same three lines are in P, so no P-safe discriminator
exists. Residual. The only mechanical half-measure is positional (require the three lines to be
contiguous and to follow the last OBS line, which P satisfies); it is cosmetic — a false conclusion
can sit directly above contiguous census lines. Do not count it as a fix.

### E1, E2 — one id cited and contradicted (mechanical / residual split)

E1 (`fixtures/E1-id-contradiction/`) appends to P's entry:

```
**NOTE** S291 is unrelated to the size path: no rule ever writes static_.size.
```

`admitted=1/1`: clause g only needs *one* line per id (the `any(...)` at `:490`), and a second line
naming S291 with neither quote nor locator is ignored. Tightening (probe
`probes/c2-probe-every-naming-line-bound.py`, patch at `cl["g"] = int(g_ok)`): every unfenced body
line naming a cited id must carry that id's Gate quote and computed locator, header `source:` lines
exempt. P stays `1/1` (its body names ids only on the OBS lines); E1 becomes `g:0`.

E2 (`fixtures/E2-anonymous-contradiction/`) says the same without naming S291; still admitted, still
admitted under the probe. Residual — the assertion is about the source but does not cite it, and
nothing forces a contradiction to carry an id.

### F1 — ADMIT/REFUSE name the right basename in a directory that does not exist (mechanical)

`fixtures/F1-fake-package-dir/corpus/lessons/round-43.md`:

```
ADMIT merge/mado/not-a-real-dir/gkeep-size-to-real-size-r11.md as corpus/knowledge/hyprland-gkeep-geometry-r43.md
REFUSE merge/mado/not-a-real-dir/gkeep-geometry-unobservable-r8.md reason=superseded by …
```

`admitted=1/1`. The check is `staged_ok = lambda p: os.path.basename(p) in STAGED` at `:503` — the
directory is never looked at, and the counter has no access to the staged package anyway (it reads
only the lane repo). The real theme lives at
`/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/<name>.md` (verified by
`verify.py`); the forged path does not exist (same script).

Tightening (probe `probes/c2-probe-package-path-exact.py`): require
`p == "merge/mado/knowledge/corpus/knowledge/" + basename(p)`. P uses exactly that prefix
(`run-c2-controls.py:28-29`), so P stays `1/1`; F1 becomes `i:0`. This is the cheapest fix in the
report: a constant, no new data, and it makes the §2b "the only paths an ADMIT/REFUSE may name"
comment true.

### F2 — REFUSE with no flip condition (mechanical via a marker list)

Fixture `fixtures/F2-refuse-no-flip/`:
`REFUSE …/gkeep-geometry-unobservable-r8.md reason=this refusal says nothing else`.
`admitted=1/1` — clause i requires `len(set(reason.lower().split())) >= 4` (`:506`) and P's own
reason happens to have 16 distinct words. The registration requires a **flip condition**; nothing
scores it.

Tightening (probe `probes/c2-probe2-refuse-flip-marker.py`): the reason must contain one of
`superseded|until|unless|once|when|if|after`. P contains `superseded` (its reason begins
"superseded by the source chain …"), so P stays `1/1`; F2 becomes `i:0`. This is a vocabulary
heuristic of the BAD_LOC kind: it raises the cost, it does not certify a flip condition. A v2 that
wants the real thing should require a fixed-form `flip=` cell.

### G1, G2 — the registry location is decoration, in P as well (tradeoff)

G1 sets S293's location to `https://example.invalid/nope/Hyprland-Target.cpp`; G2 sets S292's to
`nowhere/DefaultFloatingAlgorithm.cpp`. Both `admitted=1/1`. Clause e only compares the location's
last path component with the receipt's file name and checks uniqueness (`:452-468`, `comp = re.split` at `:455`); no host, no
scheme, no commit, no path is checked.

The decisive evidence is not the forgery but control P: **all seven code rows of P carry
`https://example.org/...` locations** (`run-c2-controls.py:38-49`), a reserved documentation domain,
while the registration records the true origin as
`https://raw.githubusercontent.com/hyprwm/Hyprland/v0.56.2/<path>` at commit
`efb50993780079460b0cbed1363e2166a2de1d9f`. So in the only admitted positive fixture, the
provenance field is fabricated by construction — admission can never mean "the location is real".

Probe `probes/c2-probe-url-exac.py` shows why the counter cannot fix this alone: requiring the
Hyprland rows' location to start with
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb5099…/` rejects **control P** (`e:0`,
`admitted=0/1`). This is a tradeoff for the canonical judge, not a seat-level patch: either the v2
fixture carries true raw URLs (and clause e can demand them, per-receipt, from a pin table), or the
location cell is declared decorative and the pins' bytes are the whole trust root — in which case
C2's "sourced" is a statement about bytes, not about a citable URL, and the entry prose must not
pretend otherwise.

### H1 — nothing requires the entry to make a claim (residual, wider than declared)

P's own entry is header + eleven `**OBS** <id> <quote> (<file>:<line>).` lines + the three census
lines (`fixtures/P-genuine/corpus/knowledge/hyprland-gkeep-geometry-r43.md`); it contains no
sentence about the floating algorithm, the target chain or the client request. H1 adds
`Nothing here is determined by the sources below; the compositor picks the size on its own.` and is
still `admitted=1/1`.

The declared residual (`:82`) assumes a claim exists to be mis-cited. The counter as frozen admits
an entry with **no claim at all**, and P is that entry. A non-author closure reading P has nothing
to falsify except the shape of the file. So the residual understates the hole: what clause g
certifies is "eleven quotations, each at a true locator", never "an assimilation of the gkeep theme
end to end". Closing it needs a content requirement (claims in a fixed form, or a required
conclusion section), which P cannot bear — v2, not a counter patch.

### X1 — index row that says the entry was removed (mechanical-lite)

`fixtures/X1-index-row-lie/corpus/README.md` row becomes
``| `knowledge/hyprland-gkeep-geometry-r43.md` | REMOVED, superseded, do not read |``; admitted.
Clause f matches only the row prefix (`:499-500`). A fix needs a grammar for the second cell
(`new|updated`); P uses `new`, so the check is P-safe, but the vocabulary is a design choice, not a
derivation — report it, do not smuggle it in.

### X2 — PROVINCE marker in the entry prose (mechanical)

`fixtures/X2-localized-in-entry/…-r43.md` appends `资料：中文文档频道解释了这个尺寸。`; admitted.
BAD_LOC is applied only to cited registry rows (`:511-513` `row_text = " ".join(rows[0]).lower()`),
never to the entry. PROVINCE excludes the localized documentation channel, so the entry prose is
inside the province rule's reach and outside the counter's. Tightening (probe
`probes/c2-probe2-bad-loc.py`): scan the entry's unfenced lines with the same BAD_LOC list. P stays
`1/1`; X2 becomes `i:0`.

### X3 — no source chain at all (mechanical, and it is the coverage claim itself)

`more.py:four_source()` builds an entry that cites only `S050` (held) + `S297`, `S298`, `S299` (the
three own-work receipts) and omits all seven Hyprland receipts; registry rows, gates and OBS lines
are consistent. `admitted=1/1`. Clause b asks for `>= 4 distinct source:` lines (`:25`), clause c
for `>= 3` new ids — the three own-work rows satisfy both; nothing requires the seven pinned code
receipts, although PINS already enumerates them and the claim's text is "what determines the size …
end to end".

Tightening (probe `probes/c2-probe2-all-pins.py`): require every PINS basename to be the basename of
a cited Gate receipt (`set(PINS) <= used`). P cites all ten, so P stays `1/1`; X3 becomes `i:0`.

## 3. What this means for the claim, and the smallest safe correction

Mechanical holes, each closed by a P-safe tightening I ran (P `1/1`, forgery `0/1`):

1. clause d — quote must occur exactly once, word-bounded (`unique-occurrence`): kills B1.
2. clause d — strip comments per extension before the occurrence test (`quote-not-in-comment`):
   kills C1, C2.
3. clause g — every body line naming a cited id must carry its quote and locator
   (`every-naming-line-bound`): kills E1.
4. clause i — ADMIT/REFUSE path must be `merge/mado/knowledge/corpus/knowledge/<staged>`:
   kills F1. **Cheapest and highest value.**
5. clause i — REFUSE reason must carry a flip marker (`refuse-flip-marker`, vocabulary):
   kills F2.
6. clause i — BAD_LOC over the entry's unfenced lines (`bad-loc-in-entry`): kills X2.
7. clause b/d/i — every PINS basename must be cited (`all-pins-cited`): kills X3.

All seven are string-local patches (probe sources in `probes/`, sha256 in
`receipts-probes-sha256.txt`); none changes the accepted fixture set, so they are the shape of a
`PRED-C2-r42`-equivalent for a v2 that keeps control P as-is.

Residual (needs a non-author reading; the counter cannot do it without a claim grammar):
A1, A2, D1, E2, H1. H1 is the load-bearing one: an entry with no claims is admitted, and control P
is such an entry, so C2 as frozen certifies citation bookkeeping, not the coverage claim. If the
canonical judge is to reject "the theme is covered" on the strength of this predicate, it should
reject it for H1 alone.

Tradeoff (fixture must change before the counter can): G1, G2 — clause e's location cell. A v2 that
wants real provenance must give P true raw URLs; otherwise the cell should be declared decorative
and the claim's "sourced" narrowed to the pinned bytes.

No C2 data exists yet (round 42 never ran a seat; round 43's w1 has no data commit at the time of
this review), so per the registration's `w1` rule these are pre-data holes and the correct route is
re-registration as v2 with a new freeze naming both predicates — not a post-data report.

## 4. Bounds of this review

* Nothing ran against the host session, no compositor read was made, no oracle was started; the
  receipts used are the pins already in `fetch/`.
* The quote-to-claim readings (A1, A2, D1, E2, H1) are mine; the locators, quotes and clause
  verdicts under them are the counter's own output (`run-forgeries.log`).
* HTML receipts, held-id receipts and symlinked receipts are covered by existing controls
  (`N*`/`X*`/`W14`); I did not re-derive them. I did not test a forged *pin* (declared trust root).
* Not tested: whether `hyprctl clients -j`'s `size` is the animation GOAL on this host (a
  compositor fact, outside a read-only seat); the census parsers are exercised only through the
  pinned receipts.
