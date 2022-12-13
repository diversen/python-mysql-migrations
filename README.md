# python mysql migration

Simple python mysql migration tool.

It executes files in `migrations/up` and `migrations/down` directories.

## Install mysql-migration

    pip install mysql-migration


## Create migrations dir

    mkdir -p migrations/up migrations/down

Add SQL files into `migrations/up` and `migrations/down` directories.

E.g.: 
    
    migrations/up/0001.sql
    migrations/up/0002.sql
    migrations/down/0001.sql
    migrations/down/0002.sql

## Usage

```python
from mysql_migration import MySQLMigration

m = MySQLMigration(migration_dir='migrations', migration_file='.migration')
m.connect(host='localhost', user='root', password='password', database='mysql_migration_test')
m.migrate_up(2) # now version is 2
m.migrate_down(1) # now version is 1

m.migrate_down() # now version is 0
m.migrate_up() # now version is 2
```