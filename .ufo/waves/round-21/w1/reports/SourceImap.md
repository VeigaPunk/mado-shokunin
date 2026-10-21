# SourceImap — CPython `IMAP4_stream`

**Axes:** C1 operability (bounded source evidence for a stdlib process-call path); C2 calibration is not tested by this source lookup.

## Observed

Fetched the exact public CPython v3.14.8 source at <https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py> on 2026-10-21. The saved body is `.ufo/waves/round-21/w1/sources/SourceImap/imaplib-v3.14.8.py`; SHA-256 `855d205bf68e202e963db64942549b1fab17b14b594dd16694b8340d453bc74b` (72,414 bytes; 2,090 lines). Fetch details and the excerpt are recorded in `.ufo/waves/round-21/w1/sources/SourceImap/receipt.json`.

Located quote (8 whitespace-delimited tokens), `Lib/imaplib.py:1809–1812`:

> `self.process = subprocess.Popen(self.command, bufsize=DEFAULT_BUFFER_SIZE, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds=True)`

The class is `IMAP4_stream` (`:1783`). Its `__init__` (`:1795–1797`) stores `command` and initializes the parent; the `Popen` call is in `open` (`:1800–1812`), not the constructor body. `open` passes the stored command to `subprocess.Popen`, with `shell=True` and stdin/stdout pipes.

## Existing S-row coverage

No existing `corpus/SOURCES.md` row found by the exact `imaplib`/`IMAP4_stream` search covers this call site. Nearby coverage is narrower/different: S108 documents `subprocess` command-argument binding/forwarding; S113 documents process-creation entry points in `os`; S115 covers `subprocess.list2cmdline` as a formatter. None anchors the implementation of `IMAP4_stream.open` in `Lib/imaplib.py`. No SOURCES row was added; registration reserves S116 onward to L1.

## Limits

This is direct, version-pinned source evidence for the code path, not evidence that any program instantiated `IMAP4_stream`, called `open`, or ran a particular command. It does not establish runtime effects, command provenance, or host behavior. No code or transcript was executed and no tool was installed.

Confidence: high for the cited static call path; runtime occurrence and effects remain unresolved.

Report: .ufo/waves/round-21/w1/reports/SourceImap.md
