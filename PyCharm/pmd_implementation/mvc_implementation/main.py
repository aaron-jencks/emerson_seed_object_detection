from mvc_implementation.display_util.daemons import PointCloudDisplayMachine
from mvc_implementation.Controller.daemons import Controller
from mvc_implementation.data_structures.Q import DequeManager

import multiprocessing as mp

from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mgr = DequeManager()
    mgr.start()

    dsp_tx = mp.Queue()
    dsp_rx = mp.Queue()
    dsp = PointCloudDisplayMachine(app, tx_q=dsp_tx, rx_q=dsp_rx, state_manager=mgr)

    avg_tx = mp.Queue()
    avg_rx = mp.Queue()
    avg = Controller(dsp, tx_q=avg_tx, rx_q=avg_rx)

    dsp.run()
    avg.start()
    print("Starting event loop")
    app.exec_()
