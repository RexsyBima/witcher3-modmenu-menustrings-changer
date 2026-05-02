from bs4 import BeautifulSoup
import shutil
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.witcher3_modmenu_changer import (
    BACKUP_DIR,
    IDs,
    IDs2,
    change_display_name,
    get_original_mod_name,
    retrieve_xml_files,
)

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
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout2 = QVBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        mod_total_widget.setFixedWidth(360)

        submit_button_widget = QPushButton("Set mod")
        submit_button_widget.setDefault(True)
        submit_button_widget.clicked.connect(self.set_mod)

        self.category_choice = QComboBox()
        self.selected_category_choice: str = IDs[0]
        self.category_choice.addItems(IDs2)
        self.category_choice.currentIndexChanged.connect(self.index_changed)
        self.category_choice.currentTextChanged.connect(self.text_changed)

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.print_ids)
        button.clicked.connect(self.the_button_was_toggled)

        self.test_label = QLabel("HELLO1")
        self.current_mod_category_widget_label = QLabel("")
        layout1.addWidget(xml_files_list_widget)
        layout1.addWidget(mod_total_widget)

        layout2.addWidget(self.category_choice)
        layout2.addWidget(submit_button_widget)
        layout2.addWidget(self.current_mod_category_widget_label)
        layout2.addWidget(self.test_label, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def set_mod(self):
        assert isinstance(self.soup, BeautifulSoup)
        print(self.selected_category_choice)
        groups = self.soup.find_all("Group")
        for g in groups:
            display_name = g["displayName"]
            assert isinstance(display_name, str)
            g["displayName"] = change_display_name(
                get_original_mod_name(display_name), self.selected_category_choice
            )
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{Path(self.selected_mod).name}.{timestamp}.bak"
        backup_path = BACKUP_DIR / backup_filename
        print(self.mod_filepath)
        shutil.copy2(self.mod_filepath, backup_path)
        with open(self.mod_filepath, "w", encoding="utf-8") as f:
            f.write(str(self.soup))
        # TODO: Display a success dialog

    def get_item(self, index: int):
        self.selected_mod = mod_list[index]
        self.selected_index = index
        self.test_label.setText(self.selected_mod)
        self.mod_filepath = xmls_file_path[index]
        with open(self.mod_filepath, "r") as f:
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


app = QApplication()
window = MainApp()
window.show()

app.exec()
