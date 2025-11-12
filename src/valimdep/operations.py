import re
import tomllib
from pathlib import Path

from valimdep.imports import imports_from

__all__ = ["dependency_import_discrepancies"]


def dependency_import_discrepancies(
    directory: Path, tests: bool = False
) -> tuple[list[str], dict[str, list[Path]]]:
    """
    list unimported dependencies (dependencies that are not explicitly imported in the source code)
    and undepended imports (explicit imports in the source code that are not included in the package dependencies), respectively

    NOTE: this assumes that the package name and module name are the same, which is NOT always the case
    """
    filename = directory / "pyproject.toml"

    imported_modules = imports_from(directory, tests=tests)

    depended_modules = []
    with open(filename, "rb") as pyproject_toml:
        metadata = tomllib.load(pyproject_toml)
        if "project" in metadata:
            constraint = re.compile("[><=@]")
            for dependency in (
                metadata["project"]["dependencies"]
                if not tests
                else metadata["project"]["extras"]["tests"]
            ):
                # TODO package names are NOT always the same as importable module names; lookup from PyPI
                module_name = (
                    re.split(constraint, dependency)[0].strip().replace("-", "_")
                )

                depended_modules.append(module_name)
        else:
            raise ValueError(f"project does not conform to PEP621: {directory}")

    return [
        module_name
        for module_name in depended_modules
        if module_name not in imported_modules
    ], {
        module_name: paths
        for module_name, paths in imported_modules.items()
        if module_name not in depended_modules
    }
