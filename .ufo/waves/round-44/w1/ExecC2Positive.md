# ExecC2Positive — C2 positive control (round 44, w1)

## Result

A complete, honest C2 entry built from the five pre-wave pins is **admitted**:

```
PRED-C2-r44 hyprland-gkeep-size-request-r44.md clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1
PRED-C2-r44: admitted=1/1 verdict=TARGET_MET rev=35bcd576a031651b80036b6b240b5207a10e3b1c
```

Fixture commit `35bcd576a031651b80036b6b240b5207a10e3b1c`, tree `76fc56095b0e1ac54a08431d8e8574d010f46443`, on top of the v2 freeze
`e2289516a9a857f55cda7be635933e89b931c3da`, base `6a1a90528fe533cadee506a9fa3e9d13d15cc41f`. The commit lives only in a throwaway shared clone under
`/fast/scratch/hyaku/mado-r44/ExecC2Positive/` (now deleted); what is retained is in this seat directory.

Scoring command (exact, run from `/home/vgpnk/Projects/shokunin/mado-shokunin`):

```
python3 -I quality/counters/c2-r44-gkeep-size-request.py --repo <fixture> --rev HEAD --base 6a1a90528fe533cadee506a9fa3e9d13d15cc41f
```

Retained evidence (all inside this seat dir):

| path | what it is |
|---|---|
| `positive/corpus/knowledge/hyprland-gkeep-size-request-r44.md` | the entry (65 lines, 9,347 B) |
| `positive/corpus/SOURCES.md` | registry with S164 used-by extended and S298-S301 appended |
| `positive/corpus/lessons/round-44.md` | lesson with `## Gate`: five GATE lines, one ADMIT, one REFUSE |
| `positive/corpus/README.md` | one column-zero index row for the entry |
| `make-positive.sh` | rebuilds the commit from `positive/` at the freeze rev; prints fixture, tree and the counter run |
| `receipts/score-positive.txt` | full counter output of the fixture |
| `receipts/diff-stat.txt` | `git diff --stat e2289516..HEAD` = 4 files, 85 insertions, 1 deletion |
| `receipts/changes.patch` | `git format-patch -1` of the whole commit |
| `receipts/quote-validation.txt` | per-quote `quote_at`/`occurrences`/`quote_in_code`/cross-receipt output and the counter's own census |
| `receipts/ablations.txt` | five single-mutation variants, each failing exactly the clauses the mutation attacks |
| `receipts/rebuild.out` | `make-positive.sh` run: different commit id, tree `76fc5609…` identical to the fixture |
| `receipts/fixture-commit.txt` | commit and tree hash of the scored fixture |

`make-positive.sh` guards the run-6 incident: it clones the lane `--shared` into an explicit `DEST`, checks `git -C "$DEST" rev-parse --show-toplevel`
equals `realpath "$DEST"` before any commit, and sets the throwaway identity with `-c user.name/-c user.email` on the commit command only. A rebuild
reproduces the same tree (commit ids differ by timestamp).

## What the control contains

- **Entry**: header inside the first 11 raw lines (`source:` x5 for S164/S298/S299/S300/S301, `verified-at: 2026-10-26`, `recheck: 30d`, `ground`,
  `Lane`, `assimilated-from`), then §1 the compositor's report path (`sendWindowSize`, `realToReportSize`, the pending-serial list, `onAck`,
  `getReportedSize`), §2 the xdg configure and its serial, §3 what xdg-shell 1.49 permits (the size is a hint; zero means the client decides),
  §4 what GTK 4.24.1 does (configured size plus shadow margins, constrained; zero configure falls back to geometry), §5 what gkeep declares
  (`set_default_size(420, 500)`, application id, no `set_size_request`), §6 the two census lines, §7 what is not established.
- **Claim lines**: exactly one id-bearing line per cited id, each carrying that id's Gate quote and the counter's computed locator —
  `Hyprland-Window.cpp:1750`, `Hyprland-XDGShell.cpp:354`, `xdg-shell.xml:1150`, `gdktoplevel-wayland.c:518`, `gkeep-ui.py:476`.
  Every other prose line that touches the mechanism uses a bare locator and no S id, so `all_body_lines_bound` holds by construction.
- **Registry**: S164 kept with cells 1-9 byte-equal, used-by extended by the entry; S298-S301 new, 11 cells each, `mined`, opened `2026-10-26`,
  recheck `30d`, locations unique, Hyprland locations under the pinned `efb5099…` raw URL, last path component and receipt name mutually
  containing (checked for all four: `xdgshell.cpp` in `hyprland-xdshell.cpp`; `xdg-shell.xml` = `xdg-shell.xml`; `gdktoplevel-wayland.c` =
  `gdktoplevel-wayland.c`; `ui.py` in `gkeep-ui.py`).
