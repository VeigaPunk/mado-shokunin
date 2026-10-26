#include <muParser.h>
#include <iostream>
#include <fstream>
int main(){ std::string line; while(std::getline(std::cin,line)){ mu::Parser p; p.DefineConst("window_w",300); p.DefineConst("window_h",200);p.DefineConst("window_x",5);p.DefineConst("window_y",6);p.DefineConst("monitor_w",1920);p.DefineConst("monitor_h",1080);p.DefineConst("cursor_x",7);p.DefineConst("cursor_y",8);
 try{p.SetExpr(line); std::cout<<"OK  ["<<line<<"] = "<<p.Eval()<<"\n";}catch(mu::Parser::exception_type&e){std::cout<<"ERR ["<<line<<"] "<<e.GetMsg()<<"\n";}}}
