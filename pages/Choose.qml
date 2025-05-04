import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI

FluentPage {
    width: parent.width
    Column{
        Layout.fillWidth: true
        Layout.alignment: parent.left
        width: parent.width
        spacing: 10
        ListView{
            id: nameList
            textRole: "name"
            width: parent.width
            height: 370
            model:ListModel {
                id: studentsModel
                ListElement { name: qsTr("example")}
            }
        }
        Button{
            width: parent.width
            highlighted: true
            text: qsTr("点击抽选")
            onClicked: {
                var pk = Bridge.Pick(chooseNum.text,sexCombo.currentText,numCombo.currentText)
                if(pk[0]!="bydcnm"){
                    studentsModel.clear()
                    for(var i = 0; i < pk.length; i++){
                        studentsModel.append({name: pk[i]})
                    }
                }
                else{
                    floatLayer.createInfoBar({
                        severity: Severity.Error,
                        title: qsTr("Error"),
                        text: qsTr(pk[1])
                    })
                }
            }
        }
        RowLayout{
            Layout.fillWidth: true
            Layout.alignment: parent.left
            width: parent.width
            Text{
                typography:Typography.Body
                text: qsTr("抽选数量")
            }
            TextField {
                id: chooseNum
                width: parent.width
                Layout.alignment: Qt.AlignRight
                placeholderText: qsTr("输入抽选数量")
                validator: IntValidator
            }
        }
        RowLayout{
            Layout.fillWidth: true
            width: parent.width
            Text{
                typography:Typography.Body
                text: qsTr("选择性别偏好")
            }
            ComboBox {
                id: sexCombo
                Layout.alignment: Qt.AlignRight
                model: ["都抽", "只抽男", "只抽女", "只抽特殊性别"]
                currentIndex: 0
                placeholderText: qsTr("选择性别偏好")
            }
        }
        RowLayout{
            Layout.fillWidth: true
            Layout.alignment: parent.left
            width: parent.width
            Text{
                typography:Typography.Body
                text: qsTr("选择学号偏好")
            }
            ComboBox {
                id: numCombo
                Layout.alignment: Qt.AlignRight
                model: ["都抽", "只抽单数", "只抽双数"]
                currentIndex: 0
                placeholderText: qsTr("选择学号偏好")
            }
        }
    }
}