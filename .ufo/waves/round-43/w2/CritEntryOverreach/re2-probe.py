"""RE2 semantics probe for the entry's INF sentence (entry line 36).

Runs the entry's regex through RE2 full-match semantics (google-re2 Python binding, which links
the same RE2 library) with default Options, exactly as RegexMatchEngine.cpp:12 constructs it
(`m_regex = makeUnique<re2::RE2>(regex);` -- no Options argument).
"""
import re2

RX = r"^(org.omarchy.gkeep)$"
CASES = [
    "org.omarchy.gkeep",
    "org.omarchy.gkeep2",
    "orgXomarchy.gkeep",
    "org.omarchy.gkeep\n",
    "org.omarchy.gkeep\nX",
    "xorg.omarchy.gkeep",
]


def fm(pattern: str, text: str) -> bool:
    return re2.fullmatch(pattern, text) is not None


print("== google-re2 version ==")
print(getattr(re2, "__version__", "?"), re2.__file__)
opts = re2.Options()
for attr in ("dot_nl", "one_line", "log_errors", "encoding"):
    try:
        print(f"Options.{attr} = {getattr(opts, attr)}")
    except Exception as e:  # noqa: BLE001
        print(f"Options.{attr} unavailable: {e}")

print("\n== host regex under fullmatch, default Options ==")
for c in CASES:
    print(f"FULLMATCH {RX!r:34} vs {c!r:27} -> {fm(RX, c)}")

print("\n== dot semantics with default Options (C++ default dot_nl=false) ==")
for pat, text in [(r"a.b", "a\nb"), (r"a.b", "axb"), (r"a.b", "a\rb"), (r"(?s)a.b", "a\nb")]:
    print(f"FULLMATCH {pat!r:12} vs {text!r:8} -> {fm(pat, text)}")

print("\n== anchor '$' before a trailing newline ==")
for pat, text in [(r"abc$", "abc\n"), (r"abc$", "abc"), (r"^abc$", "abc\n")]:
    print(f"FULLMATCH {pat!r:12} vs {text!r:8} -> {fm(pat, text)}")
