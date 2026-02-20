#include "FrameReceiver.h"
#include <QDebug>
#include <QTimer>
FrameReceiver::FrameReceiver(QObject *parent) : QObject(parent)
{
    socket = new QTcpSocket(this);
    waitingForHeader = true;
    expectedBytes = 0;
    isConnecting = false;

    connect(socket, &QTcpSocket::readyRead, this, &FrameReceiver::onReadyRead);
    connect(socket, &QTcpSocket::connected, this, &FrameReceiver::onConnected);
    connect(socket, &QTcpSocket::errorOccurred, this, &FrameReceiver::onError);

    // DO NOT connect here - wait for explicit connectToServer call
    // socket->connectToHost("127.0.0.1", 12345); // REMOVE THIS LINE
}

void FrameReceiver::connectToServer()
{
    // Don't try to connect if Python isn't running yet
    // This will be called from requestImage only when needed

    if (socket->state() == QAbstractSocket::ConnectedState) {
        return; // Already connected
    }

    if (isConnecting) {
        return; // Already attempting to connect
    }

    qDebug() << "Connecting to Python frame server...";
    isConnecting = true;
    socket->connectToHost("127.0.0.1", 12345);
}

void FrameReceiver::onConnected()
{
    qDebug() << "✓ Connected to Python frame server";
    isConnecting = false;

    // Reset state to ensure clean frame reading
    waitingForHeader = true;
    frameBuffer.clear();
}

void FrameReceiver::onError(QAbstractSocket::SocketError error)
{
    qDebug() << "Socket error:" << socket->errorString();
    isConnecting = false;

    // If we're not connected, try again in 1 second
    if (socket->state() != QAbstractSocket::ConnectedState) {
        QTimer::singleShot(1000, [this]() {
            connectToServer();
        });
    }
}

void FrameReceiver::onReadyRead()
{
    static QByteArray syncBuffer; // Buffer to help resync

    while (socket->bytesAvailable() > 0) {
        if (waitingForHeader) {
            // Need at least HEADER_SIZE bytes for header
            if (socket->bytesAvailable() < HEADER_SIZE) {
                return;
            }

            QByteArray header = socket->read(HEADER_SIZE);

            // Read header fields
            quint32 magic = *reinterpret_cast<const quint32*>(header.constData());
            expectedWidth = *reinterpret_cast<const quint32*>(header.constData() + 4);
            expectedHeight = *reinterpret_cast<const quint32*>(header.constData() + 8);

            // Check magic number to verify we're in sync
            if (magic != FRAME_MAGIC) {
                qDebug() << "Lost sync - magic mismatch:" << Qt::hex << magic << "!=" << FRAME_MAGIC;
                qDebug() << "Attempting to resync...";

                // We're out of sync. Search through the buffer for the magic number
                // Put the header back plus any extra data we might have
                QByteArray searchBuffer = header + socket->peek(socket->bytesAvailable());

                // Find the next occurrence of FRAME_MAGIC
                int magicPos = -1;
                for (int i = 1; i < searchBuffer.size() - 3; i++) {
                    quint32 val = *reinterpret_cast<const quint32*>(searchBuffer.constData() + i);
                    if (val == FRAME_MAGIC) {
                        magicPos = i;
                        break;
                    }
                }

                if (magicPos >= 0) {
                    // Found magic number at position magicPos
                    // Discard everything before it
                    int bytesToDiscard = magicPos;
                    qDebug() << "Resynced at offset" << bytesToDiscard;

                    if (bytesToDiscard > 0) {
                        socket->read(bytesToDiscard); // Discard bad data
                    }
                    // Continue loop to read the next header
                    continue;
                } else {
                    // No magic found in current buffer - discard all and wait for more
                    qDebug() << "No magic found, discarding all current data";
                    socket->readAll(); // Discard everything
                    return;
                }
            }

            // Sanity check dimensions
            if (expectedWidth <= 0 || expectedWidth > 2000 ||
                expectedHeight <= 0 || expectedHeight > 2000) {
                qDebug() << "Invalid dimensions after valid magic:" << expectedWidth << "x" << expectedHeight;
                qDebug() << "This shouldn't happen - possible memory corruption";
                waitingForHeader = true;
                continue;
            }

            expectedBytes = expectedWidth * expectedHeight * 3;
            qDebug() << "Receiving frame:" << expectedWidth << "x" << expectedHeight
                     << "(" << expectedBytes << "bytes) - Magic:" << Qt::hex << magic;

            waitingForHeader = false;
            frameBuffer.clear();
            frameBuffer.reserve(expectedBytes);

        } else {
            // Reading frame data
            QByteArray data = socket->readAll();
            frameBuffer.append(data);

            if (frameBuffer.size() >= expectedBytes) {
                // Complete frame received
                if (frameBuffer.size() > expectedBytes) {
                    qDebug() << "Warning: Received more data than expected. Truncating.";
                    frameBuffer.truncate(expectedBytes);
                }

                QImage img(reinterpret_cast<const uchar*>(frameBuffer.constData()),
                           expectedWidth, expectedHeight, QImage::Format_RGB888);

                if (!img.isNull()) {
                    {
                        QMutexLocker locker(&mutex);
                        latestFrame = img.copy();
                    }
                    qDebug() << "✓ Frame received and stored - ID:" << frameCounter++;
                } else {
                    qDebug() << "Failed to create QImage from frame data";
                }

                // Prepare for next frame
                waitingForHeader = true;

                // If we got more data than expected, the extra belongs to the next frame
                int extraBytes = frameBuffer.size() - expectedBytes;
                if (extraBytes > 0) {
                    qDebug() << "Extra bytes received:" << extraBytes << "- will process in next header";
                    // The extra data is still in the socket buffer (we readAll()),
                    // so we need to put it back? No, we already read it.
                    // Better approach: don't use readAll() in frame data mode
                }
            }
        }
    }
}

bool FrameReceiver::getFrame(QImage &out)
{
    QMutexLocker locker(&mutex);
    if (latestFrame.isNull())
        return false;
    out = latestFrame;
    return true;
}
