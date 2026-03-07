file(REMOVE_RECURSE
  "../../qml/eye_gymnastics/Constants.qml"
  "../../qml/eye_gymnastics/DirectoryFontLoader.qml"
  "../../qml/eye_gymnastics/EventListModel.qml"
  "../../qml/eye_gymnastics/EventListSimulator.qml"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/eye_gymnastics_tooling.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
