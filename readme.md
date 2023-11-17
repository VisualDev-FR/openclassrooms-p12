# Develop a secure back-end architecture with Python and SQL

This project involves implementing a Customer Relationship Management (CRM) application to manage events, contracts, and clients.

This application is developed in Python, with a MySQL database. Communication with the database is done through the [SQLAlchemy](https://docs.sqlalchemy.org/en/20/) ORM.

# Setting up the development environment

## Creating the virtual environment

1. Create the virtual environment
    ```
    python -m venv env
    ```

2. Activate the virtual environment
    ```
    env/Scripts/activate
    ```

3. Install Python packages with pip
    ```
    pip install -r requirements.txt
    ```

## Setting up the database:

1. Create a MySQL database named `epicevents`

2. Create a user in the DBMS (the username and password for this user will be saved in environment variables later)

3. Grant the following access to this user:
    - ALTER
    - CREATE
    - DELETE
    - DROP
    - INSERT
    - REFERENCES
    - SELECT
    - UPDATE

## Creating environment variables

Several environment variables are necessary to make the application work. (see the [``environ.py``](./controller/environ.py) file)

1. Database password
    ```
    set EPICEVENTS_PW <database_password>
    ```

2. Database username
    ```
    set EPICEVENTS_USER <database_username>
    ```

3. Secret key (for password hashing)
    ```
    set EPICEVENTS_SK <secret_key>
    ```

4. Sentry key for logging
    ```
    set SENTRY_KEY <sentry_key>
    ```

## Initializing the database <a name="database"></a>

1. Activate the virtual environment
    ```
    env/Scripts/activate
    ```

2. Launch the database initialization utility:
    ```
    python epicevents.py init
    ```

3. Enter the database password to run the script.

## Running the program

The application is implemented as a command-line interface with [click](https://click.palletsprojects.com/en/8.1.x/). To run the program and access the main commands, use the following command:

```
python epicevents.py
```

To access the documentation for a command, use the ``--help`` argument

Example:
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

## Running tests

1. Configure a test database named `epicevents_test`, referring to the [dedicated section](#database) with the same user and rights.

2. Run the tests
    ```
    python -m pytest
    ```