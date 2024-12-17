import QtQuick 2.9
import QtQuick.Controls 2.2

Rectangle {
    id: emergencyStopView
    width: viewController.monitor_width
    height: viewController.monitor_height
    color: "#ffff00"

    Rectangle {
        id: emergencyTextView
        width: viewController.monitor_width - 100
        height: viewController.monitor_height - 100
        color: "#ffffff"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        id: emergencyStopText
        color: "#000000"
        text: qsTr("急停止します")
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
        font.pointSize: 80*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }
}
