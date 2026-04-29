# def main() -> None:
#     print("Hello from witcher3-modmenu-changer!")
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

CONFIG_FILE = Path.cwd() / ".witcher3_modmenu_config.json"
XML_LOCATION = Path("bin/config/r4game/user_config_matrix/pc")
BACKUP_DIR = Path.cwd() / "backup"

IDs = (
    "alchemy_and_equipment",
    "camera",
    "characters",
    "combat",
    "gameplay",
    "quests_and_adventures",
    "user_interface",
    "visuals_and_graphics",
    "miscellaneous",
)


IDs2 = (
    "Alchemy and Equipment",
    "Camera",
    "Characters",
    "Combat",
    "Gameplay",
    "Quests and Adventures",
    "User Interface",
    "Visuals and Graphics",
    "Miscellaneous",
)

EXCLUDED_FILES_XML = (
    "audio.xml",
    "display.xml",
    "gameplay.xml",
    "gamma.xml",
    "graphics.xml",
    "graphicsdx11.xml",
    "hdr.xml",
    "hidden.xml",
    "hud.xml",
    "localization.xml",
    "input.xml",
)


def get_game_dir() -> tuple[Path, bool]:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return Path(config["game_dir"]), False

    print("Welcome! This appears to be your first time running this tool.")
    print("Please enter the path to your Witcher 3 game folder:")
    game_dir = Path(input("> ").strip())

    while True:
        if game_dir.exists() and (game_dir / XML_LOCATION).exists():
            break
        print(
            "Invalid path or game config folder not found. Please try again or type 'exit' to quit:"
        )
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            sys.exit(0)
        game_dir = Path(user_input)

    with open(CONFIG_FILE, "w") as f:
        json.dump({"game_dir": str(game_dir)}, f)
    print(f"Game path saved. You can change it by editing {CONFIG_FILE}")

    return game_dir, True


GAME_DIR, IS_FIRST_RUN = get_game_dir()
FULL_PATH = GAME_DIR / XML_LOCATION


def retrieve_xml_files() -> list[str]:
    output = []
    for file in os.listdir(FULL_PATH):
        full_path = os.path.join(FULL_PATH, file)
        if (
            os.path.isfile(full_path)
            and file not in EXCLUDED_FILES_XML
            and Path(file).suffix == ".xml"
        ):
            output.append(full_path)
    return output


def check_file_is_xml(filename: str) -> bool:
    return Path(filename).suffix == ".xml"


def change_display_name(input_: str, target: str) -> str:
    return input_.replace("Mods.", f"Mods.{target}.", 1)


def select_id_category():
    for i, id in enumerate(IDs2, 1):
        print(f"{i}. {id}")
    return IDs[int(input(f"Please select_id_category from 1 to {len(IDs)} > ")) - 1]


def get_original_mod_name(mod_display_name: str):
    output = []
    strings = mod_display_name.split(".")
    for s in strings:
        if s not in IDs:
            output.append(s)
    return ".".join(output)


def main():
    GAME_DIR, IS_FIRST_RUN = get_game_dir()
    FULL_PATH = GAME_DIR / XML_LOCATION
    BACKUP_DIR.mkdir(exist_ok=True)

    if not IS_FIRST_RUN:
        print(f"Game path loaded. You can change it by editing {CONFIG_FILE}")
    xml_files = retrieve_xml_files()

    print("founded modded xml files:")
    for i, file in enumerate(xml_files, 1):
        print(f"{i}. {file.split('/')[-1]}")
    mod_target_input = int(
        input(f"Please input your choice from 1 to {len(xml_files)}: ")
    )
    assert mod_target_input in range(1, len(xml_files) + 1), "invalid choice"
    mod_target_input -= 1
    mod_target = xml_files[mod_target_input]
    print("picked mod > " + xml_files[mod_target_input].split("/")[-1])
    with open(mod_target, "r") as f:
        data = f.read()
    soup = BeautifulSoup(data, "xml")
    groups = soup.find_all("Group")
    # print(groups[0].prettify())
    category = select_id_category()
    for g in groups:
        display_name = g["displayName"]
        # print("before > ", display_name)
        assert isinstance(display_name, str)
        g["displayName"] = change_display_name(
            get_original_mod_name(display_name), category
        )
        # print("after > ", g["displayName"])
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{Path(mod_target).name}.{timestamp}.bak"
    backup_path = BACKUP_DIR / backup_filename
    shutil.copy2(mod_target, backup_path)
    with open(mod_target, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Success, the original file has been backed up as {backup_path}")
