from mysql.connector import connect, cursor, Error
from os.path import exists
import os


class MySQLMigration:
    def __init__(self, migration_dir=None, migration_file=None):
        self.migration_dir = 'migrations'
        self.migration_file = '.migration'
        self.connection = None

        if migration_dir:
            self.migration_dir = migration_dir

        if migration_file:
            self.migration_file = migration_file

    def connect(self, *args, **kwargs) -> None:

        self.connection = connect(*args, **kwargs)
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def get_version_from_file(self, file) -> int:
        return int(file.split('.')[0])

    def get_current_version(self) -> int:
        """ Get current version from migration file"""
        if not exists(self.migration_file):
            return 0

        with open(self.migration_file, 'r') as f:
            return int(f.read())

    def set_current_version(self, version) -> None:
        """ Set current version in migration file"""

        if not version:
            if exists(self.migration_file):
                os.remove(self.migration_file)
                return

        with open(self.migration_file, 'w') as f:
            if not version:
                version = 0
            f.write(str(version))

    def get_migration_files(self, direction: str) -> list:

        files = os.listdir(self.migration_dir + '/' + direction)
        files.sort()

        return files

    def get_sql_statements_from_file(self, file: str) -> list:
        with open(file, 'r') as f:
            statements = f.read().split(';')
            statements = [s for s in statements if s.strip() != '']
            return statements

    def get_up_files(self, target_version=None) -> list:
        """ Get all up files from current version to target version"""
        current_version = self.get_current_version()
        if not target_version:
            target_version = self.get_latest_version()

        files = self.get_migration_files('up')
        files_to_run = []
        for file in files:
            version = self.get_version_from_file(file)
            if version > current_version and version <= target_version:
                files_to_run.append(file)
        
        return files_to_run


        # return files[current_version:target_version]

    def get_down_files(self, target_version=None) -> list:
        """ Get all down files from current version to target version in reverse order"""
        if not target_version:
            target_version = 0

        current_version = self.get_current_version()
        files_to_run = []
        files = self.get_migration_files('down')
        for file in files:
            version = self.get_version_from_file(file)
            if version <= current_version and version > target_version:
                files_to_run.append(file)

        files_to_run.reverse()
        return files_to_run

    def get_latest_version(self) -> int:
        """ Get latest version from migration up files"""
        files = self.get_migration_files('up')
        if len(files) == 0:
            return 0

        last_file = files[-1]
        version = int(last_file.split('.')[0])

        return version

    def get_migrate_up_statements(self, target_version=None) -> list:
        if not target_version:
            target_version = self.get_latest_version()

        up_files = self.get_up_files(target_version)
        statements = []
        for file in up_files:
            statements += self.get_sql_statements_from_file(
                self.migration_dir + '/up/' + file)

        return statements

    def get_migrate_down_statements(self, target_version=None) -> list:
        if not target_version:
            target_version = 0

        down_files = self.get_down_files(target_version)
        statements = []
        for file in down_files:
            statements += self.get_sql_statements_from_file(
                self.migration_dir + '/down/' + file)

        return statements

    def migrate_up(self, target_version=None):
        if not self.connection:
            raise Exception(
                'No connection. You will need to connect first. Use MySQLMigration.connect(*kwargs, **kwargs)')
        
        if not target_version:
            target_version = self.get_latest_version()

        statements = self.get_migrate_up_statements(target_version)
        for statement in statements:
            self.execute_query(statement)

        self.set_current_version(target_version)

    def migrate_down(self, target_version=None):
        if not self.connection:
            raise Exception(
                'No connection. You will need to connect first. Use MySQLMigration.connect(*kwargs, **kwargs)')

        if not target_version:
            target_version = 0
        
        statements = self.get_migrate_down_statements(target_version)
        for statement in statements:
            self.execute_query(statement)

        

        self.set_current_version(target_version)
