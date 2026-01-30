from bs4 import BeautifulSoup
import shutil
import sys
from pathlib import Path


def check_file_is_xml(filename: str) -> bool:
    return Path(filename).suffix == ".xml"


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


def change_display_name(input_: str, target: str) -> str:
    return input_.replace("Mods.", f"Mods.{target}.", 1)


def select_id_category():
    for i, id in enumerate(IDs, 1):
        print(f"{i}. {id}")
    return IDs[int(input(f"Please select_id_category from 1 to {len(IDs)}")) - 1]


def main():
    assert len(sys.argv) > 1, "Error: Please provide the .xml file you want to edit"
    filename = sys.argv[1]
    assert check_file_is_xml(filename), (
        f"Error: Please provide correct .xml file you want to edit, current argument file is {filename}"
    )
    with open(filename, "r") as f:
        data = f.read()
    soup = BeautifulSoup(data, "xml")
    groups = soup.find_all("Group")
    category = select_id_category()
    for g in groups:
        display_name = g["displayName"]
        assert isinstance(display_name, str)
        g["displayName"] = change_display_name(display_name, category)
    shutil.move(filename, filename + ".bak")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"Success, the original file has been backed up as {filename + '.bak'}")


if __name__ == "__main__":
    main()
