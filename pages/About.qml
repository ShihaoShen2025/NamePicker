import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI

FluentPage {
    title: "关于NamePicker"

    contentHeader: Item {
        width: parent.width
        height: Math.max(window.height * 0.35, 200)

        Image {
            id: banner
            anchors.fill: parent
            source: "../assets/banner.png"
            fillMode: Image.PreserveAspectCrop
            verticalAlignment: Image.AlignTop

            layer.enabled: true
            layer.effect: OpacityMask {
                maskSource: Rectangle {
                    width: banner.width
                    height: banner.height
                    gradient: Gradient {
                        GradientStop { position: 0.7; color: "white" }
                        GradientStop { position: 1.0; color: "transparent" }
                    }
                }
            }
        }
    }

    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: "Appearances"
        }

        SettingCard {
            width: parent.width
            title: qsTr("App Theme")
            description: qsTr("Select which app theme to display")
            icon: "ic_fluent_paint_brush_20_regular"

            content: ComboBox {
                property var data: ["Light", "Dark", "Auto"]
                model: ["Light", "Dark", "Use system setting"]
                currentIndex: data.indexOf(Theme.getTheme())
                onCurrentIndexChanged: {
                    Theme.setTheme(data[currentIndex])
                }
            }
        }

        SettingCard {
            width: parent.width
            title: qsTr("Window Backdrop Effect")
            description: qsTr("Adjust the appearance of the window background (Only available on Windows platform, some styles may only support on Windows 11)")
            icon: "ic_fluent_square_hint_sparkles_20_regular"

            content: ComboBox {
                property var data: ["mica", "acrylic", "tabbed", "none"]
                model: ["Mica", "Acrylic", "Tabbed", "None"]
                currentIndex: data.indexOf(Theme.getBackdropEffect())
                onCurrentIndexChanged: {
                    Theme.setBackdropEffect(data[currentIndex])
                }
            }
        }
    }


    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: "About"
        }

        SettingCard {
            width: parent.width
            title: qsTr("RinUI Gallery")
            description: qsTr("© 2025 RinLit. All rights reserved.")
            source: Qt.resolvedUrl("../assets/BA_Pic_Shiroko-chibi.png")
            iconSize: 28

            content: Text {
                color: Theme.currentTheme.colors.textSecondaryColor
                text: "0.0.8"
            }
        }
    }
}