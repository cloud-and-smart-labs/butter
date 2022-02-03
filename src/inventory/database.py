import sqlite3


class Database:
    '''
    SQLite Database for storing inventory.
    '''

    def __init__(self, table_name: str) -> None:
        self.connnection = sqlite3.connect('inventory.db')
        self.cursor = self.connnection.cursor()
        self.table_name = table_name

    def create_table(self) -> None:
        sql = f'''
        CREATE TABLE {self.table_name} (
            hostname TEXT PRIMARY KEY, 
            username TEXT NOT NULL, 
            port TEXT NOT NULL DEFAULT 22);
        '''
        self.execute(sql)

    def insert(self, hostname: str, username: str, port: str) -> None:
        sql = f'''
        INSERT INTO {self.table_name} 
            VALUES(
                '{hostname}', 
                '{username}', 
                '{port}'
            );
        '''
        self.execute(sql)

    def drop_table(self) -> None:
        sql = f'''
            DROP TABLE {self.table_name};
        '''
        self.execute(sql)

    def execute(self, sql: str) -> None:
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f'Failed!\nException: {str(e)}')
        finally:
            self.connnection.commit()

    def select(self) -> list:
        sql = f'''
            SELECT * FROM {self.table_name};
        '''
        try:
            return [row for row in self.cursor.execute(sql)]
        except Exception as e:
            print(f'Failed!\nException: {str(e)}')

    def delete(self, hostname: str):
        sql = f'''
            DELETE FROM {self.table_name} WHERE hostname='{hostname}';
        '''
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f'Failed!\nException: {str(e)}')
        finally:
            self.connnection.commit()

    def __del__(self) -> None:
        self.connnection.commit()
        self.connnection.close()
