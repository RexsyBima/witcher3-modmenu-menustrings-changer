import json
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
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.witcher3_modmenu_changer import (
    BACKUP_DIR,
    CONFIG_FILE,
    XML_LOCATION,
    IDs,
    IDs2,
    change_display_name,
    get_original_mod_name,
    retrieve_xml_files,
)

# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------

APP_STYLE = """
    QMainWindow, QDialog, QWidget {
        background-color: #1e1e1e;
        color: #d4d4d4;
        font-family: "Segoe UI", sans-serif;
        font-size: 13px
    }
    QLabel#sectionTitle {
        font-size: 11px;
        font-weight: bold;
        color: #6e6e6e;
        letter-spacing: 1px;
    }
    QLabel#modCount {
        background-color: #2a2a2a;
        color: #d4d4d4;
        font-weight: bold;
        padding: 6px 12px;
        border-radius: 4px;
        border: 1px solid #3a3a3a;
    }
    QLabel#currentCategory {
        color: #ffffff;
        font-weight: bold;
        font-size: 14px;
    }
    QListWidget {
        background-color: #252525;
        border: 1px solid #3a3a3a;
        border-radius: 6px;
        padding: 4px;
        outline: none;
    }
    QListWidget::item {
        padding: 8px 10px;
        border-radius: 4px;
        color: #c0c0c0;
    }
    QListWidget::item:selected {
        background-color: #3a3a3a;
        color: #ffffff;
    }
    QListWidget::item:hover:!selected {
        background-color: #2e2e2e;
    }
    QPushButton {
        background-color: #3a3a3a;
        color: #ffffff;
        border: 1px solid #4a4a4a;
        border-radius: 5px;
        padding: 8px 20px;
        font-weight: bold;
        font-size: 13px;
    }
    QPushButton:hover {
        background-color: #484848;
        border-color: #5a5a5a;
    }
    QPushButton:pressed {
        background-color: #2a2a2a;
    }
    QPushButton#secondary {
        background-color: #2a2a2a;
        border-color: #3a3a3a;
        color: #c0c0c0;
    }
    QPushButton#secondary:hover {
        background-color: #333333;
    }
    QComboBox {
        background-color: #252525;
        border: 1px solid #3a3a3a;
        border-radius: 5px;
        padding: 6px 12px;
        color: #d4d4d4;
    }
    QComboBox::drop-down {
        border: none;
        padding-right: 8px;
    }
    QComboBox QAbstractItemView {
        background-color: #252525;
        border: 1px solid #3a3a3a;
        selection-background-color: #3a3a3a;
        color: #d4d4d4;
    }
    QLineEdit {
        background-color: #252525;
        border: 1px solid #3a3a3a;
        border-radius: 5px;
        padding: 6px 10px;
        color: #d4d4d4;
    }
    QLineEdit:focus {
        border: 1px solid #6e6e6e;
    }
    QDialogButtonBox QPushButton {
        min-width: 80px;
    }
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_mod_category(mod_display_name: str) -> str | None:
    output = "".join(s for s in mod_display_name.split(".") if s in IDs)
    return output if output else None


# ---------------------------------------------------------------------------
# Directory Dialog
# ---------------------------------------------------------------------------


class SetDirectoryDialog(QDialog):
    def __init__(self, title: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(520, 130)
        self._build_ui()

    def _build_ui(self):
        # Folder path row
        folder_label = QLabel("Folder Path:")
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select or type a folder path...")

        browse_btn = QPushButton("Browse…")
        browse_btn.setObjectName("secondary")
        browse_btn.setFixedWidth(90)
        browse_btn.clicked.connect(self._browse_folder)

        path_row = QHBoxLayout()
        path_row.setSpacing(8)
        path_row.addWidget(self.folder_input)
        path_row.addWidget(browse_btn)

        # Buttons
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(folder_label)
        layout.addLayout(path_row)
        layout.addWidget(btn_box)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Folder", self.folder_input.text() or ""
        )
        if folder:
            self.folder_input.setText(folder)

    def accept(self):
        if not self.folder_input.text().strip():
            msg = QMessageBox(self)
            msg.setWindowTitle("Missing Input")
            msg.setText("Please provide a folder path.")
            msg.setWindowModality(Qt.WindowModality.ApplicationModal)
            msg.exec()
            return
        super().accept()

    def get_folder_path(self) -> str:
        return self.folder_input.text().strip()


# ---------------------------------------------------------------------------
# Main Window
# ---------------------------------------------------------------------------


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(1280, 720))
        self.setWindowTitle("Witcher 3 — Mod Menu Changer")

        self.selected_mod: str = ""
        self.selected_index: int = 0
        self.mod_filepath: str = ""
        self.soup: BeautifulSoup | None = None
        self.current_mod_category: str | None = None
        self.selected_category_choice: str = IDs[0]

        game_path = self._load_or_request_game_dir()
        self.xmls_file_path = retrieve_xml_files(game_path)
        self.mod_list = [f.split("/")[-1] for f in self.xmls_file_path]

        self._build_ui()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _load_or_request_game_dir(self) -> Path:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                game_dir = Path(json.load(f)["game_dir"])
                if (game_dir / XML_LOCATION).exists():
                    return game_dir
                else:
                    QMessageBox.critical(
                        self,
                        "Invalid Game Directory",
                        f"The previously saved game directory is invalid or missing:\n\n"
                        f"{game_dir}\n\n"
                        f"Please select your Witcher 3 directory again.",
                    )
        while True:
            dialog = SetDirectoryDialog("Set Your Witcher 3 Directory")
            if dialog.exec() == QDialog.DialogCode.Accepted:
                game_dir = dialog.get_folder_path()
                game_dir_path = Path(dialog.get_folder_path())
                if (game_dir_path / XML_LOCATION).exists():
                    with open(CONFIG_FILE, "w") as f:
                        json.dump({"game_dir": game_dir}, f)
                        return Path(game_dir)
                else:
                    QMessageBox.critical(
                        self,
                        "Invalid Game Directory",
                        f"The previously saved game directory is invalid or missing:\n\n"
                        f"{game_dir}\n\n"
                        f"Please select your Witcher 3 directory again.",
                    )

    def _build_ui(self):
        # ── Left panel: mod list ──────────────────────────────────────
        list_title = QLabel("MODS")
        list_title.setObjectName("sectionTitle")

        self.mod_list_widget = QListWidget()
        self.mod_list_widget.addItems(self.mod_list)
        self.mod_list_widget.setFixedWidth(360)
        self.mod_list_widget.currentRowChanged.connect(self._on_mod_selected)

        mod_count_label = QLabel(f"Total mods: {len(self.mod_list)}")
        mod_count_label.setObjectName("modCount")
        mod_count_label.setFixedWidth(360)
        mod_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        left = QVBoxLayout()
        left.setSpacing(8)
        left.setAlignment(Qt.AlignmentFlag.AlignTop)
        left.addWidget(list_title)
        left.addWidget(self.mod_list_widget)
        left.addWidget(mod_count_label)

        # ── Right panel: controls ─────────────────────────────────────
        controls_title = QLabel("CATEGORY")
        controls_title.setObjectName("sectionTitle")

        self.category_combo = QComboBox()
        self.category_combo.addItems(IDs2)
        self.category_combo.currentIndexChanged.connect(self._on_category_index_changed)
        self.category_combo.currentTextChanged.connect(self._on_category_text_changed)

        set_mod_btn = QPushButton("Apply Category")
        set_mod_btn.setDefault(True)
        set_mod_btn.clicked.connect(self._apply_mod)

        current_title = QLabel("CURRENT CATEGORY")
        current_title.setObjectName("sectionTitle")

        self.current_category_label = QLabel("—")
        self.current_category_label.setObjectName("currentCategory")

        selected_title = QLabel("SELECTED MOD")
        selected_title.setObjectName("sectionTitle")

        self.selected_mod_label = QLabel("None selected")
        self.selected_mod_label.setWordWrap(True)

        right = QVBoxLayout()
        right.setSpacing(10)
        right.setAlignment(Qt.AlignmentFlag.AlignTop)
        right.addWidget(controls_title)
        right.addWidget(self.category_combo)
        right.addWidget(set_mod_btn)
        right.addSpacing(16)
        right.addWidget(current_title)
        right.addWidget(self.current_category_label)
        right.addSpacing(16)
        right.addWidget(selected_title)
        right.addWidget(self.selected_mod_label)

        # ── Root ──────────────────────────────────────────────────────
        root = QHBoxLayout()
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(24)
        root.addLayout(left)
        root.addLayout(right)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _on_mod_selected(self, index: int):
        self.selected_mod = self.mod_list[index]
        self.selected_index = index
        self.mod_filepath = self.xmls_file_path[index]
        self.selected_mod_label.setText(self.selected_mod)

        with open(self.mod_filepath, "r") as f:
            self.soup = BeautifulSoup(f.read(), "xml")

        raw_display_name = self.soup.find_all("Group")[0]["displayName"]
        assert isinstance(raw_display_name, str)
        self.current_mod_category = get_mod_category(raw_display_name)

        self.current_category_label.setText(
            self.current_mod_category if self.current_mod_category else "Not Set"
        )

    def _on_category_index_changed(self, index: int):
        self.selected_category_choice = IDs[index]

    def _on_category_text_changed(self, text: str):
        print(f"Category changed: {text}")

    def _apply_mod(self):
        if self.soup is None:
            QMessageBox.warning(self, "No Mod Selected", "Please select a mod first.")
            return

        for group in self.soup.find_all("Group"):
            display_name = group["displayName"]
            assert isinstance(display_name, str)
            group["displayName"] = change_display_name(
                get_original_mod_name(display_name),
                self.selected_category_choice,
            )

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = BACKUP_DIR / f"{Path(self.selected_mod).name}.{timestamp}.bak"
        shutil.copy2(self.mod_filepath, backup_path)

        with open(self.mod_filepath, "w", encoding="utf-8") as f:
            f.write(str(self.soup))

        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText(
            f"<b>{self.selected_mod}</b> has been updated successfully. backup file hase been saved as {backup_path}"
        )
        msg.exec()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

app = QApplication()
app.setStyleSheet(APP_STYLE)
window = MainApp()
window.show()
app.exec()
