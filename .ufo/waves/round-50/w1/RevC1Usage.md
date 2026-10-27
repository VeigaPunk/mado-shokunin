# RevC1Usage — SHONEN box 3 for C1: can an agent run tools/mado-keysym.py from its docstring alone?

Carried round-49 w2 item, retargeted to the LANDED tool. Docstring-only discipline held: the run below used only
`tools/mado-keysym.py`'s docstring plus the two inputs the item names (`~/.config/hypr/input.conf`, the host's own binds).

**Verdict: YES for the tool — NO for the host-faithful run.** Every invocation the docstring documents ran as written, and the
tool matched the judge byte-for-byte in 11/11 pairs (stdout + exit status). But two steps the box-3 question depends on —
deriving the host keymap from `~/.config/hypr/input.conf` and spelling `--keysym ARG` canonically — are fully implicit in the
docstring. Without them a docstring-only agent (a) gets rc 2 on most bind spellings (3 of my 5), and (b) cannot detect a
wrong-FILE run at all, because the docstring's contract (tool == judge *on the same FILE*) is satisfiable by a keymap that is
not the host's. Both steps exist only in the round-49 SKILL draft (`~/.ufo/waves/round-49/w1/ScrSkill/skill-section.md`).

## Identity and environment (receipts in this seat dir)

- Landed tool `tools/mado-keysym.py` sha256 `dcc13cce3b7134946208116cd98599fb8f56a2b81fc6f26b9598ac5429b40265` = the round-49
  candidate/registration bytes; mode 0755 (bare `./mado-keysym.py` works); host python 3.14.8.
- Judge `/usr/lib/xkbcommon/xkbcli-how-to-type` sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`
  (`judge-sha256.txt`) = the SKILL draft's recorded `f6c0b122…` (`skill-section.md:15`). libxkbcommon 1.13.2-1,
  xkeyboard-config 2.48-1 (`pacman -Q`, read-only) = docstring `tools/mado-keysym.py:10`.
- Keymap: `/usr/lib/xkbcommon/xkbcli-compile-keymap --layout br --options compose:caps > host-br.xkb` → rc 0, 73079 bytes,
  sha256 `efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81` (`rmlvo.txt`, `host-br.xkb`) — equal to the SKILL
  draft's recorded host keymap digest `efd487a3…` (`skill-section.md:20`, `:70`), so the docstring-following derivation
  reproduced the round-48/49 keymap bytes exactly.
- Host binds (`hyprctl binds -j`, read-only): 192 binds; 42 with empty `key` + keycode, 6 `mouse*`, 2 `switch:`;
  60 unique name-shaped `key` strings, of which 58 are keysym names (`mouse_down`/`mouse_up` are Hyprland event names that a
  naive name regex swallows — filter subtlety; `binds-shape-counts.txt`, `binds-keysyms.txt`).
- All runs under scratch env: `HOME`/`XDG_*`/`TMPDIR` pointed at dirs under the seat scratch; scratch removed after receipts
  were copied. No tool installed this seat (no pacman transaction; `pacman -Q` query only).

## Executed runs (all receipts in this seat dir)

- `--selftest`: last line `MADO_KEYSYM_SELFTEST: 38/38 passed`, rc 0, stderr 0 bytes; scratch file set byte-identical
  before/after (`selftest.out`, `selftest.err`, `scratch-before.txt`, `scratch-after.txt`).
- 5 keysyms the host binds use, in the binds' own spelling (`parity-summary.txt`, `tool-*`/`judge-*` pairs):
  - `SLASH`, `RETURN`, `TAB` → tool rc 2 = judge rc 2, stdout empty on both, stderr line 1 identical
    `ERROR: Failed to convert argument to keysym` (`tool-SLASH.err`, `judge-SLASH.err`).
  - `E` → rc 0, 243 bytes, stdout MATCH, stderr same. `XF86AudioMute` → rc 0, 187 bytes, MATCH.
- Canonical spellings of the three refusals: `slash` → rc 0 MATCH, first row `24  AD01  1  Portuguese (Brazil)  3  [ Mod5 LevelThree ]`;
  `Return` → `36  RTRN  1 … 1  [ ]`; `Tab` → `23  TAB  1 … 1  [ ]` (`tool-slash.out`, `tool-Return.out`, `tool-Tab.out`).
- ARG forms the docstring claims (`tools/mado-keysym.py:18-19`): `0x2f` and decimal `47` both print `keysym: slash (0x002f)`
  on judge and tool, MATCH; `nosuchsym` → rc 2 both, empty stdout (`judge-0x2f.out`, `tool-47.out`, `tool-nosuchsym.err`).
- Equals-form `--keymap=FILE`: accepted by the tool — with `E` rc 0 and output byte-equal to the space-form run; with `TAB`
  the rc 2 was the resolution refusal, not an argument-parse error (`tool-eqformE.out`, `tool-eqform.err`).
- Total: 11/11 tool↔judge pairs byte-equal on stdout with equal exit status (7 rc 0, 4 rc 2); 2 equals-form consistency runs.

## Findings — steps the docstring left implicit

1. **[main] Canonical-spelling trap (actionable).** The judge resolves `--keysym` with `xkb_keysym_from_name` with no flags —
   exact match only (`tools/mado-keysym.py:19`, refusal class `:33-34`) — so the host's own bind spellings `SLASH`, `RETURN`,
   `TAB` (as stored by `hyprctl binds -j`) all exit 2, while Hyprland itself resolves bind names case-insensitively
   (`skill-section.md:43`, citing `KeybindManager.cpp:710-711`). The docstring states the resolver but never warns that bind
   spellings are usually not canonical keysym spellings. A docstring-only agent that reads rc 2 as "the bind is dead" is
   misled; the canonical respelling step exists only in the SKILL draft. Evidence: the 3 refusals vs 3 rc-0 canonical runs above.
2. **[main] Host-keymap fidelity is unverifiable from the docstring's own contract.** Parity is defined on one FILE
   (`tools/mado-keysym.py:20-21`); a FILE built from wrong RMLVO (e.g. `--layout us`) still passes 11/11 against the judge.
   Nothing in the docstring derives FILE from Hyprland's config (the docstring names no config path; grep for
   `hypr|input\.conf|binds` in the docstring hits only the context prose at `:7-9`), and no digest check is specified. The
   SKILL draft carries both the command (`skill-section.md:18`) and the digest cross-check (`:20`, `:70`); the docstring
   carries neither. One sentence in the docstring ("derive RMLVO from the compositor's `input:kb_*` values; pin FILE's
   sha256") would close it.
3. **[minor] RMLVO derivation details are implicit**: `kb_layout = br` → `--layout br` (`~/.config/hypr/input.conf:10`),
   `kb_options = compose:caps` → `--options compose:caps` (`input.conf:11`) with the inline comment `# ,grp:alts_toggle`
   stripped; absent `kb_variant`/`kb_model` → flags omitted. Verified only by the outcome (rc 0 + digest equal to the
   recorded host keymap), which is evidence, not documentation.
