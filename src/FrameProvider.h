#ifndef FRAMEPROVIDER_H
#define FRAMEPROVIDER_H

#include <QQuickImageProvider>
#include <QImage>
#include <QMutex>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <cstring>

// QML polls this via a Timer + incrementing frameTag.
// Reads fresh from mmap on every requestImage call.

class FrameProvider : public QQuickImageProvider
{
public:
    static constexpr int W          = 800;
    static constexpr int H          = 600;
    static constexpr int FRAME_SIZE = W * H * 3;
    static constexpr int BUF_SIZE   = FRAME_SIZE + 4;

    explicit FrameProvider()
        : QQuickImageProvider(QQuickImageProvider::Image)
    {}

    ~FrameProvider()
    {
        detach();
    }

    QImage requestImage(const QString &, QSize *size, const QSize &) override;

private:
    void *m_map = MAP_FAILED;
    int   m_fd  = -1;
    QMutex m_mutex;
    ino_t m_inode = 0;

    void detach();

    bool ensureAttached();

    QImage blackFrame(QSize *size);
};

#endif // FRAMEPROVIDER_H
