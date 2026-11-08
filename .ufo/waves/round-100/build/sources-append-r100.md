# round 100 w1 - SOURCES row decision and the round lesson's `## Gate` block (R100MScribeEntry draft)

> **Landing status (2026-11-08, this seat's last write).** While this draft was being written the L1
> integrated: `corpus/knowledge/gio-launch-path-default-r100.md` (mtime 02:31:20, an entry of this
> name but a shorter one, sourced to **S533 alone**), `corpus/lessons/round-100.md` (mtime 02:32:09,
> with a `## Gate` block that already carries the admit and the reject this seat was asked to
> draft), and one `corpus/SOURCES.md` change (mtime 02:31:30): **S533's** `used-by` cell, which now
> reads `corpus/knowledge/gio-launch-env-r99.md, corpus/knowledge/gio-launch-path-default-r100.md`.
> The landed registry state was re-measured read-only: `check-sources-readback.py` ->
> `rows=469 entries=121 findings=0`, exit 0; `sources-census.sh validate` -> exit 0, no `E` finding.
>
> **The landed state already implements this draft's section-1 decision** (no new row: the registry
> is still at 469 rows and the last id is still `S534`) **and this draft's section-4 Gate block**
> (the landed lesson's Admit row is S533 re-opened with the `gutils.c:388` quote, and its Reject row
> is the staged `S205` with a flip condition - the same reject this draft names, cited to the same
> sweep).
>
> What is left for the L1 to decide is the **second** append: the landed entry's front matter names
> **S533 only**, so the landed registry is complete for the landed entry. This draft's entry draft
> names S528, S532 and S533 (it cites the load gate's two `g_find_program_for_path` calls and the
> CLI's refusal line), so landing *this* draft as the entry needs the two further `used-by` appends
> of section 2. **Measured**: the landed registry + this draft -> `FINDING R4 S528` and `FINDING R4
> S532` (2 findings, exit 1); the landed registry + this draft + the two appends -> `rows=469
> entries=121 findings=0`, exit 0. The L1 picks: Option A (land this draft, add the two appends) or
> Option B (keep the landed entry, take the additions listed in the entry draft's landing-status
> note).

Target: the L1 lands the entry draft `.ufo/waves/round-100/build/gio-launch-path-default-r100.md` at
`corpus/knowledge/gio-launch-path-default-r100.md`, then applies the registry work below and pastes
the `## Gate` block into `corpus/lessons/round-100.md`. **Nothing in `corpus/` is edited by this
seat**; this file is a draft.

Ground re-measured by this seat (not inherited), 2026-11-08:

| fact | measurement |
|---|---|
| `glib2` | `2.90.1-1` (`pacman -Q glib2`) |
| `/usr/bin/gio` | sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` (equals the L1 pin and the round-99 case-file pin) |
| `gutils.c`, committed round-99 bytes | `.ufo/waves/round-99/fetch/gutils.c`, sha256 `65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771`, 100534 B, 3245 L |
| `gutils.c`, live re-fetch | `curl -sSL -o live-gutils.c -w 'HTTP %{http_code} %{url_effective}' https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c` -> `200 https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c`, sha256 `65086c29...e3771` - byte-identical to the committed bytes |
| `gdesktopappinfo.c` (round-98 fetch) | sha256 `8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d` (equals S528's digest) |
| `gio-tool-launch.c` (round-99 fetch) | sha256 `16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a` (equals S532's digest) |
| registry at the base revision | 469 rows; last id `S534`; `grep -n 'S535' corpus/SOURCES.md` returns nothing (the next free id is `S535`) |
| census, base registry | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` -> exit 0, warnings only (W01/W04), no `E` finding |
| read-back gate, base registry | `python3 -I quality/check-sources-readback.py --repo <lane>` -> `SOURCES_READBACK: rows=469 entries=120 findings=0`, exit 0 |

---

## 1. The row decision: **no new row** - S533 already covers this scope

`grep -n 'S533' corpus/SOURCES.md` (row 485) reads, in the registry's own words:

- **scope:** "the single program lookup all four launch searches call: the working-directory join,
  the absolute-or-slash branch, **the PATH source and its default, the empty PATH entry**, and the
  absolute return";
- **anchor:** "gutils.c:280-281 (the doc sentence), :322-327 (the working-dir join), **:331-357 (the
  absolute/slash branch and the executable-and-not-a-directory test)**, :359-368 (an absolute miss
  returns NULL), **:370-389 (the PATH source and the `/bin:/usr/bin:.` default)**, **:462-500 (the
  entry walk, the empty entry and the relative join)**".

