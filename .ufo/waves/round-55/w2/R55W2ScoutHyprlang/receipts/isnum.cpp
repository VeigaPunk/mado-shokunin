#include <iostream>
#include <string>
namespace Hyprutils { namespace String { bool isNumber(const std::string& str, bool allowfloat = false); } }
int main() {
    for (std::string t : {"+5", "007", "-3", "3.5", "0x10", "0X10", "-0", "5", "", "-"})
        std::cout << '"' << t << "\" isNumber(allowfloat=false)=" << Hyprutils::String::isNumber(t, false) << "\n";
    return 0;
}
