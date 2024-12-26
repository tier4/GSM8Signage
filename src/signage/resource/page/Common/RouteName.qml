import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Shapes 1.12

Item {
    id: routeName

    Text {
        id: busRouteText
        color: "#000000"
        text: viewController.route_name[0] ? viewController.route_name[0] : "行き先案内"
        anchors.bottom: busRouteTextEn.top
        anchors.horizontalCenter: parent.horizontalCenter
        font.pointSize: 80*viewController.size_ratio
        font.bold: true
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: busRouteTextEn
        color: "#000000"
        text: viewController.route_name[1] ? viewController.route_name[1] : "Route Information"
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10*viewController.size_ratio
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 45*viewController.size_ratio
        font.bold: true
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
