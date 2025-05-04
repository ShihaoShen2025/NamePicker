import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI

FluentPage {
    title: "Settings"
    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: "常规"
        }
        SettingCard {
            width: parent.width
            title: qsTr("允许重复点名")
            description: qsTr("是否允许抽到重复的名字")
            icon: "ic_fluent_arrow_repeat_all_20_regular"
            content: Switch{
                id: arpSwitch
                checked: Bridge.GetCfg("General","allowRepeat")[0]
                onClicked: Bridge.SetCfg("General","allowRepeat",[arpSwitch.checked])
            }
        }
        SettingCard {
            width: parent.width
            title: qsTr("开机自启")
            description: qsTr("目前没有浮窗功能，所以这个设置项只是拿来占位的")
            icon: "ic_fluent_bin_recycle_20_regular"
        }
        SettingCard {
            width: parent.width
            title: qsTr("抽选快捷键")
            description: qsTr("同理，也是拿来占位的")
            icon: "ic_fluent_bin_recycle_20_regular"
        }
        SettingCard {
            width: parent.width
            title: qsTr("课表软件联动")
            description: qsTr("启用后将在ClassIsland/Class Widgets上（而非主界面）显示抽选结果，需要安装对应插件")
            icon: "ic_fluent_arrow_repeat_all_20_regular"
            content: Switch{
                id: scsSwitch
                checked: Bridge.GetCfg("General","supportCS")[0]
                onClicked: Bridge.SetCfg("General","supportCS",[scsSwitch.checked])
            }
        }
    }

    Column {
        Layout.fillWidth: true
        spacing: 3
        Text {
            typography: Typography.BodyStrong
            text: "外观"
        }
        SettingCard {
            width: parent.width
            title: qsTr("明暗主题")
            description: qsTr("选择界面主题")
            icon: "ic_fluent_paint_brush_20_regular"
            content: ComboBox {
                property var data: ["Light", "Dark", "Auto"]
                model: ["亮色", "暗色", "跟随系统设定"]
                currentIndex: data.indexOf(Theme.getTheme())
                onCurrentIndexChanged: {
                    Theme.setTheme(data[currentIndex])
                }
            }
        }
        SettingCard {
            width: parent.width
            title: qsTr("窗口特效")
            description: qsTr("调整窗口背景的效果，仅在Windows上工作，部分特效仅在Windows 11上工作")
            icon: "ic_fluent_rectangle_landscape_sparkle_20_regular"
            content: ComboBox {
                property var data: ["mica", "acrylic", "tabbed", "none"]
                model: ["Mica", "亚克力", "Tabbed", "无"]
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
            text: "调试（不要乱动，除非您知道您在干什么）"
        }
        SettingCard {
            width: parent.width
            title: qsTr("日志等级")
            description: qsTr("日志的详细程度，重启生效")
            icon: "ic_fluent_document_20_regular"
            content: ComboBox {
                model: ["DEBUG","INFO","WARNING","ERROR"]
                currentIndex: Bridge.GetDbg(1)[0]
                onCurrentIndexChanged: {
                    Bridge.SetCfg("Debug","logLevel",[data[currentIndex]])
                }
            }
        }
    }
}