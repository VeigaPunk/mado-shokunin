// End-to-end check of hyprlang v0.6.8 (exact fetched sources) against the host's
// real hyprutils 0.14.2 library — the same pairing the host's libhyprlang.so.0.6.8 uses.
#include <hyprlang.hpp>
#include <any>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>

static const char* DIR = "/fast/scratch/hyaku/mado-r55/R55W2ScoutHyprlang/cases";

static void writeCase(const char* name, const std::string& body) {
    std::ofstream o(std::string(DIR) + "/" + name, std::ios::binary);
    o << body;
}

static std::unique_ptr<Hyprlang::CConfig> makeConfig(const char* file) {

    const std::string         p   = std::string(DIR) + "/" + file;
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
    if (!v)
        return "<null>";
    return std::to_string(std::any_cast<Hyprlang::INT>(v->getValue()));
}

static std::string dint(Hyprlang::CConfig& c, const char* n, const char* k) {
    auto v = c.getSpecialConfigValuePtr("device", n, k);
    if (!v)
        return "<null>";
    return std::to_string(std::any_cast<Hyprlang::INT>(v->getValue())) + (v->m_bSetByUser ? " (set)" : " (unset)");
}

static void run(const char* name, const std::string& body) {
    writeCase(name, body);
    auto c = makeConfig(name);
    std::cout << "== " << name << "\n";
    const auto res = c->parse();
    std::cout << "  parse error: " << (res.error ? "YES: " + std::string(res.getError()) : "no") << "\n";
    std::cout << "  global: rate=" << gint(*c, "input:repeat_rate") << " delay=" << gint(*c, "input:repeat_delay")
              << " numlock=" << gint(*c, "input:numlock_by_default") << "\n";
    for (const char* k : {"k1", "k2"})
        std::cout << "  device[" << k << "]: rate=" << dint(*c, "repeat_rate", k)
                  << " delay=" << dint(*c, "repeat_delay", k) << " numlock=" << dint(*c, "numlock_by_default", k) << "\n";

}

int main() {
    std::filesystem::create_directories(DIR);

    run("t1.conf", // repeated same-name device blocks merge
        "device {\n"
        "    name = k1\n"
        "    repeat_rate = 50\n"
        "}\n"
        "\n"
        "device {\n"
        "    name = k1\n"
        "    repeat_delay = 800\n"
        "}\n");

    run("t2.conf", // key line BEFORE the name line
        "device {\n"
        "    repeat_rate = 50\n"
        "    name = k1\n"
        "}\n");

    run("t3.conf", // negative and over-max values: is .min/.max enforced?
        "input:repeat_rate = -3\n"
        "input:repeat_delay = 5000\n"
        "input:numlock_by_default = 7\n");

    run("t4.conf", // hex lowercase/uppercase, leading zeros, leading plus
        "input:repeat_rate = 0x10\n"
        "input:repeat_delay = 0X10\n"
        "input:numlock_by_default = 007\n"
        "device {\n"
        "    name = k2\n"
        "    repeat_rate = +5\n"
        "}\n");

    run("t5.conf", // trailing comments on block open/close
        "input { # main\n"
        "    repeat_rate = 30\n"
        "} # end\n"
        "device {\n"
        "    name = k1\n"
        "    repeat_rate = 50\n"
        "} # keep\n"
        "repeat_delay = 400\n");

    run("t6.conf", // escaped hash leaves 'on#' -> boolean prefix
        "input:numlock_by_default = on##\n");

    return 0;
}
