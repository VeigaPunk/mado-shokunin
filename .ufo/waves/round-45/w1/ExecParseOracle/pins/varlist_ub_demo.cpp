// Minimal demonstration of the pinned CVarList2 hazard the model deliberately does not reproduce:
// m_args holds string_views into m_copyStrings, so a *second* escaped field reallocates that vector and
// the earlier views dangle (undefined behaviour; libstdc++ leaves the moved-from string empty).
// Built against hyprutils v0.14.2 src/string/VarList2.cpp + String.cpp.
#include <hyprutils/string/VarList2.hpp>
#include <iostream>
#include <string>

int main() {
    for (const char* t : {"a\\,b, c", "a\\,b, c\\,d, 0x0, 1", "DP-1, 1x1, 0x0, 1"}) {
        const auto A = Hyprutils::String::CVarList2(std::string{t});
        std::cout << t << " -> size=" << A.size() << " :";
        for (size_t i = 0; i < A.size(); ++i)
            std::cout << " [" << std::string{A[i]} << "]";
        std::cout << "\n";
    }
    return 0;
}
