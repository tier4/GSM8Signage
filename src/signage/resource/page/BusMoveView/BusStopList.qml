import QtQuick 2.9
import QtQuick.Controls 2.2

import "../Common"

Rectangle {
    id: busStopList
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
        id: beforeBusStopMarker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#ffffff"
        radius: 30*viewController.size_ratio
        anchors.left: parent.left
        anchors.leftMargin: getMargin(1)
        anchors.verticalCenter: centerBar.verticalCenter
        border.width: 10*viewController.size_ratio
        border.color: "#717171"

        Text {
            id: beforeBusStopName
            width: getTextWidth()
            color: "#717171"
            text: viewController.previous_station_name[0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: beforeBusStopMarker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: beforeBusStopNameEn
            width: getTextWidth()
            color: "#717171"
            text: viewController.previous_station_name[1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: beforeBusStopName.bottom
            anchors.topMargin: 5*viewController.size_ratio
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }

        visible : checkVisible(viewController.previous_station_name[0])
    }

    Rectangle {
        id: currentBusStopMarker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#0068b6"
        radius: 30*viewController.size_ratio
        anchors.left: parent.left
        anchors.leftMargin: getMargin(2)
        anchors.verticalCenter: centerBar.verticalCenter
        border.width: 10*viewController.size_ratio
        border.color: "#ffffff"

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
        id: nextBusStop1Marker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#ffffff"
        radius: 30*viewController.size_ratio
        anchors.left: parent.left
        anchors.leftMargin: getMargin(3)
        anchors.verticalCenter: centerBar.verticalCenter
        border.width: 10*viewController.size_ratio
        border.color: "#0068b6"

        Text {
            id: nextBusStop1Name
            width: getTextWidth()
            color: "#000000"
            text: viewController.arrival_station_name[0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop1Marker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: nextBusStop1NameEn
            width: getTextWidth()
            color: "#000000"
            text: viewController.arrival_station_name[1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop1Name.bottom
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

    Rectangle {
        id: nextBusStop2Marker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#ffffff"
        radius: 30*viewController.size_ratio
        anchors.verticalCenter: centerBar.verticalCenter
        anchors.horizontalCenter: centerBar.horizontalCenter
        border.width: 10*viewController.size_ratio
        border.color: "#0068b6"

        Text {
            id: nextBusStop2Name
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[1][0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop2Marker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: nextBusStop2NameEn
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[1][1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop2Name.bottom
            anchors.topMargin: 5*viewController.size_ratio
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }

        visible : checkVisible(viewController.next_station_list[1][0])
    }

    Rectangle {
        id: nextBusStop3Marker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#ffffff"
        radius: 30*viewController.size_ratio
        anchors.right: parent.right
        anchors.rightMargin: getMargin(3)
        anchors.verticalCenter: centerBar.verticalCenter
        border.width: 10*viewController.size_ratio
        border.color: "#0068b6"

        Text {
            id: nextBusStop3Name
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[2][0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop3Marker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: nextBusStop3NameEn
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[2][1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop3Name.bottom
            anchors.topMargin: 5*viewController.size_ratio
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        visible : checkVisible(viewController.next_station_list[2][0])
    }

    Rectangle {
        id: nextBusStop4Marker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#ffffff"
        radius: 30*viewController.size_ratio
        anchors.right: parent.right
        anchors.rightMargin: getMargin(2)
        anchors.verticalCenter: centerBar.verticalCenter
        border.width: 10*viewController.size_ratio
        border.color: "#0068b6"

        Text {
            id: nextBusStop4Name
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[3][0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop4Marker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: nextBusStop4NameEn
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[3][1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop4Name.bottom
            anchors.topMargin: 5*viewController.size_ratio
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        visible : checkVisible(viewController.next_station_list[3][0])
    }

    Rectangle {
        id: nextBusStop5Marker
        width: 60*viewController.size_ratio
        height: 60*viewController.size_ratio
        color: "#ffffff"
        radius: 30*viewController.size_ratio
        anchors.right: parent.right
        anchors.rightMargin: getMargin(1)
        anchors.verticalCenter: centerBar.verticalCenter
        border.width: 10*viewController.size_ratio
        border.color: "#0068b6"

        Text {
            id: nextBusStop5Name
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[4][0]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop5Marker.bottom
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 40*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        Text {
            id: nextBusStop5NameEn
            width: getTextWidth()
            color: "#000000"
            text: viewController.next_station_list[4][1]
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nextBusStop5Name.bottom
            anchors.topMargin: 5*viewController.size_ratio
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30*viewController.size_ratio
            font.bold: true
            elide: Text.ElideMiddle
            wrapMode: Text.WordWrap
        }
        visible : checkVisible(viewController.next_station_list[4][0])
    }

    ArrowDirection {
        id: middleArrow
        anchors.left: currentBusStopMarker.horizontalCenter
        anchors.leftMargin: (getMargin(1) / 2)
        anchors.verticalCenter: centerBar.verticalCenter
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

    function checkVisible(name) {
        return (name || name.length !== 0)
    }

    function getMargin(count) {
        // Because there will be 8 space in between the 7 station
        return viewController.monitor_width / 8 * count
    }

    function getTextWidth() {
        return viewController.monitor_width / 8 - 50
    }
}
