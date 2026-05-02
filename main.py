from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
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


def get_mod_category(mod_display_name: str) -> str:
    return "".join(s for s in mod_display_name.split(".") if s in IDs)


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        self.setFixedSize(QSize(1280, 720))
        self.setWindowTitle("Witcher 3 Modmenu Changer")
        self.selected_item: None | str = None
        self.current_mod_category: None | str = None

        xml_files_list_widget = QListWidget()
        xml_files_list_widget.addItems(xml_files)
        xml_files_list_widget.currentRowChanged.connect(self.get_item)
        xml_files_list_widget.setFixedWidth(360)

        mod_total_widget = QLabel(f"Total mod : {len(xml_files)}")
        mod_total_widget.setStyleSheet("background-color: #3498db;")
        mod_total_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        category_choice = QComboBox()
        self.selected_category_choice: str | None = None
        category_choice.addItems(IDs2)
        category_choice.currentIndexChanged.connect(self.index_changed)
        category_choice.currentTextChanged.connect(self.text_changed)

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.print_ids)
        button.clicked.connect(self.the_button_was_toggled)

        layout1.addWidget(xml_files_list_widget)
        layout1.addWidget(mod_total_widget)

        self.test_label = QLabel("HELLO1")
        # layout.addWidget(xml_files_list_widget)
        # layout.addWidget(mod_total_widget)
        layout.addLayout(layout1)
        layout.addWidget(self.test_label)
        layout.addWidget(category_choice)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_item(self, item: int):
        self.selected_item = xml_files[item]
        self.test_label.setText(self.selected_item)

    def index_changed(self, index):
        self.selected_category_choice = IDs[index]

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
