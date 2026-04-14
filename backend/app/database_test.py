# app/database_test.py
import sqlite3

class TestDB:
    def __init__(self, conn):
        self.conn = conn

    def execute_query(self, query, params=None):
        cur = self.conn.cursor()
        try:
            if params:
                modified_query = query.replace('%s', '?')
            else:
                modified_query = query
            cur.execute(modified_query, params or ())
            
            if modified_query.strip().upper().startswith('SELECT') or 'RETURNING' in modified_query.upper():
                rows = cur.fetchall()
                if rows:
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in rows]
                return []
            else:
                self.conn.commit()
                return []
        finally:
            cur.close()

def get_test_db(connection):
    return TestDB(connection)