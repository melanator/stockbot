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


def fetch(table: str, filters: List[Tuple]):
    """
    Fetch entries from table table with Tuple filters
    :param table: Searched table
    :param filters: List of Tuples (column, filter)
    :return:
    """
    where_l = []
    for pair in filters:
        where_l.append(f'{pair[0]} = {pair[1]}')
    where_str = ' and '.join(where_l)
    query = f'SELECT * from {table} WHERE {where_str}'

    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


if __name__ == '__main__':
    print(fetch('holders', [('id', 227627486)]))
