import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG
from datetime import datetime


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
    
    def save_results_to_bd(self, video_file, detected_vehicles, class_counter, total_class_counter):
        try:
            query = "INSERT INTO vehicle_counts(timestamp,total_vehicles,car,motorcycle,bike,truck,bus) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            self.connect()

            for vehicle_type, count in class_counter.items():
                total_class_counter[vehicle_type] += count

            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_detection = len(detected_vehicles)
            params = (
                current_timestamp, 
                total_detection,
                class_counter.get("car", 0),
                class_counter.get("motorcycle", 0),
                class_counter.get("bike", 0),
                class_counter.get("truck", 0),
                class_counter.get("bus", 0),
            )
            self.execute_query(query, params)
            self.close()
            print("Resultados salvos no banco de dados com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar resultados no banco de dados: {e}")