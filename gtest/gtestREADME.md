### 配置GTEST环境

* download     googletest-release-1.12.1.tar.gz

```bash
tar -zxvf googletest-release-1.12.1.tar.gz
cmake -B build
cmake --build build -v
sudo make install
```

[GoogleTest User’s Guide | GoogleTest](https://google.github.io/googletest/)



## Welcome to GoogleTest!

GoogleTest is Google’s C++ testing and mocking framework. This user’s guide has the following contents:

* [GoogleTest Primer](https://google.github.io/googletest/primer.html) - Teaches you how to write simple tests using GoogleTest. Read this first if you are new to GoogleTest.
* [GoogleTest Advanced](https://google.github.io/googletest/advanced.html) - Read this when you’ve finished the Primer and want to utilize GoogleTest to its full potential.
* [GoogleTest Samples](https://google.github.io/googletest/samples.html) - Describes some GoogleTest samples.
* [GoogleTest FAQ](https://google.github.io/googletest/faq.html) - Have a question? Want some tips? Check here first.
* [Mocking for Dummies](https://google.github.io/googletest/gmock_for_dummies.html) - Teaches you how to create mock objects and use them in tests.
* [Mocking Cookbook](https://google.github.io/googletest/gmock_cook_book.html) - Includes tips and approaches to common mocking use cases.
* [Mocking Cheat Sheet](https://google.github.io/googletest/gmock_cheat_sheet.html) - A handy reference for matchers, actions, invariants, and more.
* [Mocking FAQ](https://google.github.io/googletest/gmock_faq.html) - Contains answers to some mocking-specific questions.
