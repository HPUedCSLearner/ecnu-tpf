#include <iostream>
#include <random>
#include <memory>
#include <sstream>
#include <fstream>

#include <functional>

#include<threadPool/threadPool.h>
#include<spdlog/spdlog.h>

#include<processId/process_id.h>
#include<perf/perf_counter.h>


#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/prettywriter.h"


std::random_device rd; // 真实随机数产生器
std::mt19937 mt(rd()); //生成计算随机数mt
std::uniform_int_distribution<int> dist(-1000, 1000); //生成-1000到1000之间的离散均匀分布数
auto rnd = std::bind(dist, mt);
// 设置线程睡眠时间
void simulate_hard_computation()
{
    std::this_thread::sleep_for(std::chrono::milliseconds(2000 + rnd()));
}
// 添加两个数字的简单函数并打印结果
void multiply(const int a, const int b)
{
    simulate_hard_computation();
    const int res = a * b;
    // std::cout << a << " * " << b << " = " << res << std::endl;
    spdlog::info("{} * {} = {}", a, b, res);
}
// 添加并输出结果
void multiply_output(int &out, const int a, const int b)
{
    simulate_hard_computation();
    out = a * b;
    // std::cout << a << " * " << b << " = " << out << std::endl;
    spdlog::info("{} * {} = {}", a, b, out);
}
// 结果返回
int multiply_return(const int a, const int b)
{
    simulate_hard_computation();
    const int res = a * b;
    // std::cout << a << " * " << b << " = " << res << std::endl;
    spdlog::info("{} * {} = {}", a, b, res);
    return res;
}

template <typename... Args>
void INFO(Args &&...args)
{
    spdlog::info(std::forward<Args>(args)...);
}

void example1()
{
    std::ifstream file(std::move(std::string("./config/config.json")));
    std::string strJson((std::istream_iterator<char>(file)), std::istream_iterator<char>()); // 这个括号为什么不能省？？？ <(std::istream_iterator<char>(file))>
    rapidjson::Document json;
    json.Parse(strJson.c_str());
    if (json.HasParseError()) {
        spdlog::error("Parse json ERROR");
    } else {
        spdlog::info("Parse json SUCCESSED");
    }

    auto threads = json["threadPool"]["threads"].GetInt();
    auto ii = json["threadPool"]["i"].GetInt();
    auto jj = json["threadPool"]["j"].GetInt();

    std::shared_ptr<threadPool::ThreadPool> pool = std::make_shared<threadPool::ThreadPool>(threads);
    pool->init();

    // 提交乘法操作，总共30个
    for (int i = 1; i <= ii; ++i) {
        for (int j = 1; j <= jj; ++j)
        {
            pool->submit(multiply, i, j);
        }
    }

    // 使用ref传递的输出参数提交函数
    int output_ref;
    auto future1 = pool->submit(multiply_output, std::ref(output_ref), 5, 6);
    // 等待乘法输出完成
    future1.get();
    std::cout << "Last operation result is equals to " << output_ref << std::endl;


    // 使用return参数提交函数
    auto future2 = pool->submit(multiply_return, 5, 3);
    // 等待乘法输出完成
    int res = future2.get();
    std::cout << "Last operation result is equals to " << res << std::endl;

    pool->shutdown();
}

void example2()
{
    processId::ProcessId::getProcessPid();
    spdlog::info("[{}] [{}] welcome to example!", processId::ProcessId::getProcessPid(), processId::ProcessId::getThreadId());
    spdlog::error("Some error message with arg: {}", 1);
    
    std::stringstream ss; 
    ss << std::this_thread::get_id() ;
    spdlog::info("thread id: {}", ss.str());
}

