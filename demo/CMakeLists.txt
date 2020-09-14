cmake_minimum_required(VERSION 2.8)

include_directories(../supplementary_include)
include_directories(../generated)

set( OPCUA_TOOLKIT_PATH /opt/OpcUaToolkit-eval-1.5.5)

include_directories( ${OPCUA_TOOLKIT_PATH}/include/uastack )
include_directories( ${OPCUA_TOOLKIT_PATH}/include/uabase )
include_directories( ${OPCUA_TOOLKIT_PATH}/include )

file(GLOB GENERATED_SRCS ../generated/*.cpp)

add_executable(demo 
        demo.cpp 
        ../supplementary_src/ClientSessionFactory.cpp 
        ${GENERATED_SRCS}
        )

target_link_libraries(demo 
        ${OPCUA_TOOLKIT_PATH}/lib/libuaclient.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuabase.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuapki.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuastack.so
	${OPCUA_TOOLKIT_PATH}/lib/libxmlparser.a
	
        -lxml2	
        -lpthread
        -lcrypto
        )