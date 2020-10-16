import sqlite3


class DatabaseManager:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name, columns):
        column_types = [f"{col_name} {data_type}" for col_name, data_type in columns.items()]
        column_string = ', '.join(column_types)
        sql_string = f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({column_string});
            """
        self._execute(sql_string)

    def add(self, table_name, data):
        place_holders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())

        sql_string = f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({place_holders});
            """
        self._execute(sql_string, values=column_values)

    def delete(self, table_name, criteria):
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        criteria_string = ' AND '.join(placeholders)
        sql_string = f"""
            DELETE FROM {table_name}
            WHERE {criteria_string}
            """
        self._execute(sql_string, tuple(criteria.values()))

    def select(self, table_name, criteria=None, order_by=None):
        criteria = criteria or {}
        sql_string = f"SELECT * FROM {table_name}"
        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            criteria_string = ' AND '.join(placeholders)
            sql_string += f" WHERE {criteria_string}"
        if order_by:
            sql_string += f" ORDER BY {order_by}"
        return self._execute(sql_string, tuple(criteria.values()))
