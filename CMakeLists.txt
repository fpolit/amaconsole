cmake_minimum_required(VERSION 3.5)

project(amaconsole
  VERSION 1.0.0
  DESCRIPTION "Console to interact with Ama-Framework"
  HOMEPAGE_URL https://github.com/fpolit/amaconsole
  LANGUAGES CXX Python
)

set (CMAKE_CXX_STANDARD 11)
set(PROJECT_LICENSE "GPLv3")
# Without this, any build libraries automatically have names "lib{x}.so"
set(CMAKE_SHARED_MODULE_PREFIX "")

# Finding dependencies
find_package(Python3  COMPONENTS Interpreter Development REQUIRED)
find_package(Boost COMPONENTS python REQUIRED)

# Updating git submodules
find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
  # Update submodules as needed
  option(GIT_SUBMODULE "Check submodules during build" ON)
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

# ama CXX extensions - name structure: ama_LIBNAME_ext.so

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
### python package (amaconsole)
set(PYTHON_PKG_SOURCE_DIR, "${CMAKE_CURRENT_SOURCE_DIR}/amaconsole")
set(PYTHON_PKG_BINARY_DIR, "${CMAKE_CURRENT_BINARY_DIR}/amaconsole")
set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(INIT_PY_IN  "${PYTHON_CURRENT_PKG_DIR}/__init__.py.in")
set(INIT_PY     "${PYTHON_PKG_BINARY_DIR}/__init__.py")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/")
set(TIMESTAMP   "${OUTPUT}/timestamp")
set(REQUIREMENTS "${CMAKE_CURRENT_SOURCE_DIR}/requirements.txt")

configure_file(${SETUP_PY_IN} ${SETUP_PY})
configure_file(${INIT_PY_IN} ${INIT_PY})

add_custom_command(OUTPUT ${TIMESTAMP}
	COMMAND python3 ${SETUP_PY} build
	COMMAND ${CMAKE_COMMAND} -E touch ${TIMESTAMP})

add_custom_target(target ALL DEPENDS ${TIMESTAMP})
message(DEBUG "Installing python requirements")
install(CODE "execute_process(COMMAND python3 -m pip install -r ${REQUIREMENTS})")
message(DEBUG "Installing python package (amaconsole)")
install(CODE "execute_process(COMMAND python3 ${SETUP_PY} install --verbose)")

# initialize amaconsole home directory
set(AMACONSOLE_HOME, "$ENV{HOME}/.amaconsole")
set(HOME_SCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/home.py")
message(DEBUG "Initilizing amaconsole home")
install(CODE "execute_process(COMMAND python3 ${HOME_SCRIPT} -b ${AMACONSOLE_HOME})")

### CXX extensions
message(DEBUG "Installing CXX extensions")
#install(TARGETS hello_ext echo_ext
#	LIBRARY DESTINATION lib)

include_directories(tests)
include_directories(libs)
