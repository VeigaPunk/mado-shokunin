#include <hyprlang.hpp>
#include <cstdio>
#include <string>
#include <vector>
#include <any>
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

static void q(CConfig* c, const char* dev, const char* key, bool isFloat=false) {
    auto* v = c->getSpecialConfigValuePtr("device", key, dev);
    if (!v) { printf("  q(%s,%s)=NULL\n", dev, key); return; }
    if (isFloat) printf("  q(%s,%s)=%g set=%d\n", dev, key, (double)std::any_cast<FLOAT>(v->getValue()), (int)v->m_bSetByUser);
    else printf("  q(%s,%s)='%s' set=%d\n", dev, key, std::any_cast<STRING>(v->getValue()), (int)v->m_bSetByUser);
}

int main() {
    struct T { const char* name; const char* src; };
    std::vector<T> ts = {
      {"t1_block_name_first", "device {\n name = kbd\n kb_layout = fr\n}\n"},
      {"t2_block_key_first",  "device {\n kb_layout = fr\n name = kbd\n}\n"},
      {"t3_bracket",          "device[kbd] {\n kb_layout = fr\n}\n"},
      {"t4_empty_and_num",    "device {\n name = kbd\n kb_layout = [[EMPTY]]\n scroll_factor = 150\n}\n"},
      {"t5_two_blocks_same",  "device {\n name = a\n kb_layout = fr\n}\ndevice {\n name = a\n kb_variant = intl\n}\n"},
      {"t6_rename",           "device {\n name = a\n name = b\n kb_layout = fr\n}\n"},
      {"t7_hyprlangx_if",     "#hyprlangx if false\ninput:kb_layout = fr\n"},
      {"t8_hyprlang_if",      "#hyprlang if false\ninput:kb_layout = fr\n"},
      {"t9_no_name_key",      "device {\n name = k\n}\n"},
      {"t10_dotted",          "device {\n name = k\n kb_layout = us\n}\ninput:kb_layout = de\n"},
    };
    for (auto& t : ts) {
        std::string err; CConfig* c = mk(t.src, err);
        printf("== %s err=%s\n", t.name, err.empty() ? "-" : err.c_str());
        for (const char* dev : {"kbd","k","a","b","0"}) {
            q(c, dev, "kb_layout");
            q(c, dev, "kb_variant");
        }
        q(c, "kbd", "scroll_factor", true);
        printf("  exists(kbd)=%d exists(a)=%d\n", (int)c->specialCategoryExistsForKey("device","kbd"), (int)c->specialCategoryExistsForKey("device","a"));
        auto* g = c->getConfigValuePtr("input:kb_layout");
        printf("  global input:kb_layout='%s' set=%d\n", std::any_cast<STRING>(g->getValue()), (int)g->m_bSetByUser);
        delete c;
    }
    return 0;
}
