import QtQuick 2.9
import QtQuick.Controls 2.2

import "../Common"

Rectangle {
    id: busRouteName
    width: viewController.monitor_width
    height: viewController.monitor_height
    color: "#ACF600" 

    CurrentTime {
        id: displayCurrentTime
    }

    CenterBar {
        id: centerBar
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
    }

    RouteName {
        id: headerRouteName
        anchors.bottom: centerBar.top
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Rectangle {
        id: currentBusStopMarker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#0068b6"
        radius: 30*viewController.size_ratio
        anchors.left: parent.left
        anchors.leftMargin: getMargin()
        anchors.verticalCenter: centerBar.verticalCenter
        border.color: "#ffffff"
        border.width: 10*viewController.size_ratio

        Text {
            id: currentBusStopName
            width: getTextWidth()
            color: "#000000"
            text: viewController.departure_station_name[0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: currentBusStopMarker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: currentBusStopNameEn
            width: getTextWidth()
            color: "#000000"
            text: viewController.departure_station_name[1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: currentBusStopName.bottom
            anchors.topMargin: 5*viewController.size_ratio
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        visible : checkVisible(viewController.departure_station_name[0])
    }

    Rectangle {
        id: nextBusStopMarker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#ffffff"
        radius: 30*viewController.size_ratio
        anchors.right: parent.right
        anchors.rightMargin: getMargin()
        anchors.verticalCenter: centerBar.verticalCenter
        border.color: "#0068b6"
        border.width: 10*viewController.size_ratio

        Text {
            id: nextBusStopName
            width: getTextWidth()
            color: "#000000"
            text: viewController.arrival_station_name[0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStopMarker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: nextBusStopNameEn
            width: getTextWidth()
            color: "#000000"
            text: viewController.arrival_station_name[1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStopName.bottom
            anchors.topMargin: 5*viewController.size_ratio
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        visible : checkVisible(viewController.arrival_station_name[0])
    }

    ArrowDirection {
        id: middleArrow
        anchors.verticalCenter: centerBar.verticalCenter
        anchors.horizontalCenter: centerBar.horizontalCenter
    }

    ArrowDirection {
        id: rightArrow
        anchors.left: middleArrow.right
        anchors.leftMargin: 0
        anchors.verticalCenter: centerBar.verticalCenter
    }

    ArrowDirection {
        id: leftArrow
        anchors.right: middleArrow.left
        anchors.rightMargin: 0
        anchors.verticalCenter: centerBar.verticalCenter
    }

    Text {
        id: remainingTime
        text: viewController.display_phrase
        anchors.top: centerBar.bottom
        anchors.topMargin: 10*viewController.size_ratio
        anchors.horizontalCenter: parent.horizontalCenter
        font.bold: true
        font.pixelSize: 48*viewController.size_ratio
        visible: checkVisible(viewController.display_phrase)
    }

    function getTextWidth() {
        return viewController.monitor_width / 3 - 100
    }

    function checkVisible(name) {
        return (name || name.length !== 0)
    }

    function getMargin() {
        return viewController.monitor_width / 6
    }
}
