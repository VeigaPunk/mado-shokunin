# ScoutFrontier report (round 45 w1)

Status: DONE. Full map at `.ufo/waves/round-45/w1/ScoutFrontier/map.md`.

Headlines (lane HEAD ebdba13f; all line numbers from grep -n/sed -n):
- Frontier text moved: `corpus/README.md:131` ("output-management behavior", round-12 bullet) and `:137-139` ("runtime state agreement ...", round-14 bullet); newest precedent adds `###` tail subsections (`:295` round 43, `:304` round 44; file ends `:320`), not bullets.
- README index row: insert after line 72 (r44 row); 3 cells `| \`knowledge/hyprland-monitor-rule-r45.md\` (MADO-R45-1, round 45; ...) | Holds | S302, ... S310 |`; counter clause f = exactly one column-0 unfenced row with that prefix (`c2-r45-monitor-entry.py:614-615`); draft placeholder row at `l1-draft/build-pos.py:97-99`.
- SKILL.md: claim-first routing row after `:158`; read-only-probes row after `:225`; new section `### Monitor rule versus reported monitor` between `:312` and `:314`, mirroring per-verdict table `:272-283` and exit map `:284-285`; no gate-registry entry (geometry has none).
- PROVINCE.md: tool row after `:32` (mado-geometry); 4 cells Tool | Reads | Writes | Owner.
- Held monitor ground: `SKILL.md:75`, `:179` (99.997 vs 100), `output-colour-boundaries-r14.md` (protocol route only, no `monitor =` chain; S050 safety caveat keeps the tool file+dump-only).
- Neither counter reads SKILL/PROVINCE/Frontier; only README clause f.
Unknowns: exact CLI flags / SETUP exit code (take from reference docstring); whether to extend `SKILL.md:326` whitelist with `monitors all`.
