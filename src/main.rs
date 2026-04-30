use std::env;
use std::ffi::OsStr;
use std::path::Path;

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
