#include "BufferReader.h"
#include <QDebug>
#include <cstring>

BufferReader::BufferReader()
{
    ctrl.setKey("Global\\ctrl");
    data.setKey("Global\\frame");

    // if (!ctrl.attach())
    //     qDebug() << "ctrl attach failed:" << ctrl.errorString();

    // if (!data.attach())
    //     qDebug() << "frame attach failed:" << data.errorString();
}
bool BufferReader::tryAttach() {
    if (!ctrl.isAttached()) {
        if (!ctrl.attach())
            return false;
    }

    if (!data.isAttached()) {
        if (!data.attach())
            return false;
    }

    return true;
}
bool BufferReader::readFrame(QImage& out)
{
    // if (!ctrl.isAttached() || !data.isAttached())
    //     return false;
    if(!tryAttach()){
        return 0;
    }
    CtrlBlock cb;

    ctrl.lock();
    std::memcpy(&cb, ctrl.constData(), sizeof(CtrlBlock));
    ctrl.unlock();

    if (cb.frameId == frameId)
        return false;

    frameId = cb.frameId;

    const int size = cb.w * cb.h * 3;
    QByteArray frame(size, Qt::Uninitialized);

    data.lock();
    std::memcpy(frame.data(), data.constData(), size);
    data.unlock();

    out = QImage(
              reinterpret_cast<const uchar*>(frame.constData()),
              cb.w,
              cb.h,
              QImage::Format_RGB888
              ).copy();

    return true;
}
