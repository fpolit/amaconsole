cmake_minimum_required(VERSION 3.5)

project(amaconsole
  VERSION 1.0.3
  DESCRIPTION "Console to interact with Ama-Framework"
  HOMEPAGE_URL https://github.com/fpolit/amaconsole
)

set (CMAKE_CXX_STANDARD 11)
set(PROJECT_LICENSE "GPLv3")
# Without this, any build libraries automatically have names "lib{x}.so"
set(CMAKE_SHARED_MODULE_PREFIX "")

# options
option(CMAKE_COMPILER_WALL "Warning all" ON)
option(CMAKE_BUILD_TESTS  "Build unittest" OFF)
option(INIT_HOME "Initialize amaconsole home directory" ON)

if(${CMAKE_COMPILER_WALL})
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")
endif()

if(${CMAKE_BUILD_TYPE} STREQUAL "Debug")
  message(DEBUG "Adding -ggdb compiler flag")
  set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -ggdb" CACHE STRING "gdb debug support" FORCE)
endif()


# Finding dependencies
find_package(Python3  COMPONENTS Interpreter Development REQUIRED)

## enviroment INFO
message(DEBUG "PROJECT_VERSION: ${CMAKE_PROJECT_VERSION}")
message(DEBUG "PROJECT_AMAPROTO_VERSION: ${CMAKE_PROJECT_AMAPROTO_VERSION}")
message(DEBUG "PROJECT_AMACORE_VERSION: ${CMAKE_PROJECT_AMACORE_VERSION}")
message(DEBUG "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
message(DEBUG "CMAKE_BUILD_TESTS: ${CMAKE_BUILD_TESTS}")
message(DEBUG "GIT_UPDATE_SUBMODULES: ${GIT_UPDATE_SUBMODULES}")
message(DEBUG "INIT_HOME: ${INIT_HOME}")
message(DEBUG "CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message(DEBUG "CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
message(DEBUG "Python3_VERSION: ${Python3_VERSION}")
message(DEBUG "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")

# Updating git submodules
find_package(Git)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
    # Update submodules as needed
    option(GIT_UPDATE_SUBMODULES "Check submodules during build" ON)
    if(GIT_UPDATE_SUBMODULES)
      message(DEBUG "GIT_EXECUTABLE: ${GIT_EXECUTABLE}")
      execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      RESULT_VARIABLE GIT_SUBMOD_RESULT)
    if(NOT GIT_SUBMOD_RESULT EQUAL "0")
      message(FATAL_ERROR "git submodule update --init failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
    endif()
  endif()
endif()

# amaconsole protbuf files generation
set(CMAKE_PROJECT_AMAPROTO_VERSION "None")
set(CMAKE_BUILD_AMACONTROLLER_PY_PROTO ON CACHE BOOL "Build amacontroller python protobuf files")
set(CMAKE_BUILD_AMADB_PY_PROTO ON CACHE BOOL "Build amadb python protobuf files")
add_subdirectory(proto) # generate amacontroller_protos and amadb_protos targets

# python package (amaconsole)
set(PYTHON_PKG_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/amaconsole")
set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(INIT_PY_IN  "${PYTHON_PKG_SOURCE_DIR}/__init__.py.in")
set(INIT_PY     "${PYTHON_PKG_SOURCE_DIR}/__init__.py")

if(${CMAKE_BUILD_TYPE} STREQUAL "Debug")
  set(REQUIREMENTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements-dev.txt")
else()
  set(REQUIREMENTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")
endif()

message(DEBUG "PYTHON_PKG_SOURCE_DIR: ${PYTHON_PKG_SOURCE_DIR}")
message(DEBUG "Python requirements: ${REQUIREMENTS}")

configure_file(${SETUP_PY_IN} ${SETUP_PY})
configure_file(${INIT_PY_IN} ${INIT_PY})

add_custom_target(pybuild_amaconsole ALL
  DEPENDS amacontroller_protos amadb_protos)

add_custom_command(TARGET pybuild_amaconsole
	COMMAND ${Python3_EXECUTABLE} ${SETUP_PY} build)

install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} -m pip install -r ${REQUIREMENTS})")
install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} ${SETUP_PY} install --verbose)")

# initialize amaconsole home directory
if(INIT_HOME)
  set(AMACONSOLE_HOME "$ENV{HOME}/.amaconsole") # default amaconsole home directory
  set(HOME_SCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/utils/home.py")
  install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} ${HOME_SCRIPT} -b ${AMACONSOLE_HOME} -y)")

  set(EXTENSIONS_REQUIREMENTS "${AMACONSOLE_HOME}/extensions/requirements.txt")
  install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} -m pip install -r ${EXTENSIONS_REQUIREMENTS})")
endif()

if(CMAKE_BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
#   if(TARGET pytest)
#     add_custom_command(TARGET pytest
#       COMMAND ${Python3_EXECUTABLE} -m pytest -v ${CMAKE_CURRENT_SOURCE_DIR}/tests)
#   else()
#     add_custom_target(pytest
#       COMMAND ${Python3_EXECUTABLE} -m pytest -v ${CMAKE_CURRENT_SOURCE_DIR}/tests)
#   endif()
endif()

add_subdirectory(libs) # install amacore python package (it contains plugins to create commmands for console)
