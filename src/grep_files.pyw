import sys
from typing import List
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QHBoxLayout
    , QVBoxLayout, QLineEdit, QListWidget
)

class GrepFiles(QDialog):
    Backed = 2
    # SelectFileManager.Accepted（1）: 正常終了
    # SelectFileManager.Rejected（0）：異常終了
    def __init__(self, file_list: List[str], parent=None):
        super().__init__(parent)
        self.regex = ""

        # Title
        self.setWindowTitle("正規表現マッチ抽出")

        # Label
        self.label_regex = QLabel("正規表現")
        self.label_select_file_list = QLabel("対象ファイル")

        # Line
        self.line_edit_regex = QLineEdit()
        self.line_edit_regex.setPlaceholderText("正規表現を入力してください")
        self.line_edit_regex.textChanged.connect(self.button_next_able)

        # List
        self.list_widget = QListWidget()
        for file in file_list:
            self.list_widget.addItem(file)

        # Button
        self.button_back = QPushButton("戻る")
        self.button_back.clicked.connect(self.button_back_event)
        self.button_next = QPushButton("決定")
        self.button_next.setDisabled(True)
        self.button_next.clicked.connect(self.button_next_event)

        # Layout
        layout_v = QVBoxLayout()
        layout_v.addWidget(self.label_regex)
        layout_v.addWidget(self.line_edit_regex)
        layout_v.addWidget(self.label_select_file_list)
        layout_v.addWidget(self.list_widget)

        layout_h = QHBoxLayout()
        layout_h.addWidget(self.button_back)
        layout_h.addWidget(self.button_next)

        layout_v.addLayout(layout_h)
        self.setLayout(layout_v)

    def button_next_able(self):
        """次へボタンの活性化/非活性化
            正規表現ラベルが未入力の場合は非活性
        """
        match self.line_edit_regex.text().strip():
            case "":
                self.button_next.setDisabled(True)
            case _:
                self.button_next.setDisabled(False)

    def button_next_event(self):
        """次へボタンのイベント
        """
        self.regex = self.line_edit_regex.text()
        self.accept()

    def button_back_event(self):
        """戻るボタンのイベント
        """
        self.regex = ""
        self.done(GrepFiles.Backed)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = GrepFiles(sys.argv[1:])
    dialog.show()
    print(dialog.exec())
    sys.exit()