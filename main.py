import json
from PySide6.QtWidgets import (
    QFileDialog,
    QLineEdit,
    QMessageBox,
)
import shutil
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
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
    CONFIG_FILE,
    IDs,
    IDs2,
    change_display_name,
    get_original_mod_name,
    retrieve_xml_files,
)


def get_mod_category(mod_display_name: str) -> None | str:
    output = "".join(s for s in mod_display_name.split(".") if s in IDs)
    return None if len(output) == 0 else output


class CustomDialog(QDialog):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # --- Folder path input row ---
        folder_label = QLabel("Folder Path:")
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select or type a folder path...")

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_folder)

        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(6)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_btn)

        # --- Main layout ---
        layout = QVBoxLayout()
        layout.addLayout(folder_layout)
        layout.addWidget(self.buttonBox)
        self.resize(500, 200)
        self.setLayout(layout)

    def _browse_folder(self):
        """Open a native folder picker and populate the input field."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            self.folder_input.text() or "",  # start from current value if any
        )
        if folder:
            self.folder_input.setText(folder)

    def accept(self):
        """Validate that a folder path was provided before closing."""
        if not self.folder_input.text().strip():
            QMessageBox.warning(self, "Missing Input", "Please provide a folder path.")
            return  # block the dialog from closing
        super().accept()

    def get_folder_path(self) -> str:
        """Call this after exec() returns Accepted to retrieve the value."""
        return self.folder_input.text().strip()

    def reject(self) -> None:
        return super().reject()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout1 = QVBoxLayout()
        layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        game_path = self.get_game_dir()
        self.xmls_file_path = retrieve_xml_files(game_path)
        self.mod_list = [f"{f.split('/')[-1]}" for f in self.xmls_file_path]
        layout2 = QVBoxLayout()
        layout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(QSize(1280, 720))
        self.setWindowTitle("Witcher 3 Modmenu Changer")
        self.selected_item: None | str = None
        self.current_mod_category: None | str = None
        self.soup: None | BeautifulSoup = None

        xml_files_list_widget = QListWidget()
        xml_files_list_widget.addItems(self.mod_list)
        xml_files_list_widget.currentRowChanged.connect(self.get_item)
        xml_files_list_widget.setFixedWidth(360)

        mod_total_widget = QLabel(f"Total mod : {len(self.mod_list)}")
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

    def get_game_dir(self) -> Path:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return Path(config["game_dir"])

        dialog = CustomDialog("Set Your Witcher 3 Directory")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            game_dir = dialog.get_folder_path()
            with open(CONFIG_FILE, "w") as f:
                json.dump({"game_dir": str(game_dir)}, f)
            return Path(game_dir)
        return Path("foo")

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
        success_message_box = QMessageBox(self)
        success_message_box.setText("The file has been modified")
        success_message_box.exec()

    def get_item(self, index: int):
        self.selected_mod = self.mod_list[index]
        self.selected_index = index
        self.test_label.setText(self.selected_mod)
        self.mod_filepath = self.xmls_file_path[index]
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
