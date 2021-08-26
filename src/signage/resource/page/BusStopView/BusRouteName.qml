import QtQuick 2.9
import QtQuick.Controls 2.2

Rectangle {
    id: busRouteName
    width: 1920
    height: 360
    color: "#ffffff"
    Text {
        id: busRouteText
        color: "#000000"
        text: getRouteName()
        anchors.verticalCenterOffset: -100
        font.bold: true
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        font.pointSize: 50
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        wrapMode: Text.WordWrap
    }

    Item {
        id: beforeAndAfterBusStop
        height: 100
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: busRouteText.bottom
        anchors.topMargin: 30

        Rectangle {
            id: beforeAndAfterBar
            width: 1700
            height: 44
            color: "#69bfd2"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            id: rectangle2
            width: 70
            height: 70
            color: "#ffffff"
            radius: 35
            anchors.verticalCenter: beforeAndAfterBar.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            border.color: "#717171"
            border.width: 5

            Rectangle {
                id: rectangle1
                width: 50
                height: 50
                color: "#0068b6"
                radius: 25
                border.width: 0
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Rectangle {
            id: beforeBusStopMarker
            width: 60
            height: 60
            color: "#ffffff"
            radius: 30
            anchors.left: parent.left
            anchors.leftMargin: 300
            anchors.verticalCenter: beforeAndAfterBar.verticalCenter
            border.color: "#717171"
            border.width: 10

            Text {
                id: beforeBusStopName
                width: 350
                color: "#717171"
                text: viewController.previous_station_list[0]
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.bottom
                anchors.topMargin: 2
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 30
                font.bold: true
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.WordWrap
            }
            visible : (viewController.previous_station_list[0] || viewController.previous_station_list[0].length !== 0)
        }

        Rectangle {
            id: nextBusStopMarker
            width: 60
            height: 60
            color: "#ffffff"
            radius: 30
            anchors.right: parent.right
            anchors.rightMargin: 300
            anchors.verticalCenter: beforeAndAfterBar.verticalCenter
            border.color: "#0068b6"
            border.width: 10

            Text {
                id: nextBusStopName
                width: 350
                text: viewController.arrival_station_name
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.bottom
                anchors.topMargin: 2
                font.bold: true
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.pixelSize: 30
                wrapMode: Text.WordWrap
            }
            visible : (viewController.arrival_station_name || viewController.arrival_station_name.length !== 0)
        }

        Text {
            id: busStopName
            width: 400
            color: "#000000"
            text: getDepatureStationName()
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: beforeAndAfterBar.verticalCenter
            anchors.topMargin: 42
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 30
            font.bold: true
            wrapMode: Text.WordWrap
        }
    }

    function getRouteName() {
        var routeName = viewController.route_name
        if(!routeName || routeName.length === 0)
        {
            routeName = qsTr("バスルート名")
        }
        return routeName
    }

    function getDepatureStationName() {
        var station_name = viewController.departure_station_name
        if(!station_name || station_name.length === 0)
        {
            station_name = qsTr("バス停名")
        }
        return station_name
    }
}




/*##^## Designer {
    D{i:2;anchors_x:179;anchors_y:"-45"}D{i:8;anchors_x:179;anchors_y:82}D{i:9;anchors_x:179;anchors_y:82}
D{i:7;anchors_y:89}D{i:10;anchors_x:179;anchors_y:82}
}
 ##^##*/