void example3() {
    using namespace rapidjson;
    const char json[] = " { \"hello\" : \"world\", \"t\" : true , \"f\" : false, \"n\": null, \"i\":123, \"pi\": 3.1416, \"a\":[1, 2, 3, 4] } ";
    printf("Original JSON:\n %s\n", json);

    Document document;  // Default template parameter uses UTF8 and MemoryPoolAllocator.

#if 1
    // "normal" parsing, decode strings to new buffers. Can use other input stream via ParseStream().
    if (document.Parse(json).HasParseError())
#else
    // In-situ parsing, decode strings directly in the source string. Source must be string.
    char buffer[sizeof(json)];
    memcpy(buffer, json, sizeof(json));
    if (document.ParseInsitu(buffer).HasParseError()) {
        spdlog::error("Parse json failed");
    } else {
        spdlog::info("Parse json successed");
    }
#endif
   ////////////////////////////////////////////////////////////////////////////
    // 2. Access values in document. 

    assert(document.IsObject());    // Document is a JSON value represents the root of DOM. Root can be either an object or array.

    assert(document.HasMember("hello"));
    assert(document["hello"].IsString());
    spdlog::info("hello = {}", document["hello"].GetString());
    spdlog::info("hello = {}", document["hello"].GetString());
    spdlog::info("hello = {}", document["hello"].GetString());



 // Since version 0.2, you can use single lookup to check the existing of member and its value:
    Value::MemberIterator hello = document.FindMember("hello");
    assert(hello != document.MemberEnd());
    assert(hello->value.IsString());
    assert(strcmp("world", hello->value.GetString()) == 0);
    (void)hello;


    assert(document["t"].IsBool());     // JSON true/false are bool. Can also uses more specific function IsTrue().
    spdlog::info("t = {}", document["t"].GetBool() ? "true" : "false");

    assert(document["f"].IsBool());
    spdlog::info("f = {}", document["f"].GetBool() ? "ture" : "false");

    spdlog::info("n = {}", document["n"].IsNull() ? "null" : "?");

    assert(document["i"].IsNumber());   // Number is a JSON type, but C++ needs more specific type.
    assert(document["i"].IsInt());      // In this case, IsUint()/IsInt64()/IsUint64() also return true.
    spdlog::info("i = %d", document["i"].GetInt()); // Alternative (int)document["i"]

    assert(document["pi"].IsNumber());
    assert(document["pi"].IsDouble());
    spdlog::info("pi = {}", document["pi"].GetDouble());

        
    {
        const Value& a = document["a"]; // Using a reference for consecutive access is handy and faster.
        assert(a.IsArray());
        for (SizeType i = 0; i < a.Size(); i++) // rapidjson uses SizeType instead of size_t.
            spdlog::info("a[{}] = {}", i, a[i].GetInt());
        
        int y = a[0].GetInt();
        (void)y;

        // Iterating array with iterators
        spdlog::info("a = ");
        for (Value::ConstValueIterator itr = a.Begin(); itr != a.End(); ++itr)
             spdlog::info("{} ", itr->GetInt());
    }

    // Iterating object members
    static const char* kTypeNames[] = { "Null", "False", "True", "Object", "Array", "String", "Number" };
    for (Value::ConstMemberIterator itr = document.MemberBegin(); itr != document.MemberEnd(); ++itr)
        spdlog::info("Type of member {} is {}", itr->name.GetString(), kTypeNames[itr->value.GetType()]);





    // Adding values to array.
    {
        Value& a = document["a"];   // This time we uses non-const reference.
        Document::AllocatorType& allocator = document.GetAllocator();
        for (int i = 5; i <= 10; i++)
            a.PushBack(i, allocator);   // May look a bit strange, allocator is needed for potentially realloc. We normally uses the document's.

        // Fluent API
        a.PushBack("Lua", allocator).PushBack("Mio", allocator);
    }

    // Making string values.

    // This version of SetString() just store the pointer to the string.
    // So it is for literal and string that exists within value's life-cycle.
    {
        document["hello"] = "rapidjson";    // This will invoke strlen()
        // Faster version:
        // document["hello"].SetString("rapidjson", 9);
    }

    // This version of SetString() needs an allocator, which means it will allocate a new buffer and copy the the string into the buffer.
    Value author;
    {
        char buffer2[10];
        int len = sprintf(buffer2, "%s %s", "Milo", "Yip");  // synthetic example of dynamically created string.

        author.SetString(buffer2, static_cast<SizeType>(len), document.GetAllocator());
        // Shorter but slower version:
        // document["hello"].SetString(buffer, document.GetAllocator());

        // Constructor version: 
        // Value author(buffer, len, document.GetAllocator());
        // Value author(buffer, document.GetAllocator());
        memset(buffer2, 0, sizeof(buffer2)); // For demonstration purpose.
    }
    // Variable 'buffer' is unusable now but 'author' has already made a copy.
    document.AddMember("author", author, document.GetAllocator());

    assert(author.IsNull());        // Move semantic for assignment. After this variable is assigned as a member, the variable becomes null.



 ////////////////////////////////////////////////////////////////////////////
    // 4. Stringify JSON

    printf("\nModified JSON with reformatting:\n");
    StringBuffer sb;
    PrettyWriter<StringBuffer> writer(sb);
    document.Accept(writer);    // Accept() traverses the DOM and generates Handler events.
    puts(sb.GetString());

}


// https://www.sojson.com/ : json online Perse
// https://blog.csdn.net/hjxu2016/article/details/119357278 : reader json from file exampel
// https://rapidjson.org/zh-cn/ : RapidJSON 文档
// https://github.com/Tencent/rapidjson : raped json github


void example4() {
    // std::ifstream file(std::move(std::string("/home/tmpDevDir/ecnu-tpf/cmake/my-examples/cmake-project-example/version0.1.1/config/config.json"))); // #include <fstream>
    std::ifstream file(std::move(std::string("./config/config.json"))); // #include <fstream>
    std::string strJson((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    rapidjson::Document json;
    json.Parse(strJson.c_str());

    spdlog::info("config content {}", strJson);

    if (json.HasParseError()) {
    	spdlog::error("Perse json failed");
    } else {
    	spdlog::info("Perse json successed");
    }

    assert(json["threadPool"]["threads"].GetInt() == 30);
    spdlog::info("threads : {}, i : {}, j : {}", json["threadPool"]["threads"].GetInt(), json["threadPool"]["i"].GetInt(), json["threadPool"]["j"].GetInt());
}

int main() {
    example1();
    // example2();
    // example3();
    // example4();
    return 0;
}