// use serde_json;
use std::env;
use std::fs;
use std::path::Path;
// use std::ffi::OsStr;
use std::path::{self, PathBuf};

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

const EXCLUDED_FILES_XML: [&str; 11] = [
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
];

fn check_file_is_xml(filename: &str) -> bool {
    Path::new(filename)
        .extension()
        .map(|e| e == "xml")
        .unwrap_or(false)
}

/// Change display name for mod entries
/// Replaces the first occurrence of "Mods." with "Mods.{target}."
pub fn change_display_name(input_: &str, target: &str) -> String {
    if !input_.contains("Mods.") {
        return input_.to_string();
    }

    let (before_mods, rest) = input_.split_once("Mods.").expect("Found 'Mods.' marker");
    format!("{}Mods.{}{}", before_mods, target, rest)
}

/// Retrieve all XML files in directory, excluding excluded files.
fn retrieve_xml_files(full_path: impl AsRef<Path>) -> Vec<String> {
    let path = full_path.as_ref();
    let mut output = Vec::new();

    if !path.exists() || !path.is_dir() {
        return output;
    }

    for entry in fs::read_dir(path).expect("Failed to read directory") {
        let entry = match entry {
            Ok(e) => e,
            Err(_) => continue,
        };
        let file_path = entry.path();

        if file_path.is_file() && file_path.extension().map_or(false, |ext| ext == "xml") {
            // Filter exclusions by filename match
            let filename = match file_path.file_name() {
                Some(name) => name.to_string_lossy().to_lowercase(),
                None => continue,
            };

            if EXCLUDED_FILES_XML
                .iter()
                .any(|&excluded| filename == excluded)
            {
                continue;
            }

            output.push(file_path.to_string_lossy().to_string());
        }
    }

    output
}

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
    let xml_location = Path::new(
        "/media/KAIZEN/The Witcher 3 Wild Hunt GOTY/bin/config/r4game/user_config_matrix/pc",
    );

    let xml_files = retrieve_xml_files(xml_location);
    dbg!(xml_files);
    // println!("{}", config_file.display());
    // println!("{}", backup_dir.display());
}