- **Gate**: five lines with the pin sha256 (`d735d454…`, `d90b534c…`, `7ba7f9c8…`, `0ee38458…`, `07a3c4a5…`), an `ADMIT` of
  `gkeep-client-size-request-r12.md` as the entry, and a `REFUSE` of `gkeep-geometry-never-recorded-r15.md` with the flip word `until`.
  `gkeep-size-to-real-size-r11.md` is not touched, per the freeze.
- **Census**: `gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep` and
  `hyprland sendWindowSize xdg_setSize=1 x11_configure=1`, byte-identical to what the counter recomputes from the pinned bytes.

## Clause failures hit

**None at the entry.** The first scored commit was already `admitted=1/1`. I avoided guesswork by validating every Gate quote against the
counter's own functions before writing (`quote_at`, `occurrences`, `quote_in_code`, `norm_receipt`, `host_census`), which caught three designs
before they became commits:

1. `xdg-shell.xml` "If the client receives multiple configure events before it can respond to one" occurs **twice** in that pin (lines 571-572
   and 614-615), so `occurrences` would have been 2 (clause d). Replaced with the 22-word hint sentence at line 1150.
2. gkeep's `window.set_default_size(420, 500)` alone is a 2-word quote (clause d needs >= 3). A first replacement spanning the
   `Gtk.ApplicationWindow(application=self, title="gkeep")` line scored but put an embedded `"` inside `quote="…"` in the Gate line; the counter's
   greedy `GATE_RE` accepts it, but any verifier splitting on the first closing quote would truncate. Final quote is
   `window.set_default_size(420, 500) self.board = Board(window)` (5 words, line 476, no embedded quote).
3. The `Hyprland-Window.cpp` quote has to span the four source lines of the send branch to reach 3 words and stay unique; the counter locates it
   at its start line, so the entry cites `Hyprland-Window.cpp:1750`.

One defect was in **my own probe harness**, not the counter: an early cross-receipt check compared a quote against its own receipt (`q2` vs
`blobs[n2]`), so it reported every quote as appearing in every receipt. The counter's own loop compares quote-of-i against receipt-of-j with
`j != i` and is correct; re-run with the right pairing, `other_receipts=[]` for all five (`receipts/quote-validation.txt`).

## Ablations (evidence that the nine clauses are load-bearing on this control, `receipts/ablations.txt`)

| mutation of the fixture | clause that drops | verdict |
|---|---|---|
| delete the two census lines | `h:0` | MISSED |
| S299 locator `xdg-shell.xml:1150` -> `:1151` | `g:0` | MISSED |
| delete the README index row | `f:0` | MISSED |
| point S298's used-by at the old path alone | `c:0` | MISSED |
| mutate one word of S300's Gate quote | `d:0`, and `g:0`/`i:0` (the id loses its receipt, so `PINS <= used` breaks) | MISSED |

These are deliberate probes of the instrument, not failures of the control; the control itself was at 1/1 before and after each.

## Risks, residuals, and what the L1 should know

- **Held row S164**: clause c compares cells 1-9 to the row at base `6a1a905…`. My fixture only appends to cell 11. If the L1's data commit
  regenerates or renumbers rows before landing this entry, that comparison is the first thing to break.
- **Honesty boundary**: this is a real entry, not a scaffold. Every OBS claim is a quote plus a computed locator, or a sentence with a line range
  I read; every INF claim is marked INF and rests on those reads. The residuals of PRED-C2-r44 still apply: quote-to-claim binding is a non-author
  reading, and the census lines are bookkeeping of pinned bytes, not of behaviour. No live gkeep window was observed and none is claimed.
- **Not established (stated in the entry §7)**: the size the client actually applied never returns to the compositor; `getReportedSize()` has no
  caller inside the pinned `Window.cpp`; the X11 configure branch is read, not exercised (gkeep is a Wayland GTK app here).
- **Reuse as data entry**: because the control is the honest entry, the L1 can land these four files as the round-44 C2 data commit as well as
  keeping a copy as control P. If it lands as data, S298-S301 are the ids the freeze provisionally assigned; if the data commit renumbers them,
  `positive/` and `make-positive.sh` must be updated with the entry.
- **make-positive.sh** writes only inside its `DEST` argument (default under `/fast/scratch/hyaku/mado-r44/ExecC2Positive/rebuild`), never in the
  lane; it runs the frozen counter read-only.
- **Tool installs**: none. Only `git` and `python3` were used; no pacman transaction, no compositor interaction, no service started.
- **Scratch**: `/fast/scratch/hyaku/mado-r44/ExecC2Positive/` (clone, variant trees, probe/build authors) deleted after the receipts were copied
  here; no evidence is cited from a scratch path.
