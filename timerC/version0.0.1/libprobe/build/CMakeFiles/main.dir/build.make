# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/build

# Include any dependencies generated for this target.
include CMakeFiles/main.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/main.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/main.dir/flags.make

CMakeFiles/main.dir/testSrcs/test.c.o: CMakeFiles/main.dir/flags.make
CMakeFiles/main.dir/testSrcs/test.c.o: ../testSrcs/test.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/main.dir/testSrcs/test.c.o"
	/usr/bin//mpicc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/main.dir/testSrcs/test.c.o   -c /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/testSrcs/test.c

CMakeFiles/main.dir/testSrcs/test.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/main.dir/testSrcs/test.c.i"
	/usr/bin//mpicc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/testSrcs/test.c > CMakeFiles/main.dir/testSrcs/test.c.i

CMakeFiles/main.dir/testSrcs/test.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/main.dir/testSrcs/test.c.s"
	/usr/bin//mpicc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/testSrcs/test.c -o CMakeFiles/main.dir/testSrcs/test.c.s

# Object files for target main
main_OBJECTS = \
"CMakeFiles/main.dir/testSrcs/test.c.o"

# External object files for target main
main_EXTERNAL_OBJECTS =

main: CMakeFiles/main.dir/testSrcs/test.c.o
main: CMakeFiles/main.dir/build.make
main: src/libinstruProbe.a
main: CMakeFiles/main.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable main"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/main.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/main.dir/build: main

.PHONY : CMakeFiles/main.dir/build

CMakeFiles/main.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/main.dir/cmake_clean.cmake
.PHONY : CMakeFiles/main.dir/clean

CMakeFiles/main.dir/depend:
	cd /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/build /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/build /home/maple/myplace/github/ecnu-tpf/timerC/version0.0.1/libprobe/build/CMakeFiles/main.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/main.dir/depend

