#include "PythonController.h"
#include <QCoreApplication>
#include <QDir>
#include <QSharedMemory>


PythonController::PythonController(QObject *parent): QObject(parent){
    process.setProcessChannelMode(QProcess::MergedChannels);
    //MergedChannels for merging output and errors in single standard output channel
};
Q_INVOKABLE void  PythonController::startRenderer(){
    if (process.state() != QProcess::NotRunning)
        return;
    QSharedMemory ctrl("ctrl");
    QSharedMemory frame("frame");
    qDebug() << "Starting python renderer";
    process.setWorkingDirectory(
        QDir::cleanPath(
            QCoreApplication::applicationDirPath() + "/../../python_renderer"
            )
        );
    QString pythonExe = "D:/QtProj/app_test/python_renderer/.venv/Scripts/python.exe";
    QString script = QDir::toNativeSeparators(
        QCoreApplication::applicationDirPath() + "/../../python_renderer/renderer.py"
        );
    qDebug() << QFile::exists(script) << script;
    qDebug() << "Launching:" << pythonExe << script;

    process.start(pythonExe, QStringList() << script);

    connect(&process, &QProcess::readyReadStandardOutput, [this](){
        qDebug() << process.readAllStandardOutput();
    });
    connect(&process, &QProcess::readyReadStandardError, [this](){
        qDebug() << process.readAllStandardError();
    });

};
Q_INVOKABLE void  PythonController::stopRenderer(){
    if (process.state() == QProcess::NotRunning)
        return;

    qDebug() << "Stopping python renderer";
    process.terminate();
    process.waitForFinished(3000);
    //waitForFinished so we don't start event loop, just run renderer

};
