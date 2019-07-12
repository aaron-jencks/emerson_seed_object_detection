import socket
# import pyqtgraph as pg
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
# from PyQt5.QtCore import pyqtSlot


buffsize = 3072000
residual_data = ''


def readline(sock: socket.socket) -> str:
    """Continuously calls read on the given socket until a '\n' is found,
    then saves the residual and returns the string"""

    global residual_data

    if '~~~\n' in residual_data:
        index = residual_data.find('~~~\n')

        temp = residual_data[:index]

        if index < len(residual_data) - 4:
            residual_data = residual_data[index + 4:]
        else:
            residual_data = ''

        return temp

    result = residual_data

    data_read = sock.recv(buffsize).decode('latin-1')
    while data_read != '' and '~~~\n' not in data_read:
        result += data_read
        data_read = sock.recv(buffsize).decode('latin-1')

    if data_read != '':
        index = data_read.find('~~~\n')
        result += data_read[:index]
        if index < len(data_read) - 4:
            residual_data = data_read[index + 4:]
        else:
            residual_data = ''

    return result


# class ClientWidget(QWidget):
#     def __init__(self, hosts: list, depth_qs: dict, rgb_qs: dict):
#         super().__init__()
#
#         self.hosts = hosts
#         self.dqs = depth_qs
#         self.cqs = rgb_qs
#
#         self.grid = QGridLayout()
#         self.grid.setSpacing(10)
#         self.setLayout(self.grid)
