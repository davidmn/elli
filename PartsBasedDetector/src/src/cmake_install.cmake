# Install script for directory: /home/megaslippers/elli/PartsBasedDetector/src

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/local")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  IF(EXISTS "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so")
    FILE(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so"
         RPATH "")
  ENDIF()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so")
  IF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
  IF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
FILE(INSTALL DESTINATION "/home/megaslippers/elli/PartsBasedDetector/lib" TYPE SHARED_LIBRARY FILES "/home/megaslippers/elli/PartsBasedDetector/src/src/libPartsBasedDetector.so")
  IF(EXISTS "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so")
    FILE(RPATH_REMOVE
         FILE "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so")
    IF(CMAKE_INSTALL_DO_STRIP)
      EXECUTE_PROCESS(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/lib/libPartsBasedDetector.so")
    ENDIF(CMAKE_INSTALL_DO_STRIP)
  ENDIF()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  IF(EXISTS "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector")
    FILE(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector"
         RPATH "")
  ENDIF()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector")
  IF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
  IF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
FILE(INSTALL DESTINATION "/home/megaslippers/elli/PartsBasedDetector/bin" TYPE EXECUTABLE FILES "/home/megaslippers/elli/PartsBasedDetector/src/src/PartsBasedDetector")
  IF(EXISTS "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector")
    FILE(RPATH_REMOVE
         FILE "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector")
    IF(CMAKE_INSTALL_DO_STRIP)
      EXECUTE_PROCESS(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/megaslippers/elli/PartsBasedDetector/bin/PartsBasedDetector")
    ENDIF(CMAKE_INSTALL_DO_STRIP)
  ENDIF()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

