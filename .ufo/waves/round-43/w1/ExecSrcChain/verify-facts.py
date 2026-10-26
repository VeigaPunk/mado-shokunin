#!/usr/bin/env python3
"""Verify every row of facts.md against the pinned receipts.

For each row: check the receipt's sha256, check the 1-based line exists, check the
quote occurs verbatim in that line (grep semantics: fixed-string, single line), check
the quote is <= 25 words. Prints one line per row plus a tally.

Run: python3 verify-facts.py            (writes nothing)
"""
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
FETCH = HERE.parent.parent / "fetch"

# id | receipt file | sha256 | line | quote
ROWS = [
    # --- S290 Hyprland-RegexMatchEngine.cpp (hyprwm/Hyprland v0.56.2) ---
    ("F1", "Hyprland-RegexMatchEngine.cpp", "8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282", 7,
     'if (regex.starts_with("negative:")) {'),
    ("F2", "Hyprland-RegexMatchEngine.cpp", "8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282", 9,
     'm_regex    = makeUnique<re2::RE2>(regex.substr(9));'),
    ("F3", "Hyprland-RegexMatchEngine.cpp", "8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282", 16,
     "return re2::RE2::FullMatch(other, *m_regex) != m_negative;"),
    # --- S291 Hyprland-WindowRuleApplicator.cpp ---
    ("F4", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 390,
     "static_.floating = std::get<bool>(value);"),
    ("F5", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 394,
     "static_.floating = !std::get<bool>(value);"),
    ("F6", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 421,
     "case WINDOW_RULE_EFFECT_SIZE: {"),
    ("F7", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 422,
     "const auto& expr = std::get<Math::SExpressionVec2>(value);"),
    ("F8", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 424,
     "static_.size.reset();"),
    ("F9", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 426,
     "static_.size = expr;"),
    ("F10", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 183,
     "if (VEC->x < 1 || VEC->y < 1) {"),
    ("F11", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 188,
     "m_maxSize.first = Types::COverridableVar(*VEC, Types::PRIORITY_WINDOW_RULE);"),
    ("F12", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 190,
     "if (*PCLAMP_TILED || m_window->m_isFloating)"),
    ("F13", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 191,
     "m_window->clampWindowSize(std::nullopt, m_maxSize.first.value());"),
    ("F14", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 218,
     "m_minSize.first = Types::COverridableVar(*VEC, Types::PRIORITY_WINDOW_RULE);"),
    ("F15", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 219,
     "if (*PCLAMP_TILED || m_window->m_isFloating)"),
    ("F16", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 220,
     "m_window->clampWindowSize(m_minSize.first.value(), std::nullopt);"),
    # --- S292 Hyprland-DefaultFloatingAlgorithm.cpp ---
    ("F17", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 16,
     "constexpr const Vector2D DEFAULT_SIZE = {640, 400};"),
    ("F18", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 53,
     "WINDOW->sizeAnimation()->setValueAndWarp(DESIRED_GEOM ? DESIRED_GEOM->size : DEFAULT_SIZE);"),
    ("F19", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 55,
     "if (WINDOW->m_ruleApplicator->static_.size) {"),
    ("F20", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 56,
     "const auto COMPUTED = WINDOW->calculateExpression(*WINDOW->m_ruleApplicator->static_.size);"),
    ("F21", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 60,
     "windowGeometry.w = COMPUTED->x;"),
    ("F22", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 61,
     "windowGeometry.h = COMPUTED->y;"),
    ("F23", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 64,
     "WINDOW->positionAnimation()->setValueAndWarp(*COMPUTED);"),
    ("F24", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 79,
     "if (WINDOW->m_ruleApplicator->static_.center.value_or(false)) {"),
    ("F25", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 90,
     "if (!posOverridden && (!DESIRED_GEOM || !DESIRED_GEOM->pos))"),
    ("F26", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 91,
     "windowGeometry = CBox{WORK_AREA.middle() - windowGeometry.size() / 2.F, windowGeometry.size()};"),
    ("F27", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 95,
     "WORK_AREA.containsPoint(windowGeometry.middle()))"),
    ("F28", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 96,
     "target->setPositionGlobal(windowGeometry);"),
    # --- S293 Hyprland-Target.cpp ---
    ("F29", "Hyprland-Target.cpp", "49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06", 10,
     "void ITarget::setPositionGlobal(const STargetBox& box, uint8_t) {"),
    ("F30", "Hyprland-Target.cpp", "49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06", 11,
     "m_box = box;"),
    ("F31", "Hyprland-Target.cpp", "49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06", 12,
     "m_box.logicalBox.round();"),
    ("F32", "Hyprland-Target.cpp", "49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06", 17,
     "setPositionGlobal({.logicalBox = box}, flags);"),
    # --- S294 Hyprland-WindowTarget.cpp ---
    ("F33", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 36,
     "void CWindowTarget::setPositionGlobal(const STargetBox& box, uint8_t flags) {"),
    ("F34", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 39,
     "updatePos(flags);"),
    ("F35", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 50,
     "const bool  CONFIGURECLIENT = !(flags & TARGET_UPDATE_NO_CLIENT_CONFIGURE);"),
    ("F36", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 70,
     "if (floating() && m_window && !Fullscreen::controller()->isFullscreen(m_window.lock())) {"),
    ("F37", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 71,
     "m_window->setBox(m_box.logicalBox);"),
    ("F38", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 74,
     "m_window->sendWindowSize();"),
    ("F39", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 297,
     "Vector2D CWindowTarget::clampSizeForDesired(const Vector2D& size) const {"),
    ("F40", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 300,
     "newSize = newSize.clamp(*m);"),
    ("F41", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 302,
     "newSize = newSize.clamp(Vector2D{MIN_WINDOW_SIZE, MIN_WINDOW_SIZE}, *m);"),
    ("F42", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 313,
     "requested.size = clampSizeForDesired(DESIRED_GEOM.size());"),
    ("F43", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 227,
     "if (*PCLAMP_TILED) {"),
    ("F44", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 231,
     "calcSize = calcSize.clamp(minSize, maxSize);"),
    # --- S295 Hyprland-GeometricMovableAnimated.cpp ---
    ("F45", "Hyprland-GeometricMovableAnimated.cpp", "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d", 19,
     "case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();"),
    ("F46", "Hyprland-GeometricMovableAnimated.cpp", "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d", 20,
     "case IGeometric::GEOMETRIC_CURRENT: return m_realSize->value();"),
    ("F47", "Hyprland-GeometricMovableAnimated.cpp", "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d", 40,
     "*m_realSize = x;"),
    ("F48", "Hyprland-GeometricMovableAnimated.cpp", "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d", 45,
     "*m_realSize     = x.size();"),
    ("F49", "Hyprland-GeometricMovableAnimated.cpp", "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d", 50,
     "m_realSize->warp();"),
    ("F50", "Hyprland-GeometricMovableAnimated.cpp", "649f1a8d01d28e20e23380db65c5aeb35846d7ef48c8aada9b84ff0e4a1a207d", 58,
     "return m_realSize;"),
    # --- S296 Hyprland-HyprCtl.cpp ---
    ("F51", "Hyprland-HyprCtl.cpp", "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa", 395,
     '"size": [{}, {}],'),
    ("F52", "Hyprland-HyprCtl.cpp", "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa", 400,
     '"floating": {},'),
    ("F53", "Hyprland-HyprCtl.cpp", "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa", 427,
     "sc<int>(w->position(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x),"),
    ("F54", "Hyprland-HyprCtl.cpp", "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa", 428,
     "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y), w->m_workspace ? w->workspaceID() : WORKSPACE_INVALID,"),
    ("F55", "Hyprland-HyprCtl.cpp", "798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa", 448,
     "sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).x), sc<int>(w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL).y),"),
    # --- chain gates (S292 / S294) ---
    ("F56", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 21,
     "const auto DESIRED_GEOM = target->desiredGeometry();"),
    ("F57", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 49,
     "if (target->window() && target->window()->m_firstMap) {"),
    ("F58", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 85,
     "} else if (target->lastFloatingSize().x > 5 && target->lastFloatingSize().y > 5) {"),
    ("F59", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 86,
     "windowGeometry.w = target->lastFloatingSize().x;"),
    ("F60", "Hyprland-WindowTarget.cpp", "8bcaf37000cf55e1d2084bf732f0589b4ab49d36c778d8d4efa98949dd14734d", 77,
     "return;"),
    # --- enclosing scope / storage / remember-size rows ---
    ("F61", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 214,
     'Log::logger->log(Log::ERR, "Invalid size for maxsize");'),
    ("F62", "Hyprland-WindowRuleApplicator.cpp", "fec33f9a0bc279ffc94ca27a6e9843964840d6269bc28d330d566e05fed3307b", 378,
     "CWindowRuleApplicator::SRuleResult CWindowRuleApplicator::applyStaticRule(const SP<CWindowRule>& rule) {"),
    ("F63", "Hyprland-Target.cpp", "49323833c6bc327656e6d02245ebbccf7643fc94f4fbee3cebbae035bbd4ca06", 65,
     "return m_box.logicalBox;"),
    ("F64", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 194,
     "target->rememberFloatingSize(target->position().size());"),
    ("F65", "Hyprland-DefaultFloatingAlgorithm.cpp", "f05f256150c8dcf5041ba71eaa9b8ba0ec16b94d231bff7a213d18fc23632e91", 176,
     "CBox CDefaultFloatingAlgorithm::fitBoxInWorkArea(const CBox& box, SP<ITarget> t) {"),
]

