#include "frameprovider.h"


QImage FrameProvider::requestImage(
    const QString&,
    QSize*,
    const QSize&
    )
{
    QMutexLocker lock(&mutex);

    if (lastFrame.isNull()) {
        static QImage stub(640, 480, QImage::Format_RGB888);
        stub.fill(Qt::black);
        return stub;
    }

    return lastFrame;
}



void FrameProvider::updateLoop()
{
    static bool attached = false;

    if (!attached) {
        if (!reader.tryAttach())
            return;

        attached = true;
        qDebug() << "Shared memory attached";
    }

    QImage img;
    if (reader.readFrame(img)) {
        QMutexLocker lock(&mutex);
        lastFrame = img;
    }
}

