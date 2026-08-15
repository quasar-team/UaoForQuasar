cmake_minimum_required(VERSION 3.16)
project(UaoDemo LANGUAGES C CXX)

if(NOT DEFINED QUASAR_ROOT)
  get_filename_component(QUASAR_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../.." ABSOLUTE)
endif()

if(NOT EXISTS "${QUASAR_ROOT}/cmake/FindOpcUaToolkit.cmake")
  message(FATAL_ERROR
    "No FindOpcUaToolkit.cmake under ${QUASAR_ROOT}/cmake. "
    "Deploy UaoForQuasar inside a quasar project whose FindOpcUaToolkit.cmake "
    "provides the Client component, or point -DQUASAR_ROOT at one.")
endif()

list(APPEND CMAKE_MODULE_PATH "${QUASAR_ROOT}/cmake")

find_package(OpcUaToolkit REQUIRED COMPONENTS Client)

file(GLOB UAO_GENERATED_SRCS "${CMAKE_CURRENT_SOURCE_DIR}/../generated/*.cpp")

set(UAO_SUPPLEMENTARY_SRCS
  "${CMAKE_CURRENT_SOURCE_DIR}/../supplementary_src/ClientSessionFactory.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/../supplementary_src/UaoExceptions.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/../supplementary_src/ArrayTools.cpp"
  "${CMAKE_CURRENT_SOURCE_DIR}/../supplementary_src/CalculatedVariable.cpp")

set(UAO_LOGIT_SRCS
  "${QUASAR_ROOT}/LogIt/src/LogIt.cpp"
  "${QUASAR_ROOT}/LogIt/src/LogItInstance.cpp"
  "${QUASAR_ROOT}/LogIt/src/LogLevels.cpp"
  "${QUASAR_ROOT}/LogIt/src/LogRecord.cpp"
  "${QUASAR_ROOT}/LogIt/src/LogSinks.cpp"
  "${QUASAR_ROOT}/LogIt/src/ComponentAttributes.cpp"
  "${QUASAR_ROOT}/LogIt/src/StdOutLog.cpp")

add_executable(demo
  demo.cpp
  ${UAO_SUPPLEMENTARY_SRCS}
  ${UAO_GENERATED_SRCS}
  ${UAO_LOGIT_SRCS})

target_include_directories(demo PRIVATE
  "${CMAKE_CURRENT_SOURCE_DIR}/../supplementary_include"
  "${CMAKE_CURRENT_SOURCE_DIR}/../generated"
  "${QUASAR_ROOT}/LogIt/include")

target_compile_definitions(demo PRIVATE LOGIT_BACKEND_STDOUTLOG)

target_link_libraries(demo PRIVATE OpcUaToolkit::Client)
