#!/usr/bin/env python3
"""Falsify16 attack driver: C2 source quote/pin binding bypass.

Attacked clause (registration.md C2): "each maps to an opened-this-round `S###`
row, a pin path/revision and exact located quote <=25 words".

Method: drive the COMMITTED round-51 binding machinery (quality/counters
/c2-r51-dispatch-entry.py, the house pattern the round-52 counter clones for
"row/pin/quote bindings") against forged entry texts and REAL pinned source
bytes (Hyprland-KeybindManager.cpp @ HEAD == frozen base 85d57a818c3707397e21c840b6498b105ba798aa).

Run: python3 attack_quote_pin_binding.py <lane-repo> <outdir>
"""
import importlib.util
import pathlib
import sys

LANE_COUNTER = "quality/counters/c2-r51-dispatch-entry.py"
PIN = "Hyprland-KeybindManager.cpp"
FETCH = ".ufo/waves/round-51/fetch"


def load_counter(repo):
    spec = importlib.util.spec_from_file_location("c2r51", pathlib.Path(repo) / LANE_COUNTER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def forged_entry(binding_line):
    return (
        "# Forged dispatcher entry (Falsify16 fixture)\n\n"
        "Forged prose paragraph. This fixture is not a real knowledge entry.\n\n"
        "source: S364 - forged row citation for binding attack - "
        "https://example.invalid/src - code - forged\n\n"
        + binding_line + "\n\n"
        "## Pin manifest\n\n"
        "All paths relative to `.ufo/waves/round-51/fetch/`.\n\n"
        "| pin | file | row |\n"
        "|---|---|---|\n"
        "| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | S364 |\n"
    )


def bind_detail(mod, repo, rev, entry, rowid="S364"):
    """Replicate clause_b wiring to expose the exact matched quote (or fail reason)."""
    prose = [l for l in mod.unfenced(entry.splitlines()) if not l.strip().startswith("|")]
    anchored = [l for l in prose if mod.re.search(r"\b%s\b" % rowid, l)]
    man = mod.manifest(entry)
    pins = {p.rsplit("/", 1)[-1] for p in mod.ls_files(repo, rev, FETCH)}

    def loader(name):
        return mod.show(repo, rev, FETCH + "/" + name)

    return mod.bind_row(rowid, anchored, man, pins, loader)


def run_variant(mod, repo, rev, name, binding_line, expect_bound, note):
    # clause_b only anchors lines that NAME the rowid; mirror house style.
    anchored_line = "S364 " + binding_line
    entry = forged_entry(anchored_line)
    ok, detail = mod.clause_b(repo, rev, entry)
    bound_t, reason = bind_detail(mod, repo, rev, entry)
    bound = ok == 1
    expected = "BOUND " if expect_bound else "unbound"
    verdict = "BOUND " if bound else "unbound"
    if bound == expect_bound:
        result = "as-expected"
    elif bound:
        result = "BYPASS-DEMO"
    else:
        result = "FALSE-REJECT"
    return {
        "name": name, "line": anchored_line, "ok": ok, "detail": detail,
        "matched": bound_t[3] if bound_t else None, "reason": "" if bound_t else reason,
        "bound": bound, "expect_bound": expect_bound, "expected": expected,
        "verdict": verdict, "result": result, "note": note, "entry": entry,
    }


def main():
    repo, outdir = sys.argv[1], pathlib.Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "fixtures").mkdir(exist_ok=True)
    mod = load_counter(repo)
    # Attack target is the per-row bind_row mechanism, not the >=MIN_ROWS policy gate
    # (round 52 sets its own proposition-count rule). Isolate the binding verdict.
    mod.MIN_ROWS = 1
    rev = "HEAD"

    blob = mod.show(repo, rev, FETCH + "/" + PIN)
    text = mod.text_of(blob)
    full_hay = mod.collapse(text)
    hay785 = mod.collapse(mod.at_lines(blob, 785, 785))
    assert "m_dispatchers" in hay785

    # Real contiguous word windows from the pinned bytes (mid-file, lines 798-810).
    mid_words = mod.collapse("\n".join(text.splitlines()[797:810])).split()
    quote26 = " ".join(mid_words[10:36])
    quote24 = " ".join(mid_words[10:34])
    n26, n24 = len(quote26.split()), len(quote24.split())
    assert n26 == 26 and n24 == 24, (n26, n24)
    assert quote26 in full_hay and quote24 in full_hay
    assert quote26 not in hay785 and quote24 not in hay785

    fabricated34 = (
        "the dispatcher table is consulted only when the moon is full and the config "
        "parser has retired for the night while every key press takes the long way "
        "around the event queue twice today"
    )
    assert len(fabricated34.split()) == 34
    assert fabricated34 not in hay785

    fabricated10 = "the parser retires before every press"
    assert fabricated10 not in hay785

    HONEST = "`const auto DISPATCHER = m_dispatchers.find(k->mouse ? \"mouse\" : k->handler);`(Hyprland-KeybindManager.cpp:785)"

    variants = [
        ("V0-honest-green",
         "press path " + HONEST + " which we cite honestly.",
         True,
         "sanity: real house-style paired quote at the exact line; must bind"),
        ("V1-overlength-fallback-token",
         "The table `m_dispatchers` decides; claim text `" + fabricated34
         + "`(Hyprland-KeybindManager.cpp:785) ends here.",
         True,
         "paired quote is 34 words (>25) and fabricated, yet binds via the unrelated "
         "1-word backtick `m_dispatchers`; the <=25-word limit is filter-only, not a failure"),
        ("V2a-overlength-fragments-itself",
         "Claim text `" + quote26 + "`(Hyprland-KeybindManager.cpp:1-975) ends here.",
         True,
         "26-word paired quote at whole-file range binds through an incidental 10-word "
         "fragment between the internal double quotes of its own text (DQUOTE_RE path); "
         "paired-quote length never enforced"),
        ("V2b-wholefile-range-binds",
         "Claim text `" + quote24 + "`(Hyprland-KeybindManager.cpp:1-975) ends here.",
         True,
         "24-word quote from lines ~798-810 'verifies' against locator :1-975 (whole "
         "file): exact located quote is vacuous when the cited range spans the file"),
        ("V2c-same-quote-narrow-range-fails",
         "Claim text `" + quote24 + "`(Hyprland-KeybindManager.cpp:785) ends here.",
         False,
         "same 24-word quote at an honest narrow locator fails quote_not_at_pin: the "
         "contrast proving only the unbounded range 'located' it"),
        ("V2d-overlength-plus-fallback-wholefile",
         "The token `m_dispatchers` matters; claim text `" + quote26
         + "`(Hyprland-KeybindManager.cpp:1-975) ends here.",
         True,
         "26-word quote plus fallback at whole-file range binds: predicate's "
         "quote<=25 words defeated on both axes at once"),
        ("V3-fabricated-narrow-fails",
         "Claim text `" + fabricated10 + "`(Hyprland-KeybindManager.cpp:785) ends here.",
         False,
         "harness control: fabricated <=25-word quote at :785 must fail"),
    ]

    lines = []
    lines.append("Falsify16 C2 quote/pin binding attack -- committed r51 machinery vs forged entries")
    lines.append("lane repo: %s" % repo)
    lines.append("scored rev: %s (frozen base 85d57a818c3707397e21c840b6498b105ba798aa)" % rev)
    lines.append("counter: %s (clause_b/bind_row = row/pin/quote binding)" % LANE_COUNTER)
    lines.append("pin bytes: %s/%s (%d lines, real pinned source)" % (FETCH, PIN, len(text.splitlines())))
    lines.append("quote26 words=%d quote24 words=%d fabricated34 words=%d" % (n26, n24, len(fabricated34.split())))
    lines.append("")
    for name, bline, expect, note in variants:
        r = run_variant(mod, repo, rev, name, bline, expect, note)
        (outdir / "fixtures" / (name + ".md")).write_text(r["entry"])
        lines.append("== %s" % name)
        lines.append("forged line: %s" % r["line"])
        lines.append("clause_b -> ok=%d detail=%s" % (r["ok"], r["detail"]))
        lines.append("matched quote: %r" % r["matched"])
        lines.append("bound=%s expected=%s  ==> %s" % (r["bound"], r["expected"], r["result"]))
        lines.append("note: %s" % r["note"])
        lines.append("")
    out = "\n".join(lines)
    (outdir / "results.txt").write_text(out)
    print(out)


if __name__ == "__main__":
    sys.exit(main())
