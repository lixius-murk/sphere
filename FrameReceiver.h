#ifndef FRAMERECEIVER_H
#define FRAMERECEIVER_H
#include <QSharedMemory>
#include <QtTypes>
#include <QByteArray>
#include <QImage>
#include <QAbstractSocket>
#include <QTcpSocket>
#include <QMutex>
#include <QObject>
static const quint32 FRAME_MAGIC = 0xDEADBEEF;
static const int HEADER_SIZE = 12;
class FrameReceiver : public QObject
{
    Q_OBJECT
public:
    explicit FrameReceiver(QObject *parent = nullptr);
    bool getFrame(QImage &out);
    void connectToServer(); // Add this

private slots:
    void onReadyRead();
    void onConnected();
    void onError(QAbstractSocket::SocketError error);

private:
    QTcpSocket *socket;
    QMutex mutex;
    QImage latestFrame;
    bool waitingForHeader;
    int expectedWidth, expectedHeight;
    int expectedBytes;
    QByteArray frameBuffer;
    bool isConnecting; // Add this to prevent multiple connection attempts
    int frameCounter = 0;

};

#endif // FRAMERECEIVER_H
