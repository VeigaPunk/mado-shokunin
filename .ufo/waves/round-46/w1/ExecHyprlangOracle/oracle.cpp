// mado r46 / ExecHyprlangOracle - TRUE oracle for the C1 contract against the host's hyprlang 0.6.8.
//
// Registers exactly what Hyprland 0.56.2 registers for the input-device plane
// (fetch/Hyprland-ConfigManager.cpp:518-565 for the `device` special category,
// fetch/Hyprland-ConfigValues.cpp:271-276 for the input:kb_* globals), parses config files with the real
// libhyprlang.so, and prints what Hyprland's accessors would return:
//   getConfigValueSafeDevice / getDeviceString / deviceConfigExplicitlySet (fetch/Hyprland-ConfigManager.cpp:1115-1201)
//   InputManager.cpp:1379-1381 for the pointer scroll factor (clamp 0..100 when explicitly set, else -1)
//   InputManager.cpp:1227-1233 for the six keyboard strings.
//
// Build: g++ -std=c++23 -O2 -o oracle oracle.cpp -lhyprlang
// Input: a manifest (see gen.py). Output: one JSON object per queried device name, plus the device
// special-category keys in creation order and the parse-error count, per case.

#include <hyprlang.hpp>

#include <algorithm>
#include <any>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

using namespace Hyprlang;

static const char* EMPTY = "[[EMPTY]]";

// ---- Hyprland's accessors, transcribed 1:1 (fetch/Hyprland-ConfigManager.cpp:1115-1201) ----
static CConfigValue* safeDevice(CConfig& c, const std::string& dev, const std::string& val, const std::string& fallback) {
    CConfigValue* VAL = c.getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());
    if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())
        return c.getConfigValuePtr(fallback.c_str());
    return VAL;
}

static std::string deviceString(CConfig& c, const std::string& dev, const std::string& val, const std::string& fallback) {
    CConfigValue* val2 = safeDevice(c, dev, val, fallback);
    if (!val2)
        return "";
    std::string s{std::any_cast<STRING>(val2->getValue())};
    if (s == EMPTY)
        return "";
    return s;
}

static bool explicitlySet(CConfig& c, const std::string& dev, const std::string& val) {
    CConfigValue* VAL = c.getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());
    return VAL && VAL->m_bSetByUser;
}

static float deviceFloat(CConfig& c, const std::string& dev, const std::string& val, const std::string& fallback) {
    CConfigValue* v = safeDevice(c, dev, val, fallback);
    if (!v)
        return 0.F;
    return std::any_cast<FLOAT>(v->getValue());
}

