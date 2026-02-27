#include "CameraLogic.h"
#include <QtMultimedia/QMediaDevices>
#include <QDebug>

CameraLogic::CameraLogic(QObject *parent) : QObject(parent) {}

CameraLogic::~CameraLogic() { stop(); }

void CameraLogic::toggle()
{
    m_active ? stop() : start();
}

void CameraLogic::start()
{
    if (m_active) return;

    auto devices = QMediaDevices::videoInputs();
    if (devices.isEmpty()) { qWarning() << "No camera found"; return; }

    m_camera  = new QCamera(devices[0], this);
    m_sink    = new QVideoSink(this);
    m_session = new QMediaCaptureSession(this);

    m_session->setCamera(m_camera);
    m_session->setVideoSink(m_sink);

    connect(m_sink, &QVideoSink::videoFrameChanged,
            this,   &CameraLogic::onFrame);

    m_camera->start();
    m_active = true;
    emit activeChanged();
    qDebug() << "Camera started";
}

void CameraLogic::stop()
{
    if (!m_active) return;

    if (m_camera) { m_camera->stop(); delete m_camera; m_camera = nullptr; }
    delete m_sink;    m_sink    = nullptr;
    delete m_session; m_session = nullptr;

    m_active = false;
    emit activeChanged();
    qDebug() << "Camera stopped";
}

void CameraLogic::onFrame(const QVideoFrame &frame)
{
    if (!frame.isValid()) return;
    QImage img = frame.toImage().convertToFormat(QImage::Format_RGB888);
    if (!img.isNull())
        emit frameReady(img);
}
