import sqlite3
import os
from pathlib import Path


class Database:
    '''
    SQLite Database for storing inventory.
    '''
    __PATH = f'{str(Path.home())}/.butter'
    __DB = f'{__PATH}/inventory.db'

    def __init__(self, table_name=None) -> None:
        if not os.path.exists(self.__PATH):
            os.mkdir(self.__PATH)
        self.__connnection = sqlite3.connect(self.__DB)
        self.__cursor = self.__connnection.cursor()
        self._table_name = table_name

    def create_table(self) -> None:
        'Create new table'
        sql = f'''
        CREATE TABLE {self._table_name} (
            hostname TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            port TEXT NOT NULL DEFAULT 22);
        '''
        self._execute(sql)

    def insert(self, hostname: str, username: str, port: str) -> None:
        'Insert new host details'
        sql = f'''
        INSERT INTO {self._table_name}
            VALUES(
                '{hostname}',
                '{username}',
                '{port}'
            );
        '''
        self._execute(sql)

    def drop_table(self) -> None:
        'Delete the table'
        sql = f'''
            DROP TABLE {self._table_name};
        '''
        self._execute(sql)

    def _execute(self, sql: str) -> None:
        'Execute the SQL query'
        try:
            self.__cursor.execute(sql)
        except Exception as e:
            print(f'Failed!\nException: {str(e)}')
        finally:
            self.__connnection.commit()

    def select(self) -> list:
        'select all the host'
        sql = f'''
            SELECT * FROM {self._table_name};
        '''
        if self.table_exists():
            try:
                return [row for row in self.__cursor.execute(sql)]
            except Exception as e:
                print(f'Failed!\nException: {str(e)}')
        else:
            return []

    def table_exists(self) -> bool:
        'Table existence check'
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        self.__cursor.execute(sql)
        present_tables = set(self.__cursor.fetchall())
        temp_table_name = (self._table_name,)
        if temp_table_name in present_tables:
            return True
        else:
            return False

    def all_tables(self) -> list:
        'Get all the tables'
        sql = "SELECT name FROM sqlite_master WHERE type='table';"
        self.__cursor.execute(sql)
        return [table_name_tuple[0] for table_name_tuple in self.__cursor.fetchall()]

    def delete(self, hostname: str):
        'Delete host from the table'
        sql = f'''
            DELETE FROM {self._table_name} WHERE hostname='{hostname}';
        '''
        try:
            self.__cursor.execute(sql)
        except Exception as e:
            print(f'Failed!\nException: {str(e)}')
        finally:
            self.__connnection.commit()

    def __del__(self) -> None:
        self.__connnection.commit()
        self.__connnection.close()


class Inventory(Database):
    '''
    Inventory management with SQLite3
    '''

    def __init__(self, name=None) -> None:
        super().__init__(name)

    def create(self) -> None:
        'Create new inventory'
        self.create_table()

    def add_host(self, hostname: str, username: str, port=22) -> None:
        'Add new host into a inventory'
        self.insert(hostname, username, port)

    def remove_host(self, hostname: str) -> None:
        'Remove a host from inventory'
        self.delete(hostname)

    def clear(self) -> None:
        'Delete a inventory'
        self.drop_table()

    def get_inventory_list(self) -> list:
        'Get list of host from inventory'
        return self.select()

    def get_inventory_dict(self) -> list:
        'Get list of host from inventory'
        data = []
        for row in self.select():
            data.append({
                'hostname': row[0],
                'username': row[1],
                'port': row[2]
            })
        return data

    def get_all_inventory(self) -> list:
        'Get list of inventory names'
        return self.all_tables()

    def get_hostnames(self) -> list:
        'Get the list of hostname in the inventory'
        return [row[0] for row in self.select()]
