"""Unittest templates for witcher3-modmenu-changer."""

import unittest


class TestStringLogic(unittest.TestCase):
    """Test config file path is relative to cwd."""

    def setUp(self) -> None:
        self.subject = "Mods.alchemy_and_equipment.characters.miscellaneous.characters.Appearances.SilverSwordSetting"
        self.original_mod = "Mods.Appearances.SilverSwordSetting"
        self.IDs = (
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
        return super().setUp()

    def test_separate_string(self):
        strings = self.subject.split(".")
        print(strings)
        expected_output = [
            "Mods",
            "alchemy_and_equipment",
            "characters",
            "miscellaneous",
            "characters",
            "Appearances",
            "SilverSwordSetting",
        ]
        self.assertEqual(strings, expected_output)

    def test_get_original_mod_name(self):
        output = []
        strings = self.subject.split(".")
        for s in strings:
            if s not in self.IDs:
                output.append(s)
        self.assertEqual(".".join(output), self.original_mod)


if __name__ == "__main__":
    unittest.main()
