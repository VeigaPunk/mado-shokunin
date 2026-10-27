# R54Seat23 — C2 adversarial critique (item 23)

## Axes
Coverage: integrity and distinctness of the required host-evidence joins. Operability: whether the frozen predicate's citation rule admits an easy-to-reproduce false pass.

## Counterexample: one citation copied across separate source labels can be mistaken for two joins

PRED-C2-r54 clause (c) requires “at least two host join citations among the frozen host set” (claims-frozen.md:63–65). Registration specifies “≥2 as `file:line`” and enumerates six autostart locations plus one binding and one idle-script location (registration.md:71–76). It does not explicitly say citations must denote distinct source locations. A parser that counts citation occurrences, or distinct textual `file:line` strings without normalizing equivalent path spellings, can admit repeated evidence as two joins. The concrete repeated-identical citation case is already reported by R54Seat22; this attack is distinct: alias spelling of the *same* frozen location, e.g. a tilde path and its expanded home path, can evade a string-set deduplication while still providing only one underlying join:

```text
Host joins: `~/.config/hypr/bindings.conf:2`; `/home/vgpnk/.config/hypr/bindings.conf:2`.
```

The frozen set names the tilde form only. A permissive implementation may count both as members only if it canonicalizes aliases; a literal allowlist correctly rejects the expanded path. The underlying ambiguity remains: even when both are syntactically allowed by an alias-aware parser, they identify one file/line, not two independently distinct joins. No current counter was present to test this against an implementation, so this is a frozen-contract/parser counterexample, not an observed implementation defect.

## Evidence and commands

- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/claims-frozen.md` — lines 55–65 define clause (c) and its threshold as two citations among the host set.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/registration.md` — lines 71–87 give eight allowed locations and six controls; none requires distinct normalized identities.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/w1/R54Seat22.md` — confirmed another seat covers literal duplicate citation occurrences; this report tests path-alias identity instead.
- `read /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r54-uwsm-entry.py` — path absent.
- `bash: test -e /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r54-uwsm-entry.py && printf 'present\n' || printf 'absent\n'` (cwd `/home/vgpnk/Projects/shokunin`) → `absent`.

Attack predicate: PRED-C2-r54 clause (c), citation identity and host-join count; registration.md:71–90. No predicate changes proposed.

## Smallest safe correction

At implementation time, accept only exact frozen host-location identifiers and count a set of canonical `(file, line)` locations, not citation occurrences or path spellings. Require at least two distinct identifiers. If the contract must remain frozen, treat this as a parser acceptance condition rather than silently changing the frozen sentence. Do not read host files or expand home paths: the static-only boundary and frozen-host-set contract do not authorize that.

## Report trailer

Lane-relative report: `.ufo/waves/round-54/w1/R54Seat23.md`. No tool installs/updates. No scratch artifacts, fixture, git/jj mutation, producer execution, host/config/service/compositor mutation, package query, or source-repository writes.