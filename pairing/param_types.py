from typing import List

import click

from .rules import RULES
from .typing import Rule

__all__ = ("RulesParamType",)

_RULES_HIERARCHY = {
    # hierarchy
    "check_inversion_name_rule": [
        "same_lastname_rule",
        "same_firstname_rule",
        "fuzzy_lastname_rule",
        "fuzzy_firstname_rule",
    ],
    "fuzzy_firstname_rule": ["same_firstname_rule"],
    "fuzzy_lastname_rule": ["same_lastname_rule"],
    # group
    "filters": [
        "same_birthday_rule",
        "same_lastname_rule",
        "same_firstname_rule",
        "same_birthplace_rule",
    ],
    "fuzzy": [
        "fuzzy_lastname_rule",
        "fuzzy_firstname_rule",
        "check_inversion_name_rule",
        "fuzzy_birthplace_rule",
    ],
}


def filters_rules(rule_names: List) -> List:
    """TODO:

    :param rule_names: TODO:
    :type rule_names: Callable
    :return: TODO:
    :rtype: list
    """

    for key, rules in _RULES_HIERARCHY.items():
        if key in rule_names:
            for rule in rules:
                if rule in rule_names:
                    rule_names.remove(rule)
    return rule_names


class RulesParamType(click.ParamType):
    """TODO:"""

    name = "rules"

    def convert(
        self, value: str, param: click.Option, ctx: click.Context
    ) -> List[Rule]:
        """TODO:

        :param value: TODO:
        :type value: str
        :param param: TODO:
        :type param: click.Option
        :param ctx: TODO:
        :type ctx: click.Context
        :return: TODO:
        :rtype: TODO:
        """
        if not value:
            return []

        rule_names = sorted(set(value.split(",")), reverse=True)
        rule_names = filters_rules(rule_names)

        filters, fuzzy, invalid = [], [], []
        for rule_name in rule_names:
            if rule := RULES.get(rule_name):
                if rule_name in _RULES_HIERARCHY["filters"]:
                    filters.append(rule)
                elif rule_name in _RULES_HIERARCHY["fuzzy"]:
                    fuzzy.append(rule)
            else:
                invalid.append(rule_name)

        if invalid:
            self.fail(f"{', '.join(invalid)} is not a valid rules", param, ctx)

        return filters, fuzzy, rule_names
