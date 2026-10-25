# ExecAssimIdGuard — round-39 assimilation collision check

## Exact check and retained outputs

Ran the assigned §10 pipeline from `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/ExecAssimIdGuard/` against registry `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` and staged file `/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md`.

The exact `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' ... | grep -oE 'S[0-9]+' | sort` pipelines and `comm -12 reg-ids staged-ids > collisions` completed (shell command exit 0). Evidence files in this seat directory: `reg-ids`, `staged-ids`, `collisions`, `collision-count.txt`, `free-ids.txt`, `indented-registry.txt`, `indented-staged.txt`, `indented-reg-ids`, `indented-collisions`, `columnzero-reg-ids`, `columnzero-collisions`, `indentation-result.txt`.

### ID lists

`reg-ids` (211 IDs):

```text
S001–S189, S196, S201–S217, S221, S253, S258, S277
```

`staged-ids` (147 IDs):

```text
S203–S349
```

The ranges above are a compact transcription of the literal, ascending lists retained in the files; endpoints are inclusive and omitted IDs are not present.

Collision count: **19** (`S203` through `S221`, inclusive); literal collision IDs are retained in `collisions`.

### Indentation fixture

Scratch registry row was exactly `  | S002 |`; staged fixture contained `S002`. The 0–3-space pattern produced `indented-collisions` containing `S002` (count 1). The comparison pattern requiring column zero produced an empty `columnzero-collisions` (count 0): false green demonstrated.

### Held-ID check

Ran `grep -nE '^ {0,3}\\|[[:space:]]*S(218|219|220)([[:space:]]|\\|)'` against the registry: no output, exit 1 (recorded as no matching held rows in `free-ids.txt`). Thus S218/S219/S220 are free against the current registry. This does not establish absence from other repositories or unstaged materials.

No tools installed. No files outside this seat directory were written. The staged file was read only.

Report: `.ufo/waves/round-39/w1/ExecAssimIdGuard.md`