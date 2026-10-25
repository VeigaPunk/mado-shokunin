# ExecQuoteLint — quote-substring lint, round-34 admitted rows

Executor scope: for each admitted row (S201, S202), check the gate quote (the
located quote per the Gate block of
`corpus/knowledge/waybar-module-text-route-r25.md`) and the registry prose
quote cell (`corpus/SOURCES.md` column) against the committed fetch blob in
`.ufo/waves/round-34/fetch/`. Report contiguous-substring status and line
number. Run 2026-10-24.

## Method

- Gate quotes (authority, knowledge file lines 12–13):
  - S201: `$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr`
  - S202: `m_ipc.registerForIPC("activewindow", this);`
- Registry prose cells (SOURCES.md lines 203–204):
  - S201: `The backend warns when $XDG_RUNTIME_DIR/hypr is absent and falls back to /tmp/hypr`
  - S202: `The window module registers for activewindow on the event socket`
- Blobs: `.ufo/waves/round-34/fetch/S201.bin` (6550 B),
  `S202.bin` (8324 B). Both `git ls-files`-tracked, `git status` clean, last
  touched by commit `3420e82`. sha256 prefixes `799bf02f6d18ae04` (S201) and
  `5df496eb3cfe5cae` (S202) match the registry rows.
- Check: `grep -anF` (fixed-string, binary-safe) per quote per blob.

## Results

| id | text | in blob? | line |
|---|---|---|---|
| S201 | gate quote `$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr` | YES — contiguous substring | 38 |
| S201 | registry prose `The backend warns when $XDG_RUNTIME_DIR/hypr is absent and falls back to /tmp/hypr` | **NO — not a substring** | — |
| S202 | gate quote `m_ipc.registerForIPC("activewindow", this);` | YES — contiguous substring | 27 |
| S202 | registry prose `The window module registers for activewindow on the event socket` | **NO — not a substring** | — |

Evidence lines as they appear in the blobs:

```
S201.bin:38:    spdlog::warn("$XDG_RUNTIME_DIR/hypr does not exist, falling back to /tmp/hypr");
S202.bin:27:  m_ipc.registerForIPC("activewindow", this);
```

## Prose cells that are NOT substrings of the bytes (finding)

Both registry quote cells are paraphrases, not verbatim spans:

- S201: `The backend warns when $XDG_RUNTIME_DIR/hypr is absent and falls back to /tmp/hypr`
- S202: `The window module registers for activewindow on the event socket`

The frozen gate quotes are the located quotes per the Gate block and both
verify as contiguous substrings (lines 38 and 27). The registry "quote"
column therefore holds descriptive prose, not extractable quote spans; any
consumer treating that cell as a verbatim quote will fail substring
verification against the committed bytes.
