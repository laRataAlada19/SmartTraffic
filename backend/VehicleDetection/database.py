import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection:
            print("Conexão não estabelecida. Chame o método connect() primeiro.")
            return None
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados encerrada.")