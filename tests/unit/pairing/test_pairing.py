from click.testing import CliRunner

from pairing.cli import cli

PATH_APP = "./doc/Base2.csv"
PATH_REF = "./doc/Base1.csv"


def test_error_rule():
    """TODO:
    Test si rule existe pas
    """

    rules = "rule_doesnt_exist"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--path_ref",
            PATH_REF,
            "--path_app",
            PATH_APP,
            "--path_output",
            "output.csv",
            "--rules",
            rules,
        ],
    )
    assert result.exit_code == 2


def test_same_birthday_rule():
    """TODO:
    Test sur un filtre
    """
    rules = "same_birthday_rule"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--path_ref",
            PATH_REF,
            "--path_app",
            PATH_APP,
            "--path_output",
            "output.csv",
            "--rules",
            rules,
        ],
    )
    assert result.exit_code == 0


def test_all_filters():
    """TODO:
    Test sur tous les filtres
    """
    rules = (
        "same_birthday_rule,same_lastname_rule,"
        "same_firstname_rule,same_birthplace_rule"
    )
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--path_ref",
            PATH_REF,
            "--path_app",
            PATH_APP,
            "--path_output",
            "output.csv",
            "--rules",
            rules,
        ],
    )
    assert result.exit_code == 0


def test_fuzzy_rule():
    """TODO:
    Test fuzzy
    """
    rules = "fuzzy_lastname_rule,fuzzy_firstname_rule"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--path_ref",
            PATH_REF,
            "--path_app",
            PATH_APP,
            "--path_output",
            "output.csv",
            "--rules",
            rules,
        ],
    )
    assert result.exit_code == 0


def test_combine_filter_and_fuzzy_rule():
    """TODO:
    Test combination fuzzy et filtre
    """
    rules = "same_lastname_rule,fuzzy_firstname_rule"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--path_ref",
            PATH_REF,
            "--path_app",
            PATH_APP,
            "--path_output",
            "output.csv",
            "--rules",
            rules,
        ],
    )
    assert result.exit_code == 0


def test_inversion_name_rule():
    """TODO:
    Test inversion name
    """
    rules = "same_birthplace_rule,check_inversion_name_rule"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--path_ref",
            PATH_REF,
            "--path_app",
            PATH_APP,
            "--path_output",
            "output.csv",
            "--rules",
            rules,
        ],
    )
    assert result.exit_code == 0
