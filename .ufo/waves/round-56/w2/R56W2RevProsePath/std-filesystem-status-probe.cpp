#include <filesystem>
#include <cstdio>
namespace fs = std::filesystem;
static void show(const char* p) {
    std::error_code ec;
    auto st = fs::status(p, ec);
    std::printf("%-22s status_ec=%s regular=%d dir=%d\n", p, ec ? ec.message().c_str() : "ok",
                (int)fs::is_regular_file(st), (int)fs::is_directory(st));
}
int main() {
    show("d/real.conf"); show("d/link.conf"); show("d/dangle.conf"); show("d/dirlink"); show("d/missing.conf");
}
