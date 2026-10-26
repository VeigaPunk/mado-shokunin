#include <hyprlang.hpp>
#include <cstdio>
#include <string>
#include <any>
using namespace Hyprlang;
static void run(const char* name, const std::string& s) {
    CConfig c(s.c_str(), (SConfigOptions){.allowMissingConfig=1, .pathIsStream=1});
    c.addConfigValue("input:kb_layout", CConfigValue("us"));
    c.commence();
    auto r = c.parse();
    auto* g = c.getConfigValuePtr("input:kb_layout");
    printf("%-28s err=%-3s global='%s' set=%d\n", name, r.error?"yes":"-", std::any_cast<STRING>(g->getValue()), (int)g->m_bSetByUser);
}
int main() {
    run("vt_before_hash", "\x0b#hyprlang if false\ninput:kb_layout = fr\n");
    run("ff_before_hash", "\x0c#hyprlang if false\ninput:kb_layout = fr\n");
    run("space_before_hash", "   #hyprlang if false\ninput:kb_layout = fr\n");
    run("vt_rhs", "input:kb_layout = \x0bfr\n");
    run("tab_directive", "#\thyprlang\tif\tfalse\ninput:kb_layout = fr\n");
    return 0;
}
