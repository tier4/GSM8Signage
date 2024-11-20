import QtQuick 2.9
import QtQuick.Controls 2.2

Rectangle {
    id: emergencyStopView
    width: viewController.monitor_width
    height: viewController.monitor_height
    color: "#ffffff"
    Text {
        id: emergencyStopText
        color: "#000000"
        text: qsTr("安全のため停止中")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.verticalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 80*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }

    Text {
        id: emergencyStopEnText
        color: "#000000"
        text: qsTr("Emergency Stop")
        anchors.top: emergencyStopText.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 36*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }
}
