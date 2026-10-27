// Attack16 reproduction: does xtract's value_or fire for sendshortcut's call path?
// Models Hyprland: PHLWINDOW ~ SP<CWindow> (handle constructible from nullptr),
// Actions::pass(uint32_t, uint32_t, std::optional<PHLWINDOW>),
// xtract: return window.value_or(focused);
#include <iostream>
#include <memory>
#include <optional>
#include <string>

// Minimal stand-in for Hyprland's SP<CWindow>: a value type constructible from nullptr.
struct FakeWindow {};
class SP {
  public:
    SP(std::nullptr_t) : p(nullptr) { std::cout << "SP constructed from nullptr (value type, not a pointer)\n"; }
    SP() : p(nullptr) {}
    explicit operator bool() const { return p != nullptr; }
    FakeWindow* p;
};

// Mirrors xtract at ConfigActions.cpp:47-49
static SP xtract(std::optional<SP> window, SP focused) {
    return window.value_or(focused);
}

int main() {
    SP focused_window; focused_window.p = reinterpret_cast<FakeWindow*>(0x1); // non-null "focused"
    // Translator: PHLWINDOW PWINDOW = regexp.empty() ? nullptr : selector(...);  (empty selector -> nullptr)
    SP PWINDOW = nullptr;   // regexp.empty() branch
    std::cout << "PWINDOW engaged-as-value? operator bool = " << (bool)PWINDOW << "\n";

    // The call: Actions::pass(MOD, keycode, PWINDOW)  ->  parameter std::optional<PHLWINDOW> w
    std::optional<SP> w = PWINDOW;  // converting construction
    std::cout << "optional has_value after conversion from null PWINDOW = " << w.has_value() << "\n";

    SP result = xtract(w, focused_window);
    std::cout << "xtract returned the focused window? " << (bool)result << "  (0 = null handle returned, value_or did NOT fire)\n";

    // Contrast: a caller that passes std::nullopt (disengaged) DOES get the fallback
    SP result2 = xtract(std::nullopt, focused_window);
    std::cout << "xtract(std::nullopt, focused) returns focused? " << (bool)result2 << "\n";

    // Also show: even for a raw pointer type the same holds
    std::optional<FakeWindow*> wp = static_cast<FakeWindow*>(nullptr);
    std::cout << "optional<FakeWindow*> from null raw pointer has_value = " << wp.has_value() << "\n";
    return 0;
}
