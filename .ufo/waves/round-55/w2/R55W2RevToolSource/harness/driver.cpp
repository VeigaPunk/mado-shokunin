// Harness: drives the UNMODIFIED hyprlang v0.6.8 parser (sha-matched to upstream) with the same
// registration Hyprland 0.56.2 legacy ConfigManager uses (legacy ConfigManager.cpp:486, 518-532, 614),
// then reproduces getConfigValueSafeDevice/getDeviceInt (:1115-1137), applyConfigToKeyboard
// (InputManager.cpp:1220-1223, 1282-1283) and IKeyboard numlock (IKeyboard.cpp:120-122).
#include <hyprlang.hpp>
#include <any>
#include <cstdio>
#include <string>
#include <vector>
#include <algorithm>

static Hyprlang::CConfig* g_cfg = nullptr;

static Hyprlang::CParseResult handleSource(const char* c, const char* v) {
    Hyprlang::CParseResult result;
    const auto R = g_cfg->parseFile(v);
    if (R.error)
        result.setError(R.getError());
    return result;
}

// mirrors CConfigManager::getConfigValueSafeDevice + getDeviceInt (legacy ConfigManager.cpp:1115-1137)
static int getDeviceInt(const std::string& dev, const std::string& val, const std::string& fallback) {
    auto* VAL = g_cfg->getSpecialConfigValuePtr("device", val.c_str(), dev.c_str());
    if ((!VAL || !VAL->m_bSetByUser) && !fallback.empty())
        VAL = g_cfg->getConfigValuePtr(fallback.c_str());
    if (!VAL)
        return 0;
    return static_cast<int>(std::any_cast<Hyprlang::INT>(VAL->getValue()));
}

int main(int argc, char** argv) {
    if (argc < 2) { std::fprintf(stderr, "usage: driver CONFIG [KEYBOARD...]\n"); return 2; }
    Hyprlang::SConfigOptions opts;
    opts.throwAllErrors   = true;
    opts.allowMissingConfig = true;
    Hyprlang::CConfig cfg(argv[1], opts);
    g_cfg = &cfg;
    cfg.addConfigValue("input:repeat_rate", Hyprlang::INT{25});
    cfg.addConfigValue("input:repeat_delay", Hyprlang::INT{600});
    cfg.addConfigValue("input:numlock_by_default", Hyprlang::INT{0});
    cfg.addSpecialCategory("device", {"name"});
    cfg.addSpecialConfigValue("device", "repeat_rate", Hyprlang::INT{25});
    cfg.addSpecialConfigValue("device", "repeat_delay", Hyprlang::INT{600});
    cfg.addSpecialConfigValue("device", "numlock_by_default", Hyprlang::INT{0});
    cfg.registerHandler(&handleSource, "source", {false});
    cfg.commence();
    const auto RES = cfg.parse();
    if (RES.error)
        std::printf("HARNESS: parse_error=%s\n", RES.getError());
    else
        std::printf("HARNESS: parse_error=none\n");
    std::vector<std::string> kbs(argv + 2, argv + argc);
    if (kbs.empty()) kbs.push_back("*");
    for (const auto& kb : kbs) {
        const int rate  = std::max(0, getDeviceInt(kb, "repeat_rate", "input:repeat_rate"));
        const int delay = std::max(0, getDeviceInt(kb, "repeat_delay", "input:repeat_delay"));
        const int numlock = getDeviceInt(kb, "numlock_by_default", "input:numlock_by_default");
        std::printf("HARNESS: keyboard=%s repeat_rate=%d repeat_delay=%d numlock_by_default=%d numlock_locks=%d\n",
                    kb.c_str(), rate, delay, numlock, numlock == 1 ? 1 : 0);
    }
    return 0;
}
