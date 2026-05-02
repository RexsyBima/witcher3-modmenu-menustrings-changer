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
from bs4 import BeautifulSoup
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


xmls_file_path = retrieve_xml_files()
mod_list = [f"{f.split('/')[-1]}" for f in xmls_file_path]


def get_mod_category(mod_display_name: str) -> None | str:
    output = "".join(s for s in mod_display_name.split(".") if s in IDs)
    return None if len(output) == 0 else output


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        self.setFixedSize(QSize(1280, 720))
        self.setWindowTitle("Witcher 3 Modmenu Changer")
        self.selected_item: None | str = None
        self.current_mod_category: None | str = None
        self.soup: None | BeautifulSoup = None

        xml_files_list_widget = QListWidget()
        xml_files_list_widget.addItems(mod_list)
        xml_files_list_widget.currentRowChanged.connect(self.get_item)
        xml_files_list_widget.setFixedWidth(360)

        mod_total_widget = QLabel(f"Total mod : {len(mod_list)}")
        mod_total_widget.setStyleSheet("background-color: #3498db;")
        mod_total_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        submit_button_widget = QPushButton("Set mod")
        submit_button_widget.setDefault(True)
        submit_button_widget.clicked.connect(self.set_mod)

        category_choice = QComboBox()
        self.selected_category_choice: str | None = None
        category_choice.addItems(IDs2)
        category_choice.currentIndexChanged.connect(self.index_changed)
        category_choice.currentTextChanged.connect(self.text_changed)

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.print_ids)
        button.clicked.connect(self.the_button_was_toggled)

        self.test_label = QLabel("HELLO1")
        self.current_mod_category_widget_label = QLabel("")
        self.current_mod_category_widget_label.setFixedWidth(100)
        layout1.addWidget(xml_files_list_widget)
        layout1.addWidget(mod_total_widget)

        layout2.addWidget(category_choice)
        layout2.addWidget(submit_button_widget)
        layout2.addWidget(
            self.current_mod_category_widget_label, alignment=Qt.AlignmentFlag.AlignTop
        )
        layout2.addWidget(self.test_label, alignment=Qt.AlignmentFlag.AlignTop)
        # layout.addWidget(xml_files_list_widget)
        # layout.addWidget(mod_total_widget)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        # layout.addWidget(self.test_label)
        # layout.addWidget(category_choice)
        # layout.addWidget(self.current_mod_category_widget_label)
        # layout.addWidget(submit_button_widget)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def set_mod(self):
        print(self.selected_category_choice)

    def get_item(self, index: int):
        self.selected_index = mod_list[index]
        self.test_label.setText(self.selected_index)
        filepath = xmls_file_path[index]
        with open(filepath, "r") as f:
            data = f.read()
        self.soup = BeautifulSoup(data, "xml")
        mod_category = self.soup.find_all("Group")[0]["displayName"]
        assert isinstance(mod_category, str)
        self.current_mod_category = get_mod_category(mod_category)
        print(self.current_mod_category)
        if self.current_mod_category is not None:
            self.current_mod_category_widget_label.setText(self.current_mod_category)
        elif self.current_mod_category is None:
            self.current_mod_category_widget_label.setText("Not Set")

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
