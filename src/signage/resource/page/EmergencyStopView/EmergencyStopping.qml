import QtQuick 2.9
import QtQuick.Controls 2.2

Rectangle {
    id: emergencyStoppingView
    width: viewController.monitor_width
    height: viewController.monitor_height
    color: "#ffffff"
    Text {
        id: emergencyStoppingText
        color: "#000000"
        text: qsTr("只今オペレータ対応中です")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.verticalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 80*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }

    Text {
        id: emergencyStoppingEnText
        color: "#000000"
        text: qsTr("Now the operator is working on it")
        anchors.top: emergencyStoppingText.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 36*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }
}
