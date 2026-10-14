# WWKD plan — mado round 2 (ufo-round-plan-v1)
Axis set: depth (config semantics), operability (live verification), freshness.
Axis move: depth. Claim: hyprctl's read-only query surface (getoption/etc.)
can verify live what the config files declare — a verification layer mapping
>=10 config claims to their live hyprctl values, with divergence classes
(config-only, live-default, mismatch). Also: keybind/rule semantic decision
tables (what the declared config actually does).
Anti-claim: if hyprctl is unavailable/unsupported in this session, the layer
is documented as the recipe with the file-byte evidence only.
Also: wave-1 errata applied.
Measure: >=10 claim->live pairs; divergence table; no config mutated.
