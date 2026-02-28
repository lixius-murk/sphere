#ifndef CAMERALOGIC_H
#define CAMERALOGIC_H

#include <QObject>
#include <QtMultimedia/QCamera>
#include <QtMultimedia/QVideoSink>
#include <QtMultimedia/QVideoFrame>
#include <QImage>
#include <QtMultimedia/QMediaCaptureSession>

class CameraLogic : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool active READ active NOTIFY activeChanged)

public:
    explicit CameraLogic(QObject *parent = nullptr);
    ~CameraLogic();

    bool active() const { return m_active; }

    Q_INVOKABLE void toggle();

signals:
    void activeChanged();
    void frameReady(const QImage &frame);

private slots:
    void onFrame(const QVideoFrame &frame);

private:
    void start();
    void stop();

    bool m_active = false;
    QCamera              *m_camera  = nullptr;
    QVideoSink           *m_sink    = nullptr;
    QMediaCaptureSession *m_session = nullptr;
};

#endif // CAMERALOGIC_H
