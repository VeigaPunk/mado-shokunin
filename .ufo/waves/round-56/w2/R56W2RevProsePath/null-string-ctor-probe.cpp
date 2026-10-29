#include <cstdlib>
#include <cstdio>
#include <string>
int main() {
    const char* p = std::getenv("R56_UNSET_HOME_PROBE");   // unset env var -> nullptr, same as getenv("HOME") when unset
    try {
        std::string s(p);      // what absolutePath line 66 does: std::string(ENVHOME)
        std::printf("constructed len=%zu\n", s.size());
    } catch (const std::exception& e) {
        std::printf("threw: %s\n", e.what());
    }
    return 0;
}
