// Lab: does std::format("{:.2f}", float) equal Python '%.2f' % double(f32)?
// Emits one line per value: <hexbits>\t<fmt(float)>\t<fmt(double)>\t<source>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <cstdint>
#include <string>
#include <format>
#include <random>

static void emit(float f) {
    uint32_t bits;
    std::memcpy(&bits, &f, 4);
    std::string a = std::format("{:.2f}", f);
    std::string b = std::format("{:.2f}", static_cast<double>(f));
    std::printf("%08x\t%s\t%s\n", bits, a.c_str(), b.c_str());
}

int main(int argc, char** argv) {
    if (argc < 2) return 2;
    const std::string mode = argv[1];
    if (mode == "three-decimals") {
        // exactly what the tool reads: a 3-decimal decimal string through std::stof
        long n = 0;
        for (long i = 0; i <= 100000; ++i) {
            char buf[32];
            std::snprintf(buf, sizeof buf, "%ld.%03ld", i / 1000, i % 1000);
            float f = std::stof(buf);
            emit(f);
            ++n;
        }
        std::fprintf(stderr, "three-decimals=%ld\n", n);
        return 0;
    }
    if (mode == "ties") {
        // exact midpoints of 2-decimal grid reachable in binary: m/8 with m odd
        long n = 0;
        for (int m = 1; m <= 800; m += 2) {
            emit(static_cast<float>(m) / 8.0f);
            ++n;
        }
        std::fprintf(stderr, "ties=%ld\n", n);
        return 0;
    }
    if (mode == "random-bits") {
        long count = std::atol(argv[2]);
        uint64_t seed = std::strtoull(argv[3], nullptr, 10);
        std::mt19937_64 rng(seed);
        long n = 0, skipped = 0;
        while (n < count) {
            uint32_t bits = static_cast<uint32_t>(rng());
            float f;
            std::memcpy(&f, &bits, 4);
            if (!std::isfinite(f)) { ++skipped; continue; }
            emit(f);
            ++n;
        }
        std::fprintf(stderr, "random-bits=%ld skipped=%ld seed=%llu\n", n, skipped,
                     static_cast<unsigned long long>(seed));
        return 0;
    }
    if (mode == "random-range") {
        long count = std::atol(argv[2]);
        uint64_t seed = std::strtoull(argv[3], nullptr, 10);
        std::mt19937_64 rng(seed);
        std::uniform_real_distribution<double> u(0.0, 100.0);
        long n = 0;
        while (n < count) {
            float f = static_cast<float>(u(rng));
            emit(f);
            ++n;
        }
        std::fprintf(stderr, "random-range=%ld seed=%llu\n", n,
                     static_cast<unsigned long long>(seed));
        return 0;
    }
    if (mode == "boundaries") {
        // every rounding midpoint k/200 (k odd, 0..100) and its 3 nearest f32 neighbours on each side,
        // plus the two values the tool can see without a device block: +0.0 and -1.0.
        long n = 0;
        for (int k = 1; k <= 20000; k += 2) {
            double mid = k / 200.0;                 // exact midpoint of the 2-decimal grid
            float  f   = static_cast<float>(mid);   // nearest f32 to the midpoint
            emit(f);
            ++n;
            float lo = f, hi = f;
            for (int i = 0; i < 3; ++i) {
                lo = std::nextafterf(lo, -INFINITY);
                hi = std::nextafterf(hi, INFINITY);
                emit(lo);
                emit(hi);
                n += 2;
            }
        }
        emit(0.0f);
        emit(-0.0f);
        emit(-1.0f);
        n += 3;
        std::fprintf(stderr, "boundaries=%ld\n", n);
        return 0;
    }
    std::fprintf(stderr, "unknown mode\n");
    return 2;
}
