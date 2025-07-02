import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI
import Qt5Compat.GraphicalEffects

FluentPage {
    horizontalPadding: 0
    wrapperWidth: width - 42*2

    contentHeader: Item {
        width: parent.width
        height: Math.max(window.height * 0.4, 200)

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
        Text{
            typography: Typography.Title
            text: "关于NamePicker"
        }

        SettingCard {
            width: parent.width
            title: qsTr(Bridge.VerTxt)
            description: qsTr("『八面玲珑的狐人少女，样貌、名字、身份皆被人夺去。命运为她留下一线生机，而「毁灭」的烙印仍在蠢蠢欲动。』")
            icon: "ic_fluent_info_sparkle_20_regular"
        }
        SettingCard {
            width: parent.width
            title: qsTr("作者")
            description: qsTr("by 灵魂歌手er（GitHub @LHGS-github）")
            icon: "ic_fluent_people_20_regular"
        }
        SettingCard {
            width: parent.width
            title: qsTr("版权相关")
            description: qsTr("基于GNU GPLv3获得授权")
            icon: "ic_fluent_document_20_regular"
        }
    }
    Column{
        Layout.fillWidth: true
        spacing: 3  
        Text{
            typography: Typography.Subtitle
            text: "相关链接"
        }
        SettingCard {
            width: parent.width
            title: qsTr("官方文档")
            description: qsTr("点击查看官方文档")
            icon: "ic_fluent_document_20_regular"
            content: Hyperlink {
                text: qsTr("点击跳转")
                openUrl: "https://namepicker-docs.netlify.app"
                enabled: true
            }
        }
        SettingCard {
            width: parent.width
            title: qsTr("GitHub仓库")
            description: qsTr("觉得满意的话欢迎Star")
            icon: "ic_fluent_box_20_regular"
            content: Hyperlink {
                text: qsTr("点击跳转")
                openUrl: "https://github.com/NamePickerOrg/NamePicker"
                enabled: true
            }
        }
    }
}