// fmtsweep.cpp — does std::format("{:.2f}", float) ever print differently from Python "%.2f"
// on the same binary value? stdin: one 8-hex-digit float32 bit pattern per line.
#include <bit>
#include <cstdint>
#include <cstdio>
#include <format>
#include <iostream>
#include <string>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        uint32_t bits = static_cast<uint32_t>(std::stoul(line, nullptr, 16));
        float    v    = std::bit_cast<float>(bits);
        std::string printed = std::format("{:.2f}", v);
        std::cout << printed << "\n";
    }
}
