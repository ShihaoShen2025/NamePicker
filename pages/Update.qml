import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI

FluentPage{
    id: updp
    property string ver:""
    Column{
        width: parent.width
        spacing: 10
        RowLayout{
            Image{
                id: sticker
                source: "../assets/Firefly-well.png"
            }
            Column{
                spacing:20
                Text{
                    id: upTitle
                    typography: Typography.Title
                    text: qsTr("尚未检查更新...")
                }
                Text{
                    id: upSubtitle
                    typography: Typography.Subtitle
                    text: qsTr("点击下方按钮一键检查更新")
                }
            }
        }
        RowLayout{
            Button{
                text: qsTr("检查更新")
                highlighted: true
                onClicked:{
                    Bridge.checkNew()
                }
            }
            Button{
                id: dwnBtn
                text: qsTr("下载并安装")
                enabled: false
                onClicked:{
                    Bridge.update()
                }
            }
        }
        ProgressBar{
            id: progress
            from: 0
            to: 100
            width: parent.width
            value:0
        }
        Text{
            typography: Typography.BodyStrong
            text: qsTr("高级设置")
        }
        SettingCard {
            width: parent.width
            title: qsTr("更新频道")
            description: qsTr("选择更新频道")
            icon: "ic_fluent_branch_20_regular"
            content: ComboBox {
                property var data: ["rel","dev"]
                model: ["稳定版","开发版"]
                currentIndex: Bridge.getChannel()
                onCurrentIndexChanged: {
                    Bridge.SetCfg("Version","channel",[data[currentIndex]])
                }
            }
        }
        SettingCard{
            width: parent.width
            icon: "ic_fluent_arrow_sync_circle_20_regular"
            title: qsTr("强制更新（仅供测试，没事别乱用）")
            description: qsTr("无论当前版本是否高于当前频道最新版，都允许更新")
            content:Switch{
                checked: Bridge.getForce()
                onClicked: Bridge.setForce(checked)
            }
        }
    }
    Connections {
        target: Bridge // 绑定python的类
        ignoreUnknownSignals: true // 取消警告
        function onChgVer(name) { // 使用 on + 信号名(首字母大写) 作为信号的槽
            console.log(name)
            updp.ver = name
            if(updp.ver!="latest"){
                dwnBtn.enabled = true
                upTitle.text = qsTr("发现新版本！")
                upSubtitle.text = name
                sticker.source = "../assets/Sam-go.png"
                dwnBtn.enabled = true
            }
            else{
                upTitle.text = qsTr("无需更新")
                upSubtitle.text = qsTr("已经是最新版本了")
                sticker.source = "../assets/Firefly-heart.png"
                dwnBtn.enabled = false
            }
        }
        function onChgProg(prog){
            progress.value = prog
        }
        function onChgPhase(prog){
            if(prog=="get"){
                upSubtitle.text = qsTr("获取下载链接")
            }
            else if(prog=="down"){
                upSubtitle.text = qsTr("下载中")
            }
            else if(prog=="extract"){
                upSubtitle.text = qsTr("解压中")
            }
            else if(prog=="complete"){
                upSubtitle.text = qsTr("完成！")
            }
            else if(prog=="error"){
                upSubtitle.text = qsTr("发生错误！查看日志获取详情")
                sticker.source = "../assets/Firefly-no.png"
            }
        }
    }
}