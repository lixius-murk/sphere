#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "frameprovider.h"
#include "pythoncontroller.h"
int main(int argc, char *argv[])
{
    // qDebug() << "App started";

    // QGuiApplication app(argc, argv);

    // QQmlApplicationEngine engine;
    // qDebug() << "Engine created";

    // engine.load(QUrl("qrc:/main.qml"));

    // if (engine.rootObjects().isEmpty()) {
    //     qDebug() << "QML load FAILED";
    //     return -1;
    // }

    // qDebug() << "QML loaded OK";
    // return app.exec();
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;

    engine.addImageProvider("frames", new FrameProvider);

    auto *py = new PythonController(&engine);
    engine.rootContext()->setContextProperty("PythonController", py);

    engine.load(QUrl("qrc:/main.qml"));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