4. **[minor] Host-bind enumeration is implicit**: "keysyms the host binds use" requires a read-only `hyprctl binds -j` plus a
   three-form filter of the `key` field (keysym / empty-key+keycode / mouse+switch names), and the name-shape filter must
   exclude `mouse_down`/`mouse_up`. Docstring silent; SKILL draft covers the forms (`skill-section.md:45` row and census).
5. **[cosmetic] Docstring self-contradiction on `--selftest` writes**: `:4-5` says "writes no file" and `:23` says "Hermetic
   cases under $TMPDIR"; the code references no `tempfile`/`mkdtemp`, and with `TMPDIR` set the selftest created no file
   (identical before/after listings). `:23` is vestigial; `:4-5` is the true behavior.
6. **[verified non-gaps]** Full binary paths are in the docstring (`:10`, `:17`); the host has no `/usr/lib/xkbcommon/xkbcli`
   multi-call binary, so the docstring's full-path style is required and correct. Refusals behave exactly as `:27-34`
   documents (rc 2, empty stdout; stderr differs only by the judge's usage banner — the docstring's "stdout + exit status"
   contract at `:15-16` is the right comparison and held in 11/11). `--help`/`--selftest` lines `:22-25` ran as written.

Severity: finding 1 and 2 are candidate fixes for the SKILL/docstring plane (round-50 SKILL landing or a docstring erratum);
neither invalidates round-49 C1 — the landed contract (parity on a given FILE) held in every pair I ran, and the round-49
bytes are unchanged (`dcc13cce…0265`).

Residual risk: one keymap (host `br` + `compose:caps`), 5 bind keysyms + canonical/forms variants; multi-layout, fallback and
keycode-bind rows of the SKILL rest on the draft's pinned sources, not on my runs. No input injected; compositor touched only
by allowed reads (`hyprctl version`, `hyprctl binds -j`).

Report: .ufo/waves/round-50/w1/RevC1Usage.md
