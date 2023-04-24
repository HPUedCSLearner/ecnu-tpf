#include "AddrMap.hpp"
#include "ParseAddr.hpp"

using namespace MyUtils;

int main(int argc, char **argv)
{

    if (argc != 4) {
        std::cout << "ERROR: args must be 3" << std::endl;
        exit(1);
    }

    std::cout << argc << std::endl;
    std::string funcMapInfoFile {argv[1]};
    std::string tobeParsedFile {argv[2]};
    std::string outParseFile {argv[3]};

    auto addrMapNamePtr = std::make_shared<AddrMapName>(funcMapInfoFile);
    addrMapNamePtr->init();

    auto parsePtr = std::make_shared<ParseAddr>(addrMapNamePtr, tobeParsedFile);

    parsePtr->parseToFile(outParseFile);

    return 0;
}


// SO the run command may be below:

// ./a.out funcMapInfoFile tobeParsedFile outParseFile
// OR
// ./a.out ./funcMapInfoFile ./tobeParsedFile ./outParseFile





// no sence text

    // auto addrMapNamePtr = std::make_shared<AddrMapName>("./a.out.terminal");
    // addrMapNamePtr->init();

    // std::string parseFilename {"131015__2023-03-17__16-04-11_functrace.csv"};
    // auto parsePtr = std::make_shared<ParseAddr>(addrMapNamePtr, parseFilename);

    // parsePtr->parseToFile("./parseToFile.out");  

