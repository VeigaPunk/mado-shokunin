// scale_oracle.cpp - literal transcription of Hyprland 0.56.2 (efb50993)
// src/helpers/Monitor.cpp CMonitor::applyMonitorRule, explicit-scale branch
// (.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp:989-1051).
//
// Kept: float m_scale and float searchScale, double Vector2D components,
// std::round (half away from zero), the `float + size_t` promotion in
// (searchScale +- i), the 1..89 search, the missing z>0 guard, and the
// "no clean divisor" fallback (autoScale == false -> getDefaultScale()).
// Dropped: autoScale branch (m_scale = getDefaultScale()) and the notification.
//
// stdin : one case per line, "S W H"  (S decimal text parsed with std::stof,
//         as CMonitorRuleParser::parseScale does; W,H integers)
// stdout: "SBITS RBITS FOUND" per case, lowercase hex 8 digits.
//         SBITS = bits of the parsed float rule scale, RBITS = bits of the
//         resulting m_scale, FOUND = 1 when a corrected scale was selected,
//         0 when the "failed to find a clean divisor" fallback ran (so RBITS is
//         getDefaultScale(), not modelled here), 2 when S was integral from the
//         start (m_scale untouched).
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>

struct V2 {
    double x, y;
};

static V2 vdiv(V2 a, float s) { return V2{a.x / (double)s, a.y / (double)s}; }
static V2 vdiv(V2 a, double s) { return V2{a.x / s, a.y / s}; }
static V2 vround(V2 a) { return V2{std::round(a.x), std::round(a.y)}; }
static bool veq(V2 a, V2 b) { return a.x == b.x && a.y == b.y; }

struct Res {
    float    scale;
    int      state; // 1 corrected, 2 untouched, 0 fallback
};

static Res apply_scale(float m_scale, double wx, double hy) {
    V2 pixelSize{wx, hy}; // m_pixelSize = m_size, exact mode resolution
    V2 logicalSize = vdiv(pixelSize, m_scale);

    if (logicalSize.x != std::round(logicalSize.x) || logicalSize.y != std::round(logicalSize.y)) {
        float    searchScale = std::round(m_scale * 120.0);
        bool     found       = false;
        double   scaleZero   = searchScale / 120.0;
        V2       logicalZero = vdiv(pixelSize, scaleZero);

        if (veq(logicalZero, vround(logicalZero)))
            m_scale = scaleZero;
        else {
            for (size_t i = 1; i < 90; ++i) {
                double scaleUp   = (searchScale + i) / 120.0;
                double scaleDown = (searchScale - i) / 120.0;

                V2 logicalUp   = vdiv(pixelSize, scaleUp);
                V2 logicalDown = vdiv(pixelSize, scaleDown);

                if (veq(logicalUp, vround(logicalUp))) {
                    found       = true;
                    searchScale = scaleUp;
                    break;
                }
                if (veq(logicalDown, vround(logicalDown))) {
                    found       = true;
                    searchScale = scaleDown;
                    break;
                }
            }
            if (!found)
                return Res{m_scale, 0}; // autoScale == false -> getDefaultScale()
            m_scale = searchScale;
        }
        return Res{m_scale, 1};
    }
    return Res{m_scale, 2};
}

static uint32_t bits(float f) {
    uint32_t u;
    std::memcpy(&u, &f, 4);
    return u;
}

int main() {
    char sbuf[64];
    double w = 0, h = 0;
    while (std::scanf("%63s %lf %lf", sbuf, &w, &h) == 3) {
        float s = std::stof(std::string(sbuf));
        Res   r = apply_scale(s, w, h);
        std::printf("%08x %08x %d\n", bits(s), bits(r.scale), r.state);
    }
    return 0;
}
