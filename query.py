from typing import Dict, List, Tuple
import sqlite3

conn = sqlite3.connect("db.db")
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetch(table: str, filters: List[Tuple], columns: List = None):
    """
    Fetch entries from table table with Tuple filters
    :param table: Searched table
    :param filters: List of Tuples (column, filter)
    :param filters: List of columns to be fetched
    """
    columns_selected = ', '.join(columns) if columns is not None else '*'
    where_str = ' and '.join([f'{pair[0]} = {pair[1]}' for pair in filters])
    query = f'SELECT {columns_selected} from {table} WHERE {where_str}'
    cursor.execute(query)
    rows = cursor.fetchone()
    return rows


def update(table: str, id: int, updates: List[Tuple]):
    """Update entry in table where id = id"""
    update_list = ', '.join([f'{x[0]} = ?' for x in updates])
    placeholders = [x[1] for x in updates]
    query = f'UPDATE {table} SET {update_list} WHERE id = {id}'
    cursor.execute(query, placeholders)
    conn.commit()


if __name__ == '__main__':
    update('portfolios', 1, [('name', 'pizda')])
