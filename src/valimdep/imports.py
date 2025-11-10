from pathlib import Path

import findimports

__all__ = ["imports_from"]


def imports_from(directory: Path, tests: bool = False) -> set[str]:
    imports: set[str] = set()
    for filename in directory.glob("**.py"):
        is_test = filename.name.startswith("test_")
        if (tests and is_test) or (not tests and not is_test):
            imports.update(
                (
                    module.split(".")[0]
                    for module in findimports.ImportFinder(filename).imports
                )
            )
    return imports
