import lib.build as build
import os

include_dirs += node.makeAbsPaths(['.', 'drivers', 'utils', 'registers',
                                   'driverlib', 'inc'])

# Select files to add to the build pool
files = []
files_regex = '^.*\\.(c|h|cpp)$'

# Define build tools
cc = "arm-none-eabi-gcc"
cxx = "arm-none-eabi-g++"
ld = "arm-none-eabi-gcc"
objcopy = "arm-none-eabi-objcopy"

# Define build flags
include_flags = ["-I %s" % x for x in include_dirs]
common_flags = ["-O3", "-ffunction-sections", "-fdata-sections", "-g",
                "-mthumb", "-mcpu=cortex-m4", "-mfloat-abi=hard",
                "-mfpu=fpv4-sp-d16", "-fsingle-precision-constant"]
ccflags = ["-Wall","-std=c99"] + common_flags + include_flags
cxxflags = (["-Wall","-std=c++14", "-fno-exceptions", "-fno-rtti"] +
            common_flags + include_flags)
ldflags = (["-Wl,--gc-sections", "--specs=nano.specs", "-T " +
           node.makeAbsPath("tm4c123gh6pm.ld"), "-Wl,--entry=ResetISR", "-lm",
           "-lstdc++"] + common_flags)

# define build steps (use built-in C/C++ build steps)
build_steps = [(['r*', '^(.*\\.)c$'], ['r*', '\\1o'], build.csrc_to_obj),
               (['r*', '^(.*\\.)cpp$'], ['r*', '\\1o'], build.cppsrc_to_obj),
               (['r*', '.*\\.o'], ['a', 'main.elf'], build.obj_to_bin),
               (['a', 'main.elf'], ['a', 'main.bin'], build.elf_to_bin)]
