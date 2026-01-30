Yep 🙂 I can do that. Below are **faithful, idiomatic conversions** of your script into **Go** and **Rust**. Both versions:

* Read an XML file from `argv[1]`
* Parse `<Group displayName="...">`
* Ask the user to select a category
* Replace the first `"Mods."` with `"Mods.<category>."`
* Rename the original file to `.bak`
* Write the modified XML back

---

## ✅ Go version

**Dependencies**

```bash
go get github.com/beevik/etree
```

**Code**

```go
package main

import (
 "bufio"
 "fmt"
 "os"
 "path/filepath"
 "strconv"
 "strings"

 "github.com/beevik/etree"
)

var IDs = []string{
 "alchemy_and_equipment",
 "camera",
 "characters",
 "combat",
 "gameplay",
 "quests_and_adventures",
 "user_interface",
 "visuals_and_graphics",
 "miscellaneous",
}

func changeDisplayName(input, target string) string {
 return strings.Replace(input, "Mods.", "Mods."+target+".", 1)
}

func selectIDCategory() string {
 for i, id := range IDs {
  fmt.Printf("%d. %s\n", i+1, id)
 }

 fmt.Printf("Please select_id_category from 1 to %d: ", len(IDs))
 reader := bufio.NewReader(os.Stdin)
 text, _ := reader.ReadString('\n')
 choice, err := strconv.Atoi(strings.TrimSpace(text))
 if err != nil || choice < 1 || choice > len(IDs) {
  panic("invalid selection")
 }
 return IDs[choice-1]
}

func main() {
 if len(os.Args) < 2 {
  panic("missing filename")
 }
 filename := os.Args[1]

 doc := etree.NewDocument()
 if err := doc.ReadFromFile(filename); err != nil {
  panic(err)
 }

 category := selectIDCategory()

 for _, g := range doc.FindElements("//Group") {
  if attr := g.SelectAttr("displayName"); attr != nil {
   attr.Value = changeDisplayName(attr.Value, category)
  }
 }

 bak := filename + ".bak"
 if err := os.Rename(filename, bak); err != nil {
  panic(err)
 }

 doc.Indent(2)
 if err := doc.WriteToFile(filepath.Clean(filename)); err != nil {
  panic(err)
 }
}
```

---

## 🦀 Rust version

**Dependencies (`Cargo.toml`)**

```toml
[dependencies]
roxmltree = "0.19"
xmltree = "0.10"
```

**Code**

```rust
use std::env;
use std::fs;
use std::io::{self, Write};

use xmltree::{Element, XMLNode};

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

fn change_display_name(input: &str, target: &str) -> String {
    input.replacen("Mods.", &format!("Mods.{}.", target), 1)
}

fn select_id_category() -> &'static str {
    for (i, id) in IDS.iter().enumerate() {
        println!("{}. {}", i + 1, id);
    }

    print!(
        "Please select_id_category from 1 to {}: ",
        IDS.len()
    );
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let choice: usize = input.trim().parse().expect("invalid number");

    IDS[choice - 1]
}

fn main() {
    let filename = env::args().nth(1).expect("missing filename");

    let data = fs::read_to_string(&filename).expect("failed to read file");
    let mut root = Element::parse(data.as_bytes()).expect("invalid XML");

    let category = select_id_category();

    fn walk(elem: &mut Element, category: &str) {
        if elem.name == "Group" {
            if let Some(value) = elem.attributes.get_mut("displayName") {
                *value = change_display_name(value, category);
            }
        }
        for child in elem.children.iter_mut() {
            if let XMLNode::Element(e) = child {
                walk(e, category);
            }
        }
    }

    walk(&mut root, category);

    fs::rename(&filename, format!("{}.bak", filename)).unwrap();
    fs::write(&filename, root.to_string()).unwrap();
}
```

---

If you want:

* **no interactive prompt** (CLI flags instead),
* **better XML formatting preservation**, or
* **a version without third-party crates/libs**

just tell me which language and style you prefer 👍
