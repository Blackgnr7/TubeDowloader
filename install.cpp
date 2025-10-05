#include <iostream>
#include <cstdlib>
#include <string>
#include <algorithm>

int main(int argc, char* argv[]){
    #ifdef _WIN32
        std::string path = argv[0];;
        size_t last_slash_pos = path.find_last_of("/\\");
        std::string diretorio = path.substr(0, last_slash_pos);
        std::cout << diretorio << std::endl;
        std::string command = "setx PATH \"%PATH%;" + diretorio + "\"";       
        system(command.c_str());
    #elif __linux__
        std::string path = argv[0];;
        size_t last_slash_pos = path.find_last_of("/\\");
        std::string diretorio = path.substr(0, last_slash_pos);
        std::cout << diretorio << std::endl;
        system("sudo mv" + diretorio + "/usr/local/bin")
    #elif __APPLE__
        std::string path = argv[0];;
        size_t last_slash_pos = path.find_last_of("/\\");
        std::string diretorio = path.substr(0, last_slash_pos);
        std::cout << diretorio << std::endl;
        system("sudo mv" + diretorio + "/usr/local/bin")
    #else
        printf("Desconhecido\n");
    #endif
    system("pause");    
    return 0;
}