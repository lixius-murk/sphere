#ifndef FRAMEPROVIDER_H
#define FRAMEPROVIDER_H

#include <QQuickImageProvider>
#include <QImage>
#include <QMutex>
#include <QTimer>
#include "BufferReader.h"

class FrameProvider final : public QQuickImageProvider
{
    BufferReader reader;
    QImage lastFrame;
    QMutex mutex;
public:
    FrameProvider()
        : QQuickImageProvider(QQuickImageProvider::Image) {
        auto *timer = new QTimer(this);
        connect(timer, &QTimer::timeout, this, &FrameProvider::updateLoop);
        timer->start(16);
    }
    void updateLoop();

    QImage requestImage(
        const QString&,
        QSize*,
        const QSize&
        ) override;
};

#endif
