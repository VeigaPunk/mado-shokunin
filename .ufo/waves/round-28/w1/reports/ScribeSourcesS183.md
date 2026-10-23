# ScribeSourcesS183 — round 28, wave 1

## Behavior and finding

Created `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/mutation-testing-r28.md` (lines 1–35). It defines the scope of a finite mutation result, distinguishes mutation score from real-fault detection, explains equivalent-mutant limits, bounds the six C1 legs to their registered mutants/subjects/inputs, and cites the lane's M26-8 and M27-3 gate records. The `## Gate` records S183's URL, access date, and located quote (note lines 29–35).

Opened `https://doi.org/10.1145/2635868.2635929` with the reader on 2026-10-23. Reader returned CrossRef metadata for Just et al., including the title `Are mutants a valid substitute for real faults in software testing?`, venue, authors, and publication date; it reported no abstract. Located quote (11 words), from the reader's CrossRef `title` field: “Are mutants a valid substitute for real faults in software testing?” No finding or method detail from the paper body is attributed. The existing registry search log at `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:397-405` records that the ACM target returned HTTP 403 and that no alternate source was opened; that log was not changed.

`/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md:195` already contained S183 with the title-metadata scope and `used-by` path for the new note. I did not append a duplicate row or modify the existing row or any other row. The census accepted the registry after the note existed. No S178–S182 repair was needed.

## Gates — source census

Exact command run before the note was created:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado; rc=$?; printf '\nEXIT_CODE=%s\n' "$rc"; exit 0
```

Output and script exit code:

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	E11	S183 missing used-by corpus/knowledge/mutation-testing-r28.md

EXIT_CODE=1
```

Exact command run after the note was created:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado; rc=$?; printf '\nEXIT_CODE=%s\n' "$rc"; exit 0
```

Output and script exit code:

```text
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md

EXIT_CODE=0
```

The seven W04 duplicate-URL warnings remained in both transcripts; the post-edit validator returned 0 and reported the registry `ok`. Baseline E11 was the absent `used-by` note target, resolved by creating the note.

## Touched surfaces and provenance

- Created `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/mutation-testing-r28.md`.
- Created this report at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w1/reports/ScribeSourcesS183.md`.
- Read but did not change `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`; S183 row was already present at line 195.
- No tools installed or updated. No suite, build, or test was run; only the explicitly requested source-census validation was run.

## Out of scope and limits

No change to the frozen registration, round-27 counters, other source rows, S178–S182, or any judge/product code. No H1 held-out data or seal contents were read. This note cannot report the paper's empirical findings because the opened reader response contained metadata only; S183 supports title/question framing, while the prior lane gate records support the cited finite-suite examples.
