#include <hyprlang.hpp>
#include <cstdio>
#include <string>
#include <vector>
#include <any>
#include <cmath>
using namespace Hyprlang;
static CConfig* mk(const std::string& stream, std::string& err) {
    CConfig* c = new CConfig(stream.c_str(), (SConfigOptions){.allowMissingConfig=1, .pathIsStream=1});
    c->addConfigValue("input:kb_layout", CConfigValue("us"));
    c->addConfigValue("input:kb_variant", CConfigValue(""));
    c->addConfigValue("input:scroll_factor", CConfigValue((FLOAT)1));
    c->addSpecialCategory("device", (SSpecialCategoryOptions){.key="name"});
    for (const char* k : {"kb_layout","kb_variant","kb_options","kb_model","kb_rules","kb_file"})
        c->addSpecialConfigValue("device", k, CConfigValue(""));
    c->addSpecialConfigValue("device", "scroll_factor", CConfigValue((FLOAT)0));
    c->commence();
    auto r = c->parse();
    err = r.error ? r.getError() : "";
    return c;
}
static void q(CConfig* c, const char* dev, const char* key) {
    auto* v = c->getSpecialConfigValuePtr("device", key, dev);
    printf(" %s/%s=%s set=%d", dev, key, v ? std::any_cast<STRING>(v->getValue()) : "NULL", v ? (int)v->m_bSetByUser : -1);
}
int main() {
    struct T { const char* name; const char* src; };
    std::vector<T> ts = {
      {"A_hyprlangfoo_if",  "#hyprlangfoo if false\ninput:kb_layout = fr\n"},
      {"B_noerror",         "#hyprlang noerror\ninput:kb_layout = fr\n"},
      {"C_hyprlangx_bare",  "#hyprlangx\ninput:kb_layout = fr\n"},
      {"D_if_true",         "#hyprlang if true\ninput:kb_layout = fr\n"},
      {"E_spaces",          "#  hyprlangx  if  false\ninput:kb_layout = fr\n"},
      {"F_hash_hash_name",  "device {\n name = a##b\n kb_layout = fr\n}\n"},
      {"G_crlf",            "device {\r\n name = kbd\r\n kb_layout = fr\r\n}\r\n"},
      {"H_nested_input",    "device {\n name = a\n input {\n  kb_layout = fr\n }\n kb_variant = intl\n}\n"},
      {"I_second_block",    "device {\n name = a\n kb_layout = fr\n}\ndevice {\n kb_variant = intl\n}\n"},
      {"J_backslash",       "device {\\\n name = kbd\n kb_layout = fr\n}\n"},
      {"K_comment_in_name", "device {\n name = kbd#tail\n kb_layout = fr\n}\n"},
      {"L_brace_sameline",  "device { name = kbd\n kb_layout = fr\n}\n"},
    };
    for (auto& t : ts) {
        std::string err; CConfig* c = mk(t.src, err);
        printf("== %s err=%s\n ", t.name, err.empty() ? "-" : err.c_str());
        q(c,"kbd","kb_layout"); q(c,"a","kb_layout"); q(c,"a","kb_variant"); q(c,"a#b","kb_layout");
        auto* g = c->getConfigValuePtr("input:kb_layout");
        printf(" global='%s' set=%d\n", std::any_cast<STRING>(g->getValue()), (int)g->m_bSetByUser);
        delete c;
    }
    printf("== stof\n");
    for (const char* s : {"1e-50","1e-40","2e-38","inf","nan","0x10","abc","1.2.3","+.5","5e39","1e400","1,5"}) {
        try { float f = std::stof(s); printf(" stof(%s)=%g\n", s, (double)f); }
        catch (const std::exception& e) { printf(" stof(%s) THROWS %s\n", s, e.what()); }
    }
    return 0;
}
