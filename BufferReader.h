#ifndef BUFFERREADER_H
#define BUFFERREADER_H
#include <QSharedMemory>
#include <QtTypes>
#include <QByteArray>
#include <QImage>

struct CtrlBlock {
    quint32 w;
    quint32 h;
    quint32 fmt;
    quint32 frameId;
};


class BufferReader
{
    QSharedMemory ctrl;
    QSharedMemory data;
    quint32 frameId = 0;

public:
    BufferReader();
    bool readFrame(QImage& out);
    bool tryAttach();
};


#endif // BUFFERREADER_H
