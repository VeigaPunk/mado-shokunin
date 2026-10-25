# CritSchema — S201, S202 in corpus/SOURCES.md vs CORPUS.md contract v1

Scope: the two appended registry rows `| S201 | … |` (SOURCES.md:203) and
`| S202 | … |` (SOURCES.md:204), checked against the 11-column contract in
`/home/vgpnk/Projects/shokunin/CORPUS.md` § SOURCES.md (frozen v1).
Verdict: **no defects found in either row**.

## Checks performed and evidence

### Column count — PASS
`awk -F'|' '/^\|[[:space:]]*S(201|202)[[:space:]]*\|/ {print $2, NF}' corpus/SOURCES.md`
prints `S201 NF=13`, `S202 NF=13` — 11 data columns per the census rule
("11 columns means NF=13; must print 0").

### Pipe hygiene — PASS
Both rows contain no literal `|` inside cells (NF=13 proves no extra field
separators) and `grep '\\'` on lines 203–204 finds no backslash escapes —
no `\|` or `\\` tricks. No `|` inside any cell per the `id` rule.

### recheck cell — PASS
S201 recheck = `90d`, S202 recheck = `90d`. `NNd` cadence form accepted by
the contract (`recheck` — "ISO date or cadence (`90d`, `180d`, `on-release`)").

### status — PASS
S201 status = `mined`, S202 status = `mined`. Valid enum, and the `mined`
requirement is met: `used-by` names `corpus/knowledge/waybar-module-text-route-r25.md`,
which exists (1227 B, `ls -la`) and cites both rows:
`source: S201 — …backend.cpp` (:7), `source: S202 — …window.cpp` (:8).

### opened date — PASS
S201 opened = `2026-10-24`, S202 opened = `2026-10-24`. Valid ISO date; not
future-dated (today). Consistent with rule 1 ("write the row only after
opening the source in the round that writes the row").

### anchor cell names a real location — PASS
Anchors re-verified by fetching the cited URLs:

- **S201** anchor `backend.cpp:38 at tag 0.15.0, 6550 B, sha256 prefix 799bf02f6d18ae04`.
  Fetched file: 6550 B, sha256 `799bf02f6d18ae04…` — byte count and prefix
  match. Line 38 is `spdlog::warn("$XDG_RUNTIME_DIR/hypr does not exist,
  falling back to /tmp/hypr");` — exactly what `teaches` claims.
- **S202** anchor `window.cpp:27 at tag 0.15.0, 8324 B, sha256 prefix 5df496eb3cfe5cae`.
  Fetched file: 8324 B, sha256 `5df496eb3cfe5cae…` — byte count and prefix
  match. Line 27 is `m_ipc.registerForIPC("activewindow", this);` — exactly
  what `teaches` claims.

## Out-of-scope observations (not defects against the checked cells)

- `id` sequence in the registry jumps S189 → S196 → S201 (gaps exist at
  S190–S195, S197–S200 elsewhere in the table or not yet written). The
  contract requires `S` + ≥3 digits, "the next unused; never reused" — the
  two checked ids do not duplicate any existing row (uniq-d check implicit:
  each appears once), and gaps are not prohibited.
- `kind` = `code`, `tier` = `A` on both rows: valid enum; A-tier code is
  allowed ("source code" is named A-tier material).
