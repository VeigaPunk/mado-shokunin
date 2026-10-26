#!/usr/bin/env python3
"""Grep every quote used in findings.md against the seat's receipts.

Each pair is (quote, receipt file). Whitespace is normalised so a quote that spans a
line break in the source still matches. Exit 0 iff every quote is found.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "receipts")

PAIRS = [
    # contract (frozen counter docstring) and the reference docstring
    ("a tiled window never reads it", "ref-docstring.txt"),
    ("The effect is the first", "contract-excerpt.txt"),
    ("first token of field 0", "contract-excerpt.txt"),
    ("it has exactly two fields; field 0 has exactly two argument tokens", "contract-excerpt.txt"),
    ("field 1 fully matches", "contract-excerpt.txt"),
    ("TILED (not floating)", "contract-excerpt.txt"),
    ("Any other size or float line adds one to `unsupported`.", "contract-excerpt.txt"),
    ("Rules apply in file order: the last matching `size` rule gives want", "contract-excerpt.txt"),
    ("its class holds no character below U+0020 and `re.fullmatch(REGEX, class)` succeeds", "contract-excerpt.txt"),
    ("at most 1048577 bytes", "contract-excerpt.txt"),
    ("`--rules V` one or more times", "contract-excerpt.txt"),
    ("tokens being separated by runs of spaces and tabs only", "contract-excerpt.txt"),
    ("a line is stripped of spaces and tabs at both ends", "contract-excerpt.txt"),
    ("ignored and counted nowhere", "contract-excerpt.txt"),
    # pinned lane sources
    ("re2::RE2::FullMatch(other, *m_regex) != m_negative", "pinned-cites.txt"),
    ("static_.size = expr", "pinned-cites.txt"),
    ("if (target->window() && target->window()->m_firstMap)", "pinned-cites.txt"),
    ("w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL)", "pinned-cites.txt"),
    ("m_isFloating", "pinned-cites.txt"),
    # seat-fetched upstream sources at the pinned commit
    ("const bool FIRST_IS_PROP = el.starts_with(\"match:\");", "upstream-cites.txt"),
    ("spacePos = el.find(' ')", "upstream-cites.txt"),
    ("missing a value", "upstream-cites.txt"),
    ("el.substr(spacePos + 1)", "upstream-cites.txt"),
    ("m_rules.emplace_back(std::move(rule))", "upstream-cites.txt"),
    ("return m_rules;", "upstream-cites.txt"),
    ("listKeysForSpecialCategory(\"windowrule\")", "upstream-cites.txt"),
    ("windowrulev2 is deprecated", "upstream-cites.txt"),
    ("line = trim(line)", "upstream-cites.txt"),
    ("trim(std::string_view{m_inString}.substr(argBegin", "upstream-cites.txt"),
    ("any character, possibly including newline (s=true)", "upstream-cites.txt"),
    # docs (0.54 legacy-syntax page and the current page note)
    ("Rules are evaluated top to bottom", "docs-cites.txt"),
    ("windowrule = match:class my-window, border_size 10", "docs-cites.txt"),
    ("You can have as many props and effects per rule as you please", "docs-cites.txt"),
    ("windowrule = match:class kitty, rounding 10", "docs-cites.txt"),
    ("windowrule = no_blur on, match:class firefox", "docs-cites.txt"),
    ("Effects will be processed from top to bottom", "docs-cites.txt"),
    ("Resizes a floating window to a given size. Two expressions are space-separated.", "docs-cites.txt"),
    ("Looking for the old hyprlang syntax", "docs-cites.txt"),
    # host bytes
    ("windowrule = match:class (Alacritty|kitty|foot), scroll_touchpad 1.5", "host-rules.txt"),
    ("windowrule = size 1100 700, match:class steam, match:title Steam", "host-rules.txt"),
    ("windowrule = size 600 338, match:tag pip", "host-rules.txt"),
    ("windowrule = size 875 600, match:tag floating-window", "host-rules.txt"),
    ("windowrule = size 420 500, match:class ^(org.omarchy.gkeep)$", "host-rules.txt"),
    ("source = ~/.local/state/omarchy/toggles/hypr/*.conf", "host-rules.txt"),
]

OUTPUT_CHECKS = [
    # (needle, case name in ref-cases.txt, why)
    ("other=1", "false_agree_matchfirst", "match-first line is binned as other"),
    ("verdict=AGREE", "false_agree_matchfirst", "false AGREE on the earlier size rule"),
    ("unsupported=1", "false_agree_multieffect", "multi-effect line is binned as unsupported"),
    ("NO_SIZE_RULES", "match_first", "lone match-first size line is invisible"),
    ("NO_SIZE_RULES", "inline_comment", "inline comment hides the rule"),
    ("NO_SIZE_RULES", "double_space_after_match_absent", "placeholder never used"),
    ("effect=size arg=1x2", "tab_separated", "tab fields are accepted by the tool"),
    ("verdict=AGREE", "double_space_after_match", "double space swallowed before the regex"),
    ("rules=2", "duplicate_rules", "repeated --rules is processed twice"),
]


NUM = re.compile(r"^\s*\d+\t")


def norm(s, strip_numbers=False):
    if strip_numbers:
        s = "\n".join(NUM.sub("", line) for line in s.splitlines())
    return re.sub(r"\s+", " ", s)


def main():
    text = norm(open(os.path.join(HERE, "findings.md"), encoding="utf-8").read())
    bad = 0
    for quote, receipt in PAIRS:
        path = os.path.join(R, receipt)
        body = norm(open(path, encoding="utf-8", errors="replace").read(),
                    strip_numbers=receipt in ("contract-excerpt.txt", "ref-docstring.txt"))
        ok = norm(quote) in body
        where = "receipt"
        if not ok and norm(quote) in text:
            where = "findings-only"
        print(("PASS " if ok else "FAIL ") + receipt + " :: " + quote[:90])
        bad += 0 if ok else 1
    cases = open(os.path.join(R, "ref-cases.txt"), encoding="utf-8").read()
    blocks = {}
    cur = None
    for line in cases.splitlines():
        if line.startswith("## case "):
            cur = line[len("## case "):].strip()
            blocks[cur] = []
        elif cur is not None:
            blocks[cur].append(line)
    for needle, case, why in OUTPUT_CHECKS:
        if case.endswith("_absent"):
            continue
        body = "\n".join(blocks.get(case, []))
        ok = needle in body
        print(("PASS " if ok else "FAIL ") + "ref-cases.txt[" + case + "] :: " + needle + " (" + why + ")")
        bad += 0 if ok else 1
    print("QUOTES: %d checks, %d failed" % (len(PAIRS) + len([c for c in OUTPUT_CHECKS if not c[1].endswith('_absent')]), bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
