// Simulator: exact transcription of Hyprland 0.56.2 (efb50993)
//   src/helpers/MiscFunctions.cpp:777-790 deviceNameToInternalString
//   src/managers/input/InputManager.cpp:2119-2131 getNameForNewDevice
// driven over plug/unplug sequences. m_hids holds keyboards, mice and touch devices
// (InputManager.cpp:1138, 1322, 1946; erased at 1532), so the namespace is shared.
#include <algorithm>
#include <cctype>
#include <cstdio>
#include <string>
#include <vector>

struct HID { std::string m_hlName; };

static std::vector<HID> m_hids;

static std::string deviceNameToInternalString(const std::string& in) {
    std::string out;
    for (unsigned char ch : in) {
        switch (ch) {
            case ' ':
            case '\n':
            case ',': out += '-'; break;
            default: out += (char)std::tolower(ch);
        }
    }
    return out;
}

static std::string getNameForNewDevice(std::string internalName) {
    auto proposedNewName = deviceNameToInternalString(internalName);
    int  dupeno          = 0;
    auto makeNewName     = [&]() { return (proposedNewName.empty() ? "unknown-device" : proposedNewName) + (dupeno == 0 ? "" : ("-" + std::to_string(dupeno))); };
    while (std::ranges::find_if(m_hids, [&](const auto& other) { return other.m_hlName == makeNewName(); }) != m_hids.end())
        dupeno++;
    return makeNewName();
}

static void plug(const char* physical) {
    HID h;
    h.m_hlName = getNameForNewDevice(physical);
    m_hids.emplace_back(h);
    printf("  plug [%s] -> [%s]   live:", physical, h.m_hlName.c_str());
    for (auto& x : m_hids) printf(" %s", x.m_hlName.c_str());
    printf("\n");
}

static void unplug(const char* hlName) {
    auto it = std::find_if(m_hids.begin(), m_hids.end(), [&](const auto& h) { return h.m_hlName == hlName; });
    if (it != m_hids.end()) m_hids.erase(it);
    printf("  unplug [%s]   live:", hlName);
    for (auto& x : m_hids) printf(" %s", x.m_hlName.c_str());
    printf("\n");
}

static void scenario(const char* label) { m_hids.clear(); printf("=== %s\n", label); }

int main() {
    scenario("1 three identical");
    plug("Foo"); plug("Foo"); plug("Foo");

    scenario("2 plug, unplug all, plug again");
    plug("Foo"); unplug("foo"); plug("Foo");

    scenario("3 physical device already named -1 plugs first");
    plug("Foo 1"); plug("Foo"); plug("Foo");

    scenario("4 duplicate pair then a device whose name maps to foo-1");
    plug("Foo"); plug("Foo"); plug("Foo 1");

    scenario("5 first of a duplicate pair unplugged, a new identical unit plugged");
    plug("Foo"); plug("Foo"); unplug("foo"); plug("Foo");

    scenario("6 case-only difference is a duplicate");
    plug("FOO"); plug("foo");

    scenario("7 keyboard and mouse share the namespace");
    plug("Foo"); plug("foo");

    scenario("8 empty name");
    plug(""); plug("");

    scenario("9 virtual keyboards from the same client");
    plug("hl-virtual-keyboard"); plug("hl-virtual-keyboard");

    scenario("10 comma and space normalise to the same dash form");
    plug("Foo,Bar"); plug("Foo Bar"); plug("foo-bar");

    scenario("11 highest live suffix removed, then replug");
    plug("Foo"); plug("Foo"); plug("Foo"); unplug("foo-1"); plug("Foo");
    return 0;
}