// ---- registration: fetch/Hyprland-ConfigManager.cpp:518-565 + fetch/Hyprland-ConfigValues.cpp:271-276 ----
static void registerAll(CConfig& c) {
    // device special category: key "name", 47 values
    c.addSpecialCategory("device", SSpecialCategoryOptions{.key = "name"});
    c.addSpecialConfigValue("device", "sensitivity", CConfigValue(FLOAT{0.F}));
    c.addSpecialConfigValue("device", "accel_profile", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "rotation", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "kb_file", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_layout", CConfigValue(STRING{"us"}));
    c.addSpecialConfigValue("device", "kb_variant", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_options", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_rules", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "kb_model", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "repeat_rate", CConfigValue(INT{25}));
    c.addSpecialConfigValue("device", "repeat_delay", CConfigValue(INT{600}));
    c.addSpecialConfigValue("device", "natural_scroll", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "tap_button_map", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "numlock_by_default", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "resolve_binds_by_sym", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "disable_while_typing", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "clickfinger_behavior", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "middle_button_emulation", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "tap-to-click", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "tap-and-drag", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "drag_lock", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "left_handed", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "scroll_method", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "scroll_button", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "scroll_button_lock", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "scroll_points", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "scroll_factor", CConfigValue(FLOAT{-1.F}));
    c.addSpecialConfigValue("device", "transform", CConfigValue(INT{-1}));
    c.addSpecialConfigValue("device", "output", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "enabled", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "region_position", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "absolute_region_position", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "region_size", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "relative_input", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "active_area_position", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "active_area_size", CConfigValue(VEC2{0, 0}));
    c.addSpecialConfigValue("device", "flip_x", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "flip_y", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "drag_3fg", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "keybinds", CConfigValue(INT{1}));
    c.addSpecialConfigValue("device", "share_states", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "release_pressed_on_close", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "tags", CConfigValue(STRING{EMPTY}));
    c.addSpecialConfigValue("device", "eraser_button_mode", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "eraser_button_override", CConfigValue(INT{0}));
    c.addSpecialConfigValue("device", "pressure_range_min", CConfigValue(FLOAT{-1.0}));
    c.addSpecialConfigValue("device", "pressure_range_max", CConfigValue(FLOAT{-1.0}));

    // globals Hyprland registers (fetch/Hyprland-ConfigValues.cpp:271-276 and neighbours the plane touches)
    c.addConfigValue("input:kb_model", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_layout", CConfigValue(STRING{"us"}));
    c.addConfigValue("input:kb_variant", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_options", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_rules", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:kb_file", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:scroll_factor", CConfigValue(FLOAT{1.F}));
    c.addConfigValue("input:touchpad:scroll_factor", CConfigValue(FLOAT{1.F}));
    c.addConfigValue("input:touchpad:natural_scroll", CConfigValue(INT{0}));
    c.addConfigValue("input:touchpad:tap-to-click", CConfigValue(INT{1}));
    c.addConfigValue("input:touchpad:disable_while_typing", CConfigValue(INT{1}));
    c.addConfigValue("input:touchpad:clickfinger_behavior", CConfigValue(INT{0}));
    c.addConfigValue("input:natural_scroll", CConfigValue(INT{0}));
    c.addConfigValue("input:sensitivity", CConfigValue(FLOAT{0.F}));
    c.addConfigValue("input:accel_profile", CConfigValue(STRING{EMPTY}));
    c.addConfigValue("input:repeat_rate", CConfigValue(INT{25}));
    c.addConfigValue("input:repeat_delay", CConfigValue(INT{600}));
    c.addConfigValue("input:left_handed", CConfigValue(INT{0}));
    c.addConfigValue("input:numlock_by_default", CConfigValue(INT{0}));
    c.addConfigValue("input:resolve_binds_by_sym", CConfigValue(INT{0}));
}

// ---- JSON string escaping (bytes pass through; controls escaped) ----
static std::string jstr(const std::string& s) {
    std::string o = "\"";
    for (unsigned char ch : s) {
        switch (ch) {
            case '"': o += "\\\""; break;
            case '\\': o += "\\\\"; break;
            case '\n': o += "\\n"; break;
            case '\r': o += "\\r"; break;
            case '\t': o += "\\t"; break;
            default:
                if (ch < 0x20) {
                    char b[8];
                    std::snprintf(b, sizeof b, "\\u%04x", ch);
                    o += b;
                } else
                    o += static_cast<char>(ch);
        }
    }
    o += "\"";
    return o;
}

static void emitName(CConfig& cfg, const std::string& nm) {
    static const char* KEY[5] = {"kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules"};
    static const char* FB[5]  = {"input:kb_layout", "input:kb_variant", "input:kb_options", "input:kb_model", "input:kb_rules"};
    std::string        v[5];
    for (int i = 0; i < 5; ++i)
        v[i] = deviceString(cfg, nm, KEY[i], FB[i]);
    const std::string kbf = deviceString(cfg, nm, "kb_file", "input:kb_file");
    const bool        sset = explicitlySet(cfg, nm, "scroll_factor");
    double            raw = 0.0, exp = -1.0;
    if (sset) {
        const float f = deviceFloat(cfg, nm, "scroll_factor", "input:scroll_factor");
        raw           = static_cast<double>(f);
        exp           = static_cast<double>(std::clamp(f, 0.F, 100.F));
    }
    const bool block = cfg.specialCategoryExistsForKey("device", nm.c_str());
    // printed exactly as HyprCtl does (fetch/Hyprland-HyprCtl.cpp:770 "{:.2f}"), so -0.0 stays "-0.00"
    char sf[64], sfr[64];
    std::snprintf(sf, sizeof sf, "%.2f", static_cast<double>(exp));
    std::snprintf(sfr, sizeof sfr, "%.9g", static_cast<double>(raw));
    std::printf("{\"name\":%s,\"block\":%s,\"layout\":%s,\"variant\":%s,\"options\":%s,\"model\":%s,\"rules\":%s,"
                "\"kb_file\":%s,\"kb_file_set\":%s,\"sf_set\":%s,\"sf\":%s,\"sf_raw\":%s}\n",
                jstr(nm).c_str(), block ? "true" : "false", jstr(v[0]).c_str(), jstr(v[1]).c_str(), jstr(v[2]).c_str(),
                jstr(v[3]).c_str(), jstr(v[4]).c_str(), jstr(kbf).c_str(), kbf.empty() ? "false" : "true",
                sset ? "true" : "false", jstr(sf).c_str(), jstr(sfr).c_str());
}

static void runCase(const std::string& id, const std::vector<std::string>& files, const std::vector<std::string>& names) {
    SConfigOptions opts{};
    opts.allowMissingConfig = 1;
    CConfig cfg("/nonexistent-mado-oracle-root.conf", opts);
    registerAll(cfg);
    cfg.commence();

    int errors = 0;
    for (const auto& f : files) {
        auto res = cfg.parseFile(f.c_str());
        if (res.error)
            ++errors;
    }

    std::printf("BEGIN %s\n", id.c_str());
    for (const auto& nm : names)
        emitName(cfg, nm);
    const auto KEYS = cfg.listKeysForSpecialCategory("device");
    std::string cats = "[";
    for (size_t i = 0; i < KEYS.size(); ++i) {
        if (i)
            cats += ",";
        cats += jstr(KEYS[i]);
    }
    cats += "]";
    std::printf("{\"categories\":%s,\"errors\":%d}\n", cats.c_str(), errors);
    std::printf("END %s\n", id.c_str());
}

int main(int argc, char** argv) {
    std::string manifest;
    for (int i = 1; i + 1 < argc; i += 2) {
        if (std::strcmp(argv[i], "--manifest") == 0)
            manifest = argv[i + 1];
    }
    if (manifest.empty()) {
        std::fprintf(stderr, "usage: oracle --manifest PATH\n");
        return 2;
    }
    std::ifstream mf(manifest);
    if (!mf.good()) {
        std::fprintf(stderr, "manifest unreadable: %s\n", manifest.c_str());
        return 2;
    }
    std::string line;
    while (std::getline(mf, line)) {
        if (line.rfind("CASE ", 0) != 0)
            continue;
        std::istringstream ss(line);
        std::string        tag, id;
        size_t             nf = 0, nn = 0;
        ss >> tag >> id >> nf >> nn;
        std::vector<std::string> files(nf), names(nn);
        for (auto& f : files)
            std::getline(mf, f);
        for (auto& n : names)
            std::getline(mf, n);
        runCase(id, files, names);
    }
    return 0;
}
