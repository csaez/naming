import sys

# qt bindings
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


# application code
class MultiCompleter(QtWidgets.QCompleter):
    def pathFromIndex(self, index):
        suggestion = super(MultiCompleter, self).pathFromIndex(index)
        currentText = self.widget().text()
        splittedText = currentText.rsplit("_", 1)
        splittedText[-1] = suggestion
        return "_".join(splittedText)

    def splitPath(self, path):
        return [path.split("_")[-1]]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QMainWindow()
    pane = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()

    tokens = ["description", "side", "category", "type"]

    model = QtGui.QStringListModel()
    model.setStringList(tokens)

    tokenCompleter = MultiCompleter()
    tokenCompleter.setModel(model)

    activeRule = QtWidgets.QLineEdit()
    activeRule.setPlaceholderText("Type rule pattern here")
    activeRule.setCompleter(tokenCompleter)
    layout.addWidget(activeRule)

    tokenList = QtWidgets.QListView()
    tokenList.setModel(model)
    layout.addWidget(tokenList)

    layout.addStretch()

    pane.setLayout(layout)
    w.setCentralWidget(pane)
    w.show()

    sys.exit(app.exec_())
