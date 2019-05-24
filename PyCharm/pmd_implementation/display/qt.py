from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QGridLayout, QPushButton, QSlider, QLabel, QFileDialog
import pyqtgraph as pg


class DepthAverageerWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # QMainWindow.__init__(self)

        self.roi = False

    def run(self):
        self.init_ui()

    def init_ui(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        # region Sets up the roi and exit buttons

        try:
            self.roi_btn = QPushButton('roi', self)
            self.roi_btn.setToolTip('Create a new <b>ROI</b> (region of interest) or edit the current one.')
            self.roi_btn.clicked.connect(self.roi_clicked)
            self.roi_btn.resize(self.roi_btn.sizeHint())
        except Exception as e:
            print(e)

        self.exit_btn = QPushButton('Exit', self)
        self.exit_btn.setToolTip('Exit the program')
        self.exit_btn.clicked.connect(QApplication.instance().quit)
        self.exit_btn.resize(self.exit_btn.sizeHint())

        grid.addWidget(self.roi_btn, 2, 0)
        grid.addWidget(self.exit_btn, 2, 1)

        # endregion

        # region Sets up the colormap sliders

        cmx = QLabel('Max')
        self.cmap_max = QSlider(Qt.Vertical, self)
        self.cmap_max.setToolTip('Adjusts the upper saturation limit of the colormap')

        cmm = QLabel('Mid')
        self.cmap_mid = QSlider(Qt.Vertical, self)
        self.cmap_mid.setToolTip('Adjusts the mid-point of the colormap')

        cmn = QLabel('Min')
        self.cmap_min = QSlider(Qt.Vertical, self)
        self.cmap_min.setToolTip('Adjusts the lower saturation limit of the colormap')

        grid.addWidget(cmn, 0, 2)
        grid.addWidget(self.cmap_min, 1, 2)

        grid.addWidget(cmm, 0, 3)
        grid.addWidget(self.cmap_mid, 1, 3)

        grid.addWidget(cmx, 0, 4)
        grid.addWidget(self.cmap_max, 1, 4)

        # endregion

        # region Sets up the plots

        self.img = pg.ImageView()
        self.dmp = pg.ScatterPlotWidget()

        grid.addWidget(QLabel('Grayscale', self), 0, 0)
        grid.addWidget(self.img, 1, 0)

        grid.addWidget(QLabel('Point cloud', self), 0, 1)
        grid.addWidget(self.dmp, 1, 1)

        # endregion

        main = QWidget()
        main.setLayout(grid)
        self.setCentralWidget(main)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Depth Averaging Utility')
        self.statusBar().showMessage('Ready')
        self.show()

    def open_file(self) -> str:
        fname = QFileDialog.getOpenFileName(self, 'Select video file for reading', '/home')
        return fname[0]

    def roi_clicked(self):
        if not self.roi:
            self.statusBar().showMessage('Reading ROi')
            self.roi = True
        else:
            self.statusBar().showMessage('Finished reading ROI')
            self.roi = False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = DepthAverageerWindow()
    ex.run()
    # ex.start()
    sys.exit(app.exec_())
