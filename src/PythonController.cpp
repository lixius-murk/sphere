#include "PythonController.h"
#include <QDir>
#include <QFile>
#include <QCoreApplication>
#include <QDebug>

PythonController::PythonController(QObject *parent) : QObject(parent)
{
    m_process.setProcessChannelMode(QProcess::MergedChannels);

    // connect(&m_process, &QProcess::readyReadStandardOutput, [this](){
    //     qDebug() << "Python:" << m_process.readAllStandardOutput();
    // });

    connect(&m_process, QOverload<int,QProcess::ExitStatus>::of(&QProcess::finished),
            [this](int code, QProcess::ExitStatus){
                qDebug() << "Python exited, code:" << code;
                emit runningChanged();
            });

    connect(&m_process, &QProcess::started, [this](){
        qDebug() << "Python started, PID:" << m_process.processId();
        emit runningChanged();
    });
}

Q_INVOKABLE void PythonController::startRenderer(const QString &rendererType,
                                                const QString &blType,
                                                const QString &movement)
{
    if (m_process.state() != QProcess::NotRunning) return;
    QString cleanScript = QDir::cleanPath(
        QCoreApplication::applicationDirPath() + "/../../clean.sh");
    QProcess::execute("bash", {cleanScript});


    QString workDir = QDir::cleanPath(
        QCoreApplication::applicationDirPath() + "/../../python_renderer");
    QString python  = workDir + "/.venv/bin/python3";
    QString script  = workDir + "/renderer.py";

    if (!QFile::exists(python)) python = "python3";
    if (!QFile::exists(script)) { qWarning() << "Script not found:" << script; return; }

    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    env.insert("VIRTUAL_ENV",  workDir + "/.venv");
    env.insert("PATH",         workDir + "/.venv/bin:" + env.value("PATH"));
    env.insert("PYTHONPATH",   workDir);

    m_process.setWorkingDirectory(workDir);
    m_process.setProcessEnvironment(env);
    m_process.start(python, {script, rendererType, blType, movement});
}

void PythonController::stopRenderer()
{
    if (m_process.state() == QProcess::NotRunning) return;
    m_process.terminate();
    if (!m_process.waitForFinished(3000))
        m_process.kill();
    emit runningChanged();
}
