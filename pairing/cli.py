from typing import List

import click

from .param_types import RulesParamType
from .parser import PairingParser
from .typing import Rule

__all__ = ("cli",)


@click.command()
@click.option(
    "--path_ref",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    required=True,
    help="TODO:",
)
@click.option(
    "--path_app",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
    required=True,
    help="TODO:",
)
@click.option(
    "--path_output",
    type=click.Path(dir_okay=False, resolve_path=True),
    required=True,
    help="TODO:",
)
@click.option("--rules", type=RulesParamType(), required=True)
def cli(
    path_ref: str, path_app: str, path_output: str, rules: List[Rule]
) -> None:
    """TODO:

    \f
    :param path_ref: TODO:
    :type path_ref: str
    :param path_app: TODO:
    :type path_app: str
    :param path_output: TODO:
    :type path_output: str
    :param rules: TODO:
    :type rules: TODO:
    """
    pairing = PairingParser(path_ref, path_app)
    pairing.preprocessing_dataframe()
    pairing.parse(rules)
    pairing.save_pairing(path_output, rules)
