#ifndef PYTHONCONTROLLER_H
#define PYTHONCONTROLLER_H
#include <QDebug>
#include <QObject>
#include <QProcess>

class PythonController: public QObject
{
    Q_OBJECT
    QProcess process;
public:
    PythonController(QObject *parent = nullptr);


    //macros allow obj to be invoked via the meta-object system
    Q_INVOKABLE void  startRenderer();
    Q_INVOKABLE void  stopRenderer();
};

#endif // PYTHONCONTROLLER_H
