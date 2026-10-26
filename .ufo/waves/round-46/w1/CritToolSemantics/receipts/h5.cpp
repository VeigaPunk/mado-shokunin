#include <hyprlang.hpp>
#include <cstdio>
#include <string>
#include <any>
using namespace Hyprlang;
static void run(const char* name, const std::string& s) {
    CConfig c(s.c_str(), (SConfigOptions){.allowMissingConfig=1, .pathIsStream=1});
    c.addConfigValue("input:kb_layout", CConfigValue("us"));
    c.addConfigValue("input:kb_variant", CConfigValue(""));
    c.commence();
    auto r = c.parse();
    auto* g = c.getConfigValuePtr("input:kb_layout");
    printf("%-24s err=%-8s global=[", name, r.error ? "yes" : "-");
    for (const char* p = std::any_cast<STRING>(g->getValue()); *p; ++p) printf("%02x", (unsigned char)*p);
    printf("] set=%d\n", (int)g->m_bSetByUser);
}
int main() {
    run("vt_directive",    std::string(1,'\x0b') + "#hyprlang if false\ninput:kb_layout = fr\n");
    run("plain_directive", "#hyprlang if false\ninput:kb_layout = fr\n");
    run("vt_hash_only",    std::string(1,'\x0b') + "# note\ninput:kb_layout = fr\n");
    run("vt_rhs",          "input:kb_layout = " + std::string(1,'\x0b') + "fr\n");
    return 0;
}
