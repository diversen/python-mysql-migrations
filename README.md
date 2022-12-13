# python mysql migration

Simple python mysql migration tool.

It executes files with SQL statements in a e.g. `migrations/up` and `migrations/down` directories. 

The main usage is probably to use it if you don't use a ORM, but query the MySQL database directly - maybe using `mysql.connector`.

## Install mysql-migration

    pip install mysql-migration


## Create migrations dir

    mkdir -p migrations/up migrations/down

Add SQL files into `migrations/up` and `migrations/down` directories which can be executed by `mysql`.

E.g.: 
    
    migrations/up/0001.sql
    migrations/up/0002.sql
    migrations/down/0001.sql
    migrations/down/0002.sql

## Usage

```python
from mysql_migrations import MySQLMigrations

m = MySQLMigration(migration_dir='migrations', migration_file='.migration')
m.connect(host='localhost', user='root', password='password', database='mysql_migration_test')
m.migrate_up(2) # now version is 2
m.migrate_down(1) # now version is 1

m.migrate_down() # now version is 0
m.migrate_up() # now version is 2
```

## License

[MIT](LICENSE)