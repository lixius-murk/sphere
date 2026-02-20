import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Window {
    visible: true
    width: 900
    height: 700
    title: "App"

    ColumnLayout {
        anchors.fill: parent

        TabBar {
            id: bar
            Layout.fillWidth: true

            TabButton { text: "Main" }
            TabButton { text: "Renderer" }
        }

        StackLayout {
            id: stack
            currentIndex: bar.currentIndex
            Layout.fillWidth: true
            Layout.fillHeight: true

            Rectangle {
                color: "black"
                Label {
                    anchors.centerIn: parent

                }
            }

            Item {
                id: renderTab

                Image {
                    id: video
                    anchors.fill: parent
                    cache: false
                    source: "image://frames/current"

                    Timer {
                        interval: 16
                        running: true
                        repeat: true
                        onTriggered: {
                            video.source = "image://frames/current?" + Math.random()
                        }
                    }
                }

            }
        }
    }

    onVisibleChanged: {
        if (visible)
            console.log("UI visible")
    }

    Connections {
        target: bar
        function onCurrentIndexChanged() {
            if (bar.currentIndex === 1) {
                console.log("Starting python renderer")
                PythonController.startRenderer()
            } else {
                console.log("Stopping python renderer")
                PythonController.stopRenderer()
            }
        }
    }
}


// Window {
//     visible: true
//     width: 900
//     height: 700
//     title: "App"


//     ColumnLayout {
//         anchors.fill: parent

//         TabBar {
//             id: bar
//             Layout.fillWidth: true

//             TabButton { text: "Main" }
//             TabButton { text: "Renderer" }
//         }

//         StackLayout {
//             currentIndex: bar.currentIndex
//             Layout.fillWidth: true
//             Layout.fillHeight: true

//             Rectangle { color: "black" }
//             Rectangle { color: "red" }
//         }
//     }
// }