MAX_WORDS = 25


def main() -> int:
    cache = {}
    bad = 0
    for rid, name, want_sha, lineno, quote in ROWS:
        path = FETCH / name
        if name not in cache:
            cache[name] = path.read_text(encoding="utf-8", errors="replace").splitlines()
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            cache[name + "|sha"] = actual
            ok = actual == want_sha
            print(f"SHASUM {name} {actual} {'OK' if ok else 'MISMATCH'}")
            if not ok:
                bad += 1
        lines = cache[name]
        problems = []
        if not (1 <= lineno <= len(lines)):
            problems.append(f"line {lineno} out of range (file has {len(lines)} lines)")
            found = ""
        else:
            found = lines[lineno - 1]
            if quote not in found:
                problems.append("quote not a substring of the numbered line")
        words = len(quote.split())
        if words > MAX_WORDS:
            problems.append(f"{words} words > {MAX_WORDS}")
        if "\n" in quote:
            problems.append("quote spans lines")
        status = "OK" if not problems else "FAIL " + "; ".join(problems)
        if problems:
            bad += 1
        print(f"{rid} {name}:{lineno} words={words} {status}")
        print(f"    grep: {found}")
    print()
    print(f"rows={len(ROWS)} failures={bad} distinct_receipts={len(cache) // 2}")
    return 1 if bad else 0


