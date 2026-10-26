// NFC vs NFD and non-ASCII case: byte-exact key comparison.
#include <hyprlang.hpp>
#include <cstdio>
#include <fstream>
int main() {
    const std::string body = "device {\n  name = f\xC3\xB6\xC3\xB6\n  kb_layout = de\n}\n"; // NFC föö
    { std::ofstream f("./nfc.conf", std::ios::binary); f << body; }
    Hyprlang::CConfig c("./nfc.conf", {});
    c.addSpecialCategory("device", {"name"});
    c.addSpecialConfigValue("device", "kb_layout", {"us"});
    c.commence();
    c.parse();
    std::printf("stored=%zu\n", c.listKeysForSpecialCategory("device").size());
    const char* nfd = "fo\xCC\x88o\xCC\x88"; // NFD
    const char* upper = "F\xC3\x96\xC3\x96"; // FÖÖ
    std::printf("NFC key exists=%d NFD key exists=%d upper exists=%d\n",
        (int)c.specialCategoryExistsForKey("device", "f\xC3\xB6\xC3\xB6"),
        (int)c.specialCategoryExistsForKey("device", nfd),
        (int)c.specialCategoryExistsForKey("device", upper));
    return 0;
}
