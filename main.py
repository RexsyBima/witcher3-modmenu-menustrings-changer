from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QListWidgetItem,
    QWidget,
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
        layout = QHBoxLayout()
        self.setFixedSize(QSize(1280, 720))
        self.setWindowTitle("Witcher 3 Modmenu Changer")
        self.selected_item: None | str = None
        xml_files_list_widget = QListWidget()
        xml_files_list_widget.addItems(xml_files)
        xml_files_list_widget.currentRowChanged.connect(self.get_item)
        xml_files_list_widget.setFixedWidth(360)
        test_label = QLabel("Hello world")
        category_choice = QComboBox()
        category_choice.addItems(IDs2)
        category_choice.currentIndexChanged.connect(self.index_changed)
        category_choice.currentTextChanged.connect(self.text_changed)
        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.print_ids)
        button.clicked.connect(self.the_button_was_toggled)
        layout.addWidget(xml_files_list_widget)
        layout.addWidget(test_label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_item(self, item: int):
        self.selected_item = xml_files[item]

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
