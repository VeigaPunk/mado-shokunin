// stmt.cpp — exact reproduction of the Hyprland 0.56.2 scroll-factor arithmetic.
//  parse:  Hyprland-InputManager.cpp:1379-1383
//            if (deviceConfigExplicitlySet(dev,"scroll_factor"))
//              m_scrollFactor = std::clamp(getDeviceFloat(...), 0.F, 100.F);   // optional<float>
//            else m_scrollFactor = std::nullopt;
//          hyprlang-config.cpp:465-472 (CONFIGDATATYPE_FLOAT) is the only producer of the float:
//            VALUEIT->second.setFrom(std::stof(value)); catch -> setError, m_bSetByUser stays false.
//  print:  Hyprland-HyprCtl.cpp:765-772  std::format(R"(...#(...,"scrollFactor": {:.2f}...)#", ..., value_or(-1))
// stdin: one candidate RHS per line (already trimmed the way each side trims it).
// stdout: STATUS \t BITS-or-reason \t PRINTED
#include <algorithm>
#include <bit>
#include <cstdint>
#include <cstring>
#include <format>
#include <iostream>
#include <optional>
#include <string>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::optional<float> scroll;                 // m_scrollFactor
        std::string          err;
        try {
            scroll = std::clamp(std::stof(line), 0.F, 100.F);   // hyprlang parse + std::clamp
        } catch (const std::invalid_argument&) { err = "invalid_argument";
        } catch (const std::out_of_range&)     { err = "out_of_range";
        } catch (const std::exception& e)      { err = std::string("other:") + e.what(); }
        if (!scroll) { std::cout << "UNSET\t" << err << "\t-\n"; continue; }
        // HyprCtl prints the optional<float> via value_or(-1)
        std::string printed = std::format("{:.2f}", scroll.value_or(-1));
        std::cout << "SET\t" << std::format("{:08x}", std::bit_cast<uint32_t>(*scroll)) << "\t"
                  << printed << "\n";
    }
}
