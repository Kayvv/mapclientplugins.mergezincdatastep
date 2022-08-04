"""
User interface for github.com/OpenCMISS-Bindings/mergedatatozinc
"""
from PySide2 import QtCore, QtWidgets

from mapclientplugins.mergezincdatastep.view.ui_mergezincdatawidget import Ui_MergeZincDataWidget


class MergeZincDataWidget(QtWidgets.QWidget):

    def __init__(self, model, parent=None):
        """
        """
        super(MergeZincDataWidget, self).__init__(parent)
        self._ui = Ui_MergeZincDataWidget()
        self._ui.setupUi(self)
        self._done_callback = None

        self._model = model

        self._ui.tableViewMarkerMap.setModel(self._model.get_marker_model())
        self._ui.tableViewMarkerMap.setItemDelegateForColumn(1, ComboBoxDelegate())
        self._make_connections()

    def _make_connections(self):
        self._ui.pushButtonDone.clicked.connect(self._done_button_clicked)

    def _done_button_clicked(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self._model.done()
        QtWidgets.QApplication.restoreOverrideCursor()
        self._done_callback()

    def register_done_execution(self, callback):
        self._done_callback = callback


class ComboBoxDelegate(QtWidgets.QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.setFrame(False)

        return editor

    def setEditorData(self, editor, index):
        data = index.model().data(index, QtCore.Qt.EditRole)
        if data is not None:
            editor.clear()
            editor.insertItems(0, data)
            cell_data = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setCurrentText(cell_data)

    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
