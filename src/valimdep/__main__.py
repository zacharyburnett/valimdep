import sys
from pathlib import Path

import click
from valimdep.operations import dependency_import_discrepancies


@click.command()
@click.argument("directory", type=Path, default=Path.cwd())
@click.option("--ignore", type=str, multiple=True)
@click.option("--ignore-path", type=str, multiple=True)
@click.option("--tests-extra", type=str, default=None)
@click.option("--show-import-paths", is_flag=True)
def valimdep(
    directory: Path,
    ignore: list[str] = [],
    ignore_path: list[str] = [],
    tests_extra: bool = False,
    show_import_paths: bool = False,
):
    unimported_dependencies, undepended_imports = dependency_import_discrepancies(
        directory,
        ignore=list(ignore),
        ignore_paths=list(ignore_path),
        tests_extra=tests_extra,
    )

    if len(unimported_dependencies) > 0:
        click.echo(
            f"[{directory.name}] found {len(unimported_dependencies)} package dependencies not explicitly imported\n"
            + "\n".join(unimported_dependencies)
        )

    if len(undepended_imports) > 0:
        click.echo(
            f"[{directory.name}] found {len(undepended_imports)} explicit imports not listed in package dependencies\n"
            + "\n".join(
                (
                    f"{undepended_import} {paths}"
                    for undepended_import, paths in undepended_imports.items()
                )
                if show_import_paths
                else undepended_imports
            )
        )


if __name__ == "__main__":
    sys.exit(valimdep())
