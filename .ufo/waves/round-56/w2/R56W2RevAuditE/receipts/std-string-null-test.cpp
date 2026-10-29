#include <string>
#include <cstdio>
int main(){ const char* p = nullptr; try { std::string s(p); printf("constructed len=%zu\n", s.size()); } catch (const std::exception& e){ printf("threw: %s\n", e.what()); } return 0; }
