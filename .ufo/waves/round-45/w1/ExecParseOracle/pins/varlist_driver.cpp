// Reads one config-value line per stdin line, prints the CVarList2 split as JSON array of strings.
// Built against the pinned hyprutils v0.14.2 sources: src/VarList2.cpp, src/String.cpp,
// include/hyprutils/string/{VarList2,String}.hpp (see pins/SHA256SUMS.txt).
#include <hyprutils/string/VarList2.hpp>
#include <iomanip>
#include <iostream>
#include <string>

int main() {
    std::string line;
    size_t      n = 0;
    while (std::getline(std::cin, line)) {
        const auto ARGS = Hyprutils::String::CVarList2(std::string{line});
        std::cout << n++ << "\t[";
        for (size_t i = 0; i < ARGS.size(); ++i) {
            if (i)
                std::cout << ",";
            std::cout << "\"";
            for (char c : std::string{ARGS[i]}) {
                if (c == '"' || c == '\\')
                    std::cout << "\\" << c;
                else if (static_cast<unsigned char>(c) < 0x20)
                    std::cout << "\\u00" << std::hex << std::setw(2) << std::setfill((char)48) << (int)(unsigned char)c << std::dec;
                else
                    std::cout << c;
            }
            std::cout << "\"";
        }
        std::cout << "]\n";
    }
    return 0;
}
