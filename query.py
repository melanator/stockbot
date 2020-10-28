from typing import Dict, List, Tuple
import sqlite3

conn = sqlite3.connect("db.db")
cursor = conn.cursor()


def insert(table: str, **values_dict):
    """
    Inserts new entry to table with values in **values_dict
    """
    columns = ', '.join(values_dict.keys())
    values = [_ for _ in values_dict.values()]
    placeholders = ", ".join( "?" * len(values_dict.keys()) )
    cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
    conn.commit()


def fetch(table: str, columns: List = None, **filters):
    """
    Fetch entries from table table with Tuple filters
    :param table: Searched table
    :param **filters: Filters
    :param columns: List of columns to be fetched
    """
    columns_selected = ', '.join(columns) if columns is not None else '*'
    where_str = ' and '.join([f'{k} = ?' for k in filters.keys()])
    values = [_ for _ in filters.values()]
    query = f'SELECT {columns_selected} from {table} WHERE {where_str}'
    cursor.execute(query, values)
    rows = cursor.fetchmany()
    return rows


def update(table: str, id: int, **updates):
    """Update entry in table where id = id"""
    update_list = ', '.join([f'{x} = ?' for x in updates.keys()])
    placeholders = [x for x in updates.values()]
    query = f'UPDATE {table} SET {update_list} WHERE id = {id}'
    cursor.execute(query, placeholders)
    conn.commit()


if __name__ == '__main__':
    pass
