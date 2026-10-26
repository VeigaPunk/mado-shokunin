#include <hyprlang.hpp>
#include <cstdio>
#include <string>
#include <vector>

static std::vector<std::string> g_fired;
static Hyprlang::CParseResult monHandler(const char* cmd, const char* val) {
    g_fired.emplace_back(std::string(cmd) + " | " + std::string(val));
    Hyprlang::CParseResult r; return r;
}

static void runCase(const char* label, const char* stream) {
    g_fired.clear();
    Hyprlang::CConfig cfg(stream, Hyprlang::SConfigOptions{.pathIsStream = 1});
    cfg.addConfigValue("decoration:blur:enabled", Hyprlang::INT{1});
    cfg.registerHandler(&monHandler, "monitor", {.allowFlags = false});
    cfg.addSpecialCategory("monitorv2", {.key = "output"});
    cfg.addSpecialConfigValue("monitorv2", "mode", {Hyprlang::STRING{"preferred"}});
    cfg.addSpecialConfigValue("monitorv2", "scale", {Hyprlang::STRING{"auto"}});
    cfg.commence();
    Hyprlang::CParseResult res = cfg.parse();
    printf("== %s\n   parse error=%d %s\n", label, res.error, res.error ? res.getError() : "");
    for (auto& f : g_fired) printf("   HANDLER FIRED: %s\n", f.c_str());
    auto keys = cfg.listKeysForSpecialCategory("monitorv2");
    printf("   v2 keys:");
    for (auto& k : keys) printf(" [%s]", k.c_str());
    printf("\n");
    for (auto& k : keys) {
        auto* v = cfg.getSpecialConfigValuePtr("monitorv2", "mode", k.c_str());
        printf("   mode[%s] setByUser=%d value=%s\n", k.c_str(), v ? (int)v->m_bSetByUser : -1,
               v ? std::any_cast<Hyprlang::STRING>(v->getValue()) : "<null>");
    }
}

int main() {
    runCase("block-context: monitor inside decoration {}",
            "decoration {\n    monitor = INNER, 1920x1080@60, 0x0, 1\n}\nmonitor = TOP, 1920x1080@60, 0x0, 1\n");
    runCase("bracket special category: monitorv2[DP-1] { mode = ... }",
            "monitorv2[DP-1] {\n    mode = 1920x1080@60\n}\n");
    runCase("keyed special category: monitorv2 { output = DP-1 ... }",
            "monitorv2 {\n    output = DP-1\n    mode = 1920x1080@60\n}\n");
    runCase("keyed + bracket both",
            "monitorv2[HDMI-A-1] {\n    mode = 1280x720@50\n}\nmonitorv2 {\n    output = DP-1\n    mode = 1920x1080@60\n}\n");
    return 0;
}
