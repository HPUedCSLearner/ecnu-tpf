#include <stdio.h>

#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/IRBuilder.h>

using namespace llvm;

int main()
{
    auto llvmContext = std::make_unique<LLVMContext>();
    auto module = std::make_unique<Module>("ir", *llvmContext);
    auto irBuilder = std::make_unique<IRBuilder<>>(*llvmContext);

    Type *intType = irBuilder->getInt32Ty();
    FunctionType *fType = FunctionType::get(intType, {intType, intType}, false);
    Function *sumFunc = Function::Create(fType, GlobalValue::ExternalLinkage, "sum", *module);

    BasicBlock *entryBB = BasicBlock::Create(*llvmContext, "entry", sumFunc);

    irBuilder->SetInsertPoint(entryBB);
    AllocaInst *a = irBuilder->CreateAlloca(intType, nullptr, "a");
    AllocaInst *b = irBuilder->CreateAlloca(intType, nullptr, "b");
    AllocaInst *ret = irBuilder->CreateAlloca(intType, nullptr, "ret");
    irBuilder->CreateStore(sumFunc->getArg(0), a);
    irBuilder->CreateStore(sumFunc->getArg(1), b);
    Value *sum = irBuilder->CreateNSWAdd(a, b);
    irBuilder->CreateStore(sum, ret);
    irBuilder->CreateRet(ret);



    module->print(errs(), nullptr);

    return 0;
}