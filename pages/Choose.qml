import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import RinUI

FluentPage {
    RowLayout{
        width: parent.width
        ListView{
            id: nameList
            textRole: "name"
        }
        Text{
            typography:Typography.Title
            text:qsTr("qwertyuiop")
        }
    }
}