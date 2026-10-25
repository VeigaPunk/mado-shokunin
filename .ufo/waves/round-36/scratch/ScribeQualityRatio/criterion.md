# Draft criterion 59 — domain-versus-meta commit ratio per round report

Numbered for insertion after criterion 58 in `corpus/QUALITY.md` (read-only at
draft time; that file was last touched for criteria numbering in round 30/31,
so 59 is the next free number in the numbering the file carried when this wave's
prompts were written).

```text
59. Every round report states the domain-versus-meta ratio of the lane's last
    30 commits with the command that produced it: domain-facing commits are
    those touching `tools/`, `corpus/knowledge/` or `PROVINCE.md`; commits
    touching only records and instruments (LOG.md, SCORECARD.md,
    corpus/lessons/, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md,
    quality/, .ufo/) are meta. When the count shows the lane has gone two or
    more consecutive rounds without a domain-facing change — or the longest
    record-only streak spans two or more rounds' worth of commits — the report
    says so in the same sentence as the ratio, not only in a reflection. A
    commit whose only domain-path hits are fixture or control copies carried
    under `.ufo/` is meta. Check:
    `git log -30 --name-only --format='%h' | awk '/^[0-9a-f]{7}$/{c=$1;next}
    /^(tools\/|corpus\/knowledge\/|PROVINCE\.md)/{print c}' | sort -u | wc -l`
    over the committed HEAD at report time; the report pins that HEAD.
    (ground: considerthese/2026-10-24.md proposal 1, 2026-10-24)
```

## Grounding — the counts this criterion would have reported

Measured by this seat at the round-36 freeze commit `dbf8b57` (the HEAD the
wave-1 scout measured over), 2026-10-25:

- `git log -30 dbf8b57 --name-only` → 30 commits, **3 domain / 27 meta**,
  longest record-only streak **20** (dbf8b57 down through 19e4ab3, covering the
  round-36 freeze, all of round-35 closure, and the round-34 freeze/spot-check
  tail).
- Domain-flagged commits in the window:
  - `02088b4` (round 35): lands the three idle-lock `corpus/knowledge/` entries
    — the only new-knowledge commit.
  - `4f35c80` (round 35): wave-2 errata; also touches the same three
    knowledge files.
  - `fa7ba11` (round 34): admits the waybar event-socket entry; touches
    `corpus/knowledge/waybar-module-text-route-r25.md`.
- `SKILL.md` is untouched in the window (0 hits), so the proposal's three-path
  domain set and any widened set including `SKILL.md` coincide here.
- Limit: the rule is path-syntactic. An erratum/admission edit to an existing
  knowledge note (4f35c80, fa7ba11) counts domain though it adds no new domain
  content; a fixture tree under `.ufo/` containing `corpus/knowledge/` copies
  would false-positive and is excluded by the meta clause. A semantic
  new-capability reading of the same window yields 1 domain / 29 meta.
- Round-36 side: at `dbf8b57` only the freeze commit had landed (meta); the
  ratio for round 36 is under-counted until the round's data commits land.

## Provenance

- Proposal: `considerthese/2026-10-24.md` (2026-10-24), proposal 1 under
  "Self-improvement suggestions": "Track a domain-versus-meta ratio per window
  … flag when the lane goes two or more rounds without a desktop-facing change."
- The scout measurement seat for this wave (`ScoutConsiderRatio`, prompt at
  `.ufo/waves/round-36/w1/prompts/ScoutConsiderRatio.md`) had no committed report
  at draft time; the counts above are this seat's own re-derivation from the
  lane's commit record, per criterion 10's re-derive-not-transcribe rule.
- Citation form follows criteria 57/58's `(ground: …)` / `(lesson: …)` tail;
  this criterion grounds in an operator-authored reflection file, not a
  `lessons/` mistake, so the anchor is the file and proposal number with date.
