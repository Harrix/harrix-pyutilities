"""
CLI console removes the date from the names of folders and markdown files
and transfers it to yaml.

## Usage example

With arguments:

```console
python date_from_filename_to_yaml.py C:/test/2022
```

Without arguments:

```console
python date_from_filename_to_yaml.py
C:/test/2022
```

## Result

### Before

Folder structure:

```text
C:/test/2022
├─ 2022-04-16-test
│  ├─ 2022-04-16-test.en.md
│  ├─ 2022-04-16-test.md
│  ├─ featured-image.png
│  └─ img
│     └─ test.png
└─ 2022-04-17-test2
   ├─ 2022-04-17-test.md
   ├─ featured-image.png
   └─ img
      └─ test.png
```

File `C:/test/2022/2022-04-16-test/2022-04-16-test.en.md`:

```md
---
categories: [it, program]
---

# Test

![Test image](img/test.png)

```

### After

Folder structure:

```text
C:/test/2022
├─ test
│  ├─ featured-image.png
│  ├─ img
│  │  └─ test.png
│  ├─ test.en.md
│  └─ test.md
└─ test2
   ├─ featured-image.png
   ├─ img
   │  └─ test.png
   └─ test.md
```

File `C:/test/2022/test/test.en.md`:

```md
---
data: 2022-04-16
categories: [it, program]
---

# Test

![Test image](img/test.png)

```
"""
import argparse
import os
import re
from pathlib import Path


def rename_file(file: Path):
    if file.is_file():
        pattern = r"^(\d{4}-\d{2}-\d{2})-(.*)\.md$"
        res = re.match(pattern, file.name)
        if bool(res):
            lines = file.read_text(encoding="utf8").splitlines()
            lines[0] = f"---\ndata: {res.group(1)}"
            file.write_text("\n".join(lines) + "\n", encoding="utf8")

            new_filename = f"{res.group(2)}.md"
            os.rename(file.parent / file.name, file.parent / new_filename)
            print(f"File '{file.parent / file.name}' renamed.")


def rename_dir(dir: Path):
    if dir.is_dir() and dir.name[0] != ".":
        pattern = r"^\d{4}-\d{2}-\d{2}-(.*)$"
        res = re.match(pattern, dir.name)
        if bool(res):
            new_filename = res.group(1)
            os.rename(dir.parent / dir.name, dir.parent / new_filename)
            print(f"Dir '{dir.parent / dir.name}' renamed.")


def date_from_filename_to_yaml(path: str) -> None:
    for child_dir in Path(path).iterdir():
        if child_dir.name[0] != ".":
            for file in Path(child_dir).glob("**/*"):
                rename_file(file)
    for child_dir in Path(path).iterdir():
        if child_dir.name[0] != ".":
            for dir in Path(child_dir).glob("**/*"):
                rename_dir(dir)
    for child_dir in Path(path).iterdir():
        rename_dir(child_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove the date from the names of folders and markdown files "
        "and transfers it to yaml. See docstring for more information."
    )
    parser.add_argument(
        "path", type=str, nargs='?', help="path of the folder with markdown files"
    )

    args = parser.parse_args()
    if args.path is not None and Path(args.path).is_dir():
        date_from_filename_to_yaml(args.path)
    else:
        path = input("Input path: ")
        if Path(path).is_dir():
            date_from_filename_to_yaml(path)
        else:
            print("Invalid path.")