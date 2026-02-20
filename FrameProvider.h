#ifndef FRAMEPROVIDER_H
#define FRAMEPROVIDER_H

#include <QQuickImageProvider>
#include <QImage>
#include <QMutex>
#include <QTimer>
#include "FrameReceiver.h"
class FrameProvider : public QQuickImageProvider
{
    FrameReceiver receiver;
    QImage lastFrame;
    QMutex mutex;
public:
    FrameProvider() : QQuickImageProvider(QQuickImageProvider::Image) {}
    QImage requestImage(const QString&, QSize*, const QSize&)
    {
        static bool pythonStarted = false;

        // Check if Python is running (you might want to expose this from PythonController)
        // For now, just try to connect if we don't have frames yet
        if (!pythonStarted && lastFrame.isNull()) {
            receiver.connectToServer();
        }

        QImage newFrame;
        if (receiver.getFrame(newFrame)) {
            QMutexLocker lock(&mutex);
            lastFrame = newFrame;
            pythonStarted = true;
            qDebug() << "✓ First frame received!";
        }

        if (lastFrame.isNull()) {
            static QImage stub(800, 600, QImage::Format_RGB888);
            stub.fill(Qt::black);

            // Draw "Waiting for Python..." text
            static bool firstTime = true;
            if (firstTime) {
                qDebug() << "Waiting for Python renderer to start...";
                firstTime = false;
            }

            return stub;
        }

        return lastFrame;
    }
};

#endif
