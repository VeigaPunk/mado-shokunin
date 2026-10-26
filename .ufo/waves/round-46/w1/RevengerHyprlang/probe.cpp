// probe: hyprlang 0.6.8 special-category state machine for Hyprland's `device` category.
// Registers `device` exactly as Hyprland 0.56.2 src/config/ConfigManager.cpp:518-563 does
// (special category key = "name", 47 fields), then parses a raw config stream and dumps
// every resulting special-category instance with m_bSetByUser flags.
#include <hyprlang.hpp>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <any>
#include <typeinfo>

using namespace Hyprlang;

static std::string toStr(CConfigValue* v) {
    if (!v) return "<null>";
    std::any a;
    try { a = v->getValue(); } catch (...) { return "<empty>"; }
    if (a.type() == typeid(INT)) return std::to_string(std::any_cast<INT>(a));
    if (a.type() == typeid(FLOAT)) { char b[64]; snprintf(b, sizeof b, "%.6g", (double)std::any_cast<FLOAT>(a)); return b; }
    if (a.type() == typeid(STRING)) { auto p = std::any_cast<STRING>(a); return std::string("<") + (p ? p : "(null)") + ">"; }
    if (a.type() == typeid(VEC2)) { auto p = std::any_cast<VEC2>(a); char b[64]; snprintf(b, sizeof b, "%.6g,%.6g", (double)p.x, (double)p.y); return b; }
    return "<other>";
}


static void registerDevice(CConfig& config) {
    config.addSpecialCategory("device", {"name"});
    config.addSpecialConfigValue("device", "sensitivity", {0.F});
    config.addSpecialConfigValue("device", "accel_profile", {""});
    config.addSpecialConfigValue("device", "rotation", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "kb_file", {""});
    config.addSpecialConfigValue("device", "kb_layout", {"us"});
    config.addSpecialConfigValue("device", "kb_variant", {""});
    config.addSpecialConfigValue("device", "kb_options", {""});
    config.addSpecialConfigValue("device", "kb_rules", {""});
    config.addSpecialConfigValue("device", "kb_model", {""});
    config.addSpecialConfigValue("device", "repeat_rate", Hyprlang::INT{25});
    config.addSpecialConfigValue("device", "repeat_delay", Hyprlang::INT{600});
    config.addSpecialConfigValue("device", "natural_scroll", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "tap_button_map", {""});
    config.addSpecialConfigValue("device", "numlock_by_default", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "resolve_binds_by_sym", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "disable_while_typing", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "clickfinger_behavior", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "middle_button_emulation", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "tap-to-click", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "tap-and-drag", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "drag_lock", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "left_handed", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "scroll_method", {""});
    config.addSpecialConfigValue("device", "scroll_button", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "scroll_button_lock", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "scroll_points", {""});
    config.addSpecialConfigValue("device", "scroll_factor", Hyprlang::FLOAT{-1});
    config.addSpecialConfigValue("device", "transform", Hyprlang::INT{-1});
    config.addSpecialConfigValue("device", "output", {""});
    config.addSpecialConfigValue("device", "enabled", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "region_position", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "absolute_region_position", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "region_size", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "relative_input", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "active_area_position", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "active_area_size", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "flip_x", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "flip_y", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "drag_3fg", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "keybinds", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "share_states", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "release_pressed_on_close", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "tags", "");
    config.addSpecialConfigValue("device", "eraser_button_mode", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "eraser_button_override", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "pressure_range_min", Hyprlang::FLOAT{-1.0});
    config.addSpecialConfigValue("device", "pressure_range_max", Hyprlang::FLOAT{-1.0});
}

// One fresh CConfig per (field, literal): what does the host parser store, and does it error?
static void floatMatrix() {
    static const char* FIELDS[] = {"scroll_factor", "repeat_rate"};
    static const char* VALS[]   = {"0.5", "100", "101", "-5", "1e2", "+3", ".5", "5.", " 0.5", "",
                                  "inf", "-inf", "infinity", "NAN", "nan", "0x10", "0X1p4", "1e40", "1e-45", "true", "1e3"};
    for (auto* field : FIELDS) {
        for (auto* v : VALS) {
            const std::string cfg = "device {\n name = A\n " + std::string(field) + " = " + v + "\n}\n";
            CConfig c(cfg.c_str(), Hyprlang::SConfigOptions{.pathIsStream = true});
            registerDevice(c);
            c.commence();
            auto r = c.parse();
            auto* val = c.getSpecialConfigValuePtr("device", field, "A");
            printf("F|%s|%s|%s|%s|%s\n", field, v, toStr(val).c_str(),
                   val && val->m_bSetByUser ? "set" : "def", r.error ? r.getError() : "-");
        }
    }
}

