# Exercice 1 : Pairing

# Description 

Pairing est une librairie permettant l'appareillement entre deux bases de données de personnes décédées.
Pour cela, il prend en entrée 2 csv, une série de règles et essaye de faire de la correspondance sur les identités le mieux possibles.
Pairing s'appuie le plus possible sur les fonctions de vectorization avec des séries Pandas ou des Numpy array pour une efficacité maximale.


# Features

- [x] Exact Recherche sur nom / prénom / date de naissance
- [x] Fuzzy Recherche sur nom / prénom / commune de naissance via rapidfuzz (Levenshtein Distance)
- [x] Verification d'inversion du nom / prénom dans la base de données
- [x] Export des résultats dans un CSV

**To do :**
-  Approximation recherche sur des TF-IDF via calcul de distance
-  Comptabilité avec Spark pour une meilleure montée à l'échelle.
-  Utiliser un transformer (Bert) afin d'extraire une signature (embedding) pour chaque nom / prénom / commun de naissance afin d'exécuter des calculs de distance et faire un matching fuzzy scalable 



# Requirements

- Uunbu / macOS / Windows
- Pythonn 3

Pairing tire les dépendances suivantes:
- rapidfuzz
- pandas
- numpy
- click


# Installation

Via pip :
```
pip install -r requirements.txt
```


# Usage

## Execution :

```
python -m pairing --path_ref path/to/base1.csv --path_app path/to/base2.csv  --path_output output.csv --rules rules
```

**List des arguments :**
```
--path_ref : emplacement du premier csv
--path_app : emplacement du second csv
--path_output: emplacement du fichier de sortie
--rules: Liste des règles séparées par une virgule (ex: same_firstname_rule,same_lastname_rule,same_birthplace_rule )
```

# Liste des strategies disponible :

## Correspondance Exacte (filtre):

Ces règles permettent d'exécuter des correspondances exactes entre les deux bases de données.
Cependant la correspondance n'est pas sensible à la casse, mais elle l'est sur les caractères spéciaux tels que les accents.

- same_lastname_rule : Correspondance sur le nom
- same_firstname_rule : Correspondance sur le nom
- same_birthplace_rule : Correspondance sur la commune de naissance
- same_birthday_rule : Correspondance sur la date de naissance

Ps : Concernant la date de naissance, les champs ont été normalisés et transformés en format datatime dans les deux bases de données.

## Correspondance Flou (fuzzy) :

Ces règles permettent d'exécuter des correspondances dites fuzzy (ou "floue") entre des champs des deux bases de données. La correspondance se fait via des distances de Levenshtein entre les mots.

Ainsi, les fautes de frappe / accents peuvent être traitées :
```
josé = jose
belchador = belchiador 
```

**Attention** : Malgré l'utilisation de RapidFuzz ( une librairie ultra rapide de matching de chaines de caractères, écrit pratiquement qu'en C++ et implémentant de nombreuses optimisations), une recherche fuzzy peut être très lente si elle est faite sur une large base de données.

**Il est recommandé de toujours effectuer une ou plusieurs Recherches Exact avant une recherche floue afin de réduire la taille de la base de données à parcourir**

- fuzzy_lastname_rule : Correspondance floue sur le nom
- fuzzy_firstname_rule : Correspondance floue sur le prenom
- fuzzy_birthplace_rule : Correspondance floue sur la commune de naissance
- check_inversion_name_rule : Correspondance floue en alternant Nom / Prenom (au cas d'une inversion de saisie dans le nom et le prénom)

# Exemple :
- Recherche en filtrant sur la date de naissance et en effectuer une recherche floue sur le nom :

```
python -m pairing --path_ref doc/Base1.csv --path_app doc/Base2.csv --path_output output.csv --rules same_birthday_rule,fuzzy_lastname_rule
```


# Test unitaire et vérification du style python pep8

- Pour exécuter les tests unitaires :
```
make test
```
ou

```
pytest tests/unit --junitxml=reports/report_unit_tests.xml
```


- Pour exécuter les tests python (pep8):
```
make style
```

ou
```
pylint --reports=n --rcfile=pylintrc pairing tests
```
