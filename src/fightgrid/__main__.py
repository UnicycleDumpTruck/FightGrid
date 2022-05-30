"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """FightGrid."""


if __name__ == "__main__":
    main(prog_name="FightGrid")  # pragma: no cover
