#include<processId/process_id.h>
#include<perf/perf_counter.h>

#include <gtest/gtest.h>
#include <sstream>
#include <iostream>
#include <string>

class QuickTest : public testing::Test {
protected:
  // Remember that SetUp() is run immediately before a test starts.
  // This is a good place to record the start time.
    void SetUp() override { 
        start_time_ = time(nullptr);
        std::cout << "I am SetUp()" << std::endl;
    }

  // TearDown() is invoked immediately after a test finishes.  Here we
  // check if the test was too slow.
  void TearDown() override {
    std::cout << "I am TearDown()" << std::endl;

    // Gets the time when the test finishes
    const time_t end_time = time(nullptr);

    // Asserts that the test took no more than ~5 seconds.  Did you
    // know that you can use assertions in SetUp() and TearDown() as
    // well?
    EXPECT_TRUE(end_time - start_time_ <= 5) << "The test took too long.";
  }

  // The UTC time (in seconds) when the test starts
  time_t start_time_;
};


TEST(QuickTest, PrintsMessage) {
    printf("Printing something from the test body...\n");
}

TEST(QuickTest, printProcessId) {
    printf("ThreadId : %s\n", processId::ProcessId::getThreadId().c_str());
    printf("pid : %s\n", processId::ProcessId::getProcessPid().c_str());
    printf("ppid : %s\n", processId::ProcessId::getProcessPpid().c_str());
}

TEST(QuickTest, printTsc) {
    std::stringstream ss;
    ss << myPerf::Perf::getTsc();
    std::cout << ss.str() << std::endl;
}


TEST(QuickTest, printTscCpuHz) {
    std::cout << myPerf::Perf::getConstCpuHz();
    std::cout << myPerf::Perf::getConstCpuHz();
    std::cout << myPerf::Perf::getConstCpuHz();
    std::cout << myPerf::Perf::getConstCpuHz();
    std::cout << myPerf::Perf::getConstCpuHz();
}
