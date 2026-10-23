# ReopenS172 — SOURCES row S172 re-open (a3w2)

Reviewer seat: MadoR25A3.ReopenS172. Re-opened row S172 (`corpus/SOURCES.md:184`), drafted by a3w1 seat WikiHyprlang (`.ufo/waves/round-25/a3w1/reports/WikiHyprlang.md`). Method: fresh fetch with curl, anchor comparison, verbatim quote checks at stated lines (whitespace-collapsed substring), teaches-cell fidelity against the bytes.

## What I did

1. Fresh fetch (no proxy of the a3w1 capture):

```sh
timeout 60 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/hypr-ecosystem/dev/hyprlang.md' -o /fast/scratch/hyaku/mado-r25a3/reopen/S172.bin && echo "curl_exit=0" && sha256sum .../S172.bin && wc -c -l .../S172.bin
```

```text
curl_exit=0
8ce3d33ea39757ed7316fd4146d0b0fed975c79fca1ab912153e5ed1acc9e60e  /fast/scratch/hyaku/mado-r25a3/reopen/S172.bin
 193 4772 /fast/scratch/hyaku/mado-r25a3/reopen/S172.bin
```

2. Anchor comparison (row cell): `content/hypr-ecosystem/dev/hyprlang.md:18-21,25-51,72-77 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:8ce3d33ea39757ed7316fd4146d0b0fed975c79fca1ab912153e5ed1acc9e60e, 4772 B`.

- sha256 fresh `8ce3d33ea39757ed7316fd4146d0b0fed975c79fca1ab912153e5ed1acc9e60e` = anchor ✓
- 4772 bytes = anchor "4772 B" ✓; 193 lines matches report ✓
- a3w1 capture `.ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin` hashes identically (`8ce3d33e…`, 4772 B) — report capture is the same bytes as today's fetch ✓
- Anchor ranges land on real content: 18-21 = Line Style prose (variable vs keyword, single definition), 25-51 = Categories section (regular/special, block and keyed forms), 72-77 = Comments section. Commit in URL = anchor commit `c66e8de2…` ✓

3. Quote checks — Python (`python3 -I -B`) over the fresh bytes, UTF-8 decode, `\s+`→single space on line and quote, quote asserted inside the collapsed stated line and inside the collapsed document; each ≤ 25 words:

```text
line=74 words=7 at_stated_line=True in_doc=True   "Comments are started with the `#` character."
line=76 words=19 at_stated_line=True in_doc=True  "If you want to escape it (put an actual `#` and not start a comment) you can use `##`."
line=77 words=16 at_stated_line=True in_doc=True  "It will be turned into a single `#` that _will_ be a part of your line."
line=27 words=6 at_stated_line=True in_doc=True   "Categories can be regular or "special"."
ALL_QUOTES_OK
```

All four located quotes in the a3w1 report are verbatim at their stated lines.

4. Teaches cell vs bytes. Cell: "Documents comment and `##` escape rules plus category syntax relevant to parsing config lines; does not describe `source =` traversal or Hyprland bind-table construction".

- Comments (`#`) documented at line 74; `##` escape at 76-77 with the "single `#` … part of your line" semantics ✓
- Category syntax documented: regular vs "special", block form, keyed special form, inline `category:variable` and `category[key]:variable` ✓
- Case-insensitive count of "source" in the bytes: 0 — no `source =` traversal claim anywhere ✓; "glob": 0 ✓
- "bind" occurs exactly twice, only as literal example config lines in the "Escaping Errors" and "Arithmetic Escaping" sections; the page never describes how Hyprland constructs its bind table or its 18-field output ✓
- Scope cell ("…not source-graph behavior") matches the same evidence ✓

No claim in the `teaches` cell exceeds what the bytes show; nothing the bytes clearly show is contradicted.

## Verdict

REOPEN S172: agree

Residual risk: the page does document `bind = …` as example syntax and `hyprctl keyword` in passing, so it is fine as C1 config-syntax context but must stay out of bind-table-construction citations — which is exactly how S172 scopes it. No actionable finding.

Verification artifacts: fresh bytes `/fast/scratch/hyaku/mado-r25a3/reopen/S172.bin` (left in place as evidence). No lane file touched except this report; no processes left running; no tools installed; no `__pycache__` created (`python3 -I -B`).