def check_table() -> int:
    """Cross-check the markdown table in facts.md against ROWS (no hand-drift)."""
    table = (HERE / "facts.md").read_text(encoding="utf-8").splitlines()
    rows = {}
    bad = 0
    for raw in table:
        if not raw.startswith("| F"):
            continue
        cells = raw.replace("\\|", "\x00").split("|")
        if len(cells) != 7:
            print(f"TABLE-BAD cell count {len(cells)}: {raw[:80]}")
            bad += 1
            continue
        rid = cells[1].strip()
        quote = cells[3].strip().strip("`").replace("\x00", "|")
        loc = cells[4].strip().strip("`")
        sha = cells[5].strip().strip("`")
        rows[rid] = (quote, loc, sha)
    want = {r[0]: (r[4], f"{r[1]}:{r[3]}", r[2]) for r in ROWS}
    for rid in want:
        if rid not in rows:
            print(f"TABLE-MISSING {rid}")
            bad += 1
            continue
        if rows[rid] != want[rid]:
            print(f"TABLE-DRIFT {rid}")
            print(f"    table: {rows[rid]}")
            print(f"    rows:  {want[rid]}")
            bad += 1
    for rid in rows:
        if rid not in want:
            print(f"TABLE-EXTRA {rid}")
            bad += 1
    print(f"table_rows={len(rows)} table_failures={bad}")
    return bad


if __name__ == "__main__":
    rc = main()
    rc |= 1 if check_table() else 0
    sys.exit(rc)
