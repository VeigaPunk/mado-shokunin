# ScrAssimK2 — K2 (`host-producer-outputs-r29`) scope check, verdict, re-grounded draft

Seat: mado round-40 w1, leaf (no dispatch, no background jobs, no package transaction). Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Date 2026-10-25.

**Deliverable:** `.ufo/waves/round-40/w1/ScrAssimK2/verdict-and-draft.md` (34 605 B, 467 lines) —
scope/held/quality check with evidence, verdict slot, re-grounded entry draft with `<<QUOTE>>` slots,
reject list with flip conditions, verbatim conflicts.

## Verdict

- **Candidate `host-producer-outputs-r29.md`, as written: REFUSE.**
- **Re-grounded successor (drafted in §5): ADMIT**, conditional on gates G1–G5 in §6 of the deliverable.
- Recommendation: reject the candidate, admit the census successor. That pairing also satisfies the
  registration's assimilation gate (≥1 admit and ≥1 reject) from one candidate.

## Findings (each names what it attacks)

1. **D1 — the producer count is the upstream layer, not the host layer (fatal).** Candidate line 37 says
   "the bar's five JSON producers". Host `~/.config/waybar/config.jsonc` (6354 B, sha256
   `a408a33d…aae829`, mtime 2026-10-17) declares **7** `return-type: json` modules and **8** `exec`
   modules (`host-reads.txt:19-30`; seat re-derivation of the same bytes agrees). The stock upstream config
   on the same host (5114 B backup) declares **5** — the candidate counted the upstream set while writing
   about the host (QUALITY criteria 10/14/15/16).
2. **D2 — the headline sentence is internally false and the idle-chip reason is inverted (fatal).**
   Candidate 37-40 says three of five render empty and then names a member "which instead shows 'Idle lock
   disabled'". On this host `hypridle` runs (`host-reads.txt:16` → `1680 /usr/bin/hypridle`), so
   `idle.sh:3` is true and `idle.sh:4` prints `{"text": ""}` — the chip is empty *because the lock is
   armed*, the inverse of the candidate's stated reason (criteria 3/10). Corrected census: 3 of 7 json
   producers render empty today, all three indicator chips.
3. **D3 — the S241 quote is a rotating volatile value and has already rotated (fatal for a quote).**
   Candidate line 35 quotes `"updated_at": "2026-10-23T22:52:44Z",`; the field now reads
   `…-10-25T20:47:13Z` (`quotes.md:100`, verdict DIFFERENT). The cache is rewritten on a ~5-minute cadence
   (held `waybar-walker-semantics.md:149`; seat saw 29 865 → 29 877 B within minutes). The quote is also
   2 words, below the 3–25-word band (criteria 6/27).
4. **D4 — the five source ids are not in the lane registry.** `grep -cE '^\| S(237|238|239|240|241) '
   corpus/SOURCES.md` → `0`; S237–S241 are free per `assimilation/{reg-ids,collisions}` (criterion 2 +
   registry contract v1).
5. **D5 — anchors name symlinks as files, one pinned size drifted.** `~/.local/bin/gkeep` →
   `Projects/gkeep/bin/gkeep` (252 B) and `~/.local/bin/ai-usage` → `Projects/omarchy-usage-tray/bin/ai-usage`
   (114 246 B, not the candidate's 134 777 B) (`host-reads.txt:36-45`; criteria 6/18).
6. **Held-duplication:** four of the candidate's seven OBS blocks restate `waybar-walker-semantics.md:138,140,149`,
   and its `custom/voxtype` UNK ("scripts located but not read") is stale against `:137`, which reads the
   script and measures its payload. What is genuinely unheld: the host/upstream byte identity of the two
   indicator scripts, the `custom/gkeep` producer row, the resolved shims, and a census with a denominator.
7. **Scope:** producer contracts are IN as the bar's chain (precedent `waybar-walker-semantics.md:135-149`);
   the gkeep package is OUT (`config-drift-r12.md:109`); network producers stay UNK; both host-local
   producers resolve outside the owned config plane.

## Verified by this seat (read-only)

`cmp`/`sha256sum` over the six indicator files → host == v3.8.4 == v3.8.3, all rc=0 (169 B
`28491cd3…a199bc63c`, 174 B `312900d1…9d6de69`); `json.loads` census of the two waybar configs (host
`exec= 8 json= 7`, stock `exec= 6 json= 5`); `cat -n`/`sha256sum` of `idle.sh`
(`6d8d2c11…d10f0f1750`); `pgrep -a -x hypridle` → `1680 /usr/bin/hypridle`; `ls`/`stat` of the two
symlinks and the cache. No compositor verb, no socket, no `makoctl`, no producer run, no package
transaction, no tool installed.

## Conflicts reported verbatim (for the canonical judge; not resolved here)

1. `makoctl mode`: `quotes.md:124` declares it barred ("it opens the mako daemon socket") vs
   `host-reads.txt:105-107` showing `default` / `makoctl_rc=0`. Both executor receipts.
2. `hypridle` state: candidate "no `hypridle` runs" vs `host-reads.txt:16` pid 1680 (and S205's pid 1667).
3. `ai-usage` size 134 777 B vs 114 246 B.
4. `updated_at` 2026-10-23T22:52:44Z vs 2026-10-25T20:47:13Z.
5. Producer count 5 vs 7 json / 8 exec.

## Open mechanical dependency (for L1)

Gate G2: the two receipt files (`w1/ExecK2HostReads/host-reads.txt`, `w1/ExecFetchK2Sources/quotes.md`)
live in seat dirs, not `.ufo/waves/round-40/fetch/`. L1 either copies them into `fetch/` (this seat does
not write another seat's files) or the lesson's `## Gate` shape admits the committed seat path.

## Touched surfaces

Wrote only: `.ufo/waves/round-40/w1/ScrAssimK2/verdict-and-draft.md` and this report. No tracked file
edited, no `corpus/`, `tools/`, `quality/`, `scripts/`, `templates/`, `MANIFEST.json`, `.ufo/state/` write,
no git/jj mutation, no fleet or sibling-lane write. Tools installed: none.

Report: .ufo/waves/round-40/w1/ScrAssimK2.md
