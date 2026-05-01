from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QMainWindow,
    QPushButton,
    QComboBox,
)
from src.witcher3_modmenu_changer import (
    IDs,
    IDs2,
    CONFIG_FILE,
    XML_LOCATION,
    BACKUP_DIR,
    EXCLUDED_FILES_XML,
    retrieve_xml_files,
)
import sys


xml_files = [f"{f.split('/')[-1]}" for f in retrieve_xml_files()]


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(1280, 720))
        self.setWindowTitle("Witcher 3 Modmenu Changer")
        xml_files_list_widget = QListWidget()
        xml_files_list_widget.addItems(xml_files)
        category_choice = QComboBox()
        category_choice.addItems(IDs2)
        category_choice.currentIndexChanged.connect(self.index_changed)
        category_choice.currentTextChanged.connect(self.text_changed)
        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.print_ids)
        button.clicked.connect(self.the_button_was_toggled)
        self.setCentralWidget(xml_files_list_widget)

    def index_changed(self, index):
        print(index)

    def text_changed(self, text):
        print(text)

    def print_ids(self):
        print(*IDs, *IDs2, sep=",")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)


app = QApplication(sys.argv)
window = MainApp()
window.show()

app.exec()