Every `gutils.c` line the round-100 entry cites is already inside S533's declared scope and inside
its anchor: the PATH source (`:371`), the unset guard (`:376`), the `/bin:/usr/bin:.` literal
(`:388`), the absolute-or-slash short-circuit (`:332-357`), the empty-entry rule (`:471-477`), the
working-directory join (`:480-484`) and the cwd join (`:490-497`). S533's `teaches` cell already
carries the branch's meaning: "one lookup, four callers ... and the working directory changes what
a relative name means".

Four independent reasons the registry gains no row this round:

1. **The scope is held, not absent.** A new row for a *subset* of a held row's scope restates the
   held row in a second place. The registry's mechanism for "this entry cites ground a row already
   holds" is the `used-by` cell - 157 rows in the registry already name more than one entry there.
2. **CORPUS rule 4** (SOURCES-CONTRACT-v1): "Expansion is knowledge, not rows. ... There is no row
   quota; a short registry of opened, honestly tiered rows beats a long one."
3. **The declaration agrees.** `.ufo/waves/round-100/claims-declaration-r100.md` names the source
   claim as "**S533** (`gutils.c`, opened and quoted again this round)" - a re-open and a re-quote
   of a held row, which is a `used-by` append plus a Gate admit, not a new id.
4. **Precedent.** Round 96 opened a row only for a *new file* (S524) and a *new scope on a spec
   locator* (S525), and round 97 opened S526 for a *different question of the same file* (the
   file-name-only guess against the data-given guess); both re-opened held rows got `used-by`
   appends only (round 97's draft section 2: "Only `used-by` cells change; no anchor, digest or
   scope cell of a held row moves"). Here the file is the same and the question is a subset of the
   held scope.

**Census consequence of the decision (measured, not asserted).** With no new row, the registry stays
at 469 rows and no new duplicate-URL warning appears. A new row carrying S533's URL would raise one
`W04` warning (same URL across scopes), and a new row whose `scope` cell were **identical** to
S533's would raise `E04` ("duplicate url ... within scope", no `supersedes`) and make the census
exit 1 - so the "new row" option is not free either.

**Landing order (census E11, measured).** A `mined` row's `used-by` path must exist on disk
(`scripts/sources-census.sh:567`), and `corpus/knowledge/gio-launch-path-default-r100.md` does not
exist at the base revision. The entry must land **before or with** the registry commit that appends
the three `used-by` cells, or the census fails on the rows this round touches.

## 2. The registry work: three `used-by` appends (old -> new, exact cell text)

Only `used-by` cells change; no anchor, digest, scope, status, opened or recheck cell of a held row
moves (CORPUS rule 2).

| id | old `used-by` (verbatim, base revision) | new `used-by` | why |
|---|---|---|---|
| S528 | `corpus/knowledge/gio-exec-argv-r98.md, corpus/knowledge/gio-launch-env-r99.md` | the same plus `, corpus/knowledge/gio-launch-path-default-r100.md` | the entry cites the load gate's two `g_find_program_for_path` calls (`gdesktopappinfo.c:1951`, `:1993`) and their `working_dir` comments (`:1950`, `:1992`) |
| S532 | `corpus/knowledge/gio-launch-env-r99.md` | the same plus `, corpus/knowledge/gio-launch-path-default-r100.md` | the entry cites the CLI's constructor (`:106`) and the load-refusal line it prints (`:109`, exit 1 at `:111`) |
| S533 | `corpus/knowledge/gio-launch-env-r99.md` | the same plus `, corpus/knowledge/gio-launch-path-default-r100.md` | the entry cites the whole unset-default branch: PATH source `:371`, guard `:376`, literal `:388`, short-circuit `:331-357`, empty entry `:471-477`, joins `:480-484`, `:490-497` |

Each append uses the **comma-space** separator, which is the style S528's cell already carries and
the style round 99 used when it appended to a single-entry cell (S528 became
`corpus/knowledge/gio-exec-argv-r98.md, corpus/knowledge/gio-launch-env-r99.md` that way). Nothing
sits outside the closing pipe. Measured over a scratch copy of the registry with the entry file in
place and the three cells set to these values: `check-sources-readback.py` -> `rows=469 entries=121
findings=0`, exit 0; `sources-census.sh validate` -> exit 0 with no `E` finding (the entry file's
presence is what clears the `E11` used-by check).

**Symmetry with the entry's front matter.** The entry's `source:` block names exactly `S528`,
`S532`, `S533` - the three rows above - so the read-back gate's R4 rule ("an entry-cited row with
status `mined` whose used-by cell does not name that entry") is satisfied in both directions once
the entry lands. A trial of the read-back gate over a scratch copy of the registry with the entry
present and the three cells appended is reported in section 5.

## 3. Fallback if the L1 rules a distinct scope row is wanted (drafted, **not** appended anywhere)

If the L1 prefers a row of its own for the narrower unset-branch scope (the round-96/97 precedent
for a *new scope* on a held file), the next free id is `S535` and the row is drafted here in the
registry's 11-column shape. **This is the fallback, not the recommendation** - section 1 gives the
reasons the recommendation is "no new row". Two changes follow from it: the entry's `source:` block
must then also name `S535`, and S533's `used-by` would **not** be appended (the row that carries the
entry's citation is the new one).

```
| S535 | GLib 2.90.1 `g_find_program_for_path` - the PATH-unset default branch - https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c (sha256 65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771, 100534 B, 3245 L, HTTP 200 at the recorded URL, re-fetched byte-identical on 2026-11-08; the same file S533 holds, new scope, census W04 expected); host package glib2 2.90.1-1 | code | A | the PATH-unset default search path of the launch load gate: the default literal, the unset guard, the empty-entry rule, the absolute-or-slash short-circuit, and the load-time consequence that the resolving process's cwd decides the trailing dot | gutils.c:388 (the `/bin:/usr/bin:.` literal), :370-371 (the PATH source), :376 (the unset guard), :383-386 (the security comment), :331-357 (the absolute-or-slash branch; :332-333 the test, :339-340 the executable-and-not-a-directory test), :471-477 (the empty-entry rule), :480-484 (the working-dir join), :490-497 (the cwd join) | an absent PATH is a three-entry default search, not an empty one, and the difference is visible in the argv0 string the load gate hands the child - `{root}/./probe` against `{root}/probe` | mined | 2026-11-08 | 2027-05-07 | corpus/knowledge/gio-launch-path-default-r100.md |
```

Field notes for the fallback row:

- `id` `S535` continues the registry (the base registry's last id is `S534`; `grep -n 'S535'
  corpus/SOURCES.md` returns nothing).
- `status` `mined` (the row is cited by the entry that this round lands).
- `recheck` `2027-05-07` - an **ISO date**, which the census accepts (E09 admits an ISO date, `NNd`
  or a symbolic cadence) and which is `2026-11-08 + 180d`, i.e. the same cadence S533 and S534
  carry, written in the date form.
- `used-by` names **only** the entry this round drafts:
  `corpus/knowledge/gio-launch-path-default-r100.md`.
- `scope` differs from S533's scope cell, so the census raises `W04` (same URL across scopes - a
  warning) and **not** `E04` (which fires only on an identical url+scope pair). Making the scope
  cell identical to S533's would make the census exit 1.
- Row count: 469 -> 470 (tier A +1, status `mined` +1) if the fallback is taken; 469 -> 469
  otherwise.

## 4. The round lesson's `## Gate` block (draft for `corpus/lessons/round-100.md`)

Shape copied from `corpus/lessons/round-99.md`'s `## Gate` (id | row | url | access | located quote
(<=25 words) | decision), plus the "Rejected this round" line the round-99 lesson carries.

> Every row below was re-opened by this seat on **2026-11-08**; the `gutils.c` bytes were taken from
> the committed round-99 fetch **and** from a live re-fetch of the recorded URL (HTTP 200,
> byte-identical, sha256 `65086c29...e3771`), so the digest is confirmed twice.

| id | row | url | access | located quote (<=25 words) | decision |
|---|---|---|---|---|---|
| S533 | `gutils.c` (tier A) | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c (HTTP 200, 100534 B, sha256 `65086c29...e3771`); host package glib2 2.90.1-1 | 2026-11-08 | `path = "/bin:/usr/bin:.";` (`:388`, 4 words) | **admit** - the PATH-unset default literal the round's branch is about, re-opened and quoted again; the row's own scope and anchor already carry the branch (`:370-389`, `:462-500`), so the registry gains a `used-by` name, not a new id |
| S533 | `gutils.c`, the empty-entry rule (tier A) | as above | 2026-11-08 | `Two adjacent colons, or a colon at the beginning or the end of 'PATH' means to search the current directory.` (`:472-473`, 20 words) | **admit** - the rule that makes the unset default and the set-but-empty PATH different walks |
| S533 | `gutils.c`, the absolute-or-slash short-circuit (tier A) | as above | 2026-11-08 | `if (g_path_is_absolute (program) || strchr (original_program, G_DIR_SEPARATOR) != NULL` (`:332-333`, 9 words) | **admit** - the branch that returns before the PATH source is read, which is why the two round-99 `path-unset` cases cannot witness the default |

Rejected this round: the staged merge package
(`/home/vgpnk/Projects/shokuknow/merge/mado/`, read-only) holds **nothing on this ground** - see the
reject row below.

| candidate | staged path | decision | reason | flip |
|---|---|---|---|---|
| the staged package's launch/exec-adjacent rows (`S205` Hyprland dispatchers, `S211` Waybar theming, `S244` privileged Wayland clients, `S257` omarchy app restart helper, `S262`/`S263` uwsm app slice and app-daemon, `S267`/`S268` omarchy idle ladder and host idle daemon) | `MERGE-REPORT.md:105`; `SOURCES.append.md:9`, `:15`, `:48`, `:61`, `:66`, `:67`, `:71`, `:72` | **reject** as sources for this round's C1 scope | the sweep `grep -niE 'launch\|/bin:/usr/bin\|PATH default\|elapsed\|per-leg\|spawn' MERGE-REPORT.md SOURCES.append.md` returns 9 hits and **zero** of them is on this ground: 0 hits for `/bin:/usr/bin`, 0 for `PATH default`, 0 for `per-leg` (measured this seat, 2026-11-08); every hit is a Round 6-7 artifact about the session's app lifecycle (uwsm slices, an app-restart helper, the idle timer ladder), not about how a program name is resolved from a PATH. The connector's own sweep reaches the same verdict (`.ufo/waves/round-100/assimilation/connector-sweep-r100.txt`, PART 2: "Assimilation: none on this ground") | a staged row that opens `gutils.c`'s default search path, or the harm panel's per-leg timing, would become admissible - a staged row about *app lifecycle* is still not a row about *program resolution* |

### Locator correction the L1 should apply to the declaration (not a predicate change)

The declaration (C1, frozen statement) cites the default literal as "`gutils.c:370-382`", and the
round's assignment repeats that range. The literal is **not** inside that range: `gutils.c:371`
reads the PATH source, `:376` is the `if (path == NULL)` guard, and the assignment
`path = "/bin:/usr/bin:.";` is at **`:388`** (the block runs `:376-389`). S533's own anchor cell is
correct (`:370-389` covers the literal). This is the round-99 M99-2 class - a locator inferred from
the block rather than from the line the quote sits on - and it is a **locator** correction, not a
widening of the frozen predicate: the sentence's claim (the default is `/bin:/usr/bin:.`) is
confirmed by the bytes and by the L1's own ground measurement. The entry draft therefore quotes
`:388` (and the gate rows above quote `:388`, `:472-473` and `:332-333`), while the declaration's
`:370-382` stands as written for the L1 to correct in place or in an erratum.

## 5. Measurements of the draft's own registry claims

| check | command | observed |
|---|---|---|
| S533's scope and anchor really cover the branch's lines | `awk -F'|' '$2 ~ / S533 /' corpus/SOURCES.md` | scope names "the PATH source and its default, the empty PATH entry"; anchor names `:331-357`, `:370-389`, `:462-500` |
| the next free id | `grep -n 'S535' corpus/SOURCES.md` | no match; the base registry's last id is `S534` |
| the base registry validates | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | exit 0; warnings only (W01/W04); no `E` finding |
| the base registry reads back clean | `python3 -I quality/check-sources-readback.py --repo <lane>` | `rows=469 entries=120 findings=0`, exit 0 |
| the draft's row shape is census-legal | a scratch copy of the registry with the section 3 row inserted, validated with `scripts/sources-census.sh validate --file <copy>` over a scratch mirror of the lane's `corpus/` (the entry file copied in, so the `used-by` path resolves) | the copy produces **one** new finding class only: `W04 S535 duplicate url gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c across scopes` (a warning; `scripts/sources-census.sh:648`). Census **exit 0**, zero `E01`-`E11` findings: 13 pipe-separated cells, `S535` matches `^S[0-9]{3,}$`, kind `code` and tier `A` are enums, status `mined` is an enum, `opened` 2026-11-08 is not in the future, `recheck` 2027-05-07 is a valid ISO date, and the `used-by` path resolves because the entry file is present |
| the primary path (no new row, three `used-by` appends) is clean | the same scratch mirror with the `S535` row removed, the three `used-by` cells set to the section 2 values, and the entry file in place: `python3 -I quality/check-sources-readback.py --repo <mirror>` and `bash scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md --today 2026-11-08` | read-back: `SOURCES_READBACK: rows=469 entries=121 findings=0`, **exit 0** (no R1/R3/R4/R5/R6 finding; the `NOTE outside-corpus` lines are the registry's pre-existing non-findings). Census: **exit 0**, zero `E` findings. The cell text is what matters: appending without the comma (`...r99.md corpus/...r100.md`) makes the gate report `R3` (the whole cell is one path) and `R4` for the un-appended entry - the comma-space form clears both |
| the row's `recheck` date is derived, not invented | `python3 -c "import datetime; print(datetime.date(2026,11,8)+datetime.timedelta(days=180))"` | `2027-05-07` |
| the entry's ASCII-only property | `LC_ALL=C grep -cP '[^\x00-\x7F]' .ufo/waves/round-100/build/gio-launch-path-default-r100.md` | `0` |

## 6. What this seat did not do, and what the L1 must do

- **Not done here:** nothing under `corpus/` was edited; no row was appended; no `used-by` cell was
  changed; `corpus/lessons/round-100.md` was not created. This file and the entry draft are the
  deliverables; the L1 lands them.
- **L1 checklist:** (1) land the entry at `corpus/knowledge/gio-launch-path-default-r100.md`;
  (2) append the three `used-by` cells of section 2 (or take the section 3 fallback and add `S535`);
  (3) paste the section 4 `## Gate` block into the round lesson, including the reject row and the
  locator correction; (4) re-run `sources-census.sh validate` and
  `check-sources-readback.py` over the landed tree and land the receipts. The census's `E11` fires
  if the entry is not on disk when the `used-by` cells are appended, so (1) precedes (2).
- **Open question for the L1 (one sentence, no verdict claimed here):** the declaration's C1
  separation (3) is a prose sentence and not a predicate conjunct, and the wave's reviewer and
  critic have both measured that its found/not-found half does not hold for the fixture shapes the
  oracle's schema can express (the trailing `.` is observable only as the extra `./` in argv0).
  This entry documents the measured behaviour and does not widen the frozen predicate; if the L1
  narrows C1, the entry's section 2 (3) is the text to re-check.
