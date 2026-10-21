# ImapStream — C1 falsification

**Verdict:** The frozen expectation is warranted for the exact one-element `command` list. The current rule is not keyed to the fixture's `loginctl` text, but it is an API-specific rule and its handling is not general to `IMAP4_stream` command sequences: one nearby two-element variant is misclassified because the scanner joins the list as command arguments instead of applying `Popen(shell=True)` sequence semantics.

## Observed facts

- Frozen case: `oracle/expected.json:215-232` selects the primary `ImapStream` fixture (`620e256886cb637436614b23542ad89564081732484d2fc8e3a6752223ff6743`) and expects `live_probe`, normalized command `loginctl`, evidence `observed`. `w1/oracles/ImapStream.json` records the underlying rule as `loginctl:list-sessions`; the frozen normalization explicitly removes that classifier-rule suffix from the command field.
- CPython source pinned by the w1 receipt is v3.14.8, SHA-256 `855d205bf68e202e963db64942549b1fab17b14b594dd16694b8340d453bc74b`. `IMAP4_stream.__init__` binds `self.command` and calls `IMAP4.__init__` (`w1/sources/SourceImap/imaplib-v3.14.8.py:1783-1797`). The base initializer calls `self.open(...)` (`:217-224`); dynamic dispatch reaches `IMAP4_stream.open`, which calls `subprocess.Popen(self.command, ..., shell=True)` (`:1800-1812`).
- On POSIX, the official Python 3.14 subprocess documentation says that with `shell=True`, a sequence is equivalent to `Popen(['/bin/sh', '-c', args[0], args[1], ...])`; items after `args[0]` are arguments to the shell itself. With the frozen one-item list `['loginctl']`, the shell command text is exactly `loginctl`.
- systemd `src/login/loginctl.c` registers `verb_list_sessions` as `VERB_DEFAULT_NOARG(..., "list-sessions", ...)`; `src/shared/verbs.h` defines that macro with the `VERB_DEFAULT` flag. Thus no-argument `loginctl` selects its read-only session-listing default. This supports class `live_probe` and rule `loginctl:list-sessions`. The `observed` label is a fully resolved static path, not a claim that this transcript was executed.
- Current `tools/mado-tripwire.py` bytes at probe time: SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. The existing `oracle-candidate.json` receipt is measured at commit `843d301d1b17af78427918f7845af336b2218de0`; I did not use it as proof for the current bytes.

## Nearby variant and scanner result

I created inert fixture `.ufo/waves/round-21/w2/fixtures/AtkImapStream/shell-sequence.jsonl`, SHA-256 `bb6160ae3d03e5bc92015da125c247032424248accf3a9061ba3c8099fa0c325`. It contains the frozen call as a baseline and this single variant:

```python
import imaplib

imaplib.IMAP4_stream(["loginctl", "disable-linger"])
```

Using `measure.py`'s `scan` API only (scanner subprocess bounded by its 384 MiB address-space limit and 15 s timeout; neither snippet nor shell payload was executed), current scanner output was:

- Baseline: `live_probe`, command `loginctl`, rule `loginctl:list-sessions`, evidence `observed`.
- Variant: `host_mutation`, command `loginctl disable-linger`, rule `loginctl:disable-linger`, evidence `observed`.
- Probe totals: exit 1 (unpermitted findings), `live_probe=1`, `host_mutation=1`, `eval_unparsed=0`, `unparsed_spawns=0`.

**Counterexample inference:** For the variant, CPython passes `loginctl` as the shell command string and `disable-linger` as the shell's `$0`; the command string does not expand `$0`, so `loginctl` receives no verb. Its default remains `list-sessions` (`live_probe`), not `disable-linger` (`host_mutation`). The observed scanner output is therefore a false-positive class/command for this nearby input, not a reason to alter the frozen one-item expectation.

## Generality, confidence, and gaps

`spawn_path()` explicitly recognizes the canonical symbol `imaplib.IMAP4_stream` (`tools/mado-tripwire.py:1540-1546`), then the spawn path converts a literal list with `shlex.join(argv)` (`:2359-2369`). This is not a comparison against the literal fixture command `loginctl`; it is a special case for this stdlib API followed by generic command classification. However, joining the entire list as an executable argv conflicts with that API's `shell=True` behavior when the list has additional elements. **Confidence: high** for the frozen one-item result and the two-item counterexample, grounded in the pinned CPython source, official subprocess documentation, systemd verb registration, and the bounded scanner output. This is one counterexample, not a global assessment of other `IMAP4_stream` inputs.

No LSP device was mounted (`read xd://lsp` returned “No such tool”); source search located symbols, while conclusions rely on the read source bodies and primary documentation, not grep as semantic proof. No runtime command or transcript snippet was executed; no tools were installed or updated. No expectation or production file was changed.

Report: `.ufo/waves/round-21/w2/reports/AtkImapStream.md`
