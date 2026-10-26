// Oracle: exactness of hyprlang special-category key matching on the host's libhyprlang 0.6.8
// (the library Hyprland 0.56.2 links). Registration mirrors Hyprland ConfigManager.cpp:518-545.
#include <hyprlang.hpp>

#include <cstdio>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>

static int failures = 0;
static void check(bool ok, const char* what) {
    printf("%s %s\n", ok ? "PASS" : "FAIL", what);
    if (!ok)
        failures++;
}

static std::string gdir = ".";

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

struct Case {
    std::string name;
    std::string body;
};

static std::string val(Hyprlang::CConfig& c, const char* name, const char* key, bool& set) {
    auto p = c.getSpecialConfigValuePtr("device", name, key);
    if (!p) {
        set = false;
        return "<null>";
    }
    set = p->m_bSetByUser;
    auto v = p->getValue();
    if (v.type() == typeid(Hyprlang::STRING))
        return std::string{"\""} + std::any_cast<Hyprlang::STRING>(v) + "\"";
    if (v.type() == typeid(Hyprlang::FLOAT))
        return std::to_string(std::any_cast<Hyprlang::FLOAT>(v));
    return "<other>";
}

int main() {
    const std::vector<Case> cases = {
        {"A_plain_foo", "device {\n  name = foo\n  kb_layout = de\n  scroll_factor = 0.5\n}\n"},
        {"B_capital_key", "device {\n  name = Foo\n  kb_layout = de\n}\n"},
        {"C_upper_key", "device {\n  name = FOO\n  kb_layout = de\n}\n"},
        {"D_trailing_space", "device {\n  name = foo \n  kb_layout = de\n}\n"},
        {"E_leading_space", "device {\n  name =  foo\n  kb_layout = de\n}\n"},
        {"F_quoted_trailing_space", "device {\n  name = \"foo \"\n  kb_layout = de\n}\n"},
        {"G_suffix_block", "device {\n  name = foo-1\n  kb_layout = fr\n  scroll_factor = 2.0\n}\n"},
        {"H_both_blocks", "device {\n  name = foo\n  kb_layout = de\n}\ndevice {\n  name = foo-1\n  kb_layout = fr\n}\n"},
        {"I_bracket_form", "device[foo]:kb_layout = de\ndevice[foo]:scroll_factor = 0.25\n"},
        {"J_flat_top_level", "device:name = foo\ndevice:kb_layout = de\n"},
        {"K_dup_blocks_same_key", "device {\n  name = foo\n  kb_layout = de\n}\ndevice {\n  name = foo\n  kb_layout = fr\n}\n"},
        {"L_tab_trailing", "device {\n  name = foo\t\n  kb_layout = de\n}\n"},
        {"M_prefix_only", "device {\n  name = fo\n  kb_layout = de\n}\n"},
        {"N_unicode", "device {\n  name = föö\n  kb_layout = de\n}\n"},
    };

    std::vector<std::string> keys = {"foo", "foo-1", "Foo", "FOO", "foo ", " foo", "fo", "foobar", "foo-1-1", "föö", "\"foo \"", "foo\t"};

    for (const auto& cs : cases) {
        const std::string path = gdir + "/" + cs.name + ".conf";
        { std::ofstream f(path, std::ios::binary); f << cs.body; }
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        auto r = c.parse();
        printf("=== CASE %s parse_error=%d%s%s\n", cs.name.c_str(), (int)r.error, r.error ? " msg=" : "", r.error ? r.getError() : "");
        auto stored = c.listKeysForSpecialCategory("device");
        printf("  STORED_KEYS n=%zu", stored.size());
        for (auto& k : stored)
            printf(" [%s]", k.c_str());
        printf("\n");
        for (const auto& k : keys) {
            bool setA = false, setB = false;
            std::string la = val(c, "kb_layout", k.c_str(), setA);
            std::string sc = val(c, "scroll_factor", k.c_str(), setB);
            bool ex = c.specialCategoryExistsForKey("device", k.c_str());
            printf("  KEY [%s] exists=%d kb_layout=%s(set=%d) scroll_factor=%s(set=%d)\n", k.c_str(), (int)ex, la.c_str(), (int)setA, sc.c_str(), (int)setB);
        }
    }

    // Assertions on the four headline questions (case A, B, C, D, G, H, K).
    {
        const std::string path = gdir + "/A_plain_foo.conf";
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        c.parse();
        bool s = false;
        check(c.getSpecialConfigValuePtr("device", "kb_layout", "foo") != nullptr, "A: block foo matches key foo");
        check(c.getSpecialConfigValuePtr("device", "kb_layout", "foo-1") == nullptr, "A: block foo does NOT match key foo-1");
        check(!c.specialCategoryExistsForKey("device", "foo-1"), "A: specialCategoryExistsForKey(foo-1) false");
        check(!c.specialCategoryExistsForKey("device", "Foo"), "A: case differs (Foo) -> no match");
        check(!c.specialCategoryExistsForKey("device", "foo "), "A: trailing space -> no match");
        check(!c.specialCategoryExistsForKey("device", "fo"), "A: prefix fo -> no match");
    }
    {
        const std::string path = gdir + "/G_suffix_block.conf";
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        c.parse();
        check(c.specialCategoryExistsForKey("device", "foo-1"), "G: block name foo-1 matches device foo-1");
        check(!c.specialCategoryExistsForKey("device", "foo"), "G: block name foo-1 does NOT match device foo");
        check(!c.specialCategoryExistsForKey("device", "foo-1-1"), "G: no prefix bleed to foo-1-1");
    }
    {
        const std::string path = gdir + "/H_both_blocks.conf";
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        c.parse();
        bool s = false;
        check(val(c, "kb_layout", "foo", s) == "\"de\"", "H: foo gets de from its own block");
        check(val(c, "kb_layout", "foo-1", s) == "\"fr\"", "H: foo-1 gets fr, independent block");
    }
    {
        const std::string path = gdir + "/I_bracket_form.conf";
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        c.parse();
        check(c.specialCategoryExistsForKey("device", "foo"), "I: bracket form device[foo] creates key foo");
        check(!c.specialCategoryExistsForKey("device", "foo-1"), "I: bracket key foo not foo-1");
    }
    {
        const std::string path = gdir + "/K_dup_blocks_same_key.conf";
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        c.parse();
        bool s = false;
        auto v = val(c, "kb_layout", "foo", s);
        printf("-- K duplicate blocks same name: stored kb_layout=%s\n", v.c_str());
        check(v == "\"fr\"", "K: last duplicate block wins (fr)");
    }
    {
        const std::string path = gdir + "/C_upper_key.conf";
        Hyprlang::CConfig c(path.c_str(), {});
        reg(c);
        c.parse();
        check(c.specialCategoryExistsForKey("device", "FOO"), "C: config key kept as written (FOO)");
        check(!c.specialCategoryExistsForKey("device", "foo"), "C: config key FOO never matches device foo (no folding)");
    }
    printf("FAILURES=%d\n", failures);
    return failures ? 1 : 0;
}
