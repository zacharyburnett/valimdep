import sys
from pathlib import Path

import click
from valimdep.operations import dependency_import_discrepancies


@click.command()
@click.argument("directories", nargs=-1, type=Path, default=[Path.cwd()])
def valimdep(directories: list[Path]):
    for directory in directories:
        try:
            unimported_dependencies, undepended_imports = dependency_import_discrepancies(
                directory
            )
        except ValueError:
            continue

        if len(unimported_dependencies) > 0:
            click.echo(
                f"[{directory.name}] found {len(unimported_dependencies)} package dependencies not explicitly imported\n"
                + "\n".join(unimported_dependencies)
            )

        if len(undepended_imports) > 0:
            click.echo(
                f"[{directory.name}] found {len(undepended_imports)} explicit imports not listed in package dependencies\n"
                + "\n".join(undepended_imports)
            )


if __name__ == "__main__":
    sys.exit(valimdep())
