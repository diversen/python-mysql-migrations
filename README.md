# python mysql migration

Simple Python MySQL migration tool.

It executes files with SQL statements in e.g. `migrations/up` and `migrations/down` directories. 

The main usage is probably if you don't use a ORM, but query the MySQL database directly - maybe using `mysql.connector`.

## Install mysql-migration

    pip install git+https://github.com/diversen/python-mysql-migrations

Or using a tag:

    pip install git+https://github.com/diversen/python-mysql-migrations@v0.0.1

## Create migrations dir

    mkdir -p migrations/up migrations/down

Add SQL files into `migrations/up` and `migrations/down` directories, which will then be executed.

E.g.: 
    
    migrations/up/0001.sql
    migrations/up/0002.sql
    migrations/down/0001.sql
    migrations/down/0002.sql

## Usage

```python
from mysql_migrations import MySQLMigrations

# The 'migration_file' should be in a .gitignore file if using git
# This file holds the current version of the database
m = MySQLMigrations(migration_dir='migrations', migration_file='.migration')
m.connect(host='localhost', user='root', password='password', database='mysql_migration_test')

# Executes 0001.sql and 0002.sql The .migration version is 2
m.migrate_up(2) 

# Excutes 0002.sql. Now version the .migration version is 1
m.migrate_down(1) 

# 0002.sql is executed. The version .migration is 2
m.migrate_up()

# Executes 0002.sql and then 0001.sql, The .migration version is 0
m.migrate_down() 

# Get current version
m.get_current_version() # -> 0

```

## Tests

The test uses a docker container with MySQL and a database named 'mysql_migration_test'.
    
These a the connection parameters:

```python
m = MySQLMigrations(migration_dir='migrations', migration_file='.migration')
m.connect(host='localhost', user='root', password='password', database='mysql_migration_test')
```

To run the tests:

    python -m unittest discover -s tests
    

## License

[MIT](LICENSE)