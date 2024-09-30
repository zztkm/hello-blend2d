cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(app C CXX)

# Some basics, set accordingly to your needs.
set(CMAKE_CXX_STANDARD 11)

# Where the 'app' and 'blend2d' are.
set(APP_DIR "${CMAKE_CURRENT_LIST_DIR}"
    CACHE PATH "Application directory")

set(BLEND2D_DIR "${APP_DIR}/../blend2d"
    CACHE PATH "Location of 'blend2d'")

# Enable Blend2D static build.
set(BLEND2D_STATIC TRUE)
include("${BLEND2D_DIR}/CMakeLists.txt")

# Your application target.
add_executable(app app.cpp)

# Add Blend2D dependency to your application. The dependency
# should provide everything needed - include paths, libraries,
# compiler flags, and compiler definitions.
target_link_libraries(app blend2d::blend2d)
