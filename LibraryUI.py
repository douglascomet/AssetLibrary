import pprint
from maya import cmds
from Qt import QtWidgets, QtCore, QtGui

import AssetLibrary
reload(AssetLibrary)


class AssetLibraryUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AssetLibraryUI, self).__init__(parent)

        self.library = AssetLibrary.AssetLibrary()

        # print self.library

        self.build_ui()

        self.populate_list_widget()

    def build_ui(self):
        '''Builds the UI using Qt.py to determine which version of PyQt/Pyside to use.
        '''

        # =====================================================================
        # PYQT Widget Defintions
        # =====================================================================

        self.setWindowTitle('AssetLibraryUI')

        # option_btn_widget = QtWidgets.QWidget()
        option_btn_widget_layout = QtWidgets.QHBoxLayout()
        save_widget_layout = QtWidgets.QHBoxLayout()
        self.save_name_le = QtWidgets.QLineEdit()
        save_widget_layout.addWidget(self.save_name_le)

        save_btn = QtWidgets.QPushButton('Save')
        save_widget_layout.addWidget(save_btn)

        thumbnail_size = 64
        thumbnail_buffer_size = 12
        self.thumbnail_list_widget = QtWidgets.QListWidget()
        self.thumbnail_list_widget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.thumbnail_list_widget.setIconSize(QtCore.QSize(
            thumbnail_size, thumbnail_size))
        self.thumbnail_list_widget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.thumbnail_list_widget.setGridSize(QtCore.QSize(
            thumbnail_size + thumbnail_buffer_size,
            thumbnail_size + thumbnail_buffer_size))

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(QtWidgets.QVBoxLayout())
        central_widget.layout().addLayout(save_widget_layout)
        central_widget.layout().addWidget(self.thumbnail_list_widget)
        central_widget.layout().addLayout(option_btn_widget_layout)

        self.setCentralWidget(central_widget)

        import_btn = QtWidgets.QPushButton('Import')
        option_btn_widget_layout.addWidget(import_btn)

        refresh_btn = QtWidgets.QPushButton('Refresh')
        option_btn_widget_layout.addWidget(refresh_btn)

        close_btn = QtWidgets.QPushButton('Close')
        option_btn_widget_layout.addWidget(close_btn)

        # =====================================================================
        # PYQT Execution Connections
        # =====================================================================

        save_btn.clicked.connect(self.save_ctrls)
        import_btn.clicked.connect(self.load_ctrls)
        refresh_btn.clicked.connect(self.populate_list_widget)
        close_btn.clicked.connect(self.close)

    def populate_list_widget(self):
        '''Populates QListWidget with assets loaded from json files.
        '''

        self.thumbnail_list_widget.clear()
        self.library.find_ctrl()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.thumbnail_list_widget.addItem(item)

            screenshot = info.get('screenshot')

            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load_ctrls(self):
        '''Loads selected asset from QListWidget Library
        '''

        current_item = self.thumbnail_list_widget.currentItem()

        if not current_item:
            return
        else:
            name = current_item.text()
            self.library.load_ctrl(name)

    def save_ctrls(self):
        '''Saves and adds to new asset entry to QListWidget
        '''

        name = self.save_name_le.text()

        if not name.strip():
            cmds.warning('You must give a name!')
            return

        self.library.save_ctrl(name)
        self.populate_list_widget()
        self.save_name_le.setText('')


def showUI():
    '''Shows Qt UI and attaches the UI to the main Maya window

    Returns:
        Qt Interface -- Qt UI that executes functionality from
                        controllerLibrary
    '''

    main_window = \
        [o for o in QtWidgets.qApp.topLevelWidgets()
            if o.objectName() == 'MayaWindow'][0]

    ui = AssetLibraryUI(main_window)
    ui.show()
    return ui
