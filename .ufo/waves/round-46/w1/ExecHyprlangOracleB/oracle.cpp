// mado round 46 / ExecHyprlangOracleB: a TRUE oracle for the input-device plane.
// Registers exactly what Hyprland 0.56.2 registers (ConfigManager.cpp:481-628), parses one
// config file with the host's own hyprlang 0.6.8, and prints what Hyprland's
// getConfigValueSafeDevice / getDeviceString / deviceConfigExplicitlySet would return.
//
// build: g++ -std=c++23 -O0 -o oracle oracle.cpp -lhyprlang
#include <hyprlang.hpp>

#include <any>
#include <cmath>
#include <cstdio>
#include <string>
#include <vector>

static Hyprlang::CConfig* CFG = nullptr;

// Hyprland src/macros.hpp:24  #define STRVAL_EMPTY "[[EMPTY]]"
static const char* STRVAL_EMPTY = "[[EMPTY]]";

static std::string esc(const std::string& s) {
    // json.dumps(..., ensure_ascii=True) subset: quote, backslash, control chars <= 0xFF.
    std::string o = "\"";
    for (unsigned char c : s) {
        switch (c) {
            case '"': o += "\\\""; break;
            case '\\': o += "\\\\"; break;
            case '\n': o += "\\n"; break;
            case '\r': o += "\\r"; break;
            case '\t': o += "\\t"; break;
            case '\b': o += "\\b"; break;
            case '\f': o += "\\f"; break;
            default:
                if (c < 0x20 || c >= 0x7f) {
                    char buf[8];
                    std::snprintf(buf, sizeof(buf), "\\u%04x", c);
                    o += buf;
                } else
                    o += (char)c;
        }
    }
    return o + "\"";
}

enum class KV { ABSENT, DEFAULT, SET };

static KV stateOf(Hyprlang::CConfigValue* v) {
    if (!v)
        return KV::ABSENT;
    return v->m_bSetByUser ? KV::SET : KV::DEFAULT;
}

static const char* stateName(KV k) {
    switch (k) {
        case KV::ABSENT: return "absent";
        case KV::DEFAULT: return "default";
        default: return "set";
    }
}

// Hyprland ConfigManager.cpp:1115-1123
static Hyprlang::CConfigValue* getConfigValueSafeDevice(const std::string& dev, const std::string& val, const std::string& fallback) {
    const auto VAL = CFG->getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());

    if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())
        return CFG->getConfigValuePtr(fallback.c_str());

    return VAL;
}

// Hyprland ConfigManager.cpp:1156-1167
static std::string getDeviceString(const std::string& dev, const std::string& v, const std::string& fallback, std::string* rawOut = nullptr,
                                   KV* stateOut = nullptr) {
    auto val = getConfigValueSafeDevice(dev, v, fallback);
    if (stateOut)
        *stateOut = stateOf(val);
    if (!val) {
        if (rawOut)
            *rawOut = "<nullptr>";
        return "";
    }
    std::string VAL;
    try {
        VAL = std::string{std::any_cast<Hyprlang::STRING>(val->getValue())};
    } catch (const std::bad_any_cast&) {
        if (rawOut)
            *rawOut = "<not-a-string>";
        return "";
    }
    if (rawOut)
        *rawOut = VAL;
    if (VAL == STRVAL_EMPTY)
        return "";
    return VAL;
}

// Hyprland ConfigManager.cpp:1125-1129
static bool deviceConfigExplicitlySet(const std::string& dev, const std::string& val) {
    const auto VAL = CFG->getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());
    return VAL && VAL->m_bSetByUser;
}

// Hyprland ConfigManager.cpp:1139-1145 (getDeviceFloat)
static std::string getDeviceFloatStr(const std::string& dev, const std::string& v, const std::string& fallback) {
    auto val = getConfigValueSafeDevice(dev, v, fallback);
    if (!val)
        return "<nullptr>";
    try {
        const auto F = std::any_cast<Hyprlang::FLOAT>(val->getValue());
        if (!std::isfinite(F))
            return (F > 0 ? "inf" : (F < 0 ? "-inf" : "nan"));
        char buf[64];
        std::snprintf(buf, sizeof(buf), "%.9g", (double)F);
        return buf;
    } catch (const std::bad_any_cast&) { return "<not-a-float>"; }
}

