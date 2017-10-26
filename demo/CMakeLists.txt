cmake_minimum_required(VERSION 2.8)

include_directories(../include)
include_directories(../generated)

set( OPCUA_TOOLKIT_PATH /opt/OpcUaToolkit-1.3.3)

include_directories( ${OPCUA_TOOLKIT_PATH}/include/uastack )
include_directories( ${OPCUA_TOOLKIT_PATH}/include/uabase )
include_directories( ${OPCUA_TOOLKIT_PATH}/include )

add_executable(demo 
        demo.cpp 
        ../src/ClientSessionFactory.cpp 
        ../generated/HilariousClass.cpp
        )

target_link_libraries(demo 
        ${OPCUA_TOOLKIT_PATH}/lib/libuaclient.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuabase.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuapki.a
        ${OPCUA_TOOLKIT_PATH}/lib/libuastack.so
        -lpthread
        -lcrypto
        )