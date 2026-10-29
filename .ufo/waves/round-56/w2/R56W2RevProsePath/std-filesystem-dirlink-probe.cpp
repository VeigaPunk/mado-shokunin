#include <filesystem>
#include <cstdio>
namespace fs = std::filesystem;
int main(){ std::error_code ec; auto st=fs::status("topdirlink",ec);
 std::printf("topdirlink status_ec=%s dir=%d regular=%d\n", ec?ec.message().c_str():"ok", (int)fs::is_directory(st), (int)fs::is_regular_file(st)); }
