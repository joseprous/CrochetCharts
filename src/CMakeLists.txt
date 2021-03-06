include_directories(${QT_INCLUDES} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR})

file(GLOB crochet_srcs "*.cpp")
file(GLOB crochet_uis "*.ui")

set(crochet_resources
    ../crochet.qrc
    ../stitches/stitches.qrc
    )

qt5_add_resources(crochet_rcc_srcs ${crochet_resources})
qt5_wrap_ui(crochet_ui_h ${crochet_uis})

if(WIN32)
    #generate the embeded icon for the exe file.
    set(CMAKE_RC_COMPILER_INIT windres)
    enable_language(RC)
    set(CMAKE_RC_COMPILE_OBJECT "<CMAKE_RC_COMPILER> <FLAGS> -O coff <DEFINES> -i <SOURCE> -o <OBJECT>")
    set(crochet_win "${CMAKE_SOURCE_DIR}/crochet.rc")

    set(QT_WIN_LIBS "C://qt//4.8.5//bin")
    set(MINGW_LIBS "C://MinGW-4.4//bin")
    
    set(QT_LIBS_WINDOWS "${QT_WIN_LIBS}//QtSvg4.dll" "${QT_WIN_LIBS}//QtCore4.dll" "${QT_WIN_LIBS}//QtGui4.dll"
                        "${QT_WIN_LIBS}//QtNetwork4.dll" "${QT_WIN_LIBS}//QtXml4.dll")
    set(QT_DEPS_WINDOWS "${MINGW_LIBS}//libgcc_s_dw2-1.dll" "${MINGW_LIBS}//mingwm10.dll"
                        "${CMAKE_SOURCE_DIR}/resources/qt.conf")

    set(QT_PLUGINS_WINDOWS "${QT_PLUGINS_DIR}/imageformats" "${QT_PLUGINS_DIR}/accessible" "${QT_PLUGINS_DIR}/iconengines")

else()

    set(crochet_nix)

endif()

if(WIN32 AND CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_executable(${EXE_NAME} ${crochet_srcs} ${crochet_ui_h} ${crochet_rcc_srcs}
            ${crochet_version} ${crochet_win} ${crochet_mac} ${crochet_nix})
else()
    add_executable(${EXE_NAME} WIN32 MACOSX_BUNDLE ${crochet_srcs} ${crochet_ui_h} ${crochet_moc_srcs} ${crochet_rcc_srcs}
            ${crochet_version} ${crochet_win} ${crochet_mac} ${crochet_nix})
endif()

target_link_libraries(${EXE_NAME} ${Qt5Widgets_LIBRARIES} ${Qt5Gui_LIBRARIES} ${Qt5Network_LIBRARIES} ${Qt5OpenGL_LIBRARIES} ${Qt5Svg_LIBRARIES} ${Qt5PrintSupport_LIBRARIES})

if(APPLE)
    #install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME} DESTINATION ../MacOS)

    if(APP_STORE)
        set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_DEFINITIONS "APPLE_APP_STORE=1")
    endif()

    install(CODE "
        execute_process(
            COMMAND \"/usr/bin/macdeployqt\"
            \"@CMAKE_CURRENT_BINARY_DIR@/@PROJECT_NAME@.app/\"
            WORKING_DIRECTORY \"@CMAKE_BINARY_DIR@\"
            OUTPUT_VARIABLE _output)
        file(COPY \"@CMAKE_SOURCE_DIR@/images/@PROJECT_MACOSX_ICON@\"
            DESTINATION \"@CMAKE_CURRENT_BINARY_DIR@/@PROJECT_NAME@.app/Contents/Resources\") 
        file(COPY \"@CMAKE_CURRENT_BINARY_DIR@/@PROJECT_NAME@.app\" 
            DESTINATION \"@CMAKE_BINARY_DIR@/_CPack_Packages/Darwin/@CPACK_GENERATOR@/@PROJECT_NAME@-@VERSION_SHORT@\")
    " COMPONENT Runtime)

else()

    install(TARGETS ${EXE_NAME} BUNDLE DESTINATION . COMPONENT Runtime RUNTIME DESTINATION bin COMPONENT Runtime)
    if(WIN32)
        set_property(TARGET ${EXE_NAME} PROPERTY OUTPUT_NAME "${PROJECT_NAME}")
    endif()
endif()

if(WIN32)
    install(PROGRAMS ${QT_LIBS_WINDOWS} ${QT_DEPS_WINDOWS} DESTINATION bin)
    install(DIRECTORY ${QT_PLUGINS_WINDOWS} DESTINATION plugins)
endif()
