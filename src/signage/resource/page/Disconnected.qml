import QtQuick 2.9
import QtQuick.Controls 2.2

import "Common"

Rectangle {
    id: disconnectedView
    width: viewController.monitor_width
    height: viewController.monitor_height
    color: "#ffffff"

    CurrentTime {
        id: displayCurrentTime
    }

    Text {
        id: disconnectedText
        color: "#ef642c"
        text: qsTr("自動運転システムとの通信が遅延しています")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.verticalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 40*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }

    Text {
        id: disconnectedEnText
        color: "#ef642c"
        text: qsTr("Communication with the autonomous system is delayed.")
        anchors.top: disconnectedText.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 40*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }
}
