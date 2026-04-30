use std::env;
// use std::ffi::OsStr;
// use std::path::Path;

const IDS: [&str; 9] = [
    "alchemy_and_equipment",
    "camera",
    "characters",
    "combat",
    "gameplay",
    "quests_and_adventures",
    "user_interface",
    "visuals_and_graphics",
    "miscellaneous",
];

const IDS2: [&str; 9] = [
    "Alchemy and Equipment",
    "Camera",
    "Characters",
    "Combat",
    "Gameplay",
    "Quests and Adventures",
    "User Interface",
    "Visuals and Graphics",
    "Miscellaneous",
];

fn main() {
    // CONFIG_FILE = Path.cwd() / ".witcher3_modmenu_config.json"
    // XML_LOCATION = Path("bin/config/r4game/user_config_matrix/pc")
    // BACKUP_DIR = Path.cwd() / "backup"

    let config_file = env::current_dir()
        .expect("Get the current working directory")
        .join(".witcher3_modmenu_config.json");

    let backup_dir = env::current_dir()
        .expect("Get the backup directory")
        .join("backup");

    println!("Hello, world!");
    // println!("{}", config_file.display());
    // println!("{}", backup_dir.display());
}
