#include <hyprlang.hpp>
#include <any>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>

static const char* DIR = "/fast/scratch/hyaku/mado-r55/R55W2ScoutHyprlang/cases";

static std::unique_ptr<Hyprlang::CConfig> makeConfig(const char* file) {
    const std::string p = std::string(DIR) + "/" + file;
    auto c = std::make_unique<Hyprlang::CConfig>(p.c_str(), Hyprlang::SConfigOptions{.allowMissingConfig = false});
    c->addConfigValue("input:repeat_rate", Hyprlang::INT{25});
    c->addConfigValue("input:repeat_delay", Hyprlang::INT{600});
    c->addConfigValue("input:numlock_by_default", Hyprlang::INT{0});
    c->addSpecialCategory("device", {"name"});
    c->addSpecialConfigValue("device", "repeat_rate", Hyprlang::INT{25});
    c->addSpecialConfigValue("device", "repeat_delay", Hyprlang::INT{600});
    c->addSpecialConfigValue("device", "numlock_by_default", Hyprlang::INT{0});
    c->commence();
    return c;
}
static std::string gint(Hyprlang::CConfig& c, const char* n) {
    auto v = c.getConfigValuePtr(n);
    return v ? std::to_string(std::any_cast<Hyprlang::INT>(v->getValue())) : "<null>";
}
static std::string dint(Hyprlang::CConfig& c, const char* n, const char* k) {
    auto v = c.getSpecialConfigValuePtr("device", n, k);
    if (!v) return "<null>";
    return std::to_string(std::any_cast<Hyprlang::INT>(v->getValue())) + (v->m_bSetByUser ? " (set)" : " (unset)");
}
static void run(const char* name, const std::string& body, const char* devKey) {
    { std::ofstream o(std::string(DIR) + "/" + name, std::ios::binary); o << body; }
    auto c = makeConfig(name);
    const auto res = c->parse();
    std::cout << "== " << name << "\n  parse error: " << (res.error ? "YES: " + std::string(res.getError()) : "no") << "\n";
    std::cout << "  global: rate=" << gint(*c, "input:repeat_rate") << " delay=" << gint(*c, "input:repeat_delay")
              << " numlock=" << gint(*c, "input:numlock_by_default") << "\n";
    std::cout << "  device[" << devKey << "]: rate=" << dint(*c, "repeat_rate", devKey) << " delay=" << dint(*c, "repeat_delay", devKey) << "\n";
}
int main() {
    std::filesystem::create_directories(DIR);
    run("s1.conf", "device {\n    name = k1\n    repeat_rate = 50\n}\ndevice {\n    name = k1\n    repeat_rate = 70\n}\n", "k1");
    run("s2.conf", "device {\n    name = kbd#1\n    repeat_rate = 50\n}\n", "kbd");
    run("s3.conf", "#hyprlang if NOPE\ninput:repeat_rate = 60\n#hyprlang endif\ninput:repeat_delay = 700\n", "k1");
    run("s4.conf", "$V = 40\ninput:repeat_rate = $V\n", "k1");
    run("s5.conf", "input:repeat_rate = -3\ninput:repeat_delay = 5000\n", "k1");
    run("s6.conf", "input:repeat_rate = rgba(10,20,30,1.0)\n", "k1");
    return 0;
}
