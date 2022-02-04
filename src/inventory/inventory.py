# from database import Database
from src.inventory.database import Database


class Inventory:
    '''
    Inventory management with SQLite3
    '''

    def __init__(self, name=None) -> None:
        self.name = name
        self.inventory_db = Database(self.name)

    def create(self) -> None:
        self.inventory_db.create_table()

    def add_host(self, hostname: str, username: str, port=22) -> None:
        self.inventory_db.insert(hostname, username, port)

    def remove_host(self, hostname: str) -> None:
        self.inventory_db.delete(hostname)

    def clear(self) -> None:
        self.inventory_db.drop_table()

    def get_inventory_list(self) -> list:
        return self.inventory_db.select()

    def get_inventory_dict(self) -> list:
        data = []
        for row in self.inventory_db.select():
            data.append({
                'hostname': row[0],
                'username': row[1],
                'port': row[2]
            })
        return data

    def get_all_inventory(self) -> list:
        return self.inventory_db.all_tables()

    def get_hostnames(self) -> list:
        return [row[0] for row in self.inventory_db.select()]
