# CritOracleClaim — w2 critic: the oracle observation entry §4 cites

Seat: w2 critic, round 43 (hyaku run 8, 2026-10-26). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Item attacked: `corpus/knowledge/hyprland-gkeep-geometry-r43.md:62` (entry §4 INF), at data commit
`1959770657f1f8665097c1aed4be6c1cbb07139f` (entry sha `4d16b3fb…`, identical in the worktree), and the
apparatus it cites, `.ufo/waves/round-43/w1/ExecOracleGkeep/`. Registration v1 and v2 read first; v2
does not touch this item. Full findings with receipt:line citations:
`.ufo/waves/round-43/w2/CritOracleClaim/findings.md`.

## Verdict

The observed numbers and all five control outcomes reproduce exactly from the receipts. Two clauses of
the entry's oracle sentence are stronger than the receipts, and one receipt field is unusable.

| entry §4 clause | verdict |
|---|---|
| "the isolated round-27 oracle" | **OVERSTATED** — the run is an adaptation, not the pinned harness |
| "a Hyprland 0.56.2 nested under tinywl in bubblewrap, never the host session" | SUPPORTED |
| "a client with that app id" | literal SUPPORTED, **under-disclosed** (a shm surrogate that requests no size, not the app) |
| `"size": [420, 500]`, `"floating": true`, under the host's three rules | **SUPPORTED exactly** |
| "with the size line removed **the same client** reported its own 200x200 buffer" | size SUPPORTED; "the same client" **OVERSTATED** |
| "with `size 300 300` it reported 300x300" | SUPPORTED |
| "with the `float on` line removed it was tiled" | SUPPORTED |
| "In that oracle, the rule, not the client, is the origin of 420x500" | SUPPORTED as scoped; cannot repair the host ambiguity the same paragraph raises |

Specifics asked by the assignment:

- **Which compositor, sha?** `/usr/bin/Hyprland`, read-only in bwrap (`--ro-bind /usr /usr`, boot
  `exec Hyprland -c …`). **No sha256 of that binary is recorded**; identity rests on the nested
  server's `hyprctl version -j` (`version 0.56.2`, `tag v0.56.2`, `commit efb5099…`,
  `receipt-headlesshost.json:481-501`) and the instance signature (`:207`, different from the host's
  live `…_1792986098_301483618`). Today's host binary hashes `55da553b…` with the same commit.
- **Host rule file byte-identical?** Yes. `rules-host.conf`, the pin `fetch/host-gkeep.conf` and the
  live `~/.config/hypr/gkeep.conf` are one sha (`3726e488…`), `diff` empty, and the receipt records it
  (`receipt-headlesshost.json:439`). No `exec` line, so the runner's strip is a no-op.
- **Does `clients -j` carry size [420,500] and floating true?** Yes —
  `receipt-headlesshost.json:36-39` (`"size": [420, 500]`), `:21` (`"floating": true`), `:19`
  (`"class": "org.omarchy.gkeep"`); the single-line quote in `20-observation.txt` parses to exactly
  that object; the map line and the client's `TOPLEVEL_CONFIGURE w=420 h=500` are in the receipt.
- **Do the controls show what the entry says?** Yes for every number: `nofloat` [918,498]/false,
  `size300` [300,300]/true, `nomatch` [918,498]/false on class `gkeep2`, `floatonly` [200,200]/true,
  `minsize` [420,500]/true with `CLIENT_MIN_SIZE 800x700` logged. The `at` values follow the centring
  arithmetic on the 960x540 logical output.

## Counterexample (strongest)

The control that licenses "the rule, not the client, is the origin" did not run the same client binary
as the case it explains: `floatonly` used `client_sha a3319a74…`, `headlesshost` used `227cf419…`
(`receipt-headlesshost.json:8` vs `receipt-floatonly.json:8`). Rebuilding the seat's kept
`gkeep-shm.c` with the seat's own command reproduces `a3319a74…`; the headline build's source is not
kept and is not the kept source minus the `--min-size` block (two reconstructions: `b06f3510…`,
`5482381a…`). Behaviour is consistent (both log `buffer=200x200`, no `CLIENT_MIN_SIZE`), so the sizes
stand — the word "same" does not.

Second: the oracle cannot answer the ambiguity §4 states for the app. The surrogate requests no size;
with the rule absent it reports its own 200x200, i.e. a client's own size is what the report carries.
The real app requests 420x500 (`gkeep-ui-excerpt.py:33-34`), so a 420x500 report would not separate
rule from app default. `minsize` does not close this (`set_min_size` is a minimum, and the buffer
stays 200x200).

Two more defects: `clients_repeat_equal: false` on every positive receipt although the parsed
`clients` and `clients_second` are equal (the flag compares raw text with a sorted re-dump — do not
read it as instability); and the seat's own client locator is wrong (`20-observation.txt:24` cites
`gkeep-shm.c:156-164` for app_id/title/attach/commit, which are at 150-151/157/159).

Provenance: entry §4 cites `w1/ExecOracleGkeep/…`, but that path is absent at the data commit
(`git cat-file -e` fails; the seat's 48 files arrive at HEAD `2a3707c`). The evidence is real and
unmodified; the citation is later-dated than the commit that carries it.

## Impacted axes

**Coverage** (C2 entry prose §4 and the lesson ledger) — not the C2 predicate
(`c2-r43-gkeep-entry-v2.py` never reads this seat) and not **operability** (C1 untouched). No axis
harmed; the registration's residual ("an oracle observation … is reported, not scored") means this
must not be used to re-score C2.

## Smallest safe correction

Replace §4's oracle sentence with an explicitly *adapted* layout (rebuilt wlroots, headless output
created on the nested instance, client forced to the nested `WAYLAND_DISPLAY`), name the client as a
purpose-built shm surrogate **that requests no size** and give its sha per case, and end with: "that
shows the rule acting on a client that requests nothing; it does not separate the rule from gkeep's
own `set_default_size(420, 500)`, so a 420x500 report from a real gkeep window remains UNK." Plus:
repair the repeat flag (compare parsed objects), fix the client locator to 150-159, and date the w1
citation to commit `2a3707c`.

## Checks run / not run

Ran: sha/diff of the three rule files, binary and host-version reads (`hyprctl version` only), quote vs
receipt equality, per-case size/floating/class/at over all 11 receipts, repeat-flag vs parsed
equality, round-27 pins vs recorded shas, config-tree handling, C2 counter's references to this seat,
client locator lines, one `gcc -O2` rebuild of the kept client and two minus-`--min-size`
reconstructions in `/fast/scratch/hyaku/mado-r43/CritOracleClaim/` (deleted at seat end).
Not run: no compositor, no host write verb, no package transaction; nothing installed (gcc 16.2.1,
wayland-scanner 1.26.0 reused); nothing written outside `.ufo/waves/round-43/w2/CritOracleClaim/`.

Evidence: `.ufo/waves/round-43/w2/CritOracleClaim/receipts/` — `identity.txt`, `observation.txt`,
`controls-lines.txt`, `client-and-apparatus.txt`, `binary-and-negatives.txt`, `locators.txt`.
