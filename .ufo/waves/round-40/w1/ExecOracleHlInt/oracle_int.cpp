// ExecOracleHlInt / round-40 w1 -- oracle over the REAL hyprlang 0.6.8
//
// Registers an INT option `x`, parses the file body `x = <spelling>` through
// Hyprlang::CConfig (the same path Hyprland uses: parseLine -> configSetValueSafe
// -> configStringToInt), and prints one JSON object per corpus entry:
//   id, cat, scope, decl (the corpus spelling), body (the exact file bytes),
//   ok (no parse error), value (stored int, or null on error), error (or null).
//
// Build: g++ -std=c++23 -O2 oracle_int.cpp -o oracle_int $(pkg-config --cflags --libs hyprlang)
// hyprlang 0.6.8 is the installed library (/usr/lib/libhyprlang.so.0.6.8).
#include <hyprlang.hpp>

#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <unistd.h>

static std::string jsonEscape(const std::string& s) {
    std::string out;
    for (unsigned char c : s) {
        switch (c) {
            case '"': out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default:
                if (c < 0x20) {
                    char buf[8];
                    std::snprintf(buf, sizeof buf, "\\u%04x", c);
                    out += buf;
                } else
                    out += static_cast<char>(c);
        }
    }
    return out;
}

// corpus.tsv: id \t cat \t scope \t spelling   (spelling may contain tabs)
struct Entry {
    std::string id, cat, scope, spelling;
};

static std::vector<Entry> readCorpus(const char* path) {
    std::ifstream fh(path);
    if (!fh)
        throw std::runtime_error(std::string("cannot open corpus ") + path);
    std::vector<Entry> out;
    std::string        line;
    while (std::getline(fh, line)) {
        if (line.empty())
            continue;
        std::vector<size_t> tabs;
        for (size_t i = 0; i < line.size() && tabs.size() < 3; ++i)
            if (line[i] == '\t')
                tabs.push_back(i);
        if (tabs.size() != 3)
            throw std::runtime_error("bad corpus line: " + line);
        Entry e;
        e.id       = line.substr(0, tabs[0]);
        e.cat      = line.substr(tabs[0] + 1, tabs[1] - tabs[0] - 1);
        e.scope    = line.substr(tabs[1] + 1, tabs[2] - tabs[1] - 1);
        e.spelling = line.substr(tabs[2] + 1);
        out.push_back(e);
    }
    return out;
}

// A raw entry's spelling is the whole file body; "\n" is a real newline.
static std::string unescape(const std::string& s) {
    std::string out;
    for (size_t i = 0; i < s.size(); ++i) {
        if (s[i] == '\\' && i + 1 < s.size() && s[i + 1] == 'n') {
            out += '\n';
            ++i;
        } else
            out += s[i];
    }
    return out;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        std::cerr << "usage: oracle_int <corpus.tsv> <out.jsonl>\n";
        return 2;
    }
    const auto ENTRIES = readCorpus(argv[1]);

    char tmpl[] = "/tmp/hl-oracle-XXXXXX";
    if (!mkdtemp(tmpl)) {
        std::cerr << "mkdtemp failed\n";
        return 2;
    }
    const std::string cfgPath = std::string(tmpl) + "/cfg.conf";

    std::ofstream out(argv[2]);
    if (!out) {
        std::cerr << "cannot open output\n";
        return 2;
    }

    for (const auto& e : ENTRIES) {
        const std::string BODY = e.cat == "raw" ? unescape(e.spelling) : "x = " + e.spelling + "\n";

        {
            std::ofstream cf(cfgPath, std::ios::binary | std::ios::trunc);
            cf << BODY;
        }

        bool        ok    = false;
        long long   value = 0;
        std::string error;

        try {
            Hyprlang::SConfigOptions opts; // allowMissingConfig = false, not a stream
            Hyprlang::CConfig        cfg(cfgPath.c_str(), opts);
            cfg.addConfigValue("x", Hyprlang::INT{0});
            cfg.commence();

            const auto RES = cfg.parse();
            ok             = !RES.error;
            if (!ok)
                error = RES.getError() ? RES.getError() : "(no error string)";

            const auto ANY = cfg.getConfigValue("x");
            if (ANY.has_value())
                value = static_cast<long long>(std::any_cast<Hyprlang::INT>(ANY));
            else
                error += ok ? " [value missing]" : "";
        } catch (const std::exception& ex) {
            ok    = false;
            error = std::string("exception: ") + ex.what();
        } catch (const char* ex) {
            ok    = false;
            error = std::string("exception: ") + ex;
        } catch (...) {
            ok    = false;
            error = "exception: unknown";
        }

        out << "{\"id\":\"" << jsonEscape(e.id) << "\",\"cat\":\"" << jsonEscape(e.cat) << "\",\"scope\":\"" << jsonEscape(e.scope)
            << "\",\"decl\":\"" << jsonEscape(e.spelling) << "\",\"body\":\"" << jsonEscape(BODY) << "\",\"ok\":" << (ok ? "true" : "false")
            << ",\"value\":" << (ok ? std::to_string(value) : "null") << ",\"stored\":" << value << ",\"error\":"
            << (ok ? "null" : "\"" + jsonEscape(error) + "\"") << "}\n";
    }

    out.close();
    std::remove(cfgPath.c_str());
    rmdir(tmpl);
    return 0;
}