static void regInt(const char* n, int64_t v) { CFG->addConfigValue(n, Hyprlang::INT{v}); }
static void regFloat(const char* n, float v) { CFG->addConfigValue(n, Hyprlang::FLOAT{v}); }
static void regStr(const char* n, const char* v) { CFG->addConfigValue(n, Hyprlang::STRING{v}); }

static void regSpInt(const char* n, int64_t v) { CFG->addSpecialConfigValue("device", n, Hyprlang::INT{v}); }
static void regSpFloat(const char* n, float v) { CFG->addSpecialConfigValue("device", n, Hyprlang::FLOAT{v}); }
static void regSpStr(const char* n, const char* v) { CFG->addSpecialConfigValue("device", n, Hyprlang::STRING{v}); }
static void regSpVec(const char* n, float x, float y) { CFG->addSpecialConfigValue("device", n, Hyprlang::VEC2{x, y}); }

int main(int argc, char** argv) {
    if (argc < 2) {
        std::printf("usage: oracle <config> [names...]\n");
        return 2;
    }
    const char* CONFIG = argv[1];

    CFG = new Hyprlang::CConfig(CONFIG, Hyprlang::SConfigOptions{.throwAllErrors = true, .allowMissingConfig = true});

    // ---- regular values Hyprland registers (ConfigValues.cpp:271-276, :296, :324 and neighbours)
    regStr("input:kb_model", "");
    regStr("input:kb_layout", "us");
    regStr("input:kb_variant", "");
    regStr("input:kb_options", "");
    regStr("input:kb_rules", "");
    regStr("input:kb_file", "");
    regInt("input:numlock_by_default", 0);
    regInt("input:resolve_binds_by_sym", 0);
    regInt("input:repeat_rate", 25);
    regInt("input:repeat_delay", 600);
    regFloat("input:sensitivity", 0);
    regStr("input:accel_profile", "");
    regInt("input:force_no_accel", 0);
    regInt("input:rotation", 0);
    regInt("input:left_handed", 0);
    regStr("input:scroll_points", "");
    regStr("input:scroll_method", "");
    regInt("input:scroll_button", 0);
    regInt("input:scroll_button_lock", 0);
    regFloat("input:scroll_factor", 1);
    regInt("input:natural_scroll", 0);
    regInt("input:follow_mouse", 1);
    regFloat("input:follow_mouse_threshold", 0);
    regFloat("input:touchpad:scroll_factor", 1);
    regStr("input:touchdevice:output", "");
    regStr("input:tablet:output", "");
    regInt("autogenerated", 0);

    // ---- device special category, verbatim from ConfigManager.cpp:518-565 (47 values)
    CFG->addSpecialCategory("device", {"name"});
    regSpFloat("sensitivity", 0.F);
    regSpStr("accel_profile", STRVAL_EMPTY);
    regSpInt("rotation", 0);
    regSpStr("kb_file", STRVAL_EMPTY);
    regSpStr("kb_layout", "us");
    regSpStr("kb_variant", STRVAL_EMPTY);
    regSpStr("kb_options", STRVAL_EMPTY);
    regSpStr("kb_rules", STRVAL_EMPTY);
    regSpStr("kb_model", STRVAL_EMPTY);
    regSpInt("repeat_rate", 25);
    regSpInt("repeat_delay", 600);
    regSpInt("natural_scroll", 0);
    regSpStr("tap_button_map", STRVAL_EMPTY);
    regSpInt("numlock_by_default", 0);
    regSpInt("resolve_binds_by_sym", 0);
    regSpInt("disable_while_typing", 1);
    regSpInt("clickfinger_behavior", 0);
    regSpInt("middle_button_emulation", 0);
    regSpInt("tap-to-click", 1);
    regSpInt("tap-and-drag", 1);
    regSpInt("drag_lock", 0);
    regSpInt("left_handed", 0);
    regSpStr("scroll_method", STRVAL_EMPTY);
    regSpInt("scroll_button", 0);
    regSpInt("scroll_button_lock", 0);
    regSpStr("scroll_points", STRVAL_EMPTY);
    regSpFloat("scroll_factor", -1);
    regSpInt("transform", -1);
    regSpStr("output", STRVAL_EMPTY);
    regSpInt("enabled", 1);
    regSpVec("region_position", 0, 0);
    regSpInt("absolute_region_position", 0);
    regSpVec("region_size", 0, 0);
    regSpInt("relative_input", 0);
    regSpVec("active_area_position", 0, 0);
    regSpVec("active_area_size", 0, 0);
    regSpInt("flip_x", 0);
    regSpInt("flip_y", 0);
    regSpInt("drag_3fg", 0);
    regSpInt("keybinds", 1);
    regSpInt("share_states", 0);
    regSpInt("release_pressed_on_close", 0);
    regSpStr("tags", STRVAL_EMPTY);
    regSpInt("eraser_button_mode", 0);
    regSpInt("eraser_button_override", 0);
    regSpFloat("pressure_range_min", -1.0);
    regSpFloat("pressure_range_max", -1.0);

    CFG->commence();
    const auto RES = CFG->parse();

    std::printf("ORACLE_PARSE: error=%d message=%s\n", RES.error ? 1 : 0, esc(RES.error ? std::string{RES.getError() ? RES.getError() : ""} : std::string{""}).c_str());

    // every device category hyprlang holds, in listKeysForSpecialCategory order
    const auto KEYS = CFG->listKeysForSpecialCategory("device");
    std::printf("ORACLE_NKEYS: n=%zu\n", KEYS.size());
    for (size_t i = 0; i < KEYS.size(); ++i) {
        std::printf("ORACLE_CAT: idx=%zu name=%s exists=%d", i, esc(KEYS[i]).c_str(), CFG->specialCategoryExistsForKey("device", KEYS[i].c_str()) ? 1 : 0);
        std::string setkeys = "";
        static const char* PROBE[] = {"kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file", "scroll_factor", "sensitivity"};
        for (auto* p : PROBE) {
            const auto V = CFG->getSpecialConfigValuePtr("device", p, KEYS[i].c_str());
            if (V && V->m_bSetByUser)
                setkeys += std::string(setkeys.empty() ? "" : ",") + p;
        }
        std::printf(" set=%s\n", esc(setkeys).c_str());
    }

    // globals, as Hyprland reads them
    for (const char* G : {"input:kb_layout", "input:kb_variant", "input:kb_options", "input:kb_model", "input:kb_rules", "input:kb_file", "input:scroll_factor"}) {
        const auto V = CFG->getConfigValuePtr(G);
        std::string repr = "<nullptr>";
        if (V) {
            try {
                repr = std::string{std::any_cast<Hyprlang::STRING>(V->getValue())};
            } catch (const std::bad_any_cast&) {
                try {
                    char buf[64];
                    std::snprintf(buf, sizeof(buf), "%.9g", (double)std::any_cast<Hyprlang::FLOAT>(V->getValue()));
                    repr = buf;
                } catch (const std::bad_any_cast&) { repr = "<non-string>"; }
            }
        }
        std::printf("ORACLE_GLOBAL: key=%s raw=%s set=%d\n", esc(G).c_str(), esc(repr).c_str(), (V && V->m_bSetByUser) ? 1 : 0);
    }

    // per queried device name: what applyConfigToKeyboard would pass to setKeymap
    for (int a = 2; a < argc; ++a) {
        const std::string NAME = argv[a];
        std::printf("ORACLE_DEV: name=%s exists=%d\n", esc(NAME).c_str(), CFG->specialCategoryExistsForKey("device", NAME.c_str()) ? 1 : 0);
        struct {
            const char* field;
            const char* glob;
        } F[] = {{"kb_layout", "input:kb_layout"},
                 {"kb_variant", "input:kb_variant"},
                 {"kb_options", "input:kb_options"},
                 {"kb_model", "input:kb_model"},
                 {"kb_rules", "input:kb_rules"},
                 {"kb_file", "input:kb_file"}};
        for (auto& f : F) {
            std::string raw;
            KV          st = KV::ABSENT;
            const auto  S  = getDeviceString(NAME, f.field, f.glob, &raw, &st);
            std::printf("ORACLE_FIELD: name=%s field=%s state=%s raw=%s projected=%s\n", esc(NAME).c_str(), f.field, stateName(st), esc(raw).c_str(), esc(S).c_str());
        }
        const bool EX = deviceConfigExplicitlySet(NAME, "scroll_factor");
        std::printf("ORACLE_SCROLL: name=%s explicit=%d float=%s resolved=%s\n", esc(NAME).c_str(), EX ? 1 : 0,
                    getDeviceFloatStr(NAME, "scroll_factor", "").c_str(), getDeviceFloatStr(NAME, "scroll_factor", "input:scroll_factor").c_str());
    }

    std::printf("ORACLE_END\n");
    (void)getDeviceFloatStr;
    return 0;
}
