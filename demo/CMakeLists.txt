cmake_minimum_required(VERSION 2.8)

include_directories(../supplementary_include)
include_directories(../generated)

set( OPCUA_TOOLKIT_PATH /opt/OpcUaToolkit-1.6.5)

include_directories( ${OPCUA_TOOLKIT_PATH}/include/uastack )
include_directories( ${OPCUA_TOOLKIT_PATH}/include/uabasecpp )
include_directories( ${OPCUA_TOOLKIT_PATH}/include )

file(GLOB GENERATED_SRCS ../generated/*.cpp)
file(GLOB SUPPLEMENTARY_SRCS ../supplementary_src/*.cpp)

add_executable(demo 
        demo.cpp 
        ${SUPPLEMENTARY_SRCS}
        ${GENERATED_SRCS}
        )

target_link_libraries(demo 
        ${OPCUA_TOOLKIT_PATH}/lib/libuaclientcpp.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuabasecpp.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuapkicpp.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuastack.so
	${OPCUA_TOOLKIT_PATH}/lib/libxmlparsercpp.a

        -lxml2
        -lpthread
        -lcrypto
        )
