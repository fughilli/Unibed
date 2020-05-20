import lib.build as build

build_opts = {
    build_type : 'c++',
    
    cc : 'arm-none-eabi-gcc',
    cxx : 'arm-none-eabi-g++',
    ld : 'arm-none-eabi-gcc',
    
    ccflags : ['-Wall'],
    cxxflags : [],
    ldflags : []
}
