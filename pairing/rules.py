from pandas import DataFrame
from rapidfuzz import fuzz, process

from .typing import Row, Rule

__all__ = ("RULES",)


RULES = {}


def register_rule(func: Rule) -> Rule:
    """Register a callable as a rule.

    :param func: the callable to register
    :type func: Rule
    :return: return the untouched rule
    :rtype: Rule
    """
    RULES[func.__name__] = func
    return func


@register_rule
def same_birthday_rule() -> str:
    """TODO:

    :return: TODO:
    :rtype: str
    """
    return "date_naissance_norm"


@register_rule
def same_lastname_rule() -> str:
    """TODO:

    :return: TODO:
    :rtype: str
    """
    return "nom_norm"


@register_rule
def same_firstname_rule() -> str:
    """TODO:

    :return: TODO:
    :rtype: str
    """
    return "prenom_norm"


@register_rule
def same_birthplace_rule() -> str:
    """TODO:

    :return: TODO:
    :rtype: str
    """
    return "commune_naissance_norm"


@register_rule
def fuzzy_lastname_rule(ref_row: Row, lookup_df: DataFrame) -> bool:
    """TODO:

    :param ref_row: TODO:
    :type ref_row: Row
    :param lookup_df: TODO:
    :type lookup_df: DataFrame
    :return: TODO:
    :rtype: bool
    """
    lookup_df.reset_index()
    fuzzy_lastname = (
        x[2]
        for x in process.extract(
            ref_row.nom_norm, lookup_df["nom_norm"], score_cutoff=75
        )
    )
    return (
        lookup_df.loc[fuzzy_lastname] if fuzzy_lastname else lookup_df.loc[[]]
    )


@register_rule
def fuzzy_firstname_rule(ref_row: Row, lookup_df: DataFrame) -> bool:
    """TODO:

    :param ref_row: TODO:
    :type ref_row: Row
    :param lookup_df: TODO:
    :type lookup_df: DataFrame
    :return: TODO:
    :rtype: bool
    """
    lookup_df.reset_index()
    fuzzy_lastname = (
        x[2]
        for x in process.extract(
            ref_row.prenom_norm, lookup_df["prenom_norm"], score_cutoff=75
        )
    )
    return (
        lookup_df.loc[fuzzy_lastname] if fuzzy_lastname else lookup_df.loc[[]]
    )


@register_rule
def check_inversion_name_rule(ref_row: Row, lookup_df: DataFrame) -> bool:
    """TODO:

    :param ref_row: TODO:
    :type ref_row: Row
    :param lookup_df: TODO:
    :type lookup_df: DataFrame
    :return: TODO:
    :rtype: bool
    """
    lookup_df.reset_index()
    fuzzy_inverse = process.extractOne(
        ref_row.nom_prenom_norm,
        lookup_df["nom_prenom_norm"],
        score_cutoff=75,
        scorer=fuzz.token_set_ratio,
    )
    return (
        lookup_df.loc[[fuzzy_inverse[2]]]
        if fuzzy_inverse
        else lookup_df.loc[[]]
    )


@register_rule
def fuzzy_birthplace_rule(ref_row: Row, lookup_df: DataFrame) -> bool:
    """TODO:

    :param ref_row: TODO:
    :type ref_row: Row
    :param lookup_df: TODO:
    :type lookup_df: DataFrame
    :return: TODO:
    :rtype: bool
    """
    lookup_df.reset_index()
    fuzzy_birth = process.extractOne(
        str(ref_row.commune_naissance_norm),
        lookup_df["commune_naissance_norm"],
        score_cutoff=75,
        scorer=fuzz.token_set_ratio,
    )
    return (
        lookup_df.loc[[fuzzy_birth[2]]] if fuzzy_birth else lookup_df.loc[[]]
    )
