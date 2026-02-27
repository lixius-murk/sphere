#include "FrameProvider.h"


QImage FrameProvider::blackFrame(QSize *size)
{
    QImage img(W, H, QImage::Format_RGB888);
    img.fill(Qt::black);
    if (size) *size = img.size();
    return img;
}
bool FrameProvider::ensureAttached()
{
    if (m_map != MAP_FAILED) {
        struct stat st;
        if (fstat(m_fd, &st) != 0 || st.st_nlink == 0) {
            detach();
        }
    }

    if (m_map != MAP_FAILED) return true;

    int fd = open("/dev/shm/frames", O_RDONLY);
    if (fd < 0) return false;

    void *map = mmap(nullptr, BUF_SIZE, PROT_READ, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) { close(fd); return false; }

    struct stat st;
    fstat(fd, &st);

    m_fd    = fd;
    m_map   = map;
    m_inode = st.st_ino;
    return true;
}
void FrameProvider::detach()
{
    if (m_map != MAP_FAILED) { munmap(m_map, BUF_SIZE); m_map = MAP_FAILED; }
    if (m_fd  >= 0)          { close(m_fd);             m_fd  = -1; }
    m_inode = 0;
}
QImage FrameProvider::requestImage(const QString &, QSize *size, const QSize &)
{
    QMutexLocker lock(&m_mutex);

    if (!ensureAttached()) {
        return blackFrame(size);
    }

    const uchar *data = static_cast<const uchar *>(m_map);

    quint32 counter;
    memcpy(&counter, data, 4);

    QImage img(data + 4, W, H, W * 3, QImage::Format_RGB888);
    QImage copy = img.copy();

    if (size) *size = copy.size();
    return copy;
}
