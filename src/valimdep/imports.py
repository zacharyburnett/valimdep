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
        and subdir.name not in ["dist", "build", "docs"]
    ):
        directory_names = [node[0].name for node in subdir.walk()]

        for filename in subdir.glob("**/*.py"):
            is_test = filename.name.startswith("test_")
            if (tests and is_test) or (not tests and not is_test):
                with open(filename, "r") as file:
                    lines = file.read()

                module_names = set()
                for node in ast.walk(ast.parse(lines)):
                    if isinstance(node, ast.Import):
                        module_names.update((module.name for module in node.names))
                    elif isinstance(node, ast.ImportFrom) and node.level == 0:
                        module_names.add(node.module)

                for module_name in module_names:
                    if module_name is not None:
                        module_name = module_name.split(".")[0]
                        if (
                            module_name not in stdlib_module_names
                            and module_name not in directory_names
                        ):
                            if module_name not in imports:
                                imports[module_name] = []
                            imports[module_name].append(str(filename))
    return imports
