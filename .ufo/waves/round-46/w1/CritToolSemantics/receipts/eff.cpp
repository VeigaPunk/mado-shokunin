#include <hyprlang.hpp>
#include <cstdio>
#include <string>
#include <any>
using namespace Hyprlang;
static const char* KEYS[] = {"kb_layout","kb_variant","kb_options","kb_model","kb_rules","kb_file"};
int main(int argc, char** argv) {
    if (argc < 2) return 1;
    CConfig c(argv[1], (SConfigOptions){.allowMissingConfig=1});
    c.addConfigValue("input:kb_layout", CConfigValue("us"));
    c.addConfigValue("input:kb_variant", CConfigValue(""));
    c.addConfigValue("input:kb_options", CConfigValue(""));
    c.addConfigValue("input:kb_model", CConfigValue(""));
    c.addConfigValue("input:kb_rules", CConfigValue(""));
    c.addConfigValue("input:kb_file", CConfigValue(""));
    c.addSpecialCategory("device", (SSpecialCategoryOptions){.key="name"});
    for (const char* k : KEYS) c.addSpecialConfigValue("device", k, CConfigValue(""));
    c.addSpecialConfigValue("device", "scroll_factor", CConfigValue((FLOAT)0));
    c.commence();
    auto r = c.parse();
    printf("{\"error\":%s", r.error ? "\"yes\"" : "null");
    printf(",\"globals\":{");
    bool first = true;
    for (const char* k : KEYS) {
        std::string n = std::string("input:") + k;
        auto* v = c.getConfigValuePtr(n.c_str());
        printf("%s\"%s\":[\"%s\",%d]", first ? "" : ",", k, v ? std::any_cast<STRING>(v->getValue()) : "", v ? (int)v->m_bSetByUser : -1);
        first = false;
    }
    printf("},\"devices\":{");
    first = true;
    for (auto& dev : c.listKeysForSpecialCategory("device")) {
        printf("%s\"%s\":{", first ? "" : ",", dev.c_str());
        first = false;
        bool f2 = true;
        for (const char* k : KEYS) {
            auto* v = c.getSpecialConfigValuePtr("device", k, dev.c_str());
            printf("%s\"%s\":[\"%s\",%d]", f2 ? "" : ",", k, v ? std::any_cast<STRING>(v->getValue()) : "", v ? (int)v->m_bSetByUser : -1);
            f2 = false;
        }
        auto* sf = c.getSpecialConfigValuePtr("device", "scroll_factor", dev.c_str());
        printf(",\"scroll_factor\":[%g,%d]}", sf ? (double)std::any_cast<FLOAT>(sf->getValue()) : 0.0, sf ? (int)sf->m_bSetByUser : -1);
    }
    printf("}}\n");
    return 0;
}
