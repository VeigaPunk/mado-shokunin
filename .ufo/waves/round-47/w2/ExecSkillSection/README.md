# ExecSkillSection seat directory (w2, round 47)

Falsification of the SKILL section draft `.ufo/waves/round-47/w1/ScrSkill/section.md` run as written against the
L1 reference `.ufo/waves/round-47/l1-draft/mado-terminal.py`. Findings: `../ExecSkillSection.md`.

Everything here is reproduced by three scripts; each takes a work dir as `$1`, keeps `XDG_CACHE_HOME` inside it,
and never starts a terminal (resolver invocations are print modes only).

| file | what it is |
|---|---|
| `run-section.sh` → `receipts/section-as-written.txt` | every command of the section, host env, reference substituted |
| `run-probes.sh` → `receipts/section-probes.txt` | hermetic probes of the symptom-table rules, tool vs resolver bytes |
| `run-divergences.sh` → `receipts/divergences.txt` | H1–H8: where the text and the tool diverge |
| `verify-quotes.sh` + `receipts/quotes.tsv` → `receipts/quotes-verified.txt` | every quoted fragment greped at its stated `file:line`, ≤ 25 words |
| `receipts/script-locators.txt` | `grep -n` locators in `/usr/bin/xdg-terminal-exec` (sha256 89f2be9a…27ac) |
| `receipts/strace-print.txt` | one print run: 1 execve (python3), no clone/fork, no socket |

Run, e.g.: `./run-section.sh /fast/scratch/hyaku/mado-r47/ExecSkillSection/run` (about 4 s).
