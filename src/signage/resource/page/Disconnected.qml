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
        id: disconnectedText1
        color: "#000000"
        text: qsTr("通信不良が発生しています。")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.verticalCenter
        anchors.bottomMargin: 50*viewController.size_ratio
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 40*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }

        Text {
        id: disconnectedText2
        color: "#000000"
        text: qsTr("急な停車にご注意ください。")
        anchors.top: disconnectedText1.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 40*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }

    Text {
        id: disconnectedEnText
        color: "#000000"
        text: qsTr("Communication with the autonomous system is delayed.")
        anchors.top: disconnectedText2.bottom
        anchors.topMargin: 20*viewController.size_ratio
        anchors.horizontalCenter: parent.horizontalCenter
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.pointSize: 30*viewController.size_ratio
        font.bold: true
        elide: Text.ElideMiddle
    }
}
