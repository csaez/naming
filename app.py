import sys
Qt = None


if Qt is None:
    try:
        import PyQt5 as Qt
        from PyQt5 import QtCore, QtGui, QtWidgets
    except ImportError:
        pass

if Qt is None:
    try:
        import PySide2 as Qt
        from PySide2 import QtCore, QtGui, QtWidgets
    except ImportError:
        pass

if Qt is None:
    try:
        import PyQt4 as Qt
        from PyQt4 import QtCore, QtGui
        QtWidgets = QtGui
    except ImportError:
        pass

if Qt is None:
    try:
        import PySide as Qt
        from PySide import QtCore, QtGui
        QtWidgets = QtGui
    except ImportError:
        pass

if Qt is None:
    raise Exception("Qt binding not found")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QMainWindow()
    l = QtWidgets.QLabel("Hello {}".format(Qt.__name__))
    w.setCentralWidget(l)
    w.show()

    sys.exit(app.exec_())
