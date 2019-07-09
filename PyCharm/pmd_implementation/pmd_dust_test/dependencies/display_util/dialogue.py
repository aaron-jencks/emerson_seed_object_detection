from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QPushButton
import queue


def get_text(prompt: str, title: str = "Get Text", parent: QWidget = None):
    text, ok_pressed = QInputDialog.getText(parent, title, prompt, QLineEdit.Normal, "")
    if ok_pressed:
        return text


def get_filename(prompt: str, start_directory: str = "/home", valid_files: str = "All Files(*)",
                 parent: QWidget = None):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename, _ = QFileDialog.getOpenFileName(parent, prompt, start_directory, valid_files, options=options)
    return filename


def get_yes_no(prompt: str = "???", description: str = "", detailed_text: str = "", parent: QWidget = None):
    msg = QMessageBox(parent=parent)
    msg.setIcon(QMessageBox.Question)

    msg.setText(prompt)

    if description != "":
        msg.setInformativeText(description)

    if detailed_text != "":
        msg.setDetailedText(detailed_text)

    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    q = queue.Queue()

    def msgbtn(i: QPushButton):
        q.put(i.text())

    msg.buttonClicked.connect(msgbtn)

    msg.exec_()

    try:
        btn = q.get(True, 1)
        return btn == "&Yes"
    except queue.Empty as e:
        return False
