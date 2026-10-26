// Oracle 3: RHS value quoting and comment handling (what the config key / value actually stores).
#include <hyprlang.hpp>
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>

static void reg(Hyprlang::CConfig& c) {
    c.addConfigValue("input:kb_layout", {"us"});
    c.addConfigValue("input:kb_options", {"[[EMPTY]]"});
    c.addSpecialCategory("device", {"name"});
    c.addSpecialConfigValue("device", "kb_layout", {"us"});
    c.addSpecialConfigValue("device", "kb_options", {"[[EMPTY]]"});
    c.addSpecialConfigValue("device", "scroll_factor", Hyprlang::FLOAT{-1});
    c.commence();
}

struct Case { std::string name; std::string body; };

int main() {
    const std::vector<Case> cases = {
        {"V1_quoted_value", "device {\n  name = foo\n  kb_layout = \"de\"\n}\n"},
        {"V2_quoted_options", "device {\n  name = foo\n  kb_options = \"compose:caps,grp:alts_toggle\"\n}\n"},
        {"V3_hash_in_name", "device {\n  name = \"foo#bar\"\n  kb_layout = de\n}\n"},
        {"V4_single_quotes", "device {\n  name = 'foo'\n  kb_layout = de\n}\n"},
        {"V5_quoted_scroll", "device {\n  name = foo\n  scroll_factor = \"0.5\"\n}\n"},
        {"V6_braces", "device {\n  name = foo\n  kb_layout = {{de}}\n}\n"},
    };
    for (const auto& cs : cases) {
        const std::string path = "./" + cs.name + ".conf";
        { std::ofstream f(path, std::ios::binary); f << cs.body; }
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        auto r = c.parse();
        printf("=== %s parse_error=%d msg=%s\n", cs.name.c_str(), (int)r.error, r.error ? r.getError() : "-");
        auto ks = c.listKeysForSpecialCategory("device");
        printf("  STORED_KEYS n=%zu", ks.size());
        for (auto& k : ks) printf(" [%s]", k.c_str());
        printf("\n");
        for (const char* nm : {"kb_layout", "kb_options", "scroll_factor"}) {
            auto p = c.getSpecialConfigValuePtr("device", nm, "foo");
            if (!p) { printf("  %s=null(set=0)\n", nm); continue; }
            auto v = p->getValue();
            std::string s = v.type() == typeid(Hyprlang::STRING) ? std::string("\"") + std::any_cast<Hyprlang::STRING>(v) + "\"" :
                            v.type() == typeid(Hyprlang::FLOAT)  ? std::to_string(std::any_cast<Hyprlang::FLOAT>(v)) : "<other>";
            printf("  %s=%s(set=%d)\n", nm, s.c_str(), (int)p->m_bSetByUser);
        }
    }
    return 0;
}
