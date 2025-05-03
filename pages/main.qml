import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import Qt.labs.platform 1.1 as Platform
import "./assets/"
import RinUI

FluentWindow {
    id: window
    visible: true
    title: qsTr("NamePicker")
    width: 900
    height: 700
    minimumWidth: 550
    minimumHeight: 400

    // 托盘图标 / Tray Icon //
    Platform.SystemTrayIcon {
        visible: Platform.SystemTrayIcon.isAvailable
        icon.source: "assets/favicon.ico"
        menu: Platform.Menu {
            Platform.MenuItem {
                text: qsTr("Quit")
                onTriggered: Qt.quit()
            }
        }
    }

    // 从 ItemData 获取控件数据
    function generateSubItems(type) {
        return ItemData.getItemsByType(type).map(item => ({
            title: item.title,
            page: item.page,
        }));
    }

    navigationItems: [
        {
            title: "随机抽选",
            page: Qt.resolvedUrl("pages/Choose.qml"),
            icon: "ic_fluent_home_20_regular",
        },
        {
            title: "设置",
            page: Qt.resolvedUrl("pages/Settings.qml"),
            icon: "ic_fluent_home_20_regular",
        },
        {
            title: "关于",
            page: Qt.resolvedUrl("pages/About.qml"),
            icon: "ic_fluent_home_20_regular",
        }
    ]
}