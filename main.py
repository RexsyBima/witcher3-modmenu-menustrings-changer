from bs4 import BeautifulSoup
import shutil

import sys

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
    filename = sys.argv[1]
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


if __name__ == "__main__":
    main()
