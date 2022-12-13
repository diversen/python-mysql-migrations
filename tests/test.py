import sys
sys.path.append(".")

import unittest

from mysql_migrations import MySQLMigrations

class TestMySQLMigration(unittest.TestCase):

    
    def test_versions(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')

        latest_version = m.get_latest_version()
        self.assertEqual(latest_version, 3)

        m.set_current_version(0)
        
        version = m.get_current_version()
        self.assertEqual(version, 0)

        m.set_current_version(1)
        version = m.get_current_version()
        self.assertEqual(version, 1)

        m.set_current_version(0)
        version = m.get_current_version()
        self.assertEqual(version, 0)

    def test_files(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')

        up_files = m.get_migration_files('up')
        self.assertEqual(up_files, ['0001.sql', '0002.sql', '0003.sql'])

        down_files = m.get_migration_files('up')
        self.assertEqual(down_files, ['0001.sql', '0002.sql', '0003.sql'])

        sql_statments = m.get_sql_statements_from_file('./tests/migrations/up/0001.sql')
        self.assertEqual(len(sql_statments), 4)
        self.assertEqual(sql_statments[0], "DROP TABLE IF EXISTS `table_1_a`")

    def test_get_up_files(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')

        m.set_current_version(0)
        up_files = m.get_up_files(2)
        
        self.assertEqual(['0001.sql', '0002.sql'], up_files)

        m.set_current_version(2)
        up_files = m.get_up_files(3)
        self.assertEqual(['0003.sql'], up_files)
                

    def test_get_down_files(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')

        m.set_current_version(3)
        down_files = m.get_down_files(1)

        self.assertEqual(['0003.sql', '0002.sql'], down_files)

    def test_get_migrate_up_statements(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')

        m.set_current_version(0)
        statements = m.get_migrate_up_statements(2)

        self.assertEqual(len(statements), 6)
        self.assertEqual(statements[0], "DROP TABLE IF EXISTS `table_1_a`")

    def test_get_migrate_down_statements(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')

        m.set_current_version(3)
        statements = m.get_migrate_down_statements(1)

        self.assertEqual(len(statements), 2)
        self.assertEqual(statements[0], "DROP TABLE IF EXISTS `table_3`")

    def get_current_tables(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')
        m.connect(host='localhost', user='root', password='password', database='mysql_migration_test')
        m.execute_query('SHOW TABLES')
        tables = m.cursor.fetchall()
        return tables

        
    def test_migrate(self):
        m = MySQLMigrations(migration_dir='tests/migrations', migration_file='tests/.migration')
        m.connect(host='localhost', user='root', password='password', database='mysql_migration_test')

        m.set_current_version(0)
        
        m.migrate_up(2)
        self.assertEqual(self.get_current_tables(), [('table_1_a',), ('table_1_b',), ('table_2',)])
        
        m.migrate_up()
        self.assertEqual(self.get_current_tables(), [('table_1_a',), ('table_1_b',), ('table_2',), ('table_3',)])

        m.migrate_down(2)
        self.assertEqual(self.get_current_tables(), [('table_1_a',), ('table_1_b',), ('table_2',)])

        m.migrate_down(0)
        self.assertEqual(self.get_current_tables(), [])

        m.migrate_up()
        self.assertEqual(self.get_current_tables(), [('table_1_a',), ('table_1_b',), ('table_2',), ('table_3',)])
        
        current_version = m.get_current_version()
        self.assertEqual(current_version, 3) 

        m.migrate_down()
        self.assertEqual(self.get_current_tables(), [])

        


if __name__ == '__main__':
    unittest.main()

