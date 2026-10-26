// Oracle 2: config-key normalization, name position, flat/bracket forms.
#include <hyprlang.hpp>
#include <cstdio>
#include <fstream>
#include <string>
#include <vector>

static void reg(Hyprlang::CConfig& c) {
    c.addConfigValue("input:kb_layout", {"us"});
    c.addConfigValue("input:kb_variant", {"[[EMPTY]]"});
    c.addConfigValue("input:kb_options", {"[[EMPTY]]"});
    c.addConfigValue("input:kb_model", {"[[EMPTY]]"});
    c.addConfigValue("input:kb_rules", {"[[EMPTY]]"});
    c.addConfigValue("input:kb_file", {"[[EMPTY]]"});
    c.addSpecialCategory("device", {"name"});
    c.addSpecialConfigValue("device", "kb_layout", {"us"});
    c.addSpecialConfigValue("device", "kb_variant", {"[[EMPTY]]"});
    c.addSpecialConfigValue("device", "scroll_factor", Hyprlang::FLOAT{-1});
    c.commence();
}

struct Case { std::string name; std::string body; };

int main() {
    const std::vector<Case> cases = {
        {"O_space_and_case_key", "device {\n  name = Logitech MX Keys\n  kb_layout = de\n}\n"},
        {"P_name_last", "device {\n  kb_layout = de\n  name = foo\n}\n"},
        {"Q_flat_with_key", "device:foo:kb_layout = de\n"},
        {"R_comment_trailing", "device {\n  name = foo # my keyboard\n  kb_layout = de\n}\n"},
        {"S_comma_name", "device {\n  name = Foo,Bar\n  kb_layout = de\n}\n"},
        {"T_two_keys_one_block_then_reopen", "device {\n  name = foo\n  kb_layout = de\n}\ndevice {\n  name = foo\n  scroll_factor = 3\n}\n"},
        {"U_virtual", "device {\n  name = hl-virtual-keyboard\n  kb_layout = de\n}\n"},
    };
    std::vector<std::string> keys = {"foo", "foo-1", "logitech-mx-keys", "Logitech MX Keys", "logitech mx keys", "Foo,Bar", "foo,bar", "hl-virtual-keyboard", "hl-virtual-keyboard-1", "0"};
    for (const auto& cs : cases) {
        const std::string path = "./" + cs.name + ".conf";
        { std::ofstream f(path, std::ios::binary); f << cs.body; }
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        auto r = c.parse();
        printf("=== CASE %s parse_error=%d msg=%s\n", cs.name.c_str(), (int)r.error, r.error ? r.getError() : "-");
        auto stored = c.listKeysForSpecialCategory("device");
        printf("  STORED_KEYS n=%zu", stored.size());
        for (auto& k : stored) printf(" [%s]", k.c_str());
        printf("\n");
        for (const auto& k : keys) {
            auto p = c.getSpecialConfigValuePtr("device", "kb_layout", k.c_str());
            auto s = c.getSpecialConfigValuePtr("device", "scroll_factor", k.c_str());
            printf("  KEY [%s] exists=%d kb_layout=%s scroll_factor=%s\n", k.c_str(), (int)c.specialCategoryExistsForKey("device", k.c_str()),
                   p && p->m_bSetByUser ? std::any_cast<Hyprlang::STRING>(p->getValue()) : "-",
                   s && s->m_bSetByUser ? std::to_string(std::any_cast<Hyprlang::FLOAT>(s->getValue())).c_str() : "-");
        }
    }
    return 0;
}
