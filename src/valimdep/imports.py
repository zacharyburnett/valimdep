import ast
from pathlib import Path
from sys import stdlib_module_names

__all__ = ["imports_from"]

 
def imports_from(directory: Path, tests: bool = False) -> dict[str, list[Path]]:
    imports = {}
    for subdir in (
        subdir
        for subdir in directory.iterdir()
        if subdir.is_dir()
        and not subdir.name.startswith(".")
        and subdir.name not in ["dist", "build"]
    ):
        for filename in subdir.glob("**/*.py"):
            is_test = filename.name.startswith("test_")
            if (tests and is_test) or (not tests and not is_test):
                with open(filename, "r") as file:
                    lines = file.read()

                modules = set()
                for node in ast.walk(ast.parse(lines)):
                    if isinstance(node, ast.Import):
                        modules.update((module.name for module in node.names))
                    elif isinstance(node, ast.ImportFrom)and node.level == 0:
                        modules.add(node.module)

                for module in modules:
                    if module is not None:
                        module = module.split(".")[0]
                        if module not in stdlib_module_names:
                            if module not in imports:
                                imports[module] = []
                            imports[module].append(str(filename))
    return imports
