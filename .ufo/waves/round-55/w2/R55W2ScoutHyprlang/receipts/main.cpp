#include <algorithm>
#include <cmath>
#include <cstdint>
#include <expected>
#include <iostream>
#include <string>

namespace Hyprlang {
    typedef std::int64_t INT;
}

namespace Hyprutils {
    namespace String {
        std::string trim(const std::string& in);
        bool        isNumber(const std::string& str, bool allowfloat = false);
    }
}

using namespace Hyprutils::String;

#include "string.inc"
#include "body.inc"

int main() {
    const char* toks[] = {"0x10",  "0X10", "+5",      "007",     "-3",     "3.5",   "5.",   ".5",    "true",
                          "true1", "on",   "onion",   "yes",     "yes123", "false", "off",  "no",    "nope",
                          "25",    "0",    "200",     "201",     "",       "   25", "25 ",  "1e3",   "0b101",
                          "-0x10", "--5",  "25#",     "2#3",     "999999", "1000000", "123456789012345678901", "abc"};
    for (auto t : toks) {
        auto r = configStringToInt(std::string(t));
        std::cout << '"' << t << "\" -> "
                  << (r.has_value() ? std::string("OK ") + std::to_string(r.value()) : std::string("ERR ") + r.error())
                  << "\n";
    }
    return 0;
}