int main(int argc, char** argv) {
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc > 1 && std::string(argv[1]) == "floats") { floatMatrix(); return 0; }
    if (argc < 2) { fprintf(stderr, "usage: %s <config-stream-file> | floats\n", argv[0]); return 2; }
    std::ifstream f(argv[1]);
    std::stringstream ss;
    ss << f.rdbuf();
    const std::string stream = ss.str();

    CConfig config(stream.c_str(), Hyprlang::SConfigOptions{.pathIsStream = true});

    // == Hyprland 0.56.2 ConfigManager.cpp:518-563 verbatim shape ==
    config.addSpecialCategory("device", {"name"});
    config.addSpecialConfigValue("device", "sensitivity", {0.F});
    config.addSpecialConfigValue("device", "accel_profile", {""});
    config.addSpecialConfigValue("device", "rotation", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "kb_file", {""});
    config.addSpecialConfigValue("device", "kb_layout", {"us"});
    config.addSpecialConfigValue("device", "kb_variant", {""});
    config.addSpecialConfigValue("device", "kb_options", {""});
    config.addSpecialConfigValue("device", "kb_rules", {""});
    config.addSpecialConfigValue("device", "kb_model", {""});
    config.addSpecialConfigValue("device", "repeat_rate", Hyprlang::INT{25});
    config.addSpecialConfigValue("device", "repeat_delay", Hyprlang::INT{600});
    config.addSpecialConfigValue("device", "natural_scroll", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "tap_button_map", {""});
    config.addSpecialConfigValue("device", "numlock_by_default", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "resolve_binds_by_sym", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "disable_while_typing", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "clickfinger_behavior", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "middle_button_emulation", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "tap-to-click", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "tap-and-drag", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "drag_lock", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "left_handed", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "scroll_method", {""});
    config.addSpecialConfigValue("device", "scroll_button", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "scroll_button_lock", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "scroll_points", {""});
    config.addSpecialConfigValue("device", "scroll_factor", Hyprlang::FLOAT{-1});
    config.addSpecialConfigValue("device", "transform", Hyprlang::INT{-1});
    config.addSpecialConfigValue("device", "output", {""});
    config.addSpecialConfigValue("device", "enabled", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "region_position", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "absolute_region_position", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "region_size", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "relative_input", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "active_area_position", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "active_area_size", Hyprlang::VEC2{0, 0});
    config.addSpecialConfigValue("device", "flip_x", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "flip_y", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "drag_3fg", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "keybinds", Hyprlang::INT{1});
    config.addSpecialConfigValue("device", "share_states", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "release_pressed_on_close", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "tags", "");
    config.addSpecialConfigValue("device", "eraser_button_mode", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "eraser_button_override", Hyprlang::INT{0});
    config.addSpecialConfigValue("device", "pressure_range_min", Hyprlang::FLOAT{-1.0});
    config.addSpecialConfigValue("device", "pressure_range_max", Hyprlang::FLOAT{-1.0});

    config.commence();
    CParseResult res = config.parse();

    const bool DYN = argc > 2 && std::string(argv[2]) == "dyn";

    printf("ERR|%s\n", res.error ? res.getError() : "-");

    const auto KEYS = config.listKeysForSpecialCategory("device");
    std::string keys;
    for (auto& k : KEYS) keys += "[" + k + "]";
    printf("NKEYS|%zu\n", KEYS.size());
    printf("KEYS|%s\n", keys.c_str());

    static const char* FIELDS[] = {"kb_layout", "kb_variant", "sensitivity", "scroll_factor",
                                   "repeat_rate", "enabled", "tags"};
    for (auto& k : KEYS) {
        printf("CAT|%s", k.c_str());
        for (auto* fl : FIELDS) {
            auto* v = config.getSpecialConfigValuePtr("device", fl, k.c_str());
            printf("|%s=%s,%s", fl, toStr(v).c_str(), v && v->m_bSetByUser ? "set" : "def");
        }
        printf("\n");
    }
    if (argc > 2 && std::string(argv[2]) == "twice") {
        CParseResult r2 = config.parse();
        printf("REPARSE|%s\n", r2.error ? r2.getError() : "-");
        for (auto& k : config.listKeysForSpecialCategory("device")) printf("REKEY|[%s]", k.c_str());
        printf("\n");
    }
    if (DYN) {
        auto r1 = config.parseDynamic("device[K]:kb_layout", "hr");
        printf("DYN1|%s|", r1.error ? r1.getError() : "-");
        for (auto& k : config.listKeysForSpecialCategory("device")) printf("[%s]", k.c_str());
        printf("\n");
        auto r2 = config.parseDynamic("device:kb_variant", "intl");
        printf("DYN2|%s|", r2.error ? r2.getError() : "-");
        for (auto& k : config.listKeysForSpecialCategory("device")) printf("[%s]", k.c_str());
        printf("\n");
        for (auto& k : config.listKeysForSpecialCategory("device")) {
            auto* v = config.getSpecialConfigValuePtr("device", "kb_variant", k.c_str());
            printf("DYNCAT|%s|kb_variant=%s,%s\n", k.c_str(), toStr(v).c_str(), v && v->m_bSetByUser ? "set" : "def");
        }
    }

    // existence probe for stale-key questions
    for (auto& k : std::vector<std::string>{"0", "", "A", "B", "Lexa"}) {
        printf("EXISTS|%s|%d\n", k.c_str(), (int)config.specialCategoryExistsForKey("device", k.c_str()));
    }
    return 0;
}
