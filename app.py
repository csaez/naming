import logging
import importlib

logger = logging.getLogger(__name__)

# qt bindings
_qtBindings = None
for name in ("PyQt5", "PySide2"):
    try:
        QtCore = importlib.import_module("{}.QtCore".format(name))
        QtGui = importlib.import_module("{}.QtGui".format(name))
        QtWidgets = importlib.import_module("{}.QtWidgets".format(name))
        _qtBindings = name
        break
    except ImportError:
        pass

if _qtBindings is None:
    for name in ("PyQt4", "PySide"):
        try:
            QtCore = importlib.import_module("{}.QtCore".format(name))
            QtGui = importlib.import_module("{}.QtGui".format(name))
            QtWidgets = QtGui
            _qtBindings = name
            break
        except ImportError:
            pass

if _qtBindings is None:
    raise Exception("Qt binding not found: PyQt5, PySide2, PyQt4, PySide")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info(_qtBindings)
    logger.info(QtWidgets)
