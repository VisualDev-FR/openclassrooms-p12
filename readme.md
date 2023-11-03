# Développez une architecture back-end sécurisée avec Python et SQL

Ce projet consiste à implémenter une application Customer Relationship Management (CRM) pour gérer des évenements, des contrats et des clients.

Cette application est développée en python, avec une base de données MySQL. La communication avec avec la base de données se fait au travers de l'ORM [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)


# Mise en place de l'environnement de developpement

## création de l'environnement virutel

1. Création de l'environnement virtuel
```
python -m venv env
```

2. Activation de l'environnement virtuel
```
env/Scripts/activate
```

3. Installation des packages python avec pip
```
pip install -r requirements.txt
```

## mise en place de la base de données:

1. créer une base de données mysql nommée `epicevents`

2. créer un utilisateur dans le SGBD (le nom et le mot de passe de cet utilisateur seront enregistrés dans des variables d'environnement ultérieurement)

3. Donner à cet utilisateur, les accès suivants:
    - ALTER
    - CREATE
    - DELETE
    - DROP
    - INSERT
    - REFERENCES
    - SELECT
    - UPDATE

## création des variables d'environnement

Plusieurs variables d'environnement son nécéssaires pour faire fonctionner l'application. (voir le fichier [``environ.py``](./controller/environ.py))

1. Le mot de passe de la base de donnée
```
set EPICEVENTS_PW <database_password>
```

2. Nom de l'utilisateur de la base de donnée
```
set EPICEVENTS_USER <database_username>
```

3. Secret key (pour le hachage des mots de passe)
```
set EPICEVENTS_SK <secret_key>
```

4. Clé Sentry pour la journalisation
```
set SENTRY_KEY <sentry_key>
```

## Initialisation de la base de donnée <a name="database"></a>

1. Activer l'environnement virtuel
```
env/Scripts/activate
```

2. Lancer l'utilitaire d'initialisation de la base de données:
```
python epicevents.py init
```

## Lancement du programme

L'application est implémentée en ligne de commande avec [click](https://click.palletsprojects.com/en/8.1.x/). Pour lancer le programme et accéder aux commandes principales, lancer la commande suivante:

```
python epicevents.py
```

Pour accéder à la documentation d'une commande utiliser l'argument ``--help``

Exemple:
```
python epicevents.py create employee --help
```

```
Usage: epicevents.py create employee [OPTIONS]

  Create a new employee

Options:
  --email TEXT                    The email of the employee  [required]
  --password TEXT                 The password of the employee  [required]
  --fullname TEXT                 The full name of the employee. sample :
                                  'FirstName, LastName'  [required]
  --department [sales|accounting|support]
                                  The department of the employee  [required]
  --help                          Show this message and exit.
```

## Lancement des tests

1. configuer une base de données de tests nommée `epicevents_test`, en vous référant à la [section dédiée](#database) avec le même utilisateur, les mêmes droits.

2. Lancer les tests

```
python -m pytest
```