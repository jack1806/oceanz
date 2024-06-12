from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt


class EntryWidget(QWidget):

    def __init__(self, parent=None):
        super(EntryWidget, self).__init__(parent)
        self.text_box_layout = QHBoxLayout()
        self.text_box_layout.setContentsMargins(0, 0, 0, 0)

        self.text_up_label = QLabel()
        self.text_up_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.text_up_label.setMargin(0)

        self.text_down_label = QLabel()
        self.text_down_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.text_down_label.setMargin(0)

        self.text_box_layout.addWidget(self.text_up_label)
        self.text_box_layout.addWidget(self.text_down_label)
        self.setLayout(self.text_box_layout)

        self.text_up_label.setStyleSheet('''color: rgb(0, 255, 255);font: bold 14px;''')
        self.text_down_label.setStyleSheet('''color: rgb(255, 255, 255);font: bold 24px;''')

    def set_amount(self, text):
        self.text_down_label.setText(text)

    def set_session(self, text):
        self.text_up_label.setText(text)
