# ScribeE01D3 — C2 D3 E01 red-before evidence

## Behavior and gates

- **Red gate: PASS.** The assigned fixture at `.ufo/waves/round-28/evidence/e01-red-before/SOURCES.md` has the registry header and exactly five malformed two-cell rows for S178–S182 (fixture lines 1–10). Its required validation emitted exactly five tab-delimited E01 findings, each `fields=2`, and exited 1.
- **Green gate: PASS for observed census behavior.** Validation of the pre-existing clone at `/fast/scratch/hyaku/mado-r28/d3clone` exited 0 and emitted no E01 lines. It did emit seven non-fatal W04 duplicate-URL warnings; the final `d3clone\tok\t.../corpus/SOURCES.md` line and exit 0 are preserved below.
- **Census implementation digest: PASS.** `sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` returned `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, the frozen value. The implementation documents E01 as `NF!=13` and prints `fields=NF-2` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:24-29,634-638`). The historical defect is recorded as five two-cell S178–S182 quote rows in `.ufo/waves/round-27/drafts/lesson-round-27.md:14`; the frozen round-28 registration assigns this receipt to D3 at `.ufo/waves/round-28/registration.md:57-63`.

## Verbatim red transcript

Also recorded at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/e01-red-before.txt`:

```text
$ sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/e01-red-before/SOURCES.md
55969efeacb23dd17c9ac8f7d5f448bef60572ca8ca9c95390863f14714b4ba9  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/e01-red-before/SOURCES.md
fixture_sha256=55969efeacb23dd17c9ac8f7d5f448bef60572ca8ca9c95390863f14714b4ba9
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/e01-red-before/SOURCES.md --today 2026-10-23
file	E01	S178 fields=2
file	E01	S179 fields=2
file	E01	S180 fields=2
file	E01	S181 fields=2
file	E01	S182 fields=2
exit=1
```

## Verbatim green transcript

The requested destination already existed when this session inspected it. Its observed origin is the lane and its full HEAD is `123d8cd07fada3b75fbe6d726b30e5b96abd39d7` (the prompt-named pinned pre-freeze suite baseline); `git status --short` emitted no output. The clone command was **not rerun** to avoid overwriting the pre-existing destination. Therefore this report does not claim direct observation of a `git clone --no-hardlinks` invocation. The green census run itself is observed:

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-23 /fast/scratch/hyaku/mado-r28/d3clone
d3clone	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
d3clone	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
d3clone	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
d3clone	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
d3clone	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
d3clone	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
d3clone	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
d3clone	ok	/fast/scratch/hyaku/mado-r28/d3clone/corpus/SOURCES.md
exit=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-23 /fast/scratch/hyaku/mado-r28/d3clone | { grep -F $'\tE01\t' || true; } | wc -l
E01 stdout lines: 0
```

## Touched surfaces and provenance

- `.ufo/waves/round-28/evidence/e01-red-before/SOURCES.md` — the assigned fixture was already present with the exact requested header and five malformed rows when inspected; it was left byte-for-byte unchanged. Its measured SHA-256 is recorded in the red transcript.
- `.ufo/waves/round-28/evidence/e01-red-before.txt` — created as the red/green transcript.
- `.ufo/waves/round-28/w1/reports/ScribeE01D3.md` — this report.
- No product code, frozen registration, either round-28 counter, census script, or round-27 counter was edited. No suite/counter was run, no tool was installed, no network source was opened, and no H1 material was read.

## Findings and limits

The red-before result directly demonstrates the literal E01 behavior for the five historical malformed row shapes; the green census result is clean with respect to E01 and has only the seven reported W04 warnings. The destination clone pre-existed, so no-hardlinks command provenance is unobserved in this session. The observed clone HEAD and origin are in the transcript; the fact that the destination object directory and lane object directory had different device/inode pairs (`66309:1995087037` versus `56:10602800`) does not by itself establish that no individual object files are hard-linked. This limitation is disclosed rather than upgraded into execution evidence.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/e01-red-before/SOURCES.md`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/evidence/e01-red-before.txt`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w1/reports/ScribeE01D3.md`
