from cam_viewer.data_structures.state_machine import SocketedStateMachine, JMsg

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

import sys


class DisplayWindow(QMainWindow):

    def __init__(self):
        super().__init__()


class DisplayMachine(QMainWindow):
    """Used to create the Qt interface"""

    update = pyqtSignal([JMsg])

    def __init__(self, app: QApplication):
        super().__init__()

        self.app = app
        self.window = QMainWindow()
        self.grid = QGridLayout()
        self.widgets = {}
        self.states = {}
        self.run()
        self.update.connect(self.parse_update)

    def run(self):
        # self.app = QApplication(sys.argv)

        # Creates the new main window
        # self.window = DisplayWindow()
        self.window.statusBar().showMessage("Initializing...")

        # Sets up the grid layout
        # self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Creates basic layout widget
        widg = QWidget()
        widg.setLayout(self.grid)
        self.set_widget(JMsg("", widg))

        self.window.setGeometry(300, 300, 500, 400)
        self.window.setWindowTitle('Depth Averaging Utility')
        self.window.statusBar().showMessage('Ready')
        self.window.show()

        # region Sets up the states dict

        self.states['set_widget'] = self.set_widget
        self.states['status'] = self.set_status
        self.states['title'] = self.set_title
        self.states['show'] = self.window.show
        self.states['hide'] = self.window.hide
        self.states['create_button'] = self.create_button
        self.states['create_label'] = self.create_label
        self.states['create_text_entry'] = self.create_line_edit
        self.states['create_slider'] = self.create_slider
        self.states['create_widget'] = self.create_widget

        # endregion

    # region States

    def parse_update(self, msg: JMsg):
        """Collects the next state from the state_queue, if it doesn't exist, or the queue is empty, goes to idle."""
        self.states[msg.message](msg)

    def set_widget(self, msg: JMsg):
        """Changes the central widget of the display contained in this window"""
        self.window.setCentralWidget(msg.data)
        self.window.show()

    def set_status(self, msg: JMsg):
        """Changes the status bar message of this display's window"""
        self.window.statusBar().showMessage(msg.data)

    def set_title(self, msg: JMsg):
        """Changes the window title"""
        self.window.setWindowTitle(msg.data)

    def __create_widget(self, widg: QWidget, msg: JMsg):
        """Creates a new widget object"""

        if 'tip' in msg.data:
            widg.setToolTip(msg.data['tip'])

        # btn.clicked.connect(self.roi_clicked)
        widg.resize(widg.sizeHint())

        self.widgets[msg.data['id']] = widg
        self.grid.addWidget(widg, msg.data['row'], msg.data['col'], msg.data['rowSpan'], msg.data['columnSpan'])
        # widg = QWidget()
        # widg.setLayout(self.grid)
        # self.state_queue.append(JMsg('set_widget', widg))

        return widg

    def create_widget(self, msg: JMsg):
        """Creates a custom widget based on the arguments and type given"""
        if 'kwargs' in msg.data:
            temp = msg.data['type'](**msg.data['kwargs'], parent=self.window)
        else:
            temp = msg.data['type'](parent=self.window)

        self.__create_widget(temp, msg)

    def create_button(self, msg: JMsg):
        """Creates a new button with the given arguments"""
        msg.data['type'] = QPushButton
        msg.data['kwargs'] = {'text': msg.data['text']}
        self.create_widget(msg)

    def create_label(self, msg: JMsg):
        """Creates a new label with the given arguments"""
        msg.data['type'] = QLabel
        msg.data['kwargs'] = {'text': msg.data['text']}
        self.create_widget(msg)

    def create_line_edit(self, msg: JMsg):
        """Creates a new lineEdit (text entry) box with the given arguments"""
        msg.data['type'] = QLineEdit
        self.create_widget(msg)

    def create_slider(self, msg: JMsg):
        """Creates a new slider with the given arguments"""
        msg.data['type'] = QSlider
        msg.data['kwargs'] = {'orientation': msg.data['orient']}
        self.create_widget(msg)

    # endregion
