#include "llvm/Support/InitLLVM.h"
#include "llvm/Support/raw_ostream.h"
#include "simplelang/Basic/Version.h"

int main(int argc, const char **argv)
{
    llvm::InitLLVM X(argc, argv);

    llvm::outs() << "Hello World! (version " << simplelang::getSimpleLangVersion() << ")\n";
}
