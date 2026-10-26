#include <hyprlang.hpp>
#include <cstdio>
#include <string>
#include <any>
using namespace Hyprlang;
static const char* KEYS[] = {"kb_layout","kb_variant"};
static CConfig* C;
static CParseResult onSource(const char* cmd, const char* val) { return C->parseFile(val); }
int main(int argc, char** argv) {
    C = new CConfig(argv[1], (SConfigOptions){.allowMissingConfig=1});
    C->addConfigValue("input:kb_layout", CConfigValue("us"));
    C->addConfigValue("input:kb_variant", CConfigValue(""));
    C->addSpecialCategory("device", (SSpecialCategoryOptions){.key="name"});
    for (const char* k : KEYS) C->addSpecialConfigValue("device", k, CConfigValue(""));
    C->registerHandler(&onSource, "source", {false});
    C->commence();
    auto r = C->parse();
    printf("err=%s\n", r.error ? r.getError() : "-");
    for (auto& dev : C->listKeysForSpecialCategory("device")) {
        printf("dev=%s", dev.c_str());
        for (const char* k : KEYS) {
            auto* v = C->getSpecialConfigValuePtr("device", k, dev.c_str());
            printf(" %s='%s' set=%d", k, v ? std::any_cast<STRING>(v->getValue()) : "NULL", v ? (int)v->m_bSetByUser : -1);
        }
        printf("\n");
    }
    auto* g = C->getConfigValuePtr("input:kb_layout");
    printf("global='%s' set=%d\n", std::any_cast<STRING>(g->getValue()), (int)g->m_bSetByUser);
    return 0;
}
