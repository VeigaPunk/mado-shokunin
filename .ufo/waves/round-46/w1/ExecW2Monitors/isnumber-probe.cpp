#include <hyprutils/string/String.hpp>
#include <cstdio>
#include <string>
int main() {
    const char* cases[] = {"3","07","+3","-0","123456789","1234567890","3.5","", " 3","0x10","1e3","-","7abc","-7"};
    for (auto c : cases) {
        printf("isNumber(\"%s\")=%d isNumber(float)=%d\n", c,
               (int)Hyprutils::String::isNumber(std::string{c}), (int)Hyprutils::String::isNumber(std::string{c}, true));
    }
    return 0;
}
