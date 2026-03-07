file(REMOVE_RECURSE
  "../../../../../qml/QtQuick/Studio/Utils/ChildListModel.qml"
  "../../../../../qml/QtQuick/Studio/Utils/JsonBackend.qml"
  "../../../../../qml/QtQuick/Studio/Utils/JsonListModel.qml"
)

# Per-language clean rules from dependency scanning.
foreach(lang )
  include(CMakeFiles/QuickStudioUtils_tooling.dir/cmake_clean_${lang}.cmake OPTIONAL)
endforeach()
