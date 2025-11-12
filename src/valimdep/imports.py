import ast
from pathlib import Path
from sys import stdlib_module_names

__all__ = ["imports_from"]


def imports_from(
    directory: Path,
    ignore: list[str] = [],
    ignore_paths: list[str] = [],
    tests: bool = False,
) -> dict[str, list[Path]]:
    ignore.append(directory.name)
    ignore_paths.extend(("dist", "build"))

    imports = {}
    for subdir in (
        subdir
        for subdir in directory.iterdir()
        if subdir.is_dir()
        and not subdir.name.startswith(".")
        and str(subdir.relative_to(directory)) not in ignore_paths
    ):
        for filename in subdir.glob("**/*.py"):
            is_test = (
                filename.parent.name == "tests"
                or filename.name.startswith("test_")
                or filename.name == "conftest.py"
            )
            if (tests and is_test) or (not tests and not is_test):
                if not any(dir in str(filename) for dir in ignore_paths):
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
                                and module_name not in ignore
                            ):
                                if module_name not in imports:
                                    imports[module_name] = []
                                imports[module_name].append(
                                    str(filename.relative_to(directory))
                                )
    return imports
