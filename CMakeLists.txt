cmake_minimum_required(VERSION 3.5)

project(amaconsole
  VERSION 1.0.2
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
option(GIT_SUBMODULE "Check submodules during build" ON)
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
find_package(Boost COMPONENTS python REQUIRED)

## enviroment INFO
message(DEBUG "PROJECT_VERSION: ${CMAKE_PROJECT_VERSION}")
message(DEBUG "CMAKE_BUILD_TYPE: ${CMAKE_BUILD_TYPE}")
message(DEBUG "CMAKE_BUILD_TESTS: ${CMAKE_BUILD_TESTS}")
message(DEBUG "GIT_SUBMODULE: ${GIT_SUBMODULE}")
message(DEBUG "INIT_HOME: ${INIT_HOME}")
message(DEBUG "CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message(DEBUG "CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
message(DEBUG "Python3_VERSION: ${Python3_VERSION}")
message(DEBUG "Python3_EXECUTABLE: ${Python3_EXECUTABLE}")

# Updating git submodules
find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
  # Update submodules as needed
  if(GIT_SUBMODULE)
    message(STATUS "Submodule update")
    execute_process(COMMAND ${GIT_EXECUTABLE} submodule update --init --recursive
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
      RESULT_VARIABLE GIT_SUBMOD_RESULT)
    if(NOT GIT_SUBMOD_RESULT EQUAL "0")
      message(FATAL_ERROR "git submodule update --init --recursive failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
    endif()
  endif()
endif()

# Python extensions (C/CXX) - name structure: ama_LIBNAME_ext.so

# # Add a shared module - modules are intended to be imported at runtime.
# # - This is where you add the source files
# ## HELLO_EXT
# add_library(hello_ext MODULE src/boost_python/hello_ext.cpp)

# # Set up the libraries and header search paths for this target
# target_link_libraries(hello_ext ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
# target_include_directories(hello_ext PRIVATE ${PYTHON_INCLUDE_DIRS})


# # echo
# add_library(echo_ext MODULE src/boost_python/utils/echo/echo_ext.cpp)

# # Set up the libraries and header search paths for this target
# target_link_libraries(echo_ext ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
# target_include_directories(echo_ext PRIVATE ${PYTHON_INCLUDE_DIRS})


## INSTALLATION

# Copy bin scripts to build directory
#file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/bin/amaconsole.py DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# python package (amaconsole)
set(PYTHON_PKG_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/amaconsole")
set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(INIT_PY_IN  "${PYTHON_PKG_SOURCE_DIR}/__init__.py.in")
set(INIT_PY     "${PYTHON_PKG_SOURCE_DIR}/__init__.py")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build")
set(TIMESTAMP   "${OUTPUT}/timestamp")

if(${CMAKE_BUILD_TYPE} STREQUAL "Debug")
  set(REQUIREMENTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements-dev.txt")
else()
  set(REQUIREMENTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")
endif()

message(DEBUG "PYTHON_PKG_SOURCE_DIR: ${PYTHON_PKG_SOURCE_DIR}")
message(DEBUG "Python requirements: ${REQUIREMENTS}")

configure_file(${SETUP_PY_IN} ${SETUP_PY})
configure_file(${INIT_PY_IN} ${INIT_PY})

add_custom_command(OUTPUT ${TIMESTAMP}
	COMMAND ${Python3_EXECUTABLE} ${SETUP_PY} build
	COMMAND ${CMAKE_COMMAND} -E touch ${TIMESTAMP})

add_custom_target(target ALL DEPENDS ${TIMESTAMP})
#install(CODE "message(INFO 'Installing python requirements')")
install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} -m pip install -r ${REQUIREMENTS})")
#install(CODE "message(INFO 'Installing python package (amaconsole - ${CMAKE_PROJECT_VERSION})')")
install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} ${SETUP_PY} install --verbose)")

# initialize amaconsole home directory
if(INIT_HOME)
  set(AMACONSOLE_HOME "$ENV{HOME}/.amaconsole")
  set(HOME_SCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/utils/home.py")
  # message(INFO "Initilizing amaconsole home")
  install(CODE "execute_process(COMMAND ${Python3_EXECUTABLE} ${HOME_SCRIPT} -b ${AMACONSOLE_HOME} -y)")
endif()

if(CMAKE_BUILD_TESTS)
  enable_testing()
  add_subdirectory(tests)
  add_custom_target(pytest
    COMMAND ${Python3_EXECUTABLE} -m pytest -v ${CMAKE_CURRENT_SOURCE_DIR}/tests)
endif()
add_subdirectory(libs)
