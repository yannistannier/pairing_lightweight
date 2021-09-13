import time

from datetime import datetime
from typing import Any, Callable, Collection, Generic, TypeVar

import numpy as np
import pandas as pd

from pairing.typing import Rule

pd.options.mode.chained_assignment = None

__all__ = ("PairingParser",)


T = TypeVar("T")  # pylint: disable=invalid-name


def timeit(func: Callable) -> Callable:
    """TODO:

    :param func: TODO:
    :type func: Callable
    :return: TODO:
    :rtype: Callable
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """TODO:

        :param args: TODO:
        :type args: Any
        :param kwargs: TODO:
        :type kwargs: Any
        :return: TODO:
        :rtype: Any
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        print(">>", func.__name__, round(time.time() - start_time, 4), "sec")
        return result

    return wrapper


class PairingParser(Generic[T]):
    """TODO:"""

    def __init__(self, path_ref: str, path_lookup: str) -> None:
        """TODO:

        :param path_ref: TODO:
        :type path_ref: str
        :param path_lookup: TODO:
        :type path_lookup: str
        """
        self.reference = pd.read_csv(path_ref)
        self.lookup = pd.read_csv(path_lookup)
        self.matching = []

    @timeit
    def preprocessing_dataframe(self) -> None:
        """TODO:"""
        # On normalise le champs date de naissance / Complexite : O(n)
        self.reference["date_naissance_norm"] = pd.to_datetime(
            self.reference["date_naissance"],
            infer_datetime_format=True,
            errors="coerce",
        )
        self.lookup["date_naissance_norm"] = pd.to_datetime(
            self.lookup["Date de naissance"],
            format="%d/%m/%Y",
            exact=False,
            infer_datetime_format=True,
            dayfirst=True,
        )

        # On normalise les champs nom et prenom
        self.reference["nom_norm"] = self.reference["nom"].apply(
            lambda x: str(x).lower()
        )
        self.reference["prenom_norm"] = self.reference["prénoms"].apply(
            lambda x: str(x).lower()
        )

        self.lookup["nom_norm"] = np.where(
            ~self.lookup["Nom de naissance"].isnull(),
            self.lookup["Nom de naissance"].str.lower(),
            self.lookup["Nom d’usage"].str.lower(),
        )
        self.lookup["prenom_norm"] = self.lookup["Prénoms"].apply(
            lambda x: str(x).lower()
        )

        # On normalise le champs commune naissance
        self.reference["commune_naissance_norm"] = self.reference[
            "commune_naissance"
        ].apply(lambda x: str(x).lower())
        self.lookup["commune_naissance_norm"] = self.lookup[
            "Commune de naissance "
        ].apply(lambda x: str(x).lower())

        # On cree un champ prenom - nom pour la verification des inversions
        self.reference["nom_prenom_norm"] = (
            self.reference["nom_norm"] + " " + self.reference["prenom_norm"]
        )
        self.lookup["nom_prenom_norm"] = (
            self.lookup["nom_norm"] + " " + self.lookup["prenom_norm"]
        )

    @timeit
    def parse(self, rules: Collection[Rule]) -> None:
        """TODO:

        :param rules: TODO:
        :type rules: TODO:
        """
        filters, fuzzy, _ = rules

        merge = [rule() for rule in filters]
        if merge:
            self.reference = pd.merge(
                self.lookup[["Id", *merge]],
                self.reference,
                on=merge,
                how="inner",
            )

        if fuzzy:
            for row in self.lookup.itertuples():
                matching = (
                    self.reference[self.reference["Id"].values == row.Id]
                    if merge
                    else self.reference
                )
                if len(matching) == 0:
                    for rule in fuzzy:
                        matching = rule(row, matching)
                self.matching.extend(
                    [(row.Id, x) for x in matching["id_certificat"]]
                )
        else:
            self.matching = [
                (row.Id, row.id_certificat)
                for row in self.reference.itertuples()
            ]

    @timeit
    def save_pairing(self, path_output: str, rules: Collection[Rule]) -> None:
        """TODO:

        :param path_output: TODO:
        :type path_output: str
        :param rules: TODO:
        :type rules: TODO:
        """
        file = pd.DataFrame(self.matching, columns=["Id base 2", "Id base 1"])
        file["Date calcul"] = datetime.now()
        file["Regles"] = ",".join(list(rules[2]))
        file.to_csv(path_output, index=False)
