import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 900
    height: 600
    title: "Sphere Trainer"

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        TabBar {
            id: tabBar
            Layout.fillWidth: true
            TabButton { text: "Main" }
            TabButton { text: "Render + Camera" }
        }

        StackLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            currentIndex: tabBar.currentIndex

            //main
            Item {
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 16



                    Item { Layout.fillHeight: true }
                }
            }

            //render
            Item {
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 0

                    Rectangle {
                        id: renderRect
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "black"

                        property int frameTag: 0

                        Image {
                            id: liveStream
                            anchors.fill: parent
                            fillMode: Image.PreserveAspectFit
                            source: "image://frameprovider/frame_" + renderRect.frameTag
                            cache: false
                        }

                        // FrameProvider::requestImage reads fresh mmap data
                        // every time the URL changes (frameTag increments).
                        Timer {
                            interval: 33
                            running: tabBar.currentIndex === 1
                            repeat: true
                            onTriggered: renderRect.frameTag++
                        }

                    }

                    // Controls toolbar
                    Rectangle {
                        Layout.fillWidth: true
                        height: 52
                        color: "#1e1e1e"

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 12

                            Button {
                                text: pythonCtrl.running ? "Stop Renderer" : "Start Renderer"
                                onClicked: {
                                            cameraLogic.toggle();
                                            (pythonCtrl.running) ? pythonCtrl.stopRenderer() : pythonCtrl.startRenderer()}

                            }

                            Item { Layout.fillWidth: true }
                        }
                    }
                }
            }
        }
    }
}
